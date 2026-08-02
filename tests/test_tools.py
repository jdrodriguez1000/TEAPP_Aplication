"""Tests de las tres herramientas.

Ninguno toca el marcador real: los que escriben usan `tmp_path`, una carpeta
temporal que pytest crea y borra sola en cada corrida.
"""

from app.tools import FAKE_VERDICT, add_point, count_words, judge_grammar, read_score


# ── count_words ───────────────────────────────────────────────────────────


def test_count_words_counts_a_simple_sentence():
    assert count_words("I like coffee") == 3


def test_count_words_ignores_extra_spaces():
    # Los espacios de más no son palabras.
    assert count_words("  I   like    coffee  ") == 3


def test_count_words_of_empty_string_is_zero():
    assert count_words("") == 0


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
