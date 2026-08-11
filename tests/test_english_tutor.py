"""Tests del agente: que llame a las tres herramientas y pase el resultado.

⚠️ **Aquí no se prueba el juez, se prueba el cableado.** Desde [T-076]
`judge_grammar` es una llamada real a Claude, y `conftest.py` la sustituye por
un maniquí en toda la suite ([C-001]: ningún test sale a internet). Lo que estos
tests miden es que `respond` llame a las tres piezas, en su orden, y pase lo que
devuelvan hacia arriba tal cual. Al juez de verdad lo prueba `test_tools.py`.

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

import fake_tutor
from app import english_tutor
from app.english_tutor import TutorReply
from app.tools import TutorUnavailableError, read_score

# Quién practica. `respond` ya no funciona sin esto, y es intencional: sin saber
# de quién es la frase no hay marcador al que sumarla.
USER = "juan"


def test_respond_returns_the_grammar_verdict():
    # 🔑 El veredicto sale del maniquí de `conftest.py`, no de Claude. Desde
    # [T-076] el juez cuesta dinero y no responde igual dos veces, así que aquí
    # no se prueba QUÉ dice — se prueba que `respond` lo pasa hacia arriba tal
    # cual. Al juez de verdad lo prueba `test_tools.py`.
    assert english_tutor.respond("I like coffee", USER).verdict == fake_tutor.STUB_VERDICT


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


# ── El fallo del tutor no suma punto ──────────────────────────────────────
#
# 🚨 Los dos tests de aquí abajo vigilan la MISMA línea desde dos ángulos, y es
# a propósito: `app/english_tutor.py:53`.
#
# `TutorReply(...)` evalúa sus argumentos en el orden en que están escritos —
# `count_words`, `judge_grammar`, `add_point`—, así que una excepción del juez
# corta **antes** de tocar el marcador. Eso es lo que sostiene [D-050].
#
# 🔑 Y por eso ese orden dejó de ser cosmético. Reordenar las tres líneas
# cobraría el punto de una práctica que nunca tuvo veredicto — **sin romper la
# sintaxis y sin que nada más se pusiera rojo**. Es la misma clase de fallo mudo
# que [D-042] vigila en el Caddyfile.


def _tutor_that_fails(monkeypatch):
    """Deja al juez reventando como revienta de verdad cuando Claude falla."""

    def explode(sentence):
        raise TutorUnavailableError("el tutor no contesto", request_sent=True)

    monkeypatch.setattr(english_tutor, "judge_grammar", explode)


def test_a_tutor_failure_does_not_score_a_point(monkeypatch):
    # [D-050]: si no hubo veredicto, no hubo práctica. El marcador se queda
    # quieto — y se mira en el disco, no en lo que devuelva nadie.
    _tutor_that_fails(monkeypatch)

    with pytest.raises(TutorUnavailableError):
        english_tutor.respond("I like coffee", USER)

    assert read_score(USER) == 0


def test_the_tutor_is_asked_before_the_point_is_scored(monkeypatch):
    # 🔑 El ángulo que de verdad clava el orden. El de arriba se quedaría verde
    # si alguien sumara el punto y luego lo deshiciera; este exige que
    # `add_point` **ni siquiera se llame**.
    scored = []
    monkeypatch.setattr(
        english_tutor, "add_point", lambda user: scored.append(user) or 1
    )
    _tutor_that_fails(monkeypatch)

    with pytest.raises(TutorUnavailableError):
        english_tutor.respond("I like coffee", USER)

    assert scored == []
