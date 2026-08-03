"""Tests del agente falso.

`respond` suma un punto al marcador real, así que aquí se sustituye `add_point`
por una versión falsa. Es el mismo truco que usa el proyecto entero: cambiar la
pieza ruidosa por una que responde siempre igual, para poder probar lo de
alrededor.
"""

from dataclasses import FrozenInstanceError

import pytest

from app import english_tutor
from app.english_tutor import TutorReply
from app.tools import FAKE_VERDICT

# Quién practica. `respond` ya no funciona sin esto, y es intencional: sin saber
# de quién es la frase no hay marcador al que sumarla.
USER = "juan"


@pytest.fixture(autouse=True)
def fake_add_point(monkeypatch):
    """Evita que los tests toquen el marcador real. Devuelve siempre 7."""
    monkeypatch.setattr(english_tutor, "add_point", lambda user: 7)


def test_respond_returns_the_grammar_verdict():
    assert english_tutor.respond("I like coffee", USER).verdict == FAKE_VERDICT


def test_respond_reports_the_word_count():
    assert english_tutor.respond("I like coffee", USER).words == 3


def test_respond_reports_the_score():
    assert english_tutor.respond("I like coffee", USER).score == 7


def test_respond_scores_the_person_who_wrote_the_sentence(monkeypatch):
    # 🔑 El test del paso 4 en el agente: el punto tiene que caer en el marcador
    # de QUIEN escribio la frase. Sin esto, `respond` podria recibir el nombre y
    # no pasarlo hacia abajo — todo seguiria en verde y los puntos irian todos
    # al mismo sitio, que es justo el fallo que este paso viene a matar.
    scored = []

    def remember(user):
        scored.append(user)
        return 7

    monkeypatch.setattr(english_tutor, "add_point", remember)

    english_tutor.respond("I like coffee", "ana")

    assert scored == ["ana"]


def test_respond_returns_the_three_pieces_separately():
    # El contrato del enchufe: entra un texto, salen TRES piezas sueltas, no un
    # texto ya cocinado. Si esto cambia, la pantalla del paso 3 se queda sin
    # poder colocar cada pieza en su sitio.
    assert isinstance(english_tutor.respond("I like coffee", USER), TutorReply)


def test_the_reply_cannot_be_modified():
    # `frozen=True`: una vez contestado, nadie cambia el veredicto por el camino.
    reply = english_tutor.respond("I like coffee", USER)

    # La excepción exacta, no `Exception` a secas: esa atraparía cualquier
    # fallo, incluido uno que no tuviera nada que ver, y el test pasaría en
    # verde por la razón equivocada.
    with pytest.raises(FrozenInstanceError):
        reply.score = 999
