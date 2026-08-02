# Avance — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [S-000]`. Búscala con `grep`, no leas el archivo entero.

## Estado actual

| | |
|---|---|
| **paso** | 2 de 9 — completo. FastAPI corre al lado de la terminal, con la concurrencia ya resuelta |
| **última sesión** | 2026-08-02 |
| **siguiente acción** | Empezar el paso 3 del roadmap: CORS (T-029) y crear `index.html` + `app.ts` contra `/practice` local (T-030) |

## Índice

| id | fecha | qué avanzó | paso |
|---|---|---|---|
| S-005 | 2026-08-02 | Paso 2 completo: `app/api.py` con FastAPI, `respond` devuelve `TutorReply`, dos fallos de concurrencia arreglados, 53 tests pasando | 2 |
| S-004 | 2026-08-02 | Dos arreglos de robustez sobre el paso 1: marcador roto y `count_words` con no-texto, 30 tests pasando | 1 |
| S-003 | 2026-08-02 | Paso 1 completo: agente FALSO con 3 herramientas, 14 tests pasando | 1 |
| S-002 | 2026-08-02 | Cierre del paso 0: T-006 a T-009 resueltas | 0 |
| S-001 | 2026-08-02 | Repositorio y esqueleto completos | 0 |

---

## Entradas

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
