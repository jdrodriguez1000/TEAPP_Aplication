# Lecciones aprendidas — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [L-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

| id | fecha | qué se aprendió | a raíz de |
|---|---|---|---|
| L-029 | 2026-08-08 | 🚨 **Lo que nace DESPUÉS del cierre no tiene dueño.** El `session-closer` corre **una vez** y el commit del día ya está hecho: cualquier archivo escrito después cae en tierra de nadie. Hoy pasó con `[D-044]` —escrita a las 13:37, veinte minutos después del cierre de las 13:17— y se salvó solo porque la conversación siguió; con levantarse de la silla se quedaba en el disco. ⚠️ **Y no es un accidente raro: es donde va a volver a pasar**, porque en este proyecto las decisiones buenas salen conversando *después* de que el trabajo técnico acabó. 🔑 **Una costura no deja hueco:** al abrir mañana se lee un día que terminó limpio y sin nada pendiente, y nadie echa de menos lo que no está. 🔧 Regla: **lo que se escriba después del cierre se commitea en el momento, no se aplaza al día siguiente.** 📌 Se estuvo a punto de aplazar ESTA entrada por no ensuciar el árbol recién limpio — argumento estético que es el propio hallazgo aplicándose a sí mismo: **el árbol limpio no es el objetivo del protocolo, es su efecto secundario** | `[D-044]` escrita tras el cierre `84599f5`; revisión externa |
| L-028 | 2026-08-08 | 🚨 **Partir una tarea en dos deja al guion operativo describiendo la mitad vieja — y ningún `grep` lo encuentra.** `console_steps.md` paso 3 punto 5 decía *"Elastic IP: reservarla y asociarla"*, escrito cuando la IP no existía; al partirse `[T-059]` el 2026-08-06 se ejecutó **solo reservar** y el punto se quedó igual. Ejecutarlo al pie de la letra —que es lo que el archivo **manda** hacer— llevaba a `Allocate` y a una **segunda** dirección, y la IP que cobra es justo **la ociosa**. 📌 No costó dinero: lo cazó una revisión externa minutos antes del clic. 🔑 **La diferencia con `[L-018]` y `[L-025]`:** allí una copia diverge **porque alguien edita otra**, y se caza con `grep`; aquí **nadie editó nada — cambió el mundo que la frase describía**. No hay dos frases en desacuerdo, hay una sola que era verdad y dejó de serlo. 🔧 Regla: **el commit que parte una tarea revisa el guion que la ejecuta** — *¿algún paso escrito describe trabajo que ya está hecho?* ⚠️ Segunda mitad del mismo día: el aviso de no aceptar el `launch-wizard` (que dejaba el **22 abierto al mundo** y el grupo de `T-060a` sin usar) vivía **solo en el chat** — `[L-013]` con otro traje. Los dos huecos se escribieron **antes** de tocar la consola | revisión externa antes de lanzar la EC2 de `T-059` |
| L-027 | 2026-08-07 | 🚨 **Esta vez el ciego fue el CONTROL, no la medida — y un control ciego devuelve el mismo verde que uno que funciona.** Midiendo `T-055` se hizo lo correcto: antes de creerse el resultado bueno (`origen 172.17.0.4`, la dirección real), arrancar uvicorn **sin** `--proxy-headers` para verlo fallar. **Salió verde igual.** No porque la cadena fuera robusta, sino porque en uvicorn 0.52.1 esa bandera **ya viene puesta por defecto** — dato que `[D-034]` tenía escrito desde el 2026-08-06 y que se olvidó al diseñar el control. 🔑 **El sabotaje no saboteaba nada**, así que su verde no era información: era silencio, exactamente `[L-020]`. El rojo de verdad exigió romper la bandera que sí manda — `--forwarded-allow-ips 203.0.113.5`— y entonces el log escribió `127.0.0.1`, con `[A-014]` a la vista. ⚠️ **La novedad respecto a `[L-020]`:** allí el instrumento ciego era el que medía; aquí era **el que autorizaba a creerse la medida**, que es peor — un control ciego no da un falso negativo, da permiso. 🔧 Regla: **el control se diseña contra el valor por defecto, no contra la bandera escrita.** Quitar una opción no la apaga si la librería ya la trae puesta; hay que ponerle un valor **activamente equivocado**. 📌 Cuarta vez del mismo bicho en tres sesiones (`[L-019]`, `[L-020]`, `[L-021]`, esta) | medir la mitad de Caddy de `T-055` en contenedor |
| L-026 | 2026-08-07 | 🚨 **`T-068` es el único control del proyecto ESTRUCTURALMENTE inverificable, y por eso no es un freno: es disciplina.** `LM.13` pide haber visto morder el control; este **no se puede ver morder nunca**, porque **probarlo ES el desastre** — cruzar una de las siete puertas evapora los créditos sin vuelta atrás. 🔑 La diferencia que importa: **un freno no se degrada con la repetición; la disciplina sí.** Y el desgaste ya tiene fecha de inicio — `[A-018]` obliga a abrir *Facturación y costos* **a diario** durante semanas, y es la misma página donde vive *"Actualizar plan"*. **Lo que se hace:** no llamarlo freno, y **sacar de la lista el riesgo con tráfico** — *"Actualizar plan"* pasa a ser una línea del **protocolo de lectura**, no el renglón 8 de `[C-005]`. Un control inverificable etiquetado como "freno" da la misma calma que uno probado y no la merece: `[L-013]` con otro traje |
| L-025 | 2026-08-07 | 🚨 **Cambiar un dato no termina cuando se cambia el dato: termina cuando se ha hecho `grep` de sus copias.** El defecto que más veces ha vuelto — siete contando las de hoy. Solo el 2026-08-07: `app/config.py` y `app/api.py:40-42` con **la misma frase** describiendo una plataforma descartada en `[D-029]` hace dos días; y retirar `[A-019]` dejó **cinco punteros a un ancla que ya no existe** (`test_deploy_limits.py:103,108`, `decisions.md:271`, `Caddyfile.template`, `tasks.md:65`, `progress.md:149,151`). 🔑 Lo grave son las dos primeras: **un comentario pegado a la línea que ejecuta se lee como la explicación autorizada de esa línea**, y nadie duda de él porque está al lado — ese justificaba `os.environ.setdefault` con un motivo muerto, y la regla resultó correcta **por otra razón** (`[D-039]`). ⚠️ Y **el arreglo genera el bicho**: limpiar `assumptions.md` es lo correcto y ensucia en otro sitio — `[L-023]` con el signo cambiado, la corrección ensuciando lo que corrige. 🔧 Tras cambiar un hecho: `grep` del ancla y de las palabras de la frase por `_persistence/`, `_context/`, `deploy/`, `app/` y `tests/`; lo que sea de otro dueño se deja escrito **por número de línea** | retirar `[A-019]` y corregir la precedencia del `.env` |
| L-024 | 2026-08-07 | 🚨 **"Necesita la nube" era falso, y se dio por cierto sin recorrer la lista.** `deploy/install.sh` —escrito el 2026-08-05, **nunca corrido**, solo `bash -n`— corre entero en un contenedor Ubuntu 24.04: `apt-get`, Caddy 2.11.4, `venv`, `pip` y el `.env`, y muere en `systemctl: command not found` (línea 223), **después** de la parte que importaba. Con eso se midió `[A-008]` sin EC2 y se probó `[D-038]`. 🔑 El fallo de origen fue de **censo**, no técnico: "no hay nada sin nube" es una afirmación sobre un conjunto que nadie recorrió, con un número inventado encima ("once pendientes" cuando el `grep` propio devolvía **catorce**) — `[L-021]` otra vez. 🔧 Montaje: `git ls-files` y no copiar la carpeta (el `.venv` y `node_modules` de **Windows** habrían hecho al guion saltarse el paso de Python y medir otra cosa), y `MSYS_NO_PATHCONV=1` o Git Bash convierte `/opt/teapp` en ruta de Windows. 📌 Se descartó un test que leía el **texto** del guion: ruidoso al renombrar, ciego al cambiar `-f` por `-e` — mide la forma, no el comportamiento. **Regla: antes de escribir "bloqueada", preguntarse qué mitad no lo está**. 🔻 **Ampliada el 2026-08-07**: aplicada la regla a lo que la propia lección dejaba fuera, **la sección 5 no se había ejecutado nunca** — dentro vivía `caddy validate` (línea 237). Corrida a mano: ✅ `Valid configuration`, salida 0, sin marcadores sin sustituir, con `request_body max_size 16KB` y `reverse_proxy 127.0.0.1:8000`. ⚠️ Mide **sintaxis, no comportamiento**. 📌 Y cayó una suposición sobre el propio contenedor: **NO hay aparejo Caddy↔uvicorn** ahí dentro, su `Caddyfile` es **el de fábrica** con `reverse_proxy` comentado — casi se le pide una medición que no podía dar, **y habría contestado algo**. 🔑 La **receta** (`docker run … ubuntu:24.04 sleep infinity`, todo por `docker exec … sh -c`) vivía solo en un scrollback: ya está en `deploy/README.md`. El contenedor es desechable; la receta no | intentar `T-050` sin máquina, tras una revisión externa |
| L-023 | 2026-08-06 | 🚨 **Lo que ensució los datos reales fue el instrumento de medida.** `T-072` cerrada: el camino de `[A-020]` era `measure_body.py`, la báscula de `T-054`, escrita y ejecutada seis horas antes (19:48:32 UTC = 14:48:32 local, un segundo antes de que nacieran los archivos). Se registró como `otronombrelargo` y practicó 5 veces —los 5 casos de `CASES`—, de ahí `{"score": 5}` y `{"used": 5}`. 🔑 **El mecanismo es de manual: el aislamiento necesitaba TRES desvíos y la báscula se acordó de UNO.** Desvió `accounts.ACCOUNTS_FILE` a un temporal —con su comentario *"medir no debe tocar `data/`"`*— y dejó `USERS_DIR` y `QUOTA_DIR` apuntando a los datos de verdad. Y eso explica la contradicción que abrió `[A-020]`: la cuenta no estaba en `data/accounts.json` **porque `accounts.json` fue justo el único que sí se desvió**; la cuenta se creó en el temporal, el marcador y la cuota en los datos reales. 📌 **No es un accidente, es un patrón:** `probe-log.json`, el otro huérfano de `data/users/`, sale del 2026-08-05, otra sesión y otro día. ⚠️ **Y el portero de `T-071` no lo verá nunca**, porque vive dentro de pytest y una báscula corre fuera. Encadena con `[L-020]` (un instrumento ciego da silencio) y `[L-022]` (un `md5` dice "los bytes, iguales"): **el instrumento que mide puede ensuciar lo que mide** | resolver `T-072` — el rastro estaba en las transcripciones, no en el historial de PowerShell |
| L-022 | 2026-08-06 | 🚨 **Un `md5` no dice "todo igual": dice "los bytes, iguales".** Restaurando `data/` tras el sabotaje de `T-071` (`rm -rf data && cp -r copia data`) se verificó con huella de contenido — siete archivos, siete huellas idénticas, restauración correcta. Y era cierto: **ningún dato de la aplicación se perdió.** Lo que se destruyó fue el **`mtime`**, y con él la prueba física del camino de las 14:48 de `[A-020]` — incluida la más fuerte, que el marcador y la cuota llevaban el mismo nanosegundo. 🔑 **Vuelta nueva sobre `[L-020]`/`[L-021]`:** los casos anteriores eran instrumentos **ciegos a un cambio**; este vio perfectamente el cambio que le importaba y fue ciego a **una dimensión entera del archivo**. Un archivo es contenido **y** metadatos, y `md5` solo mira la mitad. ⚠️ **Y estrenó `[L-021]` el mismo día en que se escribió, dentro de la verificación del portero construido contra ese defecto.** 📌 Regla que queda: **la prueba de un defecto no puede vivir en la carpeta que el defecto ensucia** — se copia a `_persistence/`, que sí va a Git, ANTES de tocar nada. Y antes de restaurar por copia, preguntarse qué del original no viaja en los bytes | restaurar `data/` tras sabotear el portero de `T-071` |
| L-021 | 2026-08-06 | 🚨 **El titular que contradice su propia salvedad — `[L-020]` por el lado acusatorio.** Un análisis tituló *"la trampa ya se disparó"* y tres líneas después escribió *"te lo doy como sospecha fuerte, no como hecho medido"*. Las dos frases no pueden ser ciertas a la vez, y **la que se recuerda es el titular**. La medida (md5 + fecha de los 5 marcadores, suite entera, huella idéntica) dijo lo contrario: la suite de hoy **no** escribe en `data/`. 🔑 `[L-020]` decía que el silencio no confirma que todo esté bien; esto es la otra mitad: **el silencio tampoco confirma que algo esté mal**. Ausencia de historial no es evidencia en ninguna de las dos direcciones. ⚠️ **Y una salvedad correcta no arregla un titular falso** — si la salvedad y el titular discrepan, el que hay que cambiar es el titular | la auditoría de `T-071` |
| L-020 | 2026-08-06 | 🚨 **El modo de fallo característico de este proyecto, ya con nombre: un verde producido por algo distinto de lo que el verde afirma.** El caso: se dijo *"verifiqué con `git status` que `data/` quedó intacto"* — y **`data/` está en `.gitignore` (línea 18)**. `git status` habría callado igual si los tests hubieran escrito ahí. La conclusión era correcta, pero **se supo por suerte, no por la prueba citada**; el testigo que se invocó no estaba mirando. 🔑 **Antes de citar una prueba, preguntar si el instrumento PUEDE ver el fallo que se descarta** — un instrumento ciego no da un falso negativo, da silencio, y el silencio se lee como verde. Se comprobó por el camino que sí ve: las fechas de `data/users/*.json`. Tercera vez en dos sesiones (`[L-019]`, el test contra 16384 de `[D-035]`, y esta): ya no es casualidad | la auditoría de `T-054` |
| L-019 | 2026-08-06 | **El sabotaje que llegaba disfrazado de aquello que quería atacar.** Para probar que uvicorn ignora `X-Forwarded-For` de un desconocido se le habló por `127.0.0.2`, dando por hecho que sería una dirección no confiable. Windows pone **`127.0.0.1` como origen** aunque el destino sea `127.0.0.2`: la petición entraba **como si fuera Caddy**, y el escenario medía justo lo contrario de lo que decía medir. 🔑 **De un test se verifica el montaje, no solo el resultado** — aquí salió rojo y el rojo era mío; si llega a salir verde por la misma razón, se habría cerrado `T-055` sobre nada | medir `[A-014]` con uvicorn real, T-055 |
| L-018 | 2026-08-06 | **En este proyecto los datos se replican solos, y corregir uno no corrige los demás.** Una frase falsa sobre la alarma de facturación vivía en **cinco** sitios (entrada, fila de índice y "Estado actual" de `progress.md`; dos puntos de `A-018`; y un párrafo de `console_steps.md`). 🚨 **Tercera vez con el mismo bicho:** sesión 33 (el repo "privado"), sesión 41 (lo mismo otra vez), y ahora. Ya no es casualidad: el formato de este repo —índice + entrada, más `deploy/` explicando lo mismo en operativo— **obliga a duplicar por diseño**. 🔑 **Corregir es ir a BUSCAR las copias, no editar donde se encontró el error** | la segunda auditoría de `A-018` |
| L-017 | 2026-08-05 | **Un control que comprueba MENOS de lo que su propio comentario promete.** El bloque final de `install.sh` se titulaba *"PI-4: terminado = visto funcionando"* y dos líneas después solo miraba `systemctl is-active` — que demuestra que systemd **lanzó** el proceso, no que la app conteste. Con `Restart=always`, una app que revienta al arrancar se ve `active` y el guion imprimía **"Listo"** sobre algo muerto. 🔑 **El comentario correcto hizo de coartada: nadie audita un bloque que ya se declara auditado.** ⚠️ Y el arreglo trajo la misma criatura con el signo cambiado: reintentos para lo que tarda segundos y ninguno para lo que tarda minutos — **un falso verde y un falso rojo son el mismo error** | revisión de `deploy/`, T-063 |
| L-016 | 2026-08-05 | **Dos veces el mismo error, un piso más abajo cada vez — y las dos veces el hecho salió de la FORMA del texto, no del texto.** Primero: *una lista que tiene sentido parece completa* (3 puertas de AWS se dieron por las 7). Y al corregirla, otra vez: *un documento que no dice "no" parece que dice "sí"* — de cinco de las siete puertas la doc **calla**, y ese silencio se leyó como respuesta favorable. 🔑 **El silencio de una fuente no es un dato** | cerrar `[A-016]`, T-068 |
| L-015 | 2026-08-04 | **El fixture que creía limpiar y no limpiaba.** Para medir el log sin trampas se vaciaron los handlers del raíz en un fixture — y `caplog` los repone **después** de los fixtures. El test volvía a medir el estado de pytest y lo llamaba "lo que hace la función": [L-012] otra vez, y esta vez dentro del arreglo de [L-012] | escribir `test_log_config.py`, T-033 |
| L-014 | 2026-08-04 | **Una suposición que dice qué la mata se muere sola cuando toca.** `[A-012]` llevaba escrita su propia condición de cierre; el día que se cumplió, retirarla no fue un juicio sino una comprobación. Y al retirarla se vio que no era una, sino dos: se partió en `[A-013]` y `[A-014]` | retirar `A-012` al cerrar T-053 |
| L-013 | 2026-08-04 | **Cerrar un hueco no cierra los demás**, y los que quedan no se parecen al que cerraste — por eso no se ven. El candado tapó el hueco entre leer y escribir; quedaron abiertos otros cuatro, y los cuatro cobraban o regalaban de más | los sabotajes a los frenos del paso 6 |
| L-012 | 2026-08-04 | El límite estaba **escrito** —`[A-003]` decía que un `logger.info` se pierde— y aun así se cruzó. El test lo tapó bajando el listón: `caplog.at_level(INFO)` pinta de verde un renglón que en el servidor no existe | escribir el motivo del frenazo de la cuota, T-038 |
| L-011 | 2026-08-04 | El portero de red tenía una puerta de atrás abierta —`connect_ex` devuelve un código en vez de lanzar— y su propio control no la veía: el control usaba un nombre, y lo mataba otro parche | escribir el portero de red, T-047 |
| L-010 | 2026-08-04 | 191 tests en verde y el servidor de verdad reventaba: `TestClient` no es uvicorn, y comprobar el efecto no es comprobar la respuesta | correr el paso 5 a mano, `/logout` |
| L-009 | 2026-08-04 | Una regla que vive en dos archivos se corrige en los dos: `protocol-close` prometía algo que `protocol-start` no leía | arreglar T-049, el desfase del cierre |
| L-008 | 2026-08-03 | Se comparó la opción rival en su versión floja y se le ganó a esa: eso no es comparar, es elegir y buscar razones después | revisar dónde vive el control del `.js`, T-037 |
| L-007 | 2026-08-03 | La comprobación que mide **de más**: `diff -r` gritaba "viejo" con el repo correcto. Un control se mide dos veces —con el fallo puesto y sin él— o no se midió | escribir el control del `.js` compilado, T-037 |
| L-006 | 2026-08-03 | El cierre se cumplió entero y el trabajo se quedó sin subir: si el hash no está en `origin`, no hubo cierre | la revisión cruzada del paso 4 |
| L-005 | 2026-08-03 | Buscar una palabra en un archivo entero no es comprobar el código: los comentarios también cuentan | el primer test de la pantalla, paso 3 |
| L-004 | 2026-08-02 | Una prueba que el código roto también pasa no prueba nada | validar el arreglo de concurrencia del paso 2 |
| L-003 | 2026-08-02 | 45 tests en verde no vieron un fallo que rompía 7 de cada 10 peticiones | la revisión externa del paso 2 |
| L-002 | 2026-08-02 | `pip install` sin versión fijada no da la misma versión dos veces | crear el `.venv` del paso 1 |
| L-001 | 2026-08-02 | La consola de Windows no pinta caracteres fuera de ASCII | correr `main.py` por primera vez |

---

## Entradas

### [L-029] 2026-08-08 — Lo que nace después del cierre no tiene dueño

- **Qué pasó.** El cierre commiteó a las `13:17:05`, con el árbol limpio y el
  control verificado. A las `13:37:41` —veinte minutos después— la conversación
  produjo `[D-044]`, una decisión con **fecha de caducidad de una noche**. El
  `session-closer` ya no existía y el commit del día ya estaba hecho: nadie era
  responsable de guardarla. Se salvó porque se siguió hablando.
- 🔑 **El mecanismo, y por qué va a repetirse.** No es un descuido de nadie: es
  estructural. El cierre corre **una vez**. Y en este proyecto las decisiones
  buenas nacen justo ahí — después de que el trabajo técnico acabó, cuando ya
  se puede pensar. **La costura está exactamente donde más se escribe.**
- ⚠️ **Por qué no se detecta al día siguiente.** Una costura **no deja hueco**.
  Al abrir sesión se lee `_persistence/` y se ve un día que terminó limpio y
  sin nada pendiente. No hay archivo a medias ni test rojo que delate la
  ausencia. Es el mismo modo de fallo mudo de `[A-009]` y `[A-017]`, aplicado
  al protocolo en vez de al código.
- 🔧 **Regla:** lo que se escriba después del cierre **se commitea en el
  momento**, no se aplaza al cierre siguiente.
- 📌 **Y el intento de aplazarla, que es la mitad interesante.** Se estuvo a
  punto de dejar esta entrada para mañana con el argumento *"acabamos de dejar
  el árbol limpio y no me apetece ensuciarlo para contar que se ensució"*. Una
  revisión externa lo señaló: eso es **el propio hallazgo aplicándose a sí
  mismo** —aplazar al día siguiente una lección sobre el trabajo huérfano del
  día siguiente— y el argumento es estético. 🔑 **El árbol limpio no es el
  objetivo del protocolo: es su efecto secundario.** Ensuciarlo veinte segundos
  para guardar lo aprendido es el mismo intercambio que se hizo media hora
  antes con `[D-044]`, y fue el correcto las dos veces.
- ⚖️ **Lo que esta entrada NO dice, escrito a propósito.** La misma revisión
  propuso antes otra lección —*"el cierre no se comprueba con «¿hay hash?» sino
  con `git status` limpio después"*— sobre el supuesto de que el cierre había
  **omitido** `decisions.md`. Los `mtime` lo desmintieron: el archivo se
  escribió veinte minutos después, el control corrió y dio verde, y habría dado
  verde igual porque no había nada que cazar. **Esa lección se descartó por
  venir de un no-evento**, y anotarla habría envenenado el archivo. 📌 El
  síntoma era bueno (`D-044` estaba en un solo disco); la causa, no. **Acertar
  el síntoma no vuelve buena la causa.**
- ❓ **Queda una decisión de diseño abierta, sin prisa:** si el cierre debería
  poder correrse **dos veces** en un mismo día. No se decide hoy.

### [L-028] 2026-08-08 — Partir una tarea en dos deja al documento diciendo la mitad vieja

- **Qué pasó, y hasta dónde llegó.** `deploy/console_steps.md`, paso 3, punto 5,
  decía *"Elastic IP: reservarla y asociarla a la instancia"*. Se escribió cuando
  la IP no existía. El 2026-08-06 `[T-059]` se partió en dos por `[A-018]`, se
  ejecutó **solo la mitad de reservar**, y el punto 5 se quedó igual — describiendo
  un trabajo del que la mitad ya estaba hecha. 📌 **No llegó a costar dinero: lo
  cazó una revisión externa minutos antes del clic.**
- 🚨 **Lo que habría costado.** El guion se ejecuta a propósito sin decidir dentro
  de la consola (así está escrito arriba del propio archivo), así que "hacer lo que
  dice el punto 5" era el comportamiento **correcto** — y llevaba a pulsar
  `Allocate Elastic IP address`. Resultado: **una segunda dirección**, y en AWS la
  IP elástica que cobra es justo **la que no está asociada a nada**. Un goteo
  silencioso, del tipo que `[A-018]` todavía no ha visto detectar.
- 🔑 **La novedad respecto a `[L-018]` y `[L-025]`.** Aquellas hablan de copias que
  divergen **porque alguien edita una y no las otras**: el arreglo es hacer `grep`
  de las copias al cambiar un hecho. Aquí **nadie editó nada**. El documento no
  cambió; **cambió el mundo que describía**. Ninguna búsqueda de texto lo encuentra,
  porque no hay dos frases en desacuerdo — hay una frase sola, que era verdad y dejó
  de serlo.
- 🔧 **Regla que queda:** cuando una tarea se parte en dos, el mismo commit que la
  parte revisa **el guion operativo que la ejecuta**. Partir es un cambio de estado
  del mundo, no solo de `tasks.md`. La pregunta concreta: *¿algún paso escrito
  describe ahora trabajo que ya está hecho?*
- ⚠️ **Y hay una segunda mitad, del mismo día y del mismo tipo.** El aviso de no
  aceptar el `launch-wizard` del asistente —que habría dejado el **22 abierto al
  mundo** y el grupo de `T-060a` sin usar— existía **solo en la conversación**. El
  paso 3 no nombraba el cortafuegos ni una vez. Es `[L-013]` con otro traje: **un
  freno que vive en un chat se muere al cerrar la sesión.** Los dos huecos se
  taparon escribiéndolos en el archivo **antes** de tocar la consola, no después:
  arreglar el guion mirando lo que ya pasó es escribir la crónica, no el guion.

### [L-027] 2026-08-07 — El ciego era el control, y un control ciego da permiso

- **Qué pasó:** midiendo la mitad de Caddy de `T-055`, la cadena real contestó lo
  que se quería oír — seis logins fallidos con seis orígenes falsos distintos y el
  freno saltando igual, contra el origen **real** (`172.17.0.4`).
- ✅ **Y se hizo lo correcto:** no creérselo. Antes de escribirlo se montó un
  control para **verlo fallar** — arrancar uvicorn **sin** `--proxy-headers`, que
  debería dejar a todo el mundo compartiendo el cubo de `127.0.0.1`.
- 🚨 **El control salió VERDE.** Mismo origen real, mismo resultado. Durante un
  minuto eso parecía tranquilizador: *"aguanta incluso sin las banderas"*.
- 🔑 **Y era lo contrario.** En **uvicorn 0.52.1 `--proxy-headers` ya viene puesta
  por defecto** — un dato que `[D-034]` tenía escrito desde el 2026-08-06 y que se
  olvidó justo al diseñar el control. **Quitar la bandera no apagaba nada.** El
  sabotaje no saboteaba: su verde no era una medida, era **silencio**.
- **El rojo de verdad** salió poniéndole a la bandera que sí manda un valor
  activamente equivocado — `--forwarded-allow-ips 203.0.113.5`, que excluye
  loopback. Entonces el log escribió `origen 127.0.0.1`, que es `[A-014]` en falso
  y a la vista. **Solo después la medida verde significó algo.**
- 🚨 **En qué se diferencia de `[L-020]`, y por qué es peor:**

  | | `[L-020]` | esta |
  |---|---|---|
  | quién estaba ciego | **el instrumento que medía** | **el control que autorizaba a creerse la medida** |
  | qué produce el fallo | una conclusión sin respaldo | **permiso para publicar la conclusión** |

  Un instrumento ciego da un dato flojo. Un **control** ciego da algo peor: da la
  sensación de haber hecho la comprobación. Es el sello de calidad falsificado.
- 🔧 **La regla que queda, y es concreta:** **un control se diseña contra el valor
  POR DEFECTO, no contra la bandera escrita.** Quitar una opción no la apaga si la
  librería ya la trae puesta. Para romper algo de verdad hay que darle un valor
  **activamente equivocado**, no ausente. Y antes de escribir el control:
  *¿sé cuál es el valor por defecto de lo que estoy quitando?*
- 📌 **Cuarta vez del mismo bicho en tres sesiones** — `[L-019]` (el montaje que
  medía lo contrario), `[L-020]` (el testigo que no miraba), `[L-021]` (el silencio
  leído como acusación) y esta. El patrón del proyecto ya no es "los tests
  mienten": es **verde producido por algo distinto de lo que el verde afirma**.

### [L-026] 2026-08-07 — `T-068` no es un freno: es disciplina, y la disciplina se gasta

- **Qué pasó:** al preparar el primer clic en la consola se releyó la lista de
  `T-068` —las siete puertas que cruzan al plan de pago sin vuelta atrás— y se
  cayó en algo que no estaba escrito en ninguna parte.
- 🚨 **`T-068` es el único control del proyecto ESTRUCTURALMENTE inverificable.**
  `LM.13` dice que un freno que no has visto morder es una nota, no un freno. Y
  este **no se puede ver morder nunca** — no por descuido ni por falta de tiempo:
  **probarlo ES el desastre.** Cruzar la puerta para comprobar que la puerta hace
  daño evapora los créditos y no tiene vuelta atrás.
- 🔑 **Eso no lo invalida. Lo convierte en OTRA COSA, y la diferencia importa:**

  | | freno | disciplina |
  |---|---|---|
  | ejemplo | el portero de `no_data_writes.py`, el tope de Caddy | `T-068` |
  | se ha visto morder | ✅ sí | ❌ imposible por construcción |
  | con la repetición | **no se degrada** — la máquina no se cansa | 🚨 **se degrada** |

- ⚠️ **Y el desgaste ya tiene fecha de inicio:** el experimento de `[A-018]`
  obliga a abrir *Facturación y costos* **a diario** durante semanas. Dentro de
  dos semanas esa página será rutina. **La rutina es exactamente lo que gasta la
  disciplina** — y es la misma página donde vive *"Actualizar plan"*.
- 🔑 **Lo que se hace con esto, y es lo único que se puede hacer:** no fingir que
  la lista es un freno, y **mover el riesgo de más tráfico fuera de la lista**.
  *"Actualizar plan"* deja de ser el renglón 8 de `[C-005]` y pasa a ser una línea
  del **protocolo de lectura** del experimento, donde sí se lee cada día. El
  detalle, en `[A-018]`.
- 📌 **La regla general que deja:** cuando un control no se puede verificar,
  **decirlo en voz alta y llamarlo por su nombre**. Un control inverificable
  etiquetado como "freno" da la misma calma que uno probado, y no la merece —
  es `[L-013]` con otro traje: **verde porque no existe nada capaz de ponerlo
  rojo.**

### [L-025] 2026-08-07 — Un dato que se toca obliga a salir a buscar sus copias

- **La regla, y ya no es una nota al pie:** en este proyecto, **cambiar un dato
  no termina cuando se cambia el dato**. Termina cuando se ha hecho `grep` de su
  nombre por todo el repo y se ha mirado qué dicen las otras apariciones. Un
  hecho vive repetido en documentos, comentarios, docstrings y anclas, y **la
  copia vieja no avisa: se queda ahí, afirmando lo contrario, con la misma cara
  de verdad que la buena**.

- 🚨 **Por qué merece nombre propio: es el defecto que más veces ha vuelto.**
  Recuento sin redondear, solo del 2026-08-07:

  | dónde | qué decía la copia muerta |
  |---|---|
  | `app/config.py`, docstring de `load_env_file` | *"en la nube no hay `.env`, los pone la plataforma"* — plataforma descartada en `[D-029]`, hace dos días |
  | `app/api.py:40-42` | **la misma frase**, en otro archivo |
  | `tests/test_deploy_limits.py:103,108` | apuntaban a `[A-019]` después de que `[A-019]` muriera |
  | `_persistence/decisions.md:271` | *"esto está leído, no medido"* — ya estaba medido |
  | `deploy/Caddyfile.template` | *"falta correr `caddy adapt`"* — ya se había corrido |

  Y antes del día de hoy: las cuatro menciones de `T-068` dándola por pendiente
  con la tarea cerrada, y los casos de las sesiones 33, 41 y 50.

- 🔑 **Lo que hace tan resistente al bicho, y es lo que hay que entender.** Las
  dos primeras filas son **comentarios dentro del código que corre**, y ahí el
  daño es distinto: un documento desactualizado se lee con desconfianza, pero un
  comentario pegado a la línea que ejecuta **se lee como la explicación
  autorizada de esa línea**. Nadie duda de él porque está al lado. Ese comentario
  llevaba dos días justificando `os.environ.setdefault` con un motivo que ya no
  existía — y la regla resultó ser correcta **por otra razón** (`[D-039]`). Un
  motivo falso sostiene bien hasta el día que alguien lo comprueba.

- ⚠️ **Y el arreglo genera el bicho.** Retirar `[A-019]` de `assumptions.md`
  —el gesto correcto, *"las suposiciones se mueren ascendiendo"*— dejó **cinco
  punteros apuntando a un ancla que ya no existe**. Limpiar es una operación que
  ensucia en otro sitio. 📌 Encadena con `[L-023]`: allí el instrumento ensuciaba
  lo que medía; aquí **la corrección ensucia lo que corrige**.

- 🔧 **Qué hacer, en concreto:** después de cambiar un hecho o de retirar una
  entrada, `grep` de su ancla y de las palabras clave de la frase por
  `_persistence/`, `_context/`, `deploy/`, `app/` y `tests/`. Y las que
  pertenezcan a otro dueño —`tasks.md` y `progress.md` son del `session-closer`—
  **se dejan escritas por número de línea**, no se arreglan a medias ni se
  olvidan.

### [L-024] 2026-08-07 — "Necesita la nube" era falso: un contenedor corre el guion de verdad

- **Qué se aprendió:** que `deploy/install.sh` —escrito el 2026-08-05 y **nunca
  corrido**, con `bash -n` como única verificación— **sí se puede correr hoy**, en
  un contenedor Ubuntu, sin EC2 y sin gastar un céntimo. Once tareas estaban
  clasificadas como "piden máquina". Al menos una no la pedía.

- 🚨 **El error no fue técnico, fue de censo.** Se dio "no hay nada que hacer sin
  nube" como conclusión, y era una **suposición sobre un conjunto** que nadie
  había recorrido. Encadena con `[L-021]`: el titular era más fuerte que la
  evidencia. Y llegó acompañado de un número inventado —"las once pendientes"
  cuando el `grep` propio ya había devuelto **catorce** filas—, que es el mismo
  defecto en pequeño: **poner una cifra redonda encima de la evidencia que ya
  estaba en pantalla**.

- 🔧 **El montaje, para repetirlo.** `git ls-files` en vez de copiar la carpeta:
  el repo local lleva un `.venv` y un `node_modules` **de Windows**, y con ellos
  dentro el guion habría visto un `.venv` ya existente, se habría saltado el paso
  de Python y habría medido otra cosa. ⚠️ `MSYS_NO_PATHCONV=1` o Git Bash
  convierte `/opt/teapp` en una ruta de Windows y el `docker exec` falla mudo.

- **Hasta dónde llega y dónde se para, medido:** el guion corrió entero —`apt-get`,
  Caddy 2.11.4, `venv`, `pip`, el `.env`— y murió en `systemctl: command not
  found` (línea 223). **La parte que importaba queda ANTES de ese punto.** Lo que
  el contenedor no puede medir: systemd, el cortafuegos, el certificado real y el
  disco que persiste a un reinicio. Esos siguen siendo de EC2.

#### 🔻 Ampliada el 2026-08-07 (noveno tramo) — se le cobró un trozo más al contenedor

- 🔑 **Aplicando la propia regla de esta lección a lo que la lección dejaba fuera:**
  si el guion muere en la 223, **la sección 5 entera no se ha ejecutado nunca** —ni
  aquí ni en EC2, que no existe—. Dentro está `caddy validate` (línea 237), y un
  error de sintaxis en `Caddyfile.template` se habría descubierto **mañana, en la
  máquina, con `install.sh` abortando a mitad de despliegue**.
- ✅ **Se ejecutó a mano, con el mismo `sed` de la 232. Primera vez en la vida del
  proyecto:** `Valid configuration`, salida **0**, sin `DOMAIN_PLACEHOLDER` sin
  sustituir. Directivas efectivas: `request_body { max_size 16KB }` y
  `reverse_proxy 127.0.0.1:8000`. El validador confirmó de paso *"enabling
  automatic HTTP->HTTPS redirects"* y el 443 con política TLS.
- ⚠️ **Mide la SINTAXIS, no el comportamiento.** Que la configuración sea válida no
  dice que Caddy escriba `X-Forwarded-For` ni que el 413 llegue: eso es `T-055` y
  `T-060b`, y siguen necesitando la máquina.
- 📌 **Y se cayó de paso una suposición sobre el propio contenedor:** *"ahí dentro
  hay un aparejo de Caddy hablando con uvicorn"*. **No lo hay.** Su
  `/etc/caddy/Caddyfile` es **el de fábrica**, con `reverse_proxy` comentado —
  porque la sección 5 nunca corrió. Son **dos procesos sueltos** levantados a mano
  para medir el tope de 16 KB, no un aparejo. 🔑 Casi se le pide a ese contenedor
  una medición que no podía dar, y **habría contestado algo**.
- 🔑 **La receta del contenedor vivía solo en el scrollback de una terminal, y eso
  es lo único irrecuperable de todo esto.** Ya está escrita en `deploy/README.md`:
  `docker run -d --name teapp-test ubuntu:24.04 sleep infinity`, sin puertos y sin
  volúmenes, todo por `docker exec ... sh -c '...'`. **El contenedor es desechable;
  la receta no.**

- 🔑 **Lo que deja como regla:** *"necesita la nube"* casi nunca es cierto de la
  **tarea entera**. Es cierto de una parte, y la otra suele ser medible hoy. Es el
  mismo corte de `T-054` y `T-055` —la mitad medible y la que espera— aplicado
  esta vez al guion de despliegue completo. **Antes de escribir "bloqueada",
  preguntarse qué mitad no lo está.**

- 📌 **Y el atajo que se descartó:** se propuso un test que leyera el **texto** de
  `install.sh` y comprobara que unas líneas siguen dentro de un `if`. Habría sido
  ruidoso (rojo al renombrar una variable) y ciego donde duele (verde al cambiar
  `-f` por `-e`). 🔑 Es el material de `[L-023]`: un control que mide **la forma
  del código** en vez del comportamiento. Se descartó **porque existía la vía que
  mide de verdad**, no por gusto.

### [L-023] 2026-08-06 — El instrumento que mide puede ensuciar lo que mide

- **Qué pasó:** `[A-020]` denunciaba un camino desconocido que escribía en `data/`
  real: el 2026-08-06 a las 14:48:33 aparecieron `data/users/otronombrelargo.json`
  (`{"score": 5}`) y `data/quota/otronombrelargo.json` (`{"used": 5}`) de una
  cuenta que no existía en `data/accounts.json`. `T-072` lo resolvió. El culpable
  fue **`measure_body.py`, la báscula de `T-054`** — la propia medición del peor
  caso de bytes, escrita y ejecutada esa misma tarde.

- **La cadena, con relojes** (19:48 UTC = 14:48 local):

  | reloj | qué |
  |---|---|
  | 19:48:17.409 UTC | se escribe `measure_body.py` |
  | 19:48:32.094 UTC | se ejecuta desde la raíz de TEAPP |
  | 19:48:33.051 local | nacen los dos archivos en `data/` |
  | 19:48:33.182 UTC | la báscula imprime su tabla |

  El script termina registrando a `otronombrelargo` y recorriendo `CASES`, que
  tiene **cinco** elementos: cinco `/practice`, `{"score": 5}` y `{"used": 5}`.
  Cuadra exacto.

- **Por qué pasó — y es de manual.** La báscula **sí se acordó de desviar**. Tenía
  su línea, con comentario y todo: `accounts.ACCOUNTS_FILE = Path(_tmp) /
  "accounts.json"`, *"medir no debe tocar `data/`"*. Lo que no desvió fue
  `USERS_DIR` ni `QUOTA_DIR`. 🔑 **El aislamiento necesitaba tres desvíos y se
  acordó de uno.**

- 🔑 **Y ahí estaba la contradicción de `[A-020]`, explicada.** `otronombrelargo`
  no aparecía en `data/accounts.json` **porque `accounts.json` fue el único que sí
  se desvió**: la cuenta se creó en el temporal, el marcador y la cuota se fueron
  a los datos de verdad. La ausencia no probaba lo que parecía probar.

- ⚠️ **Y por eso mismo, una corrección al análisis que la investigó.** Ese
  análisis dedujo de la cuenta ausente que *"`/practice` nunca comprueba que la
  cuenta exista, y un script que se firme su propia cookie entra sin
  registrarse"*, y lo llamó *"la pista principal"*. **La pista apuntaba al desvío
  incompleto, no a la puerta**: el script se registró. 📌 Es `[L-021]` otra vez —
  un titular fuerte apoyado en una prueba que significaba otra cosa. La lectura
  del código (`app/api.py:554` → `_current_user`) valía por su cuenta y **se
  verificó aparte**: ver `[A-021]`.

- **No es un accidente, es un patrón.** `probe-log.json`, el otro huérfano de
  `data/users/`, sale del 2026-08-05 — otra sesión, otro día, la misma clase de
  script.

- **Qué se hace distinto:**
  1. 🚨 **Un script de medición que importe `app` desvía los TRES sitios**:
     `accounts.ACCOUNTS_FILE`, `tools.USERS_DIR` y `quota.QUOTA_DIR`. Acordarse de
     uno no es acordarse.
  2. **Y toma la huella de `data/` real antes y después**, con
     `tests/no_data_writes.py`, que ya sirve fuera de pytest. Un desvío que hay que
     recordar falla el día que se olvida; el portero delante lo caza igual.
  3. 🔑 **La regla de fondo, que es más grande que la tarea:** el acto de medir es
     código que corre, y corre **fuera** de la suite. El portero de `T-071` vive
     dentro de pytest y **no lo verá nunca**. Encadena con `[L-020]` —un
     instrumento ciego da silencio— y `[L-022]` —un `md5` dice "los bytes,
     iguales"—: esta añade que el instrumento no solo puede no ver, **puede
     ensuciar lo que mide**.
  4. ⚠️ **Y por eso importa antes de la nube:** en el servidor esa carpeta tiene
     fichas de personas de verdad, y una báscula que se acuerde de dos desvíos de
     tres las escribe sin que nadie proteste.

- 📌 **El rastro estaba en las transcripciones de la otra terminal, no en el
  historial de PowerShell** — ese archivo no se tocó desde las 07:51, así que lo
  de las 14:48 no lo tecleó nadie a mano. Vale como método para la próxima.

### [L-022] 2026-08-06 — Un `md5` no dice "todo igual", dice "los bytes, iguales"

- **Qué pasó:** para demostrar que el portero de `T-071` muerde, se quitó a
  propósito la línea del `conftest.py`. Como el sabotaje escribe en `data/` de
  verdad, se hizo copia antes y se restauró después con
  `rm -rf data && cp -r copia data`. La verificación fue huella `md5` de los
  siete archivos: idénticas antes y después. **Restauración correcta, y ningún
  dato de la aplicación se perdió.**
- **Lo que sí se destruyó:** las **fechas de modificación**. Los siete archivos
  quedaron con el mismo segundo, el de la copia de vuelta. Con ellas se fue la
  prueba física del camino de `[A-020]`, y en particular la más fuerte de todas:
  que `data/users/otronombrelargo.json` y `data/quota/otronombrelargo.json`
  llevaban **el mismo nanosegundo**, que era el argumento de que fue una petición
  a `/practice` y no alguien tocando archivos a mano.
- **Por qué pasó:** `md5` es del contenido. Es ciego al `mtime` **por
  construcción**, no por accidente. Era el instrumento correcto para *"¿se
  corrompió un dato?"* y no podía contestar *"¿se perdió la prueba?"*. Nadie hizo
  la segunda pregunta.
- 🔑 **La vuelta nueva sobre `[L-020]` y `[L-021]`:** los tres casos anteriores
  eran instrumentos **ciegos a un cambio** — `git status` sobre una carpeta
  ignorada, un test escrito contra el número equivocado. Este **vio** el cambio
  que le importaba, y fue ciego a **una dimensión entera del archivo**. Un
  archivo es contenido *y* metadatos. La frase "las huellas coinciden" suena a
  "todo igual" y significa "los bytes, iguales".
- ⚠️ **Y estrenó `[L-021]` el mismo día en que se escribió**, dentro de la
  verificación del portero que se construyó justo contra ese defecto. El titular
  *"restaurada y verificada con las mismas siete huellas"* era cierto y decía más
  de lo que la medida sostenía.
- **Qué se hace distinto, dos reglas:**
  1. 🚨 **La prueba de un defecto no puede vivir en la carpeta que el defecto
     ensucia.** Se copia a `_persistence/` —que sí va a Git— **antes** de tocar
     nada. Es lo mismo que hizo falso el `git status` de `[L-020]`, un día
     después y en la otra dirección.
  2. **Antes de restaurar por copia, preguntarse qué del original no viaja en los
     bytes:** fechas, permisos, orden, enlaces. `cp -r` no es una máquina del
     tiempo, es un duplicador de contenido.
- 📌 Consecuencia para el portero, ya escrita en su docstring: **compara
  contenido, así que un camino que reescriba un archivo con los mismos bytes le
  pasa invisible.** Hoy no importa —sumar un punto siempre cambia el número—
  pero es de la misma clase que "vive dentro de pytest" y va escrito al lado.

### [L-021] 2026-08-06 — El titular que contradice su propia salvedad

- **Qué pasó:** al analizar `T-071` se encontraron cinco marcadores en
  `data/users/` con nombres que olían a test (`otronombrelargo`, `probe-log`,
  `juan` con 13 puntos). El punto se tituló **"la trampa ya se disparó"**, y tres
  líneas más abajo el mismo texto decía *"te lo doy como sospecha fuerte, no como
  hecho medido"*. Las dos frases no pueden ser ciertas a la vez.
- **Por qué pasó:** `data/` no va a Git, así que no hay historial que consultar.
  De esa ausencia se sacó una conclusión — y encima la más llamativa. Es
  `[L-020]` con el signo cambiado: allí el silencio de `git status` se leyó como
  *"todo bien"*; aquí el silencio del historial se leyó como *"ya pasó"*.
  🔑 **La ausencia de dato no es evidencia en ninguna de las dos direcciones.**
- **Lo que dijo la medida**, hecha después: huella `md5` + fecha de los cinco
  marcadores → suite entera (328 verdes) → huella **idéntica**. La suite de hoy
  no escribe en `data/`. Y por otro camino: `conftest.py` desvía la cuota, así
  que una corrida normal de pytest **no puede** escribir en `data/quota/` —
  luego lo del 14:48 no fue pytest. La trampa estaba **armada**, no disparada.
- ⚠️ **Una salvedad correcta no arregla un titular falso.** La salvedad estaba
  bien escrita y no sirvió de nada: nadie recuerda la letra pequeña de un
  epígrafe en negrita. Si la salvedad y el titular discrepan, **el que se
  cambia es el titular**, no al revés.
- **Qué se hace distinto:** un titular afirma lo que se midió. Si hace falta una
  salvedad para que el titular sea honesto, el titular está mal escrito. Y lo
  que se sospecha se titula como sospecha — "hay marcadores sin explicar",
  no "la trampa ya se disparó".

### [L-020] 2026-08-06 — El testigo ciego, y el animal que ya tiene nombre

- **Qué pasó:** al cerrar `T-054` se escribió *"verifiqué con `git status` que
  `data/` quedó intacto"*. **`data/` está en `.gitignore`, línea 18.** `git
  status` no la mira y no la puede mirar: habría dicho exactamente lo mismo si
  los tests hubieran escrito dentro.
- ⚠️ **El testigo no se equivocó — no estaba mirando.** Y esa diferencia importa:
  un instrumento equivocado da un dato falso, que se puede contradecir. Un
  instrumento ciego da **silencio**, y el silencio se lee como confirmación. Es
  `[L-016]` otra vez ("el silencio de una fuente no es un dato"), pero aplicado a
  una herramienta en vez de a una documentación.
- **La conclusión era correcta**, y se comprobó después por el camino que sí ve:
  las fechas de `data/users/*.json`. El más nuevo era de las 14:48, la corrida de
  la suite fue a las ~20:00. El `fixture` funciona. 🔑 **Pero se supo por suerte,
  no por la prueba que se citó.**
- **La regla que queda:** antes de citar una prueba, preguntar **si el
  instrumento puede ver el fallo que se está descartando**. Aquí bastaba con
  saber que la carpeta está ignorada — y está escrito en `.gitignore`, que es un
  archivo de este repo.
- 📌 **Los instrumentos que sí ven `data/`**, para la próxima vez:
  - `git check-ignore -v data/…` → contesta **por qué** está ignorada, con
    archivo y línea. Es el que convierte "creo que git no la mira" en un dato.
  - `git status --porcelain --ignored` → lista también lo ignorado.
  - las **fechas de modificación** de los archivos, que es lo que se usó aquí.
  ⚠️ Ninguno de los tres es más difícil que el que se citó. **No falló el
  esfuerzo: falló no preguntarse qué mira cada herramienta.**

#### 🚨 Y esto ya no es un caso suelto: es EL modo de fallo de este proyecto

**Un verde producido por algo distinto de lo que el verde afirma.** Tres veces en
dos sesiones, y cada vez con una cara nueva:

| dónde | el verde decía | lo que de verdad lo producía |
|---|---|---|
| `[L-019]` | "uvicorn ignora al suplantador" | la petición entraba **como Caddy**, por `127.0.0.1` |
| `[D-035]` | "cabe bajo el tope de Caddy" | se habría medido contra **16384**, y Caddy corta en 16000 |
| aquí | "los tests no tocaron `data/`" | `git status` **no mira** `data/` |

Y más atrás está el mismo animal: `[L-017]` (un `is-active` que declaraba
"funcionando"), `[L-015]` (un fixture que creía limpiar), `[L-012]` (un
`at_level` que pintaba de verde un renglón inexistente), `[L-011]` (un control
que parcheaba un nombre distinto del que se usaba).

🔑 **Ninguno de estos se descubre mirando el verde: solo se descubren
preguntando qué lo produce.** De ahí sale el hábito que ya es de la casa —
sabotear el montaje además del resultado (`[L-019]`)— y su ampliación de hoy:
**sabotear también en la dirección para la que el control se escribió.** Los
cuatro sabotajes de `[D-035]` atacaban el instrumento; el que faltaba —subir
`MAX_SENTENCE_LENGTH` a 5000— era el único que atacaba el escenario que el test
decía existir para cazar. Lo aportó la auditoría, no quien escribió el test.

### [L-019] 2026-08-06 — El sabotaje llegaba disfrazado de aquello que quería atacar

- **Qué pasó:** para medir `[A-014]` se montaron cuatro escenarios contra un
  uvicorn de verdad. El cuarto era el importante: fingir ser **alguien que no es
  Caddy** mandando un `X-Forwarded-For` inventado, para ver que uvicorn lo
  ignoraba. Se hizo hablándole por `127.0.0.2`, dando por supuesto que esa
  dirección no estaría en la lista de confianza. Salió **rojo**: uvicorn se creyó
  la cabecera.
- **Por qué pasó:** el rojo no era de uvicorn, era del montaje. Windows usa
  **`127.0.0.1` como dirección de origen** aunque el destino sea `127.0.0.2`
  (medido aparte, con dos sockets). Así que la petición llegaba desde la
  dirección de confianza: el escenario que decía *"esto lo manda un extraño"*
  entraba **por la puerta de Caddy**. Medía lo contrario de lo que anunciaba.
- 🔑 **Lo que lo hace grave es la simetría.** Aquí el error se delató porque el
  resultado salió rojo y el rojo pedía explicación. Pero el mismo montaje
  equivocado, aplicado a cualquiera de los otros tres escenarios, habría salido
  **verde por la razón falsa** — y `T-055` se habría dado por cerrada sobre una
  medición que no midió nada. Es `[L-007]` otra vez, con el signo cambiado: allí
  el control medía de más, aquí el escenario mentía sobre desde dónde llamaba.
- **Qué se hace distinto:** de un sabotaje se verifica **el montaje, no solo el
  resultado**. Antes de creerse el veredicto, comprobar por separado que la
  condición que el escenario dice reproducir se está reproduciendo de verdad —
  aquí, preguntarle al sistema qué dirección de origen ve, en vez de deducirla
  del destino al que se marcó.

### [L-018] 2026-08-06 — Los datos se replican solos, y corregir uno no corrige los demás

- **Qué pasó:** una frase falsa —*"si no llega correo, la alarma está bien
  montada"*— se corrigió al encontrarla. Al ir a buscarla en serio, estaba en
  **cinco** sitios: la entrada `[S-019]`, su fila de índice y el "Estado actual"
  de `progress.md`; dos puntos distintos de `[A-018]`; y un párrafo de
  `deploy/console_steps.md`. Corregir el primero habría dejado cuatro mintiendo.
- 🚨 **Y es la tercera vez con el mismo bicho:** sesión 33 (el repo dado por
  "privado"), sesión 41 (lo mismo otra vez), y esta. **Tres veces deja de ser
  casualidad y pasa a ser una propiedad del proyecto.**
- 🔑 **Por qué pasa aquí y no es descuido:** el formato de `_persistence/`
  **obliga a duplicar por diseño** — cada hecho vive en la entrada *y* en su fila
  de índice, porque el índice existe para no leer el archivo entero. Y `deploy/`
  vuelve a contar lo mismo en clave operativa, porque quien está en la consola no
  va a abrir `assumptions.md`. La redundancia es útil; **el precio es que un error
  nace multiplicado.**
- ✅ **La regla que queda:** al corregir un hecho, **no se edita donde se
  encontró: se va a buscar dónde más vive.** Un `grep` de la frase antes de dar
  la corrección por hecha.
- ⚠️ **Y la asimetría que lo hace peligroso:** escribir en dos sitios cuesta el
  doble, pero **corregir en uno solo cuesta cero y parece terminado.** Por eso el
  fallo no se siente como fallo mientras se comete.
- 📌 **Corolario aplicado el mismo día:** la tabla de lectura del experimento de
  `[A-018]` se escribió **en un solo sitio**, y `console_steps.md` la referencia
  en vez de copiarla. Documentar el problema de las copias haciendo una copia
  habría sido la sexta.

### [L-017] 2026-08-05 — El comentario correcto que sirvió de coartada

- **Qué pasó:** el bloque de comprobación final de `deploy/install.sh` llevaba
  escrito, textualmente, *"PI-4: terminado = visto funcionando. Un guion que
  acaba sin error no demuestra que la app conteste — solo que el guion acabó."*
  Y lo único que hacía dos líneas más abajo era `systemctl is-active` de los dos
  servicios.
- **Por qué eso no comprueba lo que dice:** `is-active` demuestra que **systemd
  lanzó el proceso**, no que la app conteste. Y el hueco es alcanzable, no
  teórico:

      uvicorn arranca → medio segundo después `require_secret` revienta porque
      `ubuntu` no puede leer el `.env` → `Restart=always` lo relanza → y
      `systemctl restart` ya había vuelto, así que `is-active` lo ve `active`

  El guion habría impreso **"Listo. TEAPP corriendo en https://..."** sobre una
  app muerta. Una afirmación que nunca se comprobó.
- 🔑 **Lo que hay que llevarse, y es lo incómodo:** el comentario **no evitó** el
  fallo — **lo escondió.** Un bloque que se declara a sí mismo auditado es un
  bloque que nadie vuelve a auditar. Saber enunciar el principio y cumplirlo son
  dos habilidades distintas, y la primera **disfraza** la ausencia de la segunda.
- 📌 **Y es la misma familia de la sesión de `[L-006]`**, donde el cierre se
  cumplió entero y el trabajo se quedó sin subir: el procedimiento se recitó
  completo y el resultado no se miró. Aquí, otra vez: **el principio citado, el
  efecto sin medir.**
- **Cómo se arregló:** tres comprobaciones en vez de una, porque prueban cosas
  distintas — `is-active` (systemd lo lanzó), `curl` a `127.0.0.1:8000` (la app
  contesta) y `curl` al dominio (se llega desde fuera, con certificado). Y el
  mensaje final cambió de *"Listo, TEAPP corriendo en…"* a **"Comprobado: TEAPP
  contesta en…"**. 🔑 **Ese cambio de verbo es el arreglo de verdad; los `curl`
  son solo cómo se consigue.**
- ⚠️ **La regla práctica que deja:** cuando un comentario prometa que algo está
  comprobado, **leer lo de debajo con MÁS desconfianza, no con menos.** Es donde
  menos ojos van a mirar.
- 🔑 **Y el arreglo trajo la misma criatura con el signo cambiado**, que es lo
  que convierte esto en una lección general y no en una anécdota. Al añadir los
  dos `curl` se le dieron **10 reintentos al que tarda segundos** (arrancar
  uvicorn) y **ninguno al que tarda minutos** (que Let's Encrypt emita el
  certificado). El primero decía verde sin haber mirado; el segundo habría dicho
  **rojo por haber mirado demasiado pronto**.

  > 🚨 **Las dos veces el control no medía lo que su nombre promete.** Un falso
  > verde y un falso rojo no son errores opuestos: son el mismo error —no haber
  > pensado *cuándo* es válido preguntar— y por eso el segundo se coló mientras
  > se arreglaba el primero.

- 📌 **Y un tercer filo del mismo cuchillo, en el mismo bloque:** la ruta del
  `curl` es `/` **porque entrega `index.html` sin pedir sesión**. Apuntarlo a
  `/me` —que suena más representativo— daría 401, `curl -f` lo tomaría por
  fallo, y **cada instalación se pararía en rojo estando todo bien**. Quedó
  escrito en el guion para que nadie lo "mejore": un control que se pone rojo
  por el motivo equivocado es un control verde disfrazado.

### [L-016] 2026-08-05 — El mismo error dos veces, un piso más abajo cada vez

> 🔑 **Las dos mitades van juntas a propósito.** No son dos lecciones parecidas:
> es la misma, y la segunda se cometió **corrigiendo la primera**. Separarlas
> escondería justo lo que hay que ver.

**Primera mitad — la lista supuesta tenía tres de siete**

- **Qué pasó:** `[C-005]` nació con tres puertas al plan de pago —Organization,
  Control Tower, Partner Network— y una nota al margen que decía *"la FAQ
  menciona algún caso más"*. Al leer las fuentes enteras aparecieron **siete**.
  Las cuatro que faltaban: contrato de **Professional Services**, **Enterprise
  Agreement**, suscripción **Skill Builder Team**, y marcar la cuenta **HIPAA o
  SEC compliant**.
- 🔑 **Por qué se coló:** las tres conocidas formaban una familia coherente
  —"cosas de empresa grande organizando cuentas"— y esa coherencia se leyó como
  completitud. **Una lista que tiene sentido parece terminada.** Las que faltaban
  venían de familias distintas (formación, cumplimiento normativo) y por eso no
  se echaban de menos: **para notar que falta algo hay que haberlo imaginado.**
- 🚨 **El aviso estaba escrito.** La propia entrada decía *"menciona algún caso
  más"* y aun así se siguió adelante — familia de `[L-012]`, donde el límite
  también estaba anotado antes de cruzarlo. **Una nota que dice "puede que falte
  algo" es una tarea, no un descargo de responsabilidad.**
- **Qué lo salvó:** que la mitad floja se escribiera **aparte**, como `[A-016]`,
  en vez de enterrada dentro de `[C-005]`. Una suposición con nombre propio se
  puede poner como bloqueante de una tarea; una frase en medio de un párrafo, no.
  Es `[L-014]` desde el otro lado.

**Segunda mitad — y al corregirla se cayó en lo mismo**

- **Qué pasó:** con las siete puertas ya verificadas, se escribió que las dos
  primeras evaporan los créditos **y las otras cinco los conservan**. La
  documentación **no dice eso**. Solo se moja con las dos primeras; de las cinco
  restantes no dice ni que se salvan ni que se pierden. La frase de "los créditos
  se aplican a facturas futuras" existe, pero es del **upgrade manual**, y se le
  pegó al caso equivocado.
- 🔑 **Por qué se coló, que es la primera mitad un piso más abajo:** **un
  documento que no dice "no" parece que dice "sí".** El silencio de una fuente se
  leyó como respuesta favorable — y encima la favorable, que es la que menos se
  audita. 🚨 **El silencio de una fuente no es un dato. Es un silencio.**
- 📌 **Y una trampa de método que venía dentro:** se escribió *"las tres fuentes
  repiten la misma frase"*. Cierto **para la lista de siete**; falso para los
  créditos — los Términos, que son la fuente que manda porque es la que se firma,
  solo hablan de Organizations, ni mencionan Control Tower, y con palabras
  peores. **Tres fuentes que coinciden en el párrafo A no coinciden
  automáticamente en el párrafo B: la coincidencia se verifica por afirmación,
  no por documento.**
- **Cómo se arregló:** las cinco desconocidas se marcan ❓ y **se tratan como si
  evaporaran**. Es `PERMISOS.get(nombre, "prohibir")` aplicado a una fuente en
  vez de a un usuario: sin dato, se asume lo caro, para que el olvido falle hacia
  el lado seguro.

**Lo común, que es lo que hay que llevarse**

- 🔑 **Las dos veces el hecho no salió del texto: salió de la FORMA del texto.**
  De que la lista *pareciera* cerrada, y de que el silencio *pareciera*
  permiso. Ninguna de las dos cosas estaba escrita en ningún sitio.
- **El coste de las dos:** unas lecturas y una corrección. Comparado con lo que
  protegían —la única ventana de 6 meses de `[C-006]`, que no se repite— barato
  hasta el ridículo.

### [L-015] 2026-08-04 — El fixture que creía limpiar y no limpiaba

- **Qué pasó:** `T-033` configura el log, y hacía falta un test que midiera eso
  **sin usar `caplog`** — porque `caplog` es justo la herramienta que miente
  sobre esta pregunta ([L-012]). Se escribió un fixture que vaciaba los handlers
  del logger raíz para dejarlo como en un servidor recién arrancado. Tres de los
  cinco tests salieron rojos con un mensaje revelador: los handlers **estaban
  ahí otra vez**, y eran `LogCaptureHandler`.
- **Por qué pasó:** pytest instala el handler de `caplog` **alrededor de la fase
  de ejecución del test**, o sea **después** de que corran los fixtures. El
  fixture vaciaba, pytest volvía a llenar, y para cuando corría el cuerpo del
  test el raíz tenía handlers otra vez. Y `logging.basicConfig` **no hace nada si
  el raíz ya tiene handlers**: la función que se quería medir se salía por la
  primera línea sin hacer nada.
- 🚨 **Lo que lo hace grave no es el fallo, es dónde estaba.** Ese test era el
  arreglo de [L-012] — el test cuyo trabajo era impedir que un renglón se
  aprobara a sí mismo. Y reproducía el mismo defecto: **medía el estado que había
  puesto el framework y lo llamaba "lo que hace `configure_logging`"**.
  > Si el fixture hubiera "funcionado" en silencio, habría quedado un test verde
  > vigilando exactamente nada, en el sitio donde más falta hacía uno de verdad.
- 🔑 **Por qué se vio a tiempo, y esto es lo que hay que repetir:** porque el test
  se puso rojo **por su cuenta**, no porque alguien sospechara. Al lado del test
  del estado bueno se escribió el del estado malo —*sin configurar, `info` no
  pasa*—, y ese par es lo que delata a un fixture que no hace su trabajo. Un test
  que solo mira el estado bueno no distingue *"lo arreglé"* de *"esto ya estaba
  así"*.
- **Cómo se arregló:** midiendo en **otro proceso**. Un intérprete recién
  arrancado es la única condición honesta, porque es exactamente la de uvicorn:
  raíz limpia, nada configurado, nadie escuchando. `subprocess.run` con
  `sys.executable`, sin red, sin instalar nada — [C-001] sigue en pie.
- **Qué se hace distinto:** cuando un test necesite **quitar** algo que el
  framework pone, no basta con quitarlo en un fixture: hay que comprobar que
  sigue quitado **dentro del cuerpo del test**. Y si el framework lo repone,
  medir fuera del framework.
  🔑 La regla corta: **cuando lo que quieres medir es "cómo arranca esto de
  cero", arráncalo de cero.**

### [L-014] 2026-08-04 — Una suposición que dice qué la mata se muere sola cuando toca

- **Qué pasó:** al terminar `T-053`, `[A-012]` —*"nadie prueba contraseñas a la
  fuerza contra `/login`"*— dejó de ser cierta y de ser necesaria a la vez.
  Retirarla no costó ninguna discusión: la propia entrada decía **de qué dependía
  y qué la mataría**, así que solo hubo que mirar si eso ya había pasado.
- **Por qué pasó:** porque estaba escrita con fecha de caducidad **atada a un
  hecho concreto** —*"el día que la app tenga una URL pública"*, *"hoy no hay
  tope de intentos"*— y no a un vago "más adelante". 🔑 **Una suposición con
  condición de cierre se comprueba; una sin ella se opina**, y lo que se opina no
  se retira nunca: se queda ahí envejeciendo y mintiendo.
- **La otra mitad, que no se esperaba:** al ir a retirarla se vio que `A-012` no
  era **una** suposición sino **dos pegadas**, y que solo una se había resuelto.
  - Lo que `T-053` resolvió: que no hubiera freno. Eso ya no se supone.
  - Lo que quedó vivo: que **los números del freno sean los correctos**
    (`[A-013]`), y que **el origen que lee el servidor sea el origen real**
    (`[A-014]`). Lo segundo caduca el mismo día que caducaba `A-012`.
  - 🚨 Y `[D-026]` **no** las sustituye. Una decisión guarda lo que se eligió y
    por qué; una suposición guarda **lo que se está dando por cierto sin
    comprobar**. Meter lo segundo dentro de lo primero lo esconde: `decisions.md`
    no es la lista que uno repasa buscando qué puede estar mal.
- **Qué se hace distinto:** al escribir una suposición, decir **qué hecho
  concreto la mata**. Y al retirarla, no darla por muerta entera: preguntar qué
  parte se resolvió y qué parte solo cambió de nombre. Lo que sigue sin
  comprobarse se queda en `assumptions.md`, aunque la entrada vieja se vaya.

### [L-013] 2026-08-04 — Cerrar un hueco no cierra los demás

- **Qué pasó:** los frenos del paso 6 se escribieron con mucho cuidado puesto en
  **un** hueco: el que hay entre leer el contador y escribirlo. Ese se cerró con
  candado, se probó con 50 hilos y se demostró que sin candado se rompía.
  Con 247 tests en verde, dos sabotajes encontraron **otros cuatro huecos** —y
  ninguno se parecía al primero.
- 🔑 **La lección, y es la que vale para lo que venga:** un hueco cerrado
  entrena la vista para ese hueco, no para los demás. Los otros cuatro no se
  vieron **porque no tenían la forma del que ya conocía**.

  | hueco | entre qué y qué | qué costaba |
  |---|---|---|
  | el conocido | leer el contador y escribirlo | prácticas gratis, ya cerrado |
  | 1 | preguntar el día y volver a preguntarlo | cuota regalada en la medianoche |
  | 2 | encolar el trabajo y empezarlo | cobrar por trabajo que nadie empezó |
  | 3 | contestar el 504 y terminar el trabajo | el marcador sube sin nadie mirando |
  | 4 | acabar un test y acabar sus hilos | un test contó puntos de otro |

- **Hueco 1 — la medianoche.** `spend` preguntaba **dos veces** qué día era: una
  para sí y otra dentro de `read_usage`. Entre las dos cabe la medianoche.
  Cuando cabía, comprobaba contra el día **nuevo** —limpio, así que pasaba— y
  escribía bajo el día **viejo**, borrando lo gastado. Cuota gratis, una vez al
  día, y precisamente a quien esté practicando a esa hora.
  🔑 **El comentario del código defendía justo lo contrario de lo que el código
  hacía.** Arreglado preguntando el día UNA vez y pasándolo hacia dentro.
- **Hueco 2 — la cola.** `result(timeout=)` cuenta desde que se **llama**, no
  desde que la tarea **arranca**. Con el pool lleno, el tiempo de cola se le
  cobraba a quien esperaba en ella. Medido: 23 peticiones a la vez contra un
  pool de 20 → 20 llegaron al tutor y **3 pagaron un 504 por nada**.
  ⚠️ Y el pool no tenía tamaño escrito: `ThreadPoolExecutor()` lo saca de las
  CPUs de la máquina —20 aquí, otro en la nube—. **Un freno cuyo tamaño depende
  de dónde corra no se puede razonar.** Ahora el tamaño está escrito (40) y
  `future.cancel()` distingue lo que empezó de lo que no: lo que no empezó se
  devuelve.
  🔑 Eso no contradice *"se cobra el intento"*: **lo completa**. Se cobra por
  intentar porque intentar cuesta; una petición que nunca salió de la cola no
  intentó nada.
- **Hueco 3 — después del 504.** El tutor sigue corriendo y acaba llamando a
  `add_point`: el marcador sube cuando quien preguntó ya se fue con un error.
  **Se decidió dejarlo** —el marcador cuenta frases practicadas ([A-001]), y esa
  se practicó— pero lo que cambia es que ahora está **escrito y con test**, no
  descubriéndose el día que alguien pregunte por qué le subió el número.
- **Hueco 4 — el que apareció al arreglar los otros.** El test del hueco 3 falló
  con `['juan', 'juan']`: dos puntos donde solo hubo una práctica. Eran hilos
  colgados de tests anteriores despertando **dentro** de este y llamando a su
  `add_point`. 🔑 Es la limitación del propio freno —un hilo no se puede matar—
  mordiendo dentro de la suite. Arreglado dándole a cada test lento su propio
  pool y esperándolo con `shutdown(wait=True)`.
- **Y lo que enseña sobre el verde:** los 247 tests no vieron ninguno de los
  cuatro, y no por descuido — cada uno probaba bien lo que decía probar. Es
  [L-003] otra vez, con más tests: **el verde mide lo que se te ocurrió
  preguntar.** Lo que no se te ocurrió no sale rojo, sale ausente.
- 🔑 **El remate, y es media lección más: se arregló el número y quedó heredada
  la RAZÓN del número.** Escribir `TUTOR_POOL_SIZE = 40` quitó la dependencia de
  las CPUs de la máquina. Pero el 40 solo es correcto porque el limitador de
  hilos de `anyio` —el que usa FastAPI para las rutas `def`— trae 40 fichas por
  defecto. Y `anyio` **ni siquiera está fijado**: entra de rebote con `fastapi`.
  Una subida de FastAPI podía romper el invariante *"la cola nunca es el cuello
  de botella"* **sin que nadie tocara una línea de este proyecto**, y con él
  volvía el cobro por espera del hueco 2.
  Cerrado con un test que compara los dos números, medido en los dos sentidos:
  verde con `anyio` en 40, rojo simulándolo en 15.
  > **Un invariante que depende del valor por defecto de otro necesita quien lo
  > vigile, no un comentario que lo explique.**
  Es [D-022] otra vez —un vigía sin quien lo vigile no demuestra nada— aplicado
  a una suposición prestada en vez de a un portero.

### [L-012] 2026-08-04 — El límite estaba escrito, y aun así se cruzó

- **Qué pasó:** el cuarto freno del paso 6 es *"registrar por qué se frenó"*. Se
  escribió `logger.info("Cuota agotada: ...")` en `app/api.py`, y su test pasó.
  Con uvicorn de verdad: **20 frenazos seguidos y cero líneas en el log.**
- **Por qué:** nadie ha configurado el log todavía ([T-033]), así que actúa el
  handler de último recurso de Python, **que empieza en WARNING**. Se midió:
  `logger.getEffectiveLevel()` devuelve `WARNING`, y `isEnabledFor(INFO)`
  devuelve `False`. Un `info` no se pierde por poco: no existe.
- 🔑 **Lo primero, y es lo incómodo: esto ya estaba escrito.** `[A-003]` lo decía
  con estas palabras desde el 2 de agosto — *"Solo sale WARNING o peor. Un
  `logger.info(...)` se pierde en silencio."* No fue un límite desconocido. Fue
  un límite **conocido, anotado, y cruzado igual**.
  ⚠️ [L-011] cerraba con *"un límite sabido y no escrito es un límite que alguien
  va a cruzar"*. Esta lección es la corrección de aquella: **escribirlo no
  basta.** Un límite que solo vive en un `.md` no frena a nadie en el momento de
  teclear. Lo único que lo frena es algo que se ponga rojo.
- 🔑 **Lo segundo, que es lo que enseña de verdad: el test tapó el agujero
  activamente.** `caplog.at_level(logging.INFO)` **baja el listón del logger para
  ese test**. O sea que el test creaba las condiciones que hacían visible el
  renglón, y luego comprobaba que era visible. Se aprobaba a sí mismo.
  > No medía *"¿se ve esto?"*. Medía *"¿se vería esto si el log estuviera
  > configurado?"* — y respondía que sí a una pregunta que nadie hizo.
- **Familia:** es [L-004] con otra ropa —una prueba que el código roto también
  pasa— y prima de [A-009], donde la suite apaga `Secure` para poder trabajar y
  al apagarlo deja de mirar el otro lado. 🔑 **En los tres casos el fallo no está
  en lo que el test afirma, sino en la condición que el propio test cambia para
  poder afirmarlo.**
- **Cómo se arregló:** el renglón pasa a `logger.warning`, que es el nivel más
  bajo que hoy se ve de verdad, y el test pide `caplog.at_level(WARNING)` — el
  nivel que el servidor tiene, no uno prestado. Comprobado con uvicorn: el
  renglón sale. Cuando [T-033] configure el log, vuelve a `info`.
- **Y lo que cierra `[A-003]`:** dejó de ser una suposición porque se midió. Sale
  de `assumptions.md` y llega aquí. ⚠️ La tarea que la resuelve, [T-033], **sigue
  pendiente** — lo que se acabó es la duda, no el trabajo.

> ⏩ **Continúa el 2026-08-04.** [T-033] se hizo ([D-028]): el log ya está
> configurado, `info` se ve de verdad, y este renglón —el de la cuota— volvió a
> `info`. El "sigue pendiente" de arriba ya no lo está.
>
> 🚨 **Y esta lección se repitió dentro de su propio arreglo, que es lo que hay
> que leer antes de tocar nada de esto: [L-015].** El test escrito para que un
> renglón no se aprobara a sí mismo medía el estado que ponía pytest y lo llamaba
> "lo que hace la función". La forma de esta trampa no es "usar `caplog` mal":
> es **cambiar la condición que hace verdad lo que vas a afirmar**, y tiene más
> disfraces de los que parece.

### [L-011] 2026-08-04 — El portero tenía una puerta de atrás, y su control no la veía

- **Qué pasó:** el portero de red bloqueaba `socket.connect` y `getaddrinfo`, y
  sus dos controles se ponían rojos como debían. Parecía terminado. La revisión
  externa probó `socket().connect_ex(('example.com', 80))` con el portero puesto
  y devolvió **`0`**: conectó. El portero estaba abierto de par en par.
- **Por qué se coló:** `connect_ex` hace lo mismo que `connect`, pero **devuelve
  un código de error en vez de lanzarlo**. Es la misma puerta con otra manija, y
  yo solo había cerrado la que conocía.
- 🔑 **Lo segundo, que es lo que enseña.** Al parchear `connect_ex` escribí el
  control con un **nombre** (`example.com`). Se puso rojo. Pero un nombre pasa
  primero por `getaddrinfo`, **que ya estaba parcheado desde antes**: ese rojo lo
  producía el parche viejo, y habría salido igual de rojo con el parche nuevo
  vacío. **El control no medía lo que decía medir.** Se separó con una IP literal
  (`1.1.1.1`), que no pasa por resolución de nombres: `0` sin portero,
  `NetworkTouched` con él. Recién ahí quedó demostrado.
- **Lo que se aprendió:** un control tiene que poder **fallar por una sola
  razón**. Si dos protecciones distintas producen el mismo rojo, el rojo no dice
  cuál de las dos funcionó — y una de ellas puede estar muerta sin que nadie se
  entere. Es [L-007] visto desde el otro lado: allí un control medía de más y
  gritaba con el código sano; aquí medía de más y **callaba el hueco**.
- **Y una tercera, del tamaño de la anterior:** el portero no ve los subprocesos
  (`node`, `git`), y no los verá nunca — son otro proceso. Eso no se arregla, se
  **escribe**: quedó en el docstring del portero y en la mitad "a mano" de
  [C-001]. 🔑 Un límite sabido y no escrito es un límite que alguien va a cruzar
  creyendo que estaba cubierto.

### [L-010] 2026-08-04 — 191 tests en verde y el servidor de verdad reventaba en `/logout`

- **Qué pasó:** `/logout` estaba escrito así —`def logout(response: Response) ->
  Response:` … `return response`—, devolviendo el objeto que FastAPI inyecta. La
  suite entera pasaba, incluido `test_logout_ends_the_session`. Al correrlo con
  uvicorn de verdad: `curl` devolvió **HTTP 000** y el log del servidor,
  `KeyError: None` en `STATUS_PHRASES[status]`. El `Response` inyectado nace con
  `status_code = None`, y uvicorn no tiene nombre para el código `None`.
- **Por qué la suite no lo vio.** Dos motivos que se sumaron, y el segundo es el
  que enseña:
  - `TestClient` no habla por HTTP: no pasa por `h11`, que es donde estaba la
    línea que reventaba. **El servidor de mentira era más tolerante que el de
    verdad.**
  - 🔑 **El test miraba el EFECTO, no la RESPUESTA.** Comprobaba que después de
    `/logout` la sesión estaba cerrada —y lo estaba, la cookie se borraba
    igual—, así que pasaba mientras la respuesta era inservible. Un test que
    solo mira consecuencias da por bueno cualquier camino que llegue ahí.
- **Lo que se aprendió:** *"terminado = visto funcionando"* (PI-4) no es una
  formalidad que se cumple después de tener los tests verdes. 🔑 **Los tests y la
  corrida real no miden lo mismo, así que uno no sustituye al otro.** Y es la
  tercera vez que este proyecto lo aprende: [L-003] (45 tests no vieron un fallo
  en 7 de cada 10 peticiones), [L-004] (una prueba que el código roto también
  pasa) y ahora esta.
- **El arreglo, y el test que faltaba:** se toca la cookie en el `response`
  inyectado y se devuelve `None`; FastAPI arma la respuesta con el 204 declarado.
  Y se añadió `test_logout_answers_the_status_code_it_declares`, que mira el
  código de estado y no solo lo que pasó después.
- **Toca:** `app/api.py` (`logout`), `tests/test_api.py`, y cualquier ruta futura
  que devuelva el `Response` inyectado en vez de dejar que FastAPI lo arme.

### [L-009] 2026-08-04 — Una regla que vive en dos archivos se corrige en los dos, o no se corrigió

- **Qué pasó:** al arreglar T-049 había que dejar escrito que el resultado del
  push no cabe en `tasks.md`, y que **el arranque de mañana lo recoge leyendo
  `git status -sb`**. La frase sonaba completa. Al ir a comprobarla,
  `protocol-start` no leía `-sb`: leía **`git status --short`**.
- **Medido aquí el 2026-08-04**, en un repo de prueba con un commit sin subir a
  propósito:

  ```
  === git status --short ===
  [vacío — no vio nada]

  === git status -sb ===
  ## main...origin/main [ahead 1]
  ```

  `--short` **no imprime la línea de la rama**. Los dos comandos listan los
  archivos sueltos, y por eso se parecen; solo uno dice si el trabajo llegó a
  `origin`.
- **Qué habría pasado sin comprobarlo:** el cierre se ejecuta entero, todo en
  verde, la nota dice "esto lo recoge mañana el arranque" — y mañana el arranque
  no ve nada, porque el repo le parece limpio. 🔑 **Una promesa escrita en un
  archivo que otro archivo tiene que cumplir no vale nada hasta que se abre el
  otro archivo.**
- **Por qué es [L-006] otra vez, y por eso duele:** L-006 fue "el cierre se
  cumplió entero y el trabajo se quedó sin subir". Este arreglo iba a reconstruir
  exactamente ese fallo, esta vez con la red de seguridad escrita y rota. La forma
  de la trampa es la misma: **algo que parece cubierto porque está escrito.**
- **La regla que queda:** cuando corrijas una regla, **pregunta quién más la
  dice**. Si la corrección se apoya en el comportamiento de otro archivo, ese
  archivo se abre y se comprueba — no se supone. Aquí la regla vivía en dos
  skills y solo se iba a tocar una.
- **Cómo se aplica:** antes de dar por cerrada una corrección de protocolo,
  `grep` del comando, del nombre del paso o de la promesa por todo el repo. En
  este arreglo eso sacó cinco sitios más: `session-closer.md`, `test_api.py`,
  `[A-006]`, y las referencias al nombre viejo del control.

### [L-008] 2026-08-03 — Se comparó la opción rival en su versión floja y se le ganó a esa

- **Qué pasó:** había que decidir dónde vivía el control del `.js`: en `pytest` o
  en el cierre. Se describió la opción del cierre como "un comando que tú corres
  antes de commitear" y se rechazó con "un freno que depende de tu memoria no es
  un freno". Nadie había propuesto esa versión: `.claude/agents/session-closer.md`
  existe y ya dispara controles solo, sin memoria de nadie.
- **Por qué pasó:** el principio invocado era correcto, y eso fue lo que lo
  escondió. Un argumento válido aplicado a una versión que nadie defendía suena
  igual de bien que uno bueno. 🔑 **Ganarle a la peor versión de la otra opción
  no es compararlas: es elegir primero y buscar razones después.**
- **Qué se hace distinto:** antes de recomendar entre dos caminos, escribir la
  opción rival **como la defendería quien la prefiere**, con lo mejor que tenga
  a favor. Si al lado de esa versión la recomendación se cae, es que no había
  recomendación. Aquí se cayó: el control acabó en el cierre, ver [D-017].
  Y ojo con el otro lado del mismo error — cuando el argumento propio se aplica
  también a la propia propuesta, hay que decirlo: `pytest` tampoco avisa si no
  corres los tests.

### [L-007] 2026-08-03 — La comprobación que mide de más: gritaba "viejo" con el repo correcto

- **Qué pasó:** el primer control del `.js` compilado usaba `diff -r` entre la
  carpeta que produce `tsc` y `app/static/`. Con el `.js` **perfectamente al
  día**, salía `Only in app/static: index.html` y el control lo declaraba viejo.
  La causa: `diff -r` compara en **las dos direcciones**, y `app/static/` es una
  carpeta mixta —también vive ahí `index.html`, escrito a mano, que ningún
  compilador va a generar nunca.
- **Por qué pasó:** se comprobó que el control **detectaba el fallo** y no se
  comprobó que **dejara pasar lo correcto**. Es el mismo animal de [L-003],
  [L-004], [L-005] y [L-006], pero por la cara que faltaba: las anteriores medían
  **de menos** —pasaban con el defecto puesto—; esta medía **de más**.
  🔑 **Y medir de más es peor de una forma concreta:** una alarma que nunca suena
  te deja ciego; una que suena **todas las noches con el repo correcto te entrena
  a apagarla**, y el día que suene de verdad ya le enseñaste a la gente a no
  mirar. La primera falla sola; la segunda se lleva por delante tu atención.
- **Lo doloroso:** la lección ya estaba escrita en este repo, por quien la volvió
  a incumplir un paso antes. `tests/test_tools.py`, en
  `test_normalize_user_accepts_ordinary_names`: *"El freno tiene que dejar pasar
  lo normal. Un validador que rechaza todo también pasaría los tests de arriba."*
  `diff -r` era exactamente ese validador que rechaza todo. **Saber un principio
  y aplicárselo a lo que estás escribiendo ahora son dos habilidades distintas**,
  y por eso el arreglo no puede ser "acordarse mejor" — [L-006] otra vez.
- **Qué se hace distinto:**
  1. **Un control se mide dos veces o no se midió:** una corrida con el fallo
     puesto y otra con el caso bueno. Las dos, en pantalla.
  2. **Y se mide en el caso que el diseño presume manejar.** La primera versión
     se midió con **un** archivo generado, y con uno solo el bug del bucle no
     puede aparecer: `for` devuelve el código del **último** comando, no de
     "alguno falló". Se destapó al probar con dos, con el que difiere delante.
  3. **La lista de lo que se vigila la declara el compilador**, no una lista
     negra de excepciones: se recorre lo que hay en su carpeta de salida. Una
     lista negra hay que mantenerla; esta se mantiene sola.
  4. **Detectar, informar y devolver éxito es no tener control.** Cada rama que
     encuentra algo mal levanta la bandera; un `echo` no frena nada.
  5. **El texto que se revisa tiene que ser el texto que se corrió.** La versión
     medida llevaba bandera y la que se pasó a revisar no: se "limpió" al
     transcribirla. El control vive en un archivo y se corre ese archivo.

### [L-006] 2026-08-03 — El cierre se cumplió entero y el trabajo se quedó sin subir: si el hash no está en `origin`, no hubo cierre

- **Qué pasó:** el cierre del paso 4 terminó con su commit y su hash, `f015a01`.
  La regla de cierre pedía exactamente eso, y se cumplió. Pero `origin/main`
  seguía en `460b04f`: el commit existía **solo en este disco**. Lo descubrió una
  revisión cruzada desde otra terminal haciendo `git fetch`. Un disco roto esa
  noche se habría llevado el paso 4 entero, con el cierre marcado como correcto.
- **Por qué pasó:** la regla vieja —nacida en la sesión 31— era *"si no hay hash,
  no hubo cierre"*. Esa regla comprueba que **existe un commit**, y de ahí se
  dedujo que el trabajo estaba a salvo. Son dos cosas distintas: un commit es
  local. 🔑 **Un control puede cumplirse entero y no comprobar lo que su nombre
  promete.** Cumplirlo daba tranquilidad y la tranquilidad era falsa, que es
  peor que no tener control: un hueco conocido se vigila, uno tapado no.
- **Y de qué familia es este fallo:** es el mismo defecto de [L-003], [L-004] y
  [L-005] —*la comprobación mide algo distinto de lo que dice medir*—, pero esta
  vez **no estaba en el código: estaba en el protocolo**. Sexta aparición del
  patrón, y la primera fuera de los tests. Donde haya un control hay que
  preguntarle qué mide de verdad, y los protocolos son controles.
- **Qué se hace distinto:** la regla queda corregida a **"si el hash no está en
  `origin`, no hubo cierre"**, y se comprueba con:

  ```bash
  git status -sb
  ```

  Si la primera línea dice **`ahead`**, no terminaste. El cierre acaba cuando esa
  palabra no aparece — no cuando aparece un hash.

### [L-005] 2026-08-03 — Buscar una palabra en un archivo entero no es comprobar el código: los comentarios también cuentan

- **Qué pasó:** la pantalla del paso 3 tiene que llamar a `/practice` con ruta
  relativa, sin nombrar host ni puerto — un `http://localhost:8000` escrito a
  mano funcionaría hoy y se rompería el día del despliegue. Para fijarlo se
  escribió un test que pedía el `app.js` compilado y comprobaba
  `assert "localhost" not in script`. Falló al primer intento, con el código
  **correcto**.
- **Por qué pasó:** la palabra `localhost` sí estaba en el archivo — dentro de un
  comentario que explica justamente por qué NO se usa. El compilador conserva los
  comentarios en la salida. El test decía medir "cómo llama la pantalla al
  servidor" y en realidad medía "qué letras aparecen en el archivo", incluidas
  las de la prosa que nadie ejecuta.
- **Qué se hizo:** apuntar a la llamada en sí, no al archivo:
  `assert 'fetch("/practice"' in script` y `assert 'fetch("http' not in script`.
  Eso sí distingue entre lo que el navegador ejecuta y lo que solo lee un humano.
- **Qué se hace distinto:** 🔑 **cuando un test busca texto dentro de un archivo,
  el patrón tiene que incluir la parte que lo hace código.** `"localhost"` cabe en
  un comentario; `fetch("http` no. Es la misma familia de [L-003] y [L-004] vista
  desde otro ángulo: allí el test no creaba el estado que decía probar, aquí no
  mira el sitio que dice mirar. En los tres casos el síntoma es el mismo —**la
  prueba mide algo distinto de lo que su nombre promete**— y solo se descubre
  preguntándose qué tendría que pasar para que fallara.
- **Y lo que salió bien:** falló al primer intento y por eso se encontró. Un test
  que hubiera pasado por casualidad —si el comentario no llega a existir— habría
  quedado ahí, dando una confianza falsa hasta el paso 7.

### [L-004] 2026-08-02 — Una prueba que el código roto también pasa no prueba nada

- **Qué pasó:** para comprobar el arreglo de concurrencia se montó una prueba de
  50 peticiones simultáneas por HTTP, con PowerShell. Dio **0 errores y marcador
  50**: perfecto. Pero por un puerto ocupado resultó que quien había contestado
  era el servidor **viejo**, sin el arreglo. Y también había dado 50 de 50.
- **Por qué pasó:** las 50 peticiones no salían lo bastante juntas. PowerShell
  tarda en arrancar cada hilo, así que llegaban en fila y nunca llegaron a
  pisarse. La prueba medía otra cosa distinta de la que decía medir.
- **Qué se hizo:** correr el `add_point` viejo y el nuevo, uno al lado del otro,
  con 50 hilos de Python sobre el mismo archivo. El viejo: **45 errores de 50**,
  marcador 1, números repetidos. El nuevo: 0 errores, marcador 50, 50 números
  distintos. Eso sí es una prueba.
- **Qué se hace distinto:** 🔑 **antes de fiarse de una prueba, comprobar que
  falla con el código roto.** Una prueba que pasa en los dos casos no está
  midiendo el arreglo, y da una confianza que no existe. Es el mismo criterio
  que ya está en `CLAUDE.md` como PI-4 —terminado = visto funcionando— llevado
  un paso más: **visto fallando cuando debía fallar.**
- **Y una segunda:** al levantar un servidor, comprobar en su log que dice
  "Uvicorn running on…". Si dice `[Errno 10048] error while attempting to bind`,
  el que contesta es otro, y todo lo que se mida después es sobre el código
  equivocado.

### [L-003] 2026-08-02 — 45 tests en verde no vieron un fallo que rompía 7 de cada 10 peticiones

- **Qué pasó:** el paso 2 se cerró con 45 tests en verde y el servidor probado a
  mano. Una revisión externa lo levantó con **50 peticiones a la vez** y entre 31
  y 39 devolvieron error 500. De 50 puntos esperados, el marcador guardaba 8.
- **Por qué pasó:** `TestClient` manda las peticiones **de una en una**. Todos
  los tests, y todas las pruebas a mano, ejercitaban un solo escritor. Con un
  solo escritor el código era correcto — el fallo no estaba en las piezas, estaba
  en dos piezas ocurriendo a la vez, que es un estado que ninguna prueba creaba.
- **Qué se hace distinto:** 🔑 **un test en verde no dice "el código está bien",
  dice "el código está bien para lo que este test hace".** Al cambiar de terminal
  a servidor cambió una suposición de fondo —de un escritor a muchos— y ninguna
  prueba se enteró. Cuando cambie esa clase de suposición, hay que escribir el
  test que la ejercite: aquí, hilos de verdad sobre el mismo archivo.
- **Cuándo vuelve a pasar:** en el paso 4 (memoria por persona) y en el paso 7
  (la nube decide cuántos procesos hay). Anotado como suposición [A-002].

### [L-002] 2026-08-02 — `pip install` sin versión fijada no da la misma versión dos veces

- **Qué pasó:** al crear el entorno virtual, `pip install pytest` instaló
  **pytest 9.1.1**. El Python global de la misma máquina tenía **8.1.1**. Dos
  versiones distintas, el mismo día, sin haber hecho nada raro.
- **Por qué pasó:** `pip install pytest` no pide "pytest": pide "el pytest más
  nuevo que haya hoy". La respuesta cambia con el calendario. El global se
  instaló hace meses; el del entorno, hoy.
- **Qué se hace distinto:** toda dependencia va en `requirements.txt` con `==` y
  versión exacta. Se instala con `pip install -r requirements.txt`, nunca por
  nombre suelto. Sin eso, un fallo que solo aparece en una máquina —o solo en el
  servidor del paso 7— se vuelve casi imposible de encontrar: el código es el
  mismo y las librerías no.

### [L-001] 2026-08-02 — La consola de Windows no pinta caracteres fuera de ASCII

- **Qué pasó:** `main.py` imprimía `TEAPP — write a sentence...` con guion largo,
  y en pantalla salió `TEAPP ? write a sentence...`. Los tests no lo detectaron:
  pasaban los 14. Se vio solo al correr la app de verdad.
- **Por qué pasó:** la consola de Windows no usa UTF-8 por defecto, y el guion
  largo no existe en su tabla de caracteres. Lo sustituye por `?`. El código era
  correcto; lo que fallaba era el sitio donde se imprimía.
- **Qué se hace distinto:** en lo que se imprime por terminal, solo ASCII. Y la
  lección de fondo, que es la que importa: **PI-4 no es burocracia.** Los tests
  daban verde sobre un texto que en pantalla salía roto. Un test comprueba lo que
  la función devuelve, no lo que la persona ve. Por eso "terminado = visto
  funcionando" pide las dos cosas, no una.

<!-- La más reciente arriba. Formato:

### [L-001] 2026-08-02 — <la lección, en una línea>

- **Qué pasó:** <el fallo o la sorpresa>
- **Por qué pasó:** <la causa, ya entendida>
- **Qué se hace distinto:** <la regla que queda para adelante>

-->
