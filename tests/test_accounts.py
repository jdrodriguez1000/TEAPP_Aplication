"""Tests del almacén de credenciales.

Lo que aquí se prueba es la mitad A del paso 5: cómo se prueba quién eres la
primera vez. La mitad B —cómo se recuerda después— está en `test_sessions.py`.
"""

import json

import pytest

from app.accounts import (
    MAX_PASSWORD_LENGTH,
    MIN_PASSWORD_LENGTH,
    AccountsFileError,
    UserExistsError,
    WeakPasswordError,
    read_accounts,
    register,
    user_exists,
    verify,
)
from app.tools import InvalidUserError

GOOD_PASSWORD = "una-contrasena-larga"


@pytest.fixture
def accounts_file(tmp_path):
    """Un archivo de cuentas propio para cada test."""
    return tmp_path / "accounts.json"


# ── Registrarse y entrar ──────────────────────────────────────────────────


def test_a_new_account_can_be_verified(accounts_file):
    register("juan", GOOD_PASSWORD, accounts_file)

    assert verify("juan", GOOD_PASSWORD, accounts_file) is True


def test_a_wrong_password_is_rejected(accounts_file):
    register("juan", GOOD_PASSWORD, accounts_file)

    assert verify("juan", "otra-contrasena-larga", accounts_file) is False


def test_someone_who_never_registered_is_rejected(accounts_file):
    # 🔑 Contesta lo MISMO que una contraseña mala, a propósito: distinguirlos
    # dejaría averiguar quién tiene cuenta aquí probando nombres.
    assert verify("nadie", GOOD_PASSWORD, accounts_file) is False


def test_register_returns_the_normalized_name(accounts_file):
    assert register("  JUAN ", GOOD_PASSWORD, accounts_file) == "juan"


def test_the_name_is_the_same_person_however_it_is_written(accounts_file):
    # `  JUAN ` y `juan` tienen que ser la misma cuenta, igual que son el mismo
    # marcador desde [D-014]. Si no, en la nube del paso 7 serían dos personas.
    register("  JUAN ", GOOD_PASSWORD, accounts_file)

    assert verify("juan", GOOD_PASSWORD, accounts_file) is True


# ── 🚨 El freno de [D-020]: una identidad no se reclama ───────────────────


def test_a_name_that_already_exists_cannot_be_registered_again(accounts_file):
    # 🔑 Este es el test que sostiene el paso entero. Sin este freno, verificar
    # la identidad no sirve de nada: cualquiera se registra como `juan` y hereda
    # su marcador — el agujero de [D-013] con un formulario delante.
    register("juan", GOOD_PASSWORD, accounts_file)

    with pytest.raises(UserExistsError):
        register("juan", "otra-contrasena-larga", accounts_file)


def test_the_name_is_taken_however_it_is_written(accounts_file):
    # Sin normalizar antes de comparar, `JUAN` se colaría como cuenta nueva y
    # acabaría en el mismo `juan.json` del marcador. El freno se saltaría solo
    # con la tecla de mayúsculas.
    register("juan", GOOD_PASSWORD, accounts_file)

    with pytest.raises(UserExistsError):
        register("  JUAN  ", "otra-contrasena-larga", accounts_file)


def test_a_failed_takeover_does_not_change_the_password(accounts_file):
    # Que se rechace el registro no basta: hay que comprobar que no tocó nada.
    # Si escribiera antes de mirar, el ataque funcionaría igual y con un error
    # en pantalla que parecería tranquilizador.
    register("juan", GOOD_PASSWORD, accounts_file)

    with pytest.raises(UserExistsError):
        register("juan", "la-del-atacante", accounts_file)

    assert verify("juan", GOOD_PASSWORD, accounts_file) is True
    assert verify("juan", "la-del-atacante", accounts_file) is False


def test_user_exists_only_after_registering(accounts_file):
    assert user_exists("juan", accounts_file) is False

    register("juan", GOOD_PASSWORD, accounts_file)

    assert user_exists("juan", accounts_file) is True


# ── 🚨 La contraseña no se guarda ─────────────────────────────────────────


def test_the_password_is_not_written_to_the_file(accounts_file):
    # 🔑 El test que justifica todo `scrypt`. Si esto falla, quien se lleve el
    # archivo se lleva las contraseñas.
    register("juan", GOOD_PASSWORD, accounts_file)

    assert GOOD_PASSWORD not in accounts_file.read_text(encoding="utf-8")


def test_two_people_with_the_same_password_get_different_hashes(accounts_file):
    # Esto es lo que hace la sal. Sin ella, dos hashes iguales en el archivo
    # anunciarían que esas dos personas comparten contraseña.
    register("juan", GOOD_PASSWORD, accounts_file)
    register("ana", GOOD_PASSWORD, accounts_file)

    saved = json.loads(accounts_file.read_text(encoding="utf-8"))

    assert saved["juan"]["hash"] != saved["ana"]["hash"]
    assert saved["juan"]["salt"] != saved["ana"]["salt"]


# ── Lo que no se acepta ───────────────────────────────────────────────────


@pytest.mark.parametrize("short", ["", "abc", "a" * (MIN_PASSWORD_LENGTH - 1)])
def test_a_short_password_is_rejected(accounts_file, short):
    with pytest.raises(WeakPasswordError):
        register("juan", short, accounts_file)


def test_an_absurdly_long_password_is_rejected(accounts_file):
    # `scrypt` tarda a propósito, así que una contraseña enorme sería una forma
    # barata de tener el servidor ocupado.
    with pytest.raises(WeakPasswordError):
        register("juan", "a" * (MAX_PASSWORD_LENGTH + 1), accounts_file)


def test_an_absurdly_long_password_never_reaches_scrypt(accounts_file):
    # El mismo tope también al entrar, no solo al registrarse: si no, el freno
    # se saltaría llamando a /login en vez de a /register.
    register("juan", GOOD_PASSWORD, accounts_file)

    assert verify("juan", "a" * (MAX_PASSWORD_LENGTH + 1), accounts_file) is False


@pytest.mark.parametrize(
    "bad", ["", "   ", "josé", "juan perez", "con", "../../CLAUDE.md", "a" * 33]
)
def test_a_name_that_cannot_be_a_file_is_rejected(accounts_file, bad):
    # Las reglas del nombre son las mismas de [D-014] y viven en un solo sitio.
    # Aquí solo se comprueba que este camino también pasa por ellas.
    with pytest.raises(InvalidUserError):
        register(bad, GOOD_PASSWORD, accounts_file)


def test_a_rejected_name_creates_no_file(accounts_file):
    with pytest.raises(InvalidUserError):
        register("../fuera", GOOD_PASSWORD, accounts_file)

    assert not accounts_file.exists()


# ── Cuando el archivo está roto ───────────────────────────────────────────
#
# 🔑 **Nunca sobrescribas un dato que no lograste entender**, igual que en
# [D-006] con el marcador. Aquí el daño sería peor: no un marcador, todas las
# cuentas del servidor.


def test_no_accounts_file_means_nobody_registered_yet(accounts_file):
    assert read_accounts(accounts_file) == {}


def test_a_broken_accounts_file_is_reported(accounts_file):
    accounts_file.write_text("{esto no es json", encoding="utf-8")

    with pytest.raises(AccountsFileError):
        read_accounts(accounts_file)


def test_an_accounts_file_that_is_not_an_object_is_reported(accounts_file):
    accounts_file.write_text('["juan", "ana"]', encoding="utf-8")

    with pytest.raises(AccountsFileError):
        read_accounts(accounts_file)


def test_a_broken_accounts_file_is_not_overwritten(accounts_file):
    # Mientras el archivo roto siga entero, las cuentas son recuperables a mano.
    # En cuanto se pise, ya no.
    broken = "{esto no es json"
    accounts_file.write_text(broken, encoding="utf-8")

    with pytest.raises(AccountsFileError):
        register("juan", GOOD_PASSWORD, accounts_file)

    assert accounts_file.read_text(encoding="utf-8") == broken


def test_an_account_without_a_hash_is_reported(accounts_file):
    accounts_file.write_text('{"juan": {"salt": "aabb"}}', encoding="utf-8")

    with pytest.raises(AccountsFileError):
        verify("juan", GOOD_PASSWORD, accounts_file)


# ── No queda basura ───────────────────────────────────────────────────────


def test_registering_leaves_no_temporary_file(accounts_file):
    register("juan", GOOD_PASSWORD, accounts_file)

    assert list(accounts_file.parent.glob("*.tmp")) == []
