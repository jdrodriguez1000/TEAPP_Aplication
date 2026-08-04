# Suposiciones sin comprobar — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [A-000]`. Búscala con `grep`, no leas el archivo entero.

⚠️ Aquí vive **solo lo que no se ha comprobado**. Cuando una suposición se
comprueba o se decide, **sale de aquí** y entra en `decisions.md` o `lessons.md`.

## Índice

| id | fecha | qué se está dando por cierto | riesgo si es falsa |
|---|---|---|---|
| A-007 | 2026-08-04 | Entre el Paso 2b del cierre y el `git add` no se toca ningún `.ts` | se comprueba un `.js` y se commitea otro: el control da verde sobre un archivo que ya no es el del commit |
| A-006 | 2026-08-03 | La ruta de `mktemp -d` de Git Bash le sirve a `node`, que es un binario de Windows | el control del `.js` del Paso 2b no compila nunca: siempre "SIN COMPROBAR" |
| A-005 | 2026-08-03 | `data/` vive en el **disco del servidor**, y ese disco sigue ahí mañana | el marcador se borra solo al redesplegar: `scope.md` promete lo contrario |
| A-003 | 2026-08-02 | Lo que se manda al log se ve y se puede reconstruir | [D-010] deja de valer: el detalle se escribe y no le sirve a nadie |
| A-002 | 2026-08-02 | El archivo de **una misma persona** lo escribe un solo proceso a la vez (🔻 encogida el 2026-08-03 por el paso 4) | el candado deja de servir y los puntos de esa persona se vuelven a perder |
| A-001 | 2026-08-02 | El marcador cuenta frases **practicadas**, no correctas | hay que cambiar el contrato de `judge_grammar` |

---

## Entradas

### [A-007] 2026-08-04 — Entre el Paso 2b del cierre y el `git add` no se toca ningún `.ts`

- **Se supone que:** desde que el Paso 2b compila y compara, hasta que el Paso 6
  hace `git add -A`, **nadie edita un archivo `.ts`**. Si alguien lo editara, el
  control habría dado su veredicto sobre un `.js` que ya no se corresponde con la
  fuente que entra en el commit.
- **Por qué nace hoy:** hasta el 2026-08-04 el control corría pegado al `git add`,
  con solo un paso de por medio. Al moverlo arriba ([D-019]) quedan cuatro pasos
  en medio, y esa distancia es exactamente lo que hay que suponer limpio. **La
  suposición no existía antes; la creó el arreglo.**
- **Por qué hoy es cierta:** entre los dos puntos, el `session-closer` solo
  escribe `progress.md` y `tasks.md` — archivos `.md`. Y el protocolo le prohíbe
  expresamente escribir código: *"No escribas código ni arregles nada, aunque veas
  algo roto"*. Ninguna de las dos cosas es un accidente, pero ninguna está
  comprobada por una máquina: las dos son texto que alguien tiene que seguir.
- **Cómo se comprobaría:** guardar el hash de `frontend/*.ts` en el Paso 2b y
  volver a calcularlo justo antes del `git add`. Si cambió, la suposición es
  falsa. **No se implementa hoy:** sería una pieza nueva para un problema que
  todavía no ha ocurrido — PI-2.
- **Si es falsa:** el control da **verde sobre el archivo equivocado**, que es
  peor que no tenerlo. Un rojo se ve; un verde falso se cree. Es la familia de
  [L-006]: confundir "no lo comprobé" con "está bien", solo que aquí la confusión
  es "comprobé otra cosa".
- **Qué la haría caer:** que algún día el cierre gane un paso que toque código
  —recompilar, formatear, arreglar un lint— entre el Paso 2b y el commit. 🔑 **Si
  eso se propone, esta entrada es la que hay que releer antes de aceptarlo.**

### [A-006] 2026-08-03 — La ruta de `mktemp -d` de Git Bash le sirve a `node`

- **Se supone que:** el Paso 2b de `protocol-close` hace `OUT=$(mktemp -d)` y le
  pasa esa ruta a `node`. `mktemp` devuelve algo tipo `/tmp/tmp.lu0Fzd9e5G` —una
  ruta de estilo Unix— y `node` es un **binario de Windows**, que entiende
  `C:\...`. Se supone que la traducción que hace Git Bash en medio funciona
  siempre, no solo aquí.
- **Cómo se comprobaría:** correr el Paso 2b tal cual en **otra máquina**, o con
  otra versión de Git Bash o de Node. Si sale "SIN COMPROBAR" con el compilador
  instalado y `node_modules/` en su sitio, la suposición es falsa.
- **Si es falsa:** el control no compila nunca y cae siempre en la tercera fila,
  "SIN COMPROBAR". No da falsos verdes —eso está cubierto por diseño— pero deja
  de vigilar, avisando. El arreglo sería convertir la ruta con `cygpath -w`.
- **Medido aquí el 2026-08-03:** `mktemp -d` dio `/tmp/tmp.lu0Fzd9e5G`, `node`
  lo aceptó y `tsc` compiló con `exit=0`. Funciona en esta máquina; que funcione
  en general es lo que sigue sin comprobar.

### [A-005] 2026-08-03 — `data/` vive en el disco del servidor, y ese disco sigue ahí mañana

- **Se supone que:** los marcadores `data/users/<nombre>.json` —uno por persona
  desde el paso 4— viven como **archivos en el disco del servidor**, y ese disco
  es el mismo mañana que hoy. Sobre eso descansa la promesa de `_context/scope.md`: un
  marcador "que sigue ahí mañana".
- **Por qué está aquí:** `_context/architecture.md` dice de `data/` **dónde no
  va** (a Git, no) pero **no dice dónde vive**. En todo el documento no aparece la
  palabra "base de datos", ni para elegirla ni para descartarla. Hoy son archivos
  porque es lo que salió del paso 1, no porque se haya decidido.
- **Por qué hoy no se nota:** en local el disco es el mismo siempre. Se apaga el
  servidor, se enciende, y el archivo sigue ahí. La suposición es **cierta en
  local** y por eso no molesta hasta el paso 7.
- **Cómo se comprobaría:** en el paso 7, sumar puntos, **volver a desplegar** la
  aplicación, y mirar el marcador. Si volvió a cero, la suposición era falsa.
- **Si es falsa:** el marcador y la memoria de cada persona se borran solos, sin
  error y sin aviso, cada vez que se actualice o se reinicie la aplicación.
  Es el peor tipo de fallo: **no rompe nada, solo olvida.** Y el arreglo no es un
  parche — es sacar `data/` a algo que viva fuera del servidor (una base de datos
  o un almacenamiento aparte), lo que toca `app/tools.py` entero.
- **Relación con [A-002] — son hermanas, no la misma:**
  - `A-002` pregunta **quién escribe a la vez** → el candado.
  - `A-005` pregunta **dónde está lo escrito** → el disco.
  Se pueden romper por separado: un disco que sobrevive no arregla dos procesos
  pisándose, y un candado perfecto no sirve si el archivo desaparece al
  redesplegar.
- ⚠️ **Se mira en el paso 7, no antes.** Elegir almacenamiento hoy sería una
  pieza nueva sin problema que resolver. Lo que valía era **dejarlo escrito**: la
  decisión es cara de deshacer, y aplazarla en silencio era la única forma mala
  de aplazarla.

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

- **Se supone que:** en un momento dado hay **un solo proceso** escribiendo el
  archivo de una misma persona (`data/users/<nombre>.json`). Sobre eso descansa
  el candado `_SCORE_LOCK` de `app/tools.py`, que es lo que impide que dos
  escrituras a la vez pierdan puntos ([D-009]).
- 🔻 **2026-08-03 — el paso 4 ENCOGE esta suposición, no la amplía.** Antes había
  un solo archivo para todo el mundo, así que **cualquier** par de escrituras
  simultáneas podía chocar. Con un archivo por persona, dos personas distintas
  en dos procesos distintos ya **no** se pisan nunca: escriben en archivos
  distintos. Lo que queda es **la misma persona dos veces a la vez** —dos
  pestañas, dos dispositivos, o la terminal y el servidor a la vez— cayendo en
  procesos distintos. Más raro, y exactamente igual de silencioso cuando pasa.
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
