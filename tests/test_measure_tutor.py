"""El corte duro de la báscula: que se le vea morder.

🚨 **Por qué existe este archivo.** `measure_tutor.py` es el único sitio del
proyecto que llama a Claude fuera de la app, y desde `[D-059]` lleva el freno
que protege el saldo compartido de `[C-008]`. Hasta hoy ese freno era un número
suelto sin nadie mirándolo: un `MAX_CALLS = 10` que en realidad hacía cumplir un
recorte de lista, no un contador.

🔑 **Un freno que no has visto morder es una nota, no un freno.** Estos tests se
vieron en ROJO a propósito antes de darlos por buenos —saboteando el contador—,
como se hizo con el `refund` en `T-076`.

⚠️ Aquí no se llama a Anthropic ni una vez: el cliente de dentro es de mentira y
el portero de `no_network.py` vigila que siga siendo así.
"""

import pytest

from app import tools
from measure_tutor import (
    ACCEPTED_CUT_RATE,
    BUDGET_PER_RUN_USD,
    COST_PER_CALL_USD,
    CUT_THRESHOLD_SECONDS,
    MAX_CALLS_PER_RUN,
    ROUTE_THRESHOLD_SECONDS,
    SENTENCES,
    TARGET_SAMPLES,
    CallBudget,
    CallBudgetExceeded,
    RecordingClient,
    verdict_for,
)


class FakeInnerClient:
    """Un cliente de Anthropic de mentira que apunta cuántas veces lo llamaron.

    Sustituye a `anthropic.Anthropic`, no a `RecordingClient`: lo que se prueba
    es el envoltorio de verdad, con el freno dentro.
    """

    def __init__(self):
        self.calls = 0

    @property
    def messages(self):
        return self

    def create(self, **kwargs):
        self.calls += 1
        return _FakeAnswer()


class _FakeAnswer:
    """Lo mínimo que `RecordingClient` mira de una respuesta: su `usage`."""

    usage = "usage-de-mentira"


# --- El tope sale del dinero ------------------------------------------------


def test_the_cap_is_derived_from_the_budget_not_from_a_remembered_number():
    """El tope es una división, no una cifra escrita a mano.

    🔑 Este test parece tonto y no lo es. El fallo que arregla `[D-060]` fue
    exactamente escribir a mano un número que venía de otra pregunta. Si alguien
    vuelve a poner una constante suelta, esto se pone rojo.
    """
    assert MAX_CALLS_PER_RUN == int(BUDGET_PER_RUN_USD / COST_PER_CALL_USD)


def test_the_budget_is_the_one_that_was_decided():
    """$0,25 por tanda — decidido en `[D-060]`, no elegido aquí."""
    assert BUDGET_PER_RUN_USD == 0.25


def test_the_cap_still_lets_the_whole_run_through():
    """El monedero tiene que dejar pasar la tanda entera que el criterio exige.

    🚨 Los dos topes salen de sitios distintos y nadie los cruzaba:
    `MAX_CALLS_PER_RUN` viene del DINERO y `TARGET_SAMPLES` viene de la REGLA
    DE TRES. Si el coste por llamada sube lo suficiente, el monedero corta la
    tanda antes de las 60 muestras — y entonces `verdict_for` devuelve
    `SIN VEREDICTO` después de haber gastado, que es la peor forma de fallar:
    se paga y no se concluye.

    🔑 El acantilado está en $0,00416 por llamada (`int(0,25 / x) >= 60`). Hoy
    con $0,00304 caben 82, veintidós de sobra. Este test es lo que convierte
    ese margen en algo que muerde en vez de un número en un comentario.
    """
    assert MAX_CALLS_PER_RUN >= TARGET_SAMPLES


# --- El monedero cuenta y corta ---------------------------------------------


def test_the_budget_allows_exactly_what_it_promises():
    """Hasta el tope se puede gastar. Ni una menos: cortar antes también es un
    fallo, y de los que salen como un rojo falso a mitad de una medición."""
    budget = CallBudget(max_calls=3)

    budget.spend()
    budget.spend()
    budget.spend()

    assert budget.spent == 3


def test_the_call_past_the_cap_is_refused():
    """La llamada que rebasa el tope revienta."""
    budget = CallBudget(max_calls=3)
    for _ in range(3):
        budget.spend()

    with pytest.raises(CallBudgetExceeded):
        budget.spend()


def test_a_refused_call_does_not_count_as_spent():
    """Un intento rechazado no sube el contador.

    Si subiera, un guion que insistiera dejaría un `spent` mayor que el tope y
    el resumen final mentiría sobre lo gastado.
    """
    budget = CallBudget(max_calls=1)
    budget.spend()

    with pytest.raises(CallBudgetExceeded):
        budget.spend()

    assert budget.spent == 1


# --- El freno está en el paso obligado --------------------------------------


def test_the_budget_is_charged_before_the_real_call_happens():
    """🚨 El freno impide el gasto, no lo denuncia después.

    Con el monedero agotado, el cliente de dentro **no se toca**. Si se cobrara
    después de llamar, esta llamada ya se habría hecho y ya se habría pagado.
    """
    inner = FakeInnerClient()
    budget = CallBudget(max_calls=1)
    client = RecordingClient(inner, budget)

    client.messages.create(model="da-igual")
    assert inner.calls == 1

    with pytest.raises(CallBudgetExceeded):
        client.messages.create(model="da-igual")

    assert inner.calls == 1, "la llamada rechazada llego al cliente de verdad"


def test_the_counter_is_shared_across_new_clients():
    """🔑 **El fallo que este test existe para cazar.**

    `main()` construye un `RecordingClient` NUEVO en cada vuelta del bucle. Un
    contador que viviera dentro del cliente se pondría a cero en cada frase y no
    frenaría nada — y no se notaría, porque el guion seguiría funcionando.
    """
    inner = FakeInnerClient()
    budget = CallBudget(max_calls=2)

    RecordingClient(inner, budget).messages.create(model="da-igual")
    RecordingClient(inner, budget).messages.create(model="da-igual")

    with pytest.raises(CallBudgetExceeded):
        RecordingClient(inner, budget).messages.create(model="da-igual")

    assert inner.calls == 2


def test_the_recorded_usage_still_works_with_the_brake_in_place():
    """El freno no se llevó por delante lo que la báscula venía a hacer.

    `RecordingClient` existe para apuntar `usage`. Un freno que rompiera eso
    dejaría la medición inútil sin dar ningún error.
    """
    inner = FakeInnerClient()
    client = RecordingClient(inner, CallBudget(max_calls=5))

    client.messages.create(model="da-igual")

    assert client.usages == ["usage-de-mentira"]


# --- El criterio de T-093: los umbrales salen del codigo --------------------
#
# 🚨 **Por que existe esta seccion.** El criterio se escribio como funcion justo
# para poder auditarlo sin gastar — y aun asi se le colaron tres defectos que
# nadie vio, porque no habia un solo test mirandolo. Una funcion sin test es un
# parrafo con parentesis.


def test_the_cut_threshold_is_read_from_production_not_copied():
    """El umbral de corte es el `read` de verdad, no un 6,5 escrito a mano.

    Si el reparto de fases cambia, la tanda tiene que contar contra el nuevo sin
    que nadie se acuerde de venir aqui.
    """
    assert CUT_THRESHOLD_SECONDS == tools.TIMEOUT.read


def test_the_route_threshold_is_the_whole_client_budget():
    """🔑 **El defecto que este test existe para cazar.**

    Aqui vivio un `9.5` literal, POR ENCIMA del techo del cliente (9,0). El
    umbral no es "la ruta menos un margen a ojo": es el maximo que podria caber
    en `read` aunque las otras tres fases se dejaran en cero, o sea el cliente
    entero. Un literal se queda quieto cuando el presupuesto cambia.
    """
    assert ROUTE_THRESHOLD_SECONDS == tools.TIMEOUT_SECONDS


def test_the_route_threshold_is_reachable_by_some_phase_split():
    """Un umbral por encima del cliente marca como AMBAR lo que es ROJO.

    AMBAR promete "reequilibrar las fases". Si el umbral estuviera por encima de
    lo que las fases pueden sumar, esa promesa seria imposible de cumplir.
    """
    assert ROUTE_THRESHOLD_SECONDS <= tools.TIMEOUT_SECONDS


def test_a_call_that_no_phase_split_can_save_is_red():
    """🚨 **El caso de 9,2 s, que con el criterio viejo salia AMBAR.**

    9,2 s pasa del corte (6,5) y pasa del cliente entero (9,0). Ningun reparto
    lo salva: read no llega a 9,2 ni vaciando connect, write y pool. Es ROJO.
    """
    elapsed = 9.2
    assert elapsed > CUT_THRESHOLD_SECONDS
    assert elapsed > ROUTE_THRESHOLD_SECONDS

    over_cut = 1
    over_route = 1
    assert verdict_for(over_cut, over_route, TARGET_SAMPLES).startswith("ROJO")


# --- El criterio de T-093: lo que cada veredicto AFIRMA ---------------------


def test_the_sample_target_is_derived_from_the_accepted_rate():
    """Las 60 muestras son una division, no un numero redondo.

    `3/n <= tasa aceptada` es lo unico que permite afirmar la tasa con cero
    cortes. Un `60` a mano se quedaria quieto si la tasa cambiara.
    """
    assert 3 / TARGET_SAMPLES <= ACCEPTED_CUT_RATE
    assert 3 / (TARGET_SAMPLES - 1) > ACCEPTED_CUT_RATE


def test_there_are_enough_sentences_for_the_target():
    """Sesenta frases DISTINTAS: repetirlas mediria la cache, no el modelo."""
    assert len(SENTENCES) >= TARGET_SAMPLES
    assert len(set(SENTENCES)) == len(SENTENCES)


def test_a_short_run_gets_no_verdict_at_all():
    """🚨 **El defecto que este test existe para cazar.**

    Con 45 muestras el guion imprimia un aviso y **a continuacion el veredicto
    igual**, diciendo "por debajo de 6.7%, que es el 5% acordado". 6,7 no es 5.
    Y la tanda corta es alcanzable de verdad: los dos `except` del bucle hacen
    `break`. Un aviso se salta; un veredicto que no sale, no.
    """
    veredicto = verdict_for(0, 0, TARGET_SAMPLES - 15)

    assert veredicto.startswith("SIN VEREDICTO")
    assert "VERDE" not in veredicto


def test_a_short_run_with_no_samples_does_not_divide_by_zero():
    """La regla de tres con cero muestras no se calcula, se calla."""
    assert verdict_for(0, 0, 0).startswith("SIN VEREDICTO")


def test_green_only_claims_what_the_rule_of_three_allows():
    """VERDE afirma la tasa, y solo con la N entera y cero cortes."""
    veredicto = verdict_for(0, 0, TARGET_SAMPLES)

    assert veredicto.startswith("VERDE")
    assert "5.0%" in veredicto


def test_amber_does_not_claim_the_rate_is_above_the_accepted_one():
    """🚨 **El defecto que este test existe para cazar.**

    Con 1 corte de 60 el texto viejo decia "1.7%, por encima del 5% acordado".
    1,7 no esta por encima de 5. Lo cierto es mas flojo: con algun corte ya no
    se puede AFIRMAR que la tasa quede por debajo del 5% — que es distinto de
    afirmar que lo supera.
    """
    veredicto = verdict_for(1, 0, TARGET_SAMPLES)

    assert veredicto.startswith("AMBAR")
    assert "por encima del 5%" not in veredicto
    assert "AFIRMAR" in veredicto


def test_red_wins_over_amber_when_both_conditions_hold():
    """Una llamada que pasa del cliente entero manda, aunque haya cortes."""
    assert verdict_for(3, 1, TARGET_SAMPLES).startswith("ROJO")
