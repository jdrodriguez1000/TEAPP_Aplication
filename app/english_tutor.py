"""El agente. Falso por ahora: decide siempre la misma secuencia.

Un agente de verdad elige qué herramientas usar y en qué orden. Este todavía no
elige: llama a las tres, siempre, en el mismo orden. Eso basta para montar y
probar toda la tubería alrededor sin gastar un centavo.
"""

from dataclasses import dataclass

from app.tools import add_point, count_words, judge_grammar


@dataclass(frozen=True)
class TutorReply:
    """Lo que el tutor contesta, en tres piezas separadas.

    🔑 **El tutor manda los ingredientes, no el plato servido.** Antes devolvía
    una sola cadena con todo cocinado dentro —"veredicto, salto de línea,
    Words: 3…"—. Eso solo le sirve a quien vaya a imprimirlo tal cual.

    En el paso 3 quien recibe esto es la pantalla, y una cadena cocinada la deja
    sin opciones: no puede pintar el marcador en su sitio, ni resaltar el
    veredicto, ni nada. Solo puede volcarla. Separadas, en cambio, cada pieza va
    donde le toca — y quien las junte será quien las va a mostrar.

    `frozen=True` las deja de solo lectura: una vez contestado, nadie cambia el
    veredicto por el camino.
    """

    verdict: str  # lo que dice el juez de gramática
    words: int  # cuántas palabras tenía la frase
    score: int  # el marcador después de sumar el punto


def respond(sentence: str) -> TutorReply:
    """Recibe una frase en inglés y devuelve la respuesta del tutor.

    🔑 Esta función es el enchufe del proyecto. Entra un texto, salen las tres
    piezas, y nada más. Hoy la llaman `main.py` desde la terminal y FastAPI
    desde la red; la función no se entera de cuál de los dos fue, y por eso
    cualquiera de los dos puede desaparecer sin arrastrar nada consigo.
    """
    return TutorReply(
        words=count_words(sentence),
        verdict=judge_grammar(sentence),
        score=add_point(),
    )
