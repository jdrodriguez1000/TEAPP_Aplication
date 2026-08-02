---
name: protocol-start
description: Protocolo de inicio de sesión del proyecto. Lee de forma obligatoria _persistence/progress.md y _persistence/tasks.md, y a demanda decisions.md, assumptions.md, constraints.md y lessons.md, para luego presentar en pantalla el avance del proyecto, las últimas tareas realizadas y las siguientes tareas a realizar. Uso exclusivo del agente session-starter.
---

# Protocolo de inicio de sesión

Este protocolo lo ejecuta **únicamente** el agente `session-starter`. Su objetivo es
reconstruir el estado del proyecto al comenzar una sesión, leyendo la carpeta
`_persistence/` y presentando un resumen accionable.

## Paso 1 — Evidencia obligatoria

Lee siempre, sin excepción, y **en este orden**:

**Primero el repositorio** (es el hecho, no el relato):

```
git log --oneline -5
git status --short
```

**Después los dos archivos de estado:**

1. `_persistence/progress.md` — avance acumulado del proyecto.
2. `_persistence/tasks.md` — tareas realizadas, en curso y pendientes.

De estos dos lee **solo la cabecera** (`Estado actual` + `Índice`): las primeras
~30 líneas bastan. Baja a una entrada concreta únicamente si el índice no
responde. Ver *"Cómo se leen estos archivos"* más abajo.

Si alguno no existe o está vacío, indícalo explícitamente en el reporte en lugar de
inventar contenido.

### Por qué el `git` va primero

> 🔑 **`progress.md` es lo que alguien escribió que pasó. `git log` es lo que pasó.**

Un archivo de estado puede quedar desactualizado —una sesión que se cayó, un
cierre a medias— y no tiene forma de avisarlo. El repositorio sí. Al leerlo
primero, entras a los archivos ya sabiendo si se les puede creer.

### Dos desfases que hay que reportar

| lo que ves | qué significa | dilo así |
|---|---|---|
| el último commit **no** aparece reflejado en `progress.md` | la sesión anterior no cerró bien | *"⚠️ `progress.md` va por detrás del último commit"* |
| `git status` tiene cambios sin commitear | quedó trabajo suelto de la sesión anterior | *"⚠️ hay N archivos sin commitear"* |

Si detectas un desfase, **el reporte lo dice arriba del todo**, antes del estado.
Es lo primero que el usuario necesita saber.

## Paso 2 — Lectura a demanda

Los siguientes cuatro archivos **no** se leen por defecto. Léelos solo cuando algo de
lo visto en el Paso 1 lo justifique:

| Archivo | Léelo cuando… |
| --- | --- |
| `_persistence/decisions.md` | progress/tasks mencionen una decisión técnica, un cambio de rumbo, o una tarea dependa de una decisión previa. |
| `_persistence/assumptions.md` | haya tareas pendientes apoyadas en supuestos sin confirmar, o supuestos que puedan haber caducado. |
| `_persistence/constraints.md` | las siguientes tareas toquen áreas con límites conocidos (stack, plazos, integraciones, alcance). |
| `_persistence/lessons.md` | se vaya a repetir un tipo de trabajo que ya falló antes, o haya tareas rehechas/revertidas. |

Antes de leer cada uno, ten claro qué pregunta concreta quieres responder con él.
Si ninguno aplica, no los leas.

## Cómo se leen estos archivos

Los seis archivos de `_persistence/` tienen la misma forma: **índice arriba,
entradas debajo**, cada una bajo un ancla del tipo `### [D-001]`.

> 🔑 **El índice es la respuesta por defecto; la entrada es la excepción.**

1. **Lee la cabecera**, no el archivo. Las primeras ~30 líneas traen el índice
   entero.
2. **Decide desde el índice.** La mayoría de las veces el título y la fecha
   bastan para el reporte.
3. **Baja a una entrada solo si el índice no responde.** Búscala por su ancla
   (`grep "\[D-003\]"`), no leyendo el archivo de arriba abajo.

Un archivo de `_persistence/` puede crecer mucho. Leerlo entero para sacar una
línea del reporte gasta contexto que hará falta después, cuando toque trabajar.

## Paso 3 — Reporte en pantalla

Presenta el resultado en este formato, en español y sin relleno:

```
## ⚠️ Desfase detectado        <-- omitir esta sección si no hay ninguno
- <qué no cuadra entre el repositorio y los archivos>

## Estado del proyecto
<avance global: fase actual, % o hitos completados según progress.md>

## Últimas tareas realizadas
- <tarea> — <fecha si está registrada>
- ...

## Siguientes tareas
1. <tarea> — <prioridad/bloqueo si aplica>
2. ...

## Contexto relevante        <-- omitir esta sección si no leíste archivos del Paso 2
- **Decisiones:** ...
- **Supuestos:** ...
- **Restricciones:** ...
- **Lecciones:** ...
```

Reglas del reporte:

- Máximo 5 elementos por lista; si hay más, quédate con los más recientes o
  prioritarios y dilo.
- Cita el archivo de origen cuando un dato pueda ser ambiguo.
- Incluye la sección **Contexto relevante** solo con lo que cambie la decisión de qué
  hacer ahora, no como resumen de los archivos.
- Termina señalando bloqueos o información faltante, si los hay.
- No modifiques ningún archivo de `_persistence/`: este protocolo es de solo lectura.
