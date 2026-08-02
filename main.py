"""Puerta de entrada por la terminal.

⚠️ El ÚNICO archivo del proyecto donde puede aparecer `input()`. Todo lo demás
son funciones que reciben una frase y devuelven texto.

En el paso 2 este archivo se sustituye por FastAPI y no debe hacer falta tocar
nada más. Si algún día hay lógica aquí dentro, es que se coló donde no debía.
"""

from app.english_tutor import respond


def main() -> None:
    """Lee frases del teclado hasta que se escriba una línea vacía."""
    # Solo caracteres ASCII en lo que se imprime: la consola de Windows no
    # sabe pintar el guion largo y lo saca como "?".
    print("TEAPP - write a sentence in English.")
    print("Press Enter on an empty line to quit.")

    while True:
        sentence = input("\n> ")
        if not sentence.strip():
            print("Bye!")
            break
        print(respond(sentence))


if __name__ == "__main__":
    main()
