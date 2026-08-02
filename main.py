"""Puerta de entrada por la terminal.

⚠️ El ÚNICO archivo del proyecto donde puede aparecer `input()`. Todo lo demás
son funciones que reciben una frase y devuelven texto.

En el paso 2 este archivo se sustituye por FastAPI y no debe hacer falta tocar
nada más. Si algún día hay lógica aquí dentro, es que se coló donde no debía.
"""

from app.english_tutor import respond
from app.tools import ScoreFileError


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

        # Presentar los errores SI es trabajo de este archivo: es la única
        # pieza que sabe que hay una persona mirando una pantalla. Un traceback
        # de Python no le dice nada a quien solo queria practicar ingles.
        try:
            # El tutor devuelve las tres piezas sueltas; juntarlas en un texto
            # es trabajo de aqui, porque aqui es donde hay alguien mirando. En
            # el paso 3 la pantalla juntara las mismas tres piezas a su manera.
            reply = respond(sentence)
            print(f"{reply.verdict}\nWords: {reply.words}\nScore: {reply.score}")
        except ScoreFileError as error:
            print(f"\n[Error] {error}")
            # Se sale: con el marcador roto, todos los intentos siguientes
            # fallarian igual. Insistir solo repetiria el mismo mensaje.
            break


if __name__ == "__main__":
    main()
