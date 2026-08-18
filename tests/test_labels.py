"""Los porteros de `_persistence/labels/`.

🚨 **Nacen en el MISMO commit que la carpeta, y ese es el punto entero de
`[D-097]`.** Una carpeta vacía no da miedo y por eso nadie vuelve a ponerle
puerta: el archivo que se cuela es siempre el que entró el día que todavía no
había portero.

⚠️ **Lo que estos tests NO hacen.** No juzgan si una etiqueta es acertada. Que
alguien ponga `wrong` en una frase que estaba bien escrita es un error que ningún
programa puede ver, y decirlo aquí importa: un verde que se lea como *"las
etiquetas están bien"* sería peor que no tener tests.
"""

import json
import subprocess
from pathlib import Path

import pytest

import labels
from measure_tutor import SENTENCES


def _label_files() -> list[Path]:
    """Los archivos de etiquetas que hay HOY, buscados y no listados.

    🔑 Con `glob` y no con una lista escrita a mano, por lo mismo que en
    `test_eval_rubric._frozen_corpora`: una lista solo vigila lo que alguien se
    acordó de apuntar, y el que se cuela es justo el que nadie apuntó.
    """
    return sorted(labels.LABELS_DIR.glob("*.jsonl"))


def test_the_labels_folder_is_not_empty():
    """⚠️ Un portero sobre una carpeta vacía es verde y no prueba nada.

    🔑 Es `[L-048]` aplicado al test de debajo: recorre un `glob`, y un `glob` sin
    resultados lo deja pasar en silencio. Si algún día la carpeta se vacía a
    propósito, este test se borra **a mano y con la razón escrita** (`PI-6`).
    """
    assert _label_files(), (
        "No hay etiquetas en _persistence/labels/: el portero de abajo esta "
        "pasando en vacio y no vigila nada."
    )


def test_every_label_file_is_well_formed():
    """El portero de verdad, echado sobre los archivos que hay en disco."""
    for path in _label_files():
        rows = labels.load_labels(path)

        assert rows, f"{path.name} esta vacio"

        for row in rows:
            problems = labels.row_problems(row)
            assert not problems, f"{path.name}, fila {row.get('number')}: {problems}"


def test_the_labels_cover_every_sentence_exactly_once():
    """Sesenta frases, sesenta etiquetas, sin repetidas ni huecos."""
    for path in _label_files():
        numbers = [row["number"] for row in labels.load_labels(path)]

        assert sorted(numbers) == list(range(1, len(SENTENCES) + 1)), (
            f"{path.name} no cubre las {len(SENTENCES)} frases una sola vez"
        )


def test_note_is_the_only_field_where_free_prose_fits():
    """🔒 La superficie que ningún programa audita es UN campo, y se sabe cuál.

    🚨 **Este test es el que sostiene la promesa del módulo.** Si mañana alguien
    añade un campo `comment` o `reason`, la prosa no auditada se duplica en
    silencio y el docstring de `labels.py` empieza a mentir sin que nada avise.
    """
    assert labels.OPTIONAL_FIELDS == {"note"}
    assert not (labels.REQUIRED_FIELDS & labels.OPTIONAL_FIELDS)

    row = dict(labels.blank_labels()[0], comment="algo escrito a mano")

    assert labels.row_problems(row), (
        "una fila con un campo de prosa nuevo entro sin protestar"
    )


def test_a_verdict_outside_the_three_is_rejected():
    """El conjunto está cerrado, y se comprueba entero."""
    for good in labels.LABEL_VERDICTS:
        row = dict(labels.blank_labels()[0], verdict=good)
        assert not labels.row_problems(row), f"{good} deberia valer"

    row = dict(labels.blank_labels()[0], verdict="ok")
    assert labels.row_problems(row), "'ok' no es uno de los tres y entro igual"


def test_unlabelled_is_not_the_same_as_unclear():
    """🚨 `None` es "nadie la ha mirado"; `unclear` es "la miré y es discutible".

    🔑 **Y por eso el esqueleto sale con `None` y no con `unclear`:** si naciera
    con `unclear`, una frase sin tocar sería indistinguible de una que alguien
    leyó y no supo clasificar — y esa segunda es justo la que hay que poder contar
    después. Es el mismo argumento que hizo nacer a `unclear` frente al binario,
    subido un piso.
    """
    assert labels.UNLABELLED is None
    assert labels.UNLABELLED not in labels.LABEL_VERDICTS

    blank = labels.blank_labels()

    assert all(row["verdict"] is labels.UNLABELLED for row in blank)
    assert labels.progress(blank) == (0, len(SENTENCES))

    labelled = [dict(row, verdict=labels.LABEL_UNCLEAR) for row in blank]

    assert labels.progress(labelled) == (len(SENTENCES), len(SENTENCES))


def test_a_label_pinned_to_the_wrong_text_is_caught():
    """🚨 El fallo mudo que este cotejo existe para hacer ruidoso.

    Si alguien inserta o reordena una frase en `SENTENCES`, las sesenta etiquetas
    apuntan a la frase de al lado **sin dar un solo error**. Guardar el texto junto
    al número convierte eso en un desajuste que se ve.
    """
    row = dict(labels.blank_labels()[0], sentence="She go to school every day")

    problems = labels.row_problems(row)

    assert problems, "una etiqueta pegada a otro texto paso el portero"
    assert "SENTENCES" in problems[0]


def test_a_number_outside_the_range_does_not_crash_the_check():
    """Un número fuera de rango se rechaza, no revienta con `IndexError`."""
    for bad in (0, len(SENTENCES) + 1, -1, "3", None, True):
        row = dict(labels.blank_labels()[0], number=bad)
        assert labels.row_problems(row), f"el numero {bad!r} entro sin protestar"


def test_saving_refuses_a_broken_row(tmp_path):
    """🔒 Un archivo de etiquetas medio roto cuesta trabajo humano de rehacer."""
    path = tmp_path / "sentence_labels.jsonl"
    rows = labels.blank_labels()
    rows[4] = dict(rows[4], verdict="quiza")

    with pytest.raises(ValueError):
        labels.save_labels(rows, path)

    assert not path.exists(), "escribio el archivo pese a la fila mala"


def test_a_saved_file_reads_back_the_same(tmp_path):
    """Ida y vuelta: lo que se escribe es lo que se lee."""
    path = tmp_path / "sentence_labels.jsonl"
    rows = labels.blank_labels()
    rows[0] = dict(rows[0], verdict=labels.LABEL_WRONG, note="falta el articulo")

    labels.save_labels(rows, path)

    assert labels.load_labels(path) == rows


def test_labels_and_corpus_are_sisters_not_nested():
    """🔒 `[D-097]`: las dos carpetas tienen criterios de entrada OPUESTOS.

    🚨 `_persistence/corpus/` guarda lo que ya **no** es producción —y
    `test_no_frozen_corpus_carries_the_live_rubric` lo hace cumplir—, mientras que
    las etiquetas nacen contra la rúbrica **viva** y valen mientras viva. Anidarlas
    pondría aquel test en rojo, así que la separación se sostiene aquí en vez de
    descubrirse el día que alguien mueva la carpeta.
    """
    # 📌 `CORPUS_DIR` vive en el archivo de tests de al lado, no en `eval_rubric`.
    # Se importa de allí en vez de reescribir la ruta: dos rutas escritas a mano
    # es exactamente la deriva que este test dice estar vigilando.
    from test_eval_rubric import CORPUS_DIR

    assert labels.LABELS_DIR.resolve().parent == CORPUS_DIR.parent
    assert labels.LABELS_DIR.resolve() != CORPUS_DIR
    assert CORPUS_DIR not in labels.LABELS_DIR.resolve().parents


def test_the_labels_file_is_not_reachable_by_the_corpus_gatekeepers():
    """⚠️ Y al revés: un archivo de etiquetas no puede colarse como corpus.

    🔑 Los porteros de `corpus/` hacen `CORPUS_DIR.glob("*.jsonl")`. Este test deja
    escrito que las etiquetas quedan **fuera** de ese alcance a propósito — no por
    descuido—, y que por eso necesitan portero propio.
    """
    from test_eval_rubric import CORPUS_DIR

    reachable = {path.resolve() for path in CORPUS_DIR.glob("*.jsonl")}

    assert not reachable & {path.resolve() for path in _label_files()}


def test_every_labelled_sentence_is_one_of_ours():
    """🔒 `PI-8` por el lado que sí se puede comprobar.

    ⚠️ **Y solo por ese lado.** Esto reutiliza la cerradura de `sentences_are_invented`
    sobre el campo `sentence`; **no** mira `note`, que es prosa de una persona y
    ningún programa la audita. Se dice aquí para que el verde no se lea como más de
    lo que es (`[D-093]`).
    """
    import eval_rubric

    for path in _label_files():
        rows = labels.load_labels(path)

        assert eval_rubric.sentences_are_invented(rows), (
            f"{path.name} tiene una frase que no sale de SENTENCES"
        )


def test_progress_counts_against_sentences_not_against_the_file():
    """🚨 El denominador sale de la REFERENCIA, no del propio archivo.

    🔑 Es `[L-071]`: si se pierde una línea editando a mano, con `len(rows)` la
    salida diría `50 de 50 etiquetadas` — completo y limpio, y falso. El agregado
    encogió con el dato.
    """
    rows = [dict(row, verdict=labels.LABEL_CORRECT) for row in labels.blank_labels()]

    del rows[7]

    done, total = labels.progress(rows)

    assert total == len(SENTENCES), "el total salio del archivo, no de SENTENCES"
    assert done == len(SENTENCES) - 1
    assert labels.missing_numbers(rows) == [8]


def test_a_line_that_is_not_json_names_its_number(tmp_path):
    """🔒 Se para con un mensaje que dice la línea, no con un traceback.

    🔑 Mismo criterio que `eval_rubric.chosen_sentences`: quien corre esto está en
    una terminal, editando sesenta líneas a mano. Una coma de más es el fallo más
    probable de todos, y buscarla a ojo en sesenta filas es el precio de no decir
    el número.
    """
    path = tmp_path / "sentence_labels.jsonl"
    good = labels.blank_labels()[:3]
    path.write_text(
        "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in good)
        + '{"number": 4, "sentence": "roto",}\n',
        encoding="utf-8",
    )

    with pytest.raises(SystemExit) as stop:
        labels.load_labels(path)

    assert "linea 4" in str(stop.value)


def test_the_labels_file_is_backed_up_by_git():
    """🚨 La promesa entera de `[D-097]` es "aquí Git lo respalda". Esto lo cobra.

    ⚠️ **Sin este test, esa garantía descansa en un `git check-ignore` que alguien
    corrió una vez.** El día que un patrón nuevo cubra la carpeta, el archivo sin
    precio deja de estar respaldado y **los otros porteros siguen verdes**, porque
    leen el disco y no Git. Un freno que no se ha visto morder es una nota.

    🔑 Se comprueban las **dos** mitades, que son fallos distintos: que nadie lo
    ignore, y que esté de verdad dentro del repositorio. Un archivo no ignorado
    pero sin commitear tiene exactamente la durabilidad de `data/`.

    📌 **Limitación conocida, anotada a propósito y NO arreglada hoy.** Esto da por
    hecho que hay un `git` ejecutable y un `.git` alrededor. Hoy es cierto. El día
    que la suite corra desde un tarball o un contenedor sin repositorio, este test
    fallará **por un motivo que no es el suyo** —"no puedo comprobarlo" disfrazado
    de "no está respaldado"—, y los dos mensajes deberían distinguirse. ⚠️ Se
    escribe aquí porque **un freno que falla por el motivo equivocado es el que
    acaba desactivándose**, y entonces se pierde el bueno junto con el falso.
    """
    root = Path(__file__).resolve().parent.parent
    relative = labels.LABELS_FILE.resolve().relative_to(root).as_posix()

    ignored = subprocess.run(
        ["git", "check-ignore", relative],
        cwd=root, capture_output=True, text=True,
    )

    assert ignored.returncode != 0, (
        f"{relative} esta en .gitignore: [D-097] lo puso aqui para que Git lo "
        "respalde, y asi no lo respalda nadie."
    )

    tracked = subprocess.run(
        ["git", "ls-files", "--error-unmatch", relative],
        cwd=root, capture_output=True, text=True,
    )

    assert tracked.returncode == 0, (
        f"{relative} no esta en Git todavia: hasta que se commitee, el trabajo "
        "humano que lleve dentro vive en un disco sin copia."
    )


def test_the_module_says_out_loud_that_the_note_is_not_audited():
    """🚨 La frase del docstring ES el artefacto, no un adorno.

    🔑 Es lo que `sentences_are_invented` hizo bien: declarar el alcance en voz
    alta. Sin esa frase, el verde de esta suite se lee como *"las etiquetas están
    auditadas"* — y `note` no la audita nadie. Si alguien borra la advertencia,
    esto se pone rojo.
    """
    assert "NINGÚN PROGRAMA LA AUDITA" in labels.__doc__
