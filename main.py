"""Puerta de entrada por la terminal.

⚠️ El ÚNICO archivo del proyecto donde puede aparecer `input()`. Todo lo demás
son funciones que reciben una frase y devuelven texto.

En el paso 2 este archivo se sustituye por FastAPI y no debe hacer falta tocar
nada más. Si algún día hay lógica aquí dentro, es que se coló donde no debía.
"""

from getpass import getpass

from app import accounts
from app.config import MissingDataDirError, load_env_file
from app.english_tutor import respond
from app.tools import InvalidUserError, ScoreFileError, normalize_user


def sign_in() -> str | None:
    """Identifica a quien practica, o devuelve `None` si no lo consigue.

    🚨 **La terminal también pide contraseña desde el paso 5**, y no es celo de
    más. `add_point` crea el marcador la primera vez, así que una terminal que
    solo preguntara el nombre fabricaría marcadores **sin credencial** — y luego
    cualquiera podría registrar ese nombre en la web y heredar sus puntos. Sería
    volver a abrir el agujero de [D-020] por la puerta de atrás.

    > 🔑 Todo marcador nace junto a su credencial. También aquí.

    `getpass` en vez de `input` para que la contraseña no se quede escrita en la
    pantalla ni en el historial de la terminal.
    """
    try:
        user = normalize_user(input("\nYour name: "))
    except InvalidUserError as error:
        # Se sale en vez de reintentar: sin un nombre valido no hay marcador al
        # que sumar, asi que no queda nada que hacer en esta corrida.
        print(f"\n[Error] {error}")
        return None

    try:
        if accounts.user_exists(user):
            if not accounts.verify(user, getpass("Password: ")):
                print("\n[Error] El nombre o la contrasena no son correctos.")
                return None
            return user

        # Nombre nuevo: se crea la cuenta aqui mismo. Es la misma cuenta que
        # sirve para entrar por el navegador — hay UN almacen de credenciales,
        # no uno por puerta.
        print(f"\n{user!r} es nuevo por aqui. Vamos a crear su cuenta.")
        accounts.register(user, getpass("New password: "))
        return user
    except (
        accounts.WeakPasswordError,
        accounts.AccountsFileError,
        # Sin raiz de datos declarada no hay cuentas que consultar. Ver [D-037].
        MissingDataDirError,
    ) as error:
        print(f"\n[Error] {error}")
        return None


def main() -> None:
    """Identifica a quien practica y luego lee frases hasta una línea vacía."""
    # Solo caracteres ASCII en lo que se imprime: la consola de Windows no
    # sabe pintar el guion largo y lo saca como "?".
    print("TEAPP - write a sentence in English.")
    print("Press Enter on an empty line to quit.")

    # La identidad se comprueba UNA vez, al principio, y vale para toda la
    # sesion. En el navegador eso lo sostiene la cookie firmada; aqui lo sostiene
    # esta variable, y se acaba al cerrar la terminal.
    user = sign_in()
    if user is None:
        return

    while True:
        sentence = input("\n> ")
        if not sentence.strip():
            print("Bye!")
            break

        # Presentar los errores SI es trabajo de este archivo: es la única
        # pieza que sabe que hay una persona mirando una pantalla. Un traceback
        # de Python no le dice nada a quien solo queria practicar ingles.
        try:
            # El tutor devuelve las tres piezas sueltas; juntarlas en un texto
            # es trabajo de aqui, porque aqui es donde hay alguien mirando. En
            # el paso 3 la pantalla juntara las mismas tres piezas a su manera.
            reply = respond(sentence, user)
            print(f"{reply.verdict}\nWords: {reply.words}\nScore: {reply.score}")
        except ScoreFileError as error:
            print(f"\n[Error] {error}")
            # Se sale: con el marcador roto, todos los intentos siguientes
            # fallarian igual. Insistir solo repetiria el mismo mensaje.
            break


if __name__ == "__main__":
    # El `.env` también aquí, por lo mismo que en `create_account.py`: desde
    # [D-037] la raíz de los datos sale de `TEAPP_DATA_DIR`, y sin cargarla esta
    # terminal no encontraría ni las cuentas ni el marcador.
    load_env_file()

    main()
