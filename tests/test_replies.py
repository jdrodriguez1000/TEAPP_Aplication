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
    """Ninguna fila archivada trae campos de más, de menos ni tipos raros.

    🔑 **La generación entra desde el NOMBRE**, no se adivina desde la fila: si se
    dedujera de los campos presentes, una fila a la que le falte una huella se
    declararía legado a sí misma y pasaría en verde. `generation_of` es externa a la
    fila, así que el cruce muerde en las dos direcciones.
    """
    for path in _archived():
        required = replies.generation_of(path)
        for row in replies.load_replies(path):
            problems = replies.row_problems(row, required)
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
    """El nombre es el criterio de promoción de `[D-102]`: si miente, decide mal.

    📌 **Este test NO se modificó por `[D-102]`: la exigencia era que SIGUIERA
    VERDE.** Corre sobre el archivo legado, que la cláusula de `[D-102]` manda no
    renombrar — y por eso obliga a que `name_matches_rows` tenga dos ramas de verdad.
    🚨 **Resolverlo saltándose los nombres no reconocidos lo dejaría verde y al
    portero ciego sobre el único archivo archivado que existe.**
    """
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

    problems = replies.row_problems(row, replies.CAMPOS_LEGADO)

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

    problems = replies.row_problems(row, replies.CAMPOS_LEGADO)

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

    problems = replies.row_problems(row, replies.CAMPOS_LEGADO)

    assert any("no es la numero 1" in problem for problem in problems), problems


def test_a_name_that_lies_about_the_seal_is_caught():
    """Si el sello del nombre no sale de las filas, la promoción decide a ciegas.

    🔓 **Reemplaza a `test_a_name_that_lies_about_the_rubric_is_caught`, jubilado por
    la autorización `PI-6` del 2026-08-19.** Aquel no era un literal de ejemplo: era
    el contrato entero de *"la rúbrica va en el nombre"*, que `[D-102]` retira.

    ⚠️ **Y cambia de nombre, no solo de cuerpo.** Un test que sigue llamándose *"about
    the rubric"* mientras comprueba el sello manda a quien lea la lista al sitio
    equivocado — la trampa de `[L-080]`.
    """
    rows = [{
        "number": 1,
        "sentence": SENTENCES[0],
        "reply": "OK",
        "broken": [],
        "model": "claude-opus-5",
        "rubric": "deadbeef",
        "sentences": "cafe0000",
        "detector": "f00dbabe",
    }]

    problems = replies.name_matches_rows(
        Path("eval_replies_claude-opus-5_2026-08-19_run-00000000_full.jsonl"), rows
    )

    assert any("sello" in problem for problem in problems), problems


def test_a_legacy_name_that_lies_about_the_rubric_is_still_caught():
    """🚨 La rama LEGADO tiene que MORDER, no callar. Verde no demuestra nada aquí.

    🔴 **Este test nace de un sabotaje que la suite NO cazó** (2026-08-19). Se hizo
    que `name_matches_rows` se saltara los nombres que no reconoce —la salida cómoda
    que `[D-102]` prohíbe por escrito— y **los 574 tests siguieron en verde.**

    🔑 **Por qué el freno que se había previsto no bastaba.** La exigencia era que
    `test_the_archived_name_agrees_with_its_rows` *"siguiera verde"*. Pero ese test
    afirma **ausencia de problemas**, y un portero ciego produce exactamente eso:
    verde es el resultado del arreglo bueno **y** del malo, así que no los distingue.
    **Un guardián solo se demuestra enseñándole algo que tenga que rechazar.**

    ⚠️ Es la tercera vez en dos días que aparece la misma especie: el test nº 4 de la
    autorización `PI-6`, el portero de `name_matches_rows`, y este. Ver `[L-048]`.
    """
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

    assert any("rubric" in problem for problem in problems), (
        "la rama legado no mordio: si se salta los nombres que no reconoce, el "
        "portero queda CIEGO sobre el unico archivo archivado que existe."
    )


def test_a_sealed_row_missing_a_fingerprint_is_caught():
    """🚨 A una fila sellada NO se le puede caer una huella en silencio.

    🔑 **Es la razón de que las huellas nuevas sean OBLIGATORIAS y no opcionales.**
    Con opcionales, esta fila pasaría en verde — y es justo la fila que tiene que
    cantar, porque de ella se recalcula el sello. Sería comprar silencio en el sitio
    donde se acaba de poner el instrumento.
    """
    rows = [{
        "number": 1,
        "sentence": SENTENCES[0],
        "reply": "OK",
        "broken": [],
        "model": "claude-opus-5",
        "rubric": "deadbeef",
        "sentences": "cafe0000",
    }]

    path = Path("eval_replies_claude-opus-5_2026-08-19_run-00000000_full.jsonl")

    assert any("detector" in p for p in replies.name_matches_rows(path, rows))
    assert any(
        "detector" in p for p in replies.row_problems(rows[0], replies.generation_of(path))
    )


def test_the_legacy_generation_never_grows():
    """🔻 La rama de compatibilidad es CERRADA y DECRECIENTE, no una arquitectura.

    🔑 **Por qué el coste de `[D-102]` está acotado.** Desde el sello, `save_replies`
    solo sabe escribir nombres sellados: **no puede nacer un archivo legado nuevo.**
    Así que la rama vieja se escribe una vez, se prueba contra los archivos que
    existen hoy y no crece nunca.

    ⚠️ **Pueden DESAPARECER** —al promoverse a `corpus/`— **y no puede aparecer
    ninguno.** Por eso es un subconjunto, no una igualdad.

    🚨 **Si este test se pone rojo, algo volvió a escribir con el formato viejo** — que
    es exactamente el fallo que nadie notaría de otra forma. Sin él, dentro de tres
    meses alguien lee *"dos generaciones"* y asume que es un diseño, no una cola.
    """
    legacy = {
        path.name for path in _archived()
        if replies.generation_of(path) == replies.CAMPOS_LEGADO
    }

    assert legacy <= replies.LEGACY_FILES, (
        f"nacio un archivo de generacion LEGADO: {sorted(legacy - replies.LEGACY_FILES)}. "
        "Desde [D-102] save_replies solo escribe nombres sellados: si esto aparece, "
        "algo esta escribiendo con el formato viejo."
    )


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
