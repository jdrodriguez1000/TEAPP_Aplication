"""Los frenos del corrector de la rúbrica.

🚨 **Aquí no se llama a Claude ni una vez, y no es un atajo: es lo que hace que
este archivo pueda correr en cada `pytest`.** Las respuestas de abajo están
**inventadas a mano**, escritas para romper una promesa concreta cada una. Medir
la rúbrica de verdad cuesta ~`$0,18` (60 llamadas × `$0,00304` medido en
`[D-079]`) y eso lo hace el eval, aparte y a mano.

🔑 **Y las frases inventadas no son un plan B, son la forma correcta aquí.** Para
comprobar que el corrector caza un asterisco hace falta una respuesta **con un
asterisco puesto a propósito** — una respuesta real puede no traer ninguno, y
entonces el test pasaría sin haber probado nada.

📌 Ninguna frase de ninguna persona que use la app entra en este archivo (`PI-8`).
Todas están escritas para este test.

⚠️ **Este archivo enumera. Si crece, la cabecera crece con él** — `[L-074]` costó
dos conclusiones falsas por dos descripciones que se quedaron cortas sin que nadie
las tocara.
"""

import pytest

from app import rubric_check
from app.rubric_check import (
    BAD_FIRST_LINE,
    HAS_MARKDOWN,
    LEAKS_KEYWORD,
    TOO_MANY_SENTENCES,
)
from app.tools import split_verdict

# Una respuesta con el formato exactamente como lo pide la rúbrica: palabra clave
# sola en la primera línea, y debajo dos frases cortas y limpias.
WELL_FORMED = "FIX\nShe goes to school every day. Remember the s for he and she."


def test_a_well_formed_reply_breaks_nothing():
    """El caso feliz, y va primero por una razón.

    🔑 **Un corrector que dijera "roto" a todo pasaría todos los tests de abajo.**
    Cada uno de ellos comprueba que una promesa concreta salta; ninguno comprueba
    que las otras tres **no** salten. Este es el que impide el corrector que grita
    siempre, y sin él los demás no significan lo que parecen.
    """
    assert rubric_check.check_reply(WELL_FORMED) == frozenset()


def test_the_set_of_promises_is_nailed_whole():
    """🚨 Clava el CONJUNTO, no las promesas una por una. Es `[L-073]` aquí.

    Una quinta promesa que se añada a `PROMISES` sin traer su test pone esto en
    rojo. 🔑 **Y el rojo no dice "la promesa nueva está mal" —no puede saberlo—:
    dice que alguien decidió vigilar algo nuevo y hay que escribir quién lo mira.**

    ⚠️ Si esto se pone rojo, **no se edita este conjunto** para apagarlo. Se
    escribe el test de la promesa nueva y se vuelve (`PI-6`).
    """
    assert rubric_check.PROMISES == frozenset(
        {BAD_FIRST_LINE, HAS_MARKDOWN, TOO_MANY_SENTENCES, LEAKS_KEYWORD}
    )


# ---------------------------------------------------------------------------
# Promesa 1: la primera línea es una palabra, y es `OK` o `FIX`
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "answer",
    [
        # Se explica en vez de contestar el formato: el caso más probable de todos.
        "Your sentence is almost right.\nShe goes to school every day.",
        # La palabra clave está, pero acompañada. La rúbrica pide la línea sola.
        "FIX: here is your correction\nShe goes to school every day.",
        # Nada detrás de la palabra clave: no hay mensaje que enseñarle a nadie.
        "OK",
        # Vacío. Llega si el modelo contesta sin texto.
        "",
    ],
)
def test_a_first_line_that_is_not_the_keyword_is_caught(answer):
    """Los cuatro modos en que se rompe la primera línea, no solo el evidente.

    🔑 **El segundo es el que enseña.** `"FIX: here is your correction"` **contiene**
    la palabra clave, así que un corrector escrito con `in` lo dejaría pasar — y
    `split_verdict` tampoco lo acepta, porque compara la línea entera. Los dos
    tienen que estar de acuerdo, y de eso se encarga el test de más abajo.
    """
    assert BAD_FIRST_LINE in rubric_check.check_reply(answer)


def test_the_keyword_is_read_ignoring_case_and_spaces():
    """`  fix  ` es la palabra clave, porque `split_verdict` la acepta así.

    📌 Este test no está aquí por elegancia: está para que las dos funciones no
    se separen. `split_verdict` recorta y sube a mayúsculas antes de comparar; si
    el corrector fuera más estricto, marcaría como roto un formato que la app sí
    entiende — y el eval contaría fallos que no existen.
    """
    assert BAD_FIRST_LINE not in rubric_check.check_reply(
        "  fix  \nShe goes to school every day."
    )


def test_the_checker_and_split_verdict_cut_in_the_same_place():
    """🚨 El alambre contra la deriva: dos funciones parten el texto, una verdad.

    `learner_message` repite a propósito las tres líneas de `split_verdict`,
    porque necesita delatar el formato y aquella lo perdona (ver su docstring).
    **Repetir lógica se paga en deriva**, y el precio se ata aquí: si alguien
    cambia una de las dos y no la otra, esto se pone rojo.

    🔑 **Lo que se exige no es que devuelvan lo mismo** —devuelven cosas
    distintas— **sino que estén de acuerdo en dónde cortaron.**
    """
    answers = [
        WELL_FORMED,
        "OK\nThat is correct.",
        "  fix  \nShe goes to school every day.",
        "Your sentence is almost right.\nShe goes to school every day.",
        "FIX: here is your correction\nShe goes to school every day.",
        "OK",
        "",
        "FIX\n\n\nShe goes to school every day.",
    ]

    for answer in answers:
        format_ok, message = rubric_check.learner_message(answer)
        verdict = split_verdict(answer)

        if format_ok:
            # El formato estaba bien: las dos ven el mismo mensaje debajo.
            assert verdict.message == message, answer
        else:
            # El formato falló: `split_verdict` no recorta nada, y tampoco da punto.
            assert verdict.message == answer.strip(), answer
            assert verdict.correct is False, answer


# ---------------------------------------------------------------------------
# Promesa 2: nada de markdown en lo que ve el alumno
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    [
        "She goes to school every day. The *s* is what changed.",
        "She goes to school every day. Use `goes` here.",
        'She goes to school every day. Say "goes" not "go".',
        "She goes to school every day.\n- Add the s for he and she.",
        "She goes to school every day.\n* Add the s for he and she.",
        "She goes to school every day.\n  • Add the s for he and she.",
    ],
)
def test_markdown_in_the_learner_message_is_caught(message):
    """Asterisco, backtick, comilla y tres formas de viñeta.

    🔑 **Por qué importa más de lo que parece: `app/static` pinta este texto TAL
    CUAL.** No hay nada que interprete el markdown, así que un asterisco no sale
    en negrita — sale como un asterisco, delante de alguien que está aprendiendo
    y no sabe si es parte de la corrección.
    """
    assert HAS_MARKDOWN in rubric_check.check_reply(f"FIX\n{message}")


@pytest.mark.parametrize(
    "message",
    [
        # Un guion DENTRO de una frase es un guion, no una viñeta.
        "She goes to school every day. The verb changes - just a little.",
        # Un apóstrofo no es una comilla doble.
        "That's right. Well done.",
    ],
)
def test_ordinary_punctuation_is_not_markdown(message):
    """La otra mitad, y sin ella el test de arriba no dice nada.

    ⚠️ **Un corrector que marcara cualquier guion pasaría los seis casos de
    arriba y rompería la mitad de las respuestas buenas.** El eval contaría
    fallos inventados, y la conclusión sería que el modelo nuevo es peor cuando
    el roto sería el instrumento — que es `[L-057]`: una báscula que mide su
    propio tope.
    """
    assert HAS_MARKDOWN not in rubric_check.check_reply(f"OK\n{message}")


# ---------------------------------------------------------------------------
# Promesa 3: como mucho dos frases cortas
# ---------------------------------------------------------------------------


def test_more_than_two_sentences_is_caught():
    """Tres frases. La rúbrica pide dos, y el porqué está en la propia rúbrica.

    *"A1 learners give up when a reply is a list of everything they did wrong."*
    O sea: pasarse de largo no es un defecto de estilo, es el fallo que la
    rúbrica nombra por escrito.
    """
    answer = (
        "FIX\nShe goes to school every day. Remember the s. "
        "It goes with he, she and it."
    )
    assert TOO_MANY_SENTENCES in rubric_check.check_reply(answer)


@pytest.mark.parametrize(
    "message",
    [
        "She goes to school every day. Remember the s for he and she.",
        # Exactamente dos, con signos distintos: el conteo no mira solo el punto.
        "Almost! She goes to school every day.",
        # Una sola frase sin cerrar. Cero cierres no es un fallo.
        "She goes to school every day",
    ],
)
def test_two_sentences_or_fewer_pass(message):
    """El borde exacto, y el borde es donde viven estos fallos.

    🔑 **Dos tiene que pasar y tres tiene que caer**, así que se prueban los dos
    lados: con solo el caso de tres, un corrector con el límite en uno también
    pasaría — y estaría marcando como roto lo que la rúbrica pide.
    """
    assert TOO_MANY_SENTENCES not in rubric_check.check_reply(f"OK\n{message}")


# ---------------------------------------------------------------------------
# Promesa 4: la palabra clave no se le escapa al alumno
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "message",
    [
        "Your sentence is OK.",
        "I marked this FIX because of the verb.",
        # Con puntuación pegada: el corte por palabras tiene que limpiarla.
        "That one is OK, well done.",
    ],
)
def test_the_program_keyword_leaking_to_the_learner_is_caught(message):
    """La primera línea es para el programa, no para quien practica.

    La rúbrica lo dice con esas palabras: *"that first line is for the program,
    not for them"*. Un alumno que lee `FIX` no sabe qué es y no tiene por qué
    saberlo.
    """
    assert LEAKS_KEYWORD in rubric_check.check_reply(f"OK\n{message}")


@pytest.mark.parametrize(
    "message",
    [
        # La palabra inglesa en minúscula NO es la palabra clave del programa.
        "That's ok. Well done.",
        # `FIX` dentro de otra palabra tampoco.
        "Add the prefix before the verb.",
    ],
)
def test_the_english_word_is_not_the_program_keyword(message):
    """Y esta es la mitad que evita el corrector histérico.

    🔑 **Sin este test, lo cómodo es buscar `"OK" in message` y quedarse
    tranquilo** — y entonces *"that's ok"*, que es exactamente el tono cálido que
    la rúbrica pide, contaría como fallo. El instrumento castigaría justo la
    respuesta buena.
    """
    assert LEAKS_KEYWORD not in rubric_check.check_reply(f"OK\n{message}")


# ---------------------------------------------------------------------------
# Las cuatro a la vez
# ---------------------------------------------------------------------------


def test_a_reply_can_break_several_promises_at_once():
    """Devuelve un CONJUNTO, no la primera que encuentre.

    🔑 **Y esto es lo que el eval necesita de verdad.** Con sesenta respuestas, lo
    útil no es *"cuántas están rotas"* sino *"cuál de las cuatro se rompe más"* —
    porque cada una lleva a un arreglo distinto de la rúbrica. Un corrector que
    parase en la primera escondería las otras tres detrás de ella.
    """
    answer = 'Here you go:\n- Say "goes" not go. It is OK now. Try another one!'

    assert rubric_check.check_reply(answer) == frozenset(
        {BAD_FIRST_LINE, HAS_MARKDOWN, TOO_MANY_SENTENCES, LEAKS_KEYWORD}
    )
