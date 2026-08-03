# Lecciones aprendidas — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [L-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

| id | fecha | qué se aprendió | a raíz de |
|---|---|---|---|
| L-008 | 2026-08-03 | Se comparó la opción rival en su versión floja y se le ganó a esa: eso no es comparar, es elegir y buscar razones después | revisar dónde vive el control del `.js`, T-037 |
| L-007 | 2026-08-03 | La comprobación que mide **de más**: `diff -r` gritaba "viejo" con el repo correcto. Un control se mide dos veces —con el fallo puesto y sin él— o no se midió | escribir el control del `.js` compilado, T-037 |
| L-006 | 2026-08-03 | El cierre se cumplió entero y el trabajo se quedó sin subir: si el hash no está en `origin`, no hubo cierre | la revisión cruzada del paso 4 |
| L-005 | 2026-08-03 | Buscar una palabra en un archivo entero no es comprobar el código: los comentarios también cuentan | el primer test de la pantalla, paso 3 |
| L-004 | 2026-08-02 | Una prueba que el código roto también pasa no prueba nada | validar el arreglo de concurrencia del paso 2 |
| L-003 | 2026-08-02 | 45 tests en verde no vieron un fallo que rompía 7 de cada 10 peticiones | la revisión externa del paso 2 |
| L-002 | 2026-08-02 | `pip install` sin versión fijada no da la misma versión dos veces | crear el `.venv` del paso 1 |
| L-001 | 2026-08-02 | La consola de Windows no pinta caracteres fuera de ASCII | correr `main.py` por primera vez |

---

## Entradas

### [L-008] 2026-08-03 — Se comparó la opción rival en su versión floja y se le ganó a esa

- **Qué pasó:** había que decidir dónde vivía el control del `.js`: en `pytest` o
  en el cierre. Se describió la opción del cierre como "un comando que tú corres
  antes de commitear" y se rechazó con "un freno que depende de tu memoria no es
  un freno". Nadie había propuesto esa versión: `.claude/agents/session-closer.md`
  existe y ya dispara controles solo, sin memoria de nadie.
- **Por qué pasó:** el principio invocado era correcto, y eso fue lo que lo
  escondió. Un argumento válido aplicado a una versión que nadie defendía suena
  igual de bien que uno bueno. 🔑 **Ganarle a la peor versión de la otra opción
  no es compararlas: es elegir primero y buscar razones después.**
- **Qué se hace distinto:** antes de recomendar entre dos caminos, escribir la
  opción rival **como la defendería quien la prefiere**, con lo mejor que tenga
  a favor. Si al lado de esa versión la recomendación se cae, es que no había
  recomendación. Aquí se cayó: el control acabó en el cierre, ver [D-017].
  Y ojo con el otro lado del mismo error — cuando el argumento propio se aplica
  también a la propia propuesta, hay que decirlo: `pytest` tampoco avisa si no
  corres los tests.

### [L-007] 2026-08-03 — La comprobación que mide de más: gritaba "viejo" con el repo correcto

- **Qué pasó:** el primer control del `.js` compilado usaba `diff -r` entre la
  carpeta que produce `tsc` y `app/static/`. Con el `.js` **perfectamente al
  día**, salía `Only in app/static: index.html` y el control lo declaraba viejo.
  La causa: `diff -r` compara en **las dos direcciones**, y `app/static/` es una
  carpeta mixta —también vive ahí `index.html`, escrito a mano, que ningún
  compilador va a generar nunca.
- **Por qué pasó:** se comprobó que el control **detectaba el fallo** y no se
  comprobó que **dejara pasar lo correcto**. Es el mismo animal de [L-003],
  [L-004], [L-005] y [L-006], pero por la cara que faltaba: las anteriores medían
  **de menos** —pasaban con el defecto puesto—; esta medía **de más**.
  🔑 **Y medir de más es peor de una forma concreta:** una alarma que nunca suena
  te deja ciego; una que suena **todas las noches con el repo correcto te entrena
  a apagarla**, y el día que suene de verdad ya le enseñaste a la gente a no
  mirar. La primera falla sola; la segunda se lleva por delante tu atención.
- **Lo doloroso:** la lección ya estaba escrita en este repo, por quien la volvió
  a incumplir un paso antes. `tests/test_tools.py`, en
  `test_normalize_user_accepts_ordinary_names`: *"El freno tiene que dejar pasar
  lo normal. Un validador que rechaza todo también pasaría los tests de arriba."*
  `diff -r` era exactamente ese validador que rechaza todo. **Saber un principio
  y aplicárselo a lo que estás escribiendo ahora son dos habilidades distintas**,
  y por eso el arreglo no puede ser "acordarse mejor" — [L-006] otra vez.
- **Qué se hace distinto:**
  1. **Un control se mide dos veces o no se midió:** una corrida con el fallo
     puesto y otra con el caso bueno. Las dos, en pantalla.
  2. **Y se mide en el caso que el diseño presume manejar.** La primera versión
     se midió con **un** archivo generado, y con uno solo el bug del bucle no
     puede aparecer: `for` devuelve el código del **último** comando, no de
     "alguno falló". Se destapó al probar con dos, con el que difiere delante.
  3. **La lista de lo que se vigila la declara el compilador**, no una lista
     negra de excepciones: se recorre lo que hay en su carpeta de salida. Una
     lista negra hay que mantenerla; esta se mantiene sola.
  4. **Detectar, informar y devolver éxito es no tener control.** Cada rama que
     encuentra algo mal levanta la bandera; un `echo` no frena nada.
  5. **El texto que se revisa tiene que ser el texto que se corrió.** La versión
     medida llevaba bandera y la que se pasó a revisar no: se "limpió" al
     transcribirla. El control vive en un archivo y se corre ese archivo.

### [L-006] 2026-08-03 — El cierre se cumplió entero y el trabajo se quedó sin subir: si el hash no está en `origin`, no hubo cierre

- **Qué pasó:** el cierre del paso 4 terminó con su commit y su hash, `f015a01`.
  La regla de cierre pedía exactamente eso, y se cumplió. Pero `origin/main`
  seguía en `460b04f`: el commit existía **solo en este disco**. Lo descubrió una
  revisión cruzada desde otra terminal haciendo `git fetch`. Un disco roto esa
  noche se habría llevado el paso 4 entero, con el cierre marcado como correcto.
- **Por qué pasó:** la regla vieja —nacida en la sesión 31— era *"si no hay hash,
  no hubo cierre"*. Esa regla comprueba que **existe un commit**, y de ahí se
  dedujo que el trabajo estaba a salvo. Son dos cosas distintas: un commit es
  local. 🔑 **Un control puede cumplirse entero y no comprobar lo que su nombre
  promete.** Cumplirlo daba tranquilidad y la tranquilidad era falsa, que es
  peor que no tener control: un hueco conocido se vigila, uno tapado no.
- **Y de qué familia es este fallo:** es el mismo defecto de [L-003], [L-004] y
  [L-005] —*la comprobación mide algo distinto de lo que dice medir*—, pero esta
  vez **no estaba en el código: estaba en el protocolo**. Sexta aparición del
  patrón, y la primera fuera de los tests. Donde haya un control hay que
  preguntarle qué mide de verdad, y los protocolos son controles.
- **Qué se hace distinto:** la regla queda corregida a **"si el hash no está en
  `origin`, no hubo cierre"**, y se comprueba con:

  ```bash
  git status -sb
  ```

  Si la primera línea dice **`ahead`**, no terminaste. El cierre acaba cuando esa
  palabra no aparece — no cuando aparece un hash.

### [L-005] 2026-08-03 — Buscar una palabra en un archivo entero no es comprobar el código: los comentarios también cuentan

- **Qué pasó:** la pantalla del paso 3 tiene que llamar a `/practice` con ruta
  relativa, sin nombrar host ni puerto — un `http://localhost:8000` escrito a
  mano funcionaría hoy y se rompería el día del despliegue. Para fijarlo se
  escribió un test que pedía el `app.js` compilado y comprobaba
  `assert "localhost" not in script`. Falló al primer intento, con el código
  **correcto**.
- **Por qué pasó:** la palabra `localhost` sí estaba en el archivo — dentro de un
  comentario que explica justamente por qué NO se usa. El compilador conserva los
  comentarios en la salida. El test decía medir "cómo llama la pantalla al
  servidor" y en realidad medía "qué letras aparecen en el archivo", incluidas
  las de la prosa que nadie ejecuta.
- **Qué se hizo:** apuntar a la llamada en sí, no al archivo:
  `assert 'fetch("/practice"' in script` y `assert 'fetch("http' not in script`.
  Eso sí distingue entre lo que el navegador ejecuta y lo que solo lee un humano.
- **Qué se hace distinto:** 🔑 **cuando un test busca texto dentro de un archivo,
  el patrón tiene que incluir la parte que lo hace código.** `"localhost"` cabe en
  un comentario; `fetch("http` no. Es la misma familia de [L-003] y [L-004] vista
  desde otro ángulo: allí el test no creaba el estado que decía probar, aquí no
  mira el sitio que dice mirar. En los tres casos el síntoma es el mismo —**la
  prueba mide algo distinto de lo que su nombre promete**— y solo se descubre
  preguntándose qué tendría que pasar para que fallara.
- **Y lo que salió bien:** falló al primer intento y por eso se encontró. Un test
  que hubiera pasado por casualidad —si el comentario no llega a existir— habría
  quedado ahí, dando una confianza falsa hasta el paso 7.

### [L-004] 2026-08-02 — Una prueba que el código roto también pasa no prueba nada

- **Qué pasó:** para comprobar el arreglo de concurrencia se montó una prueba de
  50 peticiones simultáneas por HTTP, con PowerShell. Dio **0 errores y marcador
  50**: perfecto. Pero por un puerto ocupado resultó que quien había contestado
  era el servidor **viejo**, sin el arreglo. Y también había dado 50 de 50.
- **Por qué pasó:** las 50 peticiones no salían lo bastante juntas. PowerShell
  tarda en arrancar cada hilo, así que llegaban en fila y nunca llegaron a
  pisarse. La prueba medía otra cosa distinta de la que decía medir.
- **Qué se hizo:** correr el `add_point` viejo y el nuevo, uno al lado del otro,
  con 50 hilos de Python sobre el mismo archivo. El viejo: **45 errores de 50**,
  marcador 1, números repetidos. El nuevo: 0 errores, marcador 50, 50 números
  distintos. Eso sí es una prueba.
- **Qué se hace distinto:** 🔑 **antes de fiarse de una prueba, comprobar que
  falla con el código roto.** Una prueba que pasa en los dos casos no está
  midiendo el arreglo, y da una confianza que no existe. Es el mismo criterio
  que ya está en `CLAUDE.md` como PI-4 —terminado = visto funcionando— llevado
  un paso más: **visto fallando cuando debía fallar.**
- **Y una segunda:** al levantar un servidor, comprobar en su log que dice
  "Uvicorn running on…". Si dice `[Errno 10048] error while attempting to bind`,
  el que contesta es otro, y todo lo que se mida después es sobre el código
  equivocado.

### [L-003] 2026-08-02 — 45 tests en verde no vieron un fallo que rompía 7 de cada 10 peticiones

- **Qué pasó:** el paso 2 se cerró con 45 tests en verde y el servidor probado a
  mano. Una revisión externa lo levantó con **50 peticiones a la vez** y entre 31
  y 39 devolvieron error 500. De 50 puntos esperados, el marcador guardaba 8.
- **Por qué pasó:** `TestClient` manda las peticiones **de una en una**. Todos
  los tests, y todas las pruebas a mano, ejercitaban un solo escritor. Con un
  solo escritor el código era correcto — el fallo no estaba en las piezas, estaba
  en dos piezas ocurriendo a la vez, que es un estado que ninguna prueba creaba.
- **Qué se hace distinto:** 🔑 **un test en verde no dice "el código está bien",
  dice "el código está bien para lo que este test hace".** Al cambiar de terminal
  a servidor cambió una suposición de fondo —de un escritor a muchos— y ninguna
  prueba se enteró. Cuando cambie esa clase de suposición, hay que escribir el
  test que la ejercite: aquí, hilos de verdad sobre el mismo archivo.
- **Cuándo vuelve a pasar:** en el paso 4 (memoria por persona) y en el paso 7
  (la nube decide cuántos procesos hay). Anotado como suposición [A-002].

### [L-002] 2026-08-02 — `pip install` sin versión fijada no da la misma versión dos veces

- **Qué pasó:** al crear el entorno virtual, `pip install pytest` instaló
  **pytest 9.1.1**. El Python global de la misma máquina tenía **8.1.1**. Dos
  versiones distintas, el mismo día, sin haber hecho nada raro.
- **Por qué pasó:** `pip install pytest` no pide "pytest": pide "el pytest más
  nuevo que haya hoy". La respuesta cambia con el calendario. El global se
  instaló hace meses; el del entorno, hoy.
- **Qué se hace distinto:** toda dependencia va en `requirements.txt` con `==` y
  versión exacta. Se instala con `pip install -r requirements.txt`, nunca por
  nombre suelto. Sin eso, un fallo que solo aparece en una máquina —o solo en el
  servidor del paso 7— se vuelve casi imposible de encontrar: el código es el
  mismo y las librerías no.

### [L-001] 2026-08-02 — La consola de Windows no pinta caracteres fuera de ASCII

- **Qué pasó:** `main.py` imprimía `TEAPP — write a sentence...` con guion largo,
  y en pantalla salió `TEAPP ? write a sentence...`. Los tests no lo detectaron:
  pasaban los 14. Se vio solo al correr la app de verdad.
- **Por qué pasó:** la consola de Windows no usa UTF-8 por defecto, y el guion
  largo no existe en su tabla de caracteres. Lo sustituye por `?`. El código era
  correcto; lo que fallaba era el sitio donde se imprimía.
- **Qué se hace distinto:** en lo que se imprime por terminal, solo ASCII. Y la
  lección de fondo, que es la que importa: **PI-4 no es burocracia.** Los tests
  daban verde sobre un texto que en pantalla salía roto. Un test comprueba lo que
  la función devuelve, no lo que la persona ve. Por eso "terminado = visto
  funcionando" pide las dos cosas, no una.

<!-- La más reciente arriba. Formato:

### [L-001] 2026-08-02 — <la lección, en una línea>

- **Qué pasó:** <el fallo o la sorpresa>
- **Por qué pasó:** <la causa, ya entendida>
- **Qué se hace distinto:** <la regla que queda para adelante>

-->
