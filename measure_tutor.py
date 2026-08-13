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
(`max_retries=0`, mismo modelo, mismo esfuerzo, misma rúbrica). Un guion que
armara su propia llamada mediría otra cosa y se parecería lo bastante como para
que nadie lo notara.

🚨 **Con UNA excepción, y es deliberada: el reloj de lectura.** La báscula usa
`MEASURING_READ_SECONDS = 30.0` en vez del `read` de producción. **Un instrumento
no puede medir su propio tope:** heredándolo, toda llamada que lo cruzara dejaría
de ser una muestra y pasaría a ser un error, y la cola de la distribución —lo
único que hace falta para colocar bien ese tope— sería justo lo invisible. El
porqué largo está junto a la constante. Ver `[D-072]` y `[L-057]`.

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

# 🚨 **El reloj de lectura de ESTA BASCULA, y va a proposito MUY por encima del
# de produccion (`tools.TIMEOUT.read`).**
#
# 🔑 **Un instrumento no puede medir su propio tope.** Si la bascula heredara el
# `read` de produccion, toda llamada que lo cruzara dejaria de ser una MUESTRA y
# pasaria a ser un ERROR — y la **cola de la distribucion**, que es justo lo unico
# que hace falta para colocar bien ese tope, seria lo que el instrumento ya no
# puede ver. El resultado no seria un numero falso: seria **silencio disfrazado
# de "Anthropic tardo"**. Ver `[D-072]` y `[L-057]`.
#
# ⚠️ **Y esto es una EXCEPCION ESCRITA a la regla de `[L-043]`**, que dice —con
# razon— que un guion que arma su propia llamada mide otra cosa. La excepcion es
# exacta y no se estira:
#
# > 🔑 **La bascula es identica a produccion en TODO menos en el tope que esta
# > intentando medir.** Mismo modelo, mismo esfuerzo, misma rubrica, mismos
# > `max_retries`, misma funcion `judge_grammar`. Solo el `read` cambia.
#
# Los 30 s no salen de ningun sitio medido: son "lo bastante alto para que no
# corte nunca" en una tanda que se mira a mano. No es un freno del gasto — de eso
# se ocupa `CallBudget`, que cuenta llamadas y no segundos.
MEASURING_READ_SECONDS = 30.0

MEASURING_TIMEOUT = anthropic.Timeout(
    connect=tools.TIMEOUT.connect,
    write=tools.TIMEOUT.write,
    read=MEASURING_READ_SECONDS,
    pool=tools.TIMEOUT.pool,
)


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

# ── El criterio de `T-093`, decidido ANTES de gastar ──────────────────────
#
# 🚨 **Esto se escribe antes de correr la tanda, y ese es su punto entero.**
# Decidir el umbral DESPUES de ver los datos lleva a tomar `max(N)` como si fuera
# una cota — el error de `[L-058]`, que ya mordio dos veces hoy y que con mas
# muestras se siente MAS solido en vez de menos.
#
# **La pregunta que contesta la tanda** (`[D-073]`): no es "cuanto tarda Opus 5"
# —`read` es maximo por construccion, ninguna medida lo ajusta— sino:
#
# > 🔑 **¿Son 10 s el presupuesto correcto de la RUTA?**
#
# Se mide con `MEASURING_READ_SECONDS` (30 s), o sea con el reloj de produccion
# QUITADO: si la bascula heredara el tope, las llamadas lentas dejarian de ser
# muestras y pasarian a ser errores. Es `[L-057]`.
TARGET_SAMPLES = 60

# 🔢 **De donde sale el 60, y no es un numero redondo.** La tasa de corte que se
# acepta es **5%** (1 de cada 20 practicas cortada y cobrada). Con cero cortes
# observados, lo maximo que se puede AFIRMAR es la regla de tres: `3/n`.
#
#     n = 40  →  3/40 = 7,5%   ← afirma menos de lo que exigimos
#     n = 60  →  3/60 = 5,0%   ← coincide con el criterio
#
# Con 40 muestras y cero cortes habria que escribir "menos del 7,5%" y luego
# compararlo con un objetivo del 5%: no se puede concluir nada. Cuestan cinco
# centavos mas y hacen que la afirmacion y el criterio sean el mismo numero.
ACCEPTED_CUT_RATE = 0.05

# Los dos umbrales contra los que se cuentan las muestras. Ninguno se estima:
# los dos salen del codigo.
#
# - `tools.TIMEOUT.read` (6,5 s) es lo que corta HOY en produccion. Una llamada
#   por encima de esto es una practica cortada Y COBRADA (`[D-051]`).
# - 9,5 s es el presupuesto de la ruta (10 s) menos el trabajo local y un margen.
#   Una llamada por encima de esto no la salva NINGUN reparto de fases.
#
# 🔑 El de corte se LEE de produccion, no se copia: si el reparto de fases cambia,
# esta tanda cuenta contra el nuevo sin que nadie tenga que acordarse.
CUT_THRESHOLD_SECONDS = tools.TIMEOUT.read
ROUTE_THRESHOLD_SECONDS = 9.5


def verdict_for(over_cut: int, over_route: int, total: int) -> str:
    """El veredicto de la tanda, decidido antes de verla. ASCII puro ([L-001]).

    🔑 **Es una funcion y no un parrafo en un documento a proposito:** un
    criterio que hay que ir a buscar a `decisions.md` se reinterpreta; uno que
    imprime el guion, no.
    """
    if over_route > 0:
        return (
            "ROJO - alguna llamada paso de "
            f"{ROUTE_THRESHOLD_SECONDS} s. NINGUN reparto de fases salva esto: "
            "lo que esta mal es el presupuesto de la RUTA (10 s), no el del "
            "cliente. [A-011] NO se cierra."
        )
    if over_cut == 0:
        return (
            f"VERDE - 0 de {total} pasaron de {CUT_THRESHOLD_SECONDS} s. Por la "
            f"regla de tres, la tasa de corte esta por debajo de "
            f"{3 / total:.1%}, que es el {ACCEPTED_CUT_RATE:.0%} acordado. "
            "Los 10 s de la ruta valen y [A-011] se puede cerrar."
        )
    return (
        f"AMBAR - {over_cut} de {total} pasaron de {CUT_THRESHOLD_SECONDS} s "
        f"({over_cut / total:.1%}, por encima del {ACCEPTED_CUT_RATE:.0%} "
        "acordado) pero ninguna paso de la ruta. El presupuesto de la ruta esta "
        "bien; hay que REEQUILIBRAR las fases dentro de los 10 s: quitar de "
        "connect/write/pool y darselo a read."
    )


# Frases de nivel A1, que es lo que `_context/scope.md` pide practicar. Mezcla
# a propósito: unas correctas y otras con un error claro, para que de paso se
# vea si la rúbrica de `[D-049]` juzga como se le pidió.
#
# ⚠️ **Sesenta DISTINTAS, no diez repetidas seis veces.** Repetir la misma frase
# mediría el efecto de la caché de Anthropic, no el tiempo de generación — y
# saldría más rápido de lo real, que es el lado peligroso del error.
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
    "My brother is a doctor",
    "I am living here since 2020",
    "She don't have any money",
    "We are going to the beach tomorrow",
    "He have three cats",
    "The childrens are playing outside",
    "I don't like to wake up early",
    "Where you are going?",
    "My parents lives in Madrid",
    "This book is very interesting",
    "I did not saw him yesterday",
    "There is many people in the street",
    "She is more taller than me",
    "We have finished our homework",
    "He goed to the cinema last night",
    "I am agree with you",
    "The food was delicious",
    "They didn't went to the party",
    "My friend she is very kind",
    "How much time you need?",
    "I have been to London twice",
    "She speak three languages",
    "We was very tired after the trip",
    "The train leaves at eight o'clock",
    "I need to buy a new phone",
    "He is working here since January",
    "Do you like to play football?",
    "My car is more expensive that yours",
    "She has a beautiful red dress",
    "I forgot to bring my umbrella",
    "The movie was very boring",
    "They are knowing the answer",
    "We should to leave now",
    "My sister is younger than me",
    "I have a lot of works to do",
    "He never eats vegetables",
    "Can you tell me where is the station?",
    "She was born in a small village",
    "I am interesting in this job",
    "We didn't have enough time",
    "The weather will be sunny tomorrow",
    "He asked me what was my name",
    "I usually go to bed at eleven",
    "There are less people today",
    "She told me that she is tired",
    "My teacher explain everything clearly",
    "We enjoyed the concert very much",
    "I have lived here for ten years",
    "He don't want to talk about it",
    "The keys are on the table",
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
        timeout=MEASURING_TIMEOUT,
    )

    print(f"Modelo: {tools.MODEL_NAME} (esfuerzo {tools.EFFORT})")
    print(f"Presupuesto de esta tanda: ${BUDGET_PER_RUN_USD:.2f} = "
          f"{MAX_CALLS_PER_RUN} llamadas a ${COST_PER_CALL_USD} cada una")
    print(f"Frases a medir: {len(SENTENCES)}")
    print()
    print("CRITERIO DE T-093, decidido ANTES de correr esto:")
    print(f"    muestras objetivo:      {TARGET_SAMPLES} "
          f"(3/{TARGET_SAMPLES} = {3/TARGET_SAMPLES:.1%}, regla de tres)")
    print(f"    tasa de corte aceptada: {ACCEPTED_CUT_RATE:.0%} "
          "(1 de cada 20 practicas cortada Y COBRADA)")
    print(f"    umbral de corte:        {CUT_THRESHOLD_SECONDS} s "
          "(el read de produccion)")
    print(f"    umbral de la ruta:      {ROUTE_THRESHOLD_SECONDS} s "
          "(por encima, ningun reparto salva)")
    # Se imprimen las CUATRO fases, no el total: el total es lo que se creyo
    # tener durante media jornada sin tenerlo ([L-054]).
    print(f"Timeout de PRODUCCION: {tools.TIMEOUT_SECONDS} s = "
          f"connect {tools.TIMEOUT.connect} + write {tools.TIMEOUT.write} + "
          f"read {tools.TIMEOUT.read} + pool {tools.TIMEOUT.pool}")
    print(f"Timeout de ESTA BASCULA: read {MEASURING_READ_SECONDS} s "
          f"(a proposito mas alto; ver la cabecera del archivo)")
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
    print("    OJO: 'el peor de N' es un SUELO que crece con N, no un techo.")
    print("    No se decide nada con esta cifra. Ver [L-058].")
    print("    Y esto no es una practica entera: falta respond(). Ver [L-043].")

    # ── El veredicto de T-093 ────────────────────────────────────────────
    #
    # 🔑 Se cuenta contra umbrales fijados ARRIBA, antes de ver un solo dato.
    over_cut = sum(1 for t in times if t > CUT_THRESHOLD_SECONDS)
    over_route = sum(1 for t in times if t > ROUTE_THRESHOLD_SECONDS)

    print("\n" + "=" * 78)
    print("VEREDICTO DE T-093 - contra el criterio fijado ANTES de medir")
    print(f"    por encima de {CUT_THRESHOLD_SECONDS} s (corta y COBRA): "
          f"{over_cut} de {len(times)}")
    print(f"    por encima de {ROUTE_THRESHOLD_SECONDS} s (ni el reparto salva): "
          f"{over_route} de {len(times)}")

    if len(times) < TARGET_SAMPLES:
        print(f"\n    ⚠ SOLO {len(times)} MUESTRAS DE {TARGET_SAMPLES}.")
        print("    La regla de tres necesita la N entera para afirmar el")
        print(f"    {ACCEPTED_CUT_RATE:.0%}. Con menos, el veredicto de abajo NO")
        print("    se puede escribir en [A-011]: se repite la tanda.")

    print()
    print(f"    {verdict_for(over_cut, over_route, len(times))}")

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
