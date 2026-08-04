# Suposiciones sin comprobar — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [A-000]`. Búscala con `grep`, no leas el archivo entero.

⚠️ Aquí vive **solo lo que no se ha comprobado**. Cuando una suposición se
comprueba o se decide, **sale de aquí** y entra en `decisions.md` o `lessons.md`.

## Índice

| id | fecha | qué se está dando por cierto | riesgo si es falsa |
|---|---|---|---|
| A-012 | 2026-08-04 | **Nadie va a probar contraseñas a la fuerza contra `/login` antes del paso 7.** Hoy no hay tope de intentos ([D-025]) | alguien entra en la cuenta de otro probando contraseñas, y no queda rastro de que lo intentó |
| A-011 | 2026-08-04 | **10 segundos es lo que hay que esperar al tutor.** Predicción: hoy no hay nada que tarde, así que no hay nada que cronometrar | corto, se corta a quien iba a contestar bien; largo, la petición cuelga y el hilo con ella |
| A-010 | 2026-08-04 | **20 prácticas al día por persona es el tope correcto**: predicción, no número final. Se mide en el paso 8, cuando haya facturas | o frena a quien estudia de verdad, o deja pasar una factura que duele |
| A-009 | 2026-08-04 | La cookie con `secure=True` funciona — nunca se ha ejecutado esa rama: los 192 tests la apagan | el inicio de sesión no funciona en la nube, y el fallo es mudo: el navegador descarta la cookie sin decir nada |
| A-008 | 2026-08-04 | `TEAPP_SECRET_KEY` es la MISMA en cada arranque, y sigue siéndolo tras redesplegar | todas las sesiones mueren de golpe y todo el mundo queda fuera, sin ningún error que lo explique |
| A-007 | 2026-08-04 | Entre el Paso 2b del cierre y el `git add` no se toca ningún `.ts` | se comprueba un `.js` y se commitea otro: el control da verde sobre un archivo que ya no es el del commit |
| A-006 | 2026-08-03 | La ruta de `mktemp -d` de Git Bash le sirve a `node`, que es un binario de Windows | el control del `.js` del Paso 2b no compila nunca: siempre "SIN COMPROBAR" |
| A-005 | 2026-08-03 | `data/` vive en el **disco del servidor**, y ese disco sigue ahí mañana | el marcador se borra solo al redesplegar: `scope.md` promete lo contrario |
| A-002 | 2026-08-02 | El archivo de **una misma persona** lo escribe un solo proceso a la vez (🔻 encogida el 2026-08-03 por el paso 4) | el candado deja de servir y los puntos de esa persona se vuelven a perder |
| A-001 | 2026-08-02 | El marcador cuenta frases **practicadas**, no correctas | hay que cambiar el contrato de `judge_grammar` |

---

## Entradas

### [A-012] 2026-08-04 — Nadie prueba contraseñas a la fuerza contra `/login`

- **Se supone que:** mientras la app corra solo en la máquina de casa, nadie va
  a lanzar miles de intentos contra `/login` hasta acertar una contraseña.
- **Por qué nace hoy:** [D-025] decidió aplazar el tope de intentos al paso 7.
  Esta entrada es la otra mitad de esa decisión: **lo que hay que dar por cierto
  para que aplazarlo sea razonable.**
- 🔑 **Hoy es casi seguro que es cierta, y el día del despliegue deja de serlo de
  golpe.** No se va degradando: cambia el día que la app tiene una URL pública.
  Por eso la fecha de caducidad es un paso concreto, no "más adelante".
- **Lo que amortigua mientras tanto:** la contraseña se guarda con `scrypt`
  ([D-021]), que es lento a propósito, y `/login` contesta lo mismo tanto si el
  nombre no existe como si la contraseña no es esa — así probar no dice ni
  siquiera quién tiene cuenta. Ninguna de las dos cosas frena los intentos:
  encarecen cada uno.
- **Cómo se comprobaría:** mandar 200 intentos fallidos seguidos contra `/login`
  y ver que ninguno se rechaza por ser el número 200. Hoy pasarían todos, así
  que la comprobación no es "¿pasa?" sino **cuánto tarda cada intento**: eso dice
  cuánto cuesta el ataque hoy.
- **Si es falsa:** alguien entra en la cuenta de otro, y **no queda rastro**: sin
  tope no hay nada que registre "aquí hubo 5.000 intentos".
- **Qué la cierra:** el tope de intentos del paso 7. ⚠️ No se cuenta por persona
  —la persona es justo lo que está en duda— sino por origen de la petición.

### [A-011] 2026-08-04 — 10 segundos es lo que hay que esperar al tutor

- **Se supone que:** `TUTOR_TIMEOUT_SECONDS = 10.0` deja contestar a una llamada
  sana al modelo y corta las que se han quedado colgadas.
- 🔑 **Es una predicción, igual que el 20 de [A-010].** Hoy el tutor es falso y
  contesta al instante: **no hay nada que cronometrar**. El número no sale de
  ninguna corrida.
- **Cómo se comprobaría:** en el paso 8, midiendo cuánto tarda de verdad una
  llamada al modelo con una frase de nivel A1. El tope tiene que quedar
  cómodamente por encima de la llamada lenta normal, no de la media.
- **Si es falsa:**
  - **Corto de más:** se corta a quien iba a contestar bien. Se ve como 504 con
    el modelo funcionando — desconcertante, porque no hay nada roto.
  - **Largo de más:** quien pregunta espera de balde, y el hilo sigue ocupado
    todo ese rato.
- 🚨 **Lo que este freno NO arregla, y no es una suposición sino un hecho:**
  libera a quien pregunta, no al hilo. Python no sabe matar un hilo. Comprobado
  el 2026-08-04 con uvicorn: 504 a los 10,02 s contra un tutor de 30 s, y el
  hilo siguió durmiendo sus 30. ⚠️ **Por eso en el paso 8 la llamada al modelo
  necesita su propio timeout**, además de este: uno acota lo que espera quien
  pregunta, el otro lo que espera el servidor.

### [A-010] 2026-08-04 — 20 prácticas al día es el tope correcto

- **Se supone que:** 20 prácticas diarias por persona es un tope que deja
  estudiar de verdad y a la vez frena una factura antes de que duela.
- 🔑 **Es una predicción, no un número final.** Sale de un criterio razonado
  —"una sesión de estudio larga cabe, un bucle automático no"— pero **no de
  ninguna corrida**: hoy el tutor es falso y no cuesta nada, así que no hay nada
  que medir. Entra al código como valor por defecto, no como verdad.
- **Cómo se comprobaría:** en el **paso 8**, con el modelo enchufado y facturas
  de verdad. Dos medidas, no una:
  1. **Por arriba:** 20 prácticas × el costo real de una llamada = el techo de
     gasto diario de una persona. Si ese número asusta, 20 es demasiado.
  2. **Por abajo:** cuántas prácticas hace de verdad alguien en una sesión. Si
     nadie llega a 20 nunca, el freno no frena nada y da falsa tranquilidad;
     si todo el mundo choca contra él, estorba.
- **Si es falsa:** en un sentido, el freno estorba a quien estudia y hay que
  subirlo. En el otro, deja pasar 20 llamadas al modelo por persona y día, y esa
  cuenta la paga quien abrió la cuenta.
- **Por eso el tope se inyecta** ([D-023]): cambiar el número no puede obligar a
  tocar la lógica ni a reescribir tests.

### [A-009] 2026-08-04 — La cookie con `secure=True` funciona, y nunca se ha ejecutado esa rama

- **Se supone que:** cuando `cookie_secure()` devuelve `True`, `set_cookie` marca
  la cookie como `Secure` y el inicio de sesión sigue funcionando.
- **Por qué nace hoy:** `tests/conftest.py` pone `TEAPP_COOKIE_SECURE=false` con
  `autouse=True`, así que vale en **los 192 tests**. Se buscó en toda la suite el
  2026-08-04 y no hay ni un test que lo ponga en `true`. Y `cookie_secure()`
  devuelve `True` **cuando la variable no está puesta**, que es el valor por
  defecto y el seguro.
- 🔑 **El camino por defecto es el que menos se prueba, precisamente porque las
  pruebas lo apagan para poder trabajar.** El `false` no está ahí por capricho:
  sin él, el cliente de pruebas —que habla por `http://`— descartaría la cookie y
  fallarían todos los tests de sesión. La suite tiene que apagarlo para funcionar,
  y al apagarlo deja de mirar el otro lado.
- **De la familia de `[L-010]`, con otra cara.** Allí un test miraba el efecto y
  no la respuesta; aquí la suite mide un modo y da por bueno el otro. Las dos
  veces el hueco no estaba en lo que el test afirmaba, sino en lo que ni se
  planteaba.
- **Qué pasa si es falsa:** en el paso 7 se pone `true` **en producción**, y esa
  rama correría por primera vez en la nube. Si algo estuviera mal, el fallo es
  mudo: el navegador descarta la cookie sin ningún error, ni en pantalla ni en el
  log del servidor. Se parecería a "el inicio de sesión no hace nada".
- **Cómo se comprobaría:** un test que **anule el `autouse`**, ponga
  `TEAPP_COOKIE_SECURE=true` y compruebe que `set_cookie` recibe `secure=True`.
  📌 Queda como tarea del paso 7 en `tasks.md`, no de hoy.
- ⚠️ **Es un hueco conocido, no un descuido.** Se encontró y se midió el mismo
  día que se escribió el código; lo que se decidió fue **cuándo** taparlo.

### [A-008] 2026-08-04 — La llave de firma es la misma en cada arranque

- **Se supone que:** el valor de `TEAPP_SECRET_KEY` **no cambia** entre un
  arranque del servidor y el siguiente, ni al redesplegar en el paso 7.
- **Por qué nace hoy:** el paso 5 firma las sesiones con esa llave
  (`app/sessions.py`). Una firma solo se reconoce con la misma llave que la hizo.
- **Qué pasa si es falsa:** 🚨 **todas las sesiones abiertas mueren de golpe y
  todo el mundo queda fuera.** Nadie pierde su cuenta ni su marcador —eso vive en
  disco—, pero todos tienen que volver a escribir su contraseña.
  ⚠️ **Esto no es un fallo: es cómo funciona una firma.** Se anota justamente
  para que el día que pase no se busque un error que no existe. El síntoma es
  desconcertante —todo el mundo desconectado a la vez, sin nada en el log— y
  lleva derecho a sospechar de las cookies o del navegador.
- **Cómo se comprobaría:** arrancar, entrar, parar el servidor, cambiar la llave
  del `.env`, arrancar otra vez y recargar la página. Tiene que pedir la
  contraseña de nuevo. El caso contrario —misma llave, sesión que sobrevive al
  reinicio— **sí está comprobado hoy**, en la corrida real del 2026-08-04.
  📌 Está probado desde el otro lado en `test_a_card_signed_with_another_key_is_rejected`:
  ahí se ve que cambiar la llave invalida la tarjeta. Lo que queda sin comprobar
  es que la llave **no** cambie sola en la nube del paso 7.
- **Dónde muerde de verdad:** en el paso 7. Si la plataforma genera la variable
  al desplegar en vez de leerla de un sitio fijo, cada despliegue echaría a todo
  el mundo. Ver la tarea del paso 7 en `tasks.md`.

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
