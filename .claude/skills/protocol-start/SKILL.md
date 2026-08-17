---
name: protocol-start
description: Protocolo de inicio de sesión del proyecto. Lee de forma obligatoria el estado de git, _persistence/progress.md y _persistence/tasks.md, y _context/scope.md y _context/roadmap.md; a demanda decisions.md, assumptions.md, constraints.md y lessons.md. Con eso presenta en pantalla el avance del proyecto, las últimas tareas realizadas y las siguientes tareas a realizar. Uso exclusivo del agente session-starter.
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
git status -sb
```

🚨 **`-sb`, no `--short`.** Los dos listan los archivos sueltos, pero solo `-sb`
imprime **la línea de la rama**, que es donde se ve si la sesión anterior subió
su trabajo:

```
## main...origin/main [ahead 1]      <-- hay un commit que no está en origin
```

Con `--short` esa línea no sale. Un commit sin subir es **invisible**: el repo se
ve limpio, el arranque no dice nada, y el trabajo de ayer existe solo en este
disco. Ver [L-009].

**Después los dos archivos de estado:**

1. `_persistence/progress.md` — avance acumulado del proyecto.
2. `_persistence/tasks.md` — tareas realizadas, en curso y pendientes.

De estos dos lee **solo la cabecera** (`Estado actual` + `Índice`): las primeras
~30 líneas bastan. Baja a una entrada concreta únicamente si el índice no
responde. Ver *"Cómo se leen estos archivos"* más abajo.

**Y los dos que dicen qué es el proyecto:**

3. `_context/scope.md` — qué hace TEAPP y qué entra en la v1.
4. `_context/roadmap.md` — los 10 pasos, para saber qué significa el siguiente.

Son cortos a propósito. Léelos **siempre**: son el ancla contra inventar.

Si alguno no existe o está vacío, indícalo explícitamente en el reporte en lugar de
inventar contenido.

### Por qué el `git` va primero

> 🔑 **`progress.md` es lo que alguien escribió que pasó. `git log` es lo que pasó.**

Un archivo de estado puede quedar desactualizado —una sesión que se cayó, un
cierre a medias— y no tiene forma de avisarlo. El repositorio sí. Al leerlo
primero, entras a los archivos ya sabiendo si se les puede creer.

### Cuatro desfases que hay que reportar

| lo que ves | qué significa | dilo así |
|---|---|---|
| el último commit **no** aparece reflejado en `progress.md` | la sesión anterior no cerró bien | *"⚠️ `progress.md` va por detrás del último commit"* |
| `git status` tiene cambios sin commitear | quedó trabajo suelto de la sesión anterior | *"⚠️ hay N archivos sin commitear"* |
| la primera línea de `git status -sb` dice `ahead` | la sesión anterior **no subió**: el trabajo está solo en este disco | *"🚨 hay N commits sin subir a `origin` — el trabajo de la sesión anterior existe solo en este disco"* |
| hay commits que tocan `_persistence/` **posteriores** al último que tocó `progress.md` | el archivo de estado se selló antes que la última entrada: **puede estar diciendo que falta algo que ya está hecho** | *"⚠️ `progress.md` se selló en `<hash>` y hay N commits de `_persistence/` posteriores — su casilla de estado puede estar caducada"* |

🚨 **La cuarta es nueva y se cobró un arranque entero el 2026-08-14.** Se
comprueba con **dos** órdenes, no con una:

```
git log --oneline -3
git log --oneline -2 -- _persistence/progress.md
```

Si el hash de arriba **no** es el mismo que el de abajo, mira qué tocaron los
commits de en medio. Si tocaron `_persistence/` y `progress.md` no está entre
ellos, **el archivo de estado quedó congelado antes que la última entrada**.

> 🔑 **Y el error va en la dirección cara.** Un estado que dice *"ya está
> hecho"* cuando falta se descubre solo: alguien va a hacerlo y no lo encuentra.
> Uno que dice **"falta"** sobre algo terminado **no se descubre — se paga
> repitiéndolo**, y se paga con el arranque de la sesión siguiente, que es justo
> lo que este protocolo existe para ahorrar. Ver [L-062].

🚨 **La tercera es la más grave de las tres, y la única que se pierde para
siempre.** Las dos primeras son desorden: el trabajo está guardado, solo mal
contado. En la tercera el trabajo **no está guardado en ningún otro sitio** — un
disco que falle esa noche se lleva la sesión entera. Ver [L-006] y [L-009].

Es también la única que **no puede haberse anotado en `tasks.md`**: cuando el
cierre de anoche supo que el push había fallado, su commit ya estaba hecho. Por
eso el arranque tiene que mirarlo con sus propios ojos, en vez de fiarse de los
archivos. El razonamiento completo está en `protocol-close`, Paso 4.

Si la ves, **dilo arriba del todo y propón subirlo como primera acción del día.**

Si detectas un desfase, **el reporte lo dice arriba del todo**, antes del estado.
Es lo primero que el usuario necesita saber.

### 🚨 La regla que manda sobre todas

**Todo lo que digas sobre QUÉ ES el proyecto tiene que salir de un archivo que
abriste en esta corrida.** Si no lo abriste, no lo digas.

Vale para: las herramientas, el alcance, la arquitectura, y qué hace cada paso.
No completes con lo que suele llevar un proyecto de este tipo — **este proyecto
no es el típico, y lo que suene razonable casi nunca es lo que dice el archivo.**

Si algo no está escrito en ningún sitio, di **"no está registrado"**. Es una
respuesta válida y útil. Rellenarlo no lo es.

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

### 🚨 El campo manda sobre la prosa

En `tasks.md` cada fila termina en **dos columnas**: el estado (`✅` `🟡` `🔲`) y
el paso. **Para decir qué falta, lee el CAMPO DE ESTADO — no resumas el
párrafo.**

> 🔑 **El párrafo cuenta la historia de la tarea; el campo dice cómo acabó.** Y
> cuando alguien corrige una tarea suele reescribir el párrafo y **olvidarse del
> campo**, o al revés. Si los dos se contradicen, **no elijas: repórtalo como
> desfase** y sigue el campo mientras tanto.

Extraer los campos cuesta una orden y no gasta contexto:

```
grep -n "^| T-" _persistence/tasks.md | grep -E "\| 🔲 \| [0-9]+ \|$"
```

⚠️ **Esto pasó de verdad, tres veces con la misma tarea.** `T-090` se ofreció
como trabajo por hacer estando hecha: dos veces por prosa caducada y la tercera
porque la prosa ya decía *"CERRADA"* y **la columna seguía en `🔲`**. Ver
[L-062].

### 🚨 Lo tachado no existe — y pasa en DOS archivos, no en uno

**En `assumptions.md`** una suposición retirada se marca **tachando su id**:
`~~A-024~~`, y el texto explica dónde vive ahora (*"RETIRADA el …; vive ahora en
`[D-057]`"*). **El texto viejo se conserva a propósito**, para que se entienda
qué se creía y por qué era falso.

**Una fila con el id tachado NO se reporta como supuesto abierto. No se resume
su contenido. Se salta.** Si hace falta mencionarla, se dice *"retirada, vive en
`[D-nnn]`"* — nunca lo que decía antes.

⚠️ **`~~A-024~~` se reportó el 2026-08-14 como *"se da por cierto que la llave no
tiene tope de gasto, sin comprobar"*, estando retirada desde el 11 y siendo
falsa al revés: sí hay tope, un saldo prepagado con la recarga apagada
(`[D-057]`).** El texto estaba ahí para leerse; el `~~` estaba ahí para no
leerlo.

**En `decisions.md` pasa lo mismo**, y es más traicionero: una decisión
`~~D-nnn~~` puede estar 🔻 **SUPERADA** (otra la reemplazó, **y sus números ya
no son los del código**) o ✅ **CUMPLIDA** (su mandato se ejecutó y se acabó).
**Ninguna de las dos se reporta como decisión abierta**, y de una superada **no
se cita ni un número**.

Una sola orden cubre los dos archivos:

```
grep -n "^| ~~" _persistence/assumptions.md _persistence/decisions.md
```

⚠️ **Los dos fallos que obligaron a escribir esto ocurrieron el 2026-08-14, en
la misma corrida:**

- `~~D-071~~` se citó con sus números (`8,0 s`, `read 4,0`) como si fueran los
  del código. Lo son desde `[D-072]`: **`9,0` y `read 6,5`**. Pasó **dos veces**.
- `~~D-080~~` se presentó como *"decisión crítica abierta"* teniendo `[D-081]`
  encima, que la cumplió entera.

🔑 **Y el motivo por el que cuesta verlo: la corrección vive en la fila de la
decisión NUEVA, y quien busca por tema encuentra la VIEJA.** El índice se lee de
arriba abajo por fecha, pero se **busca** por asunto. Ver `[L-066]`.

📌 **Marcadas hoy solo las que se vieron fallar. Puede haber más.** Si una fila
del índice te da un número, **contrástalo con el código antes de reportarlo** —
es lo único que separa un dato de un recuerdo (`[L-063]`).

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
🔻 <disparador del próximo paso, si lo hay>   <-- obligatorio si existe, y va PRIMERO
1. <tarea> — <prioridad/bloqueo si aplica>
2. ...

## Contexto relevante        <-- omitir esta sección si no leíste archivos del Paso 2
- **Decisiones:** ...
- **Supuestos:** ...
- **Restricciones:** ...
- **Lecciones:** ...
```

Reglas del reporte:

- 🔻 **El disparador del próximo paso es OBLIGATORIO si existe, y va el primero
  de "Siguientes tareas".** Búscalo en la casilla *siguiente acción* de
  `progress.md` y en la decisión que cerró el paso actual. Hoy es: **antes de
  cambiar `MODEL` —cada vez—**, leer en la consola el límite por minuto de ese
  modelo en `teapp-measure` y ponerlo en `LAB_REQUESTS_PER_MINUTE` en el mismo
  cambio (`[D-081]`, `T-088`).

  ⚠️ **Un disparador se cita por su ACCIÓN, no por la fecha en que se espera.**
  Escribirlo como *"lo primero del paso 9"* lo deja gastado tras el primer
  cambio de modelo, y `[D-049]` mete dos (Sonnet 5 y Haiku 4.5). Ver `[L-064]`.

  🚨 **Un disparador no se cuelga de una tarea que no lo tiene.** El 2026-08-14
  una corrida se lo colgó a `T-081` —*"sin disparador del paso 9. Bloqueante si
  cambia el modelo"*, dos frases que se contradicen en el mismo renglón— cuando
  era de `T-088`. **Si no sabes de cuál es, dilo suelto: el disparador importa
  más que su dueño.** Ver `[L-064]`.
- 🚨 **No inventes relaciones entre tareas.** Cada tarea se describe con lo que
  dice **su** fila. Si dos se parecen, no se mezclan: se citan las dos por su
  número.
- Máximo 5 elementos por lista; si hay más, quédate con los más recientes o
  prioritarios y dilo.
- Cita el archivo de origen cuando un dato pueda ser ambiguo.
- Incluye la sección **Contexto relevante** solo con lo que cambie la decisión de qué
  hacer ahora, no como resumen de los archivos.
- Termina señalando bloqueos o información faltante, si los hay.
- No modifiques ningún archivo de `_persistence/`: este protocolo es de solo lectura.
