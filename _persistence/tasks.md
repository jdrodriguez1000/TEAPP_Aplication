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
| T-033 | Configurar el log (hora, nivel y origen): hoy se ve por el handler de último recurso de Python, no porque nadie lo haya decidido (`assumptions.md` A-003) | 🔲 | 7 |
| T-034 | Ampliar `A-002` y el `README.md`: el candado también se rompe con `main.py` y el servidor a la vez, no solo con `--workers` | ✅ | 2 |
| T-035 | Servir la pantalla desde FastAPI: `StaticFiles` en `/static`, `GET /` con `index.html` | ✅ | 3 |
| T-036 | Compilar `frontend/app.ts` a `app/static/app.js` con `tsc`, versionado en Git | ✅ | 3 |
| T-037 | Comprobar que `app/static/*.js` está **al día**, no solo que existe: correr `tsc` y verificar que no cambia nada. `test_the_compiled_script_is_served` da 200 con un `.js` viejo, que es justo el riesgo que nombra [D-012] | 🔲 | 3 |
| T-038 | Tope de peticiones por persona en el **servidor**. El `sendButton.disabled` de `app.ts` solo frena clics en el navegador: diez peticiones mandadas a mano siguen sumando diez puntos | 🔲 | 6 |

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
