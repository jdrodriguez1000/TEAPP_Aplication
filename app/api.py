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
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from app import accounts, sessions
from app.accounts import AccountsFileError, UserExistsError, WeakPasswordError
from app.config import MissingSecretError, cookie_secure, load_env_file, log_cookie_mode
from app.english_tutor import respond
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

# 🔑 **Un solo mensaje para "no existe" y para "la contrasena no es esa".**
# Separarlos dejaria averiguar quien tiene cuenta aqui probando nombres, y eso
# ya es media respuesta para quien luego vaya a por la contrasena.
BAD_CREDENTIALS_MESSAGE = "El nombre o la contrasena no son correctos."
NOT_LOGGED_IN_MESSAGE = "Inicia sesion para practicar."

# Al arrancar queda escrito si las cookies exigen HTTPS. Sin esta linea, una
# cookie `Secure` sobre `http://localhost` se descarta en silencio y el inicio de
# sesion parece no hacer nada — un fallo mudo que se buscaria a ciegas.
log_cookie_mode()


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
    """
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


@app.post("/login", response_model=MeResponse)
def login(credentials: CredentialsRequest, response: Response) -> MeResponse:
    """Comprueba la contraseña y entrega la tarjeta."""
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
        raise HTTPException(
            status_code=401, detail=BAD_CREDENTIALS_MESSAGE
        ) from error
    except AccountsFileError as error:
        logger.error("El archivo de cuentas esta roto: %s", error)
        raise HTTPException(status_code=500, detail=ACCOUNTS_BROKEN_MESSAGE) from error

    if not correct:
        raise HTTPException(status_code=401, detail=BAD_CREDENTIALS_MESSAGE)

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

    try:
        reply = respond(body.sentence, user)
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
