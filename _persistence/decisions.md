# Decisiones — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [D-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

| id | fecha | qué se decidió | toca |
|---|---|---|---|
| D-012 | 2026-08-03 | TypeScript con `tsc`: fuente en `frontend/`, el `.js` compilado sí va a Git | `tsconfig.json`, `package.json`, paso 3, paso 7 |
| D-011 | 2026-08-03 | FastAPI sirve la pantalla: mismo origen, y CORS se descarta (T-029) | `app/api.py`, paso 3, paso 7 |
| D-010 | 2026-08-02 | El detalle completo va al log; al navegador, un mensaje corto y sin rutas | `app/api.py`, todo error futuro |
| D-009 | 2026-08-02 | Candado en memoria + temporal con nombre propio para dos peticiones a la vez | `app/tools.py`, `[A-002]`, paso 4 |
| D-008 | 2026-08-02 | El tutor devuelve tres piezas separadas, no un texto cocinado | `app/english_tutor.py`, `app/api.py`, `main.py`, paso 3 |
| D-007 | 2026-08-02 | El marcador se escribe al lado y se renombra encima (escritura atómica) | `app/tools.py`, paso 4 |
| D-006 | 2026-08-02 | El marcador roto avisa con `ScoreFileError`; ausente sigue siendo 0 | `app/tools.py`, `main.py`, paso 2 |
| D-005 | 2026-08-02 | Nombres en inglés, contenido en español | todo el código del proyecto |
| D-004 | 2026-08-02 | El protocolo de inicio lee `_context/` siempre, no a demanda | `protocol-start`, `session-starter` |
| D-003 | 2026-08-02 | Recuperar 4 principios de ingeniería de un `CLAUDE.md` anterior | cómo se escribe el código |
| D-002 | 2026-08-02 | Los cuatro archivos del porqué los escribe la sesión principal, no el closer | `_persistence/` |
| D-001 | 2026-08-02 | La skill de inicio se llama `protocol-start`, no `protocol-close` | `.claude/skills/` |

---

## Entradas

### [D-012] 2026-08-03 — TypeScript con `tsc`: fuente en `frontend/`, el `.js` compilado sí va a Git

- **Se eligió:** escribir la pantalla en TypeScript de verdad y compilarla con
  `tsc`, como dice `_context/architecture.md`. Tres detalles concretos:
  - **El fuente vive en `frontend/`, la salida en `app/static/`.** Se editan solo
    los `.ts` de `frontend/`; los `.js` de `app/static/` los escribe el
    compilador. Dos carpetas y no una para que sea imposible confundirse sobre
    cuál se edita.
  - **`strict: true`.** Todos los avisos encendidos. Apagarlos sería pagar el
    costo de TypeScript sin llevarse lo comprado.
  - **`module: "es2020"`.** Un archivo suelto, sin `import` ni `export`, que el
    HTML carga con un `<script>` normal. Los módulos son un tema entero y no
    hacen falta hoy (PI-2). Se escribió primero `"none"` y **el compilador lo
    rechazó**: TypeScript 7 ya no acepta ese valor. Vale la pena anotarlo porque
    la documentación consultada no lo decía — 🔑 **el compilador es la única
    fuente que no se queda desactualizada.**
  - **Versión fija: `typescript` 7.0.2**, sin `^`. Misma razón que [L-002]: sin
    fijar, dos máquinas instalan compiladores distintos. Se consultó la
    documentación actual antes de escribir el `tsconfig.json` en vez de sacarlo
    de memoria — 7.0.2 es el compilador nativo, muy posterior a lo que el modelo
    recordaba.
- **Contra:** dos alternativas reales, no de paja.
  - **Escribir `app.js` a mano** y saltarse TypeScript en el paso 3.
  - **`app.js` con `// @ts-check` y JSDoc**, que da buena parte de los avisos sin
    compilar ni instalar nada.
  Se descartaron porque la elección de TypeScript **ya estaba tomada** en
  `architecture.md`. Cambiarla aquí habría sido decidir arquitectura de refilón,
  en medio de otra tarea. El costo previsto —instalar Node— resultó ser cero:
  ya estaba instalado (v25.8.1, npm 11.11.0), comprobado antes de proponer nada.
  📌 `// @ts-check` queda anotado como la salida buena si `tsc` diera problemas.
- **Por qué:** el aviso que se compra es concreto. El contrato de [D-008] es
  `verdict`, `words`, `score`; escribir `reply.verdcit` en JavaScript no es un
  error, vale `undefined`, y la pantalla muestra "undefined" sin explotar. Ese
  fallo miente en silencio y se busca en el sitio equivocado. TypeScript lo
  subraya al escribirlo.
  🔑 **Lo que el navegador lee es el `.js`, siempre.** El `.ts` no es una
  alternativa al `.js`: es su original. ⚠️ De ahí el riesgo real y previsible de
  esta decisión: **editar el `.ts` y olvidar compilar** deja el navegador
  comportándose como antes, con el código correcto delante. Queda escrito aquí
  para que el día que pase se busque en el sitio correcto.
  Y el `.js` compilado **se versiona** —contra la costumbre de ignorar lo
  generado— porque en la nube corre **un solo servicio, en Python**: allí no hay
  Node que compile nada. Si el `.js` no está en Git, el paso 7 sube una pantalla
  que no existe. `dist/` sigue en `.gitignore` de cuando se pensó compilar
  aparte; ya no aplica, pero no estorba y no se toca (PI-3).
- **Toca:** `package.json` y `tsconfig.json` (nuevos), `frontend/app.ts`,
  `app/static/app.js` (generado, versionado), y el paso 7, que debe subir
  `app/static/` con el `.js` ya compilado. `node_modules/` ya estaba ignorado.

### [D-011] 2026-08-03 — FastAPI sirve la pantalla: mismo origen, y CORS se descarta (T-029)

- **Se eligió:** que el mismo FastAPI que atiende `/practice` sirva también el
  `index.html` y el `.js` de la pantalla. Un solo servidor, un solo origen, desde
  el primer día de desarrollo y no solo en el despliegue. En consecuencia
  **T-029 (configurar CORS) se descarta**: no se hará, ni ahora ni en el paso 7.
- **Contra:** servir la pantalla aparte —en otro puerto local, o abriendo el HTML
  con doble clic— y configurar CORS con una lista explícita de orígenes, que era
  el plan de T-029 y estuvo a punto de escribirse hoy.
- **Por qué:** CORS solo existe cuando hay **dos orígenes**. Con la pantalla
  servida por el mismo FastAPI, el navegador ve un único edificio y no tiene nada
  que bloquear. 🔑 **La mejor configuración de CORS es no necesitar CORS.**
  T-029 no salía de ningún archivo del proyecto: se revisó `_context/
  architecture.md` y `_context/roadmap.md` a propósito antes de descartarla, y
  ninguno la pide. Al contrario, los dos empujan a un solo origen —arquitectura
  dice que la pantalla son *"archivos quietos"* y que con Next.js serían **dos**
  servidores encendidos en la nube "en vez de uno"; el roadmap describe el paso 2
  como *"una ruta, local"* y el 7 como subir *"la tubería entera"*—. La tarea
  venía de una previsión razonable ("navegador y servidor, seguro hacen falta
  permisos de origen") que no aplica a esta forma de montarlo. Es PI-2 en su
  forma más literal: **la pieza que no se añade no puede fallar, ni hay que
  entenderla, ni mantenerla, ni rehacerla en el paso 5.**
  Y mismo origen en local que en la nube quita una diferencia entre desarrollo y
  producción — de esas que solo se descubren el día del despliegue.
  ⚠️ **Si algún día vuelve a hacer falta CORS** —una pantalla servida aparte, u
  otro cliente— la regla ya está pensada y no se rediscute: **lista de orígenes
  explícita, nunca `allow_origins=["*"]`**. Tres razones. La que no es opinable:
  🚨 con `*` el navegador **se niega a enviar credenciales**, así que la
  identidad del paso 5 no viajaría. Las otras dos: con `*` cualquier página del
  mundo puede montar su pantalla encima de `/practice` y gastar la llave (regla
  5, minimizar factura), y contradice la regla 3, denegar por defecto.
  ⚠️ Y un límite que no hay que confundir después: **CORS nunca protege el
  servidor.** `curl` o un script de Python entran igual, porque no hay navegador
  que obedezca la cabecera. Lo que protege el servidor es la autenticación del
  paso 5.
- **Toca:** `app/api.py` (servir los archivos de la pantalla), el paso 3 entero
  —`index.html` y `app.ts` llamarán a `/practice` con ruta relativa, sin nombrar
  host ni puerto— y el paso 7, que sube un solo servicio. Cierra T-029 como
  descartada, no como pendiente.

### [D-010] 2026-08-02 — El detalle completo va al log; al navegador, un mensaje corto y sin rutas

- **Se eligió:** una sola regla para los dos lados del mismo problema en
  `app/api.py`. El `ScoreFileError` se registra **entero** con `logger.error` y
  se contesta un texto fijo sin ruta. Cualquier otro fallo se atrapa también, se
  registra con `logger.exception` —que guarda el traceback— y se contesta otro
  texto fijo. `Exception` y no `BaseException`, para que un Ctrl-C siga apagando
  el servidor en vez de acabar convertido en una respuesta HTTP.
- **Contra:** lo que había, que fallaba por los dos extremos a la vez. `detail=
  str(error)` **contaba de más**: devolvía la ruta absoluta del servidor, medida
  de verdad en la respuesta. Y un `PermissionError` **contaba de menos**: subía
  sin atrapar y salía como un 500 mudo, sin quedar apuntado en ningún sitio.
- **Por qué:** son dos públicos distintos, igual que el idioma en [D-005]. El
  mensaje de `ScoreFileError` se escribió para la terminal, donde saber qué
  archivo abrir es **ayuda**. Fuera del servidor esa misma frase es información
  regalada sobre cómo está organizado por dentro, y quien pregunta no puede
  hacer nada con ella. 🔑 **Quitar el detalle de la respuesta solo vale si el
  detalle queda escrito en otro sitio**; si no, se cambia un problema por otro.
- **Toca:** `app/api.py` y todo error que se añada de aquí en adelante — la
  regla es del proyecto, no de esta ruta. Cuatro tests nuevos en
  `tests/test_api.py`: dos comprueban que la respuesta no lleva la ruta, y dos
  que el detalle sí llegó al log (con `caplog`).

### [D-009] 2026-08-02 — Candado en memoria + temporal con nombre propio para dos peticiones a la vez

- **Se eligió:** dos arreglos distintos en `add_point`, porque son dos fallos
  distintos que el servidor destapó juntos.
  - **Un temporal por escritura**, con `tempfile.mkstemp(dir=path.parent)`. El
    `dir=` es obligatorio: fuera de la carpeta del definitivo, renombrar deja de
    ser atómico. Si el renombrado falla, el temporal se borra antes de dejar
    subir el error.
  - **Un `threading.Lock` que abarca la lectura Y la escritura juntas.**
- **Contra:** el nombre fijo `score.json.tmp` que puso [D-007], y un candado que
  abarcara solo la escritura. Lo segundo parecía suficiente y no lo es.
- **Por qué:** se midió con el servidor levantado y 50 peticiones simultáneas.
  Con el nombre fijo, entre 31 y 39 de 50 devolvían 500: una petición renombraba
  el temporal mientras otra lo sobrescribía, y Windows lo cortaba con
  `PermissionError: Acceso denegado`. Y de 50 puntos esperados el marcador
  guardaba 8, 10 o 12, con hasta 7 personas recibiendo el mismo número — porque
  entre `read_score` y `os.replace` había un hueco donde otra petición leía el
  mismo total.
  🔑 **La escritura atómica y el candado resuelven cosas distintas.** La primera
  protege de UNA escritura cortada por la mitad; el segundo, de DOS escrituras
  pisándose. [D-007] resolvió la primera y no tocaba la segunda. Un candado que
  abarcara solo la escritura tampoco: el problema no está en escribir, está en
  el hueco entre leer y escribir.
  Nada de esto se veía en la terminal, donde escribía una persona sola, ni en
  los tests, porque `TestClient` manda las peticiones de una en una.
- **Toca:** `app/tools.py` (`_SCORE_LOCK`, `add_point`) y cuatro tests nuevos con
  hilos de verdad en `tests/test_tools.py`. Deja la suposición [A-002]: el
  candado vale dentro de **un solo proceso**. El mismo patrón vuelve en el paso
  4, cuando el marcador pase a ser uno por persona.

### [D-008] 2026-08-02 — El tutor devuelve tres piezas separadas, no un texto cocinado

- **Se eligió:** que `respond` devuelva un `TutorReply` —un `dataclass` congelado
  con `verdict`, `words` y `score`— en vez de la cadena `"veredicto\nWords: 3\n
  Score: 7"` que devolvía antes. La ruta `POST /practice` publica esas mismas
  tres claves en su JSON. Quien junta las piezas en un texto es quien las va a
  mostrar: hoy `main.py`, mañana la pantalla del paso 3.
- **Contra:** dejar la cadena ya armada, que era lo que había y funcionaba
  perfectamente para la terminal.
- **Por qué:** el destinatario cambia en el paso 3. Un texto cocinado solo le
  sirve a quien va a imprimirlo tal cual; a `app.ts` lo deja sin opciones —no
  puede pintar el marcador en su sitio, ni resaltar el veredicto, solo volcarlo
  entero—. 🔑 **El agente manda los ingredientes, no el plato servido:** la
  presentación es de quien tiene delante a la persona, no del que calcula.
  Se hizo ahora y no en el paso 3 porque cambiar el contrato con la pantalla ya
  escrita cuesta el doble. El `frozen=True` es aparte: una vez contestado, nadie
  cambia el veredicto por el camino.
- **Toca:** `app/english_tutor.py` (`TutorReply`, `respond`), `app/api.py`
  (`PracticeResponse`), `main.py` (que ahora arma el texto él), y los tests de
  ambos. Fija el contrato que leerá `app.ts` en el paso 3.

### [D-007] 2026-08-02 — El marcador se escribe al lado y se renombra encima (escritura atómica)

- **Se eligió:** que `add_point` escriba el total en un archivo temporal de la
  misma carpeta (`score.json.tmp`) y luego lo mueva encima del bueno con
  `os.replace`. El temporal va **en la misma carpeta**, no en la de temporales
  del sistema, y se usa `os.replace` y no `Path.rename`.
- **Contra:** dejar el `write_text` de siempre, que era lo que había. También se
  descartó envolver la escritura en un `try/except` que restaurara el archivo
  viejo: eso no cubre el caso que importa —un corte de luz no ejecuta el
  `except`—, y añade código para no resolver nada.
- **Por qué:** `write_text` hace dos cosas seguidas, vaciar el archivo y luego
  llenarlo, y entre las dos hay un instante. Un Ctrl-C o un corte justo ahí deja
  el marcador partido. Esto cierra la causa de raíz que [D-006] dejó abierta:
  aquel arreglo enseña a **leer** un archivo roto sin pisarlo, pero el archivo
  roto lo estábamos creando nosotros. Renombrar es **una sola** operación del
  sistema de archivos: o pasó entera o no pasó, así que ante un corte queda el
  marcador viejo entero o el nuevo entero, nunca un pedazo.
  Los dos detalles finos tienen su razón: renombrar solo es atómico **dentro
  del mismo disco** —cruzar de disco lo convierte en copiar y borrar, que es
  justo lo que se evita—, y `Path.rename` revienta en Windows si el destino ya
  existe, mientras que `os.replace` pisa igual en Windows y en Linux.
- **Toca:** `app/tools.py` (`add_point`) y dos tests nuevos en
  `tests/test_tools.py`: uno comprueba que no queda basura `.tmp`, y el otro
  simula el corte de luz reventando `os.replace` con `monkeypatch` y verifica
  que el marcador viejo sigue legible. El mismo patrón se repetirá en el paso 4,
  cuando el marcador pase a ser uno por persona.
  ⚠️ Un corte real sí puede dejar un `.tmp` huérfano en disco. Es inofensivo: la
  siguiente escritura lo pisa, y `read_score` ni lo mira.

### [D-006] 2026-08-02 — El marcador roto avisa con `ScoreFileError`; ausente sigue siendo 0

- **Se eligió:** separar los dos casos que hasta hoy se confundían.
  - **Ausente** (no hay archivo) → `0`, y a seguir. Es el primer día.
  - **Roto** (existe pero no se entiende) → excepción propia `ScoreFileError`,
    con mensaje en español que nombra el archivo y dice qué le pasa.
  - `read_score` valida tres cosas: que sea JSON, que tenga la clave `score`, y
    que su valor sea un entero de verdad — descartando `bool`, que en Python
    hereda de `int` y colaría un `true` por un `1`.
  - `add_point` **no atrapa** el error: lo deja subir. Como lee antes de
    escribir, la escritura ni se intenta y el archivo roto queda intacto.
  - `main.py` sí lo atrapa, imprime el mensaje y sale. Es la única lógica que
    le corresponde, porque presentar errores a una persona es su trabajo.
- **Contra:** devolver `0` cuando el archivo no se puede leer, que era el camino
  fácil y el que no habría necesitado excepción ninguna. También se descartó
  dejar subir el `JSONDecodeError` de la librería estándar tal cual.
- **Por qué:** devolver `0` en silencio le diría "tienes cero puntos" a alguien
  que tenía seis, y encima le pisaría el archivo con un `1` en el siguiente
  intento. 🔑 **Nunca sobrescribas un dato que no lograste entender:** mientras
  el archivo roto siga entero, su marcador es recuperable a mano; en cuanto se
  pisa, ya no. Se comprobó de verdad — con el archivo partido a la mitad
  todavía se lee `"score": 6` dentro.
  Y la excepción es propia, no la de `json`, porque en el paso 2 FastAPI tiene
  que distinguir "el marcador está roto" —que es un 500 con su mensaje— de
  cualquier otro fallo. `JSONDecodeError` solo dice que algún JSON, en algún
  sitio, no se pudo leer.
- **Toca:** `app/tools.py` (`ScoreFileError`, `read_score`, `add_point`),
  `main.py` (el `try/except`), los 8 tests nuevos de `tests/test_tools.py`, y el
  manejo de errores del paso 2. La causa de raíz —`write_text` no es atómico, así
  que este arreglo curaba la lectura del archivo roto pero no impedía crearlo—
  quedó cerrada el mismo día en [D-007].

### [D-005] 2026-08-02 — Nombres en inglés, contenido en español

- **Se eligió:** partir el idioma por su función, no por el archivo.
  - **En inglés** lo que es *identificador*: funciones, variables, archivos,
    carpetas, ramas y mensajes de commit. Y los textos que ve quien usa la app,
    porque es una app para practicar inglés.
  - **En español** lo que es *explicación*: comentarios, docstrings, la
    conversación del chat, y los mensajes de error o de sistema.
  - Consecuencia inmediata: el agente es `english_tutor`, con guion bajo. Con
    guion no se puede importar — `import english-tutor` es un error de sintaxis,
    porque Python lee el guion como una resta.
- **Contra:** nombrar todo en español, que era el camino por defecto viniendo de
  un `CLAUDE.md` y un `_context/` escritos enteros en español.
- **Por qué:** son dos públicos distintos. El identificador lo lee Python, lo leen
  las librerías y lo lee cualquiera que abra el repo; ahí el inglés es el idioma
  franco y evita el híbrido feo (`contar_words`, `leer_score`). La explicación la
  lee quien está aprendiendo, y en su idioma se entiende mejor. El error de
  sistema es explicación, no interfaz: cuando algo se rompe, tiene que entenderse
  rápido y sin traducir.
- **Toca:** todo el código que se escriba desde el paso 1. Renombra los contratos
  acordados: `count_words`, `judge_grammar`, `read_score`, `add_point`,
  `respond`, y los archivos `app/english_tutor.py`, `app/tools.py`,
  `data/score.json`. Queda escrito en `CLAUDE.md`, sección "Cómo se escribe el
  código", como principio **PI-5**.

### [D-004] 2026-08-02 — El protocolo de inicio lee `_context/` siempre, no a demanda

- **Se eligió:** añadir `_context/scope.md` y `_context/roadmap.md` a la lectura
  obligatoria del Paso 1 de `protocol-start`, junto a `progress.md` y `tasks.md`.
  Encima, una regla que manda sobre todas: lo que el reporte diga sobre **qué es**
  el proyecto tiene que salir de un archivo abierto en esa misma corrida; si no
  está escrito, se dice "no está registrado". En `session-starter` se partió el
  límite de "no inventes" en tres: no inventar el proyecto, no dar un paso por
  completado con tareas abiertas de ese paso, y no recomendar prioridades.
- **Contra:** dejar `_context/` fuera del protocolo, como estaba, y confiar en que
  el agente lo abriera si lo necesitaba.
- **Por qué:** el agente arranca en frío y solo veía el *relato* del avance, nunca
  la *definición* del proyecto. Sin el ancla, el hueco lo rellena con lo que suele
  llevar un proyecto de este tipo — y suena convincente, que es lo peligroso. Los
  dos archivos son cortos: leerlos siempre cuesta poco y el reporte pasa a ser
  verificable. Lo de las prioridades venía de la corrida real de hoy, donde el
  reporte recomendó saltarse cuatro tareas abiertas: esa llamada es del usuario.
- **Toca:** `.claude/skills/protocol-start/SKILL.md` (Paso 1) y
  `.claude/agents/session-starter.md` (Límites). Las descripciones del frontmatter
  de ambos se actualizaron el mismo día para nombrar las tres fuentes reales —`git`,
  `_persistence/` y `_context/`— cerrando la T-009.

### [D-003] 2026-08-02 — Recuperar 4 principios de ingeniería de un `CLAUDE.md` anterior

- **Se eligió:** llevar a `CLAUDE.md`, en una sección propia "Cómo se escribe el
  código", cuatro principios de un `CLAUDE.md` genérico de proyectos IA/DS:
  razonar sin decidir en silencio, simplicidad primero, cambios quirúrgicos y
  "terminado = visto funcionando".
- **Contra:** copiar los seis originales tal cual.
  - Se descartó **"slices verticales / tracer bullet"**: el roadmap ya *es* eso
    —tubería completa con agente falso, modelo en el paso 8, "córrelo antes de
    seguir"—. Repetirlo sería duplicar.
  - Se descartó **"sin decisiones silenciosas"** como principio aparte: decía lo
    mismo que "razona antes de actuar", y su parte de documentar ya la cubre este
    archivo.
  - Se reescribió **"toda tarea tiene un test, sin excepción"**: la pantalla del
    paso 3 no se prueba con un test unitario. Quedó como "donde hay lógica, un
    test; donde hay pantalla, correrla".
- **Por qué:** `CLAUDE.md` prometía "la FORMA es de producto: estructura,
  commits, tests, frenos" sin ninguna regla detrás. Era una promesa sin cobrar.
  Y nada frenaba el refactor no pedido, que es justo lo que ensucia el `git diff`
  del que vive `session-closer`.
- **Toca:** todo el código que se escriba desde el paso 1.

### [D-002] 2026-08-02 — Los cuatro archivos del porqué los escribe la sesión principal, no el closer

- **Se eligió:** partir `_persistence/` por origen de la información.
  `progress.md` y `tasks.md` los escribe `session-closer` al cerrar; `decisions`,
  `assumptions`, `constraints` y `lessons` los escribe la sesión principal, en el
  momento en que las cosas pasan. El closer solo los **revisa** y señala huecos.
- **Contra:** que el closer actualizara los seis al final del día, como estaba
  planteado al principio.
- **Por qué:** lo que se hizo queda en el `git diff` y se puede reconstruir sin
  haber estado presente. Lo que se **decidió** no queda en ningún lado: nace en la
  conversación y ahí se muere. El closer arranca en frío, así que escribir esos
  cuatro sería inventar. Además, el porqué es lo primero que se evapora: anotarlo
  tres horas después es anotarlo a medias.
- **Toca:** `CLAUDE.md` (sección Persistencia), `protocol-close` (Paso 5) y el
  reparto de trabajo entre la sesión principal y `session-closer`.

### [D-001] 2026-08-02 — La skill de inicio se llama `protocol-start`, no `protocol-close`

- **Se eligió:** `protocol-start` para el protocolo de inicio de sesión.
- **Contra:** `protocol-close`, que fue el nombre con el que se creó.
- **Por qué:** el nombre describía un cierre y el contenido era el arranque. El
  nombre quedó libre para lo que de verdad lo necesitaba: el protocolo de cierre,
  creado después. Hoy el par es simétrico —`protocol-start` / `protocol-close`—
  y cada agente tiene el suyo.
- **Toca:** `.claude/skills/`, y el cuerpo de `session-starter`, que invoca la
  skill por su nombre.

<!-- La más reciente arriba. Formato:

### [D-001] 2026-08-02 — <qué se decidió, en una línea>

- **Se eligió:** <la opción>
- **Contra:** <las alternativas descartadas>
- **Por qué:** <la razón, no el resumen>
- **Toca:** <qué parte del proyecto condiciona>

-->
