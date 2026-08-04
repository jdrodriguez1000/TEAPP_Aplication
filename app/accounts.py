"""Quién existe y cómo se comprueba que es quien dice.

🔑 **Este archivo es la ÚNICA autoridad sobre quién existe.** `data/users/` no lo
es, aunque hoy se le parezca: ahí solo hay marcadores, y un marcador nace al
practicar. Preguntarle a esa carpeta *"¿quién existe?"* sería preguntárselo a un
sitio que cualquiera puede llenar. Ver [D-020].

> La lista de quién existe y la lista de quién tiene puntos no son la misma
> lista. `data/users/` es un DERIVADO: un marcador solo nace cuando la credencial
> ya existía.

🚨 **La contraseña no se guarda.** Se guarda un *hash*: un cifrado de ida, que
sirve para comprobar y no para desandar. Si alguien se lleva este archivo, no se
lleva las contraseñas.

⚠️ **Y va en un archivo APARTE del marcador, a propósito.** `add_point` reescribe
`data/users/<nombre>.json` entero cada vez que alguien suma un punto. Si el hash
viviera ahí, cada punto reescribiría una credencial, y un fallo del marcador se
convertiría en un fallo que borra contraseñas. **Dos cosas con vidas distintas no
comparten archivo.**
"""

import hashlib
import hmac
import json
import os
import secrets
import tempfile
import threading
from pathlib import Path

from app.tools import PROJECT_ROOT, InvalidUserError, normalize_user

# Dónde viven las credenciales. Un solo archivo para todas, y no uno por
# persona: la pregunta que se le hace es "¿quién existe?", y esa se contesta de
# una vez leyendo un archivo, no listando una carpeta.
#
# `data/` está en `.gitignore`, así que ningún hash llega nunca a Git.
ACCOUNTS_FILE = PROJECT_ROOT / "data" / "accounts.json"

# ── Los números de scrypt ─────────────────────────────────────────────────
#
# 🔑 **Un hash de contraseña es LENTO a propósito**, y ahí está toda la
# protección. `sha256` calcula millones por segundo: quien se lleve el archivo
# prueba el diccionario entero en un rato. `scrypt` está diseñado para tardar y
# para gastar memoria, así que probar en masa deja de salir a cuenta.
#
# ⚠️ Por eso NO se usa `sha256` aquí, aunque sea el hash que todo el mundo
# conoce. Su virtud —la velocidad— es justo el defecto en este trabajo.
SCRYPT_N = 2**14  # cuántas vueltas: subirlo lo hace más lento y más caro de romper
SCRYPT_R = 8  # cuánta memoria gasta cada vuelta
SCRYPT_P = 1  # cuántas se pueden hacer en paralelo
SCRYPT_KEY_LENGTH = 32
SALT_BYTES = 16

# Una contraseña de tres letras no protege nada. El mínimo va aquí y no en la
# pantalla: lo que corre en el navegador se puede saltar (mismo criterio que
# [D-014] con el nombre).
MIN_PASSWORD_LENGTH = 8

# Y un máximo, que no es cosmético: `scrypt` tarda a propósito, así que una
# contraseña de diez megas sería una forma barata de tener el servidor ocupado.
MAX_PASSWORD_LENGTH = 128

# El candado del archivo de credenciales. Misma razón que `_SCORE_LOCK` en
# `tools.py`: dos registros a la vez leerían el mismo archivo, y el segundo en
# escribir borraría al primero. Y aquí es peor que con el marcador — no se
# perdería un punto, se perdería una cuenta entera.
_ACCOUNTS_LOCK = threading.Lock()


class UserExistsError(Exception):
    """Ese nombre ya tiene dueño.

    🚨 Es el freno de [D-020]: sin él, cualquiera se registra con un nombre que
    ya existía y hereda su marcador. Verificar la identidad no sirve de nada si
    la identidad se puede reclamar.
    """

    # Los mensajes van sin tildes a proposito (ver [L-001]).


class WeakPasswordError(Exception):
    """La contraseña no cumple el mínimo."""


class AccountsFileError(Exception):
    """El archivo de credenciales existe pero no se puede entender.

    Hermana de `ScoreFileError`, y por la misma razón de [D-006]: **nunca
    sobrescribas un dato que no lograste entender.** Si el archivo está roto,
    quien administre el servidor todavía puede abrirlo y rescatar las cuentas a
    mano; si lo pisamos con uno nuevo, ya no.
    """


def _hash_password(password: str, salt: bytes) -> bytes:
    """Convierte una contraseña en algo que se puede guardar sin miedo."""
    return hashlib.scrypt(
        password.encode("utf-8"),
        salt=salt,
        n=SCRYPT_N,
        r=SCRYPT_R,
        p=SCRYPT_P,
        dklen=SCRYPT_KEY_LENGTH,
    )


def _check_password_rules(password: str) -> None:
    """Comprueba que la contraseña sirva. Solo largo: ni mayúsculas ni símbolos.

    🔑 Exigir "una mayúscula, un número y un símbolo" empuja a `Password1!`, que
    es de las primeras que prueba cualquiera. El largo es lo que de verdad
    encarece adivinarla.

    :raises WeakPasswordError: si es demasiado corta o demasiado larga.
    """
    if not isinstance(password, str):
        raise WeakPasswordError(
            f"La contrasena tiene que ser texto y llego "
            f"{type(password).__name__}."
        )

    if len(password) < MIN_PASSWORD_LENGTH:
        raise WeakPasswordError(
            f"La contrasena necesita al menos {MIN_PASSWORD_LENGTH} caracteres."
        )

    if len(password) > MAX_PASSWORD_LENGTH:
        raise WeakPasswordError(
            f"La contrasena no puede pasar de {MAX_PASSWORD_LENGTH} caracteres."
        )


def _resolve(path: Path | None) -> Path:
    """Decide qué archivo de cuentas se usa.

    🔑 **El valor por defecto se mira aquí dentro, no en la firma.** Escrito como
    `path: Path = ACCOUNTS_FILE`, Python se queda con la ruta el día que lee el
    `def` y ya no la vuelve a mirar: un test que desviara `ACCOUNTS_FILE` a una
    carpeta temporal seguiría escribiendo en las cuentas de verdad. Mirándolo
    aquí, la ruta se decide en cada llamada y el desvío funciona.
    """
    return ACCOUNTS_FILE if path is None else path


def read_accounts(path: Path | None = None) -> dict:
    """Lee todas las cuentas. Si el archivo no existe, no hay ninguna.

    🔑 **Ausente y roto no son lo mismo**, igual que en `read_score`. Sin archivo
    es el primer día y no hay cuentas. Con el archivo ilegible se avisa: devolver
    un diccionario vacío en silencio diría "aquí no hay nadie" — y el siguiente
    registro pisaría todas las cuentas de verdad con una sola.

    :raises AccountsFileError: si el archivo existe y no se puede interpretar.
    """
    path = _resolve(path)

    if not path.exists():
        return {}

    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise AccountsFileError(
            f"El archivo de cuentas {path} no es un JSON valido ({error}). "
            "No se ha tocado: revisalo antes de seguir."
        ) from error

    if not isinstance(saved, dict):
        raise AccountsFileError(
            f"El archivo de cuentas {path} no guarda un objeto JSON. "
            "No se ha tocado: revisalo antes de seguir."
        )

    return saved


def user_exists(name: str, path: Path | None = None) -> bool:
    """Dice si ese nombre ya tiene credencial.

    :raises InvalidUserError: si el nombre no puede nombrar a nadie.
    :raises AccountsFileError: si el archivo existe y no se puede interpretar.
    """
    return normalize_user(name) in read_accounts(path)


def _write_accounts(accounts: dict, path: Path) -> None:
    """Guarda las cuentas de forma atómica: al lado y renombrando encima.

    Mismo patrón que `add_point` y por la misma razón de [D-007]: escribir
    directamente hace dos cosas seguidas —vaciar y llenar— y un corte entre ambas
    deja el archivo partido. Aquí eso serían **todas** las cuentas del servidor.

    El código se repite en vez de compartirse con `tools.py` a propósito (PI-3):
    `add_point` funciona, y sacarle una función común sería refactorizar código
    que nadie pidió tocar, con el marcador de por medio.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    # `dir=path.parent` es obligatorio: renombrar solo es atomico dentro del
    # mismo disco. Cruzando de disco pasa a ser copiar y borrar.
    handle, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f"{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)

    try:
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            file.write(json.dumps(accounts, indent=2))

        # `os.replace` pisa el destino y se comporta igual en Windows y Linux.
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def register(name: str, password: str, path: Path | None = None) -> str:
    """Crea una cuenta nueva y devuelve el nombre ya normalizado.

    🚨 **Se niega si el nombre ya existe.** Es el freno de [D-020]: sin él, esto
    sería el agujero de [D-013] con un formulario delante.

    🔑 **La lectura y la escritura van juntas dentro del candado.** Si el candado
    abarcara solo la escritura, dos registros a la vez con el mismo nombre leerían
    los dos "no existe" y los dos escribirían: la segunda cuenta pisaría a la
    primera, que es exactamente lo que este freno viene a impedir. Mismo
    razonamiento que [D-009] con el marcador.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises WeakPasswordError: si la contraseña no cumple el mínimo.
    :raises UserExistsError: si ese nombre ya tiene credencial.
    :raises AccountsFileError: si el archivo existe y no se puede interpretar.
    """
    user = normalize_user(name)
    _check_password_rules(password)
    path = _resolve(path)

    with _ACCOUNTS_LOCK:
        accounts = read_accounts(path)

        if user in accounts:
            raise UserExistsError(
                f"El nombre {user!r} ya esta cogido. Elige otro."
            )

        # 🔑 Una sal distinta por persona. Sin ella, dos personas con la misma
        # contrasena tendrian el mismo hash — y quien mirase el archivo lo veria
        # de un vistazo. Ademas obliga a atacar cada cuenta por separado en vez
        # de todas a la vez.
        salt = secrets.token_bytes(SALT_BYTES)

        accounts[user] = {
            "salt": salt.hex(),
            "hash": _hash_password(password, salt).hex(),
        }

        _write_accounts(accounts, path)

    return user


def verify(name: str, password: str, path: Path | None = None) -> bool:
    """Dice si esa contraseña es la de esa persona.

    Devuelve `False` tanto si la contraseña no es esa como si la persona no
    existe. 🔑 **Los dos casos contestan lo mismo a propósito:** distinguirlos
    dejaría averiguar quién tiene cuenta aquí probando nombres, y eso ya es media
    respuesta para quien luego vaya a por la contraseña.

    :raises InvalidUserError: si el nombre no puede nombrar a nadie.
    :raises AccountsFileError: si el archivo existe y no se puede interpretar.
    """
    user = normalize_user(name)
    account = read_accounts(path).get(user)

    if account is None:
        return False

    if not isinstance(account, dict) or "salt" not in account or "hash" not in account:
        raise AccountsFileError(
            f"La cuenta {user!r} no tiene 'salt' y 'hash'. "
            "El archivo de cuentas esta a medias: revisalo antes de seguir."
        )

    try:
        salt = bytes.fromhex(account["salt"])
        expected = bytes.fromhex(account["hash"])
    except (TypeError, ValueError) as error:
        raise AccountsFileError(
            f"La cuenta {user!r} guarda un 'salt' o un 'hash' ilegible."
        ) from error

    # Una contrasena absurdamente larga se rechaza sin llegar a `scrypt`: es la
    # misma proteccion del maximo, aplicada tambien al entrar y no solo al
    # registrarse.
    if not isinstance(password, str) or len(password) > MAX_PASSWORD_LENGTH:
        return False

    # 🚨 `compare_digest` y no `==`. Comparar con `==` corta en cuanto encuentra
    # la primera diferencia, asi que tarda un poquito mas cuantas mas letras
    # acierta. Ese tiempo se puede medir desde fuera y adivinar el hash letra a
    # letra. `compare_digest` siempre tarda lo mismo.
    return hmac.compare_digest(_hash_password(password, salt), expected)
