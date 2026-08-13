"""La báscula del tutor: cuánto tarda y cuántos tokens gasta una práctica.

🚨 **Esto SÍ gasta dinero de verdad.** Es el único archivo del proyecto que
llama a Claude fuera de la app, y existe para contestar las dos preguntas que
`[A-010]` y `[A-011]` llevan desde el paso 4 dando por ciertas sin medir:

- `[A-010]` — ¿cuánto cuesta una práctica, y por tanto aguantan 20 al día?
- `[A-011]` — **solo la mitad**, y conviene tenerlo claro antes de leer nada.

🚨 **Esto cronometra `judge_grammar`, NO una práctica.** El freno de `[A-011]`
(`TUTOR_TIMEOUT_SECONDS = 10.0`) mide otra cosa: la **cola del pool** más
`respond()` entero —`count_words`, `judge_grammar` y `add_point`, que escribe en
disco con candado—. Restar `10 −` lo que salga de aquí da un margen falso, sobre
un presupuesto que paga trozos que esta báscula no toca. Pasó el 2026-08-11: se
retiró `[A-011]` con este número y hubo que reabrirla. Ver `[L-043]`.

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

# 🚨 **El corte duro, y va aquí arriba donde se ve.** Capa 1 de `[D-059]`.
#
# `[D-057]` decidió que el freno del paso 8 es el saldo prepagado, y es verdad:
# cuando se acaba, las llamadas fallan. Pero el saldo protege la cartera, no la
# medición — un guion que llamara de más gastaría saldo que hace falta para
# `[C-008]`, donde medir y servir comparten bolsillo.
#
# 🔑 **El tope sale del DINERO, no del historial.** Hasta el 2026-08-11 esto
# valía 10, que era el tamaño de la tanda que ya se había corrido — respuesta a
# "¿cuántas llamadas hice?", usada para "¿cuántas me puedo gastar?". Son dos
# preguntas distintas y la primera no contesta la segunda. Falla por los dos
# lados: el paso 9 compara modelos con decenas de llamadas y el freno mordería
# en falso, y de dinero no dice nada, que es de lo que protege. Ver `[D-060]`.
#
# Por eso la división está en el código y no en un comentario: quien cambie el
# presupuesto no tiene que recalcular nada a mano.
BUDGET_PER_RUN_USD = 0.25

# 💵 Medido, no recordado (regla 6): sale de `[D-058]`, que cruzó la consola de
# Anthropic con los tokens de la primera tanda. Es el precio de UNA práctica con
# `claude-opus-5`, que es **el modelo más caro que se va a probar**. Errar por
# ahí es errar del lado seguro: con modelos baratos el tope se queda corto —
# sobra presupuesto y no muerde nadie—, nunca largo.
COST_PER_CALL_USD = 0.00234

MAX_CALLS_PER_RUN = int(BUDGET_PER_RUN_USD / COST_PER_CALL_USD)


class CallBudgetExceeded(RuntimeError):
    """La tanda pidió más llamadas de las que tiene pagadas.

    🚨 **Esto no es un error a manejar: es un accidente parado a tiempo.** Si
    salta, hay un fallo en el guion —un bucle que no sale, un reintento mal
    puesto—, porque una tanda sana no se acerca al tope.
    """


class CallBudget:
    """El monedero de la tanda: cuenta llamadas y corta cuando se acaban.

    🔑 **Uno solo por corrida, compartido por todos los clientes.** Ese es el
    punto entero. `main()` construye un `RecordingClient` nuevo en cada vuelta
    del bucle, así que un contador que viviera dentro del cliente se pondría a
    cero cada vez y no contaría nada. El monedero se crea fuera y se pasa.

    ⚠️ **Lo que este freno NO cubre, y va escrito aquí y no en el índice de
    ninguna parte:** se reinicia cuando arranca el guion. Para de un bucle roto
    que llama mil veces **en una corrida** —que es la amenaza que `[D-057]`
    nombró y el fallo mudo de `[C-008]`—, pero **no** para de correr
    `python measure_tutor.py` una y otra vez a mano. Ahí el monedero vuelve a
    estar lleno y el saldo baja igual.

    🚨 **Y el hueco tiene número: `$6,55 ÷ $0,25 = 26 corridas` vacían el
    saldo.** Veintiséis no es un número grande — el paso 9 es comparar modelos,
    o sea correr esto una vez por modelo, varias veces. Es deliberado
    (`[D-060]`), pero se escribe con la cifra: "no protege de correrlo muchas
    veces" se lee como "habría que ser tonto"; 26 se lee como lo que es.
    """

    def __init__(self, max_calls: int = MAX_CALLS_PER_RUN):
        self.max_calls = max_calls
        self.spent = 0

    def spend(self) -> None:
        """Cobra una llamada, o revienta si ya no queda.

        🔑 **Se cobra ANTES de llamar, no después.** Cobrando después, la
        llamada que rebasa el tope ya se hizo y ya se pagó: el freno avisaría de
        un gasto en vez de impedirlo.
        """
        if self.spent >= self.max_calls:
            raise CallBudgetExceeded(
                f"Tope de la tanda alcanzado: {self.max_calls} llamadas "
                f"(${BUDGET_PER_RUN_USD:.2f} a ${COST_PER_CALL_USD} cada una). "
                "Si esto salta, el guion tiene un fallo: una tanda sana no se "
                "acerca al tope."
            )
        self.spent += 1

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

    🚨 **Y es donde se cobra el presupuesto, porque es el paso obligado.** Toda
    llamada a Anthropic de este guion pasa por aquí. Poner el corte más arriba
    —en el bucle de `main()`— dejaría escapar cualquier camino que llame sin
    pasar por el bucle; aquí no hay puerta de atrás.
    """

    def __init__(self, inner, budget):
        self._inner = inner
        self._budget = budget
        self.usages = []

    @property
    def messages(self):
        return self

    def create(self, **kwargs):
        # Primero se cobra, después se llama. Al revés, el freno llegaría tarde.
        self._budget.spend()
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
        timeout=tools.TIMEOUT,
    )

    print(f"Modelo: {tools.MODEL_NAME} (esfuerzo {tools.EFFORT})")
    print(f"Presupuesto de esta tanda: ${BUDGET_PER_RUN_USD:.2f} = "
          f"{MAX_CALLS_PER_RUN} llamadas a ${COST_PER_CALL_USD} cada una")
    print(f"Frases a medir: {len(SENTENCES)}")
    # Se imprimen las CUATRO fases, no el total: el total es lo que se creyo
    # tener durante media jornada sin tenerlo ([L-054]).
    print(f"Timeout del cliente: {tools.TIMEOUT_SECONDS} s en total = "
          f"connect {tools.TIMEOUT.connect} + write {tools.TIMEOUT.write} + "
          f"read {tools.TIMEOUT.read} + pool {tools.TIMEOUT.pool}")
    print("-" * 78)

    rows = []

    # 🔑 **Un monedero para toda la corrida, creado FUERA del bucle.** Dentro se
    # reiniciaría en cada vuelta y no contaría nada.
    budget = CallBudget()

    # `for` sobre una lista, no `while`. Ya no se recorta la lista con el tope:
    # el tope es el techo del gasto, no el plan de la tanda, y confundirlos es lo
    # que hacía el recorte viejo. Quien frena es el monedero.
    for number, sentence in enumerate(SENTENCES, start=1):
        client = RecordingClient(inner, budget)

        started = time.monotonic()
        try:
            verdict = judge_grammar(sentence, client=client)
        except CallBudgetExceeded as error:
            # 🚨 Se PARA y se enseña lo medido hasta aquí. Perder los datos ya
            # costó dinero una vez en este mismo archivo (ver [L-001] abajo).
            print(f"\n[{number}] PRESUPUESTO AGOTADO: {error}")
            break
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
    print(f"LLAMADAS COMPLETADAS: {len(rows)} de {len(SENTENCES)} frases")
    print(f"GASTADO DEL PRESUPUESTO: {budget.spent} de {budget.max_calls} llamadas")

    times = [row["elapsed"] for row in rows]
    inputs = [row["input"] for row in rows]
    outputs = [row["output"] for row in rows]

    print("\nTIEMPO de judge_grammar - NO es el tiempo de una practica")
    print(f"    minimo:       {min(times):.2f} s")
    print(f"    mediana:      {statistics.median(times):.2f} s")
    print(f"    peor de {len(times):2d}:    {max(times):.2f} s")
    print("    [A-011] mide la COLA del pool + respond() entero, no esto.")
    print("    No restar de 10 s: daria un margen falso. Ver [L-043].")

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
