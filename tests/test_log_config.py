"""Tests del log configurado — [T-033].

🚨 **Este archivo existe por [L-012], y es el que sostiene a los demás.**

Dos veces se escribió un `logger.info(...)`, su test dio verde, y en el servidor
de verdad el renglón **no salía**: sin log configurado actúa el handler de último
recurso de Python, que empieza en `WARNING`. Un `info` no se perdía por poco, no
existía.

🔑 **Y el test que fallaba lo hacía de la peor manera: se aprobaba a sí mismo.**
`caplog.at_level(INFO)` baja el listón del logger para ese test — o sea que el
test creaba las condiciones que hacían visible el renglón y luego comprobaba que
era visible.

⚠️ **Por eso aquí se mide en OTRO PROCESO, y no con `caplog`.**

Se intentó primero dentro de pytest, vaciando los handlers del logger raíz en un
fixture. **No funcionó, y falló en silencio:** `caplog` vuelve a instalar el suyo
**después** de los fixtures, así que cuando corría el test el raíz volvía a tener
handlers — y `basicConfig` no hace nada si el raíz ya tiene handlers. El test
medía el estado que había puesto pytest y lo llamaba "lo que hace
`configure_logging`". Era la trampa de [L-012] con otra ropa.

🔑 **Un intérprete recién arrancado es la única condición honesta**, porque es
exactamente la de uvicorn: raíz limpia, nada configurado, nadie escuchando.
"""

import json
import subprocess
import sys

import pytest

from app import config

# El proyecto entero, para que el proceso hijo encuentre `app`.
PROJECT_ROOT = config.PROJECT_ROOT


def in_a_fresh_interpreter(code: str, extra_env: dict | None = None) -> str:
    """Corre `code` en un Python nuevo y devuelve lo que imprimió.

    🚨 **No sale a la red** — [C-001] sigue en pie. Arranca el mismo intérprete
    que está corriendo la suite (`sys.executable`), sin instalar nada.

    ⚠️ El portero de red de `tests/no_network.py` **no ve los subprocesos**, y ya
    está escrito allí. Lo que se ejecuta aquí es código de este archivo, a la
    vista, y no toca nada de fuera.
    """
    environment = {"PATH": "", "SYSTEMROOT": ""}

    # Se hereda lo imprescindible de Windows y nada mas: un entorno heredado
    # entero podria traer un TEAPP_LOG_LEVEL puesto en la maquina de quien corre
    # la suite, y el test dependeria de su `.env` en vez de medir la funcion.
    import os

    for name in ("PATH", "SYSTEMROOT", "PATHEXT", "TEMP"):
        if name in os.environ:
            environment[name] = os.environ[name]

    if extra_env:
        environment.update(extra_env)

    finished = subprocess.run(
        [sys.executable, "-c", code],
        cwd=PROJECT_ROOT,
        env=environment,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert finished.returncode == 0, finished.stderr

    return finished.stdout.strip()


# Lo que se le pregunta al proceso nuevo: ¿qué niveles pasan, y cuántos handlers
# quedan? `CONFIGURE` se sustituye por la llamada, o por nada.
PROBE = """
import json, logging
from app import config
CONFIGURE
log = logging.getLogger("app.api")
print(json.dumps({
    "info": log.isEnabledFor(logging.INFO),
    "warning": log.isEnabledFor(logging.WARNING),
    "handlers": len(logging.getLogger().handlers),
}))
"""


def probe(configure: bool, extra_env: dict | None = None) -> dict:
    """Pregunta a un intérprete nuevo qué se ve, con y sin configurar."""
    code = PROBE.replace(
        "CONFIGURE", "config.configure_logging()" if configure else ""
    )
    return json.loads(in_a_fresh_interpreter(code, extra_env))


def test_the_configured_log_makes_info_visible():
    # 🚨 **Este es EL test.** Es el que hace legítimo que `app/api.py` y
    # `app/config.py` escriban con `info` en vez de con `warning`. Si esto se
    # pone rojo, esos renglones han vuelto a ser invisibles y hay que subirlos.
    assert probe(configure=True)["info"] is True


def test_without_configuring_the_log_info_does_not_exist():
    # 🔑 **La otra mitad, y sin ella la de arriba no prueba nada.** Un test que
    # solo mira el estado bueno no distingue "lo arreglé" de "esto ya estaba
    # así". Aquí se ve el mundo de antes de [T-033], medido y no contado: sin
    # configurar, `warning` pasa e `info` NO. Eso es lo que costó dos renglones
    # mudos en uvicorn.
    without = probe(configure=False)

    assert without["warning"] is True
    assert without["info"] is False


def test_the_level_can_be_lowered_from_the_environment():
    # En la nube puede interesar WARNING para no pagar por guardar ruido.
    quiet = probe(configure=True, extra_env={config.LOG_LEVEL_NAME: "WARNING"})

    assert quiet["warning"] is True
    assert quiet["info"] is False


def test_configuring_twice_does_not_pile_up_handlers():
    # ⚠️ Un handler de mas significa cada renglon impreso dos veces.
    code = PROBE.replace(
        "CONFIGURE", "config.configure_logging()\nconfig.configure_logging()"
    )

    assert json.loads(in_a_fresh_interpreter(code))["handlers"] == 1


def test_the_line_carries_the_time_the_level_and_the_origin():
    # 🔑 Las tres cosas que pedía [T-033], vistas en un renglón de verdad escrito
    # por un servidor de verdad — no leyendo la cadena del formato. Lo que
    # importa es lo que acaba escrito, no lo que se pidió que se escribiera.
    line = in_a_fresh_interpreter(
        """
import logging, sys
from app import config
config.configure_logging()
# El handler de `basicConfig` escribe en stderr; se desvia a stdout para leerlo.
logging.getLogger().handlers[0].stream = sys.stdout
logging.getLogger("app.quota").warning("el contador esta roto")
"""
    )

    assert "WARNING" in line  # el nivel
    assert "app.quota" in line  # el origen
    assert "el contador esta roto" in line  # el mensaje

    # Y la hora delante, con la forma de `LOG_DATE_FORMAT`: 2026-08-04 19:45:50
    stamp = line[:19]
    assert stamp.count(":") == 2
    assert stamp[:10].count("-") == 2


@pytest.mark.parametrize("piece", ["asctime", "levelname", "name", "message"])
def test_the_format_names_the_four_pieces(piece):
    # Barato y complementario: si alguien quita una pieza del formato, este test
    # dice CUAL falta. El de arriba solo diria que el renglon salio raro.
    assert f"%({piece})" in config.LOG_FORMAT
