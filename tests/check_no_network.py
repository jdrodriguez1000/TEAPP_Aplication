"""Los controles del portero: comprueban que el portero de verdad muerde.

🔑 **Sin este archivo, el verde de la suite no demuestra nada.** Si el portero
se rompe en silencio, los 192 tests siguen pasando exactamente igual — porque
ninguno intenta salir a internet. El verde de la suite dice "nadie salio"; solo
estos controles dicen "y si alguien lo intentara, se le veria".

⚠️ **A proposito NO se llama `test_*.py`**, asi que `python -m pytest` no lo
recoge. Estos controles salen a internet de verdad si el portero falla, y eso
es justo lo que `C-001` prohibe: no pueden correr en cada corrida normal.

Para reverificar el portero, se piden por su nombre:

    python -m pytest tests/check_no_network.py -v

Verde = el portero muerde. Rojo = el portero esta roto y hay que arreglarlo
antes de creerse ningun otro verde de la suite.
"""

import socket
import urllib.request

import pytest

from no_network import NetworkTouched

# Un servidor de fuera cualquiera, solo para que el portero tenga a quien parar.
OUTSIDE_HOST = "example.com"
OUTSIDE_IP = "1.1.1.1"


def test_the_doorman_stops_connect():
    """La salida normal."""
    s = socket.socket()
    s.settimeout(5)
    with pytest.raises(NetworkTouched):
        s.connect((OUTSIDE_HOST, 80))
    s.close()


def test_the_doorman_stops_connect_ex():
    """La puerta de atras: `connect_ex` devuelve un codigo, no lanza error.

    Va con IP literal y no con nombre **a proposito**: asi no pasa por
    `getaddrinfo`, y si este control se pone verde es porque muerde el parche
    de `connect_ex`, no otro. Con un nombre, el control mentiria.
    """
    s = socket.socket()
    s.settimeout(5)
    with pytest.raises(NetworkTouched):
        s.connect_ex((OUTSIDE_IP, 80))
    s.close()


def test_the_doorman_stops_name_lookup():
    """Traducir un nombre a numeros tampoco funciona sin red."""
    with pytest.raises(NetworkTouched):
        socket.getaddrinfo(OUTSIDE_HOST, 80)


def test_the_doorman_stops_a_normal_http_request():
    """Lo que haria de verdad un cliente de API: una peticion HTTP corriente."""
    with pytest.raises(NetworkTouched):
        urllib.request.urlopen(f"http://{OUTSIDE_HOST}", timeout=5).read()


def test_the_doorman_lets_the_machine_talk_to_itself():
    """Y el portero no puede pasarse de listo: `127.0.0.1` tiene que pasar.

    Si bloqueara tambien lo local, `TestClient` y cualquier servidor de prueba
    dejarian de funcionar, y el portero seria inservible.
    """
    assert socket.getaddrinfo("127.0.0.1", 80)
