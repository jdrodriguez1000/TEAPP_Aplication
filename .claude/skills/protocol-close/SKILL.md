---
name: protocol-close
description: Protocolo de cierre de sesión del proyecto. Recoge la evidencia real del trabajo (git status, git diff, git log), actualiza de forma obligatoria _persistence/progress.md y _persistence/tasks.md, y a demanda decisions.md, assumptions.md, constraints.md y lessons.md; después deja la sesión cerrada con un commit. Uso exclusivo del agente session-closer.
---

# Protocolo de cierre de sesión

Este protocolo lo ejecuta **únicamente** el agente `session-closer`. Su objetivo es
dejar el proyecto en un estado del que la próxima sesión pueda arrancar sola.

> 🔑 **La regla que gobierna todo el protocolo: se escribe desde la EVIDENCIA, no
> desde el relato.** No anotes "se hizo X" si X no aparece en el `git diff`.

La razón es concreta: tú no viste la conversación de hoy. Solo ves archivos. Si
escribes desde lo que te contaron, escribes rumores; si escribes desde el diff,
escribes hechos.

## Paso 1 — Recoger la evidencia (antes de escribir nada)

En este orden, y sin saltarte ninguno:

```
git status
git diff
git diff --staged
git log --oneline -5
```

De ahí sale **qué pasó de verdad hoy**: qué archivos nacieron, cuáles cambiaron,
y desde qué punto se venía.

Si `git status` sale limpio y no hay nada sin commitear, **dilo y detente**: no
hay sesión que cerrar. No inventes avance para llenar el reporte.

## Paso 2 — El traspaso, solo para el porqué

La sesión principal puede darte un traspaso corto: lo que se intentó, lo que se
descartó, con qué se trabó el usuario. Úsalo **solo para explicar el porqué** de
lo que ya viste en el diff.

⚠️ **El traspaso nunca sustituye la evidencia.** Si el traspaso dice que se hizo
algo y el diff no lo muestra, manda el diff — y anótalo como discrepancia en el
reporte.

Si no hay traspaso, el protocolo funciona igual, solo que con menos porqué.

## Cómo se escriben estos archivos

Los seis archivos de `_persistence/` tienen la misma forma: **índice arriba,
entradas debajo**, cada una bajo un ancla del tipo `### [S-001]`. El archivo
mismo trae el formato de su entrada en un comentario al final.

> 🚨 **El índice y las entradas se actualizan juntos, en la misma pasada.**
> Una entrada que no está en el índice es invisible: nadie la va a encontrar,
> porque nadie lee el archivo entero. Una línea de índice sin entrada apunta al
> vacío. Las dos formas de dejarlo a medias mienten igual.

Al añadir una entrada:

1. Dale el **siguiente id libre** (mira el último del índice, no cuentes
   entradas).
2. Escribe la entrada **arriba del todo** de la sección `## Entradas`.
3. Añade su fila al índice, también arriba.
4. Si el archivo aún trae `_(sin entradas)_`, **borra esa fila**.

Fechas absolutas (`2026-08-02`), nunca "ayer" ni "la semana pasada". En el índice,
títulos cortos: tienen que caber en una fila y decidirse sin abrir la entrada.

## Paso 3 — `_persistence/progress.md` (obligatorio)

Actualízalo **siempre**, en dos sitios:

**a) La tabla `Estado actual`**, arriba. Es lo único que se lee al abrir sesión,
así que se sobrescribe entera: paso, última sesión y siguiente acción.

**b) Una entrada nueva `[S-00N]`** más el índice, con:

1. **¿En qué paso va el proyecto?** (ver `_context/roadmap.md`)
2. **¿Qué quedó funcionando hoy?** — solo lo que está en el diff.
3. **¿Cuál es el siguiente paso concreto?** No "seguir con el paso 2", sino la
   primera acción de mañana.

## Paso 4 — `_persistence/tasks.md` (obligatorio)

Aquí el índice **es** el archivo: el estado de cada tarea vive en su fila.

- Mueve a ✅ **hecha** solo lo que la evidencia respalde.
- Deja en 🔄 **a medias** lo que quedó a mitad, y di **en qué punto** quedó —eso
  sí baja a una entrada, porque no cabe en una fila.
- Añade las tareas nuevas que aparecieron hoy, con su id.

Una tarea que se entiende en una línea **se queda en el índice** y no baja a
`## Entradas`. No infles el archivo.

Si una tarea estaba marcada como hecha y el diff la contradice, **desmárcala** y
dilo en el reporte.

## Paso 5 — Los otros cuatro: **revísalos, no los escribas**

`decisions.md`, `assumptions.md`, `constraints.md` y `lessons.md` **no son tuyos**.
Los escribe la sesión principal, en el momento en que las cosas pasan, porque una
decisión no aparece en el `git diff`: nace en la conversación.

Tú no estuviste ahí. Escribirlos sería inventar.

**Lo que sí haces: comprobar que no se quedaron cortos.**

1. Léelos.
2. Compáralos con lo que muestra el diff.
3. Si el diff enseña algo que **claramente fue una decisión** y no está anotado
   —se eligió una librería, se cambió una estructura, se descartó un camino—
   **no lo escribas tú**: señálalo en el reporte, en la sección "Sin resolver",
   para que el usuario lo dicte.

**La única excepción, y es mecánica:** si una suposición de `assumptions.md`
quedó comprobada por la evidencia del diff, puedes moverla a `decisions.md` o
`lessons.md` y borrarla de `assumptions.md`. Eso no es interpretar, es aplicar la
regla del ascenso — y **dilo en el reporte**. Al moverla, toca **los dos
índices**: la fila sale del de origen y entra en el de destino, con id nuevo.

## Paso 6 — El commit

**Primero la verificación, después el commit.** Nunca al revés.

```
git status
```

🚨 Comprueba que **`.env` no aparezca** en la lista. Si aparece, **detente**, no
añadas nada y repórtalo: falta una línea en `.gitignore`. Git no olvida — si una
llave entra al historial, borrar el archivo después no la borra.

Si está limpio:

```
git add -A
git commit -m "..."
```

El mensaje dice **qué avanzó y por qué**, no qué archivos cambiaron: eso ya lo
sabe Git. Primera línea corta, y debajo lo que valga la pena. Termina siempre
con:

```
Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
```

⛔ **Comandos prohibidos, sin excepción:** `git push`, `git commit --amend`,
`git reset`, `git checkout --`, `git restore`, `git rebase`, `git clean`,
cualquier cosa con `--force`. Tu trabajo es **añadir** historia, nunca reescribir
ni borrar la que hay.

## Paso 7 — Reporte en pantalla

En español, sin relleno:

```
## Cierre de sesión — <fecha>

### Lo que dice la evidencia
- <N> archivos tocados: <los principales>
- <qué quedó funcionando, según el diff>

### _persistence/ actualizado
- progress.md — <en una línea, qué cambió>
- tasks.md — <N hechas, N pendientes, N nuevas>
- <los demás, solo si los tocaste, con la razón>

### Commit
<hash corto> — <primera línea del mensaje>

### Para mañana
<el siguiente paso concreto, tal como quedó en progress.md>

### Sin resolver        <-- omitir si no hay nada
- <discrepancias entre el traspaso y el diff>
- <lo que quedó a medias y en qué punto>
```

## Reglas del protocolo

- **No inventes** avances, fechas, decisiones ni tareas.
- **No escribas código** ni arregles nada, aunque veas algo roto. Anótalo en
  `tasks.md` y sigue. Cerrar la sesión no es el momento de abrirla otra vez.
- **No dupliques.** Si algo ya está escrito en `_context/`, no lo repitas en
  `_persistence/`: cada archivo tiene un trabajo.
- **Escribe corto.** Un `progress.md` que nadie lee no orienta a nadie.
