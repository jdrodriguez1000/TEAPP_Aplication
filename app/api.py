"""La puerta de entrada por la red. Sustituye a `main.py`, no lo amplía.

🚨 Aquí NO hay `input()`, y no puede haberlo. En un servidor no hay teclado
detrás: un `input()` se quedaría esperando a un humano que nunca escribe, y con
él se quedaría colgada la petición, el servidor y todo lo demás. Esa es la
diferencia de fondo entre este archivo y `main.py`, no el protocolo.

FastAPI no es un framework de agentes: es un recepcionista. Recibe texto de
afuera, llama a `respond`, que ya existía, y devuelve el resultado. El agente no
se entera de que lo llamaron por la red.
"""

import logging
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import TimeoutError as TutorTookTooLong
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import accounts, login_guard, quota, sessions
from app.accounts import AccountsFileError, UserExistsError, WeakPasswordError
from app.config import (
    MissingSecretError,
    configure_logging,
    cookie_secure,
    load_env_file,
    log_cookie_mode,
    log_registration_mode,
    registration_open,
)
from app.english_tutor import respond
from app.login_guard import TooManyAttemptsError
from app.quota import QuotaExceededError, QuotaFileError
from app.tools import InvalidUserError, ScoreFileError, normalize_user

# Los secretos entran en el entorno ANTES de que nadie los pida. En la nube del
# paso 7 no habra `.env` y esta llamada no hara nada: alli los pone la
# plataforma, y `load_env_file` no pisa lo que ya esta puesto.
load_env_file()

app = FastAPI(title="TEAPP", description="Practica ingles escrito.")

# La carpeta de la pantalla, calculada desde ESTE archivo y no desde donde se
# lanzo el servidor. Con una ruta relativa, arrancar desde otra carpeta dejaria
# de encontrarla — y en la nube nadie garantiza desde donde se arranca.
STATIC_DIR = Path(__file__).parent / "static"

# 🔑 **El mismo servidor entrega la pantalla y atiende /practice.**
#
# Por eso no hay CORS en este archivo, y no es un olvido: CORS solo existe
# cuando hay DOS origenes, y aqui hay uno solo. El navegador ve un unico sitio
# —mismo protocolo, mismo nombre, mismo puerto— y no tiene nada que bloquear.
# Ver [D-011]. Ademas en la nube se enciende un solo servicio, que es lo que
# `_context/architecture.md` pedia al descartar Next.js.
#
# Los archivos que salen de aqui son PUBLICOS: cualquiera los puede leer. Por
# eso en `static/` no hay ni puede haber una llave.
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

# El cuaderno del servidor. Aqui se escribe lo que pasa por dentro, y esto NO
# viaja al navegador: lo lee quien administra el servidor.
logger = logging.getLogger(__name__)

# 🔑 **El detalle completo va al log; al navegador, un mensaje corto.**
#
# Son dos publicos distintos, igual que en [D-005] con el idioma. El mensaje de
# `ScoreFileError` se escribio para la terminal, donde decir QUE archivo abrir
# es ayuda. Fuera del servidor eso es informacion regalada: la ruta absoluta
# cuenta como esta organizado el servidor por dentro, y quien pregunta no puede
# hacer nada con ella.
#
# El criterio se aplica igual a los dos lados: nada de rutas hacia afuera, y
# nada de silencio hacia adentro.
SCORE_BROKEN_MESSAGE = (
    "El marcador del servidor no se pudo leer. Avisa a quien lo administra."
)
UNEXPECTED_MESSAGE = "Algo fallo en el servidor. Avisa a quien lo administra."
ACCOUNTS_BROKEN_MESSAGE = (
    "Las cuentas del servidor no se pudieron leer. Avisa a quien lo administra."
)
NO_SECRET_MESSAGE = "El servidor no esta configurado. Avisa a quien lo administra."
QUOTA_BROKEN_MESSAGE = (
    "El contador de practicas del servidor no se pudo leer. Avisa a quien lo "
    "administra."
)

# 🚨 **Lo más largo que se acepta practicar de una vez.**
#
# Hoy `judge_grammar` es falsa: da igual que lleguen tres palabras o tres
# millones, devuelve lo mismo y no cuesta nada. En el paso 8 esa función es una
# llamada al modelo, **y ahí se paga por el tamaño del texto**. Sin este tope,
# una sola peticion puede costar lo que cien.
#
# 🔑 Por eso el freno se pone HOY y no en el paso 8: en el paso 8 esta linea
# habria que escribirla el mismo dia que se enchufa el modelo, con la factura ya
# corriendo y dos sospechosos en vez de uno.
#
# El numero sale del alcance, no de una medicion: `scope.md` pide practicar
# frases de nivel A1, y 500 caracteres son varias frases largas. Es facil de
# cambiar; lo que no es facil es no tenerlo.
MAX_SENTENCE_LENGTH = 500

# ── El timeout del tutor ──────────────────────────────────────────────────
#
# 🚨 **Cuánto se espera al tutor antes de rendirse.**
#
# Hoy el tutor contesta al instante: es falso. En el paso 8 será una llamada por
# internet al modelo, y una llamada por internet puede no volver nunca. Sin este
# freno, la petición se queda colgada — y con ella el hilo que la atiende. Diez
# peticiones colgadas y el servidor deja de atender a nadie más **sin que haya
# fallado nada**: solo esperando.
#
# 🔑 **Lo que este freno hace y lo que NO hace, que es lo importante.**
# Libera a QUIEN PREGUNTA, no al hilo que trabaja. Python no sabe matar un hilo
# a la fuerza: si el tutor se queda esperando dentro, ahí sigue. Lo que se corta
# es la espera de quien llamó, que recibe su 504 y se va.
#
# ⚠️ Por eso, **en el paso 8 la llamada al modelo necesita SU PROPIO timeout**,
# además de este. Si el cliente del modelo espera para siempre, este 504 devuelve
# el control a quien pregunta y deja el hilo secuestrado igual. Los dos frenos no
# se sustituyen: **este acota lo que espera quien pregunta; el otro acota lo que
# espera el servidor.**
#
# El número es una predicción, no una medida ([A-011]): hoy no hay nada que
# tarde, así que no hay nada que cronometrar.
TUTOR_TIMEOUT_SECONDS = 10.0

TUTOR_TIMEOUT_MESSAGE = (
    "El tutor tardo demasiado en contestar. Intentalo otra vez en un momento."
)

# Cuántos tutores pueden estar trabajando a la vez.
#
# 🚨 **Escrito a mano, y no dejado por defecto.** `ThreadPoolExecutor()` sin
# número saca el tamaño de las CPUs de la máquina: aquí salían **20** (16 CPUs),
# y en la nube saldría otro. Un freno cuyo tamaño cambia según dónde corra no se
# puede razonar — y este es de los que deciden a quién se cobra.
#
# El 40 no es un número bonito: es el mismo con el que FastAPI atiende las rutas
# `def` como esta. Las manda a hilos con `anyio`, y el limitador por defecto de
# `anyio` trae **40 fichas**. Igualarlo es lo que sostiene el invariante que hace
# correcto todo lo de abajo:
#
# 🔑 **La cola del tutor nunca es el cuello de botella.** Si FastAPI no puede
# atender más de 40 peticiones a la vez, nunca habrá 41 tutores pidiendo sitio —
# y por tanto nadie espera en cola por culpa de este pool.
#
# 🚨 **Ese 40 de `anyio` es un valor por defecto de una librería que no fijamos**
# (`anyio` entra de rebote con `fastapi`, no está en `requirements.txt`). Si
# cambiara, el invariante se rompería **en silencio** y volvería el cobro por
# espera de [L-013]. Por eso hay un test que compara los dos números:
# `test_the_pool_matches_the_threads_fastapi_actually_uses`. Un invariante que
# depende del defecto de otro necesita quien lo vigile, no un comentario.
#
# ⚠️ Si algún día se arranca uvicorn con más hilos, este número sube con él.
TUTOR_POOL_SIZE = 40

# El sitio donde corre el tutor, aparte del hilo que atiende la petición. Esa
# separación es la que permite dejar de esperarlo: si corriera en el mismo hilo,
# no habría desde dónde mirar el reloj.
#
# ⚠️ Un tutor colgado deja su hilo ocupado hasta que termine —y retrasa el
# apagado del servidor, porque estos hilos se esperan al salir—. Es el precio de
# no poder matar un hilo en Python, y la razón del aviso de arriba.
_TUTOR_POOL = ThreadPoolExecutor(
    max_workers=TUTOR_POOL_SIZE, thread_name_prefix="tutor"
)

# 🔑 **Un solo mensaje para "no existe" y para "la contrasena no es esa".**
# Separarlos dejaria averiguar quien tiene cuenta aqui probando nombres, y eso
# ya es media respuesta para quien luego vaya a por la contrasena.
BAD_CREDENTIALS_MESSAGE = "El nombre o la contrasena no son correctos."
NOT_LOGGED_IN_MESSAGE = "Inicia sesion para practicar."

# 🚨 **El mensaje del frenazo no dice ni una palabra de la cuenta.** Es lo mismo
# que hace `BAD_CREDENTIALS_MESSAGE`, aplicado un escalon mas arriba: el freno
# cuenta por origen, asi que contesta igual para un nombre real que para uno
# inventado. Si dijera "esta cuenta esta bloqueada", probar nombres volveria a
# decir cuales existen — y el paso 5 se deshace por la puerta de atras.
# 🔑 **Dice que está cerrado y a quién preguntar, y nada más.** No dice cuándo
# abrirá ni quién puede entrar: eso solo serviría para saber a quién apuntar.
REGISTRATION_CLOSED_MESSAGE = (
    "El registro esta cerrado. Pide una cuenta a quien administra el servidor."
)

TOO_MANY_ATTEMPTS_MESSAGE = (
    "Demasiados intentos fallidos desde tu conexion. Espera {minutes} minutos y "
    "vuelve a intentarlo."
)

# Al arrancar queda escrito si las cookies exigen HTTPS. Sin esta linea, una
# cookie `Secure` sobre `http://localhost` se descarta en silencio y el inicio de
# sesion parece no hacer nada — un fallo mudo que se buscaria a ciegas.
# 🚨 **Lo PRIMERO, antes de cualquier otro renglón.** Las líneas de abajo se
# escriben en el log, y un log sin configurar se queda en WARNING: un `info`
# escrito antes de esta llamada no existiría. Ver [T-033] y [L-012].
configure_logging()

log_cookie_mode()

# Y si `/register` atiende o no. Sin esta linea, un registro cerrado se ve desde
# fuera como un 403 sin explicacion, y quien administre no sabria si es el
# interruptor o una averia.
log_registration_mode()


class PracticeRequest(BaseModel):
    """Lo que se espera recibir: la frase. Y nada más.

    🔑 Esto es un filtro, no un adorno. Lo que llega por la red lo escribe
    cualquiera, así que puede venir un número, un `null`, una lista o nada. Al
    declarar `sentence` como `str`, FastAPI rechaza todo eso ANTES de que el
    agente lo vea, y contesta un 422 explicando qué esperaba.

    Es el mismo criterio de los permisos, aplicado a los datos: **denegar por
    defecto.** Lo que no encaje con lo declarado, no entra.

    🚨 **Aquí ya NO hay `user`, y ese hueco es el paso 5 entero.** Hasta ahora el
    nombre venía en el cuerpo y el servidor se lo creía: cualquiera mandaba
    `{"user": "juan"}` con `curl` y se quedaba con el marcador de Juan ([D-013]).
    Ahora el nombre sale de la cookie firmada y de ningún otro sitio.

    ⚠️ Si alguien manda `user` en el cuerpo, se **ignora**. Nada lo lee.
    """

    sentence: str


class PracticeResponse(BaseModel):
    """Lo que se devuelve: las tres piezas por separado.

    Escrito aquí a propósito, aunque `TutorReply` ya diga lo mismo. Este es el
    contrato PÚBLICO —lo que la pantalla del paso 3 va a leer— y conviene que
    esté a la vista y no dependa de cómo el agente se organice por dentro.
    """

    verdict: str
    words: int
    score: int


class CredentialsRequest(BaseModel):
    """Quién dice ser y con qué lo prueba.

    ⚠️ La contraseña entra por aquí y **no sale nunca**: no se registra en el
    log, no se devuelve en ninguna respuesta y no se guarda. Lo que se guarda es
    su hash — ver `app/accounts.py`.
    """

    user: str
    password: str


class MeResponse(BaseModel):
    """Quién es, según la tarjeta que trajo. Nada más: aquí no va la contraseña."""

    user: str


# ── La identidad ──────────────────────────────────────────────────────────
#
# 🔑 **El nombre deja de venir en el cuerpo y pasa a venir en la tarjeta.**
# Antes el navegador DECIA quien era y el servidor se lo creia; ahora prueba
# quien es una vez, recibe una cookie firmada por el servidor, y en cada
# peticion la enseña. Ver [D-021].


def _start_session(response: Response, user: str) -> None:
    """Le entrega la tarjeta al navegador.

    Las tres marcas de la cookie no son adorno, y cada una tapa un agujero:

    - 🚨 **`httponly`**: el JavaScript de la pagina NO la puede leer. Esta es la
      diferencia de fondo con el `localStorage` del paso 4, que cualquier script
      leia. Con `httponly`, un script colado en la pagina no se lleva la sesion.
    - 🚨 **`secure`**: solo viaja por HTTPS, asi que nadie la copia de la red.
      En local se apaga por `.env`, porque el navegador descarta en silencio una
      cookie `Secure` que llega por `http://localhost`.
    - 🚨 **`samesite="lax"`**: el navegador no la manda cuando quien dispara la
      peticion es OTRA pagina. Sin esto, una web cualquiera podria hacer que tu
      navegador sumara puntos en tu nombre sin que te enteraras.

    `max_age` hace que el navegador la tire cuando caduque. Es el mismo plazo que
    lleva firmado dentro la tarjeta: el de dentro es el que manda —el navegador
    no es de fiar—, y el de fuera solo evita pasear una cookie ya muerta.
    """
    response.set_cookie(
        key=sessions.SESSION_COOKIE,
        value=sessions.issue(user),
        max_age=sessions.SESSION_MAX_AGE_SECONDS,
        httponly=True,
        secure=cookie_secure(),
        samesite="lax",
    )


def _current_user(request: Request) -> str:
    """Dice quién manda la petición, según su tarjeta.

    🚨 **Este es el único sitio del que sale un nombre de persona.** Mientras
    nadie lea el nombre de otro lado —del cuerpo, de una cabecera, de donde
    sea— la identidad esta verificada. El dia que aparezca una segunda fuente,
    el paso 5 estara deshecho aunque este archivo siga entero.

    :raises HTTPException: 401 si no hay tarjeta valida.
    """
    try:
        return sessions.read(request.cookies.get(sessions.SESSION_COOKIE))
    except sessions.InvalidSessionError as error:
        # 401 y no 403: "no se quien eres", no "se quien eres y no te dejo".
        raise HTTPException(status_code=401, detail=NOT_LOGGED_IN_MESSAGE) from error
    except MissingSecretError as error:
        # Culpa del servidor, no de quien pregunta. El detalle va al log; hacia
        # fuera, un mensaje que no cuenta que falta una variable de entorno.
        logger.error("No se puede leer la sesion: %s", error)
        raise HTTPException(status_code=500, detail=NO_SECRET_MESSAGE) from error


@app.post("/register", response_model=MeResponse, status_code=201)
def register(credentials: CredentialsRequest, response: Response) -> MeResponse:
    """Crea una cuenta y deja la sesión iniciada.

    🚨 **Se niega si el nombre ya existe**, y ese freno es la mitad del paso 5.
    Sin el, cualquiera se registra como `juan` y hereda su marcador: seria el
    agujero de [D-013] con un formulario delante. Ver [D-020].

    Quien se registra entra directamente: pedirle la contraseña otra vez, dos
    segundos despues de escribirla dos veces, no comprueba nada nuevo.

    🚨 **Y con el registro cerrado ni siquiera se mira la contraseña.** Ese orden
    es el freno entero, y esta medido ([D-027]): un nombre NUEVO cuesta 128 ms de
    CPU y una reescritura del archivo de todas las cuentas, porque pasa por
    `scrypt`. Un rechazo aqui arriba cuesta lo que cuesta un `if`.
    """
    if not registration_open():
        # 403 y no 401: no es "no se quien eres" —da igual quien seas—, es "se lo
        # que pides y no se lo doy a nadie". Y no dice ni una palabra de quien
        # puede registrarse, porque hoy no puede nadie.
        raise HTTPException(
            status_code=403, detail=REGISTRATION_CLOSED_MESSAGE
        )

    try:
        user = accounts.register(credentials.user, credentials.password)
    except InvalidUserError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except WeakPasswordError as error:
        raise HTTPException(status_code=422, detail=str(error)) from error
    except UserExistsError as error:
        # 409 y no 422: el nombre es perfectamente valido, lo que pasa es que ya
        # tiene dueño. "Conflicto" es exactamente eso.
        raise HTTPException(status_code=409, detail=str(error)) from error
    except AccountsFileError as error:
        # El mensaje original lleva la ruta del archivo dentro: se queda en el
        # log. Misma regla que con el marcador — ver [D-010].
        logger.error("El archivo de cuentas esta roto: %s", error)
        raise HTTPException(status_code=500, detail=ACCOUNTS_BROKEN_MESSAGE) from error

    try:
        _start_session(response, user)
    except MissingSecretError as error:
        # ⚠️ La cuenta YA quedo creada. Se avisa claro en el log para que quien
        # administre sepa que el registro funciono y lo que fallo fue la firma:
        # con la llave puesta, esa persona entra sin volver a registrarse.
        logger.error(
            "Cuenta %r creada, pero no se pudo iniciar sesion: %s", user, error
        )
        raise HTTPException(status_code=500, detail=NO_SECRET_MESSAGE) from error

    return MeResponse(user=user)


def _request_origin(request: Request) -> str:
    """De dónde viene la petición, para el freno de intentos.

    ⚠️ **`request.client` puede no existir**, y no es un caso raro de manual: en
    los tests y en algunas plataformas llega vacío. Cuando no se sabe de dónde
    viene, se devuelve un origen único compartido — todas las peticiones sin
    remitente caen en el mismo cubo y se frenan juntas. **Denegar por defecto**:
    dejar pasar lo que no se sabe de dónde viene sería abrir la puerta de atrás.

    🚨 **Con un proxy delante, esta dirección sería la del proxy** — la misma
    para todo el mundo, y entonces el freno dejaría fuera a todos a la vez.
    ✅ **Eso ya está resuelto, y NO aquí:** lo arregla uvicorn antes de que esta
    función llegue a ejecutarse, con `--proxy-headers` y
    `--forwarded-allow-ips 127.0.0.1` en `deploy/teapp.service` — reescribe
    `request.client` con la dirección real de `X-Forwarded-For`, y **solo** si la
    petición llega por loopback. Medido con uvicorn real el 2026-08-06: los
    cuatro escenarios están en [D-034].

    🚨 **Por eso aquí NO se lee `X-Forwarded-For` a mano, y no es un olvido.**
    Esa cabecera la escribe cualquiera: leerla sin comprobar de dónde viene la
    petición no es un freno flojo, es un freno **inservible** — quien ataca pone
    una dirección distinta en cada intento y no se frena nunca. Si algún día
    parece que "falta" leerla, la respuesta está en [D-034] y en [T-055].
    """
    return request.client.host if request.client else login_guard.UNKNOWN_ORIGIN


@app.post("/login", response_model=MeResponse)
def login(
    credentials: CredentialsRequest, request: Request, response: Response
) -> MeResponse:
    """Comprueba la contraseña y entrega la tarjeta.

    🚨 **El freno de intentos va ANTES de mirar la contraseña.** Al revés, cada
    intento seguiría pagando un `scrypt` entero —que es lento a propósito
    ([D-021])— y el freno no ahorraría el trabajo que quien ataca provoca.
    """
    origin = _request_origin(request)

    try:
        login_guard.check(origin)
    except TooManyAttemptsError as error:
        # 🚨 **WARNING, y este SE QUEDA en warning aunque [T-033] ya esté hecho.**
        #
        # Los otros dos renglones que se habían subido de nivel —la cuota agotada
        # y el registro cerrado— han vuelto a `info`, porque describen el sistema
        # funcionando. Este no.
        #
        # 🔑 **La diferencia no es el log, es lo que cuenta cada renglón.** Que
        # alguien agote su cuota es el freno haciendo su trabajo. Que alguien
        # falle cinco contraseñas seguidas es **alguien intentando entrar en una
        # cuenta que no es suya**, y eso se mira aunque no se esté buscando.
        #
        # ⚠️ Y pesa el doble porque el contador vive en memoria: se borra entero
        # en cada reinicio, así que este renglón es **el único rastro que
        # sobrevive** de que aquello pasó. Ver [D-026].
        logger.warning(
            "Demasiados intentos: el origen %s lleva %s de %s (faltan %s s)",
            error.origin,
            error.attempts,
            error.limit,
            error.retry_after,
        )
        # Los segundos exactos se redondean hacia arriba a minutos para el
        # mensaje: quien lo lee necesita saber si esperar o irse, no el segundo.
        raise HTTPException(
            status_code=429,
            detail=TOO_MANY_ATTEMPTS_MESSAGE.format(
                minutes=-(-error.retry_after // 60)
            ),
            # `Retry-After` es la cabecera estandar: la entienden los clientes
            # sin tener que leer un texto en español.
            headers={"Retry-After": str(error.retry_after)},
        ) from error

    try:
        # El nombre se normaliza aqui para que la tarjeta lleve la forma unica,
        # la misma con la que se guardo la cuenta y con la que se nombra el
        # marcador. `  JUAN ` y `juan` son la misma persona — ver [D-014].
        user = normalize_user(credentials.user)
        correct = accounts.verify(user, credentials.password)
    except InvalidUserError as error:
        # 🔑 Un nombre imposible contesta lo MISMO que una contraseña mala. Un
        # 422 explicando la regla aqui seria contarle a quien prueba cuales de
        # sus intentos merecen la pena.
        #
        # Y cuenta como intento fallido por la misma razon: si los nombres
        # imposibles salieran gratis, habria una forma de tantear la puerta sin
        # gastar cupo.
        login_guard.record_failure(origin)
        raise HTTPException(
            status_code=401, detail=BAD_CREDENTIALS_MESSAGE
        ) from error
    except AccountsFileError as error:
        # ⚠️ **Esto NO cuenta como intento fallido.** El fallo es del servidor,
        # no de quien pregunta: si el archivo de cuentas se rompe, todo el mundo
        # acabaria bloqueado por una averia que no provoco nadie.
        logger.error("El archivo de cuentas esta roto: %s", error)
        raise HTTPException(status_code=500, detail=ACCOUNTS_BROKEN_MESSAGE) from error

    if not correct:
        login_guard.record_failure(origin)
        raise HTTPException(status_code=401, detail=BAD_CREDENTIALS_MESSAGE)

    # 🔑 **Acertar borra la cuenta de fallos.** Es lo que hace que este freno no
    # moleste a quien no esta atacando: cuatro intentos recordando la contraseña
    # y un acierto no dejan a nadie a un fallo del castigo.
    login_guard.clear(origin)

    try:
        _start_session(response, user)
    except MissingSecretError as error:
        logger.error("No se pudo firmar la sesion: %s", error)
        raise HTTPException(status_code=500, detail=NO_SECRET_MESSAGE) from error

    return MeResponse(user=user)


@app.post("/logout", status_code=204)
def logout(response: Response) -> None:
    """Retira la tarjeta.

    🔑 **Borrar la cookie es todo lo que hace, y hay que saber lo que eso NO
    hace:** la tarjeta que ya salio de aqui sigue siendo valida hasta que
    caduque. Quien tuviera una copia podria seguir usandola. Cerrar sesion de
    verdad —invalidarla en el servidor— exigiria llevar una lista de sesiones
    vivas, que es un almacen mas y no hace falta hoy (PI-2). Queda escrito para
    que no se confunda con lo que no es.

    Las marcas tienen que coincidir con las de `set_cookie` o el navegador no
    reconoce cual borrar, y la sesion seguiria en pie.

    ⚠️ **Aqui NO se devuelve el `response` inyectado, y costo una corrida real
    descubrirlo.** Devolverlo hace que FastAPI lo use tal cual, y ese objeto nace
    con `status_code = None`: uvicorn revienta con `KeyError: None` al buscar
    como se llama ese codigo. Se toca la cookie en el `response` inyectado y se
    devuelve `None`; FastAPI arma la respuesta con el 204 declarado arriba y le
    pega las cabeceras. Ver [L-010].
    """
    response.delete_cookie(
        key=sessions.SESSION_COOKIE,
        httponly=True,
        secure=cookie_secure(),
        samesite="lax",
    )


@app.get("/me", response_model=MeResponse)
def me(request: Request) -> MeResponse:
    """Dice quién eres, según tu tarjeta. La pantalla la usa para saber qué pintar."""
    return MeResponse(user=_current_user(request))


@app.get("/", response_class=FileResponse)
def index() -> FileResponse:
    """Entrega la pantalla. Es lo primero que ve quien abre la direccion.

    Se sirve aparte de `/static` a proposito: asi la direccion de entrada es la
    raiz limpia y no `/static/index.html`.
    """
    return FileResponse(STATIC_DIR / "index.html")


@app.post("/practice", response_model=PracticeResponse)
def practice(body: PracticeRequest, request: Request) -> PracticeResponse:
    """Recibe una frase, la pasa por el tutor y devuelve las tres piezas.

    Una sola ruta, a propósito: el paso 2 no añade funciones, solo cambia la
    puerta por la que se entra.
    """
    # 🚨 **Quien practica sale de la tarjeta, no de lo que mande.** Esta linea
    # es el paso 5: antes aqui se leia `request.user` y se normalizaba, que es
    # tanto como comprobar que un nombre inventado esta bien escrito. Sin
    # tarjeta valida no hay nadie, y se contesta 401.
    #
    # 🔑 Sigue valiendo lo de [D-014]: que el nombre llegue firmado no libera a
    # `tools.py` de validarlo otra vez. Aqui viene de un sitio de fiar; alli se
    # rechaza porque es quien toca el disco y no puede fiarse de quien lo llame.
    user = _current_user(request)

    # Una frase vacia —o solo espacios— no es practicar ingles, y sumaria un
    # punto por nada. Se rechaza con 422, el mismo codigo que usa FastAPI
    # cuando lo que llega no encaja con lo declarado.
    if not body.sentence.strip():
        raise HTTPException(status_code=422, detail="La frase no puede estar vacia.")

    # El otro extremo de lo mismo: ni vacia ni infinita. Se dice cuanto llego y
    # cuanto cabe, igual que hace `normalize_user` con el nombre — un "no vale"
    # a secas deja a quien lo lea adivinando por cuanto se paso.
    #
    # ⚠️ **Este freno protege el bolsillo, no el ancho de banda.** Cuando llega
    # aqui, el cuerpo de la peticion ya se leyo entero: quien mande 100 MB los
    # sube igual y luego recibe el 422. Lo que este tope impide es que ese texto
    # llegue al modelo, que es donde cuesta dinero. Frenar la subida es trabajo
    # del servidor de delante, en el paso 7, no de esta linea.
    if len(body.sentence) > MAX_SENTENCE_LENGTH:
        raise HTTPException(
            status_code=422,
            detail=(
                f"La frase no puede pasar de {MAX_SENTENCE_LENGTH} caracteres, "
                f"y esta tiene {len(body.sentence)}."
            ),
        )

    # 🚨 **El freno va AQUI: antes de trabajar, no después.** Ver [D-023].
    #
    # Hoy el tutor es falso y no falla nunca, así que el orden parece un detalle.
    # En el paso 8 no lo es: una llamada al modelo que gasta tokens y luego
    # revienta se colaría gratis si el contador subiera al final. Lo que se cobra
    # es haber intentado.
    #
    # ⚠️ Y va DESPUÉS del 422 de la frase vacía, a propósito: una petición que se
    # rechaza en la puerta no llega al tutor, no cuesta nada, y no gasta cuota.
    try:
        quota.spend(user)
    except QuotaExceededError as error:
        # 🔑 **429, y con motivo.** Un 429 pelado deja a quien lo recibe
        # adivinando si el servidor está caído, si es un fallo suyo o si es a
        # propósito. Se dice cuánto gastó, de cuánto era el tope y de qué día:
        # con eso se entiende sin preguntarle a nadie.
        #
        # Aquí no hay ruta de archivo que filtrar —a diferencia de los 500 de
        # abajo—, porque estos son datos de quien pregunta, sobre sí mismo.
        # ✅ **`info`, y ahora sí se ve.** Este renglón es el de [L-012]: nació
        # como `info`, se comprobó con uvicorn que **no salía ni una vez** —20
        # frenazos, cero líneas— y se subió a `warning` para que existiera.
        # [T-033] ya configuró el log, así que vuelve a su nivel de verdad.
        #
        # 🔑 **Y su nivel de verdad es `info`, no `warning`:** que alguien agote
        # su cuota diaria es el freno funcionando, no una avería. Dejarlo en
        # `warning` para siempre habría sido mentir sobre su importancia — y un
        # log donde todo es aviso no tiene avisos.
        logger.info(
            "Cuota agotada: %s lleva %s de %s el %s",
            error.user,
            error.used,
            error.limit,
            error.day,
        )
        raise HTTPException(
            status_code=429,
            detail=(
                f"Ya practicaste {error.used} veces hoy, que es el maximo "
                f"({error.limit}). Vuelve manana."
            ),
        ) from error
    except QuotaFileError as error:
        # 🔑 **El contador roto NO deja pasar.** Dejarlo pasar sería regalar la
        # cuota entera justo cuando el freno está averiado: el fallo caería del
        # lado inseguro. Denegar por defecto, la regla 3 del proyecto.
        logger.error("El contador de cuota esta roto: %s", error)
        raise HTTPException(status_code=500, detail=QUOTA_BROKEN_MESSAGE) from error

    # El tutor corre en otro hilo para poder dejar de esperarlo. `result` vuelve
    # a lanzar aqui lo que haya reventado alla, asi que los `except` de abajo
    # siguen cazando lo mismo que antes de que existiera el timeout.
    attempt = _TUTOR_POOL.submit(respond, body.sentence, user)

    try:
        reply = attempt.result(timeout=TUTOR_TIMEOUT_SECONDS)
    except TutorTookTooLong as error:
        # 🚨 **504 y no 500.** No es que algo se haya roto: es que no contesto a
        # tiempo. Quien lo reciba tiene que saber que reintentar puede funcionar,
        # y con un 500 no lo sabria.
        #
        # 🚨 **Aqui se decide si la practica se cobra o se devuelve, y `cancel()`
        # es quien lo sabe.** Devuelve `True` solo si la tarea seguia en la cola,
        # o sea si el tutor **nunca llego a empezar**.
        #
        # - **Nunca empezo** → no hubo intento, no se llamo al modelo, no se
        #   gasto un token. Cobrarlo seria cobrar por trabajo que nadie empezo,
        #   asi que se devuelve.
        # - **Ya estaba corriendo** → hubo intento, y en el paso 8 ese intento ya
        #   costo dinero aunque no devolviera nada. Se queda cobrado ([D-023]).
        #
        # 🔑 Sin esta distincion, el timeout cobraba de mas: `result(timeout=)`
        # cuenta desde que se LLAMA, no desde que la tarea arranca, asi que el
        # tiempo de cola se le cargaba a quien esperaba en ella. Medido: 23
        # peticiones a la vez, 20 llegaron al tutor, **3 pagaron por nada**.
        # Ver [L-013].
        never_started = attempt.cancel()

        if never_started:
            quota.refund(user)

        logger.warning(
            "El tutor no contesto en %s segundos (usuario %s, empezo: %s)",
            TUTOR_TIMEOUT_SECONDS,
            user,
            "no" if never_started else "si",
        )
        # ⚠️ **Y una consecuencia que hay que saber, no descubrir.** Si el tutor
        # SÍ habia empezado, sigue corriendo ahi detras — y `respond` termina
        # llamando a `add_point`. O sea: **el marcador sube despues del 504**,
        # cuando quien pregunto ya se fue con un error.
        #
        # 🔑 Se deja asi a proposito. El marcador cuenta frases PRACTICADAS
        # ([A-001]), y esa se practico: el trabajo se hizo, lo unico que no
        # llego a tiempo fue la respuesta. Deshacerlo tampoco se puede de
        # verdad — habria que coordinarse con un hilo que no se controla.
        # El precio es que el numero de la pantalla se ve viejo hasta que se
        # recargue.
        raise HTTPException(status_code=504, detail=TUTOR_TIMEOUT_MESSAGE) from error
    except ScoreFileError as error:
        # El marcador roto es culpa del servidor, no de quien pregunta: 500.
        # Se traduce a HTTPException aqui, y no se deja subir, porque una
        # excepcion sin atrapar devuelve un 500 mudo — quien lo reciba no sabria
        # que el problema es el marcador. Por esto [D-006] creo una excepcion
        # propia en vez de dejar pasar la de `json`.
        #
        # El mensaje original —con la ruta del archivo— se queda en el log.
        logger.error("El marcador esta roto: %s", error)
        raise HTTPException(
            status_code=500, detail=SCORE_BROKEN_MESSAGE
        ) from error
    except Exception as error:
        # Todo lo demas. Sin este bloque, un fallo inesperado sube solo y sale
        # como un 500 mudo: quien lo recibe no sabe nada, y nadie lo apunta en
        # ninguna parte. `exception` guarda el traceback entero en el log.
        #
        # ⚠️ `Exception`, no `BaseException`: un Ctrl-C tiene que poder apagar
        # el servidor, no acabar convertido en una respuesta HTTP.
        logger.exception("Fallo inesperado atendiendo /practice")
        raise HTTPException(status_code=500, detail=UNEXPECTED_MESSAGE) from error

    return PracticeResponse(
        verdict=reply.verdict,
        words=reply.words,
        score=reply.score,
    )
