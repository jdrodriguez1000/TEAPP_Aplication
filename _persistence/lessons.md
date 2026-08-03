# Lecciones aprendidas — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [L-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

| id | fecha | qué se aprendió | a raíz de |
|---|---|---|---|
| L-006 | 2026-08-03 | El cierre se cumplió entero y el trabajo se quedó sin subir: si el hash no está en `origin`, no hubo cierre | la revisión cruzada del paso 4 |
| L-005 | 2026-08-03 | Buscar una palabra en un archivo entero no es comprobar el código: los comentarios también cuentan | el primer test de la pantalla, paso 3 |
| L-004 | 2026-08-02 | Una prueba que el código roto también pasa no prueba nada | validar el arreglo de concurrencia del paso 2 |
| L-003 | 2026-08-02 | 45 tests en verde no vieron un fallo que rompía 7 de cada 10 peticiones | la revisión externa del paso 2 |
| L-002 | 2026-08-02 | `pip install` sin versión fijada no da la misma versión dos veces | crear el `.venv` del paso 1 |
| L-001 | 2026-08-02 | La consola de Windows no pinta caracteres fuera de ASCII | correr `main.py` por primera vez |

---

## Entradas

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
