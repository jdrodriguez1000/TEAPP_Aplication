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

from measure_tutor import (
    BUDGET_PER_RUN_USD,
    COST_PER_CALL_USD,
    MAX_CALLS_PER_RUN,
    CallBudget,
    CallBudgetExceeded,
    RecordingClient,
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
