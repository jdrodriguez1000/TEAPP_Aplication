"""El corrector de la rúbrica: mira si el juez contestó como se le pidió.

🚨 **Esto NO juzga si el veredicto acierta.** No sabe si `"She go to school"`
estaba bien o mal, y no puede saberlo: para eso hacen falta las 60 frases
etiquetadas a mano, que es la otra mitad del paso 9. Aquí se mira **la forma de
la respuesta**, no su contenido.

## Por qué la forma merece su propio instrumento

`GRAMMAR_RUBRIC` (`tools.py:260`) le pide al modelo **siete** cosas. Tres de
ellas necesitan que una persona lea la respuesta y opine —si acertó, si corrigió
un error o tres, si se fue del tema—. Las otras cuatro **las comprueba un
programa sin opinar**, y son las que están aquí.

🔑 **Y no son las cuatro fáciles: son las cuatro que se van a romper primero.**
`[D-049]` tiene programado bajar el modelo a Sonnet 5 y después a Haiku 4.5. Un
modelo pequeño sigue viendo que `"She go to school"` está mal —eso es gramática
de primer año—; lo que se le va es **la forma**: mete un asterisco, se estira a
cuatro frases, o le escribe `FIX` al alumno. Y esos fallos **salen a la
pantalla**, porque `app/static` pinta este texto tal cual.

## 🚨 El agujero que este módulo existe para tapar

`split_verdict` (`tools.py:601`) ya hace lo correcto cuando el modelo se salta el
formato: no da el punto y enseña el mensaje entero. Pero **no se lo cuenta a
nadie**. Y la traza escribe `correct: bool`, así que un fallo de formato llega al
cuaderno como `correct=False` — **idéntico a un alumno que escribió mal la
frase**.

    el juez rompe el formato  →  correct=False
    el alumno se equivoca     →  correct=False

Dos causas opuestas, un solo número. El día que el modelo nuevo empiece a
romperse, `trace.jsonl` va a decir *"la gente falla más"* cuando lo cierto es
*"el juez dejó de contestar como se le pidió"*, y los dos diagnósticos llevan a
arreglos contrarios: uno a la rúbrica, el otro a la clase de inglés.

⚠️ **Es `LM.15` dentro del paso que se llama Observabilidad:** el fallo no da un
dato falso, da un dato **ambiguo**, y la ambigüedad no se ve en la gráfica.

## Lo que este módulo NO hace todavía

📌 Hoy es un instrumento **de fuera**: lo llama el eval, no la ruta. Que la ruta
lo llame y la traza apunte el fallo de formato es un cambio en producción y **no
está decidido** — se decide aparte, no se cuela aquí.

## Por qué devuelve un conjunto de nombres y no cuatro booleanos

Porque quien lo llama quiere **contar**: sesenta respuestas, cuántas rompieron
cada promesa. Un conjunto de nombres se suma con un `Counter` en una línea; cuatro
booleanos hay que desmontarlos primero.

🚨 **Y `PROMISES` está aquí para que una promesa nueva no pueda nacer muda.** Es
`[L-073]` aplicado a este módulo: el test clava **el conjunto entero**, así que
añadir la quinta promesa sin darle su test pone la suite en rojo. Sin eso, la
quinta nacería exactamente como nació `TutorReply.correct` — con el archivo
teniendo ya aspecto de cobertura completa.
"""

from app.tools import VERDICT_CORRECT, VERDICT_WRONG

# Los nombres de las cuatro promesas mecánicas. Se devuelven tal cual, así que
# también son lo que se lee en el informe del eval: se escriben para leerse.
BAD_FIRST_LINE = "bad_first_line"
HAS_MARKDOWN = "has_markdown"
TOO_MANY_SENTENCES = "too_many_sentences"
LEAKS_KEYWORD = "leaks_keyword"

# 🚨 El conjunto entero, clavado por un test. Ver la cabecera: si aparece una
# quinta promesa y no se añade aquí, el test NO se pone rojo por ella: se pone
# rojo porque este conjunto dejó de cuadrar, que es lo que obliga a decidir quién
# la vigila antes de seguir.
PROMISES = frozenset(
    {BAD_FIRST_LINE, HAS_MARKDOWN, TOO_MANY_SENTENCES, LEAKS_KEYWORD}
)

# Lo que la rúbrica prohíbe por escrito: "no markdown, no bullet points, no
# asterisks, no quotation marks". El backtick no lo nombra, y va igual: es
# markdown y llega a la pantalla como un acento suelto.
MARKDOWN_CHARACTERS = ("*", "`", '"')

# Los arranques de viñeta. Se miran al principio de una línea ya recortada, no
# en medio: un guion dentro de una frase es un guion, no una lista.
BULLET_STARTS = ("- ", "* ", "• ", "+ ")

# Lo que cierra una frase. La rúbrica pide "at most two short sentences", así que
# con más de dos cierres hay más de dos frases.
SENTENCE_ENDS = (".", "!", "?")
MAX_SENTENCES = 2


def learner_message(answer: str) -> tuple[bool, str]:
    """Parte la respuesta igual que `split_verdict`, pero **delatando el formato**.

    Devuelve dos cosas: si la primera línea traía la palabra clave que la rúbrica
    pidió, y el texto que le queda al alumno.

    🚨 **Por qué no se reutiliza `split_verdict` y se acepta el precio de repetir
    tres líneas.** `split_verdict` está construido para *aguantar* el fallo de
    formato: cuando la primera línea no es `OK` ni `FIX`, devuelve el mensaje
    entero y `correct=False` — y desde fuera **eso es indistinguible** de un `FIX`
    bien puesto. La información que este módulo necesita es justo la que aquella
    función tira a propósito.

    ⚠️ **Y repetir lógica se paga en deriva**, así que el precio está atado: hay
    un test que corre las dos funciones sobre las mismas cadenas y exige que
    coincidan en dónde cortan. Si alguien cambia una y no la otra, se pone rojo.
    """
    first_line, _, rest = answer.partition("\n")
    message = rest.strip()

    # Sin nada detrás de la palabra clave no hay mensaje que enseñar. `split_verdict`
    # trata este caso como formato mal puesto, y aquí se trata igual: la respuesta
    # completa es lo que vería el alumno.
    if not message:
        return False, answer.strip()

    head = first_line.strip().upper()

    if head in (VERDICT_CORRECT, VERDICT_WRONG):
        return True, message

    return False, answer.strip()


def check_reply(answer: str) -> frozenset[str]:
    """Devuelve qué promesas mecánicas rompió esta respuesta. Vacío = ninguna.

    :param answer: la respuesta **cruda** del modelo, con su primera línea. No el
        mensaje ya recortado: la primera promesa habla justo de esa línea.
    """
    broken: set[str] = set()

    format_ok, message = learner_message(answer)

    if not format_ok:
        broken.add(BAD_FIRST_LINE)

    if _has_markdown(message):
        broken.add(HAS_MARKDOWN)

    if _counts_sentences(message) > MAX_SENTENCES:
        broken.add(TOO_MANY_SENTENCES)

    if _leaks_keyword(message):
        broken.add(LEAKS_KEYWORD)

    return frozenset(broken)


def _has_markdown(message: str) -> bool:
    """Asteriscos, backticks, comillas, o una línea que arranca como viñeta.

    ⚠️ **Honestidad sobre lo que mide: la comilla es la parte basta.** La rúbrica
    prohíbe comillas *alrededor de la corrección*, y aquí se rechaza cualquier
    comilla doble. Puede sobrar —una respuesta legítima podría llevar una— y se
    acepta a propósito: 🔑 **este instrumento existe para avisar de que la forma
    se movió, y un aviso de más se investiga; uno de menos no se sabe que faltó.**
    """
    if any(character in message for character in MARKDOWN_CHARACTERS):
        return True

    return any(
        line.strip().startswith(BULLET_STARTS) for line in message.splitlines()
    )


def _counts_sentences(message: str) -> int:
    """Cuenta cierres de frase.

    ⚠️ **Lo que este conteo NO distingue**, dicho aquí y no descubierto luego: una
    abreviatura con punto —`e.g.`— cuenta como dos cierres, y `8 a.m.` como dos
    más. Sobre respuestas de tutor A1 de dos frases eso casi no aparece, y cuando
    aparezca **el error va hacia avisar**, no hacia callarse.
    """
    return sum(message.count(end) for end in SENTENCE_ENDS)


def _leaks_keyword(message: str) -> bool:
    """Busca `OK` o `FIX` dentro de lo que ve el alumno.

    🔑 **Se compara RESPETANDO las mayúsculas y como palabra suelta, y las dos
    cosas hacen falta.** Sin lo primero, el `ok` de *"that's ok"* contaría como
    fallo y no lo es: la rúbrica prohíbe **la palabra clave del programa**, que va
    en mayúsculas, no la palabra inglesa que la rúbrica misma pide usar con tono
    cálido. Y sin el corte por palabras, el `FIX` de *"prefix"* saltaría solo.

    ⚠️ **Y sí, aquí se distinguen mayúsculas y en `learner_message` NO.** No es un
    descuido, son dos preguntas distintas: allí se pregunta *"¿entendió la app esta
    primera línea?"* —y `split_verdict` acepta `  fix  `, así que hay que aceptarlo
    igual o el eval contaría fallos que la app no tiene—; aquí se pregunta *"¿se le
    escapó la palabra del programa al alumno?"*, y en minúscula no se le escapó
    nada.

    🔴 **Escrito después de un rojo.** Esta función subía todo a mayúsculas y
    marcaba *"That's ok"* como fallo — con este mismo docstring diciendo que no
    había que hacerlo. El test lo cazó; la explicación estaba bien y el código no
    la seguía.
    """
    words = {word.strip(".,;:!?()") for word in message.split()}
    return bool(words & {VERDICT_CORRECT, VERDICT_WRONG})
