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

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from app.english_tutor import respond
from app.tools import ScoreFileError

app = FastAPI(title="TEAPP", description="Practica ingles escrito.")

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


class PracticeRequest(BaseModel):
    """Lo que se espera recibir: una frase, y nada más.

    🔑 Esto es un filtro, no un adorno. Lo que llega por la red lo escribe
    cualquiera, así que puede venir un número, un `null`, una lista o nada. Al
    declarar `sentence: str`, FastAPI rechaza todo eso ANTES de que el agente lo
    vea, y contesta un 422 explicando qué esperaba.

    Es el mismo criterio de los permisos, aplicado a los datos: **denegar por
    defecto.** Lo que no encaje con lo declarado, no entra.
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


@app.post("/practice", response_model=PracticeResponse)
def practice(request: PracticeRequest) -> PracticeResponse:
    """Recibe una frase, la pasa por el tutor y devuelve las tres piezas.

    Una sola ruta, a propósito: el paso 2 no añade funciones, solo cambia la
    puerta por la que se entra.
    """
    # Una frase vacia —o solo espacios— no es practicar ingles, y sumaria un
    # punto por nada. Se rechaza con 422, el mismo codigo que usa FastAPI
    # cuando lo que llega no encaja con lo declarado.
    if not request.sentence.strip():
        raise HTTPException(status_code=422, detail="La frase no puede estar vacia.")

    try:
        reply = respond(request.sentence)
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
