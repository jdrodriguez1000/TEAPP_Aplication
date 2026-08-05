# Tareas — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [T-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

Estados: 🔲 pendiente · 🔄 a medias · ✅ hecha · ❌ descartada

| id | tarea | estado | paso |
|---|---|---|---|
| T-001 | Inicializar repo y conectarlo al remoto de GitHub | ✅ | 0 |
| T-002 | Llenar `.gitignore`, `.env.example`, `README.md`, `CLAUDE.md` | ✅ | 0 |
| T-003 | Llenar los tres archivos de `_context/` | ✅ | 0 |
| T-004 | Llenar los seis archivos de `_persistence/` con formato índice + entradas | ✅ | 0 |
| T-005 | Crear agentes `session-starter` y `session-closer` con sus skills | ✅ | 0 |
| T-006 | Corregir incoherencia: `protocol-close` (descripción vs. Paso 5) dice que actualiza `decisions/assumptions/constraints/lessons`, pero el Paso 5 dice que solo los revisa | ✅ | 0 |
| T-007 | Añadir a los límites de `session-closer` que los cuatro archivos de porqué no son suyos para escribir | ✅ | 0 |
| T-008 | Revisar que el Paso 7 (reporte) de `protocol-close` deje explícito el resultado de revisar los cuatro archivos | ✅ | 0 |
| T-009 | Actualizar descripciones de `session-starter` / `protocol-start` para que mencionen que también leen `git` | ✅ | 0 |
| T-010 | Crear `app/tools.py`: `count_words`, `judge_grammar` (falsa), `read_score`, `add_point` | ✅ | 1 |
| T-011 | Crear `app/english_tutor.py` con `respond(sentence) -> str` | ✅ | 1 |
| T-012 | Crear `main.py`, la terminal (único archivo con `input()`) | ✅ | 1 |
| T-013 | Escribir tests: `tests/test_tools.py`, `tests/test_english_tutor.py`, `conftest.py` — 14 pasando | ✅ | 1 |
| T-014 | Correr la app en terminal y verificar que el marcador persiste entre ejecuciones | ✅ | 1 |
| T-015 | Crear entorno virtual `.venv/` y `requirements.txt` con `pytest==9.1.1` fijado | ✅ | 1 |
| T-016 | Completar en `README.md` las secciones "Cómo se corre", estado y estructura | ✅ | 1 |
| T-017 | Arreglar `read_score`/`add_point`: distinguir marcador ausente (0) de roto (`ScoreFileError`), sin sobrescribir el archivo roto | ✅ | 1 |
| T-018 | Arreglar `count_words`: lanzar `TypeError` si no recibe un `str`, en vez de reventar con `AttributeError` | ✅ | 1 |
| T-019 | Decidir si el marcador cuenta frases practicadas o correctas (ver `assumptions.md` A-001) | 🔲 | 8 |
| T-020 | Hacer atómica la escritura de `add_point`: escribir al lado y renombrar encima (ver `decisions.md` D-007) | ✅ | 2 |
| T-021 | Arreglar que dos peticiones a la vez revienten con `PermissionError`: un temporal con nombre propio por escritura (D-009) | ✅ | 2 |
| T-022 | Arreglar que dos peticiones a la vez pierdan puntos y repitan el marcador: candado sobre lectura + escritura (D-009) | ✅ | 2 |
| T-023 | Registrar que el candado solo vale con un proceso de uvicorn (`assumptions.md` A-002) y anotarlo en `README.md` | ✅ | 2 |
| T-024 | Dejar de devolver la ruta del servidor en el 500, y que un fallo inesperado no salga mudo (D-010) | ✅ | 2 |
| T-025 | Levantar uvicorn a mano y ver la ruta contestar: `/docs`, una frase, un 422 y el 500 sin ruta | ✅ | 2 |
| T-026 | Poner el `README.md` al día con el paso 2: uvicorn, `/docs`, `app/api.py`, y arrancar sin `--workers` | ✅ | 2 |
| T-027 | Poner `tasks.md` al día con las tareas del paso 2 | ✅ | 2 |
| T-028 | Afinar `test_the_reply_cannot_be_modified`: esperar `FrozenInstanceError`, no `Exception` | ✅ | 2 |
| T-029 | Configurar CORS: la pantalla se abrirá desde otro origen y el navegador bloqueará la llamada | ❌ descartada | 3 |
| T-030 | Crear `index.html` y `app.ts` contra la ruta `/practice` local | ✅ | 3 |
| T-031 | Cambiar `respond` para que devuelva `TutorReply` —tres piezas sueltas— en vez de un texto cocinado (D-008) | ✅ | 2 |
| T-032 | Crear `app/api.py` con FastAPI: `POST /practice`, validación del cuerpo y `requirements.txt` al día | ✅ | 2 |
| T-033 | Configurar el log (hora, nivel y origen). Hecho en `config.configure_logging()`, con `INFO` por defecto y `TEAPP_LOG_LEVEL` para bajarlo. Con él, la cuota agotada y el registro cerrado vuelven a `info`; los intentos fallidos se quedan en `warning` (`D-028`). Medido con uvicorn: el renglón de `L-012` ya sale | ✅ | 7 |
| T-034 | Ampliar `A-002` y el `README.md`: el candado también se rompe con `main.py` y el servidor a la vez, no solo con `--workers` | ✅ | 2 |
| T-035 | Servir la pantalla desde FastAPI: `StaticFiles` en `/static`, `GET /` con `index.html` | ✅ | 3 |
| T-036 | Compilar `frontend/app.ts` a `app/static/app.js` con `tsc`, versionado en Git | ✅ | 3 |
| T-037 | Comprobar que `app/static/*.js` está **al día**, no solo que existe. Resuelta en el cierre, no en `pytest` ([D-017]): Paso 5b de `protocol-close`. El test se renombró a `test_the_script_is_served` y su comentario ya dice qué **no** mide | ✅ | 3 |
| T-038 | Tope de peticiones por persona en el **servidor**. El `sendButton.disabled` de `app.ts` solo frena clics en el navegador: diez peticiones mandadas a mano siguen sumando diez puntos | ✅ | 6 |
| T-039 | Crear `app/tools.py`: `normalize_user`, `InvalidUserError`, `score_file`; `read_score`/`add_point` reciben el nombre de la persona | ✅ | 4 |
| T-040 | Cambiar `respond(sentence, user)` sin valor por defecto; `main.py` pide el nombre una vez al arrancar | ✅ | 4 |
| T-041 | `app/api.py`: `PracticeRequest` gana `user`, validado primero y traducido a 422 | ✅ | 4 |
| T-042 | `frontend/app.ts` + `index.html`: casilla "Your name" recordada en `localStorage`; recompilar a `app/static/app.js` | ✅ | 4 |
| T-043 | Borrar `data/score.json`, el marcador global que dejó el paso 3 (`D-015`) | ✅ | 4 |
| T-044 | Tests del paso 4: recorrido de ruta, nombres reservados de Windows, normalización, memoria por persona, concurrencia entre dos personas — de 57 a 121 pasando | ✅ | 4 |
| T-045 | Quitar la casilla "Your name" de la pantalla en el paso 5, sustituyéndola por identidad de verdad, no añadiéndole nada al lado (`D-013`) | ✅ | 5 |
| T-046 | Comprobar `[A-006]` en otra máquina: que la ruta de `mktemp -d` le sirva a `node`. Si falla, el Paso 5b cae siempre en "SIN COMPROBAR" y el arreglo es `cygpath -w` | 🔲 | 7 |
| T-047 | Comprobar `[C-001]` de verdad. **Medida y se cumple:** 192 tests verdes con la red cortada, y los 5 controles del portero verdes. El motivo real es más fuerte que el verde: en `app/` y `tests/` hay **cero** `requests`/`httpx`/`urllib`/`socket`/`aiohttp`/`subprocess` — los tests usan `TestClient`, que llama la app en el mismo proceso sin abrir un socket. No pasaron porque el portero los dejara pasar: pasaron porque **no había nada que interceptar**. El portero (`D-022`) es el vigía de que siga siendo así mañana. La redacción de `C-001` se corrigió al medirla: el `git push` del cierre la contradecía | ✅ | 6 |
| T-049 | `protocol-close` escribía `tasks.md` (Paso 4) **antes** de correr el Paso 5b y el push (Pasos 5b y 6b). Resuelta: el control del `.js` sube al Paso 2b (antes de escribir `tasks.md`), y el resultado del push queda escrito como imposibilidad lógica, no como pendiente (`D-019`) | ✅ | 5 |
| T-048 | Correr el Paso 5b de punta a punta en un cierre real, con el `session-closer` haciéndolo. Estrenado en el cierre del 2026-08-03 (commit `6af7597`): `compilar: 0`, `comparar: 0`, y la línea salió en el reporte | ✅ | 5 |
| T-050 | Que `TEAPP_SECRET_KEY` exista en la nube y sea **estable entre despliegues**: si cambia, todas las sesiones mueren de golpe sin ningún error que lo explique (`A-008`) | 🔲 | 7 |
| T-051 | Poner `TEAPP_COOKIE_SECURE=true` en la nube. En local va en `false` porque el navegador descarta en silencio una cookie `Secure` sobre `http://localhost` | 🔲 | 7 |
| T-052 | Escribir un test que anule el `autouse` de `tests/conftest.py`, ponga `TEAPP_COOKIE_SECURE=true` y compruebe que `set_cookie` recibe `secure=True`: la rama por defecto no corre en ningún test hoy (`A-009`) | 🔲 | 7 |
| T-053 | Tope de intentos fallidos contra `/login`, contado por origen de la petición, no por persona. Hecho en `app/login_guard.py`: contador en memoria con barrido, 429 con `Retry-After` y motivo al log. Visto con uvicorn real (`D-026`) | ✅ | 7 |
| T-054 | Tope de tamaño de cuerpo en el servidor de delante (el reverse proxy de la nube). `MAX_SENTENCE_LENGTH` frena el gasto, no la subida: un cuerpo de 5 MB se sube entero antes del 422 (`C-002`) | 🔲 | 7 |
| T-055 | Que el origen que lee `_request_origin` sea el REAL cuando haya un proxy delante. Hoy es `request.client.host`; tras el despliegue será la dirección del proxy y el freno de `/login` dejaría fuera a todo el mundo a la vez (`A-014`). ⚠️ Leer `X-Forwarded-For` **sin** proxy de confianza delante es peor que no tener freno: la cabecera la escribe cualquiera | 🔲 | 7 |
| T-056 | Decidir y poner `TEAPP_REGISTRATION_OPEN` en la nube. Por defecto vale `false`, que es lo que se quiere (`D-027`), pero **conviene ponerlo explícito**: un ajuste de seguridad que depende de que nadie lo escriba es un ajuste que alguien abre 'un momentito'. Y comprobar que `create_account.py` corre en la plataforma: sin él no hay forma de crear la primera cuenta allí | 🔲 | 7 |

⚠️ T-031 y T-032 son el trabajo central del paso 2 y se hicieron **antes** que
T-021…T-029, aunque lleven número mayor. Los números de T-021 en adelante venían
ya puestos en la revisión externa que los encontró, y se respetaron para que las
referencias no mintieran.

⚠️ **T-037 lleva paso 3 a propósito**, aunque se haga después: es **deuda del
paso 3**, no trabajo del 6. La columna dice de dónde viene la tarea, no cuándo
toca hacerla.

---

## Entradas

<!-- Solo las tareas que necesitan detalle. Las que se entienden en una línea
     se quedan en el índice y no bajan aquí. Formato:

### [T-001] <título corto>

- **Estado:** 🔲 / 🔄 / ✅
- **Dónde quedó:** <solo si está a medias: en qué punto exacto>
- **Notas:** <lo que haga falta para retomarla sin releer nada>

-->
