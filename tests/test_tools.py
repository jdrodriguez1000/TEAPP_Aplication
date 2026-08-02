"""Tests de las tres herramientas.

Ninguno toca el marcador real: los que escriben usan `tmp_path`, una carpeta
temporal que pytest crea y borra sola en cada corrida.
"""

import json
import re
from concurrent.futures import ThreadPoolExecutor

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


# ── La escritura atomica ──────────────────────────────────────────────────
#
# No basta con negarse a pisar un archivo roto: hay que no crearlo. `add_point`
# escribe al lado y renombra encima, porque renombrar es una sola operacion del
# sistema y no deja nunca el archivo a medias.


def test_add_point_does_not_leave_temporary_files_behind(tmp_path):
    # Si el temporal sobrevive, es que el renombrado no ocurrio: se escribio
    # directamente encima y la proteccion no esta puesta.
    score_file = tmp_path / "score.json"

    add_point(score_file)
    add_point(score_file)

    assert list(tmp_path.iterdir()) == [score_file]


def test_add_point_survives_a_crash_while_writing(tmp_path, monkeypatch):
    # 🔑 El test que de verdad importa: simulamos el corte de luz reventando
    # justo en el renombrado, con el temporal ya escrito. El marcador viejo
    # tiene que seguir entero y legible.
    score_file = tmp_path / "score.json"
    add_point(score_file)
    add_point(score_file)  # el marcador vale 2

    def blackout(*args, **kwargs):
        raise OSError("se corto la luz")

    monkeypatch.setattr("app.tools.os.replace", blackout)

    with pytest.raises(OSError):
        add_point(score_file)

    # El archivo bueno ni se entero: sigue valiendo 2 y se lee sin errores.
    assert read_score(score_file) == 2


# ── Dos peticiones a la vez ───────────────────────────────────────────────
#
# En la terminal escribia una persona. Con servidor, dos peticiones llegan a la
# vez de verdad, y aparecen dos fallos distintos que se parecen en el sintoma:
#
#   1. Se pelean por el archivo temporal (Windows corta con "Acceso denegado").
#   2. Las dos leen el mismo total antes de que ninguna lo haya escrito, y un
#      punto se pierde.
#
# Los tests van separados a proposito: son dos problemas y dos arreglos.

WRITERS = 50  # suficientes para que se pisen de verdad, no tantos que tarde


def add_many_points_at_once(score_file, writers=WRITERS):
    """Lanza `writers` hilos sumando un punto a la vez. Devuelve los totales."""
    with ThreadPoolExecutor(max_workers=writers) as pool:
        return list(pool.map(lambda _: add_point(score_file), range(writers)))


def test_add_point_survives_two_writers_at_once(tmp_path):
    # T-021: con un temporal de nombre fijo, esto reventaba con PermissionError
    # en Windows. Ninguna llamada debe fallar.
    score_file = tmp_path / "score.json"

    add_many_points_at_once(score_file, writers=2)

    assert read_score(score_file) == 2


def test_no_points_are_lost_with_many_writers_at_once(tmp_path):
    # 🔑 T-022: el test que de verdad importa. Cada hilo suma un punto, asi que
    # el marcador final tiene que valer EXACTAMENTE lo que hilos hubo. Sin el
    # candado se quedaba en 8 o 10 de 50: los puntos se perdian en el hueco
    # entre leer y escribir.
    score_file = tmp_path / "score.json"

    add_many_points_at_once(score_file)

    assert read_score(score_file) == WRITERS


def test_no_two_writers_get_the_same_score(tmp_path):
    # Y el otro lado del mismo fallo: nadie puede recibir un numero repetido.
    # Dar el mismo "llevas 6" a dos personas distintas es mentirle a una.
    score_file = tmp_path / "score.json"

    totals = add_many_points_at_once(score_file)

    assert sorted(totals) == list(range(1, WRITERS + 1))


def test_many_writers_leave_no_temporary_files_behind(tmp_path):
    # Cada escritura estrena temporal, asi que hay que comprobar que tambien se
    # limpian todos. Si no, `data/` se llenaria de basura con el uso.
    score_file = tmp_path / "score.json"

    add_many_points_at_once(score_file)

    assert list(tmp_path.iterdir()) == [score_file]
