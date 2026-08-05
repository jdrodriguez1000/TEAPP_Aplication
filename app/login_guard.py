"""El freno de los intentos: cuántas veces se puede fallar la contraseña.

🔑 **Parece la cuota y no lo es.** `quota.py` protege **la factura** y cuenta a
quien ya demostró quién es. Esto protege **las contraseñas**, y tiene que contar
a quien **todavía no** ha demostrado nada — la persona es justo lo que está en
duda. Por eso se cuenta por **origen de la petición**, que es otro dato y otra
estructura. Ver [D-025] y [D-026].

⚠️ **Y aquí el contador vive en MEMORIA, al revés que la cuota.** No es un
descuido: son dos cosas con vidas distintas.

- La cuota dura **un día entero**. Un reinicio a media tarde regala medio día de
  gasto real, y en la nube el servidor se reinicia solo.
- Esto dura **una ventana corta**. Un reinicio le devuelve los intentos a quien
  esté probando contraseñas, pero él no puede provocar el reinicio: le tocaría
  de casualidad.

🚨 **Y en disco habría una palanca que aquí no existe.** Escribir en disco cada
intento fallido pone en manos de quien ataca **cuántas veces escribe el
servidor**. Es el mismo problema que [C-002]: quien manda decide lo que cuesta
atenderle. En memoria, fallar no cuesta un archivo.

🚨 **Hereda [A-002], y de la forma más incómoda.** Un `dict` de Python solo lo ve
**su propio proceso**. Dos procesos de uvicorn son dos contadores que no se
enteran el uno del otro, y entonces el tope real es el doble del escrito. Hoy se
arranca un proceso; el día que se arranquen dos, este freno se afloja **en
silencio**.

⚠️ **Este módulo caduca en el despliegue**, y son tres cosas las que caducan a la
vez, no una:

- **El reinicio que no importa** y **el proceso único**, las dos razones de
  arriba: valen mientras esto corra en una máquina de casa.
- **Que la dirección que se lee sea la de quien pregunta** ([A-014]). Detrás de
  un proxy, todo el mundo llega con la misma y este freno deja fuera a todos a la
  vez. Ver [T-055].
- **Que los números sean los correctos** ([A-013]): 5 y 900 son predicción, no
  medida.

🔑 Aquí vivía una cuarta —*"nadie va a probar contraseñas a la fuerza"*, la vieja
`A-012`—. Esa **se murió el día que se escribió este archivo**: ya no hace falta
suponerla. Las otras tres siguen vivas. Ver [L-014].
"""

import threading
import time

# Cuántos fallos seguidos se aguantan desde un mismo origen antes de cerrar.
#
# 🔑 **Es una predicción, no un número medido** ([A-013]), igual que
# `DAILY_LIMIT`. Aquí no hay nada que cronometrar: nadie ha atacado esto todavía.
# Cinco deja sitio a quien se equivoca de verdad —una contraseña vieja, un dedo
# torcido— y corta muy por debajo de lo que necesita quien prueba a la fuerza.
MAX_FAILED_ATTEMPTS = 5

# Cuánto dura el castigo, y también cuánto se recuerda un fallo.
#
# 🔑 **Un solo número para las dos cosas, a propósito.** Es lo que hace que esto
# no necesite ni una tarea que desbloquee ni nadie que perdone: los fallos se
# olvidan por viejos, y cuando el último se olvida el origen queda libre solo.
LOCKOUT_WINDOW_SECONDS = 15 * 60

# Cuándo falló cada origen: `{"1.2.3.4": [1754300000.0, 1754300012.0]}`.
#
# ⚠️ **Se guardan los INSTANTES, no un número de fallos.** Con un contador a
# secas habría que decidir cuándo ponerlo a cero, y eso pide un reloj aparte que
# lo haga. Con los instantes, "cuántos fallos hay ahora" se calcula mirando
# cuáles siguen dentro de la ventana: no hay nada que reiniciar.
_ATTEMPTS: dict[str, list[float]] = {}

# El candado del contador. Mismo problema que en `quota.py`: el hueco entre leer
# y escribir. Sin candado, dos intentos a la vez leen los mismos 4 fallos, los
# dos se creen dentro del tope y los dos pasan.
_ATTEMPTS_LOCK = threading.Lock()

# Cuando no se sabe de dónde viene la petición. Todas las de origen desconocido
# comparten cubo, y eso es lo correcto: **denegar por defecto**. Repartirlas
# —dejar pasar lo que no se sabe de dónde viene— sería regalar la puerta de atrás.
UNKNOWN_ORIGIN = "desconocido"


class TooManyAttemptsError(Exception):
    """Este origen ya falló demasiadas veces y está cerrado un rato.

    🔑 **Lleva los datos encima**, por la misma razón que `QuotaExceededError`:
    quien la atrape necesita contar POR QUÉ se frenó y **cuánto falta** para
    poder volver, sin tener que reconstruirlo.
    """

    # Los mensajes van sin tildes a proposito (ver [L-001]).

    def __init__(
        self, origin: str, attempts: int, limit: int, retry_after: int
    ) -> None:
        self.origin = origin
        self.attempts = attempts
        self.limit = limit
        self.retry_after = retry_after
        super().__init__(
            f"El origen {origin} lleva {attempts} fallos de {limit}. "
            f"Vuelve a intentarlo en {retry_after} segundos."
        )


def _recent(stamps: list[float], moment: float) -> list[float]:
    """Los fallos que todavía cuentan: los de dentro de la ventana."""
    cutoff = moment - LOCKOUT_WINDOW_SECONDS
    return [stamp for stamp in stamps if stamp > cutoff]


def _sweep_locked(moment: float) -> int:
    """Barre lo vencido. Devuelve cuántos orígenes se fueron enteros.

    🚨 **Sin este barrido, la palanca del disco reaparece como memoria.** Quien
    ataque desde mil direcciones distintas deja mil entradas en el `dict`, y
    ninguna se iría nunca: el freno que evita escribir en disco acabaría
    llenando la memoria, que es peor porque no avisa hasta que revienta.

    ⚠️ El nombre lleva `_locked` porque **da por hecho que el candado ya está
    tomado**. Quien lo llame sin él tiene una carrera. `sweep()` es la versión
    de fuera.
    """
    emptied = []

    for origin, stamps in _ATTEMPTS.items():
        alive = _recent(stamps, moment)

        if alive:
            _ATTEMPTS[origin] = alive
        else:
            # No se borra aqui dentro: cambiar el `dict` mientras se recorre lo
            # rompe en marcha. Se apunta y se borra despues.
            emptied.append(origin)

    for origin in emptied:
        del _ATTEMPTS[origin]

    return len(emptied)


def sweep(now: float | None = None) -> int:
    """Barre los orígenes cuyos fallos ya caducaron. Devuelve cuántos se fueron."""
    moment = time.time() if now is None else now

    with _ATTEMPTS_LOCK:
        return _sweep_locked(moment)


def tracked_origins() -> int:
    """Cuántos orígenes se están recordando ahora mismo.

    🔑 **Existe para que el barrido tenga testigo.** Un barrido que no se puede
    mirar desde fuera es una promesa, no un freno: el test tendría que hurgar en
    `_ATTEMPTS`, y entonces estaría probando cómo está hecho esto por dentro en
    vez de lo que hace.

    Es también el número que hay que mirar el día que se sospeche que este
    módulo se está comiendo la memoria.
    """
    with _ATTEMPTS_LOCK:
        return len(_ATTEMPTS)


def check(origin: str, now: float | None = None, limit: int | None = None) -> None:
    """Deja pasar, o se niega porque este origen ya falló demasiado.

    🚨 **Se llama ANTES de mirar la contraseña.** Comprobar primero y frenar
    después dejaría que cada intento siguiera costando un `scrypt` entero
    —que es lento a propósito ([D-021])— y el freno no ahorraría nada.

    El `limit` entra por parámetro por lo mismo que en `quota.spend`: con el tope
    incrustado en 5, ver el freno morder costaría seis peticiones en cada test.

    ⚠️ Y llega como `None`, no como `limit: int = MAX_FAILED_ATTEMPTS`: un valor
    por defecto en la firma se evalúa **al importar el módulo** y congelaría el 5
    para siempre, así que desviarlo desde un test no cambiaría nada.

    :raises TooManyAttemptsError: si este origen está cerrado ahora mismo.
    """
    moment = time.time() if now is None else now
    ceiling = MAX_FAILED_ATTEMPTS if limit is None else limit

    with _ATTEMPTS_LOCK:
        recent = _recent(_ATTEMPTS.get(origin, []), moment)

        if len(recent) < ceiling:
            return

        # Cuánto falta: lo que le queda de ventana al fallo MÁS VIEJO de los que
        # cuentan. Cuando ese caduque habrá un hueco libre y se podrá reintentar.
        retry_after = int(min(recent) + LOCKOUT_WINDOW_SECONDS - moment) + 1

        raise TooManyAttemptsError(
            origin=origin,
            attempts=len(recent),
            limit=ceiling,
            retry_after=retry_after,
        )


def record_failure(origin: str, now: float | None = None) -> int:
    """Apunta un fallo de este origen y devuelve cuántos lleva en la ventana.

    🔑 **El barrido va aquí**, y no en un reloj aparte, porque este es el **único
    sitio donde el `dict` crece**. Lo que crece es lo que limpia: así el barrido
    no puede quedarse sin ejecutar por mucho tiempo, que es lo que le pasa a toda
    limpieza que depende de que alguien se acuerde de llamarla.

    ⚠️ El barrido recorre el `dict` entero en cada fallo. Con los tamaños de este
    proyecto no se nota, y a cambio no hay ningún hilo de mantenimiento que
    escribir, arrancar y apagar. Si algún día se notara, aquí está el sitio.
    """
    moment = time.time() if now is None else now

    with _ATTEMPTS_LOCK:
        _sweep_locked(moment)

        stamps = _ATTEMPTS.setdefault(origin, [])
        stamps.append(moment)

        return len(stamps)


def clear(origin: str) -> None:
    """Olvida los fallos de este origen. Se llama cuando alguien acierta.

    🔑 **Acertar borra la cuenta entera**, y eso es lo que hace que este freno no
    moleste a quien no está atacando. Alguien que falla cuatro veces recordando
    su contraseña y entra a la quinta vuelve a empezar de cero: no arrastra un
    castigo por haberse acercado al tope.

    ⚠️ **Lo que esto NO hace:** perdonar a los demás. El origen es compartido —una
    casa entera sale por la misma dirección—, así que un acierto de alguien limpia
    los fallos de todos los que salgan por ahí. Se acepta a propósito: la
    alternativa es contar por persona, y la persona es justo lo que no se sabe
    todavía ([D-025]).
    """
    with _ATTEMPTS_LOCK:
        _ATTEMPTS.pop(origin, None)
