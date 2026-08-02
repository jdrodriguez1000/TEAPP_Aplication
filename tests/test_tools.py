"""Tests de las tres herramientas.

Ninguno toca el marcador real: los que escriben usan `tmp_path`, una carpeta
temporal que pytest crea y borra sola en cada corrida.
"""

import json
import re

import pytest

from app.tools import (
    FAKE_VERDICT,
    ScoreFileError,
    add_point,
    count_words,
    judge_grammar,
    read_score,
)


# ── count_words ───────────────────────────────────────────────────────────


def test_count_words_counts_a_simple_sentence():
    assert count_words("I like coffee") == 3


def test_count_words_ignores_extra_spaces():
    # Los espacios de más no son palabras.
    assert count_words("  I   like    coffee  ") == 3


def test_count_words_of_empty_string_is_zero():
    assert count_words("") == 0


def test_count_words_splits_on_newlines():
    # `split()` sin argumentos parte por cualquier espacio en blanco, no solo
    # por el espacio. Este test lo deja clavado: si alguien lo cambia por
    # `split(" ")`, esto se pone rojo.
    assert count_words("I like\ncoffee") == 3


def test_count_words_splits_on_tabs():
    assert count_words("I\tlike\tcoffee") == 3


@pytest.mark.parametrize("not_a_sentence", [None, 42, ["hola"], {"a": 1}, 3.5])
def test_count_words_rejects_anything_that_is_not_text(not_a_sentence):
    # En el paso 2 esto llega de internet: FastAPI recibe JSON y por ahi entra
    # un numero, un null o una lista. Avisar es mejor que convertir en silencio.
    with pytest.raises(TypeError):
        count_words(not_a_sentence)


def test_the_type_error_says_what_arrived():
    # El mensaje tiene que nombrar lo que llego, o no sirve para depurar.
    with pytest.raises(TypeError, match="int"):
        count_words(42)


# ── judge_grammar ─────────────────────────────────────────────────────────


def test_judge_grammar_returns_the_fake_verdict():
    assert judge_grammar("I like coffee") == FAKE_VERDICT


def test_judge_grammar_is_fake_and_ignores_the_sentence():
    # Este test dice en voz alta que la herramienta es falsa: una frase
    # correcta y una rota reciben la misma respuesta. Cuando en el paso 8
    # entre el modelo, este test DEBE fallar. Es la señal de que algo cambió.
    assert judge_grammar("I like coffee") == judge_grammar("me likes coffees")


# ── read_score / add_point ────────────────────────────────────────────────


def test_read_score_is_zero_when_the_file_does_not_exist(tmp_path):
    assert read_score(tmp_path / "score.json") == 0


def test_add_point_creates_the_file_and_returns_one(tmp_path):
    score_file = tmp_path / "score.json"

    assert add_point(score_file) == 1
    assert score_file.exists()


def test_add_point_accumulates(tmp_path):
    score_file = tmp_path / "score.json"

    add_point(score_file)
    add_point(score_file)

    assert add_point(score_file) == 3


def test_the_score_survives_being_read_back(tmp_path):
    # Lo importante del marcador no es sumar: es seguir ahí mañana.
    score_file = tmp_path / "score.json"
    add_point(score_file)
    add_point(score_file)

    assert read_score(score_file) == 2


def test_add_point_creates_the_folder_if_it_is_missing(tmp_path):
    # La primera vez que se usa la app, `data/` todavía no existe.
    score_file = tmp_path / "data" / "score.json"

    assert add_point(score_file) == 1


# ── El marcador roto ──────────────────────────────────────────────────────
#
# Un `add_point` interrumpido a medias —un Ctrl-C, un corte de luz— deja el
# archivo escrito por la mitad. A partir de ahí hay que avisar, no adivinar:
# devolver 0 en silencio le diría "tienes cero puntos" a quien tenía seis.


@pytest.mark.parametrize(
    "reason, content",
    [
        ("no es json", "esto no es json"),
        ("le falta la clave score", json.dumps({"puntos": 3})),
        ("el score no es un numero", json.dumps({"score": "seis"})),
        ("el score es un booleano", json.dumps({"score": True})),
        ("el json no es un objeto", json.dumps([1, 2, 3])),
    ],
)
def test_read_score_raises_when_the_file_is_broken(tmp_path, reason, content):
    score_file = tmp_path / "score.json"
    score_file.write_text(content, encoding="utf-8")

    with pytest.raises(ScoreFileError):
        read_score(score_file)


def test_the_error_message_names_the_file(tmp_path):
    # Quien lea el error tiene que saber QUÉ archivo hay que ir a mirar.
    score_file = tmp_path / "score.json"
    score_file.write_text("esto no es json", encoding="utf-8")

    with pytest.raises(ScoreFileError, match=re.escape(str(score_file))):
        read_score(score_file)


def test_add_point_raises_on_a_broken_file(tmp_path):
    score_file = tmp_path / "score.json"
    score_file.write_text("esto no es json", encoding="utf-8")

    with pytest.raises(ScoreFileError):
        add_point(score_file)


def test_add_point_leaves_a_broken_file_untouched(tmp_path):
    # 🔑 El test que de verdad importa: no basta con que falle, tiene que dejar
    # el archivo EXACTAMENTE como estaba. Mientras el original siga entero,
    # quien lo use puede abrirlo y recuperar su marcador a mano.
    score_file = tmp_path / "score.json"
    broken = '{"score": 6, "y aqui se corto la lu'
    score_file.write_text(broken, encoding="utf-8")

    with pytest.raises(ScoreFileError):
        add_point(score_file)

    assert score_file.read_text(encoding="utf-8") == broken
