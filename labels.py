"""El etiquetado a mano de las 60 frases: la verdad de referencia contra la que
se mide al juez.

🚨 **Por qué existe este archivo y por qué no se puede volver a comprar.**
`measure_tutor.SENTENCES` dice de sí misma que mezcla *"unas correctas y otras
con un error claro"*, pero es una lista plana de 60 cadenas: **en ningún sitio
está escrito cuáles son cuáles.** Se supo al escribirlas y no se anotó. Así que
esto no reproduce un dato que exista en otro lado — **crea el único que falta**
(`[D-097]`, `T-106`).

🔑 **Y por eso vive en `_persistence/labels/` y no en `data/`.** El corpus de
respuestas cuesta `$0,20` y se vuelve a comprar; sesenta juicios humanos **no
tienen precio**, y `data/` es un disco sin copia y fuera de Git (`[C-009]`).

🔒 **Tampoco vive en `_persistence/corpus/`, que es la hermana de al lado.**
Aquella carpeta guarda lo que ya **no** es producción, y
`test_no_frozen_corpus_carries_the_live_rubric` lo hace cumplir. Estas etiquetas
nacen contra la rúbrica **viva** y valen mientras viva: son vidas opuestas, y
meterlas allí pondría ese test en rojo mañana. Ver `[D-092]` para el criterio de
la otra carpeta.

⚠️ **Alcance honesto del portero de este módulo, dicho antes de que nadie lea su
verde como una auditoría.** Un programa **no** puede juzgar prosa: un detector de
*"¿este texto lleva datos de una persona?"* pasaría en verde sobre lo que no sabe
ver, y ese verde se leería como comprobado. Un instrumento ciego no da un dato
falso: da silencio, y el silencio se confunde con confirmación. Lo que este módulo
hace es lo otro — **estrechar la superficie no auditable hasta un solo campo con
nombre**:

- `number` y `sentence` se cotejan contra `SENTENCES`.
- `verdict` está cerrado a un conjunto fijo, comprobable por completo.
- **`note` es prosa libre y NINGÚN PROGRAMA LA AUDITA.** Es el único campo así, y
  se sabe cuál es. Este repositorio es **público** (`[C-007]`): lo que se escriba
  ahí se publica.
- Cualquier otro campo se rechaza, para que la superficie ciega no crezca sin que
  nadie lo note.

Es el mismo movimiento —y la misma honestidad— que `eval_rubric.sentences_are_invented`,
que declara en voz alta que no audita `reply`. Ver `[D-093]`.

📌 **Cuando toque comparar, el veredicto del juez se saca con
`app.tools.split_verdict`, no con un lector nuevo.** El corpus **no guarda
`outcome`**: sus filas son `number`, `sentence`, `reply`, `broken`, `model` y
`rubric`, y el veredicto vive solo dentro de `reply`. Escribir aquí un segundo
lector de esa primera línea deja dos que un día discrepan — que es la razón por la
que `rubric_check` **importa** `VERDICT_CORRECT` en vez de copiarlo (`[D-091]`).
⚠️ Y el lector bueno es `split_verdict`, **no** `rubric_check.learner_message`:
aquella contesta *si* había palabra clave y tira **cuál** de las dos era.
"""

import json
from pathlib import Path

from measure_tutor import SENTENCES

# La carpeta es HERMANA de `_persistence/corpus/`, no hija. El porqué, arriba.
LABELS_DIR = Path(__file__).parent / "_persistence" / "labels"

# 🔑 **Un solo archivo y sin ejes en el nombre — al revés que el corpus (`[D-092]`).**
# El corpus se nombra por modelo y rúbrica porque una respuesta depende de las dos.
# Una etiqueta no: dice si LA FRASE está mal escrita, y eso no cambia porque se
# mueva el modelo ni porque se reescriba la rúbrica. Sin ejes tampoco hay dos
# corridas que se pisen, que es el bicho de `T-109`.
LABELS_FILE = LABELS_DIR / "sentence_labels.jsonl"

# Los tres valores que puede poner quien etiqueta.
#
# 🚨 **`unclear` es el tercero a propósito: es gratis hoy e imposible de recuperar
# después.** Con solo `correct`/`wrong`, una frase discutible se resuelve a la
# fuerza hacia un lado y la duda se evapora dentro de `note`, que no audita nadie.
# Eso **mueve la tasa de acierto medida del juez** en la dirección en que se haya
# resuelto. El día que alguien descubra que una frase era discutible, ya estará
# clasificada como una de las dos y **no habrá forma de saber cuáles se dudaron**.
LABEL_CORRECT = "correct"
LABEL_WRONG = "wrong"
LABEL_UNCLEAR = "unclear"

LABEL_VERDICTS = frozenset({LABEL_CORRECT, LABEL_WRONG, LABEL_UNCLEAR})

# 🔑 **Y `None` NO es un cuarto veredicto: es "todavía no la ha mirado nadie".**
# Se separa de `unclear` por el mismo argumento que hizo nacer a `unclear`: meter
# "sin etiquetar" dentro de "dudosa" borra una distinción que después no se
# recupera — el esqueleto nacería ya opinando. Cuando `T-106` termine no queda
# ningún `None`.
UNLABELLED = None

# Los campos que puede traer una fila. Cerrado a propósito: un campo nuevo es
# superficie que nadie audita, y `note` ya es toda la que se acepta.
REQUIRED_FIELDS = frozenset({"number", "sentence", "verdict"})
OPTIONAL_FIELDS = frozenset({"note"})


def blank_labels() -> list[dict]:
    """El esqueleto: las 60 frases sin etiquetar, en el orden de `SENTENCES`.

    Sale con `verdict` a `None` — sin opinión. Rellenarlo es `T-106`, y lo hace
    una persona.
    """
    return [
        {"number": number, "sentence": sentence, "verdict": UNLABELLED}
        for number, sentence in enumerate(SENTENCES, start=1)
    ]


def row_problems(row: dict) -> list[str]:
    """Qué le pasa a esta fila. Lista vacía = está bien formada.

    🔑 **Devuelve los problemas en vez de romper**, para que quien etiqueta los vea
    todos de un tirón y no los descubra de uno en uno.

    ⚠️ Comprueba **forma**, no criterio: que alguien ponga `wrong` en una frase que
    estaba bien es un error que ningún programa puede ver.
    """
    problems = []

    fields = set(row)
    missing = REQUIRED_FIELDS - fields
    extra = fields - REQUIRED_FIELDS - OPTIONAL_FIELDS

    if missing:
        problems.append(f"le faltan campos: {sorted(missing)}")

    # 🚨 Un campo de más es superficie ciega nueva. Se rechaza aunque parezca
    # inofensivo: `note` es el único sitio donde cabe prosa, y se sabe cuál es.
    if extra:
        problems.append(f"trae campos que no existen: {sorted(extra)}")

    verdict = row.get("verdict", UNLABELLED)
    if verdict is not UNLABELLED and verdict not in LABEL_VERDICTS:
        problems.append(f"veredicto {verdict!r} no esta en {sorted(LABEL_VERDICTS)}")

    if "note" in row and not isinstance(row["note"], str):
        problems.append("la nota tiene que ser texto")

    number = row.get("number")
    sentence = row.get("sentence")

    # `bool` es subclase de `int` en Python, así que `True` pasaría por un número
    # sin este filtro. Vale poco y cierra una rendija tonta.
    if isinstance(number, bool) or not isinstance(number, int):
        problems.append(f"el numero {number!r} no es un entero")
        return problems

    if not 1 <= number <= len(SENTENCES):
        problems.append(f"el numero {number} esta fuera de 1..{len(SENTENCES)}")
        return problems

    # 🚨 **La etiqueta se pega al TEXTO, no solo a la posición.** El número es la
    # posición dentro de `SENTENCES`; el día que alguien inserte una frase o
    # reordene la lista, las sesenta etiquetas apuntarían a la frase de al lado
    # **sin dar un solo error**. Cotejar las dos convierte ese fallo mudo en uno
    # que se ve.
    if sentence != SENTENCES[number - 1]:
        problems.append(
            f"la frase no es la numero {number} de SENTENCES: "
            f"guardada {sentence!r}, hoy {SENTENCES[number - 1]!r}"
        )

    return problems


def load_labels(path: Path | None = None) -> list[dict]:
    """Lee un archivo de etiquetas.

    No comprueba el CONTENIDO —de eso se encarga `row_problems`—, pero sí se para
    con un mensaje si una línea no es JSON.

    🚨 **Y dice QUÉ LÍNEA, que es lo único que sirve aquí.** Esto se corre mientras
    alguien edita sesenta líneas a mano: una coma de más o una comilla sin cerrar
    es el fallo más probable de todos, y un `JSONDecodeError` crudo obliga a buscar
    a ojo por un archivo de sesenta filas.

    :raises SystemExit: si alguna línea no es JSON. Se para con un mensaje, no con
        un traceback — mismo criterio que `eval_rubric.chosen_sentences`: quien
        corre esto está en una terminal.
    """
    path = path or LABELS_FILE

    rows = []

    # `enumerate` desde 1 porque el número que hace falta es el que enseña el
    # editor de texto, no el índice de Python.
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


def save_labels(rows: list[dict], path: Path | None = None) -> Path:
    """Escribe las etiquetas, una fila por juicio.

    🚨 **Se niega a escribir una fila mal formada.** Un archivo de etiquetas medio
    roto cuesta trabajo humano de rehacer, no dinero de volver a gastar.
    """
    path = path or LABELS_FILE

    for row in rows:
        problems = row_problems(row)
        if problems:
            raise ValueError(f"fila {row.get('number')!r}: {'; '.join(problems)}")

    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows),
        encoding="utf-8",
    )
    return path


def missing_numbers(rows: list[dict]) -> list[int]:
    """Qué frases de `SENTENCES` no tienen fila en este archivo."""
    present = {row.get("number") for row in rows}
    return [n for n in range(1, len(SENTENCES) + 1) if n not in present]


def progress(rows: list[dict]) -> tuple[int, int]:
    """Cuántas están etiquetadas, sobre las que TENDRÍA que haber.

    🚨 **El denominador sale de `SENTENCES`, NO de `len(rows)`, y ahí estaba el
    bicho.** Editando sesenta líneas a mano se pierde una — es exactamente así
    como se pierde una línea—, y con el total sacado del propio archivo la salida
    diría `50 de 50 etiquetadas, 0 filas mal formadas`: completo y limpio. Es
    `[L-071]`: **cuadrar contra un agregado no es cuadrar**, porque el agregado
    también encogió.

    ⚠️ Que falte una fila lo caza `test_the_labels_cover_every_sentence_exactly_once`,
    pero eso vive en `pytest` — y lo que se corre sesenta veces durante `T-106` es
    `python labels.py`. Un control que solo existe donde nadie mira no es control.
    """
    done = sum(1 for row in rows if row.get("verdict") is not UNLABELLED)
    return done, len(SENTENCES)


def main() -> None:
    """Valida el archivo de etiquetas y dice por dónde va. No etiqueta nada."""
    if not LABELS_FILE.exists():
        written = save_labels(blank_labels())
        print(f"Esqueleto creado en {written}")
        print(f"{len(SENTENCES)} frases sin etiquetar.")
        return

    rows = load_labels()
    broken = [
        (row.get("number"), problems)
        for row, problems in ((row, row_problems(row)) for row in rows)
        if problems
    ]

    for number, problems in broken:
        print(f"  fila {number}: {'; '.join(problems)}")

    # 🚨 **Las filas que FALTAN se cantan aparte**, porque son las únicas que
    # ningún bucle sobre `rows` puede encontrar: no están ahí para ser miradas.
    missing = missing_numbers(rows)
    if missing:
        print(f"  FALTAN filas para las frases: {missing}")

    done, total = progress(rows)
    print(
        f"{done} de {total} etiquetadas. "
        f"Filas mal formadas: {len(broken)}. Filas perdidas: {len(missing)}."
    )


if __name__ == "__main__":
    main()
