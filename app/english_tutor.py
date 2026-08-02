"""El agente. Falso por ahora: decide siempre la misma secuencia.

Un agente de verdad elige qué herramientas usar y en qué orden. Este todavía no
elige: llama a las tres, siempre, en el mismo orden. Eso basta para montar y
probar toda la tubería alrededor sin gastar un centavo.
"""

from app.tools import add_point, count_words, judge_grammar


def respond(sentence: str) -> str:
    """Recibe una frase en inglés y devuelve la respuesta del tutor.

    🔑 Esta función es el enchufe del proyecto. Entra un texto, sale un texto,
    y nada más. Hoy la llama `main.py` desde la terminal; en el paso 2 la
    llamará FastAPI desde internet. La función no se entera del cambio, y por
    eso `main.py` puede desaparecer entero sin arrastrar nada consigo.
    """
    words = count_words(sentence)
    verdict = judge_grammar(sentence)
    total = add_point()

    return f"{verdict}\nWords: {words}\nScore: {total}"
