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

import time
from dataclasses import dataclass

from app.tools import count_words, judge_grammar, record_practice


@dataclass(frozen=True)
class TutorReply:
    """Lo que la ruta necesita saber de esta práctica, en piezas separadas.

    🔴 **Esta línea decía "en tres piezas separadas" hasta el 2026-08-17, y para
    entonces ya eran cinco.** No es una errata: una caja que se describe más
    pequeña de lo que es invita a defenderle una pureza que ya perdió. Pasó en
    vivo — ver `[D-087]`, donde se discutió si meterle un reloj "contaminaba" al
    veredicto del juez, cuando **tres de los cinco campos no venían del juez**
    desde `[D-066]`: `words` lo cuenta `respond` en local, y `score` y `practice`
    salen del archivo de contadores.

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

    verdict: str  # lo que dice el juez, ya sin la palabra clave de [D-067]
    words: int  # cuántas palabras tenía la frase
    score: int  # frases CORRECTAS, después de anotar esta ([D-066])
    practice: int  # frases practicadas, acertadas o no

    # 🚨 **La MITAD DE MÁQUINA del veredicto, añadida el 2026-08-17 para la traza
    # de [D-085]. No es un duplicado de `verdict`: es lo contrario de él.**
    #
    # `verdict` es texto libre y **puede citar la frase de la persona dentro**
    # ("you wrote 'I has a cat'…"), así que no puede entrar en ningún archivo:
    # `PI-8`. `correct` dice lo mismo sin decir nada de nadie.
    #
    # 🔑 **Y no es una separación nueva: es la de [D-066] llegando un piso más
    # arriba.** `GrammarVerdict` ya venía partido en `correct` + `message` por
    # esta misma razón —"quien muestre la respuesta nunca debe ver la palabra
    # clave"—, pero `TutorReply` solo se llevaba el `message`, así que arriba la
    # mitad legible por una máquina no existía.
    #
    # ⚠️ **Por qué NO se deduce de `score`, que era la alternativa gratis:** con
    # dos líneas de traza consecutivas se ve si el marcador subió. Pero la traza
    # **puede perder líneas a propósito** —su fallo no propaga, [D-086]—, y con
    # una línea perdida el marcador salta de dos y no hay a quién atribuirlo. Una
    # deducción que se rompe justo por el comportamiento diseñado del sistema no
    # es una deducción.
    correct: bool

    # 🚨 **Cuánto tardó la parte del MODELO, añadido el 2026-08-17 para el reparto
    # de tiempo de [D-087]. No es "cuánto tardó la práctica": eso lo mide la ruta.**
    #
    # 🔑 **Por qué se mide AQUÍ y no dentro de `judge_grammar`.** Lo que decide
    # `[D-049]` —bajar de modelo— es *"¿el lento es el modelo o somos nosotros?"*.
    # Un reloj alrededor de la llamada a `judge_grammar` contesta eso sin entrar en
    # la función: la nota sube **un piso**, no tres. Meter el campo en
    # `GrammarVerdict` sí habría sido contaminarlo — esa clase tiene dos campos y
    # los dos son del juez.
    #
    # ⚠️ **Lo que este número incluye de más, dicho para que no sorprenda:** además
    # de la llamada al modelo, va dentro construir el cliente y leer la respuesta.
    # Es deliberado: el handshake vive ahí, y es parte de lo que cuesta preguntar.
    #
    # ⚠️ **Y lo que significa depende de `MAX_RETRIES`,** que hoy es `0`
    # (`tools.py:64`). Un intento, un reloj. Si algún día deja de ser cero, este
    # número pasa a ser "todos los intentos juntos" — que **sigue siendo el número
    # correcto** para observabilidad, porque es lo que espera la persona, pero deja
    # de poder compararse con el precio de una llamada.
    model_seconds: float


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
    # 🚨 **Estas líneas están en este orden a propósito, y reordenarlas cambia
    # lo que se le cobra a una persona.**
    #
    # Si `judge_grammar` revienta —Claude caído, llave mala—, la excepción sale
    # de aquí **antes** de llegar a `record_practice`: no sube nada, ni acierto
    # ni práctica, que es exactamente lo que decidió [D-050]. Una práctica sin
    # veredicto no es una práctica floja, es una práctica que no ocurrió.
    #
    # 🔑 **Antes esto eran tres argumentos y el orden lo garantizaba Python**,
    # que los evalúa como están escritos. Desde [D-066] ya no puede ser así: el
    # veredicto hace falta **como valor** para saber si se suma acierto, y un
    # valor que se usa dos veces no cabe dentro de una llamada. El freno sigue
    # siendo el mismo, solo que ahora se ve a simple vista en vez de depender de
    # una regla del lenguaje.
    #
    # El modo de fallo es **mudo** —reordenar no rompe la sintaxis—, así que hay
    # un test que vigila el orden. Un comentario solo protege a quien lo lee.
    words = count_words(sentence)

    # 🔑 **El reloj abraza la línea del juez, y solo esa.** Es la única de las tres
    # que sale a la red ([D-087]). `count_words` y `record_practice` son trabajo
    # local; meterlas dentro diluiría el número con milisegundos que no dependen
    # del modelo, que es justo lo que el número existe para separar.
    before_judge = time.perf_counter()
    verdict = judge_grammar(sentence)
    model_seconds = time.perf_counter() - before_judge

    counters = record_practice(user, correct=verdict.correct)

    return TutorReply(
        verdict=verdict.message,
        words=words,
        score=counters.score,
        practice=counters.practice,
        correct=verdict.correct,
        model_seconds=model_seconds,
    )
