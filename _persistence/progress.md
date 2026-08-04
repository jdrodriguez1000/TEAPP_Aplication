# Avance — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [S-000]`. Búscala con `grep`, no leas el archivo entero.

## Estado actual

| | |
|---|---|
| **paso** | 6 de 9 — completo. Los cuatro frenos de producción están escritos y vistos funcionando con uvicorn real: cuota por persona y día, timeout del tutor, tope al tamaño de la frase, motivo del frenazo |
| **última sesión** | 2026-08-04 |
| **siguiente acción** | Empezar el paso 7 del roadmap: la nube. ⚠️ Alarma de facturación PRIMERO, luego subir. Antes de abrir la cuenta, revisar las deudas que quedaron con dueño para el paso 7: `T-053` (tope de intentos en `/login`), `T-054` (tope de tamaño de cuerpo en el servidor de delante), `T-033`, `T-046`, `T-050`, `T-051`, `T-052` |

## Índice

| id | fecha | qué avanzó | paso |
|---|---|---|---|
| S-012 | 2026-08-04 | Paso 6 completo: los cuatro frenos de producción, `T-038` resuelta. `app/quota.py` (nuevo) cobra por persona y por día, con reloj y tope inyectados. `app/api.py` suma `MAX_SENTENCE_LENGTH` (422), timeout del tutor en `ThreadPoolExecutor` (504) y el motivo del frenazo en cada 429/504. Una revisión externa encontró cinco huecos y los cinco se cerraron: la carrera de medianoche en `spend`, el cobro por trabajo que nunca salió de la cola, el marcador subiendo tras un 504 (decidido, no arreglado), un `logger.info` que el handler de último recurso silenciaba, y `/login` sin tope de intentos (anotado como deuda con dueño). De 192 a **257 tests pasando**, `tests/test_quota.py` nuevo | 6 |
| S-011 | 2026-08-04 | T-047 resuelta: `[C-001]` medida de verdad. 192 tests verdes con la red cortada, 5 controles del portero verdes. Entra `tests/no_network.py` (portero, autouse), `tests/check_no_network.py` (sus controles) y el enganche en `tests/conftest.py` (`D-022`). Hueco cerrado: `connect_ex` atravesaba el portero. `[C-001]` reescrita: no prohíbe salir a internet, prohíbe salir **a buscar algo que falta** | 6 |
| S-010 | 2026-08-04 | Paso 5 completo: identidad verificada. `app/accounts.py` (credenciales con `scrypt`), `app/sessions.py` (cookie firmada con `hmac`), `app/config.py` (`.env`). `PracticeRequest` pierde `user`; `/register`, `/login`, `/logout`, `/me` nuevas. Pantalla e `main.py` piden contraseña. 192 tests pasando, corrida real con uvicorn+curl, y un fallo real de `/logout` cazado y arreglado (`L-010`) | 5 |
| S-009 | 2026-08-04 | T-049 resuelta: el control del `.js` se mueve del Paso 5b al Paso 2b de `protocol-close` (antes de escribir `tasks.md`); el resultado del push queda escrito como imposibilidad lógica, no como pendiente. `protocol-start` pasa de `git status --short` a `-sb` — el primero no imprimía la línea de la rama | 5 |
| S-008 | 2026-08-03 | T-037 resuelta: nuevo Paso 5b en `protocol-close` comprueba que `app/static/app.js` es el compilado de `frontend/app.ts`, disparado desde `session-closer` antes del commit. `test_the_compiled_script_is_served` se renombró y ya dice qué no mide. Primera corrida real del Paso 5b: verde, `.js` al día | 3 |
| S-007 | 2026-08-03 | Paso 4 completo: marcador por persona en `data/users/<nombre>.json`, `normalize_user` con cuatro frenos, `data/score.json` global borrado, 121 tests pasando | 4 |
| S-006 | 2026-08-03 | Paso 3 completo: `index.html` + `app.ts` compilado, FastAPI sirve la pantalla en el mismo origen, CORS descartado (T-029), 57 tests pasando | 3 |
| S-005 | 2026-08-02 | Paso 2 completo: `app/api.py` con FastAPI, `respond` devuelve `TutorReply`, dos fallos de concurrencia arreglados, 53 tests pasando | 2 |
| S-004 | 2026-08-02 | Dos arreglos de robustez sobre el paso 1: marcador roto y `count_words` con no-texto, 30 tests pasando | 1 |
| S-003 | 2026-08-02 | Paso 1 completo: agente FALSO con 3 herramientas, 14 tests pasando | 1 |
| S-002 | 2026-08-02 | Cierre del paso 0: T-006 a T-009 resueltas | 0 |
| S-001 | 2026-08-02 | Repositorio y esqueleto completos | 0 |

---

## Entradas

### [S-012] 2026-08-04 — Paso 6 completo: los cuatro frenos de producción

- **Paso:** 6 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/quota.py` (nuevo): cuota diaria por persona en `data/quota/<nombre>.json`.
    Reloj (`now`), tope (`limit`) y carpeta (`quota_dir`) inyectados, resueltos
    dentro de cada función y no en la firma. `today()` exige zona horaria y usa
    un offset fijo −05:00 (`D-024`) — `ZoneInfo("America/Bogota")` revienta en
    Windows, comprobado. `spend()` cobra **antes** de llamar al tutor (`D-023`)
    y `refund()` devuelve solo lo que nunca llegó a empezar. Candado sobre leer
    y escribir juntos, como `add_point`.
  - `app/api.py`: `MAX_SENTENCE_LENGTH = 500` (422 con cuánto llegó y cuánto
    cabe). El tutor corre en un `ThreadPoolExecutor(max_workers=40)` propio
    (`_TUTOR_POOL`), con `TUTOR_TIMEOUT_SECONDS = 10.0` — pasado ese tiempo,
    504, y `future.cancel()` decide si se devuelve la cuota (nunca empezó) o se
    queda cobrada (ya estaba corriendo). Los 429 y 504 llevan el motivo en la
    respuesta: cuánto se gastó, el tope, el día.
  - Una revisión externa encontró cinco huecos, cerrados los cinco:
    1. La carrera de medianoche en `spend` — preguntaba el día dos veces y
       podía escribir bajo el día viejo. Arreglado preguntándolo una sola vez.
    2. El cobro por trabajo que nunca salió de la cola del pool —
       `result(timeout=)` cuenta desde que se llama, no desde que arranca.
       Medido: 23 peticiones a la vez, 20 llegaron al tutor, 3 pagaron un 504
       por nada. Arreglado con `future.cancel()` + `refund()`.
    3. El marcador sube después del 504 si el tutor ya había empezado —
       **decidido dejarlo así** (el marcador cuenta frases practicadas,
       `A-001`), ahora escrito y con test.
    4. Un `logger.info` que el handler de último recurso de Python silencia
       (`L-012`, cierra `A-003`) — se sube a `warning`.
    5. `/login` sin tope de intentos — anotado como deuda con dueño para el
       paso 7 (`D-025`, `A-012`), no arreglado hoy.
  - Tests: de 192 a **257** pasando (`python -m pytest`, corrido en este
    cierre). `tests/test_quota.py` nuevo. `tests/conftest.py` desvía
    `quota.QUOTA_DIR` a una carpeta temporal.
  - `_persistence/decisions.md`: `D-023`, `D-024`, `D-025`.
    `_persistence/assumptions.md`: `A-010`, `A-011`, `A-012`; `A-003` ascendió a
    `lessons.md` (`L-012`) y salió de aquí. `_persistence/lessons.md`: `L-012`,
    `L-013`. `_persistence/constraints.md`: `C-002`.
  - Paso 2b de este cierre: `.js` compilado, al día (`compilar: 0`,
    `comparar: 0`).
- **Siguiente acción:** Empezar el paso 7 del roadmap — la nube. ⚠️ Alarma de
  facturación primero, luego subir. Revisar antes las deudas con dueño:
  `T-053`, `T-054`, `T-033`, `T-046`, `T-050`, `T-051`, `T-052`.

### [S-011] 2026-08-04 — T-047 resuelta: `[C-001]` medida de verdad, con un portero que la vigila cada día

- **Paso:** 6 (deuda de restricción, no de la app) — no mueve el paso general,
  que sigue en 5 completo.
- **Quedó funcionando:**
  - `tests/no_network.py` (nuevo): el portero. Parchea `socket` para que
    cualquier intento de salir a la red reviente en el momento, activo en
    **todos** los tests vía el enganche `autouse` de `tests/conftest.py`.
  - `tests/check_no_network.py` (nuevo): sus cinco controles, fuera de la
    corrida normal de `pytest` a propósito — salen a internet de verdad si el
    portero falla, y eso es justo lo que `C-001` prohíbe.
  - Hueco cerrado: `connect_ex` (devuelve código, no lanza) atravesaba el
    portero sin que se enterara. Parcheado y verificado con una IP literal.
  - Límite escrito en el docstring del portero: no ve subprocesos —`node` y
    `git` son otro proceso, y eso es por construcción, no un pendiente.
  - **Medición del 2026-08-04:** 192 tests verdes con la red cortada; los 5
    controles del portero, verdes. `node_modules/typescript/bin/tsc` en disco
    (v7.0.2), sin descarga.
  - `[C-001]` reescrita: la redacción vieja ("nada de lo que corre en el cierre
    toca la red") era falsa desde que el `git push` entró en el cierre
    (`D-016`) — un push va a GitHub por internet. La nueva dice lo que de
    verdad se quiso decir: "nada sale a internet a buscar algo que le falta".
  - `_persistence/decisions.md`: `D-022` (el portero entra al repo, y con sus
    controles; `C-001` se mide en dos mitades porque el portero no ve
    subprocesos). `_persistence/constraints.md`: `C-001` corregida.
- **Siguiente acción:** Empezar el paso 6 del roadmap — frenos de producción:
  tope de peticiones por persona y por día, timeouts (`T-038`).

### [S-010] 2026-08-04 — Paso 5 completo: identidad verificada

- **Paso:** 5 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/accounts.py` (nuevo): almacén de credenciales en `data/accounts.json`,
    `hashlib.scrypt` con sal por persona, `hmac.compare_digest` al comparar.
  - `app/sessions.py` (nuevo): cookie firmada con `hmac`, caducidad de una
    semana.
  - `app/config.py` (nuevo): lector de `.env`, `require_secret()` y
    `cookie_secure()`.
  - `app/api.py`: rutas nuevas `/register` (201), `/login` (200), `/logout`
    (204) y `/me`; `PracticeRequest` pierde el campo `user` — quien practica
    sale de la cookie firmada (`_current_user`), y no de ningún otro sitio.
  - `frontend/app.ts` + `app/static/index.html`: la casilla "Your name" y el
    `localStorage` del paso 4 desaparecen; entra el formulario de inicio de
    sesión (`signin-form`) y la sección "signed-in". Recompilado a
    `app/static/app.js` — comprobado al día en este cierre (Paso 2b:
    `compilar: 0`, `comparar: 0`).
  - `main.py`: la terminal pide contraseña con `getpass`, cerrando la puerta
    de atrás que creaba marcadores sin credencial.
  - `.env.example`, `README.md`: documentan `TEAPP_SECRET_KEY` y
    `TEAPP_COOKIE_SECURE`.
  - `tests/conftest.py`, `tests/test_accounts.py`, `tests/test_sessions.py`
    (nuevos) y `tests/test_api.py` ampliado: **192 tests pasando** con
    `python -m pytest` (corrido en esta sesión, y también por el usuario:
    192 passed in 5.56s).
  - Corrida real con uvicorn + `curl`, según el traspaso: practicar sin
    sesión → 401; tarjeta con una letra cambiada → 401; tarjeta fabricada a
    mano sin la llave → 401; registrar `JUAN` con `juan` ya existente → 409;
    entrado como `juan` mandando `{"user":"ana"}` en el cuerpo → el punto cae
    en `juan`; contraseña equivocada → 401; `/logout` → 204 y `/me` después →
    401. `main.sign_in` ejercitada sin teclado, seis casos correctos.
    Comprobado en disco que ningún marcador existe sin credencial.
  - Un fallo real encontrado corriendo el servidor de verdad (no lo veía la
    suite): `/logout` devolvía el `Response` inyectado con
    `status_code = None`, y uvicorn reventaba con `KeyError: None`. Arreglado
    y cubierto con `test_logout_answers_the_status_code_it_declares` — ver
    `L-010`.
  - `_persistence/decisions.md`: `D-020` (los cuatro marcadores huérfanos de
    `data/users/` se borran) y `D-021` (contraseña propia y cookie firmada;
    OAuth descartado). `_persistence/assumptions.md`: `A-008` (la llave de
    firma no cambia entre arranques) y `A-009` (la rama `secure=True` nunca se
    ha ejecutado). `_persistence/lessons.md`: `L-010`.
- **Siguiente acción:** Empezar el paso 6 del roadmap — frenos de producción:
  tope de peticiones por persona y por día, timeouts (`T-038`).

### [S-009] 2026-08-04 — T-049 resuelta: el desfase del protocolo de cierre, en dos mitades

- **Paso:** 5 (deuda de protocolo, no de la app) — no mueve el paso general, que
  sigue en 4 completo.
- **Quedó funcionando:**
  - `.claude/skills/protocol-close/SKILL.md`: el control del `.js` se renombró
    de "Paso 5b" a **Paso 2b**, y se movió de después del Paso 4 (`tasks.md`) a
    justo después del Paso 2 (el traspaso). Motivo: el control produce tareas
    —marca una hecha o añade una nueva— y corriendo al final su resultado
    llegaba tarde para anotarse. Queda escrito que va **después** de la puerta
    del Paso 1 (si `git status` está limpio, no hay nada que compilar) y
    **antes** de escribir `tasks.md`.
  - El mismo archivo deja escrito, en el Paso 4, que el resultado del `push`
    **no puede** anotarse en `tasks.md`: para saberlo, el commit —que contiene a
    `tasks.md`— ya tiene que existir. Su sitio son el reporte de hoy y el
    arranque de mañana (`D-019`).
  - `.claude/skills/protocol-start/SKILL.md`: cambió `git status --short` por
    `git status -sb`. El primero no imprime la línea de la rama, así que un
    commit sin subir le resultaba invisible — comprobado en un repo de prueba:
    `--short` no imprimió nada, `-sb` imprimió
    `## main...origin/main [ahead 1]`. La tabla de desfases pasó de dos filas a
    tres.
  - `.claude/agents/session-closer.md`: la referencia al control pasa de "Paso
    5b" a "Paso 2b", con el porqué del movimiento resumido.
  - `tests/test_api.py`: el comentario de `test_the_script_is_served` apunta
    ahora al Paso 2b.
  - `_persistence/decisions.md`: `[D-019]`. `_persistence/lessons.md`: `[L-009]`
    — una regla que vive en dos archivos se corrige en los dos, o no se
    corrigió. `_persistence/assumptions.md`: `[A-007]` — entre el Paso 2b y el
    `git add` no se toca ningún `.ts`.
  - Primera corrida real del Paso 2b en su posición nueva, en este mismo
    cierre: `compilar: 0`, `comparar: 0` — el `.js` sigue al día.
  - 121 tests pasando con `python -m pytest` (según el traspaso; no se
    re-corrieron en este cierre).
- **Siguiente acción:** Empezar el paso 5 del roadmap — identidad de verdad,
  quitando la casilla "Your name" (`D-013`).

### [S-008] 2026-08-03 — T-037 resuelta: el `.js` compilado se vigila en el cierre, no en `pytest`

- **Paso:** 3 de 9 — cierra deuda que venía del paso 3. No mueve el paso general,
  que sigue en 4 completo.
- **Quedó funcionando:**
  - `.claude/skills/protocol-close/SKILL.md`: nuevo **Paso 5b**, antes del
    `git add`. Compila `frontend/*.ts` con el `tsc` local (nunca `npx`, ver
    `C-001`) y compara cada archivo que produjo contra `app/static/`. Dos
    verdades con su propio código de salida — `COMPILAR` y `COMPARAR` — para
    que "no se pudo comprobar" nunca se confunda con "está bien" (`D-017`,
    `D-018`, `L-007`, `L-008`).
  - `.claude/agents/session-closer.md`: nuevo punto en `## Límites` que obliga
    a correr el Paso 5b antes de `git add`, y deja explícito que si falla, el
    cierre **commitea y sube igual**, y la tarea va a "Sin resolver".
  - `tests/test_api.py`: `test_the_compiled_script_is_served` se renombró a
    `test_the_script_is_served`; el comentario ahora dice qué **no** cubre
    (que el `.js` esté al día) y por qué eso no se puede ver desde un test.
  - `_persistence/decisions.md`: `D-017` (el control vive en el cierre, no en
    `pytest`) y `D-018` (un control no puede causar un daño mayor que el que
    previene: el `.js` viejo no cancela el cierre).
  - `_persistence/lessons.md`: `L-007` (la primera versión del control con
    `diff -r` gritaba "viejo" con el repo correcto) y `L-008` (se comparó la
    opción rival en su versión floja, no en la real).
  - `_persistence/constraints.md`: primera entrada del archivo, `C-001` — la
    suite y el cierre no tocan la red.
  - `_persistence/assumptions.md`: `A-006` — que la ruta de `mktemp -d` de Git
    Bash le sirva a `node` sigue sin comprobarse en otra máquina.
  - **Primera corrida real del Paso 5b**, en este mismo cierre: `compilar: 0`,
    `comparar: 0` — el `.js` está al día. Cierra T-048.
  - 121 tests siguen pasando con `python -m pytest`.
- **Siguiente acción:** Empezar el paso 5 del roadmap — identidad de verdad,
  quitando la casilla "Your name" (`D-013`).

### [S-007] 2026-08-03 — Paso 4 completo: marcador por persona en `data/users/<nombre>.json`, `normalize_user` con cuatro frenos, `data/score.json` global borrado, 121 tests pasando

- **Paso:** 4 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/tools.py`: `SCORE_FILE` desaparece, entra `USERS_DIR` (`data/users/`).
    Nueva `normalize_user` — minúsculas + `strip`, y cuatro frenos: vacío, largo
    máximo 32, lista blanca `^[a-z0-9_-]+$`, y nombres reservados de Windows
    (`con`, `prn`, `com1`…). Nueva excepción `InvalidUserError`. Nueva
    `score_file(name, users_dir)`. `read_score` y `add_point` reciben ahora el
    nombre de la persona (`D-014`).
  - `app/english_tutor.py`: `respond(sentence, user)`, sin valor por defecto a
    propósito — un `user="anonimo"` de repuesto taparía el olvido de pasarlo.
  - `app/api.py`: `PracticeRequest` gana el campo `user`; se valida lo primero,
    antes de mirar la frase, y `InvalidUserError` se traduce a 422.
  - `frontend/app.ts` + `app/static/index.html`: casilla "Your name", recordada
    en `localStorage` bajo `teapp.user` (`D-013` — identidad declarada, no
    verificada). Recompilado a `app/static/app.js`.
  - `main.py`: pide el nombre una vez al arrancar, con `input()`.
  - `data/score.json` (el marcador global de 19 puntos del paso 3) se borró, no
    se adoptó (`D-015`).
  - Tests: de 57 a **121**, todos en verde con `python -m pytest` (verificado
    en esta sesión de cierre). Nuevos: recorrido de ruta (`../../CLAUDE.md`,
    etc.), nombres reservados de Windows, normalización, memoria separada por
    persona, y concurrencia entre dos personas a la vez.
  - `README.md` al día con el paso 4.
  - Verificado corriendo de verdad, según el traspaso de la sesión: uvicorn con
    curl (juan/ana separados, `  JUAN  ` cayendo en el mismo archivo, ataques
    de ruta rechazados con 422), terminal con `main.py`, y el usuario lo probó
    en el navegador. `data/users/` en disco confirma `ana.json`, `juan.json`,
    `maria.json` y `pedro.json` — consistente con esa prueba manual.
  - Costo de la sesión: $0,00 — no hay ninguna llamada a la API en el repo.
- **Siguiente acción:** Empezar el paso 5 del roadmap — identidad de verdad.
  Tiene que **quitar** la casilla "Your name", no añadirle nada al lado
  (`D-013`).

### [S-006] 2026-08-03 — Paso 3 completo: `index.html` + `app.ts` compilado, FastAPI sirve la pantalla en el mismo origen, CORS descartado (T-029), 57 tests pasando

- **Paso:** 3 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/api.py`: monta `/static` con `StaticFiles` y sirve `index.html` en
    `GET /` con `FileResponse`. El mismo servidor atiende `/practice`, así que
    hay un solo origen (`D-011`).
  - `frontend/app.ts` (nuevo, fuente que se edita) se compila con `tsc` a
    `app/static/app.js` (generado, versionado en Git porque en la nube no hay
    Node — `D-012`). `package.json` y `tsconfig.json` nuevos en la raíz;
    `typescript` fijado en 7.0.2, `module: "es2020"` tras comprobar que
    `"none"` ya no lo acepta el compilador.
  - `app/static/index.html` (nuevo): la pantalla con el formulario de práctica.
  - Tests: de 53 a **57**, todos en verde con `python -m pytest`. Nuevos en
    `tests/test_api.py`: la pantalla se sirve (200, `text/html`), trae el
    formulario correcto, el `.js` compilado se sirve, y la llamada a
    `/practice` usa ruta relativa (sin `localhost`).
  - Servidor levantado de verdad y comprobado a mano: `GET /` → 200
    `text/html`, `GET /static/app.js` → 200, `POST /practice` → 200 con las
    tres piezas. El usuario confirmó que la pantalla funciona en un navegador
    real.
  - `README.md`: comandos de arranque reales (`npm install`, `npm run build` +
    `uvicorn`) y tabla de qué recompilar según lo que se toque.
  - `T-029` (CORS) se descarta, no queda pendiente: mismo origen, no aplica
    (`D-011`). `T-030` (pantalla) queda hecha.
  - Costo de la sesión: $0,00 — no hay ninguna llamada a la API en el repo.
- **Siguiente acción:** Empezar el paso 4 del roadmap — memoria por persona.

### [S-005] 2026-08-02 — Paso 2 completo: `app/api.py` con FastAPI, `respond` devuelve `TutorReply`, dos fallos de concurrencia arreglados, 53 tests pasando

- **Paso:** 2 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/api.py` (nuevo): ruta `POST /practice` con FastAPI. `PracticeRequest`
    valida el cuerpo (rechaza lo que no sea una frase con texto, 422).
    `ScoreFileError` responde 500 con un mensaje corto y sin ruta, y el
    detalle completo se manda al log (`D-010`); cualquier otra excepción
    también se atrapa, se registra con traceback y responde 500 sin quedar
    muda.
  - `app/english_tutor.py`: `respond` ya no devuelve un texto cocinado, sino
    `TutorReply` — un `dataclass(frozen=True)` con `verdict`, `words` y
    `score` (`D-008`). `main.py` arma el texto de la terminal a partir de esas
    tres piezas.
  - `app/tools.py`: `add_point` escribe ahora de forma atómica (temporal con
    `tempfile.mkstemp` en la misma carpeta + `os.replace`) y protegida por un
    `threading.Lock` que cubre lectura y escritura juntas (`D-007`, `D-009`).
    Resuelve dos fallos de concurrencia que una revisión externa encontró con
    50 peticiones a la vez: `PermissionError` al pelearse por un temporal de
    nombre fijo, y pérdida de puntos por el hueco entre leer y escribir.
  - `requirements.txt`: se añaden `fastapi==0.141.1`, `uvicorn==0.52.1` y
    `httpx2==2.9.1`.
  - `README.md`: documenta las dos puertas (terminal y servidor) y advierte
    que no deben correr a la vez — comparten el mismo candado, que solo vale
    dentro de un proceso (`A-002`).
  - Tests: de 30 a **53**, todos en verde con `python -m pytest`. Nuevos en
    `tests/test_api.py` (la ruta, la validación, los dos tipos de 500),
    `tests/test_tools.py` (concurrencia con hilos de verdad) y
    `tests/test_english_tutor.py` (`TutorReply`, `FrozenInstanceError`).
  - Costo de la sesión: $0,00 — no hay ninguna llamada a la API en el repo.
  - Queda pendiente: `T-029` (CORS) y `T-030` (pantalla) para el paso 3;
    `T-033` (configurar el log) para el paso 7; `T-019` (frases practicadas
    vs. correctas) para el paso 8.
- **Siguiente acción:** Empezar el paso 3 del roadmap — configurar CORS y
  crear `index.html` + `app.ts` contra `/practice` local.

### [S-004] 2026-08-02 — Dos arreglos de robustez sobre el paso 1: marcador roto y `count_words` con no-texto, 30 tests pasando

- **Paso:** 1 de 9 — sigue completo; esta sesión no avanza de paso, refuerza el
  código que ya existía.
- **Quedó funcionando:**
  - `app/tools.py`: excepción propia `ScoreFileError`. `read_score` distingue
    **ausente** (no hay archivo → 0, sigue igual) de **roto** (existe pero no
    se entiende: JSON inválido, sin clave `score`, valor no entero o booleano,
    o el JSON no es un objeto → `ScoreFileError` con mensaje en español que
    nombra el archivo). `add_point` deja subir el error sin atraparlo, y como
    lee antes de escribir, el archivo roto **no se sobrescribe**.
  - `main.py`: atrapa `ScoreFileError` y muestra el mensaje en español antes de
    salir, en vez de un traceback.
  - `app/tools.py`: `count_words` ahora comprueba que reciba un `str`; si no,
    lanza `TypeError` nombrando el tipo que llegó (antes reventaba con
    `AttributeError` ante `None`, un número o una lista).
  - `tests/test_tools.py`: 16 tests nuevos que cubren ambos arreglos. La
    corrida completa pasa de 14 a **30 tests**, todos en verde con
    `python -m pytest`.
  - Se probó a mano contra el marcador real: se corrompió `data/score.json`,
    se corrió `main.py`, salió el mensaje entendible y el archivo quedó byte a
    byte idéntico; después se restauró y la app siguió funcionando normal.
  - Costo de la sesión: $0,00 — no hay ninguna llamada a la API en el repo.
  - Queda pendiente y sin resolver (anotado en `decisions.md` D-006):
    `add_point` sigue escribiendo con `write_text`, que no es atómico. Este
    arreglo cura la lectura del archivo roto, no impide crearlo.
  - Queda sin decidir (anotado en `assumptions.md` A-001): si el marcador
    cuenta frases **practicadas** o **correctas**. Se resuelve en el paso 8,
    cuando el juez deje de ser falso.
- **Siguiente acción:** Empezar el paso 2 del roadmap — sacar `respond` de
  `main.py` y ponerla detrás de FastAPI, sin tocar `app/`.

### [S-003] 2026-08-02 — Paso 1 completo: agente FALSO con 3 herramientas, 14 tests pasando

- **Paso:** 1 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/tools.py`: las tres herramientas — `count_words` (cuenta palabras en
    Python puro), `judge_grammar` (FALSA: devuelve siempre el mismo veredicto,
    sin llamar al modelo) y `read_score` / `add_point` (marcador persistido en
    `data/score.json`).
  - `app/english_tutor.py`: `respond(sentence) -> str`, el enchufe del
    proyecto — llama a las tres herramientas siempre en el mismo orden.
  - `main.py`: la terminal. Único archivo con `input()`; lee frases hasta una
    línea vacía y llama a `respond`.
  - `tests/test_tools.py` y `tests/test_english_tutor.py` + `conftest.py`: 14
    tests, todos en verde con `python -m pytest`.
  - Se corrió en terminal de verdad: el marcador persistió entre ejecuciones
    distintas (`data/score.json`), y el usuario también la corrió a mano y
    confirmó que funciona.
  - Se cerraron tres huecos que venían del paso 0: entorno virtual `.venv/`,
    `requirements.txt` con `pytest==9.1.1` fijado, y las secciones del
    `README.md` que quedaban en deuda ("Cómo se corre", estado, estructura).
  - Costo del paso: $0,00 — no hay ninguna llamada a la API en el repo.
- **Siguiente acción:** Empezar el paso 2 del roadmap — sacar `respond` de
  `main.py` y ponerla detrás de FastAPI, sin tocar `app/`.

### [S-002] 2026-08-02 — Cierre del paso 0: T-006 a T-009 resueltas

- **Paso:** 0 de 9 — queda completo con esta sesión.
- **Quedó funcionando:**
  - `protocol-close/SKILL.md`: descripción del frontmatter y Paso 5 ya
    coinciden en que los cuatro archivos del porqué se **revisan**, no se
    escriben (T-006); el Paso 7 (reporte) trae ahora una sección propia "Los
    cuatro del porqué — revisados, no escritos" (T-008).
  - `session-closer.md`: nuevo límite explícito en `## Límites` — esos cuatro
    archivos no son suyos para escribir, con la única excepción mecánica del
    ascenso de una suposición comprobada (T-007).
  - `protocol-start/SKILL.md` y `session-starter.md`: las descripciones del
    frontmatter ya nombran las tres fuentes reales que se leen —`git`,
    `_persistence/` y `_context/`— (T-009). De paso, `protocol-start` suma
    `_context/scope.md` y `_context/roadmap.md` a la lectura obligatoria del
    Paso 1, y `session-starter` parte el límite "no inventes" en tres reglas
    (no inventar el proyecto, no dar un paso por completado con tareas
    abiertas, no recomendar prioridades). Ver decisión `D-004`.
- **Siguiente acción:** Empezar el paso 1 del roadmap — el agente en terminal,
  falso (sin llamar a Claude), con las 3 herramientas.

### [S-001] 2026-08-02 — Repositorio y esqueleto completos

- **Paso:** 0 de 9
- **Quedó funcionando:**
  - `.gitignore`, `.env.example`, `README.md` y `CLAUDE.md` llenos (antes vacíos).
  - Los tres archivos de `_context/` llenos: `scope.md`, `architecture.md`, `roadmap.md`.
  - Los seis archivos de `_persistence/` con el formato índice + entradas, listos
    para usarse (antes vacíos).
  - Dos agentes nuevos: `.claude/agents/session-starter.md` y
    `.claude/agents/session-closer.md`.
  - Dos skills nuevas: `.claude/skills/protocol-start/SKILL.md` y
    `.claude/skills/protocol-close/SKILL.md`.
  - `CLAUDE.md` documenta cómo se usan `_persistence/` y quién escribe cada
    archivo, más una sección nueva "Cómo se escribe el código" (PI-1 a PI-4).
- **Siguiente acción:** Empezar el paso 1 del roadmap — el agente en terminal,
  falso (sin llamar a Claude), con las 3 herramientas.

<!-- La más reciente arriba. Formato:

### [S-001] 2026-08-02 — <título corto>

- **Paso:** <n de 9>
- **Quedó funcionando:** <solo lo que está en el diff>
- **Siguiente acción:** <la primera acción concreta de mañana>

-->
