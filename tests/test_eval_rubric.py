"""Los frenos del eval de la forma.

🚨 **Cero llamadas a Claude, y `tests/no_network.py` las tiene prohibidas en toda
la suite (`[C-001]`).** Lo que se prueba aquí es todo lo que rodea a la llamada:
sacar el texto de la respuesta, contar los fallos, y escribir el informe.

🔑 **Y eso es justo lo que se puede equivocar sin que se note.** La llamada, si
falla, falla a gritos. Un informe que cuenta mal, o un `raw_text` que saca el
texto de otra manera que la app, devuelve **números plausibles** — y un número
plausible no se audita.

⚠️ Las respuestas de abajo están **inventadas** para este archivo (`PI-8`).
"""

import hashlib
import json
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import pytest

import eval_rubric
from app import rubric_check, tools
from app.tools import judge_grammar, split_verdict
import measure_tutor
from measure_tutor import CallBudget

# ── Una respuesta de Anthropic de mentira, con la forma que importa ─────────
#
# 🔑 **Solo los tres campos que `judge_grammar` mira.** Un doble que copiara la
# respuesta entera del SDK se rompería con cada versión y no probaría más.


@dataclass
class FakeBlock:
    type: str
    text: str


@dataclass
class FakeUsage:
    input_tokens: int = 361
    output_tokens: int = 49


@dataclass
class FakeAnswer:
    content: list
    usage: FakeUsage
    stop_reason: str = "end_turn"


def answer_with(text: str, thinking_first: bool = False) -> FakeAnswer:
    """Una respuesta con el texto dado, opcionalmente detrás de un bloque vacío."""
    blocks = []

    if thinking_first:
        # Con el pensamiento encendido, Opus 5 manda un bloque `thinking` vacio
        # delante. Es el caso que hace que `content[0]` a ciegas falle.
        blocks.append(FakeBlock(type="thinking", text=""))

    blocks.append(FakeBlock(type="text", text=text))
    return FakeAnswer(content=blocks, usage=FakeUsage())


class FakeClient:
    """Un cliente que devuelve una respuesta fija, por la puerta de `judge_grammar`."""

    def __init__(self, answer):
        self._answer = answer

    @property
    def messages(self):
        return self

    def create(self, **kwargs):
        return self._answer


# ── El alambre contra la deriva ────────────────────────────────────────────


@pytest.mark.parametrize(
    "text",
    [
        "FIX\nShe goes to school every day. Remember the s.",
        "OK\nThat is correct. Well done.",
        # Formato roto: es donde las dos formas de sacar el texto podrian
        # separarse sin que nadie lo notara.
        "Your sentence is almost right.\nShe goes to school every day.",
        "  fix  \nShe goes to school every day.",
    ],
)
@pytest.mark.parametrize("thinking_first", [False, True])
def test_raw_text_agrees_with_what_judge_grammar_sees(text, thinking_first):
    """🚨 El eval y la app tienen que sacar EL MISMO texto de la respuesta.

    `eval_rubric.raw_text` repite a propósito la línea de `tools.py:542`, porque
    `judge_grammar` no devuelve el texto crudo. **Repetir se paga en deriva**, y el
    precio se ata aquí: se comprueba que partir el texto del eval da exactamente
    el veredicto que devuelve la app.

    🔑 **Y si esto se pone rojo, el fallo sería MUDO sin este test.** Las dos
    formas devolverían una cadena plausible, el informe saldría con números
    creíbles, y estaríamos midiendo una respuesta distinta de la que ve el alumno.

    ⚠️ Se prueba con y sin bloque `thinking` delante, que es el caso por el que la
    línea de `tools.py` existe.
    """
    answer = answer_with(text, thinking_first=thinking_first)

    extracted = eval_rubric.raw_text(answer)
    from_the_app = judge_grammar("I like coffee", client=FakeClient(answer))

    assert split_verdict(extracted) == from_the_app


# ── La cuenta ──────────────────────────────────────────────────────────────


def test_tally_counts_each_promise_separately():
    """Tres respuestas, tres fallos distintos, y cada uno en su casilla."""
    replies = [
        "FIX\nShe goes to school every day. Remember the s.",
        "FIX\nShe goes to school every day. Use *goes* here.",
        "Here you go\nShe goes to school every day.",
    ]

    counted = eval_rubric.tally_breaks(replies)

    assert counted[rubric_check.HAS_MARKDOWN] == 1
    assert counted[rubric_check.BAD_FIRST_LINE] == 1
    assert counted[rubric_check.TOO_MANY_SENTENCES] == 0
    assert counted[rubric_check.LEAKS_KEYWORD] == 0


def test_one_reply_breaking_three_promises_counts_in_all_three():
    """🔑 La suma de la cuenta NO es el número de respuestas rotas.

    Una sola respuesta mala puede sumar tres. Confundir las dos cifras haría decir
    *"tres respuestas malas"* cuando hay una — y el informe las enseña por
    separado justamente por esto.
    """
    # 📌 Cuatro cierres, no tres: el tope subió a tres en `[D-090]` y este ejemplo
    # tiene que seguir pasándose de largo para que la promesa 3 entre en la cuenta.
    replies = [
        'Here you go\n- Say "goes" not go. It is OK now. Try again! You can do it.'
    ]

    counted = eval_rubric.tally_breaks(replies)

    assert sum(counted.values()) == 4
    assert len(replies) == 1


def test_an_empty_run_counts_nothing_instead_of_crashing():
    """Cero respuestas es lo que queda si la primera llamada se corta.

    📌 Y pasa de verdad: la tanda para en el primer `TutorUnavailableError`. Un
    informe que reventara ahí perdería el aviso de que no hay datos, que es
    exactamente lo que hay que enseñar.
    """
    assert eval_rubric.tally_breaks([]) == {}


# ── El informe ─────────────────────────────────────────────────────────────


def test_the_report_lists_every_promise_even_the_ones_at_zero():
    """🚨 Una promesa que nunca falló TIENE que salir en el informe, con su cero.

    🔑 **Si solo se listara lo contado, una promesa sin fallos desaparecería del
    papel — y desaparecer se lee igual que "no la estoy mirando".** Es `[L-048]`:
    lo que tranquiliza sin vigilar es peor que nada.
    """
    replies = ["OK\nThat is correct. Well done."]

    text = "\n".join(eval_rubric.report_lines(replies, "claude-opus-5"))

    for promise in rubric_check.PROMISES:
        assert promise in text


def test_the_report_warns_when_the_run_was_cut_short():
    """Una tanda parcial no vale como línea base, y el informe lo tiene que decir.

    🔑 **Sin este aviso, 12 respuestas limpias de 12 se leen como "todo bien"**
    cuando lo cierto es *"se cortó en la doceava"*. Es el cero de `[A-018]`: un
    número que significa "no pude ver" impreso igual que uno que significa "no
    hubo".
    """
    partial = ["OK\nThat is correct. Well done."] * 12

    text = "\n".join(eval_rubric.report_lines(partial, "claude-opus-5"))

    assert "AVISO" in text
    assert "parciales" in text


def test_a_full_clean_run_does_not_warn():
    """La otra mitad: con las 60 no hay aviso, o el aviso no significaría nada."""
    full = ["OK\nThat is correct. Well done."] * len(eval_rubric.SENTENCES)

    text = "\n".join(eval_rubric.report_lines(full, "claude-opus-5"))

    assert "AVISO" not in text


def test_the_report_says_out_loud_that_it_does_not_judge_the_verdict():
    """🚨 El límite del instrumento va IMPRESO, no solo en el docstring.

    Un informe limpio invita a concluir *"el juez funciona"*, y lo único que dice
    es *"contestó con la forma pedida"*. 🔑 **La advertencia tiene que viajar con
    el número**, porque quien lea la salida pegada en un chat no va a abrir el
    archivo — es `LM.20`: una copia correcta que nadie alcanza no sirve.
    """
    text = "\n".join(eval_rubric.report_lines([], "claude-opus-5"))

    assert "NO dice si el veredicto acierta" in text


def test_everything_printed_is_pure_ascii():
    """`[L-001]`: la consola de Windows tumba lo que no sea ASCII.

    Los comentarios del archivo van con tildes y emoji —son explicación—, pero
    **lo que sale por pantalla, no.** Aquí se comprueba lo segundo.
    """
    replies = ['Here you go\n- Say "goes" not go. It is OK now. Try again!'] * 3

    for line in eval_rubric.report_lines(replies, "claude-opus-5"):
        line.encode("ascii")  # revienta con UnicodeEncodeError si se cuela algo


# ── El freno del dinero ────────────────────────────────────────────────────


# 🚨 **Lo que este test guarda es DINERO, no frases. No lo derives.**
#
# 🔓 **`PI-6`: autorizado por el usuario el 2026-08-19.** Razón escrita: `SENTENCES`
# pasa de 60 a 90 por `T-112` (las 30 discriminantes de `[D-101]`), y la corrida
# entera pasa de **$0,2052 a $0,3078** — medidos con `COST_PER_CALL_USD = 0,00342`
# (`[D-096]`), no con el `0,00304` que `measure_tutor.py:84-89` marca como caducado.
#
# 🔑 **Por qué aquí el número va A MANO, justo al revés que en los otros dos tests
# que esta misma autorización tocó.** El corte: *se DERIVA cuando el test afirma una
# RELACIÓN; se escribe A MANO cuando afirma una DECISIÓN.* La forma vieja era
# `MAX_CALLS == len(SENTENCES) == 60`, y su primera mitad **ya es una tautología** —
# `eval_rubric.py:145` dice literalmente `MAX_CALLS = len(SENTENCES)`. O sea que
# **todo lo que este test afirmaba de verdad era el 60**.
#
# ⚠️ **Y ahí estaba la trampa:** aplicarle el criterio de *"que no pueda caducar
# nunca"* y dejarlo en `MAX_CALLS == len(SENTENCES)` lo convierte en `len(SENTENCES)
# == len(SENTENCES)`. **Verde para siempre**, ocupando su sitio en la lista, con la
# alarma de coste muerta y sin que nada lo diga. Es `[L-087]` con otra cara: un test
# que no puede fallar no se distingue de uno que no existe.
def test_a_full_run_costs_what_we_decided_to_pay():
    """🚨 La firma del gasto: cuánto se acepta pagar por una corrida entera.

    El `0.31` es la firma del usuario, del 2026-08-19. No es una medida: es un
    **techo aceptado**, y por eso se escribe y no se calcula.

    🔻 **SALTA POR DOS EJES, y se dice porque solo uno es obvio:**

    1. **Si crece `SENTENCES`.** Hoy son 90 = `$0,3078`. **La frase 91 da `$0,3112`
       y ya no pasa: cero holgura, a propósito.**
    2. **Si `COST_PER_CALL_USD` se vuelve a medir hacia arriba.** Con las mismas 90
       frases, un coste de `$0,00345` da `$0,3105` y tampoco pasa. Ese número **ya
       ha caducado dos veces** por tocar la rúbrica (`[L-059]`,
       `measure_tutor.py:92-95`).

    🚨 **Por eso el `assert` habla de DÓLARES y no de frases.** Quien vea este test
    en rojo mañana no puede "arreglarlo" contando frases: le saltaría igual por el
    otro eje, y peor, **habría cambiado el techo del gasto creyendo que ajustaba un
    inventario**. Si hay que subirlo, se sube diciendo la cifra en voz alta — que es
    exactamente lo que este test hizo hoy.

    📌 **El primer `assert` se queda aunque sea tautológico**, y no por descuido: dice
    que el tope va pegado al plan, y es lo que hace que la cuenta de la segunda línea
    sea la del gasto real. Lo que NO se queda es que sea la única afirmación.
    """
    # El tope va pegado al plan: una llamada por frase, sin holgura donde esconder
    # un bucle roto. `measure_tutor` deja 73 porque su tanda se recorta sola.
    assert eval_rubric.MAX_CALLS == len(eval_rubric.SENTENCES)

    # ── La decisión, a mano: "acepto pagar hasta esto por una corrida entera" ──
    assert eval_rubric.MAX_CALLS * eval_rubric.COST_PER_CALL_USD <= 0.31


def test_the_recording_client_charges_the_budget_before_calling():
    """El monedero se cobra al pasar por el cliente, que es el paso obligado.

    📌 Se hereda de `RecordingClient`, así que lo que se comprueba aquí es que la
    herencia **no perdió el cobro** al añadir la libreta del texto.
    """
    budget = CallBudget(max_calls=2)
    answer = answer_with("OK\nThat is correct.")
    client = eval_rubric.ReplyRecordingClient(FakeClient(answer), budget)

    client.messages.create(model="x")
    assert budget.spent == 1

    client.messages.create(model="x")
    assert budget.spent == 2

    with pytest.raises(Exception):
        client.messages.create(model="x")


# ── Elegir la tanda ────────────────────────────────────────────────────────


def test_no_numbers_means_all_of_them():
    """Sin argumentos entran TODAS, que es la corrida de línea base.

    🔓 **`PI-6`: autorizado por el usuario el 2026-08-19.** Razón escrita:
    `SENTENCES` pasa de 60 a 90 por `T-112` (las 30 frases discriminantes de
    `[D-101]`), y este test clavaba el `60` a mano.

    🔑 **Se DERIVA, y el criterio es de la autorización, no de la comodidad:**
    *se deriva cuando el test afirma una RELACIÓN; se escribe a mano cuando
    afirma una DECISIÓN.* Lo que este test afirma es *"sin argumentos entran
    todas"* — una relación. El `60` nunca fue su contenido: era **su encarnación
    de aquel día**, y por eso caducó al crecer la lista.

    ⚠️ Compárese con `test_a_full_run_costs_what_we_decided_to_pay`, donde el
    número **se queda a mano a propósito**: allí lo que se afirma es cuánto
    dinero se acepta pagar, y eso es una decisión, no una relación.
    """
    plan = eval_rubric.chosen_sentences([])

    assert len(plan) == len(eval_rubric.SENTENCES)
    assert plan[0] == (1, eval_rubric.SENTENCES[0])
    assert plan[-1] == (len(eval_rubric.SENTENCES), eval_rubric.SENTENCES[-1])


def test_numbers_pick_those_sentences_counting_from_one():
    """🔑 Empieza en 1, no en 0, y eso importa más de lo que parece.

    El número que se elige es **el mismo que sale en pantalla**, así que lo que se
    lee en la salida se puede volver a pedir tal cual. Si la línea de comandos
    contara desde 0, cada investigación empezaría restando uno a mano — y ahí es
    donde se mira la frase equivocada sin enterarse.
    """
    plan = eval_rubric.chosen_sentences(["1", "3"])

    assert plan == [
        (1, eval_rubric.SENTENCES[0]),
        (3, eval_rubric.SENTENCES[2]),
    ]


# 🔓 **`PI-6`: autorizado por el usuario el 2026-08-19.** Razón escrita:
# `SENTENCES` pasa de 60 a 90 por `T-112`, y aquí había un `"61"` a mano que
# significaba *"uno más allá del final"*. Con 90 frases, **61 es una frase
# válida**: el caso dejó de probar lo que su nombre dice y el test se puso rojo.
#
# 🔑 **Se DERIVA porque afirma una RELACIÓN**, no una decisión. Y con `"91"` a
# mano volvería a caducar el día que la lista crezca otra vez — **y esta vez ya
# sabemos que crece**. Es la postura que el propio proyecto ya tenía escrita en
# `tests/test_measure_tutor.py:255`: *"Un 60 a mano se quedaria quieto si la tasa
# cambiara"*.
@pytest.mark.parametrize("bad", [
    ["0"],
    [str(len(eval_rubric.SENTENCES) + 1)],
    ["dos"],
    ["-1"],
    ["1.5"],
    [""],
])
def test_a_bad_number_stops_before_calling_anybody(bad):
    """🚨 Se valida ANTES de gastar, y el mensaje lo dice.

    🔑 **Un número fuera de rango con la tanda ya empezada dejaría llamadas pagadas
    y ningún informe.** Por eso `chosen_sentences` corre antes de pedir la llave, y
    por eso el mensaje termina con *"no se ha llamado a nadie"*: quien lo lea tiene
    que saber si esto le costó dinero.
    """
    with pytest.raises(SystemExit) as stopped:
        eval_rubric.chosen_sentences(bad)

    assert "no se ha llamado a nadie" in str(stopped.value)


# ── Guardar las respuestas ─────────────────────────────────────────────────


def test_the_replies_file_hangs_off_the_data_dir_that_is_set_now(tmp_path, monkeypatch):
    """🚨 La ruta se resuelve al LLAMAR, no al importar.

    🔑 **Una constante de módulo se congela cuando se importa**, o sea antes de que
    `monkeypatch` pueda desviar nada — y entonces la corrida escribiría en la
    carpeta de datos de verdad aunque alguien la hubiera movido. Es la condición que
    `[D-085]` dejó escrita para la traza, comprobada aquí igual: **se mueve
    `TEAPP_DATA_DIR` y se exige que el archivo se haya movido con él.**
    """
    monkeypatch.setenv("TEAPP_DATA_DIR", str(tmp_path))

    assert eval_rubric.replies_file().parent == tmp_path


def test_saving_writes_one_json_line_per_reply(tmp_path):
    """Una línea por respuesta, y con la frase dentro.

    🔑 **Sin la frase, la respuesta no se puede juzgar**: *"She goes to school every
    day"* no dice nada si no se sabe qué se preguntó. Ese fue el hueco que costó
    `$0,18` en la primera corrida.
    """
    destination = tmp_path / "eval_replies.jsonl"
    records = [
        {"number": 2, "sentence": "She go to school", "reply": "FIX\nShe goes.",
         "broken": [], "model": "claude-opus-5"},
        {"number": 3, "sentence": "They is my friends", "reply": "FIX\nThey are.",
         "broken": ["too_many_sentences"], "model": "claude-opus-5"},
    ]

    eval_rubric.save_replies(records, path=destination)

    lines = destination.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["sentence"] == "She go to school"
    assert json.loads(lines[1])["broken"] == ["too_many_sentences"]


def test_saving_refuses_to_touch_a_file_that_already_exists(tmp_path):
    """🚨 La segunda corrida NO pisa a la primera: se niega y no escribe nada.

    🔓 **Reemplaza a `test_saving_overwrites_instead_of_appending`, jubilado por la
    autorización `PI-6` del 2026-08-19 (`[D-102]`).** Aquel test no estaba
    equivocado: describía bien el contrato de `"w"`. Lo que cambió es el contrato.

    🔑 **Por qué el modo de apertura y no el nombre.** El nombre puede identificar
    la corrida perfectamente y aun así no salvarla: **la fila que lo confirma se lee
    DESPUÉS del `open`**, o sea después de que el archivo ya esté truncado. Quien
    impide el pisotón es `"x"`.

    ⚠️ **Y comprueba DOS cosas donde el viejo comprobaba una.** No basta con que
    reviente: hay que ver que **lo de antes sigue ahí**. Un `SystemExit` lanzado
    después de haber truncado el archivo pasaría la mitad fácil de este test y
    habría perdido `$0,21` irrepetibles igual.
    """
    destination = tmp_path / "eval_replies.jsonl"
    eval_rubric.save_replies([{"number": 1, "reply": "vieja"}], path=destination)

    with pytest.raises(SystemExit) as stopped:
        eval_rubric.save_replies([{"number": 1, "reply": "nueva"}], path=destination)

    assert "borra el archivo a mano" in str(stopped.value)

    lines = destination.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["reply"] == "vieja", (
        "el archivo original no sobrevivio: se trunco antes de negarse."
    )


def test_the_recording_client_keeps_the_raw_text_of_every_reply():
    """La libreta nueva: el texto crudo, con su primera línea intacta.

    🔑 **La primera línea es el dato entero.** Sin ella no se puede distinguir un
    `FIX` bien puesto de un fallo de formato, que es para lo que existe este eval.
    """
    budget = CallBudget(max_calls=5)
    answer = answer_with("FIX\nShe goes to school every day.")
    client = eval_rubric.ReplyRecordingClient(FakeClient(answer), budget)

    client.messages.create(model="x")

    assert client.replies == ["FIX\nShe goes to school every day."]


def test_the_wallet_is_imported_not_copied():
    """🚨 `COST_PER_CALL_USD` era una COPIA aquí, y la copia es la que gasta.

    El comentario de arriba de los imports dice que el monedero se importa, y el
    monedero no estaba en la lista: `[L-075]` otra vez, el comentario diciendo la
    regla y la línea de debajo incumpliéndola.

    🔑 **Y el daño no era "un duplicado":** el aviso de caducidad de `[D-090]` se
    escribió en `measure_tutor.py`, así que la corrida de 60 —que la lanza ESTE
    guion— iba a imprimir su coste desde la copia sin nota. Ver `[L-077]`.
    """
    assert eval_rubric.COST_PER_CALL_USD is measure_tutor.COST_PER_CALL_USD


# ── La identidad del corpus: los cuatro ejes del nombre ────────────────────


def test_the_rubric_fingerprint_changes_when_the_rubric_changes(monkeypatch):
    """🔑 La huella sirve para algo solo si se mueve cuando se mueve la rúbrica.

    🚨 **Es lo único que distingue una huella de una etiqueta escrita a mano.** Un
    `rubric_version = "2"` también identifica... hasta que alguien edita la rúbrica
    y no lo sube. `GRAMMAR_RUBRIC` ya se movió dos veces así (`[L-059]`, `[D-090]`).
    """
    before = eval_rubric.rubric_fingerprint()

    monkeypatch.setattr(tools, "GRAMMAR_RUBRIC", tools.GRAMMAR_RUBRIC + " one more")

    assert eval_rubric.rubric_fingerprint() != before


def test_the_replies_file_name_carries_model_date_seal_and_sample():
    """Los ejes de `[D-102]`: modelo, fecha, **sello de corrida** y marca de muestreo.

    🔓 **Reemplaza a `test_the_replies_file_name_carries_model_date_rubric_and_sample`,
    jubilado por la autorización `PI-6` del 2026-08-19.** Aquel exigía la huella de
    `GRAMMAR_RUBRIC` en el nombre; `[D-102]` la sustituye por el sello.

    ⚠️ **Y es MÁS FUERTE que el viejo en las dos cosas que importan:** el viejo
    comprobaba **una** huella y con `in` (subcadena); este comprueba **las tres** —
    recalculándolas— y exige que el sello salga **exacto**.
    """
    name = eval_rubric.replies_file(len(eval_rubric.SENTENCES)).name

    assert tools.MODEL_NAME in name
    assert date.today().isoformat() in name
    assert "full" in name

    # El sello no se copia de `run_seal()`: se recompone desde las tres huellas,
    # que es justo lo que hara `replies.name_matches_rows` leyendo una fila.
    pieces = (
        eval_rubric.rubric_fingerprint()
        + eval_rubric.sentences_fingerprint()
        + eval_rubric.detector_fingerprint()
    )
    seal = hashlib.sha256(pieces.encode("utf-8")).hexdigest()[:8]

    assert f"_run-{seal}_" in name

    # 🚨 La huella de rubrica SUELTA ya no manda en el nombre. Sin esto, un nombre
    # que siguiera llevandola pasaria el test de arriba y `[D-102]` estaria a medias.
    assert f"_rubric-{eval_rubric.rubric_fingerprint()}_" not in name


def test_a_partial_run_is_named_pick_not_full():
    """⚠️ Una tanda parcial NO es una línea base, y el nombre tiene que decirlo.

    🚨 **Sin esta marca el archivo miente por omisión:** quien saque un porcentaje
    de una selección de fallos obtiene `100%` y se lo cree. Es `[L-071]`.
    """
    partial = eval_rubric.replies_file(10).name
    whole = eval_rubric.replies_file(len(eval_rubric.SENTENCES)).name

    assert "pick" in partial and "full" not in partial
    assert "full" in whole and "pick" not in whole


def test_two_rubrics_do_not_share_a_file_name(monkeypatch):
    """🔴 El bicho de `T-107`, cazado por donde de verdad dolía: el MISMO día.

    🔑 **La fecha sola no separa estas dos corridas.** La línea base corrió a las
    21:43 UTC y el diagnóstico a las 21:54, mismo día, con la rúbrica cambiada
    entre medias — y con el nombre viejo la segunda borró a la primera (`[L-076]`).
    """
    first = eval_rubric.replies_file()

    monkeypatch.setattr(tools, "GRAMMAR_RUBRIC", tools.GRAMMAR_RUBRIC + " changed")
    second = eval_rubric.replies_file()

    assert first != second


def test_two_sentence_sets_do_not_share_a_file_name(monkeypatch):
    """🚨 Cambiar EL EXAMEN cambia el nombre. El agujero entero de `[D-102]`.

    🔑 **Es el gemelo que faltaba, y el que más falta hacía.** Hasta hoy el conjunto
    de frases no entraba en ningun eje: `T-112` lo cambia a proposito, y la corrida
    discriminante habria salido con **el mismo nombre** que la que sostiene el 58/58
    —mismo modelo, misma huella de rubrica, mismo `full`—.

    ⚠️ **Se cambia una frase por otra, no se anaden frases.** Con una lista mas larga
    el test pasaria por `len(SENTENCES)` sin demostrar nada: lo que hay que ver es que
    el CONTENIDO manda.
    """
    first = eval_rubric.replies_file()

    swapped = list(eval_rubric.SENTENCES)
    swapped[0] = swapped[0] + " changed"
    monkeypatch.setattr(eval_rubric, "SENTENCES", swapped)

    assert eval_rubric.replies_file() != first


def test_two_detectors_do_not_share_a_file_name(monkeypatch, tmp_path):
    """🚨 Cambiar LA BASCULA cambia el nombre. El agujero de `[L-081]` y `T-110`.

    🔑 **`rubric_check.py` decide el campo `broken` de cada fila**, y no entraba en
    ninguna huella. Comprobado el 2026-08-18: 10 filas guardadas como rotas, 1 rota
    con el detector de hoy. **La misma respuesta, dos veredictos segun el dia.**

    ⚠️ Se falsea la FUENTE del modulo, que es lo que `detector_fingerprint()` hashea.
    """
    fake = tmp_path / "rubric_check_falso.py"
    fake.write_text("# otro detector\n", encoding="utf-8")

    first = eval_rubric.replies_file()
    monkeypatch.setattr(rubric_check, "__file__", str(fake))

    assert eval_rubric.replies_file() != first


def test_the_verdict_words_are_inside_the_seal(monkeypatch):
    """🚨 Cambiar `OK`/`FIX` cambia el nombre, aunque el detector no se toque.

    🔑 **El agujero que este test tapa es `~~D-092~~` un piso más abajo.** Aquella
    selló la rúbrica y dio por sellado el EXAMEN; `detector_fingerprint()` sellaba el
    ARCHIVO del detector y daba por sellado el DETECTOR. Pero `VERDICT_CORRECT` y
    `VERDICT_WRONG` viven en `app/tools.py` **después** de que `GRAMMAR_RUBRIC`
    termine: no estaban en la rúbrica, no estaban en la fuente del detector, no
    estaban en nada.

    ⚠️ **Y no son decorativas.** `rubric_check.py:124` y `:214` las usan para separar
    *"el juez rompió el formato"* de *"el alumno se equivocó"* — la distinción de
    `[D-067]`. Con `"FIX"` renombrado, el detector reclasificaría **todo** como
    formato roto y el nombre del archivo no se habría movido.
    """
    before = eval_rubric.replies_file()

    monkeypatch.setattr(tools, "VERDICT_WRONG", "WRONG")

    assert eval_rubric.replies_file() != before


def test_the_sentence_cap_is_inside_the_seal(monkeypatch):
    """🚨 `MAX_SENTENCES` entra por su propia puerta, no de rebote.

    🔑 **Hoy ya estaba cubierto — por COINCIDENCIA, y esa es la razón del test.**
    `rubric_fingerprint()` lo tapa porque `app/tools.py:296` interpola
    `{MAX_SENTENCES}` dentro del texto de la rúbrica. El día que alguien reescriba esa
    frase sin la interpolación, la cobertura **desaparece y nada lo dice**.

    ⚠️ Por eso se comprueba contra `detector_fingerprint()` y no contra el nombre: el
    nombre pasaría igual gracias a la rúbrica, que es justo la dependencia que este
    test existe para no tener.
    """
    before = eval_rubric.detector_fingerprint()

    monkeypatch.setattr(tools, "MAX_SENTENCES", 99)

    assert eval_rubric.detector_fingerprint() != before


# ── La cerradura de PI-8 ───────────────────────────────────────────────────


def test_a_corpus_of_invented_sentences_can_be_promoted():
    """El caso bueno: todo lo que sale de `SENTENCES` pasa la cerradura."""
    records = [{"sentence": eval_rubric.SENTENCES[0]},
               {"sentence": eval_rubric.SENTENCES[3]}]

    assert eval_rubric.sentences_are_invented(records) is True


def test_a_sentence_that_is_not_invented_blocks_promotion():
    """🔒 `PI-8` con cerradura: una frase que no está en `SENTENCES` para la puerta.

    🚨 **La frase de abajo es INVENTADA por mí para este test** —`PI-8` prohíbe
    meter aquí lo que escriba una persona usando la app, también como ejemplo—. Lo
    que se comprueba es la forma: viene de fuera de `SENTENCES`, así que no pasa.

    🔑 **Y éste es el test que convierte la advertencia en artefacto** (`[D-093]`):
    sin él, `PI-8` en este camino sería una frase en un comentario.
    """
    records = [{"sentence": eval_rubric.SENTENCES[0]},
               {"sentence": "yesterday i buyed a red bicycle for my brother"}]

    assert eval_rubric.sentences_are_invented(records) is False


def test_a_row_without_a_sentence_blocks_promotion():
    """⚠️ Un corpus viejo, sin el campo, tampoco pasa: no se puede comprobar.

    🔑 **Denegar por defecto** (regla 3): lo que no se puede verificar se rechaza,
    no se deja pasar por ser antiguo.
    """
    assert eval_rubric.sentences_are_invented([{"reply": "FIX"}]) is False


# ── El portero de _persistence/corpus/ ─────────────────────────────────────
#
# 🚨 **Por qué esto existe y no basta con la cerradura.** `sentences_are_invented`
# comprueba lo que se le pasa; la promoción es un `mv` a mano, así que **invocarla
# era un acto de acordarse** — exactamente lo que `[D-093]` existe para eliminar.
# La cerradura estaba puesta en la puerta y sin echar. Estos dos tests la echan:
# recorren la carpeta de verdad, con `glob` y no con una lista escrita, así que
# corren en cada `pytest` **da igual quién movió el archivo, por qué vía y si se
# acordó**. Es el portero de `[T-071]` sobre `data/`, un piso más abajo.


CORPUS_DIR = Path(__file__).resolve().parent.parent / "_persistence" / "corpus"


def _frozen_corpora() -> list[Path]:
    """Los corpus congelados que hay HOY en la carpeta, buscados, no listados.

    🔑 **Con `glob` y no con una lista escrita a mano**, que es la diferencia entre
    un portero y un saludo: una lista solo vigila lo que alguien se acordó de
    apuntar, y el archivo que se cuela es justo el que nadie apuntó.
    """
    return sorted(CORPUS_DIR.glob("*.jsonl"))


def test_the_corpus_folder_is_not_empty():
    """⚠️ Un portero sobre una carpeta vacía es verde y no prueba nada.

    🔑 **Es `[L-048]` aplicado a los dos tests de abajo:** ambos recorren un `glob`,
    y un `glob` sin resultados los deja pasar en silencio. Si algún día la carpeta
    se vacía a propósito, este test se borra **a mano y con la razón escrita** — que
    es lo que `PI-6` pide, y lo contrario de que se apague solo.
    """
    assert _frozen_corpora(), (
        "No hay corpus en _persistence/corpus/: los dos porteros de abajo estan "
        "pasando en vacio y no vigilan nada."
    )


def test_every_frozen_corpus_passes_the_pi8_lock():
    """🔒 `PI-8` echada de verdad sobre la carpeta, no comprobada a mano al mover.

    🚨 **Este repositorio es público** (`[C-007]`). Un corpus con la frase de una
    persona dentro no puede vivir aquí, y hasta ahora lo único que lo impedía era
    acordarse de llamar a la cerradura antes del `mv`.
    """
    for path in _frozen_corpora():
        rows = [json.loads(line) for line in
                path.read_text(encoding="utf-8").splitlines() if line.strip()]

        assert rows, f"{path.name} esta vacio"
        assert eval_rubric.sentences_are_invented(rows), (
            f"{path.name} tiene alguna frase que NO sale de SENTENCES. "
            "PI-8: aqui no entra lo que escriba una persona usando la app."
        )


def test_no_frozen_corpus_carries_the_live_rubric():
    """🔻 Un corpus congelado con la rúbrica VIVA es una promoción disparada de más.

    🔑 **Qué caza y qué no, dicho claro:** caza una promoción que **sobra** —alguien
    congeló una configuración que sigue en producción—, y **no** caza una que
    falta. Cuesta una línea y cubre la mitad barata. La otra mitad es el disparador
    pegado al commit de `~~D-092~~`, que `[D-102]` NO tocó y que ningún test puede
    comprobar.
    """
    live = eval_rubric.rubric_fingerprint()
    live_seal = eval_rubric.run_seal()

    for path in _frozen_corpora():
        # 🔓 **Autorizacion `PI-6` del 2026-08-19.** Aqui habia `assert live not in
        # path.name`, y `[D-102]` lo habria dejado VERDE Y HUECO: en cuanto el nombre
        # deja de llevar la huella de la rubrica, esa condicion se cumple SIEMPRE,
        # para cualquier archivo. No se ponia rojo — dejaba de mirar. Un rojo llama;
        # un verde hueco tranquiliza y ocupa el sitio de un guardian.
        if "_run-" in path.name:
            assert f"_run-{live_seal}_" not in path.name, (
                f"{path.name} lleva el sello de produccion ({live_seal}): "
                "se congelo una configuracion que todavia es la de produccion."
            )
        else:
            # Generacion legado (`[D-102]` manda no renombrarla): el criterio viejo,
            # que sobre ESTOS nombres si sigue significando algo.
            assert live not in path.name, (
                f"{path.name} lleva la huella de la rubrica VIVA ({live}): "
                "se congelo una configuracion que todavia es la de produccion."
            )

        rows = [json.loads(line) for line in
                path.read_text(encoding="utf-8").splitlines() if line.strip()]

        assert all(row.get("rubric") != live for row in rows), (
            f"{path.name} tiene filas con la huella viva ({live}) dentro."
        )


def test_a_run_that_is_cut_short_is_named_by_what_arrived(tmp_path, monkeypatch, capsys):
    """🚨 Se planearon 60 y llegaron 30: el archivo tiene que llamarse `pick`.

    🔑 **Es el unico test que entra en `main()`, y por eso caza lo que los demas no.**
    `test_a_partial_run_is_named_pick_not_full` prueba `replies_file(10)` — una tanda
    que se PIDIO parcial. El agujero era el otro camino: la tanda se pidio entera y se
    corto sola, y el nombre se calculaba con el plan, no con lo que llego.

    ⚠️ **Y el bicho era mudo.** `report_lines` imprime el AVISO de tanda cortada, asi
    que la corrida se ve honesta en pantalla; lo que mentia era el nombre del archivo,
    que es justo la parte que sobrevive cuando la consola se cierra.

    🚨 **La segunda mitad es peor:** `save_replies` abre en `"w"`, y modelo, fecha y
    huella no cambian dentro del mismo dia. Con el nombre calculado sobre el plan, una
    segunda corrida cortada borraba la linea base pagada de la primera — `[L-076]`.
    """
    monkeypatch.setenv("TEAPP_DATA_DIR", str(tmp_path))
    monkeypatch.setattr(eval_rubric.config, "load_env_file", lambda: None)
    monkeypatch.setattr(eval_rubric.config, "require_anthropic_key", lambda: "sk-de-mentira")
    monkeypatch.setattr(eval_rubric.anthropic, "Anthropic", lambda **kwargs: object())

    arrived = 30

    def cut_short_judge(sentence, client):
        # 🔑 La respuesta se apunta en la libreta del cliente, que es de donde
        # `main` la saca. Inventada (`PI-8`).
        if len(cut_short_judge.seen) >= arrived:
            raise eval_rubric.TutorUnavailableError("cortado a proposito", request_sent=True)
        cut_short_judge.seen.append(sentence)
        client.replies.append("FIX\nTry: She goes to school every day.")

    cut_short_judge.seen = []

    monkeypatch.setattr(eval_rubric, "judge_grammar", cut_short_judge)

    eval_rubric.main([])

    written = list(tmp_path.glob("*.jsonl"))
    assert len(written) == 1, written

    name = written[0].name
    assert "pick" in name and "full" not in name, name

    rows = written[0].read_text(encoding="utf-8").strip().splitlines()
    assert len(rows) == arrived

    # El nombre real, el que hay que mirar, sale tambien impreso al final.
    assert name in capsys.readouterr().out
