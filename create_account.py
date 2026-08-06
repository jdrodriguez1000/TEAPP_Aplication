"""Crea una cuenta desde la línea de comandos, sin pasar por `/register`.

🔑 **Esta es la contrapartida del interruptor.** Con `TEAPP_REGISTRATION_OPEN`
cerrado ([D-027]), nadie se registra por la red — y sin esta herramienta tampoco
podría hacerlo quien administra el servidor. Un freno que no deja trabajar a
nadie no se queda puesto: se quita a los tres días.

⚠️ **`main.py` ya crea cuentas, y aun así hace falta esto.** Se comprobó el
2026-08-04: `main.py` usa `getpass`, y en Windows `getpass` lee **de la consola**,
no de la entrada estándar. Con la entrada por tubería se queda colgado esperando
un teclado que no existe. Sirve para quien está sentado delante; **en un servidor
no sirve**, y en el paso 7 no hay nadie sentado delante.

🚨 **Por eso aquí no hay `input()` ni `getpass`** — es la regla 2 del proyecto.
Nada espera a un humano: el nombre llega por argumento y la contraseña por
variable de entorno.

    TEAPP_NEW_PASSWORD='la-contrasena' python create_account.py juan

⚠️ **La contraseña va por variable de entorno y no por argumento** a propósito.
Lo que se escribe como argumento queda en el historial de la terminal y lo ve
cualquiera que liste los procesos de la máquina. Y no se imprime nunca, ni
entera ni a trozos — regla 7.
"""

import os
import sys

from app import accounts
from app.config import MissingDataDirError, load_env_file
from app.tools import InvalidUserError

# De dónde se lee la contraseña. No se escribe en `.env`: se pone delante del
# comando, para esa sola corrida, y se va con ella.
PASSWORD_NAME = "TEAPP_NEW_PASSWORD"

USAGE = (
    f"Uso: {PASSWORD_NAME}='la-contrasena' python create_account.py <nombre>\n"
    "La contrasena va por variable de entorno, no como argumento: lo que se "
    "escribe como argumento queda en el historial de la terminal."
)


def main(argv: list[str], environ: dict) -> int:
    """Crea la cuenta. Devuelve 0 si salió bien y 1 si no.

    🔑 **Recibe `argv` y `environ` en vez de mirarlos por dentro**, y esa es la
    única razón por la que esto se puede probar. Leyendo `sys.argv` directamente,
    un test tendría que lanzar un proceso aparte para cada caso.
    """
    if len(argv) != 1:
        print(USAGE)
        return 1

    password = environ.get(PASSWORD_NAME, "")

    if not password:
        print(f"Falta {PASSWORD_NAME}.\n{USAGE}")
        return 1

    try:
        user = accounts.register(argv[0], password)
    except InvalidUserError as error:
        print(f"[Error] {error}")
        return 1
    except accounts.WeakPasswordError as error:
        # ⚠️ Se imprime el motivo —"necesita al menos 8 caracteres"— pero nunca
        # la contrasena. El mensaje de `accounts` ya viene escrito asi.
        print(f"[Error] {error}")
        return 1
    except accounts.UserExistsError as error:
        print(f"[Error] {error}")
        return 1
    except accounts.AccountsFileError as error:
        print(f"[Error] {error}")
        return 1
    except MissingDataDirError as error:
        # 🚨 Sin raiz de datos declarada no se escribe nada, y se dice por que.
        # Esta es LA herramienta con la que se crea la primera cuenta en el
        # servidor: si aqui se cayera con un traceback, quien administra se
        # quedaria fuera con el registro por red cerrado y sin pista. Ver [D-037].
        print(f"[Error] {error}")
        return 1

    print(f"Cuenta {user!r} creada. Ya puede entrar por /login.")
    return 0


if __name__ == "__main__":
    # 🚨 **El `.env` se carga AQUI, y hasta [D-037] no se cargaba.** Mientras las
    # rutas tenian un valor por defecto en el codigo, esta herramienta funcionaba
    # sin leerlo; desde que la raiz de los datos sale de `TEAPP_DATA_DIR`, sin
    # esta linea no encontraria las cuentas. Y es la puerta de servicio: con el
    # registro por red cerrado ([D-027]) es la unica forma de crear la primera
    # cuenta en la maquina.
    load_env_file()

    # `sys.argv[1:]` quita el nombre del propio script, que no es un argumento.
    sys.exit(main(sys.argv[1:], os.environ))
