# Avance — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [S-000]`. Búscala con `grep`, no leas el archivo entero.

## Estado actual

| | |
|---|---|
| **paso** | 0 de 9 — completo. Repositorio y esqueleto |
| **última sesión** | 2026-08-02 |
| **siguiente acción** | Empezar el paso 1: el agente en terminal, falso, con las 3 herramientas |

## Índice

| id | fecha | qué avanzó | paso |
|---|---|---|---|
| S-002 | 2026-08-02 | Cierre del paso 0: T-006 a T-009 resueltas | 0 |
| S-001 | 2026-08-02 | Repositorio y esqueleto completos | 0 |

---

## Entradas

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
