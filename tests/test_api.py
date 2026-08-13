"""Tests de la puerta de red.

`TestClient` llama a las rutas sin levantar un servidor de verdad: no abre
ningún puerto ni hace falta tener uvicorn encendido. Por eso estos tests corren
igual de rápido que los demás.

El marcador se toca de verdad, y eso está bien: `conftest.py` lo manda a una
carpeta temporal nueva en cada test. Hasta [T-071] había aquí un maniquí que
sustituía `record_practice` entera, y con él la ruta contestaba sin llegar nunca al
disco. Por eso los marcadores empiezan en 1 y no en 7.
"""

import asyncio
import json
import logging
import time
from concurrent.futures import ThreadPoolExecutor

import anyio.to_thread
import pytest
from fastapi.testclient import TestClient

from app import accounts, api, config, english_tutor, login_guard, quota, sessions
from app.api import MAX_SENTENCE_LENGTH, app
import fake_tutor
from app.tools import (
    Counters,
    ScoreFileError,
    TutorUnavailableError,
    score_file,
)

client = TestClient(app)

# Quién practica. Desde el paso 4 la ruta no atiende sin saberlo.
USER = "juan"


GOOD_PASSWORD = "una-contrasena-larga"


@pytest.fixture(autouse=True)
def no_leftover_cookies():
    """Cada test empieza sin sesión iniciada.

    🔑 `TestClient` guarda las cookies entre peticiones —hace de navegador, y un
    navegador las guarda—. Con un cliente compartido por todo el archivo, la
    sesión de un test seguiría abierta en el siguiente: los tests de "sin
    sesión" pasarían por casualidad y dejarían de medir nada.
    """
    client.cookies.clear()
    yield
    client.cookies.clear()


@pytest.fixture
def logged_in():
    """Deja una sesión abierta como USER, con cuenta recién creada.

    Desde el paso 5 `/practice` no atiende a quien no se ha identificado, así
    que casi todos los tests de la ruta necesitan esto primero. Se pide a mano
    —no es `autouse`— para que los tests de "sin sesión" puedan no tenerlo.
    """
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    return USER


# ── La pantalla se sirve ──────────────────────────────────────────────────
#
# 🔑 El mismo servidor entrega la pantalla y atiende /practice. De ahí que no
# haya nada de CORS que probar: hay un solo origen — ver [D-011].


def test_the_home_page_is_served():
    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]


def test_the_home_page_is_the_practice_screen():
    # Que conteste 200 no dice que conteste la pantalla correcta.
    response = client.get("/")

    assert "<form id=\"practice-form\"" in response.text


def test_the_script_is_served():
    # Comprueba UNA cosa: que el archivo existe y se sirve. Eso sí cubre la mitad
    # del riesgo de [D-012] — si el `.js` nunca llegó a Git, aquí sale un 404 en
    # vez de descubrirse con una pantalla muda en el navegador.
    # ⚠️ NO comprueba que esté al día: un `.js` de hace tres días también da 200.
    # Editar el `.ts` sin compilar no se ve desde aquí, y desde un test no se
    # puede ver — el arreglo sería recompilar y commitear, no tocar el código.
    # Eso lo mira el cierre: `protocol-close`, Paso 2b. Ver [D-017] y [L-007].
    response = client.get("/static/app.js")

    assert response.status_code == 200


def test_the_home_page_asks_you_to_sign_in():
    # La casilla "Your name" del paso 4 se fue, y en su sitio hay un inicio de
    # sesion de verdad. [D-013] pedia justamente eso: quitarla, no añadirle algo
    # al lado.
    response = client.get("/")

    assert '<form id="signin-form"' in response.text
    assert 'id="password"' in response.text


def test_the_screen_does_not_send_a_name_with_the_sentence():
    # 🔑 El paso 5 visto desde la pantalla. Mientras el `.js` siga mandando
    # `user` en el cuerpo de /practice, la identidad seguiria siendo declarada
    # por el navegador aunque el servidor ya no la mire.
    script = client.get("/static/app.js").text

    assert "JSON.stringify({ sentence: sentence })" in script


def test_the_screen_calls_practice_without_naming_a_host():
    # La ruta relativa es lo que hace que la pantalla funcione igual en local y
    # en la nube. Un `http://localhost:8000` escrito a mano funcionaría hoy y se
    # rompería el día del despliegue, que es el peor momento para enterarse.
    # Se mira la llamada en sí y no el archivo entero: los comentarios nombran
    # `localhost` para explicar justamente por qué no se usa.
    script = client.get("/static/app.js").text

    assert 'fetch("/practice"' in script
    assert 'fetch("http' not in script


# ── La identidad: registrarse, entrar y salir ─────────────────────────────
#
# 🔑 El paso 5 visto desde fuera. Antes el navegador DECIA quien era; ahora lo
# prueba una vez y recibe una cookie firmada por el servidor — ver [D-021].


def test_register_creates_an_account_and_starts_the_session():
    response = client.post(
        "/register", json={"user": USER, "password": GOOD_PASSWORD}
    )

    assert response.status_code == 201
    assert response.json() == {"user": USER}
    assert sessions.SESSION_COOKIE in response.cookies


def test_the_session_cookie_cannot_be_read_by_javascript():
    # 🚨 Esta es LA diferencia con el `localStorage` del paso 4, que cualquier
    # script de la pagina leia. Sin `HttpOnly`, un script colado en la pantalla
    # se lleva la sesion entera.
    response = client.post(
        "/register", json={"user": USER, "password": GOOD_PASSWORD}
    )

    assert "httponly" in response.headers["set-cookie"].lower()


def test_the_session_cookie_is_not_sent_from_other_sites():
    # Sin `SameSite`, otra web podria hacer que tu navegador sumara puntos en tu
    # nombre sin que te enteraras.
    response = client.post(
        "/register", json={"user": USER, "password": GOOD_PASSWORD}
    )

    assert "samesite=lax" in response.headers["set-cookie"].lower()


def test_the_password_never_comes_back_in_the_answer():
    response = client.post(
        "/register", json={"user": USER, "password": GOOD_PASSWORD}
    )

    assert GOOD_PASSWORD not in response.text


def test_login_works_after_registering():
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    response = client.post("/login", json={"user": USER, "password": GOOD_PASSWORD})

    assert response.status_code == 200
    assert response.json() == {"user": USER}


def test_me_says_who_you_are():
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})

    response = client.get("/me")

    assert response.status_code == 200
    assert response.json() == {"user": USER}


def test_me_answers_401_without_a_session():
    response = client.get("/me")

    assert response.status_code == 401


def test_logout_ends_the_session():
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})

    client.post("/logout")

    assert client.get("/me").status_code == 401


def test_logout_answers_the_status_code_it_declares():
    # 🔑 Este test nacio de un fallo que la suite entera NO veia: `/logout`
    # devolvia el `Response` inyectado, cuyo `status_code` vale `None`, y el
    # servidor de verdad reventaba con `KeyError: None`. Con `TestClient` la
    # sesion se cerraba igual, asi que el test de arriba pasaba tan tranquilo.
    # Mirar el codigo de estado —y no solo el efecto— es lo que lo caza.
    # Ver [L-010].
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})

    assert client.post("/logout").status_code == 204


# ── 🚨 El freno de [D-020]: una identidad no se reclama ───────────────────


def test_a_taken_name_is_rejected_with_409():
    # 🔑 El test que sostiene el paso entero desde la red. Sin este freno,
    # cualquiera se registra como `juan` y hereda su marcador.
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    response = client.post(
        "/register", json={"user": USER, "password": "la-del-atacante"}
    )

    assert response.status_code == 409


def test_a_failed_takeover_leaves_the_old_password_working():
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()
    client.post("/register", json={"user": USER, "password": "la-del-atacante"})
    client.cookies.clear()

    assert (
        client.post(
            "/login", json={"user": USER, "password": "la-del-atacante"}
        ).status_code
        == 401
    )
    assert (
        client.post("/login", json={"user": USER, "password": GOOD_PASSWORD}).status_code
        == 200
    )


# ── Lo que no deja entrar ─────────────────────────────────────────────────


def test_a_wrong_password_does_not_start_a_session():
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    response = client.post("/login", json={"user": USER, "password": "otra-larguisima"})

    assert response.status_code == 401
    assert sessions.SESSION_COOKIE not in response.cookies


def test_someone_who_never_registered_cannot_log_in():
    response = client.post("/login", json={"user": "nadie", "password": GOOD_PASSWORD})

    assert response.status_code == 401


def test_the_two_failures_say_exactly_the_same_thing():
    # 🔑 "No existe" y "la contraseña no es esa" contestan lo mismo. Si se
    # distinguieran, se podria averiguar quien tiene cuenta aqui probando
    # nombres — media respuesta regalada a quien luego vaya a por la contraseña.
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    wrong_password = client.post(
        "/login", json={"user": USER, "password": "otra-larguisima"}
    )
    no_such_user = client.post(
        "/login", json={"user": "nadie", "password": GOOD_PASSWORD}
    )

    assert wrong_password.status_code == no_such_user.status_code
    assert wrong_password.json() == no_such_user.json()


def test_an_impossible_name_answers_like_a_wrong_password():
    # Un 422 explicando la regla del nombre le diria a quien prueba cuales de
    # sus intentos merecen la pena.
    response = client.post("/login", json={"user": "josé", "password": GOOD_PASSWORD})

    assert response.status_code == 401


@pytest.mark.parametrize("short", ["", "abc", "1234567"])
def test_register_rejects_a_short_password(short):
    response = client.post("/register", json={"user": USER, "password": short})

    assert response.status_code == 422


@pytest.mark.parametrize("bad", ["", "   ", "josé", "juan perez", "con", "../../CLAUDE.md"])
def test_register_rejects_a_name_that_cannot_be_a_file(bad):
    response = client.post("/register", json={"user": bad, "password": GOOD_PASSWORD})

    assert response.status_code == 422


@pytest.mark.parametrize(
    "reason, body",
    [
        ("falta todo", {}),
        ("falta la contrasena", {"user": USER}),
        ("falta el nombre", {"password": GOOD_PASSWORD}),
        ("el nombre es un numero", {"user": 42, "password": GOOD_PASSWORD}),
        ("la contrasena es null", {"user": USER, "password": None}),
    ],
)
def test_register_rejects_a_body_that_is_not_credentials(reason, body):
    response = client.post("/register", json=body)

    assert response.status_code == 422


# ── 🚨 La tarjeta retocada no vale ────────────────────────────────────────


def test_a_tampered_cookie_is_not_a_session():
    # 🔑 La prueba negativa del paso 5, desde la red: no basta con ver que una
    # sesion buena funciona. Se retoca la cookie y el servidor tiene que dejar
    # de reconocerla.
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.set(sessions.SESSION_COOKIE, client.cookies[sessions.SESSION_COOKIE] + "x")

    assert client.get("/me").status_code == 401


def test_a_handmade_cookie_is_not_a_session():
    client.cookies.set(sessions.SESSION_COOKIE, "juan|9999999999.firmafalsa")

    assert client.get("/me").status_code == 401


# ── La ruta contesta ──────────────────────────────────────────────────────


def test_practice_answers_ok(logged_in):
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 200


def test_practice_returns_the_three_pieces_separately(logged_in):
    # 🔑 El test que fija la decisión del paso 2: la ruta manda los
    # ingredientes, no el plato servido. La pantalla del paso 3 lee ESTO.
    response = client.post("/practice", json={"sentence": "I like coffee"})

    # `score` es 1 porque cada test estrena carpeta de marcadores y este es el
    # primer punto. Hasta [T-071] era 7, que era lo que devolvía un maniquí
    # puesto en lugar de `record_practice`: la ruta contestaba sin tocar el disco.
    #
    # 🔑 Y desde [D-066] son CUATRO piezas, no tres: `score` cuenta aciertos y
    # `practice` cuenta intentos. Aquí valen lo mismo porque el maniquí aprueba.
    assert response.json() == {
        "verdict": fake_tutor.STUB_VERDICT,
        "words": 3,
        "score": 1,
        "practice": 1,
    }


def test_practice_writes_the_score_inside_the_temporary_folder(logged_in, tmp_path):
    """🚨 El punto llega al DISCO, y al disco desviado — no a `data/` de verdad.

    Este test y el portero de `no_data_writes.py` parecen el mismo y vigilan cosas
    distintas, y conviene tener claro cuál aguanta qué:

    - El **portero** comprueba que nadie escribió en `data/` real. Cubre cualquier
      camino, incluso los que no existen todavía. Pero se queda verde si nadie
      escribe **nada** — y un maniquí puesto en lugar de `record_practice` es
      exactamente eso: nadie escribe, portero contento, y el camino completo
      (ruta → agente → marcador → disco) otra vez sin recorrer por ningún test.
    - **Este test** exige ver el archivo aparecer. Si mañana alguien vuelve a
      poner un maniquí `autouse`, el portero no dice nada y este se pone rojo.

    🔑 Un vigía que solo mira que no pase nada malo no ve que deje de pasar lo
    bueno. Hacen falta los dos.
    """
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 200

    written = tmp_path / "users" / f"{USER}.json"
    assert written.exists(), "el punto no llegó al disco: ¿hay un maniquí puesto?"
    assert json.loads(written.read_text(encoding="utf-8")) == {
        "score": 1,
        "practice": 1,
    }


def test_the_api_gives_the_same_result_as_the_terminal(logged_in, monkeypatch):
    # La regla del paso 2: cambia la puerta, no el resultado. Lo que devuelve
    # la ruta tiene que ser exactamente lo que devuelve el agente por dentro.
    #
    # 🔑 Aquí sí hace falta congelar `record_practice`, y es el único sitio. Este test
    # llama DOS veces —una por cada puerta— y el marcador de verdad avanza entre
    # las dos: la primera daría 1 y la segunda 2. Compararlas diría que las
    # puertas discrepan cuando lo único que pasó es que se sumó un punto.
    # Congelado, lo que quede distinto es una diferencia de verdad.
    monkeypatch.setattr(english_tutor, "record_practice", lambda user, correct: Counters(score=7, practice=7))

    reply = english_tutor.respond("I like coffee", USER)
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.json() == {
        "verdict": reply.verdict,
        "words": reply.words,
        "score": reply.score,
        "practice": reply.practice,
    }


# ── Lo que se rechaza ─────────────────────────────────────────────────────
#
# Denegar por defecto: lo que no encaje con lo declarado, no entra. Y todo esto
# lo para FastAPI ANTES de que el agente vea nada.


@pytest.mark.parametrize(
    "reason, body",
    [
        ("falta todo", {}),
        ("falta la frase", {}),
        ("la frase es un numero", {"sentence": 42}),
        ("la frase es null", {"sentence": None}),
        ("la frase es una lista", {"sentence": ["I like coffee"]}),
    ],
)
def test_practice_rejects_a_body_that_is_not_a_sentence(logged_in, reason, body):
    response = client.post("/practice", json=body)

    assert response.status_code == 422


@pytest.mark.parametrize("empty", ["", "   ", "\n\t"])
def test_practice_rejects_an_empty_sentence(logged_in, empty):
    # Una frase vacía no es practicar inglés, y sumaría un punto por nada.
    response = client.post("/practice", json={"sentence": empty})

    assert response.status_code == 422


# ── 🚨 Quién practica sale de la tarjeta, y de ningún otro sitio ──────────
#
# Aquí vivían los tests del nombre que llegaba en el cuerpo: recorrido de ruta,
# nombres que Windows reserva, normalización. **Ya no se pueden escribir**, y
# eso es el paso 5: no es que el freno haya mejorado, es que la puerta por la
# que entraba el nombre ya no existe. Las reglas del nombre siguen probadas
# donde les toca —`test_tools.py` y `test_accounts.py`—, que es donde el nombre
# sí llega de fuera.


def test_practice_needs_a_session():
    # 🔑 Sin este 401, todo lo demás del paso 5 sería decorado: se seguiría
    # practicando sin identificarse.
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 401


def test_practice_refuses_a_tampered_card():
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.set(
        sessions.SESSION_COOKIE, client.cookies[sessions.SESSION_COOKIE] + "x"
    )

    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 401


def test_a_user_in_the_body_is_ignored(logged_in, monkeypatch):
    # 🔑 **El test que demuestra que el agujero de [D-013] está cerrado.**
    # Se entra como `juan` y se manda `{"user": "ana"}` en el cuerpo: el punto
    # tiene que caer en el marcador de juan. Si cayera en el de ana, el paso 5
    # estaría deshecho aunque todo lo demás siguiera en verde.
    scored = []

    def remember(user, correct):
        scored.append(user)
        return Counters(score=7, practice=7)

    monkeypatch.setattr(english_tutor, "record_practice", remember)

    client.post("/practice", json={"user": "ana", "sentence": "I like coffee"})

    assert scored == [USER]


def test_nobody_can_practice_as_someone_else(monkeypatch):
    # El ataque completo, tal y como funcionaba hasta hoy: sin cuenta ninguna,
    # mandar el nombre de otra persona y sumarle puntos.
    def boom(*args, **kwargs):
        raise AssertionError("el agente no deberia haber corrido")

    monkeypatch.setattr("app.api.respond", boom)

    response = client.post(
        "/practice", json={"user": "juan", "sentence": "I like coffee"}
    )

    assert response.status_code == 401


def test_the_scored_name_comes_from_the_card(monkeypatch):
    # 🔑 `  JUAN ` y `juan` son la misma persona y tienen que caer en el mismo
    # marcador. Windows los junta solo y Linux no: sin normalizar, en la nube del
    # paso 7 serian dos personas distintas sin que saltara ningun error.
    #
    # Ahora eso se comprueba al REGISTRARSE, que es el unico momento en que el
    # nombre llega escrito a mano. A partir de ahi la tarjeta ya lo lleva en su
    # forma unica, y el marcador la recibe tal cual.
    scored = []

    def remember(user, correct):
        scored.append(user)
        return Counters(score=7, practice=7)

    monkeypatch.setattr(english_tutor, "record_practice", remember)

    client.post("/register", json={"user": "  JUAN ", "password": GOOD_PASSWORD})
    client.post("/practice", json={"sentence": "I like coffee"})

    assert scored == ["juan"]


# ── Cuando algo se rompe ──────────────────────────────────────────────────
#
# 🔑 El detalle completo va al log; al navegador, un mensaje corto y sin rutas.
# Ni contar de más (regalar cómo está organizado el servidor por dentro) ni de
# menos (un 500 mudo que no explica nada).

@pytest.fixture
def broken_score(monkeypatch):
    """Hace que el marcador falle como si el archivo estuviera roto.

    Devuelve la ruta que va dentro del mensaje, para que los tests comprueben
    contra ella sin volver a escribirla.

    🔑 La ruta se pregunta AQUÍ, con `score_file`, no en una constante del módulo.
    Antes de [T-071] era `USERS_DIR / f"{USER}.json"` calculada al importar, y
    apuntaba a la carpeta real: quedó rancia el día que `conftest.py` empezó a
    desviar el marcador a una temporal. No rompía nada —es solo texto— pero
    comparaba contra una ruta que la app ya no usaría nunca.
    """
    path = score_file(USER)

    # El mensaje real de `ScoreFileError` lleva la ruta del archivo dentro. Es el
    # que se escribió para la terminal, y es justo el que NO debe salir a la red.
    def broken(*args, **kwargs):
        raise ScoreFileError(f"El marcador {path} no es un JSON valido.")

    monkeypatch.setattr(english_tutor, "record_practice", broken)
    return path


def test_practice_answers_500_when_the_score_file_is_broken(logged_in, broken_score):
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 500


def test_the_500_explains_that_the_problem_is_the_score_file(logged_in, broken_score):
    # Un 500 mudo no le sirve a nadie: quien lo reciba tiene que saber QUÉ se
    # rompió. Para esto [D-006] creó una excepción propia del proyecto.
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert "marcador" in response.json()["detail"]


def test_the_500_does_not_leak_the_file_path(logged_in, broken_score):
    # 🔑 Saber qué archivo abrir es ayuda en la terminal y es información
    # regalada en internet. Quien pregunta no puede hacer nada con esa ruta.
    response = client.post("/practice", json={"sentence": "I like coffee"})
    detail = response.json()["detail"]

    assert str(broken_score) not in detail
    assert "data" not in detail
    assert USER not in detail


def test_the_broken_score_detail_is_written_to_the_log(logged_in, broken_score, caplog):
    # Lo que no sale al navegador tiene que quedar escrito en alguna parte, o
    # el arreglo de arriba solo habría cambiado un problema por otro.
    with caplog.at_level(logging.ERROR, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert str(broken_score) in caplog.text


def test_an_unexpected_failure_does_not_answer_a_mute_500(logged_in, monkeypatch):
    # El PermissionError de T-021 salía por aquí: sin atrapar, sin mensaje y
    # sin quedar apuntado en ninguna parte.
    def boom(*args, **kwargs):
        raise PermissionError("Acceso denegado")

    monkeypatch.setattr(english_tutor, "record_practice", boom)

    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 500
    assert response.json()["detail"]


def test_an_unexpected_failure_is_written_to_the_log(logged_in, monkeypatch, caplog):
    def boom(*args, **kwargs):
        raise PermissionError("Acceso denegado")

    monkeypatch.setattr(english_tutor, "record_practice", boom)

    with caplog.at_level(logging.ERROR, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert "PermissionError" in caplog.text


# ── El freno de la cuota ──────────────────────────────────────────────────
#
# 🔑 **Este es el primer freno que vive en el servidor.** La pantalla ya
# deshabilitaba el botón, pero el navegador es de quien lo usa: `TestClient`
# manda peticiones sin pasar por ningún botón, exactamente igual que `curl`.
# Que estos tests puedan agotar la cuota ES la demostración de [T-038].


@pytest.fixture
def tiny_quota(monkeypatch):
    """Baja el tope diario a 2, para no mandar 21 peticiones en cada test."""
    monkeypatch.setattr(quota, "DAILY_LIMIT", 2)
    return 2


def test_practice_spends_quota(logged_in):
    client.post("/practice", json={"sentence": "I like coffee"})

    assert quota.read_usage(USER) == 1


def test_practice_answers_429_when_the_quota_runs_out(logged_in, tiny_quota):
    for _ in range(tiny_quota):
        assert client.post("/practice", json={"sentence": "I like coffee"}).status_code == 200

    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 429


def test_the_429_says_why_it_was_stopped(logged_in, tiny_quota):
    # 🔑 Un 429 pelado deja adivinando si el servidor está caído, si es un fallo
    # de quien pregunta o si es a propósito. El motivo va dentro.
    for _ in range(tiny_quota):
        client.post("/practice", json={"sentence": "I like coffee"})

    detail = client.post("/practice", json={"sentence": "I like coffee"}).json()["detail"]

    assert str(tiny_quota) in detail


def test_the_reason_is_written_to_the_log(logged_in, tiny_quota, caplog):
    # 🚨 **INFO, y pedirlo aquí ya NO es bajar el listón — pero solo desde
    # [T-033].** Antes este `at_level` era la trampa de [L-012]: ponía el test en
    # verde con un renglón que en el servidor no existía, porque sin log
    # configurado el nivel efectivo era WARNING.
    #
    # 🔑 **Lo que hace legítimo este INFO no está en este test, está en
    # `configure_logging`.** Y quien comprueba que ese nivel es de verdad el del
    # servidor es `test_the_configured_log_makes_info_visible`, en
    # `test_log_config.py`. Sin ese test, esta línea volvería a aprobarse sola.
    for _ in range(tiny_quota):
        client.post("/practice", json={"sentence": "I like coffee"})

    with caplog.at_level(logging.INFO, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert "Cuota agotada" in caplog.text


def test_a_refused_practice_does_not_reach_the_tutor(logged_in, tiny_quota, monkeypatch):
    # 🚨 El freno frena de verdad: cuando muerde, el tutor ni se entera. En el
    # paso 8 esa línea es la que separa gastar dinero de no gastarlo.
    asked = fake_tutor.install(monkeypatch)

    for _ in range(tiny_quota + 3):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert len(asked) == tiny_quota


def test_an_empty_sentence_does_not_spend_quota(logged_in):
    # Se rechaza en la puerta con un 422, no llega al tutor y no cuesta nada.
    # Cobrar por ella castigaría un dedazo.
    client.post("/practice", json={"sentence": "   "})

    assert quota.read_usage(USER) == 0


def test_two_people_do_not_share_the_quota(tiny_quota):
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    for _ in range(tiny_quota):
        client.post("/practice", json={"sentence": "I like coffee"})
    client.post("/logout")

    client.post("/register", json={"user": "ana", "password": GOOD_PASSWORD})
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 200


def test_the_quota_is_not_spent_by_someone_without_a_session():
    # Sin sesión no hay a quién cobrarle: se contesta 401 antes de tocar nada.
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 401


@pytest.fixture
def broken_quota(monkeypatch, tmp_path):
    """Deja el contador de cuota de USER con basura dentro."""
    # La raiz entera se muda, y la cuota cuelga de ella ([D-037]).
    root = tmp_path / "broken-root"
    directory = root / "quota"
    directory.mkdir(parents=True)
    monkeypatch.setenv(config.DATA_DIR_NAME, str(root))
    path = directory / f"{USER}.json"
    path.write_text("esto no es json", encoding="utf-8")
    return path


def test_a_broken_quota_counter_answers_500(logged_in, broken_quota):
    # 🚨 Denegar por defecto: el freno averiado NO deja pasar.
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 500


def test_the_broken_quota_500_does_not_leak_the_file_path(logged_in, broken_quota):
    detail = client.post("/practice", json={"sentence": "I like coffee"}).json()["detail"]

    assert str(broken_quota) not in detail
    assert "data" not in detail
    assert USER not in detail


def test_the_broken_quota_detail_is_written_to_the_log(logged_in, broken_quota, caplog):
    with caplog.at_level(logging.ERROR, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert str(broken_quota) in caplog.text


# ── El tope al tamaño de la frase ─────────────────────────────────────────
#
# 🔑 El freno se escribió en el paso 6, cuando `judge_grammar` era falsa y no
# costaba nada. Desde [T-076] ya sirve para lo que se puso: esa función es una
# llamada al modelo y **se paga por el tamaño del texto**.
#
# ⚠️ Estos tests siguen sin medir el dinero: `conftest.py` desvía el juez, así
# que aquí una frase de 500 caracteres cuesta lo mismo que una de 3. Lo que se
# mide es que la puerta rechace antes de llegar al tutor.


def test_a_sentence_exactly_at_the_limit_is_accepted(logged_in):
    # El límite es "hasta aquí sí", no "hasta aquí no". Un test en el borde
    # exacto es lo único que distingue las dos cosas.
    sentence = "a" * MAX_SENTENCE_LENGTH

    response = client.post("/practice", json={"sentence": sentence})

    assert response.status_code == 200


def test_a_sentence_one_character_over_the_limit_is_refused(logged_in):
    sentence = "a" * (MAX_SENTENCE_LENGTH + 1)

    response = client.post("/practice", json={"sentence": sentence})

    assert response.status_code == 422


def test_the_refusal_says_how_long_it_was_and_how_long_it_could_be(logged_in):
    # Un "no vale" a secas deja adivinando por cuánto se pasó. Mismo criterio
    # que `normalize_user` con el nombre.
    sentence = "a" * (MAX_SENTENCE_LENGTH + 7)

    detail = client.post("/practice", json={"sentence": sentence}).json()["detail"]

    assert str(MAX_SENTENCE_LENGTH) in detail
    assert str(MAX_SENTENCE_LENGTH + 7) in detail


def test_a_sentence_too_long_does_not_reach_the_tutor(logged_in, monkeypatch):
    # 🚨 Esta es la línea que en el paso 8 separa gastar dinero de no gastarlo.
    asked = fake_tutor.install(monkeypatch)

    client.post("/practice", json={"sentence": "a" * (MAX_SENTENCE_LENGTH + 1)})

    assert asked == []


def test_a_sentence_too_long_does_not_spend_quota(logged_in):
    # Se rechaza en la puerta, no cuesta nada, no gasta cuota. Mismo criterio
    # que la frase vacía.
    client.post("/practice", json={"sentence": "a" * (MAX_SENTENCE_LENGTH + 1)})

    assert quota.read_usage(USER) == 0


def test_a_very_long_sentence_does_not_break_the_server(logged_in):
    # Un texto enorme tiene que salir por el 422, no por un 500. Si reventara,
    # el freno habría cambiado un problema de dinero por uno de caída.
    response = client.post("/practice", json={"sentence": "a" * 200_000})

    assert response.status_code == 422


# ── El timeout del tutor ──────────────────────────────────────────────────
#
# 🔑 Hoy el tutor contesta al instante, así que el freno no muerde nunca solo.
# Para verlo funcionar hay que poner un tutor lento **a propósito**. Ese es todo
# el truco: se inyecta la lentitud, igual que se inyecta el reloj en la cuota.


@pytest.fixture
def slow_tutor(monkeypatch):
    """Pone un tutor que tarda más de lo que el servidor está dispuesto a esperar.

    🚨 **Y le da su propio pool, que se espera al terminar.** Sin eso, el hilo
    colgado sigue vivo cuando el test siguiente ya empezó, y cuando por fin
    despierta llama al `record_practice` **del test siguiente**. Se vio: un test contó
    dos puntos donde solo hubo una práctica.

    🔑 Es la misma limitación que documenta el freno —un hilo no se puede matar—
    mordiendo dentro de la suite. Aquí sí hay solución, porque aquí sí se puede
    esperar: `shutdown(wait=True)` no deja pasar al siguiente test hasta que el
    tutor lento termina. Ver [L-013].
    """
    monkeypatch.setattr(api, "TUTOR_TIMEOUT_SECONDS", 0.05)

    pool = ThreadPoolExecutor(max_workers=4, thread_name_prefix="tutor-test")
    monkeypatch.setattr(api, "_TUTOR_POOL", pool)

    def slow(sentence):
        time.sleep(0.5)
        return fake_tutor.STUB_REPLY

    monkeypatch.setattr(english_tutor, "judge_grammar", slow)

    yield

    # Antes de que `monkeypatch` deshaga nada: se espera a los hilos colgados.
    pool.shutdown(wait=True)


def test_a_tutor_that_does_not_answer_in_time_gets_cut_off(logged_in, slow_tutor):
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 504


def test_the_504_says_it_can_be_retried(logged_in, slow_tutor):
    # 🔑 504 y no 500: no es que algo se rompiera, es que no llegó a tiempo.
    # Quien lo reciba tiene que entender que reintentar puede funcionar.
    detail = client.post("/practice", json={"sentence": "I like coffee"}).json()["detail"]

    assert "tardo demasiado" in detail


def test_the_timeout_is_written_to_the_log(logged_in, slow_tutor, caplog):
    # WARNING y no INFO, por lo que enseñó [L-012]: hoy un `info` no se ve.
    with caplog.at_level(logging.WARNING, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert "no contesto" in caplog.text


def test_the_caller_does_not_wait_for_the_slow_tutor(logged_in, slow_tutor):
    # 🚨 El test que de verdad mide el freno. El tutor tarda 0.5s y el tope es
    # 0.05s: si la respuesta llegara a los 0.5s, el timeout no estaría cortando
    # nada — estaría esperando igual y contestando 504 al final, que no sirve.
    started = time.monotonic()
    client.post("/practice", json={"sentence": "I like coffee"})
    waited = time.monotonic() - started

    assert waited < 0.4


def test_a_timed_out_practice_still_spends_quota(logged_in, slow_tutor):
    # ⚠️ Se cobra igual, y es a propósito. En el paso 8 esa llamada ya gastó
    # dinero aunque no devolviera nada: lo que se cobra es haber intentado.
    client.post("/practice", json={"sentence": "I like coffee"})

    assert quota.read_usage(USER) == 1


def test_a_tutor_that_answers_in_time_is_not_cut_off(logged_in, monkeypatch):
    # El otro lado del borde: el freno no puede morder a quien llega a tiempo.
    monkeypatch.setattr(api, "TUTOR_TIMEOUT_SECONDS", 5.0)

    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 200


# ── El tutor que no está disponible ───────────────────────────────────────
#
# 🚨 Distinto del timeout de arriba: aquel **no contestó a tiempo**, este
# **no contestó**. Y la diferencia que importa no es el código de estado, es el
# dinero: aquí [D-051] decide si la práctica se devuelve o se cobra, según si la
# petición llegó a salir de casa.


@pytest.fixture
def unavailable_tutor(monkeypatch):
    """Hace que el juez reviente como revienta de verdad, y deja elegir el lado.

    🔑 **El `request_sent` es el parámetro porque es el que decide el cobro.**
    Un maniquí que solo supiera fallar mediría media regla: los dos lados de la
    frontera de [D-051] tienen que poder pedirse por separado.
    """

    def install(request_sent):
        def fails(sentence):
            raise TutorUnavailableError(
                "el tutor no contesto", request_sent=request_sent
            )

        monkeypatch.setattr(english_tutor, "judge_grammar", fails)

    return install


def test_a_tutor_that_is_unavailable_answers_503(logged_in, unavailable_tutor):
    unavailable_tutor(request_sent=True)

    response = client.post("/practice", json={"sentence": "I like coffee"})

    # 🔑 503 y no 500: el servidor está bien, quien no contesta es el modelo.
    # Antes de esto caía en el `except Exception` y salía como un 500 mudo.
    assert response.status_code == 503


def test_the_503_says_it_can_be_retried(logged_in, unavailable_tutor):
    unavailable_tutor(request_sent=True)

    detail = client.post("/practice", json={"sentence": "I like coffee"}).json()["detail"]

    assert "Intentalo otra vez" in detail


def test_the_503_does_not_leak_what_broke_inside(logged_in, unavailable_tutor):
    # El motivo real —llave, red, modelo— es de quien administra, no de quien
    # practica. Mismo criterio que el 500 del marcador roto.
    unavailable_tutor(request_sent=False)

    detail = client.post("/practice", json={"sentence": "I like coffee"}).json()["detail"]

    assert "el tutor no contesto" not in detail


def test_the_unavailable_tutor_is_written_to_the_log(
    logged_in, unavailable_tutor, caplog
):
    # WARNING y no INFO, por lo que enseñó [L-012]: hoy un `info` no se ve.
    unavailable_tutor(request_sent=False)

    with caplog.at_level(logging.WARNING, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert "no esta disponible" in caplog.text
    # 🔑 Y el log dice de qué lado cayó, que es lo que explica el cobro.
    assert "la peticion salio: no" in caplog.text


def test_a_practice_whose_request_never_left_gets_the_quota_back(
    logged_in, unavailable_tutor
):
    # 🚨 **Este es el test que mide la regla, no el que comprueba que la
    # excepción existe.** La cuota se gasta ANTES de llamar al tutor
    # (`api.py`), así que empieza en 1: si nadie la devuelve, se queda en 1.
    #
    # Llave mala, red caída, 429 del propio Anthropic: cero tokens gastados.
    # Cobrar aquí sería cobrar por trabajo que nadie empezó ([D-051]).
    unavailable_tutor(request_sent=False)

    client.post("/practice", json={"sentence": "I like coffee"})

    assert quota.read_usage(USER) == 0


def test_a_practice_whose_request_did_leave_keeps_the_quota_spent(
    logged_in, unavailable_tutor
):
    # 🚨 **El otro lado de la frontera, y es el que protege el freno.** Si esto
    # devolviera cuota, con Claude saturado cada reintento gastaría tokens y
    # ninguno gastaría cuota: el freno de facturación dejaría de frenar
    # exactamente el día para el que se construyó ([D-051]).
    unavailable_tutor(request_sent=True)

    client.post("/practice", json={"sentence": "I like coffee"})

    assert quota.read_usage(USER) == 1


# ── La cola del tutor ─────────────────────────────────────────────────────
#
# 🚨 `result(timeout=)` cuenta desde que se LLAMA, no desde que la tarea
# arranca. Con el pool lleno, el tiempo de espera en la cola se le cargaba a
# quien esperaba en ella: se cobraba una práctica que nunca llegó al tutor.
# Medido: 23 peticiones a la vez, 20 llegaron, 3 pagaron por nada. Ver [L-013].


def test_the_pool_size_is_written_down_not_inherited_from_the_machine():
    # 🔑 `ThreadPoolExecutor()` sin número saca el tamaño de las CPUs: aquí 20,
    # en la nube otro. Un freno que cambia de tamaño según dónde corra no se
    # puede razonar, y este decide a quién se le cobra.
    assert api.TUTOR_POOL_SIZE == 40
    assert api._TUTOR_POOL._max_workers == api.TUTOR_POOL_SIZE


def test_the_pool_matches_the_threads_fastapi_actually_uses():
    # 🚨 **El número ya no se hereda de la máquina, pero su RAZÓN sí se heredaba.**
    #
    # El 40 solo es correcto porque FastAPI manda las rutas `def` a hilos con
    # `anyio`, y el limitador por defecto de `anyio` trae 40 fichas. De ahí sale
    # el invariante que sostiene el freno: si no puede haber más de 40 peticiones
    # a la vez, nadie espera en la cola del tutor.
    #
    # 🔑 Y ese 40 es el defecto de una librería que ni siquiera fijamos: `anyio`
    # entra de rebote con `fastapi`. Si cambia, el invariante se rompe **en
    # silencio** y vuelve el cobro por espera de [L-013] — sin que nadie toque
    # una línea de este proyecto.
    #
    # Un invariante que depende del defecto de otro necesita quien lo vigile.
    # Esto es ese vigilante: cuando los dos números dejen de coincidir, sale rojo
    # aquí y no en producción.
    async def default_thread_limit():
        return anyio.to_thread.current_default_thread_limiter().total_tokens

    assert asyncio.run(default_thread_limit()) == api.TUTOR_POOL_SIZE


@pytest.fixture
def one_tutor_at_a_time(monkeypatch):
    """Deja el pool en un solo sitio, para que el segundo tenga que hacer cola."""
    pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="tutor-test")
    monkeypatch.setattr(api, "_TUTOR_POOL", pool)
    yield pool
    # `wait=True` por lo mismo que en `slow_tutor`: un hilo colgado que despierta
    # dentro del test siguiente le suma puntos que no son suyos.
    pool.shutdown(wait=True)


def test_a_practice_that_never_left_the_queue_is_not_charged(
    logged_in, one_tutor_at_a_time, monkeypatch
):
    # 🔑 Dos peticiones, un solo sitio. La primera entra al tutor y se cuelga; la
    # segunda se queda en la cola y se corta sin haber empezado nada.
    # Se cobra el intento, no la espera: solo la primera paga.
    monkeypatch.setattr(api, "TUTOR_TIMEOUT_SECONDS", 0.2)
    started = []

    def slow(sentence):
        started.append(sentence)
        time.sleep(2)
        return fake_tutor.STUB_REPLY

    monkeypatch.setattr(english_tutor, "judge_grammar", slow)
    cookies = dict(client.cookies)

    def practice(_):
        other = TestClient(app)
        other.cookies.update(cookies)
        return other.post("/practice", json={"sentence": "I like coffee"}).status_code

    with ThreadPoolExecutor(max_workers=2) as callers:
        codes = list(callers.map(practice, range(2)))

    assert codes == [504, 504]
    assert len(started) == 1
    assert quota.read_usage(USER) == 1


def test_the_log_says_whether_the_tutor_had_started(logged_in, slow_tutor, caplog):
    # Sin este dato, dos 504 idénticos en el log esconden dos cosas distintas:
    # una que costó dinero y otra que no.
    with caplog.at_level(logging.WARNING, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert "empezo: si" in caplog.text


# ── El marcador después del 504 ───────────────────────────────────────────


def test_a_timed_out_practice_still_adds_the_point_afterwards(logged_in, monkeypatch):
    # ⚠️ **Decidido a propósito, no heredado.** El tutor sigue corriendo tras el
    # 504 y acaba llamando a `record_practice`: el marcador sube cuando quien preguntó
    # ya se fue con un error.
    #
    # 🔑 Se deja así porque esa frase SÍ se practicó — lo único que no llegó a
    # tiempo fue la respuesta. Desde [D-066] eso lo dice `practice`, que es
    # exactamente el contador que debe subir aquí; `score` subirá o no según el
    # veredicto que acabe llegando.
    # Deshacerlo tampoco se podría: habría que coordinarse con un hilo que no se
    # controla. El precio es que el número de la pantalla se ve viejo.
    monkeypatch.setattr(api, "TUTOR_TIMEOUT_SECONDS", 0.05)
    # Pool propio: sin él, un tutor colgado de otro test caería en este `scored`
    # y contaría un punto que nadie practicó aquí.
    pool = ThreadPoolExecutor(max_workers=1, thread_name_prefix="tutor-test")
    monkeypatch.setattr(api, "_TUTOR_POOL", pool)

    scored = []
    monkeypatch.setattr(english_tutor, "record_practice", lambda user, correct: scored.append(user) or Counters(7, 7))

    def slow(sentence):
        time.sleep(0.3)
        return fake_tutor.STUB_REPLY

    monkeypatch.setattr(english_tutor, "judge_grammar", slow)

    response = client.post("/practice", json={"sentence": "I like coffee"})
    assert response.status_code == 504
    assert scored == []  # todavia no: el tutor sigue trabajando

    pool.shutdown(wait=True)  # se espera al tutor colgado, en vez de adivinar
    assert scored == [USER]  # y el punto entro despues, sin nadie mirando


# ── El freno de intentos contra /login ────────────────────────────────────
#
# 🔑 **Este freno protege las contraseñas, no la factura**, y por eso cuenta por
# ORIGEN de la petición y no por persona: quien está probando contraseñas todavía
# no ha demostrado ser nadie. Ver [D-025] y [D-026].
#
# El contador vive en memoria y `conftest.py` lo vacía antes de cada test.


@pytest.fixture
def tiny_attempts(monkeypatch):
    """Baja el tope a 2 fallos, para ver el freno morder sin escribir seis."""
    monkeypatch.setattr(login_guard, "MAX_FAILED_ATTEMPTS", 2)


def fail_login() -> int:
    """Un intento con la contraseña equivocada. Devuelve el código."""
    return client.post(
        "/login", json={"user": USER, "password": "la-que-no-es-larguisima"}
    ).status_code


def test_login_answers_429_after_too_many_failures(tiny_attempts):
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    # Los dos primeros fallan por la contraseña: 401, que es "no eres tu".
    assert fail_login() == 401
    assert fail_login() == 401

    # El tercero ya no llega a mirar la contraseña: 429, que es "ahora no".
    assert fail_login() == 429


def test_the_lockout_refuses_even_the_right_password(tiny_attempts):
    # 🚨 **Este es el test que dice que el freno es un freno.** Si la contraseña
    # correcta abriera igual, quien prueba a la fuerza no estaria frenado: solo
    # tendria que seguir probando hasta acertar.
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    fail_login()
    fail_login()

    response = client.post("/login", json={"user": USER, "password": GOOD_PASSWORD})

    assert response.status_code == 429
    assert sessions.SESSION_COOKIE not in response.cookies


def test_a_success_wipes_the_failed_attempts(tiny_attempts):
    # Quien se equivoca de verdad —una contraseña vieja, un dedo torcido— y
    # luego acierta no puede quedarse a un fallo del castigo.
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    fail_login()
    assert client.post(
        "/login", json={"user": USER, "password": GOOD_PASSWORD}
    ).status_code == 200
    client.cookies.clear()

    # Con el contador borrado vuelven a caber dos fallos enteros antes del 429.
    assert fail_login() == 401
    assert fail_login() == 401


def test_the_429_says_when_to_come_back(tiny_attempts):
    # 🔑 Mismo criterio que el 429 de la cuota: un frenazo sin motivo deja a quien
    # lo recibe adivinando si el servidor esta caido o si es a proposito.
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    fail_login()
    fail_login()
    response = client.post("/login", json={"user": USER, "password": GOOD_PASSWORD})

    assert response.status_code == 429
    assert "minutos" in response.json()["detail"]
    # `Retry-After` es la cabecera estandar para esto: la entienden los clientes
    # sin tener que leer el texto en español.
    assert int(response.headers["retry-after"]) > 0


def test_the_429_does_not_say_whether_the_account_exists(tiny_attempts):
    # 🚨 El freno no puede deshacer lo que [D-021] protegia: probar nombres no
    # puede decir cuales tienen cuenta. Con el origen cerrado, los dos contestan
    # exactamente lo mismo.
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    fail_login()
    fail_login()

    real = client.post("/login", json={"user": USER, "password": GOOD_PASSWORD})
    invented = client.post("/login", json={"user": "nadie", "password": GOOD_PASSWORD})

    assert real.status_code == invented.status_code == 429
    assert real.json() == invented.json()


def test_the_lockout_is_written_to_the_log(tiny_attempts, caplog):
    # 🚨 **WARNING, y aqui pesa mas que en la cuota.** El contador vive en
    # memoria: se borra entero en cada reinicio. Este renglon del log es **el
    # unico rastro que sobrevive** de que alguien estuvo probando contraseñas.
    # Escrito con `info` no aparecería en ninguna parte mientras [T-033] no
    # configure el log — se midio en [L-012].
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    fail_login()
    fail_login()

    with caplog.at_level(logging.WARNING, logger="app.api"):
        fail_login()

    assert "Demasiados intentos" in caplog.text
    # Y con el origen dentro: sin el, el renglon dice que paso pero no de donde.
    assert "testclient" in caplog.text


def test_a_registration_is_not_stopped_by_the_login_lockout(tiny_attempts):
    # ⚠️ El freno es de `/login` y solo de `/login`. `/register` no comprueba
    # ninguna contraseña contra ninguna cuenta: no hay nada que probar a la
    # fuerza ahi. Frenarlo seria castigar a quien nunca ha fallado nada.
    fail_login()
    fail_login()

    assert client.post(
        "/register", json={"user": "otro", "password": GOOD_PASSWORD}
    ).status_code == 201


# ── El interruptor del registro ───────────────────────────────────────────
#
# 🚨 **Estos son los tests que miran la rama que `conftest.py` apaga.**
#
# El `isolated_environment` pone `TEAPP_REGISTRATION_OPEN=true` con `autouse`,
# porque casi toda la suite empieza creando una cuenta. Eso deja el camino POR
# DEFECTO —el cerrado, que es el que va a correr en produccion— sin ejecutar en
# ningun test. Es la trampa de [L-031] (antes [A-009]) y la leccion de [T-052]: la suite apaga un
# ajuste para poder trabajar, y al apagarlo deja de mirar el otro lado.
#
# Aqui se anula ese `setenv` a mano y se mira el defecto.


@pytest.fixture
def registration_closed(monkeypatch):
    """Deshace el `setenv` de `conftest.py` y deja el ajuste como viene de fábrica."""
    monkeypatch.delenv(config.REGISTRATION_OPEN_NAME, raising=False)


def test_the_registration_switch_is_closed_by_default(registration_closed):
    # 🔑 Sin variable puesta, cerrado. Es la regla 3 del proyecto: lo que no se
    # permitio por escrito, se rechaza.
    assert config.registration_open() is False


def test_register_is_refused_when_the_switch_is_closed(registration_closed):
    response = client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})

    assert response.status_code == 403
    assert sessions.SESSION_COOKIE not in response.cookies


def test_the_closed_register_does_not_reach_scrypt(registration_closed, monkeypatch):
    # 🚨 **Este es el test que hace que el freno sirva de algo.** Un 403 que
    # llegara DESPUES de `accounts.register` cerraria la puerta sin ahorrar el
    # trabajo: cada intento seguiria costando 128 ms de CPU y una reescritura del
    # archivo de todas las cuentas. Lo caro es lo que hay que no hacer.
    def explode(*args, **kwargs):
        raise AssertionError("se llamo a accounts.register con el registro cerrado")

    monkeypatch.setattr(accounts, "register", explode)

    assert client.post(
        "/register", json={"user": USER, "password": GOOD_PASSWORD}
    ).status_code == 403


def test_the_closed_register_says_nothing_about_who_may_join(registration_closed):
    response = client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})

    # Dice que esta cerrado y a quien preguntar. Ni cuando abre ni quien entra:
    # eso solo serviria para saber a quien apuntar.
    assert response.json()["detail"] == api.REGISTRATION_CLOSED_MESSAGE


@pytest.mark.parametrize("written", ["yes", "1", "si", "TRUE ", "true"])
def test_only_the_exact_word_true_opens_the_registration(monkeypatch, written):
    # ⚠️ Aqui se exige la palabra exacta, al reves que en `cookie_secure`, que
    # acepta cualquier cosa que no sea "false". Alli equivocarse deja la puerta
    # cerrada; aqui equivocarse la abriria.
    monkeypatch.setenv(config.REGISTRATION_OPEN_NAME, written)

    assert config.registration_open() is (written.strip().lower() == "true")


def test_register_works_when_the_switch_is_open():
    # La otra rama, dicha con su nombre. La cubren tambien los demas tests del
    # archivo, pero de rebote: si algun dia dejan de usar `/register`, este
    # sigue vigilando que abierto signifique abierto.
    assert config.registration_open() is True
    assert client.post(
        "/register", json={"user": USER, "password": GOOD_PASSWORD}
    ).status_code == 201


def test_the_terminal_can_still_create_accounts_with_the_registry_closed(
    registration_closed,
):
    # 🚨 **El interruptor cierra la RUTA, no `accounts.register`.** Si cerrara la
    # funcion, quien administra el servidor se quedaria fuera tambien y no habria
    # forma de crear la primera cuenta. `main.py` usa esta misma llamada.
    assert accounts.register(USER, GOOD_PASSWORD) == USER
    assert accounts.user_exists(USER)


def test_the_closed_registry_is_written_to_the_log(registration_closed, caplog):
    # 🚨 **INFO, y este test cuenta una historia de ida y vuelta.** Se escribio
    # primero con INFO y MENTIA: daba verde y en uvicorn la linea no salia, porque
    # sin log configurado el nivel efectivo era WARNING ([L-012]). Se subio a
    # WARNING para que existiera. Ahora [T-033] configuro el log, INFO se ve de
    # verdad, y el renglon vuelve a su nivel honesto: el registro cerrado es el
    # estado NORMAL, no una alarma.
    #
    # 🔑 El nivel se comprueba, no solo el texto: si alguien lo subiera otra vez
    # "por si acaso", este test lo dice.
    with caplog.at_level(logging.INFO, logger="app.config"):
        config.log_registration_mode()

    assert "CERRADO" in caplog.text
    assert [r.levelname for r in caplog.records] == ["INFO"]


# ── El interruptor de la cookie segura ────────────────────────────────────
#
# 🚨 **Esto es [T-052], y es el gemelo del bloque de arriba.**
#
# El `isolated_environment` pone `TEAPP_COOKIE_SECURE=false` con `autouse`,
# porque `TestClient` habla por `http://` y descartaria una cookie `Secure`.
# Igual que con el registro, apagar el ajuste para poder trabajar deja **la rama
# por defecto sin ningun testigo** — y aqui el defecto es `true` (`config.py`,
# `cookie_secure`): o sea que **lo que se queda sin correr es produccion**, no un
# caso raro. Es exactamente [L-031] (antes [A-009]).
#
# 📌 **Se mira la cabecera `Set-Cookie` en crudo, no el tarro de galletas del
# cliente.** El tarro de `TestClient` se comporta como un navegador de verdad y
# tirar la cookie es justo lo que hace bien; lo que hay que comprobar es lo que
# el servidor **envio**, que es lo que un navegador por `https://` si guardaria.


@pytest.fixture
def cookie_secure_by_default(monkeypatch):
    """Deshace el `setenv` de `conftest.py` y deja el ajuste como viene de fábrica.

    🔑 Se **borra** la variable en vez de ponerla a `"true"`: así lo que se mide
    es el valor por defecto de verdad — el que va a correr en la nube si nadie
    escribe nada— y no una copia nuestra de lo que creemos que es.
    """
    monkeypatch.delenv(config.COOKIE_SECURE_NAME, raising=False)


def test_the_cookie_switch_demands_https_by_default(cookie_secure_by_default):
    # 🔑 Sin variable puesta, la cookie exige HTTPS. Regla 3: lo que no se
    # permitio por escrito —viajar en claro—, se rechaza.
    assert config.cookie_secure() is True


def test_register_sends_the_session_cookie_with_secure(cookie_secure_by_default):
    response = client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})

    assert response.status_code == 201
    assert "Secure" in response.headers["set-cookie"]


def test_login_sends_the_session_cookie_with_secure(cookie_secure_by_default):
    # ⚠️ `/register` y `/login` entregan la cookie por el MISMO sitio
    # (`_start_session`), pero se comprueban los dos por separado: el dia que
    # alguien separe esos caminos, este test se entera y el otro no.
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})
    client.cookies.clear()

    response = client.post("/login", json={"user": USER, "password": GOOD_PASSWORD})

    assert response.status_code == 200
    assert "Secure" in response.headers["set-cookie"]


def test_logout_clears_the_cookie_with_secure(cookie_secure_by_default):
    # 🚨 **El segundo sitio donde vive `cookie_secure()`**, y el que se olvida:
    # `delete_cookie` en `/logout`. Un borrado que no coincide con la cookie que
    # se entrego es un borrado que el navegador puede ignorar — y entonces
    # "cerrar sesion" no cierra nada, sin ningun error que lo cuente.
    client.post("/register", json={"user": USER, "password": GOOD_PASSWORD})

    response = client.post("/logout")

    assert response.status_code == 204
    assert "Secure" in response.headers["set-cookie"]


# ── El zombi del 504 ocupa sitio del pool ─────────────────────────────────
#
# 🚨 **Este bloque decide cuál de las dos cargas de [D-070] es falsa.** La
# auditoría del 2026-08-13 mostró que [D-070] usaba dos argumentos que no pueden
# ser ciertos a la vez:
#
#   (3) "el reembolso vive dentro del `except`, retirarlo se lo lleva"
#   (4) "la cola no se forma, por construcción: pool 40 = fichas de anyio 40"
#
# Si (4) fuera cierta, la tarea siempre arrancaría, `attempt.cancel()` devolvería
# siempre `False` y el reembolso sería código muerto — o sea (3) no defendería
# nada.


def test_a_timed_out_tutor_keeps_its_pool_seat_with_nobody_waiting(
    logged_in, monkeypatch
):
    """Tras el 504, el sitio del pool sigue ocupado aunque no quede nadie vivo.

    🔑 **Es el experimento que rompe el invariante.** El invariante de
    `TUTOR_POOL_SIZE` supone que cada petición viva ocupa un sitio del pool **y
    solo uno**. Aquí las peticiones se lanzan **una detrás de otra**, nunca a la
    vez: en ningún momento hay más de una viva. Y aun así el pool acaba lleno,
    porque el 504 devuelve el control a quien preguntó y deja al tutor dentro.
    """
    monkeypatch.setattr(api, "TUTOR_TIMEOUT_SECONDS", 0.05)
    pool = ThreadPoolExecutor(max_workers=2, thread_name_prefix="tutor-test")
    monkeypatch.setattr(api, "_TUTOR_POOL", pool)

    started = []

    def slow(sentence):
        started.append(sentence)
        time.sleep(1.5)
        return fake_tutor.STUB_REPLY

    monkeypatch.setattr(english_tutor, "judge_grammar", slow)

    # Dos peticiones SECUENCIALES. Nunca coinciden vivas.
    for _ in range(2):
        assert client.post("/practice", json={"sentence": "I like coffee"}).status_code == 504

    assert len(started) == 2  # las dos arrancaron y siguen dentro

    # Cero peticiones vivas, y sin embargo los dos sitios están ocupados: la
    # tercera se queda en la cola y NO llega a arrancar.
    quota_before = quota.read_usage(USER)
    assert client.post("/practice", json={"sentence": "I like coffee"}).status_code == 504

    assert started == ["I like coffee"] * 2, "la tercera no arrancó: estaba en cola"
    assert quota.read_usage(USER) == quota_before, "y por eso se le devolvió la cuota"

    pool.shutdown(wait=True)
