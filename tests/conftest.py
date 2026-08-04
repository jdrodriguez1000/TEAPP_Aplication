"""Lo que toda la suite necesita antes de probar nada del paso 5.

Dos peligros, y los dos se atajan aquí:

1. 🚨 **Los tests no deben escribir en las cuentas de verdad.** Sin este
   desvío, `test_register_creates_the_account` crearía cuentas en
   `data/accounts.json`, que es el archivo real del servidor.
2. **Sin llave de firma no se puede firmar nada.** El servidor se niega a
   inventarla, y hace bien (ver `app/config.py`). Aquí se pone una de mentira.
"""

import pytest

import no_network
from app import accounts, config, quota

# Una llave cualquiera, solo para los tests. Que esté escrita en el código no
# contradice la regla 7 del proyecto: la regla habla de la llave DE VERDAD, y
# esta no abre nada. La de verdad vive en `.env`, que no va a Git.
TEST_SECRET = "una-llave-de-mentira-solo-para-los-tests"


@pytest.fixture(autouse=True)
def isolated_environment(monkeypatch, tmp_path):
    """Llave de firma puesta y cuentas desviadas a una carpeta temporal.

    `autouse=True` para que valga en TODOS los tests sin que ninguno tenga que
    acordarse. 🔑 Un aislamiento que hay que pedir es un aislamiento que algún
    día se olvida, y el día que se olvide escribirá en los datos reales.

    `monkeypatch` deshace los dos cambios al acabar cada test, y `tmp_path` da
    una carpeta nueva cada vez: ningún test hereda las cuentas del anterior.
    """
    monkeypatch.setenv(config.SECRET_KEY_NAME, TEST_SECRET)

    # Sin `Secure`, porque `TestClient` habla por `http://` y el navegador de
    # mentira que lleva dentro se comporta como el de verdad: descartaria la
    # cookie y todos los tests de sesion fallarian sin decir por que.
    monkeypatch.setenv(config.COOKIE_SECURE_NAME, "false")

    monkeypatch.setattr(accounts, "ACCOUNTS_FILE", tmp_path / "accounts.json")

    # 🚨 Y la cuota igual: sin este desvio, cada test que llame a `/practice`
    # gastaria cuota de verdad en `data/quota/`. Correr la suite dos veces
    # dejaria a alguien sin poder practicar, y el culpable seria pytest.
    #
    # ⚠️ Esto solo funciona porque `quota.py` resuelve la carpeta DENTRO de cada
    # funcion. Con la carpeta puesta como valor por defecto en la firma, Python
    # la habria congelado al importar y este `setattr` no cambiaria nada.
    monkeypatch.setattr(quota, "QUOTA_DIR", tmp_path / "quota")


@pytest.fixture(autouse=True)
def no_network_allowed(monkeypatch):
    """Nadie sale a internet durante los tests — restriccion `C-001`.

    `autouse=True` por la misma razon que el de arriba: una vigilancia que hay
    que pedir no vigila nada el dia que a alguien se le olvide pedirla.

    Hoy no frena a nadie: ningun test intenta salir. Ese es justo el punto — no
    esta aqui por lo que pasa hoy, sino para que el dia que alguien meta una
    llamada de verdad a la API, la suite se ponga roja **en ese momento** y no
    tres meses despues.

    ⚠️ No ve los subprocesos (`node`, `git`): el porque esta en `no_network.py`.
    """
    no_network.install(monkeypatch)
