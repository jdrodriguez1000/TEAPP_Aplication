"""La báscula del tutor: cuánto tarda y cuántos tokens gasta una práctica.

🚨 **Esto SÍ gasta dinero de verdad.** Es el único archivo del proyecto que
llama a Claude fuera de la app, y existe para contestar las dos preguntas que
`[A-010]` y `[A-011]` llevan desde el paso 4 dando por ciertas sin medir:

- `[A-011]` — ¿son 10 segundos lo que hay que esperar al tutor?
- `[A-010]` — ¿cuánto cuesta una práctica, y por tanto aguantan 20 al día?

🔑 **Mide el camino REAL, no una imitación.** Llama a `judge_grammar`, la misma
función que usa la app, con un cliente construido igual que el suyo
(`max_retries=0`, `timeout=8.0`). Un guion que armara su propia llamada mediría
otra cosa y se parecería lo bastante como para que nadie lo notara.

⚠️ **No escribe en `data/`.** `judge_grammar` no toca el disco: quien suma
puntos es `add_point`, y aquí no se llama. Es la lección de `[L-023]`, donde la
báscula de `T-054` sí escribió donde no debía.

Se corre a mano:

    python measure_tutor.py
"""

import statistics
import time

import anthropic

from app import config, tools
from app.tools import TutorUnavailableError, judge_grammar

# 🚨 **El corte duro, y va aquí arriba donde se ve.**
#
# `[D-057]` decidió que el freno del paso 8 es el saldo prepagado, y es verdad:
# cuando se acaba, las llamadas fallan. Pero el saldo protege la cartera, no la
# medición — un guion que llamara de más gastaría saldo que hace falta para
# `[C-008]`, donde medir y servir comparten bolsillo.
#
# 🔑 Por eso el tope es un número, no un `while` con condición de salida. Un
# bucle que se apoya en su propia condición para parar es exactamente el fallo
# del que `[A-024]` tenía miedo.
MAX_CALLS = 10

# Frases de nivel A1, que es lo que `_context/scope.md` pide practicar. Mezcla
# a propósito: unas correctas y otras con un error claro, para que de paso se
# vea si la rúbrica de `[D-049]` juzga como se le pidió.
SENTENCES = [
    "I like coffee",
    "She go to school every day",
    "I have 20 years old",
    "They is my friends",
    "He don't like pizza",
    "We went to the park yesterday",
    "My sister have a dog",
    "Do you want to go with me?",
    "Yesterday I go to the store",
    "The weather is nice today",
]


class RecordingClient:
    """Un cliente de verdad con una libreta encima.

    🔑 **No sustituye la llamada: la envuelve.** Por dentro corre el cliente
    real de Anthropic, así que lo que se cronometra es la llamada que hace la
    app. Lo único que añade es apuntar `usage` al pasar — que es el dato que
    `judge_grammar` usa para decidir la cuota (`[D-055]`) y que no devuelve.

    ⚠️ Entra por el parámetro `client` de `judge_grammar`, la misma puerta que
    usan los tests. Y por eso este cliente trae **los mismos frenos** que el que
    construye `judge_grammar` sola: si no, se mediría una llamada con otro
    timeout y otro número de reintentos.
    """

    def __init__(self, inner):
        self._inner = inner
        self.usages = []

    @property
    def messages(self):
        return self

    def create(self, **kwargs):
        answer = self._inner.messages.create(**kwargs)
        self.usages.append(answer.usage)
        return answer


# 🚨 **Lo que se IMPRIME va en ASCII puro: ni emoji ni tildes.** No es estilo,
# es [L-001]: la consola de Windows usa cp1252 y un emoji la tumba con
# `UnicodeEncodeError`. Pasó el 2026-08-11 en este mismo archivo, DESPUÉS de las
# diez llamadas — los datos se salvaron porque ya estaban impresos, pero el
# resumen se perdió y volver a calcularlo llamando otra vez habría costado
# dinero. 🔑 Los emoji de los COMENTARIOS no molestan: nadie los imprime.
# Tercera vez que [L-001] muerde en un guion suelto (ver [L-039]).
def main() -> None:
    config.load_env_file()

    # La llave se comprueba aquí para fallar temprano y con un mensaje claro,
    # no a mitad de la primera llamada. Nunca se imprime (regla 7).
    key = config.require_anthropic_key()
    print(f"Llave cargada: empieza por {key[:7]}..., {len(key)} caracteres\n")

    inner = anthropic.Anthropic(
        api_key=key,
        max_retries=tools.MAX_RETRIES,
        timeout=tools.TIMEOUT_SECONDS,
    )

    print(f"Modelo: {tools.MODEL_NAME} (esfuerzo {tools.EFFORT})")
    print(f"Tope de llamadas de este guion: {MAX_CALLS}")
    print(f"Timeout del cliente: {tools.TIMEOUT_SECONDS} s")
    print("-" * 78)

    rows = []

    # `for` sobre una lista acotada, no `while`. El tope se comprueba además a
    # mano, por si alguien alarga `SENTENCES` sin mirar esta constante.
    for number, sentence in enumerate(SENTENCES[:MAX_CALLS], start=1):
        client = RecordingClient(inner)

        started = time.monotonic()
        try:
            verdict = judge_grammar(sentence, client=client)
        except TutorUnavailableError as error:
            # 🚨 Se PARA, no se reintenta. Si el tutor deja de estar disponible
            # a mitad, insistir es justo lo que gasta saldo sin aprender nada.
            elapsed = time.monotonic() - started
            print(f"\n[{number}] CORTADO tras {elapsed:.2f} s: {error}")
            print(f"    la peticion salio: {'si' if error.request_sent else 'no'}")
            break

        elapsed = time.monotonic() - started
        usage = client.usages[-1]

        rows.append(
            {
                "elapsed": elapsed,
                "input": usage.input_tokens,
                "output": usage.output_tokens,
            }
        )

        print(f"\n[{number}] {elapsed:5.2f} s | "
              f"entrada {usage.input_tokens:4d} | salida {usage.output_tokens:3d}")
        print(f"    frase:    {sentence}")
        print(f"    veredicto: {verdict}")

    if not rows:
        print("\nNo se completo ninguna llamada: no hay nada que medir.")
        return

    print("\n" + "=" * 78)
    print(f"LLAMADAS COMPLETADAS: {len(rows)} de {MAX_CALLS}")

    times = [row["elapsed"] for row in rows]
    inputs = [row["input"] for row in rows]
    outputs = [row["output"] for row in rows]

    print("\nTIEMPO - contesta [A-011] (hoy el tope son 10 s)")
    print(f"    minimo:  {min(times):.2f} s")
    print(f"    mediana: {statistics.median(times):.2f} s")
    print(f"    maximo:  {max(times):.2f} s")

    print("\nTOKENS - materia prima de [A-010] (hoy el tope son 20/dia)")
    print(f"    entrada por practica:  {statistics.mean(inputs):.0f} de media "
          f"(min {min(inputs)}, max {max(inputs)})")
    print(f"    salida por practica:   {statistics.mean(outputs):.0f} de media "
          f"(min {min(outputs)}, max {max(outputs)})")
    print(f"    TOTAL de esta corrida: {sum(inputs)} entrada + {sum(outputs)} salida")

    print("\nEl precio NO se calcula aqui (regla 6): estos son tokens, no")
    print("    dolares. El gasto real se lee en la consola de Anthropic.")


if __name__ == "__main__":
    main()
