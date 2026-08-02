"""Tests del agente falso.

`respond` suma un punto al marcador real, así que aquí se sustituye `add_point`
por una versión falsa. Es el mismo truco que usa el proyecto entero: cambiar la
pieza ruidosa por una que responde siempre igual, para poder probar lo de
alrededor.
"""

import pytest

from app import english_tutor
from app.tools import FAKE_VERDICT


@pytest.fixture(autouse=True)
def fake_add_point(monkeypatch):
    """Evita que los tests toquen el marcador real. Devuelve siempre 7."""
    monkeypatch.setattr(english_tutor, "add_point", lambda: 7)


def test_respond_returns_the_grammar_verdict():
    assert FAKE_VERDICT in english_tutor.respond("I like coffee")


def test_respond_reports_the_word_count():
    assert "Words: 3" in english_tutor.respond("I like coffee")


def test_respond_reports_the_score():
    assert "Score: 7" in english_tutor.respond("I like coffee")


def test_respond_returns_text():
    # El contrato del enchufe: entra un texto, sale un texto. Si esto cambia,
    # el paso 2 (FastAPI) y el paso 3 (la pantalla) se rompen.
    assert isinstance(english_tutor.respond("I like coffee"), str)
