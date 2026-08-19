"""Las respuestas del juez, archivadas: la otra mitad del cruce de `T-111`.

🚨 **Por qué existe esta carpeta, y por qué no bastaba con dejarlas en `data/`.**
`[D-097]` mandó las etiquetas a `_persistence/` con un argumento de una línea:
*`data/` es un disco sin copia y fuera de Git* (`[C-009]`). Ese argumento vale
igual para las respuestas y no se le había aplicado — así que las dos mitades del
mismo cruce vivían en regímenes opuestos, y la desprotegida era la que costó
dinero.

🔑 **Y no es que no se puedan recomprar: es que no se pueden repetir.** `[D-096]`
fija `$0,00342` por llamada, o sea `$0,21` las sesenta. Pero el juez no es
determinista: volver a comprarlas da OTRAS respuestas, y entonces el número que
salga del cruce ya no se puede reproducir ni auditar. Lo que se protege aquí no
es el archivo — es que la medición siga siendo comprobable mañana.

⚠️ **Esta carpeta es una ANTESALA, no una hermana de `_persistence/corpus/`.**
Con las etiquetas la separación era limpia —etiquetas contra rúbrica viva, corpus
contra rúbrica muerta, vidas opuestas—. Aquí no: lo que se guarda es un corpus de
respuestas cuya única diferencia con `corpus/` es que su rúbrica **todavía vive**.

📌 **La puerta de salida ya estaba escrita, y desde `[D-102]` es más simple:** un
corpus se promueve a `_persistence/corpus/` **cuando su SELLO deja de coincidir
con el de producción**, y el disparador va pegado al commit que mueve la
configuración. ⚠️ **Antes eran cuatro comparaciones —y les faltaban dos:** ni el
conjunto de frases ni `rubric_check.py` entraban en el nombre. Hasta ese día el archivo vive aquí. Se escribe al nacer la
carpeta y no el día que haga falta, porque una antesala sin salida escrita es la
misma cosa en dos sitios con fecha diferida.

🔻 **Y `~~D-092~~` describe este agujero él mismo**, al descartar la propuesta
rival: *"al crear un corpus la rúbrica está viva por definición, así que nada se
guardaría nunca al nacer — la evidencia esperaría en `data/`, ignorado por Git y
en un solo disco, exactamente mientras se la considera todavía no valiosa"*. Esta
carpeta es esa espera, con respaldo.

⚠️ **Alcance honesto del portero, dicho antes de que nadie lea su verde como una
auditoría.** Aquí la prosa libre no es un campo lateral: **es la carga entera del
archivo.** Sesenta párrafos generados por un modelo, en un repositorio **público**
(`[C-007]`).

- `number` y `sentence` se cotejan contra `SENTENCES` — la cerradura de `PI-8`.
- `model` y `rubric` se cotejan contra el nombre del archivo.
- **`reply` es prosa libre y NINGÚN PROGRAMA LA AUDITA.** Se sabe cuál es y se
  dice aquí. Hoy la puerta es inocente —el modelo contesta a frases inventadas,
  así que solo puede citar frases inventadas—, **pero eso es una propiedad de hoy,
  no del camino.**
- Cualquier campo que no esté en `ALLOWED_FIELDS` se rechaza, para que la
  superficie ciega no crezca sin que nadie lo note. **El campo que se cuele mañana
  es justo el que nadie mirará.**

Es el mismo movimiento —y la misma honestidad— que `labels.row_problems` y que
`eval_rubric.sentences_are_invented`, que declara en voz alta que no audita
`reply`. Ver `[D-093]`.

🔴 **Un archivo con este mismo nombre en `data/` NO es este archivo.** El nombre
lleva fecha sin hora (`T-109`) y `save_replies` abre en `"w"`: otra corrida entera
el mismo día crea uno igual de nombre y distinto de contenido. **El original vive
aquí y lo respalda Git.** Quien vaya a cruzar lee esta carpeta, no `data/`.
"""

import hashlib
import json
from pathlib import Path

from measure_tutor import SENTENCES

# La carpeta es hermana de `_persistence/corpus/` en el disco, pero no en la
# vida del archivo: de aquí se sale hacia allá. El porqué, arriba.
REPLIES_DIR = Path(__file__).parent / "_persistence" / "replies"

# 🚨 **Cerrados, y todos obligatorios dentro de su generación.** Al revés que
# `labels.py`, aquí no hay campos opcionales: estas filas las escribe
# `save_replies`, no una persona a mano, así que una fila incompleta no es un
# descuido de tecleo — es que el escritor cambió y nadie se enteró.
#
# 🔻 **Hay DOS juegos porque `[D-102]` manda no renombrar lo viejo**, y esa cláusula
# —correcta: renombrar evidencia congelada y **pagada** es peor— crea requisitos que
# nadie escribió. Ya van dos: el nombre y ahora el esquema de la fila.
#
# ⚠️ **Y la salida cómoda era hacer las huellas nuevas OPCIONALES. Es la mala.**
# No es "un `if` menos": es cambiar lo que el portero afirma. Una fila **de
# generación nueva** a la que le faltara una huella pasaría en verde — y es justo la
# fila que tiene que cantar, porque de ella se recalcula el sello. Sería comprar
# silencio en el sitio donde se acaba de poner el instrumento.
CAMPOS_LEGADO = frozenset({"number", "sentence", "reply", "broken", "model", "rubric"})

# Las tres huellas por separado: de aquí se recalcula el sello del nombre.
CAMPOS_SELLADOS = CAMPOS_LEGADO | {"sentences", "detector"}

# 🔑 **La generación LEGADO está muerta por construcción, y esto acota el coste.**
# Desde `[D-102]`, `save_replies` solo sabe escribir nombres sellados: **no puede
# nacer un archivo legado nuevo.** Así que esta rama se escribe una vez, se prueba
# contra los archivos que existen hoy y **no crece nunca**. Es una cola, no una
# arquitectura — y lo sostiene `test_the_legacy_generation_never_grows`.
LEGACY_FILES = frozenset({
    "eval_replies_claude-opus-5_2026-08-18_rubric-bbf4be38_full.jsonl",
})


def generation_of(path: Path) -> frozenset[str]:
    """De qué generación es este archivo, mirando su nombre. Devuelve sus campos.

    🚨 **UNA sola función lo decide, y la usan los dos porteros.** `row_problems`
    necesita saberlo para los campos, y `name_matches_rows` para elegir su rama. Si
    cada uno lo dedujera por su cuenta, serían **dos detectores de generación que
    pueden discrepar** — la misma cosa escrita en dos sitios, que es el bicho que ya
    se pagó una vez en este proyecto.

    📌 **Y que la generación entre por el NOMBRE no es un instrumento certificándose
    a sí mismo**, aunque se le parezca. El nombre es **externo a las filas**, así que
    el cruce muerde en las dos direcciones: nombre legado con filas nuevas da
    *"campos que no existen"*; nombre sellado con filas viejas da *"faltan campos"*.
    No se certifica: se contrasta.
    """
    return CAMPOS_SELLADOS if "_run-" in path.name else CAMPOS_LEGADO


def archived_files() -> list[Path]:
    """Los archivos de respuestas que hay HOY en la carpeta, buscados, no listados.

    🔑 Con `glob` y no con una lista escrita a mano, por lo mismo que
    `_frozen_corpora` en los tests: una lista solo vigila lo que alguien se acordó
    de apuntar, y el que se cuela es justo el que nadie apuntó.
    """
    return sorted(REPLIES_DIR.glob("*.jsonl"))


def row_problems(row: dict, required: frozenset[str]) -> list[str]:
    """Qué le pasa a esta fila. Lista vacía = está bien formada.

    🔑 Devuelve los problemas en vez de romper, para verlos todos de un tirón.

    ⚠️ Comprueba **forma**, no contenido: lo que diga `reply` no lo juzga nadie.

    :param required: el juego de campos de su generación, de `generation_of()`.

    🚨 **Sin valor por defecto, a propósito.** Un `required=CAMPOS_SELLADOS` por
    omisión haría que cada llamada existente eligiera **en silencio**, y que quien
    añada una llamada mañana heredara la elección sin pensarla. Es `[L-082]`: un
    valor por defecto es acordarse por omisión. Obligatorio, cada sitio dice de qué
    generación habla.

    📌 **Y es una constante con nombre, no un `legacy=True`.** Un booleano en el
    sitio de la llamada se lee mal invertido y no dice nada; `CAMPOS_LEGADO` es una
    afirmación que se lee sola. Si algún día hay una tercera generación, el sitio de
    la llamada no cambia de forma.
    """
    problems = []

    fields = set(row)
    missing = required - fields
    extra = fields - required

    if missing:
        problems.append(f"le faltan campos: {sorted(missing)}")

    # 🚨 Un campo de más es superficie ciega nueva. Se rechaza aunque parezca
    # inofensivo: `reply` ya es toda la que se acepta, y se acepta sabiéndolo.
    if extra:
        problems.append(f"trae campos que no existen: {sorted(extra)}")

    for field in ("reply", "model", "rubric", "sentences", "detector"):
        if field in row and not isinstance(row[field], str):
            problems.append(f"el campo {field!r} tiene que ser texto")

    if "broken" in row and not isinstance(row["broken"], list):
        problems.append("el campo 'broken' tiene que ser una lista")

    number = row.get("number")
    sentence = row.get("sentence")

    # `bool` es subclase de `int` en Python, así que `True` pasaría por un número
    # sin este filtro. Mismo motivo que en `labels.row_problems`.
    if isinstance(number, bool) or not isinstance(number, int):
        problems.append(f"el numero {number!r} no es un entero")
        return problems

    if not 1 <= number <= len(SENTENCES):
        problems.append(f"el numero {number} esta fuera de 1..{len(SENTENCES)}")
        return problems

    # 🚨 **La cerradura de `PI-8`, y la misma de `labels.py`: el texto se cotea
    # contra `SENTENCES`.** Es por donde entraría la frase de una persona usando
    # la app, y de paso caza que alguien reordene la lista y deje las sesenta
    # filas apuntando a la frase de al lado sin dar un solo error.
    if sentence != SENTENCES[number - 1]:
        problems.append(
            f"la frase no es la numero {number} de SENTENCES: "
            f"guardada {sentence!r}, hoy {SENTENCES[number - 1]!r}"
        )

    return problems


def load_replies(path: Path) -> list[dict]:
    """Lee un archivo de respuestas archivado.

    :raises SystemExit: si alguna línea no es JSON, diciendo **qué línea**. Mismo
        criterio que `labels.load_labels`: quien corre esto está en una terminal,
        y un `JSONDecodeError` crudo obliga a buscar a ojo.
    """
    rows = []

    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        if not line.strip():
            continue

        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as error:
            raise SystemExit(
                f"{path.name}, linea {number}: no es JSON valido ({error.msg}). "
                "No se ha leido nada mas."
            ) from error

    return rows


def _one_value(rows: list[dict], field: str) -> tuple[str | None, list[str]]:
    """El valor único de un campo en todas las filas, o el problema de que no lo sea."""
    values = {row.get(field) for row in rows if field in row}

    if len(values) > 1:
        return None, [f"las filas traen varios {field}: {sorted(map(str, values))}"]

    return (str(next(iter(values))) if values else None), []


def name_matches_rows(path: Path, rows: list[dict]) -> list[str]:
    """¿El nombre del archivo dice lo mismo que sus filas?

    🔑 **Existe porque el nombre es el criterio de promoción.** Si el nombre miente,
    la regla que decide cuándo este archivo se muda a `corpus/` decide sobre un dato
    falso — y lo hace en silencio. Desde `[D-102]` ese criterio es **el sello**.

    🚨 **DOS ramas, y la vieja NO se salta: se comprueba.** La cláusula de `[D-102]`
    manda no renombrar lo anterior —es evidencia congelada y **pagada**—, así que
    aquí siguen llegando nombres `rubric-`. ⚠️ **La salida cómoda sería ignorar los
    nombres que no se reconocen: eso deja el test en verde y el portero CIEGO sobre
    el único archivo archivado que existe.** Es la misma especie que el guardián que
    se quedó verde y hueco al cambiar el nombre; se dice aquí para que no se
    reintroduzca al refactorizar.

    🔑 **Rama sellada: se RECALCULA el sello desde las filas y se exige igualdad
    exacta.** Una comprobación que cubre las tres huellas, donde la vieja cubría una
    sola y por subcadena. Es lo que hace segura la redundancia nombre/fila: lo mismo
    en dos sitios solo miente cuando nadie compara.
    """
    problems = []

    if generation_of(path) == CAMPOS_LEGADO:
        # Rama LEGADO — cerrada y decreciente. El cruce de antes de `[D-102]`:
        # subcadena, y solo sobre los dos campos que aquel nombre llevaba.
        for field in ("model", "rubric"):
            value, trouble = _one_value(rows, field)
            problems += trouble

            if value is not None and value not in path.name:
                problems.append(f"el nombre no lleva el {field} de las filas ({value!r})")

        return problems

    # Rama SELLADA. El modelo se sigue cruzando por subcadena —va literal en el
    # nombre—; las tres huellas se cruzan de una vez, recalculando el sello.
    value, trouble = _one_value(rows, "model")
    problems += trouble

    if value is not None and value not in path.name:
        problems.append(f"el nombre no lleva el model de las filas ({value!r})")

    pieces = []
    for field in ("rubric", "sentences", "detector"):
        value, trouble = _one_value(rows, field)
        problems += trouble

        if value is None:
            problems.append(f"las filas no traen {field}: el sello no se puede recalcular")
        else:
            pieces.append(value)

    if len(pieces) == 3:
        seal = hashlib.sha256("".join(pieces).encode("utf-8")).hexdigest()[:8]

        if f"_run-{seal}_" not in path.name:
            problems.append(
                f"el sello de las filas es {seal!r} y el nombre no lo lleva: "
                "el archivo dice ser un experimento distinto del que contiene"
            )

    return problems


def main() -> None:
    """Valida lo que hay archivado. No compra respuestas ni cruza nada."""
    files = archived_files()

    if not files:
        print(f"No hay nada archivado en {REPLIES_DIR}")
        return

    for path in files:
        rows = load_replies(path)
        required = generation_of(path)
        broken = [
            (row.get("number"), problems)
            for row, problems in ((row, row_problems(row, required)) for row in rows)
            if problems
        ]

        for number, problems in broken:
            print(f"  fila {number}: {'; '.join(problems)}")

        for problem in name_matches_rows(path, rows):
            print(f"  nombre: {problem}")

        print(f"{path.name}: {len(rows)} filas, {len(broken)} mal formadas.")


if __name__ == "__main__":
    main()
