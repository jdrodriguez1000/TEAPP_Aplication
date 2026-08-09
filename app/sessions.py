"""La tarjeta que el servidor reparte y luego reconoce.

🔑 **La diferencia entera del paso 5 está aquí.** Antes el navegador DECÍA quién
era —`{"user": "juan"}` en el cuerpo— y el servidor se lo creía. Ahora el
servidor entrega una tarjeta **firmada por él**, y en cada petición lee la firma.
Quien no tenga tarjeta no es nadie, y una tarjeta retocada deja de valer.

> Antes se preguntaba el nombre. Ahora se reparten credenciales.

La tarjeta lleva el nombre a la vista: **no está cifrada, está firmada**, y son
cosas distintas. Cualquiera puede LEER de quién es —no hay nada secreto ahí
dentro—, pero nadie puede FABRICAR una nueva sin la llave, que vive en el
servidor y no sale de ahí.

⚠️ **Sin la llave no hay firma posible.** Si `TEAPP_SECRET_KEY` cambia, todas las
tarjetas repartidas dejan de valer de golpe y todo el mundo queda fuera. No es un
fallo: es cómo funciona una firma. Anotado en `[L-032]` (antes `[A-008]`).
"""

import base64
import hmac
import time

from app.config import require_secret
from app.tools import InvalidUserError, normalize_user

# Cómo se llama la cookie en el navegador.
SESSION_COOKIE = "teapp_session"

# Cuánto vale una sesión. Una semana: suficiente para no pedir la contraseña
# cada día, y poco para que una tarjeta robada no sirva para siempre.
SESSION_MAX_AGE_SECONDS = 7 * 24 * 60 * 60

# Lo que separa el contenido de su firma dentro de la cookie. Un punto, que no
# aparece ni en un nombre válido ni en base64url.
SEPARATOR = "."


class InvalidSessionError(Exception):
    """La tarjeta no vale: retocada, caducada, mal formada o inexistente.

    🔑 **Un solo error para todos los casos, a propósito.** Decir "la firma no
    cuadra" o "caducó hace dos días" le daría a quien esté probando justo la
    pista que necesita. Aquí solo se contesta que no vale.
    """

    # Los mensajes van sin tildes a proposito (ver [L-001]).


def _encode(raw: bytes) -> str:
    """Pasa bytes a texto que se pueda meter en una cookie sin romperla."""
    # base64 **url-safe** y sin el relleno `=`: una cookie no admite cualquier
    # caracter, y el `/` y el `+` del base64 normal dan problemas.
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def _decode(text: str) -> bytes:
    """Deshace `_encode`. El relleno que se quitó se vuelve a poner aquí."""
    padding = "=" * (-len(text) % 4)
    return base64.urlsafe_b64decode(text + padding)


def _sign(payload: str) -> str:
    """Firma el contenido con la llave del servidor."""
    signature = hmac.new(
        require_secret(), payload.encode("ascii"), digestmod="sha256"
    ).digest()
    return _encode(signature)


def issue(user: str, now: float | None = None) -> str:
    """Fabrica la tarjeta de una persona.

    El `now` es un parámetro para que los tests puedan situarse en el futuro y
    comprobar la caducidad sin esperar una semana de verdad.

    :raises InvalidUserError: si el nombre no puede nombrar a nadie.
    :raises MissingSecretError: si no hay llave con la que firmar.
    """
    moment = time.time() if now is None else now
    expires_at = int(moment + SESSION_MAX_AGE_SECONDS)

    # El contenido va a la vista: nombre y hasta cuándo vale. Nada secreto.
    payload = _encode(f"{normalize_user(user)}|{expires_at}".encode("utf-8"))

    return f"{payload}{SEPARATOR}{_sign(payload)}"


def read(token: str | None, now: float | None = None) -> str:
    """Lee de quién es la tarjeta, o se niega.

    🚨 **Se comprueba la firma ANTES de mirar el contenido.** Al revés sería
    trabajar con datos que todavía no se sabe si son nuestros — y aunque hoy
    solo se separen dos campos, ese orden es el que evita que mañana alguien
    use el nombre de una tarjeta falsa por el camino.

    :raises InvalidSessionError: si no hay tarjeta, o no vale.
    :raises MissingSecretError: si no hay llave con la que comprobar.
    """
    if not token:
        raise InvalidSessionError("No hay sesion iniciada.")

    payload, separator, signature = token.partition(SEPARATOR)
    if not separator:
        raise InvalidSessionError("La sesion no vale.")

    # 🚨 `compare_digest` y no `==`, igual que al comprobar la contrasena: `==`
    # tarda un poco mas cuantas mas letras acierta, y ese tiempo se mide desde
    # fuera para adivinar la firma por partes.
    if not hmac.compare_digest(_sign(payload), signature):
        raise InvalidSessionError("La sesion no vale.")

    # A partir de aqui el contenido es NUESTRO: lo firmamos nosotros. Aun asi se
    # lee con cuidado, porque una llave filtrada o un fallo nuestro al escribirlo
    # dejarian pasar cualquier cosa por aqui.
    try:
        user, _, expires_at = _decode(payload).decode("utf-8").partition("|")
        deadline = int(expires_at)
    except (ValueError, UnicodeDecodeError) as error:
        raise InvalidSessionError("La sesion no vale.") from error

    moment = time.time() if now is None else now
    if moment >= deadline:
        raise InvalidSessionError("La sesion caduco. Vuelve a entrar.")

    # 🔑 El nombre se vuelve a validar aunque venga de una tarjeta firmada.
    # Mismo criterio que [D-014]: con este nombre se construye una ruta de
    # archivo, y quien toca el disco no se fia de nadie. **El olvido tiene que
    # fallar hacia el lado seguro.**
    try:
        return normalize_user(user)
    except InvalidUserError as error:
        raise InvalidSessionError("La sesion no vale.") from error
