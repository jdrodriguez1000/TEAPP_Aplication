# Decisiones — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [D-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

| id | fecha | qué se decidió | toca |
|---|---|---|---|
| D-006 | 2026-08-02 | El marcador roto avisa con `ScoreFileError`; ausente sigue siendo 0 | `app/tools.py`, `main.py`, paso 2 |
| D-005 | 2026-08-02 | Nombres en inglés, contenido en español | todo el código del proyecto |
| D-004 | 2026-08-02 | El protocolo de inicio lee `_context/` siempre, no a demanda | `protocol-start`, `session-starter` |
| D-003 | 2026-08-02 | Recuperar 4 principios de ingeniería de un `CLAUDE.md` anterior | cómo se escribe el código |
| D-002 | 2026-08-02 | Los cuatro archivos del porqué los escribe la sesión principal, no el closer | `_persistence/` |
| D-001 | 2026-08-02 | La skill de inicio se llama `protocol-start`, no `protocol-close` | `.claude/skills/` |

---

## Entradas

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
  manejo de errores del paso 2. Queda pendiente y **sin resolver** la causa de
  raíz: `add_point` sigue escribiendo con `write_text`, que no es atómico — este
  arreglo cura la lectura del archivo roto, no impide crearlo.

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
