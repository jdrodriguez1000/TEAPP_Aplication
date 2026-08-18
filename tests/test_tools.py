"""Tests de las tres herramientas.

Ninguno toca el marcador real: los que escriben usan `tmp_path`, una carpeta
temporal que pytest crea y borra sola en cada corrida.
"""

import json
import re
from concurrent.futures import ThreadPoolExecutor
from dataclasses import fields

import pytest

import fake_tutor
from app import api, config, tools
from app import rubric_check
from app.tools import (
    EFFORT,
    MAX_TOKENS,
    MAX_USER_LENGTH,
    MODEL_NAME,
    LOCAL_WORK_SECONDS,
    SURRENDER_MARGIN_SECONDS,
    TIMEOUT,
    TIMEOUT_SECONDS,
    Counters,
    GrammarVerdict,
    InvalidUserError,
    ScoreFileError,
    TutorUnavailableError,
    count_words,
    judge_grammar,
    normalize_user,
    read_counters,
    record_practice,
    score_file,
    split_verdict,
)

# Una persona cualquiera, para los tests que no van sobre el nombre.
USER = "juan"


def practice_ok(name, users_dir=None):
    """Una práctica ACERTADA. Atajo para los tests que van del archivo.

    La mayoría de los tests de aquí abajo no prueban el veredicto: prueban el
    candado, la escritura atómica y qué pasa con un archivo roto. A esos les da
    igual si la frase estaba bien, y escribir `correct=True` en cada uno solo
    añadiría ruido a lo que sí importa.

    Que `score` suba o no según el veredicto tiene sus propios tests, y usan
    `record_practice` directamente para que se vea el `correct`.
    """
    return record_practice(name, correct=True, users_dir=users_dir)


# ── count_words ───────────────────────────────────────────────────────────


def test_count_words_counts_a_simple_sentence():
    assert count_words("I like coffee") == 3


def test_count_words_ignores_extra_spaces():
    # Los espacios de más no son palabras.
    assert count_words("  I   like    coffee  ") == 3


def test_count_words_of_empty_string_is_zero():
    assert count_words("") == 0


def test_count_words_splits_on_newlines():
    # `split()` sin argumentos parte por cualquier espacio en blanco, no solo
    # por el espacio. Este test lo deja clavado: si alguien lo cambia por
    # `split(" ")`, esto se pone rojo.
    assert count_words("I like\ncoffee") == 3


def test_count_words_splits_on_tabs():
    assert count_words("I\tlike\tcoffee") == 3


@pytest.mark.parametrize("not_a_sentence", [None, 42, ["hola"], {"a": 1}, 3.5])
def test_count_words_rejects_anything_that_is_not_text(not_a_sentence):
    # En el paso 2 esto llega de internet: FastAPI recibe JSON y por ahi entra
    # un numero, un null o una lista. Avisar es mejor que convertir en silencio.
    with pytest.raises(TypeError):
        count_words(not_a_sentence)


def test_the_type_error_says_what_arrived():
    # El mensaje tiene que nombrar lo que llego, o no sirve para depurar.
    with pytest.raises(TypeError, match="int"):
        count_words(42)


# ── judge_grammar ─────────────────────────────────────────────────────────


# 🚨 **Este bloque es el ÚNICO sitio donde se recorre `judge_grammar` entera.**
#
# `conftest.py` pone un maniquí en `english_tutor.judge_grammar` para toda la
# suite, así que `test_api.py` y `test_english_tutor.py` no la tocan nunca. Si
# estos tests desaparecen, el juez se queda sin nadie que lo mire.
#
# Ninguno sale a internet: el cliente falso entra por el parámetro `client`, que
# existe exactamente para esto ([D-052]). Hasta [T-076] aquí había dos tests que
# decían en voz alta que la herramienta era falsa —una frase correcta y una rota
# recibían la misma respuesta—; el paso 8 los mató, que era su trabajo.


def test_judge_grammar_returns_what_the_model_answered():
    # 🔑 Desde [D-066] ya no devuelve texto: devuelve el fallo y el mensaje
    # separados. La palabra clave de la primera línea NO viaja en `message` —
    # si viajara, la pantalla le enseñaría el `OK` a quien está practicando.
    client = fake_tutor.answering("OK\nGood sentence!")

    assert judge_grammar("I like coffee", client) == GrammarVerdict(
        outcome="correct", message="Good sentence!", broken=frozenset()
    )


def test_judge_grammar_sends_the_sentence_to_the_model():
    client = fake_tutor.answering("Good sentence!")

    judge_grammar("I like coffee", client)

    assert client.calls[0]["messages"] == [
        {"role": "user", "content": "I like coffee"}
    ]


def test_judge_grammar_asks_the_model_and_the_settings_that_were_decided():
    # 🔑 No es decoración: los tres salen de [D-049] y cada uno costaba algo.
    # `MODEL_NAME` es la decisión de arrancar caro; `EFFORT` es lo que impide
    # que el pensamiento se coma el timeout; `MAX_TOKENS` es lo que impide que
    # el veredicto salga cortado. Cambiar cualquiera en silencio se nota aquí.
    client = fake_tutor.answering("Good sentence!")

    judge_grammar("I like coffee", client)

    sent = client.calls[0]
    assert sent["model"] == MODEL_NAME
    assert sent["output_config"] == {"effort": EFFORT}
    assert sent["max_tokens"] == MAX_TOKENS


def test_judge_grammar_skips_the_thinking_block_and_reads_the_text():
    # 🚨 Opus 5 piensa por defecto, así que el PRIMER trozo puede ser un bloque
    # de pensamiento vacío. Coger `content[0]` a ciegas devolvería "" y la
    # pantalla se quedaría en blanco sin un solo error.
    client = fake_tutor.answering_blocks(
        fake_tutor.FakeBlock("thinking"),
        fake_tutor.FakeBlock("text", "OK\nGood sentence!"),
    )

    assert judge_grammar("I like coffee", client) == GrammarVerdict(
        outcome="correct", message="Good sentence!", broken=frozenset()
    )


def test_judge_grammar_joins_the_text_blocks():
    # La respuesta llega en trozos, no en un texto. Si vinieran dos, se pegan.
    client = fake_tutor.answering_blocks(
        fake_tutor.FakeBlock("text", "OK\nGood "),
        fake_tutor.FakeBlock("text", "sentence!"),
    )

    assert judge_grammar("I like coffee", client) == GrammarVerdict(
        outcome="correct", message="Good sentence!", broken=frozenset()
    )


# ── Los conjuntos de campos, clavados ─────────────────────────────────────
#
# 🚨 **Estos dos no comprueban comportamiento. Impiden que un campo nazca en
# silencio**, que es otra cosa y es la que faltaba. Ver [L-073].
#
# El caso que los originó: `correct` se añadió a `TutorReply` el 2026-08-17 y
# llegó sin nadie mirándolo — saboteado con `correct=True` clavado, la suite dio
# **447 en verde**. La causa no fue un descuido: **nadie enumeraba los campos de
# ninguna clase en todo el repo**, así que un archivo con todas las piezas
# viejas cubiertas una por una *se leía* como cobertura completa de la clase.
#
# 🔑 **La línea de dónde se pone el alambre y dónde no, para que esto no crezca
# sin final:** lo lleva la clase cuyos campos **viajan en bloque a un sitio donde
# nadie los mira uno por uno** — se serializan, se persisten, o se comparan
# enteros.
#
#   TutorReply ......... a la traza ................... `test_english_tutor.py`
#   GrammarVerdict ..... al eslabón siguiente ......... aquí
#   Counters ........... al archivo de la persona ..... aquí
#   los 3 BaseModel .... a la respuesta HTTP .......... NO: ya clavados de
#                                                       rebote, porque sus tests
#                                                       comparan diccionarios de
#                                                       igualdad exacta
#
# Son tres y se acaba. Un alcance que cabe en una lista con última fila no es
# creep.


def test_the_field_set_of_grammar_verdict_is_pinned():
    """🚨 El conjunto de `GrammarVerdict`, clavado. Añadir uno pone la suite en ROJO.

    🔑 **Es el caso FUERTE de los tres, y lo dice el docstring de la propia
    clase:** *"van separados por la misma razón que en `TutorReply`: quien
    muestre la respuesta nunca debe ver la palabra clave. `message` es lo que se
    pinta en la pantalla"*.

    `message` es **texto libre del juez**, y es exactamente el campo que el
    2026-08-17 obligó a sustituir `verdict` por `correct: bool` en la traza
    ([D-085]), porque podía citar la frase del estudiante dentro. **Un campo
    nuevo y mudo aquí nace en la única clase del proyecto con antecedentes de
    llevar dentro lo que escribió una persona** — y ahora hay un `PI-8` que
    depende de que eso no pase inadvertido.

    🔻 **Si esto se pone rojo, el arreglo NO es editar este conjunto.** Es ir a
    decidir quién vigila el campo nuevo, escribirlo, y **entonces** añadirlo
    aquí. Editar el assert primero devuelve el fallo mudo con sensación de haber
    arreglado algo — `PI-6`, y [L-068] en directo.
    """
    assert {campo.name for campo in fields(GrammarVerdict)} == {
        "outcome",
        "message",
        "broken",
    }


def test_the_field_set_of_counters_is_pinned():
    """🚨 El conjunto de `Counters`, clavado. Añadir uno pone la suite en ROJO.

    🔑 **Es el caso más flojo de los tres y entra igual, por lo que dice su
    propio docstring:** *"se leen y se escriben en el mismo archivo y de una sola
    vez"*.

    Ahí está el criterio, no la importancia: **un campo nuevo viaja entero al
    archivo de una persona sin que nadie lo mire por separado.** Dos enteros con
    un trabajo estrecho no lo hacen menos cierto.

    🔻 **Si esto se pone rojo, el arreglo NO es editar este conjunto.** Es ir a
    decidir quién vigila el campo nuevo, escribirlo, y **entonces** añadirlo
    aquí. Editar el assert primero devuelve el fallo mudo con sensación de haber
    arreglado algo — `PI-6`, y [L-068] en directo.
    """
    assert {campo.name for campo in fields(Counters)} == {"score", "practice"}


# ── Partir el veredicto: [D-067] ──────────────────────────────────────────
#
# Estos no fingen a Claude ni salen a la red: `split_verdict` solo parte texto,
# así que se prueba con cadenas sueltas. Es la ventaja de tenerla aparte.


def test_split_verdict_reads_ok_and_cuts_the_keyword():
    assert split_verdict("OK\nNice sentence. Keep going.") == GrammarVerdict(
        outcome="correct", message="Nice sentence. Keep going.",
        broken=frozenset()
    )


def test_split_verdict_reads_fix_and_cuts_the_keyword():
    assert split_verdict("FIX\nTry: I cook in the morning.") == GrammarVerdict(
        outcome="wrong", message="Try: I cook in the morning.",
        broken=frozenset()
    )


def test_split_verdict_ignores_case_and_spaces_around_the_keyword():
    # El modelo escribe texto, no rellena un formulario: un " ok " sigue siendo
    # un sí. Lo que NO se perdona es que la palabra no esté (ver el de abajo).
    assert split_verdict("  ok  \nNice one.").correct is True


def test_split_verdict_keeps_the_whole_message_when_it_has_several_lines():
    answer = "FIX\nTry: I cook in the morning.\nThe verb needs no -ing here."

    assert split_verdict(answer).message == (
        "Try: I cook in the morning.\nThe verb needs no -ing here."
    )


def test_split_verdict_denies_the_point_when_the_model_skips_the_format():
    # 🚨 ESTE es el test de [D-067], y vigila un fallo MUDO. Lo que devuelve el
    # modelo es texto generado, no un contrato: algún día no pondrá la línea.
    # Ese día no puede haber acierto — un marcador que regala puntos deja de
    # significar nada, que es justo lo que [D-066] vino a arreglar.
    verdict = split_verdict("Nice sentence. Keep going.")

    assert verdict.correct is False
    # Y aun así se enseña ENTERO: el fallo de formato es del programa, no de
    # quien está practicando. Se queda sin punto, pero ve su corrección.
    assert verdict.message == "Nice sentence. Keep going."


def test_split_verdict_denies_the_point_when_there_is_only_the_keyword():
    # Sin nada detrás no hay mensaje que enseñar. Devolver `correct=True` con
    # un texto vacío dejaría la pantalla en blanco y el punto sumado.
    verdict = split_verdict("OK")

    assert verdict.correct is False
    assert verdict.message == "OK"


def test_judge_grammar_rejects_anything_that_is_not_text():
    # Igual que `count_words`: por la red entra un número, un `null` o una
    # lista, y convertirlo en silencio taparía el problema.
    with pytest.raises(TypeError, match="int"):
        judge_grammar(42, fake_tutor.answering("Good sentence!"))


def test_judge_grammar_does_not_ask_the_model_about_something_that_is_not_text():
    # 🔑 Y el freno tiene que morder ANTES de gastar dinero. Un `TypeError`
    # lanzado después de la llamada sería un error correcto y una factura igual.
    client = fake_tutor.answering("Good sentence!")

    with pytest.raises(TypeError):
        judge_grammar(42, client)

    assert client.calls == []


# ── El cliente que se construye solo ──────────────────────────────────────


def test_the_client_is_built_with_the_timeout_and_without_retries(monkeypatch):
    # 🚨 Los dos frenos de [D-053] y [D-054] en un solo test, y los dos son
    # MUDOS: sin `timeout` el SDK espera diez minutos y sin `max_retries=0`
    # reintenta dos veces, y en ninguno de los dos casos falla nada de forma
    # visible — el servidor simplemente se queda sin hilos que atender.
    #
    # Se mira cómo se CONSTRUYE el cliente, que es lo único observable desde
    # fuera sin salir a la red.
    monkeypatch.setenv(config.ANTHROPIC_KEY_NAME, "llave-de-mentira")

    built = []

    def record(**kwargs):
        built.append(kwargs)
        return fake_tutor.answering("Good sentence!")

    monkeypatch.setattr(tools.anthropic, "Anthropic", record)

    judge_grammar("I like coffee")

    assert built[0]["timeout"] == TIMEOUT
    assert built[0]["max_retries"] == 0


def test_the_timeout_is_split_by_phase_and_the_parts_add_up_to_the_budget():
    """🚨 **El test que faltaba el 2026-08-13, y sin el cual `[D-070]` mintió.**

    `httpx` NO reparte un `timeout=8.0` suelto entre las fases: **le da 8 s a
    cada una**, o sea 32 s en total. Durante media jornada el proyecto afirmó
    en tres sitios que había un techo de 8 s que nunca existió (`[L-054]`).

    🔑 **Lo que este test vigila no es que haya cuatro números: es que SUMEN.**
    Un reparto que sume 26 —el arreglo de una línea que se propuso primero— pasa
    por arreglado y sigue sin caber en los 10 s de la ruta.
    """
    fases = (TIMEOUT.connect, TIMEOUT.write, TIMEOUT.read, TIMEOUT.pool)

    assert None not in fases, "una fase sin tope es un tope que no existe"
    assert sum(fases) == TIMEOUT_SECONDS


def test_the_client_timeout_is_shorter_than_the_one_in_the_api(monkeypatch):
    # 🔑 El orden de los dos relojes ES la decisión, no una coincidencia
    # ([D-054]). Si el del cliente fuera el más largo, quien pregunta recibiría
    # el 504 del pool y el error de verdad se quedaría escondido detrás — que es
    # el mismo motivo por el que `MAX_RETRIES` vale 0.
    #
    # ⚠️ **Desde [D-070] esto se compara contra la SUMA de las fases**, no contra
    # lo que se le pasa al SDK. Es el test de arriba el que ata las dos cosas: sin
    # él, `TIMEOUT_SECONDS` podría quedarse en 8 mientras las fases suman 32, y
    # esta comparación seguiría en verde afirmando algo falso.
    assert TIMEOUT_SECONDS < api.TUTOR_TIMEOUT_SECONDS


def test_the_gap_between_the_two_clocks_fits_the_local_work():
    """🚨 **El assert que faltaba desde la sesión 71, y que `<` no cubría.**

    🔑 **«Más corto» no es suficiente: tiene que ser más corto POR ALGO.** Entre
    que el cliente se rinde y que la ruta corta hay que pagar el trabajo local de
    `respond()` —`count_words`, `add_point` escribiendo en disco con candado— más
    el margen de rendición. Eso son `0,07 + 0,50 = 0,57 s`.

    **Sabotaje que lo pone rojo:** `TIMEOUT_SECONDS = 9.9`. El hueco cae a 0,1 s,
    el test de la suma sigue verde y el `<` de arriba también — pero el cliente
    ha dejado de rendirse antes que la ruta en cuanto haya algo de disco.

    ⚠️ **Y desde `[D-075]` esto ya no es deuda aparte:** el umbral de ROJO de
    `measure_tutor.py` se deriva de `TIMEOUT_SECONDS`, así que este hueco
    sostiene también el criterio de `T-093`. Ver `[D-076]`.
    """
    hueco = api.TUTOR_TIMEOUT_SECONDS - TIMEOUT_SECONDS
    minimo = LOCAL_WORK_SECONDS + SURRENDER_MARGIN_SECONDS

    assert hueco >= minimo, (
        f"el cliente se rinde solo {hueco:.2f} s antes que la ruta, y el "
        f"trabajo local mas el margen piden {minimo:.2f} s"
    )


# ── Cuándo se devuelve la cuota y cuándo no ([D-051], [D-054]) ────────────


@pytest.mark.parametrize(
    "error, request_sent, why",
    [
        (fake_tutor.connection_error(), False, "no hubo ni conexion"),
        (fake_tutor.auth_error(), False, "401: rechazado en la puerta"),
        (fake_tutor.rate_limit_error(), False, "429: frenado en la puerta"),
        (fake_tutor.server_error(), True, "500: la frase ya iba dentro"),
    ],
)
def test_a_failure_says_whether_the_request_left_home(error, request_sent, why):
    with pytest.raises(TutorUnavailableError) as failure:
        judge_grammar("I like coffee", fake_tutor.failing(error))

    assert failure.value.request_sent is request_sent, why


def test_a_timeout_does_not_refund_the_quota():
    # 🚨 **Este test vigila el ORDEN de los `except`, no solo el resultado.**
    #
    # `APITimeoutError` HEREDA de `APIConnectionError`, y Python se queda con el
    # primer `except` que encaje. Si alguien pone el de la red primero —que se
    # lee más natural— un timeout entraría por ahí y DEVOLVERÍA la cuota. Un
    # timeout significa que la petición sí salió y los tokens ya se pagaron:
    # devolverla sería regalar cuota en el único caso que [D-051] decidió
    # cobrar. Reordenar esas líneas rompe la decisión **sin romper la sintaxis**.
    with pytest.raises(TutorUnavailableError) as failure:
        judge_grammar("I like coffee", fake_tutor.failing(fake_tutor.timeout_error()))

    assert failure.value.request_sent is True


def test_an_empty_verdict_is_an_error_and_not_an_empty_screen():
    # Pasa si el veredicto se cortó entero contra `MAX_TOKENS`. Devolver ""
    # dejaría la pantalla en blanco sin un solo error, que es peor.
    client = fake_tutor.answering_blocks(
        fake_tutor.FakeBlock("thinking"), stop_reason="max_tokens"
    )

    with pytest.raises(TutorUnavailableError):
        judge_grammar("I like coffee", client)


def test_a_verdict_cut_off_by_max_tokens_still_charges():
    # Se gastaron tokens de verdad: se cobra ([D-051]).
    client = fake_tutor.answering_blocks(
        fake_tutor.FakeBlock("thinking"), stop_reason="max_tokens"
    )

    with pytest.raises(TutorUnavailableError) as failure:
        judge_grammar("I like coffee", client)

    assert failure.value.request_sent is True


def test_a_refusal_before_any_output_refunds_the_quota():
    # 🚨 [D-054]: un rechazo del clasificador que salta ANTES de generar nada no
    # se factura en absoluto — ni entrada, ni salida. Cobrarlo le quitaría a
    # alguien una de sus 20 prácticas por algo que no costó un céntimo.
    with pytest.raises(TutorUnavailableError) as failure:
        judge_grammar("I like coffee", fake_tutor.refusing_before_output())

    assert failure.value.request_sent is False


def test_a_refusal_after_some_output_still_charges():
    # 🔑 **El test que separa [D-054] de la regla corta.** Mismo `stop_reason`
    # que el de arriba, decisión CONTRARIA: aquí ya se generó algo, así que los
    # tokens se pagaron y se cobra. Mirar solo `stop_reason` —sin mirar la
    # factura— devolvería cuota también aquí, y eso sería regalarla.
    with pytest.raises(TutorUnavailableError) as failure:
        judge_grammar("I like coffee", fake_tutor.refusing_after_output())

    assert failure.value.request_sent is True


def test_a_billed_refusal_with_no_partial_still_charges():
    # 🚨 **El guardián de [D-055], y el que tumbó al proxy anterior.**
    #
    # Por fuera esta respuesta es CALCADA a la de
    # `test_a_refusal_before_any_output_refunds_the_quota`: `content` vacío y
    # `stop_reason="refusal"`. Por dentro es lo contrario: los tokens ya se
    # pagaron. Pasa de verdad, y nos pasa a nosotros — sin streaming, que es
    # como llama `judge_grammar`, un rechazo a mitad omite el parcial.
    #
    # 🔑 Dos respuestas indistinguibles por su forma, decisión contraria. Es
    # exactamente lo que un proxy no puede hacer y el contador sí. Volver a
    # mirar `content` en vez de `usage` pone este test en rojo.
    with pytest.raises(TutorUnavailableError) as failure:
        judge_grammar(
            "I like coffee", fake_tutor.refusing_mid_output_without_partial()
        )

    assert failure.value.request_sent is True


# ── normalize_user ────────────────────────────────────────────────────────
#
# 🚨 Con este nombre se construye una RUTA DE ARCHIVO, y el nombre lo escribe
# quien usa la app. Estos tests son el freno del paso 4.


def test_normalize_user_lowercases_and_trims():
    assert normalize_user("  Juan  ") == "juan"


@pytest.mark.parametrize("written", ["juan", "Juan", "JUAN", " jUaN "])
def test_the_same_person_written_differently_is_one_person(written):
    # 🔑 El test que de verdad importa de la normalizacion. Windows no distingue
    # mayusculas y Linux si: sin esto, `Juan` y `juan` serian UNA persona en la
    # maquina local y DOS en la nube del paso 7. Sin error y en verde.
    assert normalize_user(written) == normalize_user("juan")


@pytest.mark.parametrize("empty", ["", "   ", "\n\t"])
def test_normalize_user_rejects_an_empty_name(empty):
    # Un nombre vacio daria el archivo `.json`, oculto y de nadie.
    with pytest.raises(InvalidUserError):
        normalize_user(empty)


@pytest.mark.parametrize(
    "attack",
    [
        "../CLAUDE.md",
        "../../.env",
        "..",
        ".",
        "data/score",
        "juan/../../otro",
        "C:\\Windows\\System32",
        "juan\\otro",
        "score.json",
    ],
)
def test_normalize_user_rejects_escaping_the_folder(attack):
    # 🔑 El test que de verdad importa. Sin la lista blanca, cualquiera de estos
    # saca la escritura de `data/` y aterriza donde no debe.
    with pytest.raises(InvalidUserError):
        normalize_user(attack)


@pytest.mark.parametrize("odd", ["juan perez", "josé", "juan;rm", "juan*", "juan\0x"])
def test_normalize_user_rejects_anything_outside_the_allowlist(odd):
    # Denegar por defecto: no se enumera lo prohibido —siempre falta algo— sino
    # lo permitido. Espacios, tildes y signos se quedan fuera.
    with pytest.raises(InvalidUserError):
        normalize_user(odd)


@pytest.mark.parametrize("reserved", ["con", "PRN", "aux", "nul", "com1", "lpt9"])
def test_normalize_user_rejects_windows_device_names(reserved):
    # 🔑 Validar los caracteres NO es validar el nombre: estos son letras y
    # numeros, pasan la lista blanca enteros, y Windows los reserva para
    # dispositivos incluso con extension (`con.json` sigue siendo el dispositivo).
    with pytest.raises(InvalidUserError):
        normalize_user(reserved)


def test_normalize_user_rejects_a_name_that_is_too_long():
    # Al ponerle `.json` detras se pasaria del limite del sistema de archivos, y
    # eso revienta al ESCRIBIR, no al validar: mucho mas tarde y peor.
    with pytest.raises(InvalidUserError):
        normalize_user("a" * (MAX_USER_LENGTH + 1))


def test_normalize_user_accepts_a_name_of_the_maximum_length():
    # El limite es "hasta aqui", no "menos que aqui". Sin este test, un `>=` por
    # un `>` pasaria desapercibido.
    longest = "a" * MAX_USER_LENGTH

    assert normalize_user(longest) == longest


@pytest.mark.parametrize("valid", ["juan", "ana2", "maria-lu", "user_1", "x"])
def test_normalize_user_accepts_ordinary_names(valid):
    # El freno tiene que dejar pasar lo normal. Un validador que rechaza todo
    # tambien pasaria los tests de arriba.
    assert normalize_user(valid) == valid


@pytest.mark.parametrize("not_a_name", [None, 42, ["juan"], {"a": 1}])
def test_normalize_user_rejects_anything_that_is_not_text(not_a_name):
    with pytest.raises(TypeError):
        normalize_user(not_a_name)


def test_the_invalid_name_never_becomes_a_path(tmp_path):
    # 🔑 `score_file` es el unico sitio donde un nombre se vuelve una ruta, y
    # valida por su cuenta: si algun dia lo llama alguien que se salto el filtro
    # de la puerta, tiene que negarse igual. El olvido falla hacia el lado seguro.
    with pytest.raises(InvalidUserError):
        score_file("../../CLAUDE.md", tmp_path)


def test_record_practice_refuses_to_write_outside_the_folder(tmp_path):
    # Y el mismo freno en la funcion que de verdad escribe en el disco.
    users_dir = tmp_path / "users"
    users_dir.mkdir()

    with pytest.raises(InvalidUserError):
        practice_ok("../escapado", users_dir)

    # 🔑 Estas dos lineas NO dicen lo mismo, y la segunda es la que importa.
    # La primera demuestra que no se escribio DENTRO; el test se llama "outside",
    # asi que lo que hay que demostrar es que no aparecio nada FUERA. Sin ella,
    # la linea de arriba parece cubrir la fuga y no la cubre — el unico freno de
    # verdad seria el `pytest.raises`. Es el mismo defecto de [L-003] a [L-006]:
    # la comprobacion mide algo distinto de lo que su nombre promete.
    assert list(users_dir.iterdir()) == []
    assert not (tmp_path / "escapado.json").exists()
    assert list(tmp_path.iterdir()) == [users_dir]


# ── read_counters / record_practice ────────────────────────────────────────────────


def test_read_counters_is_zero_when_the_file_does_not_exist(tmp_path):
    assert read_counters(USER, tmp_path).score == 0


def test_record_practice_creates_the_file_and_returns_one(tmp_path):
    assert practice_ok(USER, tmp_path).score == 1
    assert score_file(USER, tmp_path).exists()


def test_record_practice_accumulates(tmp_path):
    practice_ok(USER, tmp_path)
    practice_ok(USER, tmp_path)

    assert practice_ok(USER, tmp_path).score == 3


def test_the_score_survives_being_read_back(tmp_path):
    # Lo importante del marcador no es sumar: es seguir ahí mañana.
    practice_ok(USER, tmp_path)
    practice_ok(USER, tmp_path)

    assert read_counters(USER, tmp_path).score == 2


def test_record_practice_creates_the_folder_if_it_is_missing(tmp_path):
    # La primera vez que se usa la app, `data/users/` todavía no existe.
    assert practice_ok(USER, tmp_path / "data" / "users").score == 1


# ── Aciertos y prácticas: [D-066] ─────────────────────────────────────────
#
# 🚨 Aquí sí se ve el `correct`, y por eso estos NO usan `practice_ok`. Es la
# regla entera de [D-066]: `practice` siempre, `score` solo si estaba bien.
# Hasta el 2026-08-13 `score` subía pasara lo que pasara.


def test_a_correct_sentence_raises_both_counters(tmp_path):
    assert record_practice(USER, correct=True, users_dir=tmp_path) == Counters(
        score=1, practice=1
    )


def test_a_wrong_sentence_raises_only_the_practice_counter(tmp_path):
    # 🔑 ESTE es el test que no existía y por eso [A-001] sobrevivió seis días.
    # El 2026-08-13 se escribió `I cooking in these morning` —incorrecta— y el
    # marcador subió igual. Aquí queda clavado que ya no puede.
    assert record_practice(USER, correct=False, users_dir=tmp_path) == Counters(
        score=0, practice=1
    )


def test_the_two_counters_go_their_own_way(tmp_path):
    # Tres prácticas, una acertada: "1 de 3". Es el número que ve quien practica.
    record_practice(USER, correct=False, users_dir=tmp_path)
    record_practice(USER, correct=True, users_dir=tmp_path)
    record_practice(USER, correct=False, users_dir=tmp_path)

    assert read_counters(USER, tmp_path) == Counters(score=1, practice=3)


def test_the_two_counters_are_written_in_the_same_file(tmp_path):
    # 🔑 Los dos van de una sola escritura ([D-066]). Si algún día se partieran
    # en dos pasos, un fallo entre medias dejaría el archivo descuadrado sin dar
    # un solo error. Aquí se mira el archivo por dentro, no la función.
    record_practice(USER, correct=False, users_dir=tmp_path)

    saved = json.loads(score_file(USER, tmp_path).read_text(encoding="utf-8"))

    assert saved == {"score": 0, "practice": 1}


# ── Una memoria por persona ───────────────────────────────────────────────
#
# 🔑 Lo que rompe el paso 4: hasta ahora habia UN marcador para todo el mundo.


def test_two_people_do_not_share_the_score(tmp_path):
    # El test que de verdad importa del paso 4. Con un solo archivo, el segundo
    # `record_practice` devolvia 2 en vez de 1.
    practice_ok("juan", tmp_path)
    practice_ok("juan", tmp_path)

    assert practice_ok("ana", tmp_path).score == 1


def test_each_person_keeps_their_own_score(tmp_path):
    practice_ok("juan", tmp_path)
    practice_ok("juan", tmp_path)
    practice_ok("ana", tmp_path)

    assert read_counters("juan", tmp_path).score == 2
    assert read_counters("ana", tmp_path).score == 1


def test_a_broken_score_does_not_affect_the_others(tmp_path):
    # Que el archivo de una persona este roto no puede dejar sin practicar a las
    # demas: son archivos independientes y el fallo tiene que quedarse dentro.
    score_file("juan", tmp_path).parent.mkdir(parents=True, exist_ok=True)
    score_file("juan", tmp_path).write_text("esto no es json", encoding="utf-8")

    assert practice_ok("ana", tmp_path).score == 1


# ── El marcador roto ──────────────────────────────────────────────────────
#
# Un `record_practice` interrumpido a medias —un Ctrl-C, un corte de luz— deja el
# archivo escrito por la mitad. A partir de ahí hay que avisar, no adivinar:
# devolver 0 en silencio le diría "tienes cero puntos" a quien tenía seis.


def write_broken_score(users_dir, content):
    """Deja el marcador de `USER` escrito a medias. Devuelve su ruta."""
    path = score_file(USER, users_dir)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


@pytest.mark.parametrize(
    "reason, content",
    [
        ("no es json", "esto no es json"),
        ("le falta la clave score", json.dumps({"puntos": 3})),
        ("el score no es un numero", json.dumps({"score": "seis"})),
        ("el score es un booleano", json.dumps({"score": True})),
        ("el json no es un objeto", json.dumps([1, 2, 3])),
        # 🚨 Los tres de abajo son [D-068]. El primero es EL caso real: un
        # archivo del formato viejo, con el número de prácticas metido en la
        # casilla que ahora significa aciertos. Tiene que doler, no colarse.
        ("es del formato viejo", json.dumps({"score": 9})),
        ("el practice no es un numero", json.dumps({"score": 1, "practice": "dos"})),
        ("el practice es un booleano", json.dumps({"score": 1, "practice": True})),
    ],
)
def test_read_counters_raises_when_the_file_is_broken(tmp_path, reason, content):
    write_broken_score(tmp_path, content)

    with pytest.raises(ScoreFileError):
        read_counters(USER, tmp_path).score


def test_the_error_message_names_the_file(tmp_path):
    # Quien lea el error tiene que saber QUÉ archivo hay que ir a mirar.
    path = write_broken_score(tmp_path, "esto no es json")

    with pytest.raises(ScoreFileError, match=re.escape(str(path))):
        read_counters(USER, tmp_path).score


def test_record_practice_raises_on_a_broken_file(tmp_path):
    write_broken_score(tmp_path, "esto no es json")

    with pytest.raises(ScoreFileError):
        practice_ok(USER, tmp_path)


def test_record_practice_leaves_a_broken_file_untouched(tmp_path):
    # 🔑 El test que de verdad importa: no basta con que falle, tiene que dejar
    # el archivo EXACTAMENTE como estaba. Mientras el original siga entero,
    # quien lo use puede abrirlo y recuperar su marcador a mano.
    broken = '{"score": 6, "y aqui se corto la lu'
    path = write_broken_score(tmp_path, broken)

    with pytest.raises(ScoreFileError):
        practice_ok(USER, tmp_path)

    assert path.read_text(encoding="utf-8") == broken


# ── La escritura atomica ──────────────────────────────────────────────────
#
# No basta con negarse a pisar un archivo roto: hay que no crearlo. `record_practice`
# escribe al lado y renombra encima, porque renombrar es una sola operacion del
# sistema y no deja nunca el archivo a medias.


def test_record_practice_does_not_leave_temporary_files_behind(tmp_path):
    # Si el temporal sobrevive, es que el renombrado no ocurrio: se escribio
    # directamente encima y la proteccion no esta puesta.
    practice_ok(USER, tmp_path)
    practice_ok(USER, tmp_path)

    assert list(tmp_path.iterdir()) == [score_file(USER, tmp_path)]


def test_record_practice_survives_a_crash_while_writing(tmp_path, monkeypatch):
    # 🔑 El test que de verdad importa: simulamos el corte de luz reventando
    # justo en el renombrado, con el temporal ya escrito. El marcador viejo
    # tiene que seguir entero y legible.
    practice_ok(USER, tmp_path)
    practice_ok(USER, tmp_path)  # el marcador vale 2

    def blackout(*args, **kwargs):
        raise OSError("se corto la luz")

    monkeypatch.setattr("app.tools.os.replace", blackout)

    with pytest.raises(OSError):
        practice_ok(USER, tmp_path)

    # El archivo bueno ni se entero: sigue valiendo 2 y se lee sin errores.
    assert read_counters(USER, tmp_path).score == 2


# ── Dos peticiones a la vez ───────────────────────────────────────────────
#
# En la terminal escribia una persona. Con servidor, dos peticiones llegan a la
# vez de verdad, y aparecen dos fallos distintos que se parecen en el sintoma:
#
#   1. Se pelean por el archivo temporal (Windows corta con "Acceso denegado").
#   2. Las dos leen el mismo total antes de que ninguna lo haya escrito, y un
#      punto se pierde.
#
# Los tests van separados a proposito: son dos problemas y dos arreglos.

WRITERS = 50  # suficientes para que se pisen de verdad, no tantos que tarde


def add_many_points_at_once(users_dir, writers=WRITERS, user=USER):
    """Lanza `writers` hilos sumando un punto a la vez. Devuelve los marcadores.

    Devuelve solo el `score` de cada uno, no la caja entera: aquí se compara y
    se ordena, y `Counters` no tiene orden — dos marcadores no son "mayor" ni
    "menor" el uno del otro, así que no se le inventó uno.
    """
    with ThreadPoolExecutor(max_workers=writers) as pool:
        return [
            counters.score
            for counters in pool.map(
                lambda _: practice_ok(user, users_dir), range(writers)
            )
        ]


def test_record_practice_survives_two_writers_at_once(tmp_path):
    # T-021: con un temporal de nombre fijo, esto reventaba con PermissionError
    # en Windows. Ninguna llamada debe fallar.
    add_many_points_at_once(tmp_path, writers=2)

    assert read_counters(USER, tmp_path).score == 2


def test_no_points_are_lost_with_many_writers_at_once(tmp_path):
    # 🔑 T-022: el test que de verdad importa. Cada hilo suma un punto, asi que
    # el marcador final tiene que valer EXACTAMENTE lo que hilos hubo. Sin el
    # candado se quedaba en 8 o 10 de 50: los puntos se perdian en el hueco
    # entre leer y escribir.
    #
    # Sigue haciendo falta despues del paso 4: dos personas distintas ya no se
    # pisan, pero la MISMA persona con dos pestañas abiertas si.
    add_many_points_at_once(tmp_path)

    assert read_counters(USER, tmp_path).score == WRITERS


def test_no_two_writers_get_the_same_score(tmp_path):
    # Y el otro lado del mismo fallo: nadie puede recibir un numero repetido.
    # Dar el mismo "llevas 6" dos veces es mentir una de las dos.
    totals = add_many_points_at_once(tmp_path)

    assert sorted(totals) == list(range(1, WRITERS + 1))


def test_many_writers_leave_no_temporary_files_behind(tmp_path):
    # Cada escritura estrena temporal, asi que hay que comprobar que tambien se
    # limpian todos. Si no, `data/` se llenaria de basura con el uso.
    add_many_points_at_once(tmp_path)

    assert list(tmp_path.iterdir()) == [score_file(USER, tmp_path)]


def test_two_people_writing_at_once_keep_their_own_scores(tmp_path):
    # El candado es unico para todo el mundo, asi que conviene comprobar que no
    # mezcla a nadie: cada quien acaba con sus puntos, no con la suma de los dos.
    with ThreadPoolExecutor(max_workers=2) as pool:
        juan = pool.submit(add_many_points_at_once, tmp_path, WRITERS, "juan")
        ana = pool.submit(add_many_points_at_once, tmp_path, WRITERS, "ana")
        juan.result()
        ana.result()

    assert read_counters("juan", tmp_path).score == WRITERS
    assert read_counters("ana", tmp_path).score == WRITERS


# -- Los tres estados de `outcome` ------------------------------------------


def test_outcome_tells_the_learner_apart_from_a_broken_judge():
    """🚨 Lo que `correct: bool` NO podia decir, y es la razon de `[D-094]`.

    🔑 **Las dos de abajo daban `correct=False` las dos.** Una es un fallo de quien
    practica; la otra es nuestro modelo saltandose el formato. Con un booleano
    llegaban al cuaderno como el mismo dato, y los arreglos van en direcciones
    contrarias: uno a la clase de ingles, el otro a la rubrica.
    """
    assert split_verdict("FIX\nSay: I cook.").outcome == "wrong"
    assert split_verdict("Sure thing!\nSay: I cook.").outcome == "bad_format"


def test_a_broken_format_never_counts_as_a_learner_mistake():
    """⚠️ `bad_format` gana a los otros dos, y no es un empate arbitrario.

    🔑 Si la primera linea no vino, **no se leyo la frase**: el `correct=False` de
    `split_verdict` es un denegar por defecto (regla 3), no una lectura. Llamarlo
    `"wrong"` le cobraria a quien practica un fallo que fue nuestro.
    """
    verdict = split_verdict("Sure thing!\nGreat job with that sentence.")

    assert verdict.outcome == "bad_format"
    assert verdict.correct is False


def test_correct_is_derived_from_outcome_and_cannot_disagree():
    """📌 `correct` es una PROPIEDAD, no un campo: no tiene vida propia.

    🚨 **Es el freno contra las dos casillas.** Si `correct` volviera a guardarse
    aparte, podria discrepar de `outcome` — y una fila con `outcome="bad_format"` y
    `correct=True` es un estado imposible que alguien leeria como dato.
    """
    assert "correct" not in {campo.name for campo in fields(GrammarVerdict)}

    for answer, expected in [
        ("OK\nNice one.", True),
        ("FIX\nSay: I cook.", False),
        ("nonsense\nwhatever", False),
    ]:
        assert split_verdict(answer).correct is expected


def test_bad_format_and_the_broken_promise_always_agree():
    """🔒 El invariante entre los dos campos nuevos, atado en vez de prometido.

    🔑 **`outcome` nace en las ramas de `split_verdict`; `broken` sale de
    `rubric_check`.** Son dos caminos distintos sobre el mismo texto, asi que
    *podrian* desincronizarse — y entonces volverian las dos casillas que se
    contradicen. Esto lo hace imposible sin un rojo.
    """
    for answer in [
        "OK\nNice one.",
        "FIX\nSay: I cook.",
        "nonsense\nwhatever",
        "OK",
        "",
    ]:
        verdict = split_verdict(answer)

        assert (verdict.outcome == "bad_format") == (
            "bad_first_line" in verdict.broken
        ), f"outcome y broken no cuadran para {answer!r}"


def test_the_raw_answer_never_travels_out_of_the_verdict():
    """🚨 `PI-8`: del juez salen nombres de promesa, nunca la respuesta cruda.

    🔑 **La respuesta cruda puede citar dentro la frase de quien practica**
    —visto de verdad: *"Say: They are my friends"*—. Por eso `check_reply` corre
    dentro de `split_verdict`, donde el texto todavia existe, y lo que sube son
    etiquetas.
    """
    verdict = split_verdict("OK\nYou wrote it well.")

    assert all(isinstance(nombre, str) for nombre in verdict.broken)
    assert verdict.broken <= rubric_check.PROMISES
