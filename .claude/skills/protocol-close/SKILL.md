---
name: protocol-close
description: Protocolo de cierre de sesión del proyecto. Recoge la evidencia real del trabajo (git status, git diff, git log), actualiza de forma obligatoria _persistence/progress.md y _persistence/tasks.md, y solo revisa —sin escribirlos— decisions.md, assumptions.md, constraints.md y lessons.md, que son de la sesión principal; después deja la sesión cerrada con un commit. Uso exclusivo del agente session-closer.
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
   **no lo escribas tú**: señálalo en el reporte, para que el usuario lo dicte.

🚨 **Los cuatro se reportan siempre, aunque no falte nada.** El Paso 7 tiene una
sección propia para ellos: cada uno sale con "al día" o con lo que falta por
anotar. Sin esa línea, un cierre que revisó y uno que no revisó se ven igual.

**La única excepción, y es mecánica:** si una suposición de `assumptions.md`
quedó comprobada por la evidencia del diff, puedes moverla a `decisions.md` o
`lessons.md` y borrarla de `assumptions.md`. Eso no es interpretar, es aplicar la
regla del ascenso — y **dilo en el reporte**. Al moverla, toca **los dos
índices**: la fila sale del de origen y entra en el de destino, con id nuevo.

## Paso 5b — El `.js` que vas a commitear, ¿es el de su `.ts`?

`frontend/app.ts` lo escribe una persona. `app/static/app.js` lo escribe el
compilador. Los dos van a Git — ver [D-012]. Si el `.ts` se editó y no se
compiló, el commit **congela un `.js` viejo**, y eso es lo que se despliega.

🔑 **Nadie se entera solo:** la pantalla vieja no falla, hace lo de ayer. Y el
test `test_the_script_is_served` tampoco avisa — un `.js` de hace tres días
también contesta 200. Esta es la única comprobación que lo mira.

Va **antes del `git add`**: el daño no es tener el archivo viejo en el disco, es
meterlo en el commit.

```bash
# ── Verdad 1: ¿se pudo compilar? ──
OUT=$(mktemp -d)
node node_modules/typescript/bin/tsc --outDir "$OUT"
COMPILAR=$?

# ── Verdad 2: ¿coincide cada archivo que produjo el compilador? ──
COMPARAR=0
GENERADOS=$(cd "$OUT" && find . -type f -printf '%P\n')
[ -z "$GENERADOS" ] && { COMPARAR=1; echo "SIN COMPROBAR: el compilador no produjo nada"; }
for f in $GENERADOS; do diff "$OUT/$f" "app/static/$f" || COMPARAR=1; done
rm -rf "$OUT"

echo "compilar: $COMPILAR"
echo "comparar: $COMPARAR"
```

**Hay tres resultados, no dos:**

| qué sale | qué significa | qué haces |
|---|---|---|
| `compilar: 0` y `comparar: 0` | el `.js` está al día | sigue al Paso 6 |
| `compilar: 0` y `comparar: 1` | el `.js` es viejo | commit y push igual, y a **Sin resolver** |
| `compilar` ≠ 0 | **no lo comprobaste** | commit y push igual, y a **Sin resolver** |

🚨 **La tercera fila es la importante.** Si falta `node`, falta `node_modules/` o
`tsc` da error, no sabes si está al día: sabes que no miraste. **"No pude
comprobarlo" no es "está bien".** Confundir las dos es el fallo de [L-006] otra
vez, y por eso son **dos códigos de salida y no uno**: la tercera fila se detecta
sola, sin leer la salida entera ni deducir nada.

**Por qué el bucle está escrito así, y no se simplifica:**

- La lista sale de `$OUT`, **la carpeta del compilador**. Ahí solo está lo que él
  generó, así que `app/static/index.html` —escrito a mano— no puede entrar en la
  comparación. 🔑 **No es una lista negra de excepciones: es que el compilador
  declara qué le toca vigilar.** Un `styles.css` a mano mañana tampoco entra, y
  un segundo `.js` generado entra solo. Una lista negra habría que mantenerla.
  ⛔ **No lo cambies por `diff -r`**: compara en las dos direcciones, canta
  `Only in app/static: index.html` y grita "viejo" **todas las noches con el repo
  correcto**. Una alarma que siempre suena enseña a no escuchar — ver [L-007].
- **`|| COMPARAR=1` no es adorno.** Un `for` termina con el código del **último**
  comando, no de "alguno falló". Sin la bandera, un `a.js` distinto seguido de un
  `b.js` bueno da éxito con la diferencia impresa dos líneas más arriba.
- **La bandera de `GENERADOS` vacío tampoco.** Una comparación sobre cero
  archivos siempre pasa. Hoy `tsc` falla con `TS18003` si no encuentra fuentes,
  pero el control no depende de eso: lo marca él.

⛔ **No uses `npx`.** Si el compilador no está en disco, `npx` sale a internet a
bajarlo, y este protocolo no depende de tener red — ver [C-001]. Se llama al
binario local, y si no está, es la tercera fila.

⛔ **No recompiles tú, ni siquiera si es obvio.** Regenerar el `.js` y meterlo en
el commit deja el repo correcto y **borra la señal de que se olvidó** — y volvería
a olvidarse mañana. Tampoco puedes: el `.ts` podría estar a medias. **Tú
reportas; arreglarlo es de la sesión siguiente.** Anota la tarea en `tasks.md`.

⚠️ **Que falle no cancela el cierre.** Commiteas y subes igual. Ver [D-018].

🚨 **La línea del reporte sale siempre**, esté al día o no. Sin ella, un cierre
que comprobó y uno que no se leen idénticos.

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

⛔ **Comandos prohibidos, sin excepción:** `git commit --amend`, `git reset`,
`git checkout --`, `git restore`, `git rebase`, `git clean`, `git push --force`
y cualquier otra cosa con `--force`. Tu trabajo es **añadir** historia, nunca
reescribir ni borrar la que hay.

## Paso 6b — El push. El cierre no acaba en el commit

```
git push
```

🔑 **Un `git push` a secas solo añade, y por eso sí es tuyo** — encaja con la
regla de arriba, no la rompe. Lo que reescribe historia es `--force`, y ese
sigue prohibido. Ver [D-016].

Después, siempre:

```
git status -sb
```

🚨 **Si la primera línea todavía dice `ahead`, el push no ocurrió** —remoto sin
configurar, credenciales, red— y el trabajo existe solo en este disco. **No lo
tapes:** va en el reporte, en "Sin resolver", con lo que salió mal. Un disco roto
esa noche se lleva la sesión entera.

> 🔑 La regla vieja era *"si no hay hash, no hubo cierre"*. Se cumplía entera y
> el trabajo se quedaba sin subir igual: **un commit es local.** La regla
> corregida es **"si el hash no está en `origin`, no hubo cierre"**, y se
> comprueba con `git status -sb`, no con el hash. Ver [L-006].

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

### Los cuatro del porqué — revisados, no escritos
- decisions.md — <al día | falta anotar: ...>
- assumptions.md — <al día | falta anotar: ... | ascendida [A-00N] → [D-00N]>
- constraints.md — <al día | falta anotar: ...>
- lessons.md — <al día | falta anotar: ...>

### Commit
`.js` compilado — <al día | 🚨 VIEJO, falta `npm run build` | 🚨 SIN COMPROBAR — <qué falló>>
<hash corto> — <primera línea del mensaje>
<"subido a origin, `git status -sb` sin ahead" | 🚨 "SIN SUBIR — <qué falló>">

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
