# TEAPP — Teaching English Application

Agente de IA para practicar inglés escrito, puesto en producción de verdad:
navegador, identidad, servidor propio y despliegue en la nube.

**Qué hace exactamente y hasta dónde llega la v1 → `_context/scope.md`.**

## Con quién hablas

Quien construye esto está aprendiendo a programar desde cero.

- **La FORMA es de producto.** Estructura, commits, tests, frenos, despliegue.
  Nada se simplifica "porque está aprendiendo".
- **La VOZ es de profesor.** Español siempre, también en los comentarios del
  código. Concepto antes que código: analogía primero, término técnico después.
  Frases cortas.
- ⚠️ **Una pregunta a la vez.** Con varias preguntas juntas se pierde; con una
  sola las contesta todas bien.
- Explica en prosa, no con menús de opciones.
- Cuando se trabe con un error, no lo hagas sentir lento. Trabarse es lo normal.

> 🔑 **Al estudiante trátalo como principiante; al proyecto trátalo como producto.**

## Reglas duras — no se rediscuten

Si crees que alguna está mal, **dilo, no la cambies solo.**

1. 🚨 **La API key jamás toca el navegador.** Todo lo que llega al navegador el
   usuario lo puede leer. La llave vive en el servidor y no sale de ahí.
2. 🚨 **Nada de `input()` ni de nada que espere a un humano.** En un servidor no
   hay teclado: se cuelga para siempre.
3. **Los permisos se escriben de antemano**, no se preguntan. Y **denegar por
   defecto**: lo que no esté permitido explícitamente, se rechaza.
4. 🚨 **No abrir la cuenta de la nube hasta el paso 7.** El plan gratuito corre
   **6 meses desde el día que se abre**, se use o no el proyecto. Abrirla "para
   ir mirando" quema semanas sin construir nada.
5. **El objetivo máximo es aprender. Minimizar factura manda sobre todo lo demás.**
6. **Un número sin una corrida detrás no se escribe**, o se marca como estimación.
   Nada de costos, tiempos ni porcentajes sacados de memoria.
7. **Nunca escribir la API key dentro de un archivo de código.** Va en `.env`,
   que está en `.gitignore`. Nunca imprimirla completa.

## Cómo se escribe el código

**PI-1. Razona antes de actuar, y no decidas en silencio.** Ante una ambigüedad
que cambie el resultado, **detente y pregunta** — una sola pregunta, en prosa, no
un menú de opciones. Lo que decidas conmigo va a `decisions.md` en el momento.

**PI-2. Simplicidad primero.** Código mínimo, interfaces simples. Nada de
abstracciones, parámetros ni configurabilidad que no se hayan pedido. La pregunta
es la misma del alcance: **¿hace falta para que esto funcione hoy?**

**PI-3. Cambios quirúrgicos.** Toca solo lo que la tarea necesita. No
refactorices lo que funciona. No borres código muerto preexistente sin permiso.
🔑 El `git diff` del día es lo que se registra al cerrar: si viene lleno de
cambios que nadie pidió, el registro deja de servir.

**PI-4. Terminado = visto funcionando.** Donde hay lógica, un test que la
respalde. Donde hay pantalla, correrla. Lo que no se ha corrido no está
terminado, aunque el código exista.

**PI-5. Nombres en inglés, contenido en español.** El idioma se parte por
función, no por archivo:

| en inglés | en español |
|---|---|
| funciones, variables, archivos, carpetas | comentarios y docstrings |
| ramas y mensajes de commit | lo que se responde en el chat |
| los textos que ve quien usa la app | los mensajes de error y de sistema |

El **identificador** lo lee Python y quien abra el repo: ahí el inglés evita el
híbrido feo (`contar_words`). La **explicación** la lee quien está aprendiendo: en
su idioma se entiende mejor. Un error de sistema es explicación, no interfaz.

⚠️ **Guion bajo en los nombres de módulo, nunca guion.** `english_tutor`, no
`english-tutor`: Python lee el guion como una resta y el `import` no compila.

## Dónde está lo demás

Este archivo no lleva el detalle. Ábrelo cuando toque:

| archivo | ábrelo cuando… |
|---|---|
| `_context/scope.md` | dudes si algo entra en la v1 o no |
| `_context/architecture.md` | toques el servidor, la pantalla, la llave o los permisos |
| `_context/roadmap.md` | acabes un paso, o no sepas qué toca después |
| `_persistence/` | inicio y cierre de sesión (ver abajo) |

⚠️ **Si no lo abres, no lo sabes.** No supongas la arquitectura ni el alcance:
están escritos. Inventarlos suena convincente y cuesta un rediseño.

---

## Inicio de sesión

Al comenzar cada sesión de trabajo, antes de responder cualquier otra cosa, delega en
el agente `session-starter` y muestra su reporte al usuario. Solo después de eso
atiende la petición del usuario.

Aplica también cuando el usuario pida retomar el trabajo a mitad de conversación
("¿en qué íbamos?", "estado del proyecto").

El procedimiento vive en la skill `protocol-start`; no lo repliques aquí ni lo
ejecutes por tu cuenta.

## Cierre de sesión

Al terminar cada sesión de trabajo, delega en el agente `session-closer` y muestra
su reporte al usuario. Él actualiza `_persistence/` y hace el commit del día.

Aplica también cuando el usuario lo pida a mitad de conversación ("cerremos",
"guarda el avance", "terminamos por hoy").

El procedimiento vive en la skill `protocol-close`; no lo repliques aquí ni lo
ejecutes por tu cuenta.

## Persistencia

`_persistence/` es la memoria de **cómo se construyó** el proyecto, entre sesiones.

**Quién escribe cada archivo depende de dónde nace la información:**

| archivo | qué guarda | quién lo escribe | cuándo |
|---|---|---|---|
| `progress.md` | estado general: en qué paso va y qué se logró | `session-closer` | al cerrar |
| `tasks.md` | tareas hechas y las siguientes | `session-closer` | al cerrar |
| `decisions.md` | decisiones tomadas, con su porqué y su fecha | **tú** | en el momento |
| `assumptions.md` | suposiciones **sin comprobar** | **tú** | en el momento |
| `constraints.md` | restricciones del proyecto | **tú** | en el momento |
| `lessons.md` | lecciones aprendidas construyéndolo | **tú** | en el momento |

**Por qué se parten así:**

Lo que hiciste **queda en el `git diff`**, así que `session-closer` lo puede
reconstruir al final del día sin haber estado presente.

Lo que **decidiste** no queda en ningún lado. Nace en la conversación y ahí se
muere. Por eso los cuatro de abajo los escribes **tú, en el momento en que pasan**,
no al cerrar.

> 🔑 **Una decisión anotada tres horas después es una decisión a medio recordar.**
> El porqué es lo primero que se evapora.

**Cuándo escribir cada uno, sin esperar al cierre:**

- Elegiste entre alternativas y la elección condiciona el código futuro
  → `decisions.md`. Anota **qué elegiste, contra qué, por qué y la fecha**.
- Estás dando algo por cierto sin haberlo comprobado
  → `assumptions.md`. Anota también **cómo se comprobaría**.
- Apareció un límite nuevo: dinero, tiempo, plataforma, alcance
  → `constraints.md`.
- Algo falló y entendiste por qué
  → `lessons.md`.

**Todos tienen la misma forma: índice arriba, entradas debajo** con ancla
(`### [D-001]`). El formato exacto de cada entrada está escrito dentro del propio
archivo, en un comentario al final.

- **Para leer:** abre la cabecera, no el archivo. El índice suele bastar; baja a
  una entrada solo si no responde, buscándola por su ancla.
- **Para escribir:** 🚨 **entrada e índice se actualizan juntos.** Una entrada que
  no está en el índice no existe: nadie lee el archivo entero para encontrarla.

**Las suposiciones se mueren ascendiendo:** cuando una se comprueba o se decide,
**sale** de `assumptions.md` y entra en `decisions.md` o en `lessons.md`. Bórrala
del primero. No puede vivir en dos sitios: una de las dos copias acabaría mintiendo.

### 🚨 Cómo se citan las lecciones: `[L-nnn]` aquí, `[LM.nn]` allá

Hay **dos** repositorios con lecciones numeradas, y sus números **se solapan**:

| prefijo | dónde vive | qué guarda |
|---|---|---|
| `[L-013]` | `TEAPP/_persistence/lessons.md` — este repo | lecciones de construir TEAPP |
| `[LM.13]` | `Edu_TripleS/PROGRESO.md` — repo supervisor | lecciones de **método** |

**Una letra de diferencia, y `13` existe en los dos.** Una cita equivocada no da
error: manda a quien la siga a una entrada real que habla de otra cosa, y esa
persona concluye que no entendió — no que la cita estaba mal.

> 🔑 **La doble letra siempre para el supervisor; el guion solo para este repo.**
> Nunca al revés, nunca sin prefijo.

⚠️ **Y antes de citar, abrir la entrada.** Una cita que ya aparece en varios
sitios tranquiliza igual que un test en verde y deja de auditarse: se propaga
**por parecer verificada**. El 2026-08-09 se encontraron **nueve** citas
equivocadas de esta forma, la misma significando tres cosas distintas. Ver
`[L-034]`.

📌 Si la frase no la dice ninguna lección de ningún repo, **se quita el corchete y
se deja suelta**. Una frase sin puntero es honesta; un puntero falso no.

⚠️ **`_persistence/` sí va a Git** — es historia del proyecto.
**`data/` no** — son datos de las personas que usan la app.
Son dos memorias distintas y se confunden fácil.
