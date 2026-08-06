"""Tests del agente falso.

`respond` suma un punto al marcador de verdad — y eso está bien, porque
`conftest.py` manda el marcador a una carpeta temporal nueva en cada test. Hasta
[T-071] aquí había un maniquí que sustituía `add_point` por una función que
devolvía 7 y no escribía nada; se quitó porque tapaba justo lo que hay que ver:
que `respond` de verdad llega al disco.

Por eso los marcadores empiezan en 1 y no en 7: es el primer punto en una carpeta
recién estrenada.
"""

from dataclasses import FrozenInstanceError

import pytest

from app import english_tutor
from app.english_tutor import TutorReply
from app.tools import FAKE_VERDICT

# Quién practica. `respond` ya no funciona sin esto, y es intencional: sin saber
# de quién es la frase no hay marcador al que sumarla.
USER = "juan"


def test_respond_returns_the_grammar_verdict():
    assert english_tutor.respond("I like coffee", USER).verdict == FAKE_VERDICT


def test_respond_reports_the_word_count():
    assert english_tutor.respond("I like coffee", USER).words == 3


def test_respond_reports_the_score():
    # 1, no 7: cada test estrena carpeta de marcadores, así que este es el
    # primer punto de esta persona. Y ahora el punto se escribe de verdad —
    # antes lo devolvía un maniquí y el disco no se tocaba ([T-071]).
    assert english_tutor.respond("I like coffee", USER).score == 1


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
