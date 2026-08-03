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
    MAX_USER_LENGTH,
    InvalidUserError,
    ScoreFileError,
    add_point,
    count_words,
    judge_grammar,
    normalize_user,
    read_score,
    score_file,
)

# Una persona cualquiera, para los tests que no van sobre el nombre.
USER = "juan"


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


# ── normalize_user ────────────────────────────────────────────────────────
#
# 🚨 Con este nombre se construye una RUTA DE ARCHIVO, y el nombre lo escribe
# quien usa la app. Estos tests son el freno del paso 4.


def test_normalize_user_lowercases_and_trims():
    assert normalize_user("  Juan  ") == "juan"


@pytest.mark.parametrize("written", ["juan", "Juan", "JUAN", " jUaN "])
def test_the_same_person_written_differently_is_one_person(written):
    # 🔑 El test que de verdad importa de la normalizacion. Windows no distingue
    # mayusculas y Linux si: sin esto, `Juan` y `juan` serian UNA persona en la
    # maquina local y DOS en la nube del paso 7. Sin error y en verde.
    assert normalize_user(written) == normalize_user("juan")


@pytest.mark.parametrize("empty", ["", "   ", "\n\t"])
def test_normalize_user_rejects_an_empty_name(empty):
    # Un nombre vacio daria el archivo `.json`, oculto y de nadie.
    with pytest.raises(InvalidUserError):
        normalize_user(empty)


@pytest.mark.parametrize(
    "attack",
    [
        "../CLAUDE.md",
        "../../.env",
        "..",
        ".",
        "data/score",
        "juan/../../otro",
        "C:\\Windows\\System32",
        "juan\\otro",
        "score.json",
    ],
)
def test_normalize_user_rejects_escaping_the_folder(attack):
    # 🔑 El test que de verdad importa. Sin la lista blanca, cualquiera de estos
    # saca la escritura de `data/` y aterriza donde no debe.
    with pytest.raises(InvalidUserError):
        normalize_user(attack)


@pytest.mark.parametrize("odd", ["juan perez", "josé", "juan;rm", "juan*", "juan\0x"])
def test_normalize_user_rejects_anything_outside_the_allowlist(odd):
    # Denegar por defecto: no se enumera lo prohibido —siempre falta algo— sino
    # lo permitido. Espacios, tildes y signos se quedan fuera.
    with pytest.raises(InvalidUserError):
        normalize_user(odd)


@pytest.mark.parametrize("reserved", ["con", "PRN", "aux", "nul", "com1", "lpt9"])
def test_normalize_user_rejects_windows_device_names(reserved):
    # 🔑 Validar los caracteres NO es validar el nombre: estos son letras y
    # numeros, pasan la lista blanca enteros, y Windows los reserva para
    # dispositivos incluso con extension (`con.json` sigue siendo el dispositivo).
    with pytest.raises(InvalidUserError):
        normalize_user(reserved)


def test_normalize_user_rejects_a_name_that_is_too_long():
    # Al ponerle `.json` detras se pasaria del limite del sistema de archivos, y
    # eso revienta al ESCRIBIR, no al validar: mucho mas tarde y peor.
    with pytest.raises(InvalidUserError):
        normalize_user("a" * (MAX_USER_LENGTH + 1))


def test_normalize_user_accepts_a_name_of_the_maximum_length():
    # El limite es "hasta aqui", no "menos que aqui". Sin este test, un `>=` por
    # un `>` pasaria desapercibido.
    longest = "a" * MAX_USER_LENGTH

    assert normalize_user(longest) == longest


@pytest.mark.parametrize("valid", ["juan", "ana2", "maria-lu", "user_1", "x"])
def test_normalize_user_accepts_ordinary_names(valid):
    # El freno tiene que dejar pasar lo normal. Un validador que rechaza todo
    # tambien pasaria los tests de arriba.
    assert normalize_user(valid) == valid


@pytest.mark.parametrize("not_a_name", [None, 42, ["juan"], {"a": 1}])
def test_normalize_user_rejects_anything_that_is_not_text(not_a_name):
    with pytest.raises(TypeError):
        normalize_user(not_a_name)


def test_the_invalid_name_never_becomes_a_path(tmp_path):
    # 🔑 `score_file` es el unico sitio donde un nombre se vuelve una ruta, y
    # valida por su cuenta: si algun dia lo llama alguien que se salto el filtro
    # de la puerta, tiene que negarse igual. El olvido falla hacia el lado seguro.
    with pytest.raises(InvalidUserError):
        score_file("../../CLAUDE.md", tmp_path)


def test_add_point_refuses_to_write_outside_the_folder(tmp_path):
    # Y el mismo freno en la funcion que de verdad escribe en el disco.
    users_dir = tmp_path / "users"
    users_dir.mkdir()

    with pytest.raises(InvalidUserError):
        add_point("../escapado", users_dir)

    # 🔑 Estas dos lineas NO dicen lo mismo, y la segunda es la que importa.
    # La primera demuestra que no se escribio DENTRO; el test se llama "outside",
    # asi que lo que hay que demostrar es que no aparecio nada FUERA. Sin ella,
    # la linea de arriba parece cubrir la fuga y no la cubre — el unico freno de
    # verdad seria el `pytest.raises`. Es el mismo defecto de [L-003] a [L-006]:
    # la comprobacion mide algo distinto de lo que su nombre promete.
    assert list(users_dir.iterdir()) == []
    assert not (tmp_path / "escapado.json").exists()
    assert list(tmp_path.iterdir()) == [users_dir]


# ── read_score / add_point ────────────────────────────────────────────────


def test_read_score_is_zero_when_the_file_does_not_exist(tmp_path):
    assert read_score(USER, tmp_path) == 0


def test_add_point_creates_the_file_and_returns_one(tmp_path):
    assert add_point(USER, tmp_path) == 1
    assert score_file(USER, tmp_path).exists()


def test_add_point_accumulates(tmp_path):
    add_point(USER, tmp_path)
    add_point(USER, tmp_path)

    assert add_point(USER, tmp_path) == 3


def test_the_score_survives_being_read_back(tmp_path):
    # Lo importante del marcador no es sumar: es seguir ahí mañana.
    add_point(USER, tmp_path)
    add_point(USER, tmp_path)

    assert read_score(USER, tmp_path) == 2


def test_add_point_creates_the_folder_if_it_is_missing(tmp_path):
    # La primera vez que se usa la app, `data/users/` todavía no existe.
    assert add_point(USER, tmp_path / "data" / "users") == 1


# ── Una memoria por persona ───────────────────────────────────────────────
#
# 🔑 Lo que rompe el paso 4: hasta ahora habia UN marcador para todo el mundo.


def test_two_people_do_not_share_the_score(tmp_path):
    # El test que de verdad importa del paso 4. Con un solo archivo, el segundo
    # `add_point` devolvia 2 en vez de 1.
    add_point("juan", tmp_path)
    add_point("juan", tmp_path)

    assert add_point("ana", tmp_path) == 1


def test_each_person_keeps_their_own_score(tmp_path):
    add_point("juan", tmp_path)
    add_point("juan", tmp_path)
    add_point("ana", tmp_path)

    assert read_score("juan", tmp_path) == 2
    assert read_score("ana", tmp_path) == 1


def test_a_broken_score_does_not_affect_the_others(tmp_path):
    # Que el archivo de una persona este roto no puede dejar sin practicar a las
    # demas: son archivos independientes y el fallo tiene que quedarse dentro.
    score_file("juan", tmp_path).parent.mkdir(parents=True, exist_ok=True)
    score_file("juan", tmp_path).write_text("esto no es json", encoding="utf-8")

    assert add_point("ana", tmp_path) == 1


# ── El marcador roto ──────────────────────────────────────────────────────
#
# Un `add_point` interrumpido a medias —un Ctrl-C, un corte de luz— deja el
# archivo escrito por la mitad. A partir de ahí hay que avisar, no adivinar:
# devolver 0 en silencio le diría "tienes cero puntos" a quien tenía seis.


def write_broken_score(users_dir, content):
    """Deja el marcador de `USER` escrito a medias. Devuelve su ruta."""
    path = score_file(USER, users_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


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
    write_broken_score(tmp_path, content)

    with pytest.raises(ScoreFileError):
        read_score(USER, tmp_path)


def test_the_error_message_names_the_file(tmp_path):
    # Quien lea el error tiene que saber QUÉ archivo hay que ir a mirar.
    path = write_broken_score(tmp_path, "esto no es json")

    with pytest.raises(ScoreFileError, match=re.escape(str(path))):
        read_score(USER, tmp_path)


def test_add_point_raises_on_a_broken_file(tmp_path):
    write_broken_score(tmp_path, "esto no es json")

    with pytest.raises(ScoreFileError):
        add_point(USER, tmp_path)


def test_add_point_leaves_a_broken_file_untouched(tmp_path):
    # 🔑 El test que de verdad importa: no basta con que falle, tiene que dejar
    # el archivo EXACTAMENTE como estaba. Mientras el original siga entero,
    # quien lo use puede abrirlo y recuperar su marcador a mano.
    broken = '{"score": 6, "y aqui se corto la lu'
    path = write_broken_score(tmp_path, broken)

    with pytest.raises(ScoreFileError):
        add_point(USER, tmp_path)

    assert path.read_text(encoding="utf-8") == broken


# ── La escritura atomica ──────────────────────────────────────────────────
#
# No basta con negarse a pisar un archivo roto: hay que no crearlo. `add_point`
# escribe al lado y renombra encima, porque renombrar es una sola operacion del
# sistema y no deja nunca el archivo a medias.


def test_add_point_does_not_leave_temporary_files_behind(tmp_path):
    # Si el temporal sobrevive, es que el renombrado no ocurrio: se escribio
    # directamente encima y la proteccion no esta puesta.
    add_point(USER, tmp_path)
    add_point(USER, tmp_path)

    assert list(tmp_path.iterdir()) == [score_file(USER, tmp_path)]


def test_add_point_survives_a_crash_while_writing(tmp_path, monkeypatch):
    # 🔑 El test que de verdad importa: simulamos el corte de luz reventando
    # justo en el renombrado, con el temporal ya escrito. El marcador viejo
    # tiene que seguir entero y legible.
    add_point(USER, tmp_path)
    add_point(USER, tmp_path)  # el marcador vale 2

    def blackout(*args, **kwargs):
        raise OSError("se corto la luz")

    monkeypatch.setattr("app.tools.os.replace", blackout)

    with pytest.raises(OSError):
        add_point(USER, tmp_path)

    # El archivo bueno ni se entero: sigue valiendo 2 y se lee sin errores.
    assert read_score(USER, tmp_path) == 2


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


def add_many_points_at_once(users_dir, writers=WRITERS, user=USER):
    """Lanza `writers` hilos sumando un punto a la vez. Devuelve los totales."""
    with ThreadPoolExecutor(max_workers=writers) as pool:
        return list(pool.map(lambda _: add_point(user, users_dir), range(writers)))


def test_add_point_survives_two_writers_at_once(tmp_path):
    # T-021: con un temporal de nombre fijo, esto reventaba con PermissionError
    # en Windows. Ninguna llamada debe fallar.
    add_many_points_at_once(tmp_path, writers=2)

    assert read_score(USER, tmp_path) == 2


def test_no_points_are_lost_with_many_writers_at_once(tmp_path):
    # 🔑 T-022: el test que de verdad importa. Cada hilo suma un punto, asi que
    # el marcador final tiene que valer EXACTAMENTE lo que hilos hubo. Sin el
    # candado se quedaba en 8 o 10 de 50: los puntos se perdian en el hueco
    # entre leer y escribir.
    #
    # Sigue haciendo falta despues del paso 4: dos personas distintas ya no se
    # pisan, pero la MISMA persona con dos pestañas abiertas si.
    add_many_points_at_once(tmp_path)

    assert read_score(USER, tmp_path) == WRITERS


def test_no_two_writers_get_the_same_score(tmp_path):
    # Y el otro lado del mismo fallo: nadie puede recibir un numero repetido.
    # Dar el mismo "llevas 6" dos veces es mentir una de las dos.
    totals = add_many_points_at_once(tmp_path)

    assert sorted(totals) == list(range(1, WRITERS + 1))


def test_many_writers_leave_no_temporary_files_behind(tmp_path):
    # Cada escritura estrena temporal, asi que hay que comprobar que tambien se
    # limpian todos. Si no, `data/` se llenaria de basura con el uso.
    add_many_points_at_once(tmp_path)

    assert list(tmp_path.iterdir()) == [score_file(USER, tmp_path)]


def test_two_people_writing_at_once_keep_their_own_scores(tmp_path):
    # El candado es unico para todo el mundo, asi que conviene comprobar que no
    # mezcla a nadie: cada quien acaba con sus puntos, no con la suma de los dos.
    with ThreadPoolExecutor(max_workers=2) as pool:
        juan = pool.submit(add_many_points_at_once, tmp_path, WRITERS, "juan")
        ana = pool.submit(add_many_points_at_once, tmp_path, WRITERS, "ana")
        juan.result()
        ana.result()

    assert read_score("juan", tmp_path) == WRITERS
    assert read_score("ana", tmp_path) == WRITERS
