# Suposiciones sin comprobar — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [A-000]`. Búscala con `grep`, no leas el archivo entero.

⚠️ Aquí vive **solo lo que no se ha comprobado**. Cuando una suposición se
comprueba o se decide, **sale de aquí** y entra en `decisions.md` o `lessons.md`.

## Índice

| id | fecha | qué se está dando por cierto | riesgo si es falsa |
|---|---|---|---|
| A-003 | 2026-08-02 | Lo que se manda al log se ve y se puede reconstruir | [D-010] deja de valer: el detalle se escribe y no le sirve a nadie |
| A-002 | 2026-08-02 | El marcador lo escribe **un solo proceso a la vez**, sea cual sea | el candado deja de servir y los puntos se vuelven a perder |
| A-001 | 2026-08-02 | El marcador cuenta frases **practicadas**, no correctas | hay que cambiar el contrato de `judge_grammar` |

---

## Entradas

### [A-003] 2026-08-02 — Lo que se manda al log se ve y se puede reconstruir

- **Se supone que:** cuando `app/api.py` escribe en el log, eso queda registrado
  de forma que después se pueda leer y ordenar. Es lo que [D-010] da por hecho al
  mandar el detalle al log en vez de al navegador.
- **Por qué está aquí:** nadie ha configurado el log. `logging.basicConfig` no se
  llama y el logger raíz no tiene ningún handler; lo que hace que la línea
  aparezca es el **handler de último recurso** de Python, que actúa cuando no hay
  nada configurado. Funciona por defecto, no por decisión.
- **Lo que eso implica, sin que se haya elegido:**
  - Solo sale **WARNING o peor**. Un `logger.info(...)` se pierde en silencio.
  - Sale **sin hora, sin nivel y sin nombre** de quién lo escribió.
  - Sale por la salida de errores de la consola, y no queda en ningún archivo.
- **Cómo se comprobaría:** provocar el 500 del marcador roto y mirar la línea del
  servidor. Si no trae fecha ni hora, la suposición ya es falsa para la nube.
- **Si es falsa:** cuando algo se rompa con gente usándolo, el log no permitirá
  saber **cuándo** pasó ni **en qué orden**, que es lo primero que se pregunta.
- **Qué la cierra:** configurar el log una vez, al arrancar, con hora, nivel y
  origen. ⚠️ **No se hace hoy**: hoy no aporta nada y añadiría una pieza sin
  necesidad. Va con el paso 7, que es donde el log deja de tener a alguien
  mirándolo. Anotado como `T-033`.

### [A-002] 2026-08-02 — El marcador lo escribe un solo proceso a la vez

- **Se supone que:** en un momento dado hay **un solo proceso** escribiendo
  `data/score.json`. Sobre eso descansa el candado `_SCORE_LOCK` de
  `app/tools.py`, que es lo que impide que dos escrituras a la vez pierdan
  puntos ([D-009]).
- **Por qué está aquí:** un `threading.Lock` solo se ve dentro de **su** proceso.
  Dos procesos son dos candados que no se enteran el uno del otro, y el fallo
  vuelve entero. El candado no avisa: sigue pareciendo que funciona.
- **Las dos formas de romperlo, y la segunda es la probable:**
  1. Arrancar uvicorn con `--workers 2` o más. Es la que se ve venir.
  2. 🚨 **Tener `python main.py` abierto en una terminal y el servidor encendido
     en otra.** También son dos procesos, y esta es la que va a pasar de verdad:
     el `README.md` presenta las dos puertas una debajo de otra.
- **Comprobado que es real:** dos procesos sumando 200 puntos cada uno sobre el
  mismo archivo. De 400 esperados, el marcador guardó **169**, y **169** llamadas
  fallaron. Es el mismo fallo de antes de [D-009], sin arreglar y sin arreglo
  posible desde memoria.
- **Cómo se sostiene mientras tanto:** escrito en `README.md`, en "Cómo se
  corre", en los dos sitios: al presentar las dos puertas y al arrancar el
  servidor.
- **Si es falsa:** el candado de memoria no basta. Haría falta un candado del
  sistema de archivos —que lo ven todos los procesos— o sacar el marcador a algo
  que sepa contar solo, como una base de datos.
- ⚠️ **Vuelve a mirarse en el paso 7:** quien decide cuántos procesos hay en la
  nube es la plataforma, no nosotros. Ahí esta suposición deja de estar en
  nuestras manos.

### [A-001] 2026-08-02 — El marcador cuenta frases practicadas, no correctas

- **Se supone que:** el marcador mide **esfuerzo**, no acierto. `respond()` llama
  a `add_point()` siempre, sin mirar el veredicto, y eso se queda así.
- **Por qué está aquí y no en `decisions.md`:** la pregunta se planteó hoy y no
  se eligió entre las dos lecturas. Se anota como suposición —que es lo que
  es— en vez de dejarla sin escribir. **Está sin decidir.**
- **Por qué hoy no se nota:** el juez es falso y aprueba todo. Con `judge_grammar`
  devolviendo siempre el mismo veredicto, "practicadas" y "correctas" dan
  exactamente el mismo número. Las dos lecturas son indistinguibles hasta el
  paso 8.
- **Cómo se comprobaría:** en el paso 8, con el modelo enchufado, escribir una
  frase claramente incorrecta —`me likes coffees`— y mirar el marcador.
  - Si sube y eso es lo que se quería → la suposición era cierta. Sale de aquí y
    entra en `decisions.md`.
  - Si sube y chirría → era falsa. Sale de aquí y entra en `lessons.md`.
- **Si es falsa:** no basta con un `if` en `respond()`. Hoy el contrato es
  `judge_grammar(sentence) -> str`: devuelve **texto libre**, y nada dentro de
  esa cadena le dice a `respond` si la frase estaba bien. Contar aciertos obliga
  a cambiar el contrato de la herramienta para que devuelva algo que una máquina
  pueda leer —un aprobado/suspenso junto al mensaje—, y eso arrastra a `respond`
  y a lo que se le pida al modelo en el paso 8.
  🔑 El coste de equivocarse crece con el tiempo: hoy es un contrato que nadie
  usa todavía; en el paso 8 sería rediseñar la herramienta el mismo día que se
  enchufa el modelo, con dos sospechosos en vez de uno.
- **A favor de dejarlo así:** `_context/scope.md` pide que el agente "responda en
  tono positivo", y la v1 es de nivel A1. Un marcador que solo sube al acertar
  castiga justo a quien más se está esforzando.

<!-- La más reciente arriba. Formato:

### [A-001] 2026-08-02 — <qué se supone, en una línea>

- **Se supone que:** <la afirmación sin comprobar>
- **Cómo se comprobaría:** <la prueba concreta>
- **Si es falsa:** <qué se rompe>

-->
