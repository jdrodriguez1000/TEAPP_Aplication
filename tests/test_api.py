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

from app import english_tutor
from app.api import app
from app.tools import FAKE_VERDICT, SCORE_FILE, ScoreFileError

client = TestClient(app)


@pytest.fixture(autouse=True)
def fake_add_point(monkeypatch):
    """Evita que los tests toquen el marcador real. Devuelve siempre 7."""
    monkeypatch.setattr(english_tutor, "add_point", lambda: 7)


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


def test_the_compiled_script_is_served():
    # ⚠️ Este test es el que avisa del error previsto en [D-012]: si el `.ts` se
    # editó y no se compiló, o si el `.js` nunca llegó a Git, aquí sale un 404
    # en vez de descubrirse con una pantalla muda en el navegador.
    response = client.get("/static/app.js")

    assert response.status_code == 200


def test_the_screen_calls_practice_without_naming_a_host():
    # La ruta relativa es lo que hace que la pantalla funcione igual en local y
    # en la nube. Un `http://localhost:8000` escrito a mano funcionaría hoy y se
    # rompería el día del despliegue, que es el peor momento para enterarse.
    # Se mira la llamada en sí y no el archivo entero: los comentarios nombran
    # `localhost` para explicar justamente por qué no se usa.
    script = client.get("/static/app.js").text

    assert 'fetch("/practice"' in script
    assert 'fetch("http' not in script


# ── La ruta contesta ──────────────────────────────────────────────────────


def test_practice_answers_ok():
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 200


def test_practice_returns_the_three_pieces_separately():
    # 🔑 El test que fija la decisión del paso 2: la ruta manda los
    # ingredientes, no el plato servido. La pantalla del paso 3 lee ESTO.
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.json() == {"verdict": FAKE_VERDICT, "words": 3, "score": 7}


def test_the_api_gives_the_same_result_as_the_terminal():
    # La regla del paso 2: cambia la puerta, no el resultado. Lo que devuelve
    # la ruta tiene que ser exactamente lo que devuelve el agente por dentro.
    reply = english_tutor.respond("I like coffee")
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
        ("falta la frase", {}),
        ("la frase es un numero", {"sentence": 42}),
        ("la frase es null", {"sentence": None}),
        ("la frase es una lista", {"sentence": ["I like coffee"]}),
    ],
)
def test_practice_rejects_a_body_that_is_not_a_sentence(reason, body):
    response = client.post("/practice", json=body)

    assert response.status_code == 422


@pytest.mark.parametrize("empty", ["", "   ", "\n\t"])
def test_practice_rejects_an_empty_sentence(empty):
    # Una frase vacía no es practicar inglés, y sumaría un punto por nada.
    response = client.post("/practice", json={"sentence": empty})

    assert response.status_code == 422


# ── Cuando algo se rompe ──────────────────────────────────────────────────
#
# 🔑 El detalle completo va al log; al navegador, un mensaje corto y sin rutas.
# Ni contar de más (regalar cómo está organizado el servidor por dentro) ni de
# menos (un 500 mudo que no explica nada).

# El mensaje real de `ScoreFileError` lleva la ruta del archivo dentro. Es el
# que se escribió para la terminal, y es justo el que NO debe salir a la red.
BROKEN_WITH_PATH = f"El marcador {SCORE_FILE} no es un JSON valido."


@pytest.fixture
def broken_score(monkeypatch):
    """Hace que el marcador falle como si el archivo estuviera roto."""

    def broken(*args, **kwargs):
        raise ScoreFileError(BROKEN_WITH_PATH)

    monkeypatch.setattr(english_tutor, "add_point", broken)


def test_practice_answers_500_when_the_score_file_is_broken(broken_score):
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 500


def test_the_500_explains_that_the_problem_is_the_score_file(broken_score):
    # Un 500 mudo no le sirve a nadie: quien lo reciba tiene que saber QUÉ se
    # rompió. Para esto [D-006] creó una excepción propia del proyecto.
    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert "marcador" in response.json()["detail"]


def test_the_500_does_not_leak_the_file_path(broken_score):
    # 🔑 Saber qué archivo abrir es ayuda en la terminal y es información
    # regalada en internet. Quien pregunta no puede hacer nada con esa ruta.
    response = client.post("/practice", json={"sentence": "I like coffee"})
    detail = response.json()["detail"]

    assert str(SCORE_FILE) not in detail
    assert "data" not in detail
    assert "score.json" not in detail


def test_the_broken_score_detail_is_written_to_the_log(broken_score, caplog):
    # Lo que no sale al navegador tiene que quedar escrito en alguna parte, o
    # el arreglo de arriba solo habría cambiado un problema por otro.
    with caplog.at_level(logging.ERROR, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert str(SCORE_FILE) in caplog.text


def test_an_unexpected_failure_does_not_answer_a_mute_500(monkeypatch):
    # El PermissionError de T-021 salía por aquí: sin atrapar, sin mensaje y
    # sin quedar apuntado en ninguna parte.
    def boom(*args, **kwargs):
        raise PermissionError("Acceso denegado")

    monkeypatch.setattr(english_tutor, "add_point", boom)

    response = client.post("/practice", json={"sentence": "I like coffee"})

    assert response.status_code == 500
    assert response.json()["detail"]


def test_an_unexpected_failure_is_written_to_the_log(monkeypatch, caplog):
    def boom(*args, **kwargs):
        raise PermissionError("Acceso denegado")

    monkeypatch.setattr(english_tutor, "add_point", boom)

    with caplog.at_level(logging.ERROR, logger="app.api"):
        client.post("/practice", json={"sentence": "I like coffee"})

    assert "PermissionError" in caplog.text
