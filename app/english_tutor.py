"""El agente. Llama a las tres herramientas, siempre, en el mismo orden.

🚨 **Ya no es falso, y la mitad que no cambió tampoco es deuda.** Hasta [T-076]
este archivo empezaba diciendo *"falso por ahora"*, porque `judge_grammar`
contestaba lo mismo mirara lo que mirara. Eso se acabó: el juez es una llamada
real a Claude.

Lo que **no** cambió es la secuencia: sigue llamando a las tres y en el orden
escrito, sin elegir. Un agente más grande elegiría — este no, **a propósito**.
`_context/scope.md` lo dice con todas las letras: *"este proyecto no trata sobre
el agente, trata sobre lo que lo rodea"*, y el agente es pequeño de encargo.

🔑 **Distinguirlo importa porque las dos cosas se leían igual.** "Falso" era
trabajo pendiente y se fue con el paso 8; "no elige" es una decisión de alcance
y se queda. Dejar la palabra vieja invitaría a alguien a "terminar" algo que ya
está terminado.

⚠️ Y el ORDEN de esas tres llamadas no es cosmético: sostiene [D-050]. Está
explicado donde se escriben, al final de `respond`.
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


def respond(sentence: str, user: str) -> TutorReply:
    """Recibe una frase en inglés y devuelve la respuesta del tutor para esa persona.

    🔑 Esta función es el enchufe del proyecto. Entra un texto, salen las tres
    piezas, y nada más. Hoy la llaman `main.py` desde la terminal y FastAPI
    desde la red; la función no se entera de cuál de los dos fue, y por eso
    cualquiera de los dos puede desaparecer sin arrastrar nada consigo.

    `user` es obligatorio y no tiene valor por defecto **a propósito**. Un
    `user="anonimo"` de repuesto haria que olvidarse de pasarlo no diera error:
    los puntos se irian a un marcador compartido y nadie se enteraria. Es
    exactamente el fallo que este paso viene a matar, y no conviene dejar la
    puerta abierta para que vuelva a entrar.

    ⚠️ En el paso 4 el nombre es **declarado, no verificado**: quien usa la app
    dice quién es y el servidor se lo cree. Eso lo arregla el paso 5 — ver
    [D-013].
    """
    # 🚨 **Estas tres líneas están en este orden a propósito, y reordenarlas
    # cambia lo que se le cobra a una persona.**
    #
    # Python evalúa los argumentos en el orden escrito. Si `judge_grammar`
    # revienta —Claude caído, llave mala—, la excepción sale de aquí **antes**
    # de llegar a `add_point`: el marcador no sube, que es exactamente lo que
    # decidió [D-050]. Una práctica sin veredicto no es una práctica floja, es
    # una práctica que no ocurrió.
    #
    # 🔑 Poner `score=add_point(user)` primero se lee igual de bien y sumaría el
    # punto igualmente. Por eso hay un test que vigila el orden: el modo de
    # fallo es **mudo**, y un comentario solo no lo para.
    return TutorReply(
        words=count_words(sentence),
        verdict=judge_grammar(sentence),
        score=add_point(user),
    )
