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

# 🚨 Dónde viven los datos de las personas: cuentas, marcadores y cuota. Ver
# `require_data_dir` y la decisión [D-037].
DATA_DIR_NAME = "TEAPP_DATA_DIR"

# Si la cookie viaja solo por HTTPS. En local es `false`; en la nube, `true`.
COOKIE_SECURE_NAME = "TEAPP_COOKIE_SECURE"

# Si `/register` atiende a cualquiera que llegue. Por defecto NO. Ver [D-027].
REGISTRATION_OPEN_NAME = "TEAPP_REGISTRATION_OPEN"

# Desde qué nivel se escribe en el log. Ver `configure_logging`.
LOG_LEVEL_NAME = "TEAPP_LOG_LEVEL"

# 🚨 **Las tres cosas que le faltaban a cada renglón, y por qué cada una.**
#
# - **Hora** (`asctime`): sin ella, un renglón no se puede cruzar con nada. "Se
#   cayó a las 3" no sirve de nada si el log no dice qué pasó a las 3.
# - **Nivel** (`levelname`): distingue "esto pasa todos los días" de "ven a
#   mirar". Sin él hay que leerlo todo con la misma atención, que en la práctica
#   significa no leer nada.
# - **Origen** (`name`): de qué módulo salió. Es la diferencia entre "el contador
#   está roto" y "`app.quota` dice que el contador está roto".
#
# ⚠️ El `|` separa la cabecera del mensaje a ojo. Sin separador, un mensaje que
# empieza por una palabra suelta parece parte del nombre del módulo.
LOG_FORMAT = "%(asctime)s %(levelname)-8s %(name)s | %(message)s"

# Sin milisegundos y sin zona: esto lo lee una persona buscando un momento, no
# una máquina midiendo. El detalle fino estorba más de lo que ayuda.
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

logger = logging.getLogger(__name__)


class MissingSecretError(Exception):
    """No hay llave de firma, así que no se puede firmar ninguna sesión.

    Excepción propia y no `KeyError` porque esto no es "falta una clave en un
    diccionario": es "el servidor no puede hacer su trabajo". Quien la lea tiene
    que saber qué escribir en qué archivo, no qué línea de Python falló.
    """

    # Los mensajes van sin tildes a proposito (ver [L-001]).


class MissingDataDirError(Exception):
    """No se sabe dónde viven los datos, así que no se toca ningún disco.

    Excepción propia por la misma razón que `MissingSecretError`: quien la lea
    tiene que saber qué variable poner y con qué valor, no qué línea de Python
    falló.
    """

    # Los mensajes van sin tildes a proposito (ver [L-001]).


def require_data_dir() -> Path:
    """Devuelve la carpeta raíz de los datos, o se niega a seguir.

    🚨 **Sin valor por defecto, a propósito. Este es el arreglo de [T-072].**
    Hasta hoy la raíz era `PROJECT_ROOT / "data"` calculada en tres módulos
    distintos, así que **olvidarse escribía en los datos de personas de verdad**:
    es lo que hizo la báscula de `T-054`, que desvió las cuentas y se olvidó del
    marcador y de la cuota ([L-023]). Un aislamiento que hay que recordar en tres
    sitios es un aislamiento que algún día no está.

    Ahora es un sitio solo, y **si se olvida no se arranca**. Mismo criterio que
    `require_secret` con la llave: `_context/architecture.md` dice denegar por
    defecto, y aquí el defecto seguro es no tener ninguno.

    🚨 **La ruta tiene que ser ABSOLUTA, y una relativa se rechaza en vez de
    resolverse.** Una ruta relativa se resuelve contra algo —el directorio desde
    el que se lanzó el proceso—, y ese "algo" es justo la variable que esta
    función existe para eliminar: el mismo script corrido desde otra carpeta
    escribiría en otro sitio. Resolverla contra la raíz del paquete tampoco vale:
    sería una segunda fuente de verdad sobre dónde viven los datos, que es lo que
    [D-037] viene a matar.

    ⚠️ **Y la carpeta NO se crea aquí.** Se comprueba que exista y se falla si no.
    Crearla sola convertiría una ruta mal escrita en un `data/` vacío donde todo
    el mundo parece haber perdido su marcador — sin un solo error, que es el peor
    tipo de fallo ([A-008] es de la misma familia). Crear la carpeta es un acto de
    instalación y vive en `deploy/install.sh`.

    🔑 **Se resuelve en CADA llamada, y nunca se guarda en una constante de
    módulo.** Una constante se calcularía al importar y se quedaría con el valor
    de aquel momento para siempre: es exactamente el defecto que arregló [D-036].

    :raises MissingDataDirError: si la variable falta, no es absoluta, o no
        apunta a una carpeta que exista.
    """
    raw = os.environ.get(DATA_DIR_NAME, "").strip()

    if not raw:
        raise MissingDataDirError(
            f"Falta {DATA_DIR_NAME}, y sin ella no se sabe donde escribir los "
            "datos de las personas. Ponla en tu .env con una ruta ABSOLUTA a una "
            "carpeta que ya exista. En local suele ser la carpeta `data` del "
            "propio proyecto; en el servidor, la del disco que persiste."
        )

    path = Path(raw)

    if not path.is_absolute():
        raise MissingDataDirError(
            f"{DATA_DIR_NAME} tiene que ser una ruta ABSOLUTA, y {raw!r} no lo "
            "es. Una ruta relativa se resuelve contra la carpeta desde la que se "
            "lanzo el proceso, asi que el mismo programa escribiria en sitios "
            "distintos segun desde donde se arranque. Escribe la ruta entera."
        )

    # `resolve()` deja una sola forma de la misma ruta: sin `..`, sin enlaces a
    # medias y con las mayusculas que tenga el disco. Asi el renglon del log dice
    # donde se escribe DE VERDAD, y no una version disfrazada de la misma carpeta.
    path = path.resolve()

    # `is_dir` y no `exists`: un ARCHIVO llamado `data` pasaria un `exists()` y
    # luego reventaria al escribir dentro, mucho mas lejos y sin explicacion.
    if not path.is_dir():
        raise MissingDataDirError(
            f"{DATA_DIR_NAME} apunta a {path}, que no es una carpeta que exista. "
            "No se crea sola a proposito: una ruta mal escrita se convertiria en "
            "una carpeta vacia, y quien use la app pareceria haber perdido su "
            "marcador sin que salte ningun error. Creala a mano si es la primera "
            "vez, o corrige la ruta."
        )

    return path


def users_dir() -> Path:
    """Dónde viven los marcadores: `<raiz>/users/`."""
    return require_data_dir() / "users"


def quota_dir() -> Path:
    """Dónde vive el gasto del día de cada persona: `<raiz>/quota/`."""
    return require_data_dir() / "quota"


def accounts_file() -> Path:
    """Dónde viven las credenciales: `<raiz>/accounts.json`."""
    return require_data_dir() / "accounts.json"


# Lo que el `.env` PROPUSO, gane o pierda contra el entorno. Lo rellena
# `load_env_file` y solo lo lee `value_origin`.
_ENV_FILE_VALUES: dict[str, str] = {}


def value_origin(name: str) -> str:
    """De dónde salió el valor que rige hoy: del `.env` o del entorno.

    🔑 **Se compara el valor, no se recuerda quién ganó.** Apuntar "lo puse yo"
    dentro de `load_env_file` envejecería mal: cualquiera puede cambiar la
    variable después —`monkeypatch` lo hace en cada test— y el apunte seguiría
    diciendo `.env` sobre un valor que ya no viene de ahí. Comparar el valor
    vivo contra el que proponía el archivo no se queda viejo nunca.

    🚨 **El punto ciego, escrito antes de que alguien lo descubra de madrugada.**
    Como compara valores, **cuando el entorno y el `.env` traen el MISMO valor no
    puede distinguirlos**: dirá `.env` aunque venga del entorno. No engaña sobre
    nada que importe —el valor efectivo es idéntico, nadie está anulando nada—
    pero es el límite de este instrumento y conviene saberlo: este renglón
    delata **anulaciones**, no procedencias. Si algún día hace falta lo segundo,
    esta función no sirve y hay que apuntar el origen en el momento de leerlo.
    """
    if name not in os.environ:
        return "sin valor"

    if _ENV_FILE_VALUES.get(name) == os.environ[name]:
        return ".env"

    return "entorno"


def load_env_file(path: Path = ENV_FILE) -> None:
    """Vuelca las líneas de `.env` en las variables de entorno del proceso.

    Doce líneas de librería estándar en vez de un paquete nuevo. Es lo que pide
    [C-001]: ni la suite ni el arranque tocan la red, y un paquete menos es un
    paquete que no hay que fijar, instalar ni actualizar.

    🔑 **Lo que ya está en el entorno NO se pisa, y eso es deliberado.**
    El `.env` es la configuración **por defecto de esta máquina**; el entorno es
    **esta corrida en concreto**. Lo específico gana a lo general, que es la
    convención de todo el mundo.

    🚨 **No es una comodidad: es lo que sostiene el aislamiento de la suite.**
    `tests/conftest.py` pone `TEAPP_DATA_DIR` a una carpeta temporal **al
    importarse**, antes que nada. Si el `.env` ganara, ese desvío se perdería al
    hacer `from app.api import app` y los tests escribirían en `data/` de verdad
    — `T-071` y `T-072` otra vez, entrando por la puerta de un arreglo. Lo mismo
    vale para cualquier corrida de una sola vez: un contenedor, un script.

    ⚠️ **Corregido el 2026-08-07.** Aquí decía *"en la nube del paso 7 no hay
    ningún `.env`: los secretos los pone la plataforma"*. Eso describía una
    plataforma que se descartó en `[D-029]`: la nube es EC2 y `deploy/install.sh`
    **sí escribe un `.env`** en la máquina. El comentario llevaba dos días
    describiendo un mundo que no existe, dentro del código que corre.

    📌 **Y por eso existe `value_origin`.** La regla no está mal, estaba **muda**:
    quien anula desde el entorno lo hace sin dejar rastro. Ahora el arranque dice
    de dónde salió el valor. Cero cambio de comportamiento; solo deja de ser
    invisible.

    Que el archivo no exista no es un error: hay corridas que van solo con
    entorno.
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
        name, value = name.strip(), value.strip()

        # Se apunta lo que el archivo PROPONE, gane o pierda. Con eso solo,
        # `value_origin` puede decir despues quien mando de verdad.
        _ENV_FILE_VALUES[name] = value
        os.environ.setdefault(name, value)


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


def configure_logging() -> None:
    """Decide qué se escribe en el log y con qué forma. Se llama al arrancar.

    🚨 **Esto es [T-033], y lo que arregla es un fallo que ya mordió dos veces.**
    Hasta hoy nadie había configurado el log, así que actuaba el **handler de
    último recurso** de Python, que empieza en `WARNING`. Consecuencia: cualquier
    `logger.info(...)` **no se perdía por poco, no existía**. Pasó con el motivo
    del frenazo de la cuota ([L-012]) y volvió a pasar con el aviso del registro
    cerrado ([D-027]) — las dos veces con el test en verde.

    🔑 **Por eso el arreglo de verdad no es este formato bonito: es que `info`
    vuelva a significar algo.** Mientras el nivel efectivo fuera `WARNING`, la
    única forma de que un renglón saliera era subirlo de nivel, y eso obliga a
    mentir sobre su importancia. Un log donde todo es aviso no tiene avisos.

    ⚠️ **`basicConfig` no hace nada si el logger raíz ya tiene handlers**, y eso
    es a propósito, no un descuido:

    - **Con uvicorn** la raíz está limpia —uvicorn configura sus propios loggers,
      no el raíz—, así que esto sí aplica. Comprobado el 2026-08-04.
    - **Bajo pytest** la raíz ya está tomada por `caplog`. Que aquí no se pise
      nada es justo lo que se quiere: la suite captura a su manera.

    🚨 Y por eso **no** se usa `force=True`. Forzar borraría los handlers del
    raíz, y bajo pytest eso es arrancarle a `caplog` el suyo en mitad de la
    suite.
    """
    logging.basicConfig(
        # El nivel se puede subir o bajar sin tocar código: en la nube del paso 7
        # puede interesar `WARNING` para no pagar por guardar ruido.
        level=os.environ.get(LOG_LEVEL_NAME, "INFO").strip().upper(),
        format=LOG_FORMAT,
        datefmt=LOG_DATE_FORMAT,
    )


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

    🚨 **Esto NO cierra `accounts.register`, solo la ruta de red.** Las cuentas
    se siguen creando con `create_account.py` — si no, este interruptor dejaría
    fuera también a quien administra el servidor, y no habría forma de crear la
    primera cuenta. Ver [D-027].

    ⚠️ **Y la herramienta es `create_account.py`, NO `main.py`**, aunque `main.py`
    también cree cuentas. `main.py` usa `getpass`, que en Windows lee de la
    consola y no de la entrada estándar: en un servidor se queda colgado
    esperando un teclado que no hay. Comprobado el 2026-08-04.
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
        # ✅ **`info`, y ahora sí se ve.** Nació como `info`, se subió a `warning`
        # porque sin log configurado no salía ([L-012] otra vez), y vuelve a
        # `info` ahora que [T-033] está hecho: **el registro cerrado es el estado
        # NORMAL, no una alarma.** Un log donde todo es aviso no tiene avisos.
        #
        # 🔑 Lo que sostiene que esto se vea es `configure_logging`, no la suerte.
        # Y quien lo vigila es `test_the_configured_log_makes_info_visible`: sin
        # ese test, bajar esta línea de nivel sería volver a apagarla a ciegas.
        # ⚠️ **El cartel manda a `create_account.py`, y no a `main.py`, a
        # proposito.** Este renglon lo lee quien administra, y puede leerlo EN EL
        # SERVIDOR: alli `main.py` se cuelga esperando un teclado que no hay. Un
        # cartel que apunta a una herramienta que no funciona donde esta quien lo
        # lee es peor que no poner cartel.
        logger.info(
            "Registro por red CERRADO (%s no es 'true'). /register contesta 403. "
            "Las cuentas se crean con create_account.py, que no pide teclado "
            "(ejecutalo sin argumentos para ver como).",
            REGISTRATION_OPEN_NAME,
        )


def log_data_dir() -> None:
    """Deja escrito en el log dónde se van a escribir los datos. Al arrancar.

    🔑 **Una línea, y contesta una pregunta que si no hay que reconstruir.**
    "¿Dónde está escribiendo esta app?" sin este renglón se responde leyendo tres
    módulos y adivinando desde qué carpeta se lanzó el proceso. Con él se
    responde mirando.

    📌 **Y es el testigo de `T-066` gratis.** Al arrancar en la nube, este renglón
    dice si cogió el disco que persiste o cualquier otro sitio — que es justo lo
    que esa tarea tiene que comprobar.

    La ruta va **ya resuelta**, porque lo que importa es dónde acaba escribiendo,
    no lo que decía el `.env`.

    ⚠️ Va al log del servidor, que lo lee quien administra. Hacia el navegador no
    sale ninguna ruta nunca — eso cuenta cómo está organizada la máquina por
    dentro y quien pregunta no puede hacer nada con ello.
    """
    logger.info(
        "Datos de las personas en %s (%s, origen: %s)",
        require_data_dir(),
        DATA_DIR_NAME,
        value_origin(DATA_DIR_NAME),
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
