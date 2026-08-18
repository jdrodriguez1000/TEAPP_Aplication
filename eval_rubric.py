"""El eval de la forma: cuántas respuestas del juez rompen la rúbrica.

🚨 **Esto SÍ gasta dinero de verdad.** Es el segundo archivo del proyecto que
llama a Claude fuera de la app. Una corrida entera son **60 llamadas ≈ $0,18**
(`$0,00304` cada una, medido en `[D-079]`, no estimado), y sale del saldo que
`[C-009]` declaró **compartido** con otras cosas que no son TEAPP.

Se corre a mano:

    python eval_rubric.py              # las 60 frases
    python eval_rubric.py 2 3 4 5      # solo esas, por su número (empieza en 1)

🔑 **Por qué se puede correr un trozo, y no es comodidad: es dinero.** Investigar
*por qué* falló algo no necesita las 60 muestras, necesita **ver el texto de unas
pocas**. Diez frases son `$0,03` en vez de `$0,18`. ⚠️ **Pero una tanda parcial NO
es una línea base** —el informe lo dice él mismo cuando faltan respuestas—: para
comparar modelos hay que correr las 60.

## Qué contesta, y qué NO

✅ **Contesta:** de las 60 respuestas, cuántas rompieron cada una de las cuatro
promesas mecánicas de `GRAMMAR_RUBRIC`. Ver `app/rubric_check.py`.

🚨 **NO contesta si el veredicto acierta.** No sabe si `"She go to school"` está
bien o mal, y no puede saberlo: para eso hacen falta las 60 frases **etiquetadas
a mano**, que es la otra mitad del paso 9 y no está hecha. Un informe de aquí que
salga limpio significa *"contestó con la forma pedida"*, **nunca** *"juzgó bien"*.

## Para qué sirve tenerlo antes del descenso de modelo

`[D-049]` baja el modelo a Sonnet 5 y después a Haiku 4.5. 🔑 **Un modelo pequeño
no deja de ver que `"She go to school"` está mal** —eso es gramática de primer
año—; lo que se le va es **la forma**: mete un asterisco, se estira a cuatro
frases, o le escribe `FIX` al alumno. Y eso **sale a la pantalla**, porque
`app/static` pinta el mensaje tal cual.

⚠️ **Así que este número solo vale comparado consigo mismo.** Correrlo una vez y
ver "3 de 60" no dice nada: hay que tener la línea base del modelo de hoy **antes**
de bajar, o después no habrá contra qué comparar. Es lo mismo que `[D-079]` hizo
con el coste — sellar el criterio antes de mirar.

## Mide el camino REAL, y la excepción de la báscula NO se hereda

Llama a `judge_grammar`, la misma función que usa la app, con un cliente que trae
**los frenos de producción** (`tools.TIMEOUT`, `tools.MAX_RETRIES`), el mismo
modelo, el mismo esfuerzo y la misma rúbrica. Es `[L-043]`: un guion que arma su
propia llamada mide otra cosa y se parece lo bastante como para que nadie lo note.

🚨 **Y aquí NO se usa `MEASURING_READ_SECONDS`, a diferencia de `measure_tutor.py`.**
Aquella báscula sube el `read` a 30 s porque **está midiendo ese tope**, y un
instrumento no puede medir el suyo (`[L-057]`). Este eval mide **la forma de la
respuesta**, no el reloj, así que heredar el tope de producción es lo correcto:
lo que interesa es la rúbrica *tal como la vive la app*. La excepción de `[L-057]`
es exacta y no se estira.

⚠️ **El precio, dicho antes de correrlo:** si una llamada cruza el `read` de
producción (6,5 s) deja de dar muestra. **No es silencio** —`judge_grammar` lanza
`TutorUnavailableError`, el guion para y enseña lo medido hasta ahí—, pero sí es
una muestra menos, y el informe dice cuántas llegaron.

## Dónde escribe, y por qué eso cambió

🔴 **Esta sección decía "no escribe en `data/`" hasta el 2026-08-17, y se corrige
en el sitio en vez de matizarse debajo.** Ahora **sí** escribe: guarda cada
respuesta en `data/eval_replies.jsonl`.

🔑 **Por qué hizo falta, y el motivo es un fallo propio.** La primera corrida
—60 llamadas, `$0,18`— contó **18 respuestas** pasadas de largo y **tiró el
texto**. O sea que el número sorprendente llegó **después** del gasto y no había
forma de investigarlo sin volver a pagar. Es `[L-071]` exacto: *cuadrar contra un
agregado no es cuadrar*, cometido en un instrumento nuevo el mismo día que se citó
la lección. **Un instrumento que cuenta y tira la evidencia obliga a pagar dos
veces por una pregunta.**

🚨 **Las corridas VIVAS van a `data/`, y esto es `PI-8`.** `data/` está en
`.gitignore` —comprobado con `git check-ignore`, no supuesto—; `_persistence/` va
a Git a propósito y el repo es **público** (`[C-007]`). Aquí dentro hay texto que
escribió un modelo sobre frases **inventadas** (`measure_tutor.SENTENCES`), no
frases de ninguna persona — pero el sitio se elige por la regla, no por lo que hoy
haya dentro.

🔴 **Esta sección decía "y NO en `_persistence/`", a secas, hasta el 2026-08-18, y
`[D-092]` abrió una excepción estrecha que hay que decir aquí y no debajo.** Un
corpus **congelado** —aquel cuyo modelo o cuya rúbrica ya no son los de
producción— sí se promueve a `_persistence/corpus/`, porque es evidencia de una
decisión firmada que **no se puede volver a levantar ni pagando**, y `data/` es un
solo disco sin copia.

🔒 **Y la excepción no se apoya en acordarse: se apoya en `sentences_are_invented`**
(`[D-093]`). La regla que elige el sitio sigue siendo la regla — lo que cambió es
que ahora hay un programa que la comprueba en vez de una frase que la promete.

⚠️ **Lo que NO cambió:** una corrida viva escribe en `data/`. Nunca se escribe
directamente en `_persistence/`.

📌 **Y la ruta se resuelve LLAMANDO a una función**, nunca en una constante de
módulo: una constante se congela al importar, antes de que nadie pueda desviarla.
Es la condición que `[D-085]` dejó escrita para la traza, aplicada aquí.

⚠️ Lo que sigue siendo cierto de la sección vieja: **no se llama a `add_point` ni
a `trace.record`**, así que no se toca ningún contador ni el cuaderno de la app.

## Lo que este archivo NO toca

📌 **No cablea nada a producción.** Que la ruta llame al corrector y la traza
apunte el fallo de formato es un cambio en `app/api.py` que **no está decidido**.

⚠️ **Lo que se imprime va en ASCII puro: ni emoji ni tildes.** Es `[L-001]`: la
consola de Windows usa cp1252 y un emoji la tumba.
"""

import hashlib
import json
import sys
import time
from collections import Counter
from datetime import date
from pathlib import Path

import anthropic

from app import config, rubric_check, tools
from app.tools import TutorUnavailableError, judge_grammar

# 🔑 **Las 60 frases y el monedero se IMPORTAN, no se copian.** Son de
# `measure_tutor.py`, y tener dos listas de frases o dos topes de gasto es tener
# uno de los dos desactualizado sin saber cuál. Importar un guion no dispara nada:
# `measure_tutor` tiene su `if __name__ == "__main__"`.
from measure_tutor import (
    COST_PER_CALL_USD,
    SENTENCES,
    CallBudget,
    CallBudgetExceeded,
    RecordingClient,
)

# 🚨 **El tope de esta corrida es EXACTAMENTE el número de frases.**
#
# `measure_tutor` deja 82 llamadas (`$0,25 / $0,00304`) porque su tanda se recorta
# sola. Aquí el plan es fijo —una llamada por frase— así que cualquier llamada de
# más es un fallo del guion, no una tanda larga. **Un freno ajustado al plan caza
# el bucle roto en la llamada 61; uno holgado lo caza veintidós llamadas después,
# y esas veintidós ya se pagaron.**
MAX_CALLS = len(SENTENCES)

# El coste de la corrida, con las entradas a la vista y no como un producto ya
# resuelto: `[L-059]` costó una contradicción por pegar un número calculado a mano.
#
# 🔴 **Aquí había una COPIA de `COST_PER_CALL_USD`, tres líneas debajo del
# comentario que dice que el monedero se importa** — y el monedero no estaba en
# esa lista de importaciones. Es `[L-075]` otra vez: el comentario decía la regla
# y la línea de debajo la incumplía. ⚠️ **Lo que lo hacía peor que un duplicado
# normal:** el comentario convence de que hay una sola copia, así que quien
# fuera a corregir el número **no iba a ir a buscar la segunda** — y la que
# gasta la corrida de 60 es esta, la que NO llevaba la nota de caducidad.
# Ver `[L-077]`.
ESTIMATED_COST_USD = MAX_CALLS * COST_PER_CALL_USD


class ReplyRecordingClient(RecordingClient):
    """El cliente de `measure_tutor`, con una libreta más: el TEXTO.

    🔑 **Hereda en vez de copiar, y lo que hereda es lo que importa:** el cobro
    del monedero antes de llamar, y los frenos de producción. Lo único que añade
    es guardar la respuesta cruda al pasar.

    🚨 **Y hace falta porque `judge_grammar` tira justo lo que este eval mide.**
    Devuelve `GrammarVerdict` —fallo y mensaje ya separados— así que la **primera
    línea** ya no existe cuando la función vuelve. Y sin ella no se puede saber si
    el modelo cumplió la primera promesa: `split_verdict` **perdona** el fallo de
    formato y devuelve `correct=False`, que por fuera es idéntico a un `FIX` bien
    puesto. Ver la cabecera de `app/rubric_check.py`.

    📌 Se observa, no se sustituye: por dentro corre el cliente real.
    """

    def __init__(self, inner, budget):
        super().__init__(inner, budget)
        self.replies: list[str] = []

    def create(self, **kwargs):
        answer = super().create(**kwargs)
        self.replies.append(raw_text(answer))
        return answer


def raw_text(answer) -> str:
    """Saca el texto de la respuesta, igual que hace `judge_grammar`.

    🔑 **La respuesta llega en TROZOS, no en un texto.** Con el pensamiento
    encendido el primer trozo puede ser un bloque `thinking` vacío, así que coger
    `content[0]` a ciegas devolvería una cadena vacía.

    ⚠️ **Esto repite `tools.py:542` y la repetición está atada con un test.** Si
    las dos formas de sacar el texto se separan, el eval mediría una respuesta
    distinta de la que la app enseña — y sería un fallo mudo, porque los dos
    devuelven una cadena plausible. Ver `test_eval_rubric.py`.
    """
    return "".join(
        block.text for block in answer.content if block.type == "text"
    ).strip()


def rubric_fingerprint() -> str:
    """Ocho caracteres que identifican la rúbrica con la que se corrió.

    🔑 **Se calcula, no se teclea, y ése es todo el argumento.** Un
    `rubric_version = "2"` escrito a mano se queda desactualizado el primer día que
    alguien edite la rúbrica con prisa — y ese día ya pasó **dos veces** aquí:
    `678 → 1.016` caracteres (`[D-066]`) y `1.016 → 1.098` (`[D-090]`/`[D-091]`),
    las dos sin que nadie se enterara (`[L-059]`). Una huella **no puede** quedarse
    desactualizada: si el texto cambia, cambia ella.

    ⚠️ **Se calcula sobre la rúbrica YA MONTADA**, no sobre el texto fuente:
    `GRAMMAR_RUBRIC` es un `f-string` con `MAX_SENTENCES` dentro, y lo que
    identifica una corrida es lo que el modelo leyó, no lo que hay escrito en el
    archivo. Ver `[D-092]`.
    """
    return hashlib.sha256(tools.GRAMMAR_RUBRIC.encode("utf-8")).hexdigest()[:8]


def replies_file(picked: int | None = None) -> Path:
    """Dónde se guardan las respuestas de la corrida, con su identidad en el nombre.

    🚨 **Es una función y no una constante, a propósito.** Una constante de módulo
    se calcula **al importar**, o sea antes de que nadie pueda desviar la carpeta de
    datos; preguntando en cada llamada, cambiar el entorno cambia de verdad dónde se
    escribe. Es la condición que `[D-085]` dejó escrita para la traza.

    🔴 **Hasta el 2026-08-18 devolvía un nombre FIJO, y con `save_replies` abriendo
    en `"w"` eso borraba la corrida anterior.** Costó la línea base de 60 frases
    (`[L-076]`). 🔑 **No se arregló abriendo en `"a"`:** sobrescribir está bien
    razonado —dos modelos o dos rúbricas revueltos son `[L-071]`—; lo que faltaba
    era **identidad**, que es lo que `[D-092]` puso aquí.

    **Los cuatro ejes del nombre, y por qué cada uno:**

    - `model` — para que dos modelos no se pisen. `[D-049]` va a mover éste **tres
      veces**, y es la razón de ser de todo esto.
    - la fecha — para ordenar. ⚠️ **Ella sola no basta:** la línea base corrió a las
      21:43 UTC y el diagnóstico a las 21:54, **el mismo día**, con la rúbrica
      cambiada entre medias.
    - `rubric` — la huella de arriba.
    - `full` / `pick` — 🚨 **si la tanda fue entera o una selección.** El archivo del
      diagnóstico tiene 10 filas y **10 rotas**, y eso no es un resultado: es la
      selección, que escogió a propósito las que habían fallado. Sin esta marca,
      quien lo divida obtiene `100% de fallo` y se lo cree. Es `[L-071]`.

    :param picked: cuántas frases entraron en la tanda. Sin dato, se asume entera.
    """
    sample = "full" if picked is None or picked == len(SENTENCES) else "pick"

    name = (
        f"eval_replies_{tools.MODEL_NAME}_{date.today().isoformat()}"
        f"_rubric-{rubric_fingerprint()}_{sample}.jsonl"
    )

    return config.require_data_dir() / name


def sentences_are_invented(records: list[dict]) -> bool:
    """🔒 La cerradura de `PI-8`: ¿todas las frases de este corpus son inventadas?

    🚨 **Existe porque `[D-092]` abre la puerta de `_persistence/` a archivos de
    corrida, y este repositorio es PÚBLICO** (`[C-007]`). Hoy la puerta es inocente
    —el corpus se construye contra `SENTENCES`, que ya está en el repo—, **pero eso
    es una propiedad de hoy, no del camino.**

    🔑 **Por qué es una función y no un comentario, que es el punto entero.** Una
    advertencia escrita es una promesa de acordarse; `PI-8` ya se documenta a sí
    misma como la más débil de las tres reglas de código, porque *"una casilla
    pregunta, no detecta"*. Esta condición **sí** la comprueba un programa, así que
    se comprueba: un corpus hecho con frases de gente usando la app falla solo.

    ⚠️ **Alcance honesto, para no repetir el defecto que denuncia:** mira el campo
    `sentence`, que es por donde entraría la frase de una persona. **No** audita
    `reply` —eso lo escribe el modelo— ni vigila el resto del repositorio. Es un
    freno estrecho y bien puesto, no una garantía. Ver `[D-093]`.
    """
    return all(record.get("sentence") in SENTENCES for record in records)


def chosen_sentences(numbers: list[str]) -> list[tuple[int, str]]:
    """Qué frases entran en la tanda. Sin números, entran las 60.

    Devuelve pares `(número, frase)` con el número **empezando en 1**, que es el que
    se ve en pantalla: así lo que se lee en la salida se puede volver a pedir tal
    cual en la línea de comandos.

    🔑 **Se valida antes de gastar, no durante.** Un número fuera de rango con la
    tanda ya empezada dejaría llamadas pagadas y ningún informe.

    :raises SystemExit: si algún número no es un entero dentro del rango. Se para
        con un mensaje, no con un traceback: quien corre esto está en una terminal.
    """
    if not numbers:
        return list(enumerate(SENTENCES, start=1))

    chosen = []

    for raw in numbers:
        if not raw.isdigit() or not 1 <= int(raw) <= len(SENTENCES):
            raise SystemExit(
                f"'{raw}' no es un numero de frase valido: se esperaba un entero "
                f"entre 1 y {len(SENTENCES)}, y no se ha llamado a nadie."
            )
        number = int(raw)
        chosen.append((number, SENTENCES[number - 1]))

    return chosen


def save_replies(records: list[dict], path: Path | None = None) -> None:
    """Guarda las respuestas de la corrida, una por línea.

    🚨 **Escribe de una vez al final, no según van llegando.** Es lo contrario de
    `trace.record`, y por un motivo distinto: aquella apunta la vida de la app —que
    no termina— y esta apunta una tanda que sí. Escribir al final deja el archivo
    con la corrida entera o sin ella, nunca a medias de una que se cortó.

    ⚠️ **Y sobrescribe, no añade.** Dos corridas seguidas mezcladas en un archivo
    serían dos modelos o dos rúbricas revueltos sin forma de separarlos — que es
    justo el error que `[L-071]` describe. Lo que interesa mirar es la última.
    """
    path = path or replies_file()

    with path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def tally_breaks(replies: list[str]) -> Counter:
    """Cuenta, sobre un montón de respuestas, cuántas rompen cada promesa.

    🔑 **Función aparte y sin red ni dinero, y por eso se puede probar.** Es la
    misma idea que `split_verdict` estando fuera de `judge_grammar`: partir y
    contar no necesita llave, así que se prueba con cadenas sueltas.

    ⚠️ **Una respuesta puede romper varias**, así que la suma de la cuenta NO es
    el número de respuestas rotas. Las dos cifras se enseñan por separado en el
    informe, porque confundirlas es lo fácil.
    """
    counted: Counter = Counter()

    for reply in replies:
        for promise in rubric_check.check_reply(reply):
            counted[promise] += 1

    return counted


def report_lines(replies: list[str], model: str) -> list[str]:
    """El informe, en ASCII puro y como lista de líneas para poder probarlo.

    📌 Devuelve líneas en vez de imprimir: así un test lee lo que diría sin
    capturar la salida, que es lo que hace `verdict_for` en `measure_tutor`.
    """
    total = len(replies)
    counted = tally_breaks(replies)
    clean = sum(1 for reply in replies if not rubric_check.check_reply(reply))

    lines = [
        "",
        "=== FORMA DE LA RUBRICA ===",
        f"    modelo:                 {model}",
        f"    respuestas medidas:     {total} de {len(SENTENCES)}",
        f"    limpias (0 fallos):     {clean} de {total}",
        "",
        "    Por promesa (una respuesta puede romper varias):",
    ]

    # Se recorre `PROMISES` ordenado, no las claves de la cuenta: una promesa con
    # cero fallos TIENE que salir en el informe. Si solo se listara lo contado,
    # una promesa que nunca falla desaparece del papel — y desaparecer se lee
    # igual que "no la estoy mirando".
    for promise in sorted(rubric_check.PROMISES):
        lines.append(f"      {promise:<22} {counted[promise]:>3}")

    lines += [
        "",
        "    Este informe NO dice si el veredicto acierta: solo si la respuesta",
        "    vino con la forma que la rubrica pidio. Etiquetar las 60 frases es",
        "    la otra mitad del paso 9.",
    ]

    if total < len(SENTENCES):
        lines += [
            "",
            f"    AVISO: faltan {len(SENTENCES) - total} respuestas. La tanda se",
            "    corto antes de acabar, asi que estos numeros son parciales y no",
            "    valen como linea base.",
        ]

    return lines


def main(numbers: list[str] | None = None) -> None:
    # 🚨 **Primero el `.env`, o no hay llave.** `require_anthropic_key` lee el
    # ENTORNO, y la llave vive en `.env`: sin esta línea el guion muere antes de
    # llamar a nadie. Mismo orden que `measure_tutor.py:407`.
    #
    # 🔴 **Escrito después de que faltara.** Los 19 tests de este archivo estaban
    # en verde y el guion no arrancaba: ninguno llama a `main()` —hace red— así que
    # ninguno podía cazarlo. **Es `PI-4` exacto: lo que no se ha corrido no está
    # terminado, aunque el código exista y la suite esté verde.**
    #
    # ⚠️ Y queda dicho que **nadie lo vigila**: `tests/test_measure_tutor.py` no
    # tiene freno para esto tampoco. Los dos guiones dependen de que quien los
    # escriba se acuerde.
    config.load_env_file()

    # 🚨 **Se elige la tanda ANTES de tocar la llave**, porque un numero mal
    # escrito tiene que parar el guion sin haber llamado a nadie.
    plan = chosen_sentences(numbers or [])

    key = config.require_anthropic_key()

    # Los frenos de PRODUCCION, no los de la bascula. El porque esta arriba.
    inner = anthropic.Anthropic(
        api_key=key,
        max_retries=tools.MAX_RETRIES,
        timeout=tools.TIMEOUT,
    )

    # 🚨 **El tope es el tamano de ESTA tanda, no el de las 60.** Un tope holgado
    # cazaria el bucle roto decenas de llamadas despues, y esas ya se pagaron.
    calls = len(plan)

    print("=== EVAL DE LA FORMA DE LA RUBRICA ===")
    print(f"    modelo:                 {tools.MODEL_NAME}")
    print(f"    frases de esta tanda:   {calls} de {len(SENTENCES)}")
    print(f"    tope de la tanda:       {calls} llamadas")
    print(f"    coste estimado:         {calls} x ${COST_PER_CALL_USD}"
          f" = ${calls * COST_PER_CALL_USD:.4f}")
    print(f"    read de produccion:     {tools.TIMEOUT.read} s"
          " (NO se sube: no se mide el reloj)")
    print(f"    respuestas a:           {replies_file(calls)}")
    print("")

    budget = CallBudget(max_calls=calls)
    replies: list[str] = []
    records: list[dict] = []

    # 🔴 **`position` y `number` son distintos, y mezclarlos imprimia `[12/10]`.**
    # `number` es la frase en la lista de 60; `position` es por donde va esta tanda.
    # Con una tanda parcial el primero se sale del segundo, y la cuenta de progreso
    # dejaba de significar nada. Visto en la corrida de las 10.
    for position, (number, sentence) in enumerate(plan, start=1):
        client = ReplyRecordingClient(inner, budget)

        started = time.monotonic()
        try:
            judge_grammar(sentence, client=client)
        except CallBudgetExceeded as error:
            # Se para y se ensena lo medido. Perder los datos ya costo dinero.
            print(f"\n[{number}] PRESUPUESTO AGOTADO: {error}")
            break
        except TutorUnavailableError as error:
            # Se para, no se reintenta. Insistir es lo que gasta saldo sin
            # aprender nada. Un 429 del limite por minuto entra por aqui.
            elapsed = time.monotonic() - started
            print(f"\n[{number}] CORTADO tras {elapsed:.2f} s: {error}")
            print(f"    la peticion salio: {'si' if error.request_sent else 'no'}")
            break

        reply = client.replies[-1]
        replies.append(reply)

        broken = rubric_check.check_reply(reply)

        # 🚨 **La frase entra aqui porque es INVENTADA** (`measure_tutor.SENTENCES`).
        # Guardarla es lo que hace el archivo util: sin saber que se pregunto, la
        # respuesta no se puede juzgar. Y es la condicion que `sentences_are_invented`
        # comprueba antes de dejar promover nada a `_persistence/` (`[D-093]`).
        #
        # 🔑 **`rubric` viaja en la FILA ademas de en el nombre**, a proposito: asi el
        # corpus se explica solo aunque alguien mueva o renombre el archivo.
        records.append(
            {
                "number": number,
                "sentence": sentence,
                "reply": reply,
                "broken": sorted(broken),
                "model": tools.MODEL_NAME,
                "rubric": rubric_fingerprint(),
            }
        )

        mark = "ok  " if not broken else "ROTO"
        detail = "" if not broken else "  " + " ".join(sorted(broken))
        print(f"[{position:>2}/{calls}] frase {number:>2}  {mark}{detail}")

    # 🚨 **Se guarda ANTES de imprimir el informe.** Si escribir fallara, es mejor
    # enterarse con el traceback que despues de un informe bonito que da la
    # sensacion de que la corrida quedo entera.
    save_replies(records, path=replies_file(calls))

    for line in report_lines(replies, tools.MODEL_NAME):
        print(line)

    print("")
    print(f"Las {len(records)} respuestas estan en {replies_file(calls)}")
    print("El gasto real se lee en la consola de Anthropic, no aqui (regla 6).")


if __name__ == "__main__":
    main(sys.argv[1:])
