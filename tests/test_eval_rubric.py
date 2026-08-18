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

import json
from dataclasses import dataclass

import pytest

import eval_rubric
from app import rubric_check
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


def test_the_budget_is_exactly_the_number_of_sentences():
    """🚨 El tope ajustado al plan, no holgado.

    🔑 **Un bucle roto se caza en la llamada 61, no veintidós después** — y esas
    veintidós ya se habrían pagado. `measure_tutor` deja 82 porque su tanda se
    recorta sola; aquí el plan es fijo, una llamada por frase.
    """
    assert eval_rubric.MAX_CALLS == len(eval_rubric.SENTENCES) == 60


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


def test_no_numbers_means_all_sixty():
    """Sin argumentos entran las 60, que es la corrida de línea base."""
    plan = eval_rubric.chosen_sentences([])

    assert len(plan) == 60
    assert plan[0] == (1, eval_rubric.SENTENCES[0])
    assert plan[-1] == (60, eval_rubric.SENTENCES[59])


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


@pytest.mark.parametrize("bad", [["0"], ["61"], ["dos"], ["-1"], ["1.5"], [""]])
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


def test_saving_overwrites_instead_of_appending(tmp_path):
    """⚠️ Dos corridas no se mezclan, y por eso sobrescribe.

    🔑 **Dos modelos revueltos en un archivo es `[L-071]`**: un montón de datos sin
    la frontera que importa, del que se puede sacar cualquier conclusión. Lo que
    interesa mirar es la última corrida.
    """
    destination = tmp_path / "eval_replies.jsonl"

    eval_rubric.save_replies([{"number": 1, "reply": "vieja"}], path=destination)
    eval_rubric.save_replies([{"number": 1, "reply": "nueva"}], path=destination)

    lines = destination.read_text(encoding="utf-8").splitlines()
    assert len(lines) == 1
    assert json.loads(lines[0])["reply"] == "nueva"


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
