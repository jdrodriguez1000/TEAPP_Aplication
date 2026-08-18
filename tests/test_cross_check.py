"""El cruce de `T-111`, probado con filas armadas a mano.

🔑 **Se prueba con filas inventadas y no con el archivo real, a propósito.** Un
test que corra el cruce de verdad diría *"da 56"* y no probaría nada: `56` es el
dato, no el criterio. Aquí se arman las cuatro casillas una por una, con datos
donde la respuesta correcta se sabe de antemano.

⚠️ **Lo que estos tests NO hacen.** No juzgan si el juez acierta. Comprueban que la
cuenta cuenta lo que dice contar.
"""

import pytest

import cross_check
from app import tools
from measure_tutor import SENTENCES


def _label(number: int, verdict: str) -> dict:
    return {"number": number, "sentence": SENTENCES[number - 1], "verdict": verdict}


def _reply(number: int, first_line: str) -> dict:
    return {
        "number": number,
        "sentence": SENTENCES[number - 1],
        "reply": f"{first_line}\n\nUn mensaje cualquiera para quien practica.",
        "broken": [],
        "model": "claude-opus-5",
        "rubric": "bbf4be38",
    }


def test_the_four_cells_land_where_they_should():
    """Una fila de cada tipo, y cada una tiene que caer en su casilla."""
    label_rows = [
        _label(1, "correct"),   # juez OK   → acuerdo
        _label(2, "wrong"),     # juez FIX  → acuerdo
        _label(3, "correct"),   # juez FIX  → corrige de mas
        _label(4, "wrong"),     # juez OK   → PERDONA
    ]
    reply_rows = [
        _reply(1, tools.VERDICT_CORRECT),
        _reply(2, tools.VERDICT_WRONG),
        _reply(3, tools.VERDICT_WRONG),
        _reply(4, tools.VERDICT_CORRECT),
    ]

    result = cross_check.cross(label_rows, reply_rows, excluded=frozenset())

    assert result.agree_correct == 1
    assert result.agree_wrong == 1
    assert result.judge_over == 1
    assert result.judge_forgives == 1
    assert result.hits == 2
    assert result.compared == 4


def test_the_excluded_rows_do_not_reach_the_count():
    """🔒 La regla de `[D-100]`: las filas contaminadas no entran ni al denominador."""
    label_rows = [_label(1, "correct"), _label(54, "wrong"), _label(55, "correct")]
    reply_rows = [
        _reply(1, tools.VERDICT_CORRECT),
        _reply(54, tools.VERDICT_WRONG),
        _reply(55, tools.VERDICT_CORRECT),
    ]

    result = cross_check.cross(label_rows, reply_rows)

    assert result.compared == 1, "las filas 54 y 55 tenian que quedarse fuera"
    assert result.hits == 1


def test_row_37_is_not_excluded():
    """📌 La regla dice CONTENIDO o VEREDICTO expuesto; nombrar por número no excluye.

    🔑 Este test existe para que la respuesta a *"¿y la 37?"* viva en el código y no
    en la memoria de nadie. La lista sale de la regla, no al revés.
    """
    assert 37 not in cross_check.EXCLUDED_ROWS


def test_a_broken_format_is_counted_apart_and_not_as_a_disagreement():
    """⚠️ `bad_format` no es error de criterio: de la frase no se sabe nada.

    🚨 Sin esta separación, un juez que rompe el formato se lee como un juez que se
    equivoca, y los arreglos van en direcciones opuestas (`[D-067]`, `[D-094]`).
    """
    label_rows = [_label(1, "correct")]
    reply_rows = [{
        "number": 1,
        "sentence": SENTENCES[0],
        "reply": "Nice work, this sentence is perfect!",
        "broken": [],
        "model": "claude-opus-5",
        "rubric": "bbf4be38",
    }]

    result = cross_check.cross(label_rows, reply_rows, excluded=frozenset())

    assert result.bad_format == 1
    assert result.hits == 0
    assert result.judge_over == 0, "formato roto no es 'corrige de mas'"
    assert result.judge_forgives == 0, "formato roto no es 'perdona'"


def test_a_sentence_that_disagrees_between_the_two_files_stops_the_cross():
    """🚨 Cruzar por posición compararía la etiqueta con el veredicto de al lado.

    🔻 El saboteo: mismas filas, textos cambiados. Sin este freno el cruce daría un
    número **sin dar un solo error**, que es la peor forma de estar mal.
    """
    label_rows = [_label(1, "correct")]
    reply_rows = [_reply(1, tools.VERDICT_CORRECT) | {"sentence": SENTENCES[1]}]

    with pytest.raises(ValueError, match="no dice lo mismo"):
        cross_check.cross(label_rows, reply_rows, excluded=frozenset())


def test_a_label_without_its_reply_stops_the_cross():
    """Una etiqueta sin respuesta no se salta en silencio: se canta."""
    with pytest.raises(ValueError, match="no tiene respuesta"):
        cross_check.cross([_label(1, "correct")], [], excluded=frozenset())


def test_the_report_puts_raw_counts_before_the_share():
    """📏 `[D-100]`: cuentas crudas delante, porcentaje detrás.

    🔑 Sobre 58 filas cada una vale `1,72` puntos. El porcentaje es el número que
    viaja solo, así que no puede ir primero ni ir solo.
    """
    result = cross_check.Crossing(
        agree_correct=1, agree_wrong=1, judge_over=0,
        judge_forgives=0, bad_format=0, compared=2,
    )

    text = cross_check.report(result)

    assert text.index("2 de 2") < text.index("%"), (
        "el porcentaje no puede ir antes que la cuenta cruda"
    )
    assert "PERDONA" in text, "la casilla que enseña mal tiene que salir con nombre"
