"""Tests de la puerta de red.

`TestClient` llama a las rutas sin levantar un servidor de verdad: no abre
ningún puerto ni hace falta tener uvicorn encendido. Por eso estos tests corren
igual de rápido que los demás.

Como en los tests del agente, aquí se sustituye `add_point` por una versión
falsa para no tocar el marcador real.
"""

import logging

import pytest
from fastapi.testclient import TestClient

from app import english_tutor, sessions
from app.api import app
from app.tools import FAKE_VERDICT, USERS_DIR, ScoreFileError

client = TestClient(app)

# Quién practica. Desde el paso 4 la ruta no atiende sin saberlo.
USER = "juan"


GOOD_PASSWORD = "una-contrasena-larga"


@pytest.fixture(autouse=True)
def fake_add_point(monkeypatch):
    """Evita que los tests toquen el marcador real. Devuelve siempre 7."""
    monkeypatch.setattr(english_tutor, "add_point", lambda user: 7)


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

    assert response.json() == {"verdict": FAKE_VERDICT, "words": 3, "score": 7}


def test_the_api_gives_the_same_result_as_the_terminal(logged_in):
    # La regla del paso 2: cambia la puerta, no el resultado. Lo que devuelve
    # la ruta tiene que ser exactamente lo que devuelve el agente por dentro.
    reply = english_tutor.respond("I like coffee", USER)
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.json() == {
        "verdict": reply.verdict,
        "words": reply.words,
        "score": reply.score,
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

    def remember(user):
        scored.append(user)
        return 7

    monkeypatch.setattr(english_tutor, "add_point", remember)

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

    def remember(user):
        scored.append(user)
        return 7

    monkeypatch.setattr(english_tutor, "add_point", remember)

    client.post("/register", json={"user": "  JUAN ", "password": GOOD_PASSWORD})
    client.post("/practice", json={"sentence": "I like coffee"})

    assert scored == ["juan"]


# ── Cuando algo se rompe ──────────────────────────────────────────────────
#
# 🔑 El detalle completo va al log; al navegador, un mensaje corto y sin rutas.
# Ni contar de más (regalar cómo está organizado el servidor por dentro) ni de
# menos (un 500 mudo que no explica nada).

# El mensaje real de `ScoreFileError` lleva la ruta del archivo dentro. Es el
# que se escribió para la terminal, y es justo el que NO debe salir a la red.
BROKEN_SCORE_PATH = USERS_DIR / f"{USER}.json"
BROKEN_WITH_PATH = f"El marcador {BROKEN_SCORE_PATH} no es un JSON valido."


@pytest.fixture
def broken_score(monkeypatch):
    """Hace que el marcador falle como si el archivo estuviera roto."""

    def broken(*args, **kwargs):
        raise ScoreFileError(BROKEN_WITH_PATH)

    monkeypatch.setattr(english_tutor, "add_point", broken)


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

    assert str(BROKEN_SCORE_PATH) not in detail
    assert "data" not in detail
    assert USER not in detail


def test_the_broken_score_detail_is_written_to_the_log(logged_in, broken_score, caplog):
    # Lo que no sale al navegador tiene que quedar escrito en alguna parte, o
    # el arreglo de arriba solo habría cambiado un problema por otro.
    with caplog.at_level(logging.ERROR, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert str(BROKEN_SCORE_PATH) in caplog.text


def test_an_unexpected_failure_does_not_answer_a_mute_500(logged_in, monkeypatch):
    # El PermissionError de T-021 salía por aquí: sin atrapar, sin mensaje y
    # sin quedar apuntado en ninguna parte.
    def boom(*args, **kwargs):
        raise PermissionError("Acceso denegado")

    monkeypatch.setattr(english_tutor, "add_point", boom)

    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 500
    assert response.json()["detail"]


def test_an_unexpected_failure_is_written_to_the_log(logged_in, monkeypatch, caplog):
    def boom(*args, **kwargs):
        raise PermissionError("Acceso denegado")

    monkeypatch.setattr(english_tutor, "add_point", boom)

    with caplog.at_level(logging.ERROR, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert "PermissionError" in caplog.text
