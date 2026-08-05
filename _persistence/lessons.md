# Lecciones aprendidas — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [L-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

| id | fecha | qué se aprendió | a raíz de |
|---|---|---|---|
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
