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

📌 **La puerta de salida ya estaba escrita, y es de `[D-092]`:** un corpus se
promueve a `_persistence/corpus/` **cuando algún eje de su nombre deja de
coincidir con producción** —modelo, fecha, huella de rúbrica o marca de
selección—, y el disparador va pegado al commit que mueve `MODEL` o
`GRAMMAR_RUBRIC`. Hasta ese día el archivo vive aquí. Se escribe al nacer la
carpeta y no el día que haga falta, porque una antesala sin salida escrita es la
misma cosa en dos sitios con fecha diferida.

🔻 **Y `[D-092]` describe este agujero él mismo**, al descartar la propuesta
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

import json
from pathlib import Path

from measure_tutor import SENTENCES

# La carpeta es hermana de `_persistence/corpus/` en el disco, pero no en la
# vida del archivo: de aquí se sale hacia allá. El porqué, arriba.
REPLIES_DIR = Path(__file__).parent / "_persistence" / "replies"

# 🚨 **Cerrado, y todos obligatorios.** Al revés que `labels.py`, aquí no hay
# campos opcionales: estas filas las escribe `save_replies`, no una persona a
# mano, así que una fila incompleta no es un descuido de tecleo — es que el
# escritor cambió y nadie se enteró.
ALLOWED_FIELDS = frozenset({"number", "sentence", "reply", "broken", "model", "rubric"})


def archived_files() -> list[Path]:
    """Los archivos de respuestas que hay HOY en la carpeta, buscados, no listados.

    🔑 Con `glob` y no con una lista escrita a mano, por lo mismo que
    `_frozen_corpora` en los tests: una lista solo vigila lo que alguien se acordó
    de apuntar, y el que se cuela es justo el que nadie apuntó.
    """
    return sorted(REPLIES_DIR.glob("*.jsonl"))


def row_problems(row: dict) -> list[str]:
    """Qué le pasa a esta fila. Lista vacía = está bien formada.

    🔑 Devuelve los problemas en vez de romper, para verlos todos de un tirón.

    ⚠️ Comprueba **forma**, no contenido: lo que diga `reply` no lo juzga nadie.
    """
    problems = []

    fields = set(row)
    missing = ALLOWED_FIELDS - fields
    extra = fields - ALLOWED_FIELDS

    if missing:
        problems.append(f"le faltan campos: {sorted(missing)}")

    # 🚨 Un campo de más es superficie ciega nueva. Se rechaza aunque parezca
    # inofensivo: `reply` ya es toda la que se acepta, y se acepta sabiéndolo.
    if extra:
        problems.append(f"trae campos que no existen: {sorted(extra)}")

    for field in ("reply", "model", "rubric"):
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


def name_matches_rows(path: Path, rows: list[dict]) -> list[str]:
    """¿El nombre del archivo dice lo mismo que sus filas?

    🔑 **Existe porque el nombre es el criterio de promoción de `[D-092]`.** Si el
    nombre miente sobre el modelo o la rúbrica, la regla que decide cuándo este
    archivo se muda a `corpus/` decide sobre un dato falso — y lo hace en silencio.
    """
    problems = []

    for field in ("model", "rubric"):
        values = {row.get(field) for row in rows if field in row}

        if len(values) > 1:
            problems.append(f"las filas traen varios {field}: {sorted(values)}")
            continue

        if values and str(next(iter(values))) not in path.name:
            problems.append(
                f"el nombre no lleva el {field} de las filas "
                f"({next(iter(values))!r})"
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
        broken = [
            (row.get("number"), problems)
            for row, problems in ((row, row_problems(row)) for row in rows)
            if problems
        ]

        for number, problems in broken:
            print(f"  fila {number}: {'; '.join(problems)}")

        for problem in name_matches_rows(path, rows):
            print(f"  nombre: {problem}")

        print(f"{path.name}: {len(rows)} filas, {len(broken)} mal formadas.")


if __name__ == "__main__":
    main()
