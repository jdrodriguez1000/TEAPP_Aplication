"""Los porteros de `_persistence/replies/`.

🚨 **Nacen en el MISMO commit que la carpeta**, por lo mismo que en `[D-097]`: una
carpeta vacía no da miedo y por eso nadie vuelve a ponerle puerta. El archivo que
se cuela es siempre el que entró el día que todavía no había portero.

⚠️ **Lo que estos tests NO hacen.** No juzgan lo que dice `reply`. Aquí la prosa
libre no es un campo lateral —es la carga entera del archivo—, y ningún programa
la audita. Un verde que se lea como *"las respuestas están revisadas"* sería peor
que no tener tests.
"""

import json
import subprocess
from pathlib import Path

import pytest

import replies
from measure_tutor import SENTENCES


def _archived() -> list[Path]:
    """Los archivos archivados que hay HOY, buscados y no listados."""
    return sorted(replies.REPLIES_DIR.glob("*.jsonl"))


def test_the_replies_folder_is_not_empty():
    """⚠️ Un portero sobre una carpeta vacía es verde y no prueba nada.

    🔑 `[L-048]`: los tests de debajo recorren un `glob`, y un `glob` sin
    resultados los deja pasar en silencio. Si algún día la carpeta se vacía a
    propósito —porque todo se promovió a `corpus/`—, este test se borra **a mano y
    con la razón escrita** (`PI-6`).
    """
    assert _archived(), (
        f"{replies.REPLIES_DIR} esta vacia: los tests de debajo recorren un glob "
        "y pasarian en verde sin mirar nada."
    )


def test_every_archived_row_is_well_formed():
    """Ninguna fila archivada trae campos de más, de menos ni tipos raros."""
    for path in _archived():
        for row in replies.load_replies(path):
            problems = replies.row_problems(row)
            assert not problems, f"{path.name}, fila {row.get('number')}: {problems}"


def test_every_archived_sentence_is_invented():
    """🔒 La cerradura de `PI-8` sobre esta carpeta.

    Este repositorio es **público** (`[C-007]`). Una frase que no salga de
    `SENTENCES` la escribió alguien usando la app, y aquí no entra.
    """
    for path in _archived():
        for row in replies.load_replies(path):
            assert row.get("sentence") in SENTENCES, (
                f"{path.name}, fila {row.get('number')}: la frase no sale de "
                "SENTENCES. PI-8: aqui no entra lo que escriba una persona."
            )


def test_the_archived_name_agrees_with_its_rows():
    """El nombre es el criterio de promoción de `[D-092]`: si miente, decide mal."""
    for path in _archived():
        problems = replies.name_matches_rows(path, replies.load_replies(path))
        assert not problems, f"{path.name}: {problems}"


def test_a_row_with_an_extra_field_is_rejected():
    """🔻 El saboteo: un campo nuevo tiene que doler.

    🚨 **Es el freno que pidió la auditoría del 2026-08-18**, y el motivo es que
    `reply` ya es toda la superficie ciega que esta carpeta acepta. Un campo de más
    la agranda sin que nadie lo note — y el que se cuele mañana es justo el que
    nadie mirará.
    """
    row = {
        "number": 1,
        "sentence": SENTENCES[0],
        "reply": "OK",
        "broken": [],
        "model": "claude-opus-5",
        "rubric": "bbf4be38",
        "reviewer_note": "un campo que nadie pidio",
    }

    problems = replies.row_problems(row)

    assert any("campos que no existen" in problem for problem in problems), problems


def test_a_row_missing_a_field_is_rejected():
    """Aquí no hay campos opcionales: estas filas las escribe un programa.

    🔑 Una fila incompleta no es un descuido de tecleo —al revés que en
    `labels.py`, que sí lo tolera en `note`—: es que el escritor cambió y nadie se
    enteró.
    """
    row = {
        "number": 1,
        "sentence": SENTENCES[0],
        "reply": "OK",
        "broken": [],
        "model": "claude-opus-5",
    }

    problems = replies.row_problems(row)

    assert any("le faltan campos" in problem for problem in problems), problems


def test_a_sentence_that_drifted_from_its_number_is_caught():
    """🚨 La respuesta se pega al TEXTO, no solo a la posición.

    El día que alguien inserte o reordene una frase en `SENTENCES`, las sesenta
    filas apuntarían a la frase de al lado **sin dar un solo error**. Cotejar las
    dos convierte ese fallo mudo en uno que se ve.
    """
    row = {
        "number": 1,
        "sentence": SENTENCES[1],
        "reply": "OK",
        "broken": [],
        "model": "claude-opus-5",
        "rubric": "bbf4be38",
    }

    problems = replies.row_problems(row)

    assert any("no es la numero 1" in problem for problem in problems), problems


def test_a_name_that_lies_about_the_rubric_is_caught():
    """Si el nombre no lleva la rúbrica de sus filas, `[D-092]` decide a ciegas."""
    rows = [{
        "number": 1,
        "sentence": SENTENCES[0],
        "reply": "OK",
        "broken": [],
        "model": "claude-opus-5",
        "rubric": "deadbeef",
    }]

    problems = replies.name_matches_rows(
        Path("eval_replies_claude-opus-5_2026-08-18_rubric-bbf4be38_full.jsonl"), rows
    )

    assert any("rubric" in problem for problem in problems), problems


def test_a_broken_line_says_which_line(tmp_path):
    """Un JSON roto se para con el número de línea, no con un traceback."""
    path = tmp_path / "roto.jsonl"
    path.write_text('{"number": 1}\nesto no es json\n', encoding="utf-8")

    with pytest.raises(SystemExit) as error:
        replies.load_replies(path)

    assert "linea 2" in str(error.value)


def test_the_module_says_out_loud_that_the_reply_is_not_audited():
    """🚨 La frase del docstring ES el artefacto, no un adorno.

    🔑 Sin ella, el verde de esta suite se lee como *"las respuestas están
    auditadas"*, y `reply` no la audita nadie. Si alguien borra la advertencia,
    esto se pone rojo. Mismo freno que en `test_labels.py`.
    """
    assert "NINGÚN PROGRAMA LA AUDITA" in replies.__doc__


def test_the_archived_replies_are_backed_up_by_git():
    """🚨 La promesa entera de esta carpeta es "aquí Git lo respalda". Esto lo cobra.

    ⚠️ **Sin este test, la garantía descansa en un `git check-ignore` que alguien
    corrió una vez.** El día que un patrón nuevo cubra la carpeta, el archivo deja
    de estar respaldado y **los otros porteros siguen verdes**, porque leen el
    disco y no Git.

    🔑 Se comprueban las **dos** mitades, que son fallos distintos: que nadie lo
    ignore, y que esté de verdad dentro del repositorio. Un archivo no ignorado
    pero sin commitear tiene exactamente la durabilidad de `data/` — que es de lo
    que vino huyendo.

    📌 **Misma limitación conocida que en `test_labels.py`**, anotada a propósito y
    no arreglada hoy: esto da por hecho que hay un `git` alrededor. El día que la
    suite corra sin repositorio, fallará por un motivo que no es el suyo.
    """
    root = Path(__file__).resolve().parent.parent

    for path in _archived():
        relative = path.resolve().relative_to(root).as_posix()

        ignored = subprocess.run(
            ["git", "check-ignore", relative],
            cwd=root, capture_output=True, text=True,
        )

        assert ignored.returncode != 0, (
            f"{relative} esta en .gitignore: esta carpeta existe para que Git lo "
            "respalde, y asi no lo respalda nadie."
        )

        tracked = subprocess.run(
            ["git", "ls-files", "--error-unmatch", relative],
            cwd=root, capture_output=True, text=True,
        )

        assert tracked.returncode == 0, (
            f"{relative} no esta en Git todavia: hasta que se commitee, tiene la "
            "misma durabilidad que data/."
        )


def test_no_archived_file_lives_in_the_frozen_corpus_too():
    """🔴 El mismo archivo en las dos carpetas es el bicho de la sesión 33.

    🔑 `replies/` es una **antesala**: de aquí se sale hacia `corpus/`. Salir es
    **mover**, no copiar — si se copia, quedan dos archivos con el mismo nombre que
    un día discrepan, y nadie sabe cuál manda.
    """
    corpus = replies.REPLIES_DIR.parent / "corpus"
    here = {path.name for path in _archived()}
    there = {path.name for path in corpus.glob("*.jsonl")}

    assert not (here & there), (
        f"estos archivos estan en replies/ Y en corpus/: {sorted(here & there)}. "
        "Promover es mover, no copiar."
    )
