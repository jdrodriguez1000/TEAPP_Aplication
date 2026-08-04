"""El freno de la cuota: cuántas prácticas puede hacer cada persona al día.

🔑 **Este es el primer freno que vive en el SERVIDOR.** La pantalla ya
deshabilitaba el botón después de cada envío, y eso frena clics — pero el
navegador es de quien lo usa. Diez peticiones mandadas con `curl` no pasan por
ningún botón. **Un freno que vive en el navegador no es un freno: es una
sugerencia.** Ver [T-038].

⚠️ **El contador vive en disco, no en memoria.** Un contador en memoria se borra
en cada arranque, y en la nube del paso 7 el servidor se reinicia solo. Un tope
que se olvida al reiniciar regala cuota cada vez.

🚨 **Hoy cuenta peticiones. En el paso 8 contará dólares.** Por eso el tope entra
como parámetro y no incrustado: cambiar la unidad no puede obligar a rediseñar
esto. Ver [D-023] y [A-010].
"""

import json
import os
import tempfile
import threading
from datetime import datetime, timedelta, timezone
from pathlib import Path

from app.tools import PROJECT_ROOT, normalize_user

# Dónde vive el gasto de cada persona: `data/quota/<nombre>.json`.
#
# ⚠️ Carpeta APARTE de `data/users/`, por la misma razón que las credenciales
# viven aparte del marcador: el marcador es un logro que dura para siempre y la
# cuota es un contador que se reinicia cada día. **Dos cosas con vidas distintas
# no comparten archivo.** Si compartieran, reiniciar la cuota reescribiría el
# marcador todos los días, y un fallo de la cuota podría borrar puntos.
QUOTA_DIR = PROJECT_ROOT / "data" / "quota"

# 🚨 **La zona horaria con la que se decide qué día es hoy.** Ver [D-024].
#
# `sessions.py` mide una DURACIÓN —siete días son siete días en cualquier sitio—
# y por eso le basta un número de `time.time()`. Una cuota diaria mide un DÍA DEL
# CALENDARIO, y un día del calendario no existe sin zona horaria.
#
# Sin esta constante, el servidor del paso 7 —que corre en UTC— reiniciaría la
# cuota a las 7 de la tarde. Comprobado: el instante `2026-08-05 02:30 UTC` es
# día 5 en UTC y día 4 aquí.
#
# ⚠️ Offset fijo y no `ZoneInfo("America/Bogota")` a propósito: `ZoneInfo`
# revienta en Windows con `ZoneInfoNotFoundError` —Windows no trae la base de
# datos de zonas— y arreglarlo pide el paquete `tzdata`. Un offset fijo solo
# falla donde hay horario de verano, y en Colombia no lo hay.
QUOTA_TIMEZONE = timezone(timedelta(hours=-5))

# Cuántas prácticas al día por persona.
#
# 🔑 **Es una predicción, no un número medido** ([A-010]). Hoy el tutor es falso
# y no cuesta nada, así que no hay ninguna factura que mirar. Se comprueba en el
# paso 8, con el modelo enchufado.
DAILY_LIMIT = 20

# El candado del contador. Mismo problema y misma solución que `add_point`
# (`tools.py`): el hueco entre leer y escribir. Sin candado, dos peticiones a la
# vez leen el mismo 5, las dos escriben 6, y una práctica se cuela gratis.
#
# ⚠️ Hereda [A-002]: vale dentro de UN proceso de uvicorn.
_QUOTA_LOCK = threading.Lock()


class QuotaFileError(Exception):
    """El archivo de cuota existe, pero no se puede entender.

    Excepción propia por la misma razón que `ScoreFileError`: la puerta de red
    tiene que poder distinguir "el contador está roto" de cualquier otro fallo.
    """

    # Los mensajes van sin tildes a proposito (ver [L-001]).


class QuotaExceededError(Exception):
    """Esta persona ya gastó su cuota de hoy.

    🔑 **Lleva los datos encima, no solo un texto.** Quien la atrape necesita
    contar POR QUÉ se frenó —cuánto gastó, cuál era el tope, de qué día— sin
    tener que reconstruirlo. Un 429 sin motivo es un misterio, y el misterio se
    paga cuando alguien escribe preguntando por qué no puede practicar.
    """

    def __init__(self, user: str, used: int, limit: int, day: str) -> None:
        self.user = user
        self.used = used
        self.limit = limit
        self.day = day
        super().__init__(
            f"{user} ya gasto su cuota del {day}: {used} de {limit} practicas."
        )


def today(now: datetime | None = None) -> str:
    """Devuelve el día de hoy como texto, en la zona de la cuota.

    🚨 **El `now` es un parámetro, y esa es la única forma de probar esto.** Un
    tope por día no se puede ver funcionar en una corrida: nadie va a esperar a
    mañana. Si esta función llamara al reloj por dentro, el freno se quedaría sin
    testigo. Es lo mismo que hace `sessions.issue(now=...)` para poder probar la
    caducidad de una sesión.

    ⚠️ **Y el `now` tiene que traer zona horaria.** Un `datetime` sin zona no
    sabe qué día es en ningún sitio concreto: Python se lo cree como si fuera
    hora local de la máquina, que en la nube es UTC y aquí no.

    :raises ValueError: si el `datetime` que llega no trae zona horaria.
    """
    moment = datetime.now(QUOTA_TIMEZONE) if now is None else now

    if moment.tzinfo is None:
        raise ValueError(
            "El 'now' de la cuota tiene que traer zona horaria. Un datetime sin "
            "zona no sabe que dia es: en la nube seria UTC y en local seria otro."
        )

    return moment.astimezone(QUOTA_TIMEZONE).date().isoformat()


def quota_file(name: str, quota_dir: Path | None = None) -> Path:
    """Devuelve el archivo de cuota de una persona.

    Valida el nombre aquí dentro, igual que `score_file`, porque es quien toca el
    disco: si algún día la llama alguien que se saltó el filtro de la puerta,
    tiene que negarse igual. **El olvido tiene que fallar hacia el lado seguro.**

    🚨 **El valor por defecto se resuelve AQUÍ DENTRO, no en la firma.** Escribir
    `quota_dir: Path = QUOTA_DIR` parece lo mismo y no lo es: Python evalúa los
    valores por defecto **una sola vez, al importar el módulo**, y se queda con
    la carpeta de aquel momento para siempre. Los tests desvían `QUOTA_DIR` a una
    carpeta temporal, y con la firma de antes el desvío no serviría de nada:
    seguirían escribiendo en `data/quota/` de verdad. Con `None` se pregunta en
    cada llamada, y el desvío funciona.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    """
    directory = QUOTA_DIR if quota_dir is None else quota_dir
    return directory / f"{normalize_user(name)}.json"


def _usage_on(path: Path, day: str) -> int:
    """Lo gastado en `path`, si el archivo es de `day`. Si es de otro día, 0.

    🚨 **El día llega por parámetro, y no se pregunta aquí.** Esa es la
    diferencia que arregla la carrera de medianoche: quien llame decide UNA VEZ
    qué día es, y esta función usa ese, no otro que pudo haber cambiado por el
    camino. Ver [L-013].
    """
    if not path.exists():
        return 0

    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise QuotaFileError(
            f"El contador de cuota {path} no es un JSON valido ({error}). "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        ) from error

    if not isinstance(saved, dict) or "day" not in saved or "used" not in saved:
        raise QuotaFileError(
            f"El contador de cuota {path} no tiene las claves 'day' y 'used'. "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        )

    used = saved["used"]

    # `isinstance(True, int)` vale True en Python: `bool` hereda de `int`. Sin
    # descartarlo, un {"used": true} pasaria por un 1 perfectamente valido.
    if not isinstance(used, int) or isinstance(used, bool) or used < 0:
        raise QuotaFileError(
            f"El contador de cuota {path} guarda {used!r}, que no es un numero "
            "entero positivo. No se ha tocado el archivo: revisalo o borralo."
        )

    # El archivo es de otro dia: lo de ayer no cuenta contra lo de hoy.
    if saved["day"] != day:
        return 0

    return used


def _write_usage(path: Path, day: str, used: int) -> None:
    """Deja `{"day": ..., "used": ...}` en el archivo, sin dejarlo nunca a medias.

    Se escribe al lado y se renombra encima. Renombrar es UNA operacion del
    sistema: o pasa entera o no pasa. `write_text` dejaria una ventana con el
    archivo vacio, y un corte justo ahi lo rompe.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    # Cada escritura estrena su propio temporal: con un nombre fijo, dos
    # escrituras a la vez se lo quitan de las manos y Windows corta en seco con
    # un "Acceso denegado" ([T-021]).
    handle, temporary_name = tempfile.mkstemp(
        dir=path.parent, prefix=f"{path.name}.", suffix=".tmp"
    )
    temporary = Path(temporary_name)

    try:
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            file.write(json.dumps({"day": day, "used": used}))

        # `os.replace` pisa el destino aunque exista, igual en Windows que en
        # Linux. `Path.rename` revienta en Windows si el destino ya esta.
        os.replace(temporary, path)
    except BaseException:
        # `BaseException` y no `Exception` para que un Ctrl-C tambien limpie.
        temporary.unlink(missing_ok=True)
        raise


def read_usage(
    name: str, now: datetime | None = None, quota_dir: Path | None = None
) -> int:
    """Cuánto lleva gastado hoy esta persona. Si el archivo es de ayer, 0.

    🔑 **Aquí está el truco que hace que esto no necesite mantenimiento.** El
    archivo guarda el día junto al gasto:

        {"day": "2026-08-04", "used": 3}

    Si el día guardado no es el de hoy, el gasto se ignora y vale 0. **Nadie
    tiene que barrer los contadores de madrugada**: no hay tarea programada, no
    hay proceso que despierte a medianoche. El reinicio ocurre solo, en el
    momento en que esa persona vuelve.

    ⚠️ **Un archivo roto NO devuelve 0.** Devolver 0 en silencio sería regalar
    la cuota entera justo cuando el freno está averiado — el fallo caería del
    lado inseguro. Se avisa con `QuotaFileError`, y la puerta contesta un error.
    Es la regla 3 del proyecto: **denegar por defecto**.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises QuotaFileError: si el archivo existe pero no se puede interpretar.
    """
    return _usage_on(quota_file(name, quota_dir), today(now))


def spend(
    name: str,
    now: datetime | None = None,
    limit: int | None = None,
    quota_dir: Path | None = None,
) -> int:
    """Gasta una práctica de la cuota de hoy y devuelve cuánto lleva gastado.

    🚨 **Se llama ANTES de trabajar, no después.** Hoy da igual, porque el tutor
    falso no falla nunca. En el paso 8 sí importa: una llamada al modelo que
    gasta tokens y luego revienta se colaría **gratis** si el contador subiera al
    final. 🔑 Lo que se cobra es **haber intentado**, porque intentar es lo que
    cuesta dinero.

    El `limit` es un parámetro por dos razones. La primera, probar: con el tope
    incrustado en 20, ver el freno morder costaría 21 peticiones en cada test;
    con el tope inyectado, un test pone 1 y lo ve morder a la segunda. La
    segunda, que 20 es una predicción sin medir ([A-010]) y cambiarla no puede
    costar una reescritura.

    ⚠️ Y por eso llega como `None`, igual que `quota_dir`: escribir
    `limit: int = DAILY_LIMIT` en la firma congelaría el 20 al importar el
    módulo, y desviar `DAILY_LIMIT` desde un test no cambiaría nada.

    🔑 **El candado abarca leer Y escribir**, igual que en `add_point`. El
    problema no está en escribir: está en el hueco entre leer y escribir. Si dos
    peticiones leen el mismo 19, las dos se creen dentro del tope y las dos pasan
    — el freno tendría un agujero del tamaño de las peticiones simultáneas.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises QuotaFileError: si el archivo existe pero no se puede interpretar.
    :raises QuotaExceededError: si ya no queda cuota. El archivo no se toca.
    """
    path = quota_file(name, quota_dir)
    ceiling = DAILY_LIMIT if limit is None else limit

    # 🚨 **El día se pregunta UNA sola vez, y se usa para todo lo que sigue.**
    #
    # Antes se preguntaba dos veces —aquí y otra vez dentro de `read_usage`— y
    # entre las dos cabía la medianoche. Cuando cabía, el resultado era este:
    # se comprobaba contra el día NUEVO (limpio, así que pasaba) y se escribía
    # bajo el día VIEJO, borrando lo gastado ese día. **Cuota gratis.**
    #
    # 🔑 No es un caso raro que se pueda ignorar: pasa una vez al día, y
    # justamente a quien esté practicando a esa hora. Ver [L-013].
    day = today(now)

    with _QUOTA_LOCK:
        used = _usage_on(path, day)

        if used >= ceiling:
            # 🔑 Se sale ANTES de escribir. Si el contador siguiera subiendo con
            # el freno puesto, el numero dejaria de significar "practicas hechas"
            # y pasaria a significar "veces que lo intento" — y quien mirara el
            # archivo para entender el 429 leeria un dato que no es.
            raise QuotaExceededError(
                user=normalize_user(name), used=used, limit=ceiling, day=day
            )

        used += 1
        _write_usage(path, day, used)

        return used


def refund(name: str, now: datetime | None = None, quota_dir: Path | None = None) -> int:
    """Devuelve una práctica cobrada que **nunca llegó a empezar**.

    🚨 **Esto no contradice "se cobra el intento", lo completa.** Se cobra por
    intentar porque intentar cuesta dinero. Pero una petición que se quedó
    **esperando cola** y se cortó antes de arrancar no intentó nada: no llamó al
    modelo, no gastó un token. Cobrarla es cobrar por trabajo que nadie empezó.

    Ese caso existe de verdad y se midió (2026-08-04): 23 peticiones simultáneas
    contra un tutor colgado y un pool de 20 → **20 llegaron al tutor y 3
    pagaron un 504 por nada**. Ver [L-013].

    ⚠️ **Solo la llama quien SABE que el trabajo no empezó.** En `api.py` ese
    saber viene de `future.cancel()`, que devuelve `True` únicamente si la tarea
    seguía en la cola. Si ya estaba corriendo, no se devuelve nada: ahí sí hubo
    intento.

    Devolver de más sería peor que no devolver: regalaría cuota.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises QuotaFileError: si el archivo existe pero no se puede interpretar.
    """
    path = quota_file(name, quota_dir)
    day = today(now)

    with _QUOTA_LOCK:
        used = _usage_on(path, day)

        # Si no hay nada gastado hoy, no hay nada que devolver. Puede pasar si la
        # medianoche cayo entre el cobro y la devolucion: lo cobrado es de ayer y
        # ya no cuenta contra nadie. Bajar a -1 seria inventar cuota.
        if used <= 0:
            return 0

        used -= 1
        _write_usage(path, day, used)

        return used
