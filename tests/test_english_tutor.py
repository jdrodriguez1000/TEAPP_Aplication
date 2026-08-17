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

from dataclasses import FrozenInstanceError, fields

import pytest

import fake_tutor
from app import english_tutor
from app.english_tutor import TutorReply
from app.tools import Counters, TutorUnavailableError, read_counters

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
    #
    # El maniquí de `conftest.py` aprueba, así que aquí `score` sube. Que NO
    # suba con una frase mala es el test de abajo.
    assert english_tutor.respond("I like coffee", USER).score == 1


def test_respond_reports_the_practice_count():
    assert english_tutor.respond("I like coffee", USER).practice == 1


def test_the_field_set_of_tutor_reply_is_pinned():
    """🚨 El conjunto de campos de `TutorReply`, clavado. **Añadir uno pone la
    suite en ROJO, y eso es el punto.**

    🔑 **Este test no comprueba comportamiento y no pretende comprobarlo.** No
    dice que ningún campo sea correcto. Hace **imposible que un campo nazca en
    silencio**, que es otra cosa y es la que faltaba.

    ⚠️ **Por qué hizo falta, y es un caso vivido el 2026-08-17.** `correct` se
    añadió a esta clase y llegó **sin nadie mirándolo**: saboteado con
    `correct=True` clavado en `respond`, la suite dio **447 en verde**. La causa
    no fue un descuido puntual — está en `[L-073]`: los tests cubrían las cuatro
    piezas viejas **una por una**, así que el archivo *se leía* como cobertura
    completa de la clase, y la quinta llegó después de que esa costumbre
    estuviera establecida.

    🚨 **Y `[L-073]` sola arregla el caso y deja viva la fábrica.** El test de
    `correct` guarda el campo; no guarda el mecanismo que lo dejó huérfano. Sin
    esta línea, **el sexto campo nacería exactamente igual de mudo** — y con más
    razón, porque el archivo tendría ya un test parametrizado dentro dándole
    aspecto de rigor. Es *acordarse* contra *estructura*, la misma distinción que
    `[D-037]` y `LM.20` en sus terrenos.

    📌 **`PracticeResponse` ya estaba clavado, pero por accidente:**
    `test_practice_returns_the_three_pieces_separately` compara con un
    diccionario de **igualdad exacta**, así que un campo nuevo allí sale rojo
    solo. Este test le da a `TutorReply` a propósito lo que aquel tenía de
    rebote.

    🔻 **Y si esto se pone rojo, el arreglo NO es editar este conjunto.** Es ir a
    decidir quién vigila el campo nuevo, escribirlo, y **entonces** añadirlo
    aquí. Editar el assert primero devuelve el fallo mudo con sensación de haber
    arreglado algo — `PI-6`, y `[L-068]` en directo.
    """
    assert {campo.name for campo in fields(TutorReply)} == {
        "verdict",
        "words",
        "score",
        "practice",
        "correct",
    }


@pytest.mark.parametrize("dice_el_juez", [True, False])
def test_respond_carries_the_judges_verdict_as_a_boolean(monkeypatch, dice_el_juez):
    """🚨 `correct` tiene que SEGUIR al juez, no ser un adorno que dice `True`.

    🔑 **Este test existe porque el campo nació sin él y se vio.** `correct` se
    añadió a `TutorReply` el 2026-08-17 para la traza de [D-085], y al sabotearlo
    —`correct=True` clavado a mano en `respond`, ignorando al juez— **la suite dio
    447 en verde**. Un dato que puede mentir sin que nada se entere no es un dato:
    es `[L-068]` otra vez, un campo con aspecto de cobertura y sin nadie mirando.

    ⚠️ **Y las dos ramas hacen falta, no una.** Con solo el caso `True`, el
    sabotaje exacto que se encontró —clavar `True`— seguiría pasando. Es el mismo
    motivo por el que se clava el PAR y no media firma.

    📌 No se prueba el TEXTO del veredicto, que ya tiene su test arriba. Se prueba
    la mitad de máquina, que es la única que puede entrar en un archivo (`PI-8`).
    """
    fake_tutor.install(monkeypatch, correct=dice_el_juez)

    assert english_tutor.respond("I like coffee", USER).correct is dice_el_juez


def test_a_wrong_sentence_only_raises_the_practice_count(monkeypatch):
    # 🚨 [D-066] visto desde el agente, que es donde se decide. El juez dice que
    # no, y el marcador de aciertos tiene que quedarse quieto — pero la práctica
    # cuenta igual: quien falla se está esforzando.
    fake_tutor.install(monkeypatch, correct=False)

    reply = english_tutor.respond("me likes coffees", USER)

    assert (reply.score, reply.practice) == (0, 1)
    # Y se mira también en el disco: lo que devuelve `respond` podría estar bien
    # y lo escrito estar mal. Son dos cosas distintas.
    assert read_counters(USER) == Counters(score=0, practice=1)


def test_respond_scores_the_person_who_wrote_the_sentence(monkeypatch):
    # 🔑 El test del paso 4 en el agente: el punto tiene que caer en el marcador
    # de QUIEN escribio la frase. Sin esto, `respond` podria recibir el nombre y
    # no pasarlo hacia abajo — todo seguiria en verde y los puntos irian todos
    # al mismo sitio, que es justo el fallo que este paso viene a matar.
    scored = []

    def remember(user, correct):
        scored.append(user)
        return Counters(score=7, practice=7)

    monkeypatch.setattr(english_tutor, "record_practice", remember)

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
# 🚨 Los dos tests de aquí abajo vigilan lo MISMO desde dos ángulos, y es a
# propósito: el orden de las tres líneas al final de `respond`.
#
# `judge_grammar` se llama **antes** que `record_practice`, así que una excepción
# del juez corta antes de tocar el marcador. Eso es lo que sostiene [D-050].
#
# 🔑 **Antes ese orden lo garantizaba Python** —eran tres argumentos de una misma
# llamada, y se evalúan como están escritos—. Desde [D-066] son tres líneas
# sueltas, porque el veredicto hace falta como valor para saber si sube el
# acierto. El freno es el mismo; lo que cambió es que ahora se ve.
#
# Reordenarlas cobraría el punto de una práctica que nunca tuvo veredicto — **sin
# romper la sintaxis y sin que nada más se pusiera rojo**. Es la misma clase de
# fallo mudo que [D-042] vigila en el Caddyfile.


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

    # Ni acierto ni práctica: sin veredicto no hubo práctica que anotar.
    assert read_counters(USER) == Counters(score=0, practice=0)


def test_the_tutor_is_asked_before_the_point_is_scored(monkeypatch):
    # 🔑 El ángulo que de verdad clava el orden. El de arriba se quedaría verde
    # si alguien sumara el punto y luego lo deshiciera; este exige que
    # `record_practice` **ni siquiera se llame**.
    scored = []
    monkeypatch.setattr(
        english_tutor,
        "record_practice",
        lambda user, correct: scored.append(user) or Counters(1, 1),
    )
    _tutor_that_fails(monkeypatch)

    with pytest.raises(TutorUnavailableError):
        english_tutor.respond("I like coffee", USER)

    assert scored == []
