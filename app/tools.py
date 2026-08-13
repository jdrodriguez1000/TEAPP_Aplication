"""Las tres herramientas del tutor.

Cada una hace un trabajo distinto, y ninguna sabe que las otras existen. Esa
independencia es lo que permite cambiar una sin tocar las demás — y quedó
demostrado en [T-076]: `judge_grammar` se reescribió entera, de un veredicto de
mentira a una llamada real a Claude, y las otras dos ni se enteraron.
"""

import json
import os
import re
import tempfile
import threading
from dataclasses import dataclass
from pathlib import Path

import anthropic

from app import config

# Dónde viven los marcadores: uno por persona, `<raiz>/users/<nombre>.json`.
# `data/` no va a Git: son datos de quien usa la app.
#
# 🚨 **La raíz ya no se calcula aquí: la da `config.users_dir()`, y sale de
# `TEAPP_DATA_DIR`.** Antes era `PROJECT_ROOT / "data" / "users"` resuelta en
# este archivo, con la carpeta real como valor por defecto — así que cualquier
# script que importara esto y se olvidara de desviarla escribía en los datos de
# personas de verdad. Es lo que pasó ([L-023]) y lo que arregla [D-037].
#
# 🔑 Antes esto era UN archivo para todo el mundo. Mientras hubo terminal era
# verdad —habia una sola persona—; desde que hay servidor era mentira, y de las
# que no dan error: dos personas veian subir el mismo numero.

# ── El juez de gramática ──────────────────────────────────────────────────

# 🎯 El modelo, y por qué el CARO. Ver [D-049]: el paso 8 estrena el veredicto
# real, y arrancar con un modelo pequeño metería dos sospechosos a la vez —la
# rúbrica y el modelo— el día que hay que juzgar la rúbrica. Con Opus, un
# veredicto malo solo puede acusar a la rúbrica. Bajar a Sonnet o Haiku es
# trabajo MEDIDO del paso 9, no una corazonada de hoy.
MODEL_NAME = "claude-opus-5"

# 🚨 `effort` no es un adorno de ahorro: es lo que hace viable [D-049].
# Claude Opus 5 **piensa por defecto**, y esos tokens de razonamiento se cobran
# como salida Y consumen reloj. Sin acotarlos, el pensamiento se come el timeout
# de 10 s de [A-011] y convierte veredictos correctos en peticiones perdidas.
#
# ⚠️ Y no se apaga del todo (`thinking={"type": "disabled"}`), aunque a este
# `effort` la API lo aceptaria: con el pensamiento apagado, la documentacion de
# Anthropic registra que a Opus 5 se le escapan etiquetas `<thinking>` DENTRO de
# la respuesta visible — y esa respuesta va al navegador.
EFFORT = "low"

# El techo de la respuesta. 🚨 Cuenta el pensamiento Y el texto juntos, asi que
# no es "cuanto puede escribir": es cuanto puede pensar mas cuanto puede
# escribir. Ajustado a la cifra justa, el veredicto sale cortado por la mitad.
MAX_TOKENS = 1000

# 🚨 **Cero reintentos, y es deliberado.** El SDK reintenta DOS veces por su
# cuenta ante un 429 o un 500, con esperas crecientes. Tres intentos no caben en
# los 10 s de [A-011]: lo que se veria seria el 504 del timeout, con el error de
# verdad escondido detras. Quien manda en el reloj es `api.py`, no el SDK.
MAX_RETRIES = 0

# 🚨 **El reloj del cliente, y sin el la pieza de arriba no sirve de nada.**
# Comprobado en la documentacion del SDK de Python el 2026-08-10, no recordado:
# **el timeout por defecto son DIEZ MINUTOS.** Sesenta veces el presupuesto de
# [A-011].
#
# 🔑 **Son DOS frenos distintos, y no se sustituyen** — lo dice el propio
# comentario de `api.py:130`, escrito el 4 de agosto: el de alli acota **lo que
# espera quien pregunta**; este acota **lo que espera el servidor**. Sin este,
# a los 10 s quien pregunta recibe su 504 y se va, pero el hilo que le atendia
# sigue esperando aqui dentro hasta diez minutos, ocupando su sitio del pool.
# Con Anthropic atascado los hilos se acumulan y el servidor deja de atender
# **sin que haya fallado nada**. Ver [D-054].
#
# ⚠️ **8.0 sigue siendo una ESTIMACION, no una medida** (regla 6), y eso NO ha
# cambiado: nadie ha cronometrado el peor caso de Opus 5. Lo unico medido es una
# tanda de diez el 2026-08-11 —1,72 / 3,33 / 4,72 s ([L-043])—, y el maximo de
# diez muestras no es la cola de la distribucion.
#
# 🔑 **Pero desde [D-070] este numero ya no es solo una estimacion: es el TECHO
# del que cuelga el reloj de la ruta.** Los 10 s de api.py son correctos *porque*
# aqui hay un 8,0 que no deja pasar de ahi. Subirlo por encima de 10 no alarga la
# espera: se la come el otro, y el error de verdad se esconde tras un 504 mudo.
#
# Va por debajo de los 10 s a proposito, por el mismo motivo que MAX_RETRIES = 0:
# que el primero en rendirse sea el cliente. Lo vigila
# `test_the_client_timeout_is_shorter_than_the_one_in_the_api`.
TIMEOUT_SECONDS = 8.0

# La rúbrica: lo que el modelo tiene que hacer, y con qué tono.
#
# 🔑 **En inglés porque es lo que el modelo lee para escribir en inglés.** Es la
# regla PI-5 aplicada con cuidado: el veredicto lo lee quien usa la app, así que
# es interfaz. Los comentarios de alrededor —esto— son explicación, y van en
# español.
#
# 🚨 **A1 y tono positivo salen de `scope.md`, no de mi criterio.** Los "tres
# temas" que nombra el alcance no estan escritos en ninguna parte, asi que la
# rubrica NO los inventa: juzga la frase que llegue.
#
# ⚠️ Se le prohíbe el markdown a propósito: la pantalla pinta este texto tal
# cual, así que unos asteriscos llegarían al navegador como asteriscos.
GRAMMAR_RUBRIC = """You are a warm, encouraging English tutor for A1 beginners.

Judge ONLY the grammar of the sentence the learner wrote.

- If it is correct, say so briefly and warmly.
- If it is not, give the corrected sentence and name the one mistake that
  matters most, in simple words a beginner understands.
- Never correct more than one thing at a time. A1 learners give up when a
  reply is a list of everything they did wrong.
- Never comment on the topic, the spelling of names, or how interesting the
  sentence is. Only grammar.

Your reply MUST have two parts:

1. A first line with ONE word and nothing else: OK if the sentence is
   grammatically correct, FIX if it is not.
2. Then, on the following lines, your reply for the learner.

Never mention OK or FIX inside your reply for the learner: that first line is
for the program, not for them.

Write the learner's part in English, in at most two short sentences. Plain
text only: no markdown, no bullet points, no asterisks, no quotation marks
around the correction."""

# Las dos palabras que puede traer la primera línea. Se comparan en mayúsculas
# y sin espacios alrededor: el modelo escribe texto, no rellena un formulario.
VERDICT_CORRECT = "OK"
VERDICT_WRONG = "FIX"


@dataclass(frozen=True)
class GrammarVerdict:
    """Lo que el juez contesta: el fallo y el mensaje, separados.

    🔑 **Antes esto era un `str` y ahí estaba el problema.** El texto del juez
    lo entiende una persona, no un programa: `respond` no podía leer "Nice
    sentence" y deducir que la frase estaba bien. Contar aciertos ([D-066])
    obliga a que el veredicto viaje en algo que una máquina lea, y `correct` es
    exactamente eso.

    🔑 **Y van separados por la misma razón que en `TutorReply`:** quien muestre
    la respuesta nunca debe ver la palabra clave. `message` es lo que se pinta
    en la pantalla, ya limpio; `correct` es lo que decide si sube el marcador.
    Juntos en una cadena, quien la imprimiera enseñaría el `OK` al estudiante.

    `frozen=True` los deja de solo lectura: una vez juzgada, nadie cambia la
    frase por el camino.
    """

    correct: bool  # ¿estaba bien la frase? Lo lee `respond` para sumar o no
    message: str  # lo que se le enseña a quien practica, sin la palabra clave


class TutorUnavailableError(Exception):
    """No se pudo conseguir un veredicto del modelo.

    Excepción propia por la misma razón que `ScoreFileError`: `api.py` tiene que
    poder distinguir "el juez no contestó" de cualquier otro fallo, y una
    excepción del SDK de Anthropic no le dice eso — le dice que algún HTTP, en
    algún sitio, salió mal.

    🚨 **`request_sent` es la decisión [D-051] viajando dentro del error.** Dice
    si la petición llegó a salir de casa:

    - `False` → nunca salió (llave mala, red caída, 429). Cero tokens gastados,
      así que la cuota del día se DEVUELVE.
    - `True` → sí salió (500 de Anthropic, saturación, timeout). Los tokens de
      entrada ya se pagaron, así que se COBRA.

    🔑 Va aquí y no en `api.py` porque el único sitio donde se sabe si salió es
    donde se cazó la excepción del SDK. Que `api.py` lo dedujera del tipo de
    error sería la misma verdad escrita dos veces, y una de las dos acabaría
    mintiendo.
    """

    # Los mensajes van sin tildes a proposito (ver [L-001]).

    def __init__(self, message: str, request_sent: bool) -> None:
        super().__init__(message)
        self.request_sent = request_sent


# El candado del marcador. Quien quiera sumar un punto pasa por aqui, de uno en
# uno. En la terminal no hacia falta: habia una sola persona escribiendo. Desde
# que hay servidor, dos peticiones llegan a la vez de verdad.
#
# ⚠️ Vale dentro de UN proceso. Si uvicorn se lanzara con `--workers 2` serian
# dos procesos con un candado cada uno, y no se enterarian el uno del otro. Ver
# la suposicion [A-002].
#
# 🔑 Con un archivo por persona ese riesgo ENCOGE, no desaparece. Dos personas
# distintas en dos procesos distintos ya no se pisan: escriben en archivos
# distintos. Lo que queda es la MISMA persona dos veces a la vez —dos pestañas,
# dos dispositivos— cayendo en procesos distintos.
_SCORE_LOCK = threading.Lock()

# ── Las reglas del nombre ─────────────────────────────────────────────────
#
# 🚨 El nombre llega del navegador, y con el se construye una RUTA DE ARCHIVO.
# Sin frenos, quien usa la app elige a que archivo escribe el servidor: manda
# `../../CLAUDE.md` y el marcador aterriza fuera de `data/`.
#
# Por eso se sigue el criterio de `_context/architecture.md`: **denegar por
# defecto**. No se hace lista de lo prohibido —siempre falta algo— sino lista de
# lo PERMITIDO, y todo lo demas se rechaza.

# Solo minusculas, numeros, guion y guion bajo. Ni puntos (adios `..`), ni
# barras (adios `../`), ni espacios, ni tildes, ni nada fuera del ASCII.
USER_PATTERN = re.compile(r"^[a-z0-9_-]+$")

# Un nombre no puede ser infinito: al ponerle `.json` detras acabaria pasandose
# del limite del sistema de archivos, y eso revienta al escribir, no al validar.
MAX_USER_LENGTH = 32

# ⚠️ Windows reserva estos nombres para dispositivos, y los reserva **con
# cualquier extension**: `con.json` sigue siendo el dispositivo, no un archivo.
# Se cuelan enteros por la lista blanca de arriba, porque son letras y numeros.
# 🔑 Validar los caracteres no es validar el nombre.
WINDOWS_RESERVED_NAMES = frozenset(
    {"con", "prn", "aux", "nul"}
    | {f"com{digit}" for digit in range(1, 10)}
    | {f"lpt{digit}" for digit in range(1, 10)}
)


class InvalidUserError(Exception):
    """El nombre de la persona no sirve para nombrar un archivo.

    Excepción propia, y no `ValueError`, por la misma razón que
    `ScoreFileError`: FastAPI tiene que poder distinguir "el nombre no vale"
    —culpa de quien pregunta, 422— de cualquier otro fallo.
    """

    # Los mensajes van sin tildes a propósito (ver [L-001]).


class ScoreFileError(Exception):
    """El archivo del marcador existe, pero no se puede entender.

    Es una excepción propia del proyecto, y no la de `json`, a propósito. En el
    paso 2 FastAPI tiene que poder distinguir "el marcador está roto" de
    cualquier otro fallo, y un `JSONDecodeError` no le dice eso: le dice que
    algún JSON, en algún sitio, no se pudo leer.

    ⚠️ Solo para el archivo ROTO. Que el archivo no exista no es un error: es
    el primer día de esa persona, y el marcador vale 0.
    """

    # Los mensajes van sin tildes a propósito: acaban impresos en la terminal, y
    # la consola de Windows no sabe pintar nada fuera de ASCII (ver [L-001]).


def count_words(sentence: str) -> int:
    """Cuenta las palabras de una frase. Python puro, sin modelo.

    Contar tiene una sola respuesta correcta, así que no se le pregunta al
    modelo: se calcula. `split()` sin argumentos parte por cualquier espacio en
    blanco —espacios, saltos de línea, tabulaciones— y descarta los huecos
    vacíos, así que los espacios de más no cuentan.

    🔑 Si no llega un texto, se avisa; no se convierte. Hoy `main.py` siempre
    manda texto, pero en el paso 2 FastAPI recibe JSON de internet y por ahí
    entra un numero, un `null` o una lista. Hacer `str(sentence)` por nuestra
    cuenta taparia el problema: contaria "4" como una palabra y devolveria 1,
    tan campante. El problema estaria antes, y nadie se enteraria.

    :raises TypeError: si lo que llega no es un `str`.
    """
    if not isinstance(sentence, str):
        raise TypeError(
            f"count_words esperaba un texto (str) y recibio "
            f"{type(sentence).__name__}: {sentence!r}"
        )

    return len(sentence.split())


def judge_grammar(
    sentence: str, client: anthropic.Anthropic | None = None
) -> GrammarVerdict:
    """Juzga la gramática de una frase preguntándole a Claude. Con rúbrica.

    Esta es la única pieza del proyecto que no responde igual dos veces, y la
    única que cuesta dinero cada vez que corre.

    🚨 **El cliente se construye AQUÍ DENTRO, no en la firma ni al importar.**
    Es la lección de `score_file` otra vez: Python evalúa los valores por
    defecto **una sola vez, al importar el módulo**, así que un cliente en la
    firma se quedaría con la llave de aquel momento para siempre — y los tests
    no podrían desviarlo. Preguntando en cada llamada, cambiar el entorno cambia
    de verdad a quién se le pregunta. Mismo motivo que [D-036].

    🔑 **Y por eso `client` es un parámetro opcional.** No es configurabilidad
    que nadie pidió (PI-2): es lo único que hace posible probar esta función.
    `tests/no_network.py` cierra la red en TODA la suite ([C-001]), así que un
    test **no puede** llamar a Claude de verdad — tiene que meter un cliente
    falso por esta puerta. Misma forma que `users_dir` en `score_file`.

    🔑 **Devuelve `GrammarVerdict`, no texto.** El fallo y el mensaje viajan
    separados desde [D-066]: uno lo lee `respond` para decidir si sube el
    marcador, el otro lo lee quien practica. Cómo llega ese fallo desde el
    modelo —una primera línea fija— es [D-067], y está explicado en
    `split_verdict`.

    :raises TypeError: si lo que llega no es un `str`. Igual que en
        `count_words`: por la red entra un numero, un `null` o una lista.
    :raises TutorUnavailableError: si no se consiguió veredicto. Lleva
        `request_sent` encima para decidir si la cuota se devuelve ([D-051]).
    """
    if not isinstance(sentence, str):
        raise TypeError(
            f"judge_grammar esperaba un texto (str) y recibio "
            f"{type(sentence).__name__}: {sentence!r}"
        )

    # ⚠️ **Los dos frenos viven en el CONSTRUCTOR, no en esta funcion.** Un
    # cliente que llegue por el parametro trae los suyos, y `[D-053]` y `[D-054]`
    # no le aplican. Hoy no muerde —el unico que inyecta es la suite de tests, y
    # `api.py` llama sin cliente—, pero decir "judge_grammar tiene 8 segundos"
    # solo es cierto por este camino.
    if client is None:
        client = anthropic.Anthropic(
            api_key=config.require_anthropic_key(),
            max_retries=MAX_RETRIES,
            timeout=TIMEOUT_SECONDS,
        )

    try:
        answer = client.messages.create(
            model=MODEL_NAME,
            max_tokens=MAX_TOKENS,
            system=GRAMMAR_RUBRIC,
            output_config={"effort": EFFORT},
            messages=[{"role": "user", "content": sentence}],
        )
    # 🚨 **EL ORDEN DE ESTOS `except` ES LA DECISION [D-051], NO ESTILO.**
    #
    # `APITimeoutError` HEREDA de `APIConnectionError` — comprobado en el SDK
    # 0.121.0 el 2026-08-10, no recordado. Python se queda con el primer `except`
    # que encaje, asi que si el de la red fuera primero, un timeout entraria por
    # ahi y DEVOLVERIA la cuota. Un timeout significa que la peticion si salio y
    # los tokens ya se pagaron: devolverla seria regalar cuota en el unico caso
    # que [D-051] decidio cobrar. Reordenar estas lineas rompe la decision **sin
    # romper la sintaxis**, que es la clase de fallo que este proyecto persigue.
    #
    # Lo vigila `test_timeout_no_devuelve_cuota`. Un comentario solo protege a
    # quien lo lee.
    except anthropic.APITimeoutError as error:
        raise TutorUnavailableError(
            f"El tutor no contesto a tiempo: {error}", request_sent=True
        ) from error
    except anthropic.APIConnectionError as error:
        # No hubo ni conexion: la peticion nunca salio, no se gasto un token.
        raise TutorUnavailableError(
            f"No se pudo conectar con el tutor: {error}", request_sent=False
        ) from error
    except (
        anthropic.AuthenticationError,   # 401: la llave no vale
        anthropic.PermissionDeniedError,  # 403: la llave no llega a este modelo
        anthropic.NotFoundError,          # 404: el nombre del modelo esta mal
        anthropic.RateLimitError,         # 429: frenados en la puerta
    ) as error:
        # Los cuatro se rechazan ANTES de mirar la frase: cero tokens.
        raise TutorUnavailableError(
            f"El tutor rechazo la peticion: {error}", request_sent=False
        ) from error
    except anthropic.APIStatusError as error:
        # 🚨 **La red de seguridad, y cobra.** Aqui caen los 500 y el 529 de
        # saturacion —que si gastaron tokens de entrada— y tambien cualquier
        # codigo que Anthropic estrene mañana y que nadie haya clasificado.
        # Ante la duda se COBRA: es denegar por defecto (regla 3) aplicado al
        # dinero. Equivocarse cobrando cuesta una practica de 20; equivocarse
        # devolviendo deja el freno abierto de par en par.
        raise TutorUnavailableError(
            f"El tutor fallo ({error.status_code}): {error}", request_sent=True
        ) from error

    # 🔑 **La respuesta llega en TROZOS, no en un texto.** Con el pensamiento
    # encendido, el primer trozo puede ser un bloque `thinking` —vacio, porque
    # Opus 5 no devuelve el razonamiento crudo— y coger `content[0]` a ciegas
    # devolveria una cadena vacia al navegador. Se busca el trozo de texto.
    verdict = "".join(
        block.text for block in answer.content if block.type == "text"
    ).strip()

    if not verdict:
        # Aqui caen varias causas distintas —se acabaron los tokens, el
        # clasificador rechazo la peticion— y [D-051] las cobra distinto. La
        # pregunta que hay que contestar es una sola: **¿esto costo dinero?**
        #
        # 🚨 **Y no se deduce: viene escrita en la respuesta.** Comprobado en la
        # documentacion de Anthropic el 2026-08-10, no recordado: un rechazo que
        # salta ANTES de generar nada **no se factura en absoluto** — ni
        # entrada, ni salida, ni cuota de la API — y `usage` lo dice con ceros.
        # Cobrarlo le quitaria a alguien una practica de sus 20 por algo que no
        # costo un centimo.
        #
        # 🔑 **Antes esto se deducia de `content` vacio, y esa deduccion fallaba.**
        # La misma documentacion registra que **sin streaming** —que es como
        # llama esta funcion— un rechazo a MITAD omite el parcial. Ese caso llega
        # con `content` vacio y los tokens ya pagados: por fuera es identico al
        # rechazo gratis, y el proxy devolvia cuota justo donde [D-051] manda
        # cobrar. El contador los separa; la forma de `content` no. Ver [D-055].
        #
        # ⚠️ Estos dos campos son la factura entera porque este proyecto no usa
        # cache. Si algun dia se usara, habria que sumar los tokens de cache.
        tokens_billed = (
            answer.usage.input_tokens > 0 or answer.usage.output_tokens > 0
        )
        raise TutorUnavailableError(
            "El tutor contesto sin texto (se quedo sin tokens o rechazo la "
            f"peticion: stop_reason={answer.stop_reason}).",
            request_sent=tokens_billed,
        )

    return split_verdict(verdict)


def split_verdict(answer: str) -> GrammarVerdict:
    """Parte la respuesta del modelo en fallo y mensaje. Es [D-067] en código.

    La rúbrica pide abrir con una línea de una sola palabra: `OK` si la frase
    estaba bien, `FIX` si no. Aquí se lee esa línea, se **recorta**, y lo que
    queda es lo único que verá quien practica.

    🚨 **Denegar por defecto, y esto no es estilo: es la regla 3 aplicada al
    marcador.** Lo que devuelve el modelo es texto generado, no un contrato:
    puede saltarse el formato, y algún día lo hará. Cuando la primera línea no
    sea exactamente `OK`, **no hay acierto**. Equivocarse así cuesta un punto no
    sumado; al revés regalaría aciertos, y un marcador que regala deja de
    significar nada — que es justo lo que [D-066] vino a arreglar.

    🔑 **Y si el formato falla, el mensaje se muestra ENTERO igual.** Un fallo
    de formato es problema del programa, no de quien está practicando: dejarlo
    sin respuesta le cobraría a él un error nuestro. Se queda sin el punto, pero
    ve su corrección.

    Está aparte de `judge_grammar` a propósito: partir texto no necesita red ni
    llave, así que se puede probar con cadenas sueltas, sin fingir a Claude.
    """
    first_line, _, rest = answer.partition("\n")
    message = rest.strip()

    # Sin nada detrás de la palabra clave no hay mensaje que enseñar, así que
    # esto no cuenta como formato bien puesto: se trata como respuesta suelta.
    if not message:
        return GrammarVerdict(correct=False, message=answer.strip())

    head = first_line.strip().upper()

    if head == VERDICT_CORRECT:
        return GrammarVerdict(correct=True, message=message)

    if head == VERDICT_WRONG:
        return GrammarVerdict(correct=False, message=message)

    # La primera línea no era ninguna de las dos: el modelo se saltó el formato.
    # No se recorta nada —cualquier línea puede ser parte de la respuesta— y no
    # hay punto.
    return GrammarVerdict(correct=False, message=answer.strip())


def normalize_user(name: str) -> str:
    """Convierte el nombre escrito en la pantalla en un nombre de archivo seguro.

    Hace dos trabajos que se parecen y no son el mismo: **normalizar** (dejar
    el nombre en su forma única) y **validar** (rechazar lo que no sirve).

    🔑 **Normalizar primero, y una sola vez.** `  Juan `, `JUAN` y `juan` son la
    misma persona, y tienen que acabar en el mismo archivo. Si no se normaliza,
    Windows los junta —no distingue mayúsculas— y Linux los separa. O sea: en
    tu máquina serían una persona y en la nube del paso 7 serían tres. **Sin
    ningún error y con todos los tests en verde**, que es el peor tipo de fallo.

    :raises TypeError: si lo que llega no es un `str`. Igual que en
        `count_words`: por la red entra un número, un `null` o una lista, y
        convertirlo en silencio taparía el problema.
    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    """
    if not isinstance(name, str):
        raise TypeError(
            f"normalize_user esperaba un texto (str) y recibio "
            f"{type(name).__name__}: {name!r}"
        )

    user = name.strip().lower()

    # Los cuatro frenos van por separado, y cada uno dice lo suyo. Un unico
    # "nombre invalido" para todo dejaria a quien lo lea adivinando cual de las
    # cuatro reglas se salto.
    if not user:
        raise InvalidUserError("El nombre no puede estar vacio.")

    if len(user) > MAX_USER_LENGTH:
        raise InvalidUserError(
            f"El nombre no puede pasar de {MAX_USER_LENGTH} caracteres, "
            f"y este tiene {len(user)}."
        )

    if not USER_PATTERN.match(user):
        raise InvalidUserError(
            "El nombre solo admite letras sin tilde, numeros, guion y guion "
            f"bajo. Este no encaja: {name!r}"
        )

    if user in WINDOWS_RESERVED_NAMES:
        raise InvalidUserError(
            f"{user!r} es un nombre que Windows reserva para un dispositivo, "
            "y no se puede usar como archivo. Elige otro."
        )

    return user


def score_file(name: str, users_dir: Path | None = None) -> Path:
    """Devuelve el archivo del marcador de una persona.

    🔑 **Este es el único sitio donde un nombre se convierte en una ruta**, y
    por eso valida aquí dentro en vez de fiarse de quien llame. La puerta de red
    ya rechaza los nombres malos antes —para contestar un 422 con explicación—,
    pero esta función es la que toca el disco: si algún día la llama alguien que
    se saltó el filtro, tiene que negarse igual. **El olvido tiene que fallar
    hacia el lado seguro.**

    🚨 **El valor por defecto se resuelve AQUÍ DENTRO, no en la firma.** Escribir
    `users_dir: Path = config.users_dir()` parece lo mismo y no lo es: Python
    evalúa los valores por defecto **una sola vez, al importar el módulo**, y se
    queda con la carpeta de aquel momento para siempre. Hasta [T-071] esta
    función tenía esa firma, y por eso los tests no podían desviar el marcador:
    tenían que sustituir `add_point` entera por un maniquí, y el camino de verdad
    —API, marcador, disco— se quedaba sin recorrer. Preguntando en cada llamada,
    cambiar `TEAPP_DATA_DIR` cambia de verdad dónde se escribe.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises MissingDataDirError: si no hay raíz de datos declarada. Ver [D-037].
    """
    directory = config.users_dir() if users_dir is None else users_dir
    return directory / f"{normalize_user(name)}.json"


@dataclass(frozen=True)
class Counters:
    """Los dos números de una persona. Miden cosas distintas ([D-066]).

    🔑 **`score` ya no cuenta prácticas, cuenta ACIERTOS.** Hasta el 2026-08-13
    subía siempre, mirara lo que mirara el juez. Ahora sube solo si la frase
    estaba bien — y por eso hace falta `practice` al lado: sin él, quien falla
    diez veces ve un cero y no ve su esfuerzo por ningún lado. Con los dos, ve
    "3 de 10". El esfuerzo tiene su sitio y el acierto no se diluye.

    ⚠️ Van juntos en una caja, y no es cosmética: se leen y se escriben en el
    **mismo archivo y de una sola vez**. Devolverlos por separado invitaría a
    leer uno sin el otro, y a que un día no cuadraran.
    """

    score: int  # frases correctas
    practice: int  # frases practicadas, acertadas o no


def read_counters(name: str, users_dir: Path | None = None) -> Counters:
    """Lee los dos contadores de una persona. Si su archivo no existe, son 0 y 0.

    🔑 **Ausente y roto no son lo mismo.** Si no hay archivo, es el primer día y
    los contadores valen 0. Si el archivo existe pero no se entiende, se avisa
    con `ScoreFileError`: devolver 0 en silencio sería decirle "tienes cero
    puntos" a alguien que tenia seis.

    🚨 **Y por eso `practice` se EXIGE, en vez de darle un 0 por defecto.** Es
    [D-068]. Un archivo del formato viejo —`{"score": 9}`— tiene un número que
    contaba **prácticas** en la casilla que ahora significa **aciertos**: la
    misma cifra diciendo otra cosa. Tratarlo como "practice: 0" lo daría por
    bueno y enseñaría un marcador que miente. Exigiendo la clave, un archivo
    viejo da un error que se lee y se arregla borrándolo.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises ScoreFileError: si el archivo existe pero no se puede interpretar.
    """
    path = score_file(name, users_dir)

    if not path.exists():
        return Counters(score=0, practice=0)

    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ScoreFileError(
            f"El marcador {path} no es un JSON valido ({error}). "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        ) from error

    if not isinstance(saved, dict):
        raise ScoreFileError(
            f"El marcador {path} no es un objeto JSON. "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        )

    values = {}

    for key in ("score", "practice"):
        if key not in saved:
            raise ScoreFileError(
                f"El marcador {path} no tiene la clave '{key}'. "
                "No se ha tocado el archivo: revisalo o borralo para empezar "
                "de cero."
            )

        total = saved[key]

        # `isinstance(True, int)` vale True en Python: `bool` hereda de `int`.
        # Sin descartarlo, un {"score": true} pasaria por un 1 perfectamente
        # valido.
        if not isinstance(total, int) or isinstance(total, bool):
            raise ScoreFileError(
                f"El marcador {path} guarda {total!r} en '{key}', que no es un "
                "numero entero. No se ha tocado el archivo: revisalo o borralo "
                "para empezar de cero."
            )

        values[key] = total

    return Counters(score=values["score"], practice=values["practice"])


def record_practice(
    name: str, correct: bool, users_dir: Path | None = None
) -> Counters:
    """Anota una práctica de una persona y devuelve sus dos contadores nuevos.

    `practice` sube **siempre**. `score` sube **solo si `correct`**. Esa es la
    regla entera de [D-066], y vive aquí porque aquí es donde se escribe.

    Crea el archivo —y la carpeta `data/users/`— la primera vez.

    🔑 **Los dos números se escriben DE UNA VEZ, no en dos pasos.** Serían dos
    funciones perfectamente razonables —una que suma acierto, otra que suma
    práctica— y dos escrituras seguidas. Pero entre las dos hay un instante, y
    un fallo justo ahí deja el archivo con la práctica sumada y el acierto no.
    Nadie daría un error: solo un marcador que ya no cuadra, para siempre. Una
    sola escritura no tiene ese hueco.

    ⚠️ **`correct` es obligatorio y no tiene valor por defecto, a propósito.**
    Mismo motivo que `user` en `respond`: un `correct=True` de repuesto haría
    que olvidarse de pasarlo **regalara** el punto, y en silencio. Es justo el
    fallo que [D-066] viene a matar.

    🔑 **Nunca sobrescribas un dato que no lograste entender.** Si el archivo
    está roto, quien lo use todavia puede abrirlo y recuperar su marcador a
    mano; si lo pisamos con un 1, ya no. Por eso el `read_counters` va PRIMERO y
    su error sube sin atrapar: cuando falla, la escritura de abajo ni se
    intenta. No es casualidad del orden — es el orden lo que protege el dato.

    🔑 **La escritura es atómica: se escribe al lado y se renombra encima.**
    `write_text` haria dos cosas seguidas —vaciar el archivo y luego llenarlo— y
    entre las dos hay un instante. Un corte de luz justo ahi deja el marcador
    vacio o partido por la mitad, y el punto de arriba no sirve de nada: el
    archivo roto ya lo habriamos creado nosotros.

    Renombrar, en cambio, es UNA sola operacion del sistema operativo: o paso
    entera, o no paso. Nunca deja el archivo a medias. Asi, ante un corte, o
    queda el marcador viejo entero o el nuevo entero.

    🔑 **El candado y la escritura atomica resuelven cosas distintas.** La
    escritura atomica protege de UNA escritura cortada por la mitad. El candado
    protege de DOS escrituras pisandose. Tener la primera no da la segunda:
    hasta que hubo servidor no se noto, porque en la terminal solo escribia una
    persona a la vez.

    Y el candado abarca la lectura Y la escritura juntas, no solo la escritura.
    Si abarcara solo la escritura, dos peticiones leerian el mismo 5, las dos
    sumarian 1 y las dos escribirian 6: un punto perdido y dos personas con el
    mismo numero. El problema no esta en escribir, esta en el hueco entre leer
    y escribir.

    🔑 **Un candado para todos, no uno por persona.** Ahora que cada quien tiene
    su archivo, dos personas distintas ya no se pisan nunca — pero un candado
    unico sigue siendo correcto: solo hace esperar unos milisegundos a quien
    llegue segundo. Un diccionario de candados seria complejidad que nadie ha
    pedido, y candados que nadie borra nunca.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises ScoreFileError: si el archivo existe pero no se puede interpretar.
        En ese caso el archivo queda intacto.
    """
    path = score_file(name, users_dir)

    with _SCORE_LOCK:
        current = read_counters(name, users_dir)
        total = Counters(
            score=current.score + (1 if correct else 0),
            practice=current.practice + 1,
        )
        path.parent.mkdir(parents=True, exist_ok=True)

        # Cada escritura estrena su propio temporal. Con un nombre fijo y
        # compartido, dos peticiones a la vez se lo quitan de las manos —una
        # renombrando mientras la otra sobrescribe— y Windows lo corta en seco
        # con un "Acceso denegado".
        #
        # `dir=path.parent` no es un detalle: el temporal tiene que nacer en la
        # MISMA carpeta que el definitivo. Renombrar solo es atomico dentro del
        # mismo disco; cruzando de disco deja de ser un renombrado y pasa a ser
        # copiar y borrar, que es justo lo que se esta evitando.
        handle, temporary_name = tempfile.mkstemp(
            dir=path.parent, prefix=f"{path.name}.", suffix=".tmp"
        )
        temporary = Path(temporary_name)

        try:
            # `mkstemp` devuelve el archivo ya abierto, a bajo nivel. `fdopen`
            # lo envuelve para poder escribirle texto, y el `with` lo cierra.
            # Cerrarlo antes de renombrar es obligatorio en Windows: no deja
            # mover un archivo que sigue abierto.
            with os.fdopen(handle, "w", encoding="utf-8") as file:
                file.write(
                    json.dumps(
                        {"score": total.score, "practice": total.practice}
                    )
                )

            # `os.replace` pisa el destino aunque ya exista, y lo hace igual en
            # Windows y en Linux. `Path.rename` no: en Windows revienta si el
            # destino existe.
            os.replace(temporary, path)
        except BaseException:
            # Si algo falla, el temporal no se queda de recuerdo. `BaseException`
            # y no `Exception` para que un Ctrl-C tambien limpie.
            temporary.unlink(missing_ok=True)
            raise

        return total
