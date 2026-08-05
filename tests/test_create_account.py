"""Tests de la herramienta que crea cuentas sin pasar por `/register`.

🔑 **Es la contrapartida del interruptor de [D-027].** Si esto no funciona, un
registro cerrado deja fuera también a quien administra el servidor — y entonces
el interruptor se acaba abriendo "un momentito" y ya no se cierra.

El archivo de cuentas lo desvía `conftest.py` a una carpeta temporal, así que
ningún test de aquí toca `data/accounts.json`.
"""

import create_account
from app import accounts

USER = "juan"
PASSWORD = "una-contrasena-larguisima"
PASSWORD_NAME = create_account.PASSWORD_NAME


def test_it_creates_the_account():
    assert create_account.main([USER], {PASSWORD_NAME: PASSWORD}) == 0
    assert accounts.user_exists(USER)


def test_the_account_it_creates_can_log_in():
    # 🔑 Que el archivo tenga una linea mas no prueba nada. Lo que hay que ver es
    # que la credencial SIRVE: es la misma cuenta con la que se entra por la web,
    # no una paralela.
    create_account.main([USER], {PASSWORD_NAME: PASSWORD})

    assert accounts.verify(USER, PASSWORD) is True
    assert accounts.verify(USER, "otra-cosa-larguisima") is False


def test_it_refuses_without_a_password():
    # 🚨 Sin contraseña **no se inventa una**. Una cuenta con contraseña vacia o
    # generada en silencio seria una puerta abierta que nadie recuerda haber
    # dejado abierta. Denegar por defecto, la regla 3.
    assert create_account.main([USER], {}) == 1
    assert not accounts.user_exists(USER)


def test_it_refuses_an_empty_password():
    assert create_account.main([USER], {PASSWORD_NAME: ""}) == 1
    assert not accounts.user_exists(USER)


def test_it_refuses_a_short_password():
    # El minimo de `accounts` vale igual aqui: esta puerta no es mas permisiva
    # que la otra por ser la de dentro.
    assert create_account.main([USER], {PASSWORD_NAME: "corta"}) == 1
    assert not accounts.user_exists(USER)


def test_it_refuses_an_impossible_name():
    assert create_account.main(["josé"], {PASSWORD_NAME: PASSWORD}) == 1


def test_it_refuses_a_name_that_already_exists():
    # 🚨 Es el freno de [D-020], y tiene que valer tambien por esta puerta: sin
    # el, crear una cuenta desde la terminal pisaria la credencial de alguien y
    # heredaria su marcador.
    create_account.main([USER], {PASSWORD_NAME: PASSWORD})

    assert create_account.main([USER], {PASSWORD_NAME: "otra-larguisima-aun"}) == 1
    # Y la contraseña original sigue siendo la buena.
    assert accounts.verify(USER, PASSWORD) is True


def test_it_refuses_without_a_name():
    assert create_account.main([], {PASSWORD_NAME: PASSWORD}) == 1


def test_it_refuses_more_than_one_name():
    # Dos nombres es casi siempre la contraseña puesta como argumento por error.
    # Crear la cuenta del primero y callarse dejaria la contraseña en el
    # historial de la terminal sin que nadie se enterara.
    assert create_account.main([USER, PASSWORD], {PASSWORD_NAME: PASSWORD}) == 1
    assert not accounts.user_exists(USER)


def test_the_password_is_never_printed(capsys):
    # 🚨 Regla 7 del proyecto. Se prueban los dos caminos: el que sale bien y el
    # que falla, porque los mensajes de error son justo donde se escapan estas
    # cosas.
    create_account.main([USER], {PASSWORD_NAME: PASSWORD})
    create_account.main([USER], {PASSWORD_NAME: PASSWORD})
    create_account.main(["josé"], {PASSWORD_NAME: PASSWORD})
    create_account.main([USER], {PASSWORD_NAME: "corta"})

    printed = capsys.readouterr().out

    assert PASSWORD not in printed
    assert "corta" not in printed


def test_it_does_not_wait_for_a_human():
    # 🚨 **Regla 2 del proyecto, comprobada leyendo el archivo.** En un servidor
    # no hay teclado: un `input()` o un `getpass()` aqui dejaria esta herramienta
    # colgada para siempre, que es exactamente lo que le pasa a `main.py` y la
    # razon de que esta exista ([D-027]).
    source = (
        __import__("pathlib").Path(create_account.__file__).read_text(encoding="utf-8")
    )

    # Se mira solo el CODIGO, no los comentarios: el docstring de arriba nombra
    # las dos cosas justo para explicar por que no estan. Buscarlas en el archivo
    # entero daria un falso positivo — es la leccion de [L-005].
    code = "\n".join(
        line for line in source.splitlines() if not line.strip().startswith("#")
    )
    code = code.split('"""', 2)[-1]

    assert "input(" not in code
    assert "getpass" not in code
