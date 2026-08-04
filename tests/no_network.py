"""El portero de red: vigila que la suite no salga a internet (`C-001`).

Piensa en la puerta de salida de Python hacia fuera de la maquina. Este modulo
pone un portero ahi: todo lo que intente salir se para y grita `NetworkTouched`.
Hablar consigo mismo (`127.0.0.1`) sigue pasando, igual que cuando apagas el
WiFi y el ordenador se sigue oyendo a si mismo.

Se enchufa solo, en `conftest.py`, para TODOS los tests. 🔑 Un vigia que hay que
acordarse de encender es un vigia que algun dia no esta.

## 🚨 Lo que este portero NO puede ver

**Los subprocesos.** `node`, `git`, `npx` o `curl` son OTRO proceso, con su
propio Python — o sin Python ninguno. Este portero solo parchea el `socket` de
ESTE proceso, asi que un subproceso sale a internet por delante de sus narices
y el portero ni se entera. No es un descuido que se pueda arreglar: es como
esta construido.

Consecuencia directa: **la mitad "cierre" de `C-001` no la mide este portero, y
no la medira nunca.** Que `protocol-close` no baje nada de internet se comprueba
a mano — mirando que `node_modules/typescript/` este en disco y que en el
protocolo no aparezca `npx` (ver `D-017`).

## Por que hay tres puertas y no una

- `connect` — la salida normal. Lanza error si no puede.
- `connect_ex` — la misma salida, pero **devuelve un codigo en vez de lanzar**.
  Es la puerta de atras: sin parchearla, el portero se atraviesa entero.
- `getaddrinfo` — traducir un nombre (`example.com`) a numeros. Sin red no
  funciona, asi que bloquearlo imita mejor la maquina desconectada de verdad.

Para comprobar que el portero sigue mordiendo: `tests/check_no_network.py`.
"""

import socket

# Lo que sigue permitido: hablar consigo mismo.
LOCAL = {"127.0.0.1", "::1", "localhost", "", None}


class NetworkTouched(Exception):
    """Algo intento salir a internet. La restriccion `C-001` esta rota."""


def _host_of(address):
    """El destino, venga como tupla `(host, puerto)` o como texto suelto."""
    return address[0] if isinstance(address, tuple) else address


def install(monkeypatch):
    """Pone el portero en las tres puertas.

    `monkeypatch` lo quita solo al acabar cada test: no hace falta desmontarlo
    a mano, y ningun test puede dejarlo puesto para el siguiente.
    """
    real_connect = socket.socket.connect
    real_connect_ex = socket.socket.connect_ex
    real_getaddrinfo = socket.getaddrinfo

    def blocked_connect(self, address, *args, **kwargs):
        if _host_of(address) in LOCAL:
            return real_connect(self, address, *args, **kwargs)
        raise NetworkTouched(f"intento de conexion a {address!r}")

    def blocked_connect_ex(self, address, *args, **kwargs):
        if _host_of(address) in LOCAL:
            return real_connect_ex(self, address, *args, **kwargs)
        raise NetworkTouched(f"intento de conexion (connect_ex) a {address!r}")

    def blocked_getaddrinfo(host, *args, **kwargs):
        if host in LOCAL:
            return real_getaddrinfo(host, *args, **kwargs)
        raise NetworkTouched(f"intento de resolver el nombre {host!r}")

    monkeypatch.setattr(socket.socket, "connect", blocked_connect)
    monkeypatch.setattr(socket.socket, "connect_ex", blocked_connect_ex)
    monkeypatch.setattr(socket, "getaddrinfo", blocked_getaddrinfo)
