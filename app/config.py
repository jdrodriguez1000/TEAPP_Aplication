"""De dónde salen los secretos y los ajustes del servidor.

🚨 Un secreto NUNCA se escribe en un archivo de código. Vive en `.env`, que está
en `.gitignore`, y de ahí lo lee este módulo. Un secreto escrito aquí acabaría
en Git, y lo que entra en Git ya no sale: queda en el historial aunque se borre
después.

Este archivo no guarda nada. Solo sabe DÓNDE preguntar.
"""

import logging
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

ENV_FILE = PROJECT_ROOT / ".env"

# La llave con la que se firman las sesiones. Ver `app/sessions.py`.
SECRET_KEY_NAME = "TEAPP_SECRET_KEY"

# Si la cookie viaja solo por HTTPS. En local es `false`; en la nube, `true`.
COOKIE_SECURE_NAME = "TEAPP_COOKIE_SECURE"

# Si `/register` atiende a cualquiera que llegue. Por defecto NO. Ver [D-027].
REGISTRATION_OPEN_NAME = "TEAPP_REGISTRATION_OPEN"

logger = logging.getLogger(__name__)


class MissingSecretError(Exception):
    """No hay llave de firma, así que no se puede firmar ninguna sesión.

    Excepción propia y no `KeyError` porque esto no es "falta una clave en un
    diccionario": es "el servidor no puede hacer su trabajo". Quien la lea tiene
    que saber qué escribir en qué archivo, no qué línea de Python falló.
    """

    # Los mensajes van sin tildes a proposito (ver [L-001]).


def load_env_file(path: Path = ENV_FILE) -> None:
    """Vuelca las líneas de `.env` en las variables de entorno del proceso.

    Doce líneas de librería estándar en vez de un paquete nuevo. Es lo que pide
    [C-001]: ni la suite ni el arranque tocan la red, y un paquete menos es un
    paquete que no hay que fijar, instalar ni actualizar.

    🔑 **Lo que ya está en el entorno NO se pisa.** En la nube del paso 7 no hay
    ningún `.env`: los secretos los pone la plataforma directamente en el
    entorno. Si este archivo los sobrescribiera, un `.env` olvidado en la imagen
    tumbaría la configuración de producción sin decir nada.

    Que el archivo no exista no es un error: en la nube es lo normal.
    """
    if not path.exists():
        return

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()

        # Los comentarios y las lineas en blanco se saltan. Y lo que no tenga
        # un `=` tampoco es un ajuste: se ignora en vez de reventar, porque un
        # `.env` a medio escribir no debe impedir arrancar.
        if not line or line.startswith("#") or "=" not in line:
            continue

        name, _, value = line.partition("=")
        os.environ.setdefault(name.strip(), value.strip())


def require_secret() -> bytes:
    """Devuelve la llave de firma, o se niega a seguir.

    🔑 **Aquí no hay llave de repuesto, y es a propósito.** Inventar una al vuelo
    con `secrets.token_bytes` haría que el servidor arrancara siempre — y que
    cada reinicio estrenara llave, tirando fuera a todo el mundo sin decir por
    qué. Un fallo que se explica solo es mejor que una comodidad que miente.

    Es el criterio de `_context/architecture.md` aplicado a la configuración:
    **denegar por defecto.** Lo que no esté puesto explícitamente, se rechaza.

    :raises MissingSecretError: si la variable no está o está vacía.
    """
    secret = os.environ.get(SECRET_KEY_NAME, "").strip()

    if not secret:
        raise MissingSecretError(
            f"Falta {SECRET_KEY_NAME}. Copia .env.example como .env y ponle un "
            "valor generado con: python -c \"import secrets; "
            'print(secrets.token_hex(32))"'
        )

    # La firma se hace sobre bytes, no sobre texto. Se convierte aqui, en un
    # solo sitio, para que quien firme no tenga que acordarse.
    return secret.encode("utf-8")


def cookie_secure() -> bool:
    """Si la cookie de sesión debe viajar solo por HTTPS.

    🔑 **Por defecto sí, aunque eso moleste en local.** Una cookie sin `Secure`
    viaja en claro por HTTP: cualquiera en la misma red la copia y entra como si
    fuera esa persona. El valor por defecto tiene que ser el seguro, y quien
    quiera el otro que lo pida por escrito — es la regla 3 del proyecto.

    ⚠️ En local se pone `false` en el `.env`, porque el navegador **descarta en
    silencio** una cookie `Secure` que llega por `http://localhost`. El inicio de
    sesión parecería no hacer nada, sin ningún error. Por eso el arranque escribe
    en el log cuál de los dos modos está activo: para que ese fallo mudo se
    diagnostique de un vistazo y no a base de suposiciones.
    """
    return os.environ.get(COOKIE_SECURE_NAME, "true").strip().lower() != "false"


def registration_open() -> bool:
    """Si `/register` atiende por la red a quien no tiene cuenta.

    🔑 **Por defecto NO, y fíjate en que aquí el defecto seguro es el contrario
    que en `cookie_secure`.** Allí lo seguro es `true`; aquí lo seguro es
    `false`. No es una incoherencia: la regla no es "el defecto es true", es
    **denegar por defecto** — lo que no se haya permitido por escrito, se
    rechaza. En cada ajuste eso cae de un lado distinto.

    ⚠️ **Y se exige la palabra exacta `true` para abrir**, en vez de aceptar
    cualquier cosa que no sea `false`. `cookie_secure` puede permitirse lo
    segundo porque allí equivocarse deja la puerta cerrada; aquí equivocarse la
    abriría. Un `TEAPP_REGISTRATION_OPEN=yes` mal escrito **no** abre nada.

    🚨 **Esto NO cierra `accounts.register`, solo la ruta de red.** La terminal
    (`main.py`) sigue creando cuentas igual — si no, este interruptor dejaría
    fuera también a quien administra el servidor, y no habría forma de crear la
    primera cuenta. Ver [D-027].
    """
    return os.environ.get(REGISTRATION_OPEN_NAME, "false").strip().lower() == "true"


def log_registration_mode() -> None:
    """Deja escrito en el log si `/register` está abierto. Se llama al arrancar.

    Misma razón que `log_cookie_mode`: sin esta línea, un registro cerrado se ve
    desde fuera como un servidor que "no deja registrarse" —un 403 sin más—, y
    quien administre no sabría si es el interruptor o una avería.
    """
    if registration_open():
        # Sin emoji: esto acaba en la consola de Windows, que no pinta nada
        # fuera de ASCII (ver [L-001]).
        logger.warning(
            "AVISO: %s=true. Cualquiera que llegue a la direccion puede crear "
            "una cuenta, y cada cuenta nueva cuesta un scrypt entero. Solo vale "
            "mientras el registro tenga que estar abierto a proposito.",
            REGISTRATION_OPEN_NAME,
        )
    else:
        # 🚨 **`warning` y no `info`, y no es una opinion sobre la gravedad: es
        # lo que se midio.** Con `info` esta linea NO SALE. Hoy nadie ha
        # configurado el log ([T-033]), asi que Python usa su handler de ultimo
        # recurso, que empieza en WARNING. Comprobado con uvicorn el 2026-08-04:
        # escrita con `info`, el arranque no la imprimio ni una vez — y entonces
        # el unico sintoma de un registro cerrado seria un 403 sin explicacion,
        # que es justo lo que esta linea viene a evitar. Ver [L-012].
        #
        # ⚠️ Cuando [T-033] configure el log, esto vuelve a ser `info`: el
        # registro cerrado es el estado NORMAL, no una alarma.
        logger.warning(
            "Registro por red CERRADO (%s no es 'true'). /register contesta 403. "
            "Las cuentas se crean desde la terminal con main.py.",
            REGISTRATION_OPEN_NAME,
        )


def log_cookie_mode() -> None:
    """Deja escrito en el log si las cookies exigen HTTPS. Se llama al arrancar."""
    if cookie_secure():
        logger.info(
            "Cookies de sesion en modo SEGURO (Secure): solo viajan por HTTPS. "
            "Si estas en http://localhost, el navegador las descartara y el "
            "inicio de sesion parecera no hacer nada. Pon %s=false en tu .env.",
            COOKIE_SECURE_NAME,
        )
    else:
        # Sin emoji: esto acaba impreso en la consola, y la de Windows no sabe
        # pintar nada fuera de ASCII — lo saca como "\U0001f6a8". Ver [L-001].
        logger.warning(
            "AVISO: cookies de sesion SIN Secure, viajan tambien por HTTP. "
            "Vale para desarrollo local. En la nube del paso 7 esto tiene que "
            "ser %s=true.",
            COOKIE_SECURE_NAME,
        )
