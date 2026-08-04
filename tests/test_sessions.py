"""Tests de la tarjeta firmada.

🔑 **Aquí está el corazón del paso 5.** Que una tarjeta buena funcione lo prueba
un test; que una retocada NO funcione lo prueban los demás, y son los que de
verdad importan. Un control se mide dos veces — ver [L-007] y [L-008].
"""

import time

import pytest

from app import config
from app.sessions import (
    SESSION_MAX_AGE_SECONDS,
    InvalidSessionError,
    issue,
    read,
)


# ── La tarjeta buena funciona ─────────────────────────────────────────────


def test_a_fresh_card_names_its_owner():
    assert read(issue("juan")) == "juan"


def test_the_card_carries_the_normalized_name():
    # La tarjeta lleva `juan`, no `  JUAN `: es la forma única con la que se
    # guarda la cuenta y con la que se nombra el marcador ([D-014]).
    assert read(issue("  JUAN ")) == "juan"


def test_two_people_get_different_cards():
    assert issue("juan") != issue("ana")


# ── 🚨 La tarjeta retocada NO funciona ────────────────────────────────────


def test_a_card_with_a_swapped_name_is_rejected():
    # 🔑 El test que define el paso 5. Este es exactamente el ataque que hoy
    # funciona: escribir el nombre de otro y quedarse con su marcador ([D-013]).
    # Se coge la tarjeta de ana y se le pega la firma de juan.
    juan_signature = issue("juan").split(".")[1]
    ana_payload = issue("ana").split(".")[0]

    with pytest.raises(InvalidSessionError):
        read(f"{ana_payload}.{juan_signature}")


def test_a_card_with_a_tampered_payload_is_rejected():
    payload, signature = issue("juan").split(".")

    with pytest.raises(InvalidSessionError):
        read(f"{payload}x.{signature}")


def test_a_card_with_a_tampered_signature_is_rejected():
    payload, signature = issue("juan").split(".")

    with pytest.raises(InvalidSessionError):
        read(f"{payload}.{signature}x")


def test_a_card_without_a_signature_is_rejected():
    payload = issue("juan").split(".")[0]

    with pytest.raises(InvalidSessionError):
        read(payload)


def test_a_handmade_card_is_rejected():
    # Alguien que entienda el formato pero no tenga la llave. Sin firma válida,
    # saber cómo está hecha la tarjeta no sirve de nada: eso es lo que compra
    # el HMAC.
    import base64

    payload = base64.urlsafe_b64encode(b"juan|99999999999").rstrip(b"=").decode()

    with pytest.raises(InvalidSessionError):
        read(f"{payload}.firmafalsa")


@pytest.mark.parametrize("nonsense", [None, "", ".", "x", "no-tiene-punto"])
def test_nonsense_is_rejected(nonsense):
    with pytest.raises(InvalidSessionError):
        read(nonsense)


def test_a_card_signed_with_another_key_is_rejected(monkeypatch):
    # 🔑 Esto es lo que hace que la llave importe. Y es la otra cara de [A-008]:
    # cambiar la llave tira fuera a todo el mundo, precisamente porque las
    # tarjetas viejas dejan de valer.
    token = issue("juan")

    monkeypatch.setenv(config.SECRET_KEY_NAME, "otra-llave-distinta")

    with pytest.raises(InvalidSessionError):
        read(token)


# ── La tarjeta caduca ─────────────────────────────────────────────────────


def test_a_card_is_still_good_just_before_it_expires():
    now = time.time()

    assert read(issue("juan", now=now), now=now + SESSION_MAX_AGE_SECONDS - 1) == "juan"


def test_an_expired_card_is_rejected():
    # Sin caducidad, una tarjeta copiada valdría para siempre.
    now = time.time()

    with pytest.raises(InvalidSessionError):
        read(issue("juan", now=now), now=now + SESSION_MAX_AGE_SECONDS + 1)


# ── Sin llave no se firma nada ────────────────────────────────────────────


def test_without_a_key_no_card_can_be_issued(monkeypatch):
    # 🔑 El servidor se niega en vez de inventarse una llave al vuelo. Inventarla
    # haría que arrancara siempre, y que cada reinicio estrenara llave tirando
    # fuera a todo el mundo sin decir por qué.
    monkeypatch.delenv(config.SECRET_KEY_NAME, raising=False)

    with pytest.raises(config.MissingSecretError):
        issue("juan")


def test_the_missing_key_error_says_what_to_do(monkeypatch):
    monkeypatch.delenv(config.SECRET_KEY_NAME, raising=False)

    with pytest.raises(config.MissingSecretError) as error:
        issue("juan")

    assert ".env" in str(error.value)


@pytest.mark.parametrize("empty", ["", "   "])
def test_an_empty_key_counts_as_no_key(monkeypatch, empty):
    # Una variable puesta pero vacía es el error de configuración más fácil de
    # cometer, y el que peor se ve: `os.environ.get` la daría por buena.
    monkeypatch.setenv(config.SECRET_KEY_NAME, empty)

    with pytest.raises(config.MissingSecretError):
        issue("juan")
