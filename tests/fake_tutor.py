"""Todo lo que finge ser Claude durante los tests, en un solo sitio.

Hasta [T-076] este archivo no hacía falta: `judge_grammar` era `FAKE_VERDICT`,
una constante, y los tests la importaban. Desde que la función llama de verdad a
la API hay que fingir a Claude, y fingirlo bien es más trabajo que una constante.

🚨 **Y no es opcional: `tests/no_network.py` cierra la red en TODA la suite**
([C-001]). Un test que llegara a la API de verdad no gastaría dinero — se
pondría rojo. Pero se pondría rojo por el motivo equivocado, y por eso todo lo
que finge vive aquí y no repartido por los archivos de tests.

Dos piezas, para dos clientelas distintas:

1. **`STUB_VERDICT` y el maniquí de `judge_grammar`** — para quien prueba lo que
   hay *alrededor* del juez (la API, el agente). A esos no les importa qué dice
   el veredicto, solo que haya uno.
2. **`FakeClient` y sus constructores** — para quien prueba el juez *por dentro*
   (`tests/test_tools.py`): qué manda, cómo lee la respuesta y qué hace cuando
   el SDK revienta. Ese cliente entra por el parámetro `client` de
   `judge_grammar`, que existe exactamente para esto ([D-052]).
"""

from dataclasses import dataclass, field

import anthropic
import httpx

# Lo que contesta el maniquí. Es texto plano y en inglés como el veredicto de
# verdad (PI-5: lo que ve quien usa la app va en inglés), pero **no imita** a
# ningún veredicto real: nadie debe leerlo y creer que salió de un modelo.
STUB_VERDICT = "Nice sentence. Keep going."


# ── Fingir la RESPUESTA del modelo ────────────────────────────────────────


@dataclass
class FakeBlock:
    """Un trozo de la respuesta. El de verdad trae `type` y, si es texto, `text`.

    🔑 Que el bloque de pensamiento NO tenga texto no es un descuido de este
    maniquí: es lo que hace Opus 5. Devuelve el bloque, pero el razonamiento
    crudo no viaja dentro. `judge_grammar` filtra por `type == "text"` justo por
    esto, y aquí es donde se comprueba.
    """

    type: str
    text: str = ""


@dataclass
class FakeUsage:
    """El contador de la factura que viene DENTRO de la respuesta.

    🔑 **Las cifras exactas dan igual; lo que decide es cero o no cero.** No
    imitan a ninguna medida real: sirven para distinguir "esto se facturó" de
    "esto no costó nada", que es lo único que [D-055] pregunta.
    """

    input_tokens: int
    output_tokens: int


@dataclass
class FakeAnswer:
    """Lo que devuelve `client.messages.create(...)`.

    Solo lleva los tres campos que `judge_grammar` mira: `content`,
    `stop_reason` y `usage`. Si algún día mira un cuarto, este maniquí se pone
    rojo con un `AttributeError` — que es lo que se quiere, no que invente el
    dato.

    🚨 **El `usage` por defecto viene FACTURADO, y es deliberado.** Es la regla
    de [D-051] metida en el valor por defecto: ante la duda se cobra. Una
    respuesta que no costó nada tiene que decirlo a propósito, escribiendo los
    ceros; olvidarse falla del lado seguro.
    """

    content: list[FakeBlock]
    stop_reason: str = "end_turn"
    usage: FakeUsage = field(
        default_factory=lambda: FakeUsage(input_tokens=20, output_tokens=5)
    )


# ── Fingir el CLIENTE ─────────────────────────────────────────────────────


@dataclass
class _FakeMessages:
    """El `client.messages` de mentira: contesta o revienta, y toma nota."""

    answer: FakeAnswer | None = None
    error: Exception | None = None
    calls: list[dict] = field(default_factory=list)

    def create(self, **kwargs):
        # Se apunta la llamada ANTES de decidir qué hacer. Un test que comprueba
        # "la petición sí salió" necesita saberlo también cuando falla.
        self.calls.append(kwargs)

        if self.error is not None:
            raise self.error

        return self.answer


class FakeClient:
    """Un `anthropic.Anthropic` de mentira, con la única puerta que se usa.

    ⚠️ **A propósito NO hereda de `anthropic.Anthropic`.** Heredar obligaría a
    construir el cliente de verdad —y con él, a tener una llave— para poder
    fingirlo. Aquí basta con tener `.messages.create()`, que es todo lo que
    `judge_grammar` toca.
    """

    def __init__(self, answer=None, error=None):
        self.messages = _FakeMessages(answer=answer, error=error)

    @property
    def calls(self) -> list[dict]:
        """Las llamadas recibidas, en orden. Cada una, los `kwargs` tal cual."""
        return self.messages.calls


def answering(text: str, stop_reason: str = "end_turn") -> FakeClient:
    """Un cliente que contesta ese texto, como lo contestaría el modelo."""
    return FakeClient(FakeAnswer([FakeBlock("text", text)], stop_reason))


def answering_blocks(*blocks: FakeBlock, stop_reason: str = "end_turn") -> FakeClient:
    """Un cliente que contesta esos trozos exactos. Para probar el filtrado."""
    return FakeClient(FakeAnswer(list(blocks), stop_reason))


def refusing_before_output() -> FakeClient:
    """El rechazo del clasificador ANTES de generar nada: la factura en CERO.

    🚨 Este es el caso que [D-054] declara **gratis**, y lo dice el propio
    contador: ni tokens de entrada, ni de salida, ni cuota de la API. La cuota
    del día se devuelve.
    """
    return FakeClient(
        FakeAnswer(
            [],
            stop_reason="refusal",
            usage=FakeUsage(input_tokens=0, output_tokens=0),
        )
    )


def refusing_after_output() -> FakeClient:
    """El rechazo a MITAD de la respuesta: hay bloques, pero no texto útil.

    🚨 El hermano tramposo del de arriba, y el que separa [D-054] de la regla
    más corta *"si es rechazo, devuelve"*. Aquí ya se generó algo, así que **se
    cobra**. Mismo `stop_reason`, decisión contraria.
    """
    return FakeClient(
        FakeAnswer([FakeBlock("thinking")], stop_reason="refusal")
    )


def refusing_mid_output_without_partial() -> FakeClient:
    """El rechazo a mitad **sin streaming**: se facturó, y el parcial no viene.

    🚨 **Este es el caso que tumbó al proxy de [D-054], y es real, no teórico.**
    Comprobado en la documentacion de Anthropic el 2026-08-10: sin streaming
    —que es como llama `judge_grammar`— un rechazo a mitad **omite el parcial**.
    Llega entonces con `content` vacio y `stop_reason="refusal"`, *idéntico por
    fuera* al rechazo gratis de arriba... pero con los tokens ya pagados.

    🔑 Mirar `content` los confunde; mirar `usage` los separa. Ver [D-055].
    """
    return FakeClient(FakeAnswer([], stop_reason="refusal"))


def failing(error: Exception) -> FakeClient:
    """Un cliente que revienta con esa excepción en vez de contestar."""
    return FakeClient(error=error)


# ── Fingir los FALLOS del SDK ─────────────────────────────────────────────
#
# 🚨 Las excepciones de `anthropic` no se construyen con un mensaje a secas:
# piden la petición o la respuesta HTTP que las causó. Se fabrican aquí para que
# ningún test tenga que saber esto, y para que el día que el SDK cambie de forma
# se arregle en un sitio y no en quince.

_REQUEST = httpx.Request("POST", "https://api.anthropic.com/v1/messages")


def _response(status_code: int) -> httpx.Response:
    return httpx.Response(status_code, request=_REQUEST)


def timeout_error() -> anthropic.APITimeoutError:
    """Se agotó el reloj de `TIMEOUT_SECONDS`. La petición SÍ salió ([D-051])."""
    return anthropic.APITimeoutError(request=_REQUEST)


def connection_error() -> anthropic.APIConnectionError:
    """No hubo ni conexión. La petición NUNCA salió ([D-051])."""
    return anthropic.APIConnectionError(message="sin red", request=_REQUEST)


def auth_error() -> anthropic.AuthenticationError:
    """401: la llave no vale. Rechazado en la puerta, cero tokens."""
    return anthropic.AuthenticationError(
        "llave invalida", response=_response(401), body=None
    )


def rate_limit_error() -> anthropic.RateLimitError:
    """429: frenados en la puerta. Cero tokens."""
    return anthropic.RateLimitError(
        "demasiadas peticiones", response=_response(429), body=None
    )


def server_error() -> anthropic.InternalServerError:
    """500: falló Anthropic con la frase ya dentro. Los tokens ya se pagaron."""
    return anthropic.InternalServerError(
        "algo se rompio", response=_response(500), body=None
    )


# ── El maniquí de `judge_grammar` ─────────────────────────────────────────


def install(monkeypatch, verdict: str = STUB_VERDICT) -> list[str]:
    """Sustituye `judge_grammar` en `english_tutor` y devuelve las frases vistas.

    🔑 **Se parchea en `app.english_tutor`, no en `app.tools`**, y no da igual:
    `english_tutor.py:10` hace `from app.tools import judge_grammar`, así que se
    quedó con **su propia referencia** a la función. Cambiar la de `app.tools`
    no cambiaría la que el agente ya tiene en la mano.

    La lista que devuelve sirve para lo que más se comprueba en `test_api.py`:
    **que el tutor NO se entere.** Un freno que corta antes de gastar dinero se
    demuestra viendo que aquí no llegó nada.
    """
    from app import english_tutor

    seen: list[str] = []

    def stub(sentence: str) -> str:
        seen.append(sentence)
        return verdict

    monkeypatch.setattr(english_tutor, "judge_grammar", stub)

    return seen
