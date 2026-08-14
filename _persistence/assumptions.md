# Suposiciones sin comprobar — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [A-000]`. Búscala con `grep`, no leas el archivo entero.

⚠️ Aquí vive **solo lo que no se ha comprobado**. Cuando una suposición se
comprueba o se decide, **sale de aquí** y entra en `decisions.md` o `lessons.md`.

## Índice

| id | fecha | qué se está dando por cierto | riesgo si es falsa |
|---|---|---|---|
| A-030 | 2026-08-14 | 🔌 **Se da por cierto que el VERDE de `[D-077]` vale para producción, aunque la báscula REUSARA la conexión y producción la abra en cada práctica.** `measure_tutor.py:396` construye el cliente **una vez** y lo reusa en las 60; `app/tools.py:481` construye uno **nuevo** cada llamada cuando `client=None`, que es como llama `app/english_tutor.py:86`. La fase `connect` —**1,5 s de los 9,0** del cliente— se ejerció en **1 de 60** muestras. ✅ **No tumba el veredicto:** 2,6 s de holgura (3,91 contra 6,5) contra un apretón de manos de décimas. ⚠️ **Se anota porque el docstring de la báscula enumera lo idéntico** —*mismo modelo, mismo esfuerzo, misma rúbrica, mismos `max_retries`, misma `judge_grammar`*— **y esa lista se lee como exhaustiva**; el ciclo de vida del cliente no está en ella. Forma exacta de `[L-043]`. 📌 Y el proyecto ya sabía la mitad: `app/tools.py:182` avisa de que con `keepalive_expiry=5.0` y tráfico esporádico **casi cada llamada paga handshake nuevo** — el perfil de una app con pocos usuarios. 🔍 **Cómo se comprobaría:** correr la báscula construyendo el cliente dentro del bucle. **No se hace hoy** (regla 5); se reabre si el peor caso se acerca al corte. Hallazgo H-3 de la auditoría externa del 2026-08-14 | si es falsa, el tiempo real de una práctica es mayor que el medido en toda la cola, y el margen contra `read = 6,5` es menor de lo que `[D-077]` cree — el fallo aparecería como cortes esporádicos que la medición no predijo, y `[A-011]` volvería disfrazada de asunto zanjado |
| A-029 | 2026-08-14 | ⏱️ **Se da por cierto que el trabajo local de `respond()` cabe en 0,07 s, y ese número es `max(N)` redondeado — el estadístico que `[L-058]` prohíbe justo para esto.** Sale de los **56,3 ms** de `measure_local_parts.py`, que `app/api.py` cita como *"cinco corridas"* cuando el guion ya registra **seis**, la última de **62,4 ms** (`44,9 → 45,9 → 49,2 → 50,6 → 56,3 → 62,4`, **+39% y subiendo**). `max(N)` es un suelo que crece con N, no una cota: una séptima tanda puede pasar de 0,07. 🔑 **Se usa igual porque el error cae del lado seguro:** `LOCAL_WORK_SECONDS` es un sumando del **mínimo** que exige el assert de `[D-076]`, así que subestimarlo hace ese assert más PERMISIVO, nunca más estricto — deja pasar un hueco pequeño, no rechaza uno válido. ⚠️ **Lo que NO puede hacerse es tratarlo como medido:** el assert lo convierte en código, y un número en código se lee como dato. 🔍 **Cómo se comprobaría:** un percentil DECIDIDO ANTES (no `max`) sobre una tanda de `measure_local_parts.py` con la carga de 40 hilos, o directamente una resta que no dependa de medir. El día que exista, se sube `LOCAL_WORK_SECONDS` y el assert aprieta solo | si es falsa, el assert del hueco cliente→ruta pasa con un margen que no da para el trabajo local real: el cliente deja de rendirse antes que la ruta, salta el 504 y el error de Anthropic se esconde detrás (`[D-051]` cobra la práctica). Es fallo silencioso, y hoy no muerde porque el hueco real (1,0 s) sobra por mucho |
| A-026 | 2026-08-12 | 🔁 **Se da por cierto que nadie va a correr `measure_tutor.py` muchas veces SEGUIDAS — y es el único flanco del saldo que no tiene dueño.** El `CallBudget` de `[D-060]` corta a `$0,25` **dentro** de una corrida, pero **el monedero se reinicia en cada arranque**: `$6,48 ÷ $0,25 = 26` corridas vacían el saldo, y a 106 llamadas × 1,72 s son **79 minutos** — **dentro** de la ventana ciega de 120 del tope de gasto (`[A-025]`), así que el tope de `$2` de `[D-062]` **tampoco lo tapa**. 🚨 **Nada en el código lo impide: ni una capa lo cubre, ni una tarea lo reclama.** Lo único que hay entre el saldo y el vacío es la mano de quien lanza el guion. ⚠️ **Y el paso 9 es justo el día de más riesgo:** consiste en correr el guion una vez por modelo, comparando, repitiendo y reafinando — la forma de trabajo que más se parece a las 26 corridas. 🔍 **Cómo se comprobaría / cómo se cerraría:** un monedero que **sobreviva al arranque** (contador en disco, en `data/` o junto al guion) en vez de reiniciarse en cada corrida — es lo que convierte el tope por corrida en tope por día. **No se construye hoy** (`[PI-2]`: nada lo ha pedido todavía); se anota para que no vuelva a aparecer como sorpresa | si es falsa, el saldo se vacía en ~79 min **sin que ninguna capa avise**, y `[C-008]` se cumple entera: la app viva dando 503 mudo. Es el fallo silencioso, no el ruidoso |
| A-025 | 2026-08-11 | 🔍 **COMPROBADA el 2026-08-12 y SIGUE EN PIE: la pantalla salió MUDA.** `Settings → Workspaces → Spend limits` solo dice *"El límite de gastos mensual de tu organización es de $500,00. Puedes establecer un límite de gastos inferior…"* — ni `soft`, ni umbrales, ni retraso. **Salir muda no es salir falsa:** no asciende, se queda aquí. Se decidió cómo actuar mientras tanto, por la rama pesimista (`[D-062]`). ⏳ **El tope de gasto por espacio de trabajo es BLANDO y tarda ~2 horas en enterarse del gasto reciente.** La frase está leída, pero **en la página equivocada**: sale en la documentación de *Claude Platform on AWS* — *"The spend limits you set are **soft limits**: spend is calculated at list prices and can take **about two hours** to reflect recent usage"* — y se está extendiendo a la consola de primera parte, que es la que usa el proyecto y que **no dice nada** sobre cómo se hacen cumplir. 🔑 **Por qué se escribe aparte de `[D-059]`:** es la razón por la que ahí se eligió el corte duro en el guion en vez de fiarse del tope. Si mañana resultara que en primera parte el tope es duro e inmediato, `[D-059]` seguiría en pie igual —el saldo compartido no lo arregla ningún tope— pero la capa 2 pasaría de "contabilidad y velocidad" a "freno de verdad". ⚠️ **El número que la hace importar:** `measure_tutor.py` hizo diez llamadas en menos de un minuto. Un tope que reacciona en dos horas llega 119 minutos tarde. 🔍 **Cómo se comprueba:** en la consola, **Settings → Workspaces**, abrir la pestaña **Spend limits** de un espacio y leer si el texto de la propia pantalla dice `soft`, si habla de alertas por umbral en vez de corte, o si menciona retraso. Acción del usuario: el navegador lo toca él (regla 1) | si es MÁS blando de lo supuesto no pasa nada — el corte duro de `[D-059]` ya cubre ese caso, que es justo para lo que se puso. 🚨 **El daño está en creerla al revés:** si alguien la lee como "hay tope por espacio, luego estamos protegidos" y quita el corte duro del guion, se queda **sin ninguna capa** sobre el saldo compartido, que es el fallo de `[C-008]` |
| ~~A-024~~ | 2026-08-10 | ✅ **RETIRADA el 2026-08-11 al MIRARLA en la consola de Anthropic (`T-080`); vive ahora en `[D-057]`, con lo medido y el tope elegido.** Era **falsa**: sí hay tope, y de dos clases — un **saldo prepagado** (6,55 US$ el 2026-08-11) con **recarga automática DESACTIVADA**, que es un techo duro y hoy es el freno que manda; y un **límite de gasto mensual** de 500 US$ puesto por Anthropic, ajustable, que hoy no puede morder porque el saldo se agota mucho antes. Decía: 🚨 **Y `T-079` es justo la tarea que empieza a llamar de verdad**, en bucle, para medir `[A-010]` y `[A-011]`: un bucle de medición con un fallo tonto —un `while` que no sale, un reintento mal puesto— llama sin techo. 🔑 **La asimetría con AWS es el punto:** la cuenta de AWS tiene alarma (`[A-018]`, con su propia duda sobre si avisa a tiempo); la llave de Anthropic, que conste, **no tiene nada** — y un freno que no existe no es un freno flojo, es que no está. ⚠️ **Son cuatro bolsillos distintos y no se mezclan** (`[A-018]` ya se rompió una vez por juntar fuentes): la IP elástica + EC2 + EBS se miran en la consola de AWS; la **llave de la API** en la consola de Anthropic; y la **suscripción de Claude Code** en `claude.ai/settings/usage` — esta última es **el taller, no la obra**: no entra en `[A-018]` ni en `[T-067]` ni en el presupuesto del proyecto. 🔍 **Cómo se comprueba:** entrar a la consola de Anthropic y mirar si la llave admite límite de gasto o alerta de uso; si lo admite, ponerlo **antes** de que `T-079` empiece a llamar. Señalado por auditoría externa el 2026-08-10 | 🚨 un bucle de medición descontrolado gasta sin techo y **sin aviso**, en el único sitio del proyecto donde no hay ningún freno. Choca de frente con la regla 5 —minimizar factura manda sobre todo lo demás— y con `[C-006]`, que es la razón por la que el dinero de esta cuenta está contado |
| A-023 | 2026-08-10 | **Aplazar el ensayo de `T-069` hasta después del paso 8 no lo encarece ni lo debilita.** Es el precio que `[D-048]` acepta a sabiendas al cruzar de paso, y se escribe aparte para que no viaje escondido dentro de la decisión. Se apoya en dos patas, y **ninguna de las dos está medida**: (1) que `deploy/` siga levantando TEAPP dentro de unas semanas igual que hoy, y (2) que el ensayo siga costando lo mismo. 🚨 **La pata (2) es la floja, y por un motivo concreto: el paso 8 VA A TOCAR `deploy/`.** La API key tiene que llegar al servidor sin pasar por el navegador (regla 1) ni por el código (regla 7), así que entra por el archivo de entorno y `install.sh` tendrá que ponerla — 🔑 **lo que se ensaye en septiembre no será el `deploy/` de hoy, será uno con una pieza nueva y sin estrenar**, justo la que guarda el secreto. 📌 Eso no es solo riesgo: también es argumento a favor de esperar, porque ensayar hoy dejaría sin ensayar precisamente esa pieza. Lo que **no** se puede es cruzar creyendo que da igual. 🔍 **Cómo se comprueba:** corriendo `T-069` (Paso 5c de `deploy/console_steps.md`, ya escrito), con **fecha tope ≈ 2026-09-01** — el cierre del primer ciclo de facturación, que es cuando `[A-018]` deja de estar ciega y hay motivo para volver a la consola de todos modos. ⏳ Y hay un reloj que no se negocia: `[C-006]`, la cuenta muere el 2027-02-06 | 🚨 se descubre que `deploy/` no levanta **más tarde y con menos margen**, que es exactamente el escenario del que `[D-030]` quería escapar. Y en el peor caso el fallo aparece en la pieza de la llave, mezclado con el estreno del modelo: **dos sospechosos en vez de uno**, que es el error que el roadmap entero está diseñado para evitar |
| A-022 | 2026-08-09 | **`OnCalendar` aceptará la zona horaria escrita dentro (`*-*-* 23:00:00 UTC`) en cualquier máquina donde se reconstruya TEAPP.** Es la decisión central de `deploy/teapp-shutdown.timer` y todo `[D-046]` descansa en ella: es lo que hace que la hora viaje con la pieza en vez de depender de la zona de la máquina. ⚠️ **Pero el soporte de zona en `OnCalendar` depende de la versión de systemd**, y `install.sh` existe por `C-004` — la cuenta se cierra y esto se vuelve a correr en una máquina nueva, quizá con otra imagen. En una systemd más vieja sería un **error de sintaxis** y el temporizador no cargaría. 📌 Hoy no está comprobado en ningún sitio: `install.sh` verifica que el temporizador quede activo y habilitado, pero **no** que la hora se haya interpretado como se cree. 🔍 **Cómo se comprueba, y es gratis:** `systemd-analyze calendar '*-*-* 23:00:00 UTC'` en la máquina — imprime cómo lo entiende systemd y cuándo dispararía. Si dice `Next elapse: … 23:00:00 UTC`, queda demostrado y no supuesto. 🧪 Se mide en la máquina de hoy (cierra el caso presente) y **otra vez en `T-069`**, el ensayo de reconstrucción, que es donde de verdad mordería. 📌 Nace de una revisión externa el 2026-08-09, junto con `[L-034]`. 🔻 **ENCOGIDA el 2026-08-10: la mitad de hoy está MEDIDA en la máquina viva** — `systemd 255 (255.4-1ubuntu8.16)` contesta `Normalized form: *-*-* 23:00:00 UTC` / `Next elapse: Mon 2026-08-10 23:00:00 UTC`. Ni error de sintaxis ni zona ignorada: systemd entiende la línea como se cree. ⚠️ **Y no cierra la suposición, porque la suposición nunca fue sobre esta máquina** — dice *"en cualquier máquina donde se reconstruya"*, y eso solo lo mide `T-069` sobre imagen nueva. Lo que cambia es el tamaño del riesgo: ya no es "puede que la línea no funcione en ningún sitio", es "funciona en systemd 255; falta saber el suelo de versión" | 🚨 el temporizador **no carga**, y el fallo es de los mudos: `install.sh` se pararía en rojo si systemd rechaza la unidad —eso está cubierto—, pero en una reconstrucción a contrarreloj el síntoma aparece mezclado con el primer despliegue, que es exactamente lo que `[D-043]` evita en otro sitio. Y si cargara **ignorando** la zona en vez de rechazarla, la ventana de `[D-045]` se movería 5 horas sin un solo error |
| A-021 | 2026-08-06 | **Que una tarjeta firmada valga aunque su cuenta no exista no hace daño en la v1.** El mecanismo está **MEDIDO, no leído** (corrida del 2026-08-06): se registró una cuenta, se practicó, se borró la cuenta del almacén dejando la cookie intacta — y `/practice` siguió contestando `200` y `/me` siguió diciendo `efimero`. La identidad sale solo de la firma (`app/api.py:554` → `_current_user` → `sessions.read`); **nadie consulta `accounts.json` después del login**. ⚠️ Lo que NO está comprobado es que sea inofensivo. Se sostiene sobre dos patas: la v1 **no tiene forma de borrar una cuenta** (no hay ruta que lo haga), y **firmar exige la llave**, que vive en el servidor. 📌 Nació de una deducción equivocada —ver `[L-023]`— y se re-verificó por su cuenta antes de escribirla | si aparece el borrado de cuentas, o si la llave se filtra, **no hay revocación SELECTIVA**: cortar una sola sesión es imposible, y cada `/practice` con una tarjeta así **crea marcador y cuota de un fantasma** en `data/` — la misma clase de archivo huérfano que abrió `T-072`. 🔨 La palanca que sí existe es tosca y hay que tenerla pensada de antemano: **cambiar `TEAPP_SECRET_KEY` invalida TODAS las sesiones de golpe** (`[L-032]`, antes `[A-008]`), incluida la que sobra |
| A-018 | 2026-08-06 | **La alarma de facturación avisará el día que haga falta.** Están creadas **dos** alertas en un mismo presupuesto —coste **real** y coste **previsto**, ambas a 0,01 US$ absoluto— y el correo está verificado, pero **ninguna se ha visto saltar**. 🔴 Corregida dos veces el 2026-08-06. **El silencio NUNCA la confirma.** ✅ Resuelto que el presupuesto mide coste **BRUTO** (leído en pantalla): los créditos no enmascaran nada, no hace falta un segundo presupuesto, y la EC2 encendida **tiene que** hacerla sonar. 🧪 **Experimento escrito por adelantado, con tabla de lectura y DOS observaciones** (la factura = premisa, la bandeja = prueba); disparador: reservar **solo la Elastic IP**, que cobra estando ociosa. ⏳ El umbral de $0,01 **no se toca hasta después** — cambiarlo destruiría el experimento. 🔄 **Dos lecturas el 2026-08-07, las dos NO CONCLUYENTES.** La 2ª (14:36 UTC, ~23,1 h desde `t=0`) encontró tres cosas: (a) `Facturas` **era la ventana equivocada las dos veces** — una factura nace al cerrar el mes, su *"sin datos"* habla del calendario, no del gasto; la lectura buena es el campo *Importe utilizado* del **propio presupuesto**, que es el **mismo instrumento** que la alarma → hoy **0,00 US$ con un `0.00%` calculado**, un cero de verdad y no una ausencia, pero aún dentro del retraso; (b) ✅ **AWS no puede proyectar sin historial** — *Importe previsto* = `-`, leído en pantalla: la alerta de coste **previsto** no pudo disparar y su silencio no prueba nada; (c) 🔴 **corregido en caliente**: se iba a cerrar con "aplican las 750 h gratis de IPv4" y la documentación dice lo contrario — esas horas son para direcciones **EN USO**, y la nuestra está **ociosa**, así que **sí cobra** (~23 h × 0,005 US$/h ≈ 0,115 US$ bruto, >10× el umbral; aritmética de lista, no corrida). El disparador es válido y el experimento **sigue siendo falsable**. 🚨 **ENMIENDA SELLADA el 2026-08-07, antes de mirar nada: la FILA 3 de la tabla original de `cfba50a` queda ANULADA** (no borrada — se lee con autoridad y nombraba una causa hoy desmentida). `= 0,00` ya **no** significa "es gratis": quedan dos causas vivas, **(a)** el dato no aterrizó → esperar, **(b)** algo absorbe el cargo → hallazgo; los créditos ya están descartados porque mide bruto. 🚨 **Y guardia nueva sobre la FILA 2**: los presupuestos se refrescan *"up to three times a day … 8–12 hours after the previous update"* (documentación, 2026-08-07) → **"alarma rota" exige ≥12 h de silencio DESPUÉS de que el importe sea visible**. 🔴 **El motivo se corrigió DOS veces:** ni *"son dos retrasos en serie, ~24 h + 8–12 h ≈ 36 h"*, ni *"eso era doble conteo"* —**la segunda afirmaba de más**, porque llamarlo doble conteo **es** afirmar que comparten reloj, el mismo dato que la frase declaraba desconocido. ✅ Queda **un solo desconocido**: *no se sabe si lo que se MUESTRA y lo que se EVALÚA salen del mismo refresco*; si lo comparten faltan **minutos**, si van desacoplados faltan **horas**. La regla se queda porque esperar de más no produce conclusión falsa en **ninguna** rama. 🎁 Y hay **medición gratis**: se anotan `h1` (importe visible > 0,01) y `h2` (llega el correo); `h2 − h1` es un número que no tiene ni la documentación y **resuelve el desconocido** — la espera pasa a ser la **segunda medición** (`LM.19`). ⚖️ **Precio del cambio de instrumento, escrito:** premisa y prueba ahora cuelgan las dos del servicio de presupuestos — falla del lado seguro, pero el experimento **ya no cubre** un fallo en la entrada de datos, solo el tramo "el presupuesto vio el dinero → mandó el correo". ⏳ **Tercera lectura 2026-08-07 tarde: sigue 0,00**, y el presupuesto **explicó su propio silencio** con un **CUARTO reloj** que no estaba escrito — *"después de crear un presupuesto, pueden transcurrir hasta 24 h para que se rellenen todos los datos de gastos"*, que arranca en la **creación del presupuesto** (06 durante el día, antes de las 15:29 UTC) y vence **durante el 07**. Refuerza la causa (a) con motivo documentado, **no cierra nada** —*"hasta"* vuelve a ser techo, no promesa—. Próxima lectura **2026-08-08**, con el reloj 4 ya vencido; el criterio ya **no** es "que desaparezca un mensaje" —eso falló— sino que *Importe utilizado* deje de ser 0,00. 🟢 **Cuarta lectura 2026-08-08, 11:10 UTC (~43,7 h desde `t=0`): EL DATO ATERRIZÓ, y en una pantalla que no estaba en ninguna tabla** — widget `Resumen de Costos` de la página de inicio de *Facturación y costos*, campo `Costo Acumulado Mensual` = **0,12 US$**, mientras `Importe utilizado` sigue en **0,00**. ✅ **Mata la causa (b)** —hay cargo visible, nada lo absorbe— y **confirma y LOCALIZA la (a)**: no es que AWS no haya calculado el coste, es que **el presupuesto no se ha refrescado**; queda solo el tramo 2 (*8–12 h*), que hasta hoy estaba **leído y nunca observado** — ahora se ven los dos tramos en serie a la vez. ⚖️ No es enmendar la tabla con el dato delante (lo que `[D-040]` prohíbe): la tabla **encargaba** distinguir (a) de (b), y esto la **ejecuta**. 🆕 Instrumento **quinto** y el más rápido de los tres → ventana de **aviso temprano** para los seis meses; ❓ sin verificar si mide bruto o neto, **y la conclusión no depende de ello** (cualquier valor > 0 basta). 🚨 **NO cierra `A-018`: `h1` no ha ocurrido**, la guardia de ≥12 h ni ha arrancado y la alarma **sigue sin habérsele visto morder**. 📐 `0,12 ÷ 0,005 ≈ 24 h` facturadas contra ~43,7 h transcurridas → la pantalla va **~20 h por detrás** (aritmética de lista, no corrida). ❓ Se perdió la hora exacta de aparición: ayer no se miró ese widget porque **no se sabía que existía**. 🟡 **Quinta lectura 2026-08-08, 15:08 UTC (~47,7 h): `Importe utilizado` sigue en 0,00**, sin cambio en 3,9 h — `h1` no ha ocurrido y la guardia de las ≥12 h sigue sin arrancar. Se hizo por `[D-041]`, no por el experimento: **ese orden queda cumplido y la segunda mitad de `[T-059]` desbloqueada**. ⚠️ Desde que arranque la EC2 hay **dos fuentes de gasto**: `h1` y `h2 − h1` sobreviven, pero la **cuantía** deja de ser atribuible solo a la Elastic IP. ⏱️ **`t=0` de la EC2 MEDIDO en la máquina el 2026-08-08 (`uptime -s` → `15:54:27 UTC`), no deducido** — corrige la suposición de que había arrancado a las 15:08 (esa era la hora de LEER el presupuesto, 46 min antes de lanzar; tomarla por `t=0` infla el divisor ~55% en la aritmética dinero÷horas). Ahora hay **dos relojes**: IP desde el 06 a las 15:29 UTC, EC2 desde el 08 a las 15:54:27 UTC. ✅ De paso `[D-043]` verificado en la máquina: `Ubuntu 24.04.4 LTS`. 🟠 **Sexta lectura 2026-08-09 ~14:45 UTC (~71,3 h de IP, ~22,9 h de EC2): `Importe utilizado` SIGUE en 0,00 —cuarta lectura seguida— mientras `Costo Acumulado Mensual` sube a 0,37 US$.** `h1` no ha ocurrido y la guardia de las ≥12 h sigue sin arrancar. 🆕 Lo nuevo: el **tramo 2** (refresco del presupuesto, *8–12 h*) lleva **~27,6 h** desde que el coste era visible — **más del doble del techo documentado**; se anota como hecho, **no** como veredicto: declarar la alarma rota aquí sería cambiar el criterio con el dato delante (`[D-040]`). 📐 `0,37 ÷ 0,005 ≈ 74 h` facturadas contra ~71,3 h de vida de la IP → la cifra **ya no cabe en la IP sola**: primera señal en pantalla de que la EC2 pesa (aritmética de lista; el precio/hora de la `t3.micro` no se usa por no estar medido — eso es `[T-067]`). Umbral cubierto **37×**: cuando el presupuesto refresque, tiene que sonar. 🔴 **CORREGIDO el 09: son TRES fuentes de gasto, no dos** —la quinta lectura escribió "dos" y olvidó el **volumen EBS**, que cobra por existir esté la máquina encendida o no, desde el 08 15:54 UTC—; no cambia ninguna conclusión de hoy (la aritmética usó el total, no la composición) pero **`[T-067]` tiene que separar tres tarifas**, y solo una se apaga de noche con `[D-045]`. 📚 **2026-08-10, el `-` de *Importe previsto* pasa de observado a DOCUMENTADO** (auditoría externa, `ce-forecast.html`): *"If AWS doesn't have enough data to forecast an 80% prediction interval, Cost Explorer doesn't provide a forecast. This is common for accounts that have less than one full billing cycle."* La cuenta se abrió el 06 → 4 días, menos de un ciclo. 🔑 No añade una causa nueva —el 07 ya se había concluido *"no puede proyectar sin historial"*— pero añade **la fecha en que deja de ser ciego**: al cerrar el primer ciclo (≈ 2026-09-01). Hasta entonces la alerta de coste **previsto** da la misma raya con la alarma sana o rota, así que **no se le pide información a esa mitad**. 🔴 **Y se DESCARTA el experimento propuesto de "bajar el umbral por debajo de lo ya gastado": ya está por debajo.** El umbral es **0,01 US$ absoluto** desde el 06 y el gasto va por **0,37 US$** — cubierto 37× — sin que haya saltado nada en 4 días. Bajarlo más no crea una rama nueva: el campo que la alarma **evalúa** (`Importe utilizado`) sigue en **0,00**, y contra 0,00 **ningún umbral positivo dispara**. 🔑 El experimento que se proponía **ya está corriendo desde el día 6**, y su resultado hasta hoy es *"no salta"*; moverle el umbral solo destruiría la línea base y añadiría una tarea con caducidad (devolverlo) a cambio de nada. **El único suceso que discrimina sigue siendo `h1`: que `Importe utilizado` deje de ser 0,00** | 🚨 el día del gasto no avisa nadie, y se descubre por el saldo. Y aunque avise bien, **con ~24 h de retraso no puede frenar las 7 puertas de `[C-005]`**, que evaporan los créditos *"en el acto"*: protege del goteo, no del acantilado |
| A-017 | 2026-08-05 | **DuckDNS seguirá en pie los 6 meses del paso 7.** Comprobado que existe y funciona hoy, **no que vaya a durar**: es gratuito, se sostiene con donaciones y tiene caídas registradas — una el 2026-06-21 y un episodio en agosto de 2025 en que se dio por desaparecido. 🟠 **2026-08-08: fallos de resolución OBSERVADOS, 3 episodios desde 2 redes** — ráfagas de `Could not resolve host` con recuperación inmediata y la máquina sana. 🔴 **La CAUSA está SIN RESOLVER y NO es evidencia contra DuckDNS:** el diagnóstico no reprodujo (16/16 correctas, resolutor local y `8.8.8.8`), y en un episodio el puerto 80 resolvió el **mismo nombre en el mismo instante** en que HTTPS no — un autoritativo caído no hace eso, apunta al resolutor del cliente. ✅ Lo aprovechable es el modo de fallo: **se disfraza de avería propia**, y se separa con `curl --resolve`, que salta el DNS sin renunciar a verificar el certificado. ✅ **Exposición MEDIDA el mismo día:** certificado Let's Encrypt válido hasta **2026-11-06** (90 días exactos, leídos con `openssl s_client`) → la ventana de renovación cae hacia principios de octubre. 🟢 **2026-08-09, episodios 4 y 5: CAUSA LOCALIZADA — no es DuckDNS.** El fenómeno se dio **partido entre dos programas del mismo ordenador en el mismo minuto**: `ssh` decía *"Could not resolve hostname"* mientras `nslookup` (router **y** `8.8.8.8`) devolvía `32.199.55.191` y `curl` sacaba un `200`. Un autoritativo caído no responde a dos programas y le niega la respuesta al tercero → **es la resolución del cliente**. ⚖️ Los cinco episodios **dejan de contar como cargo contra DuckDNS**, y `A-017` sigue exactamente igual de sin comprobar. 🔴 Y murió una hipótesis en dos minutos: se creyó que era la consulta IPv6 y que `-4` lo arreglaba —**funcionó una vez y falló la siguiente**—; con un fallo **intermitente** el primer verde es la línea base, no una cura (`[L-020]`). ✅ Rodeo sólido: entrar **por la IP fija**, que no pasa por el DNS — hermano del `--resolve`: no arregla, **separa**. ⚠️ Y no sirve para quien use TEAPP desde su navegador: esa persona solo ve una página que no carga | 🚨 **no es que se vea feo: es que no entra nadie.** Sin nombre no resuelve, sin resolver Caddy no renueva el certificado, sin certificado la cookie `Secure` no viaja. El servidor sigue encendido y la app cerrada |
| A-015 | 2026-08-05 | **El paso 7 cabe de sobra en los $200: gasta del orden de $50.** Es aritmética de lista de precios, **no una corrida**, y le falta el costo de la IPv4 pública. Sobre esta holgura se descartó la pieza que apaga la máquina sola (`[D-029]`). 🔁 **2026-08-09: ese descarte queda REVOCADO por `[D-045]`** — hay ventana de uso y apagado automático. La holgura **sigue sin medirse**; quien la mide es `[T-067]`, y ahora bajo el régimen de ventana, no con la máquina de 24 h | se acaban los créditos antes de los 6 meses y AWS cierra la cuenta a media obra |
| ~~A-014~~ | 2026-08-04 | ✅ **RETIRADA el 2026-08-10 al comprobarse en el servidor real (`T-066`); vive ahora en `[L-036]`, con la medida entera y la trampa que la habría invalidado.** Decía: **`request.client.host` es el origen REAL de quien pregunta** (🔻 **encogida el 2026-08-06**: el mecanismo ya está MEDIDO — uvicorn 0.52.1 reescribe esa dirección desde `X-Forwarded-For` y solo se fía si la petición llega por loopback, ver `[D-034]`. 🔻 **encogida OTRA VEZ el 2026-08-07**: **Caddy escribe la cabecera, MEDIDO** con aparejo de dos contenedores —cliente `172.17.0.4` ≠ proxy `172.17.0.3`, porque con uno solo el valor no distingue "la real" de "la inventada"— y de regalo **descarta la forjada**: quien manda `X-Forwarded-For: 9.9.9.9` llega como `172.17.0.4`, porque sin `trusted_proxies` Caddy reescribe en vez de añadir. Cadena entera: seis logins fallidos con seis orígenes falsos y el freno saltó igual, contra el real. Queda **una sola** cosa sin comprobar, y **no es Python ni es Caddy**: ~~que el cortafuegos de `T-060b` deje el 8000 cerrado~~ 🔴 **corregido el 2026-08-10 — `T-060b` está MEDIDA desde el 08** (timeout desde fuera con `python` escuchando en el 8000); lo que faltaba era **`T-066`: la cadena entera en el servidor real** — ✅ **medida el 2026-08-10, ver `[L-036]`**. ⚠️ Ese puntero a `T-060b` mandó a una tarea cerrada durante tres días — `[L-028]`, la frase que nadie editó y que el mundo dejó atrás) | detrás de un proxy todo el mundo llega con la misma dirección: el primero que falle 5 veces deja fuera a todos los demás |
| A-013 | 2026-08-04 | **5 fallos y 15 minutos son los números correctos** para el tope de intentos de `/login`. Predicción, no medida. 🔑 Y lo que decide el número no es cuánta gente ataca, sino **cuánta comparte origen**: el freno reparte 5 por dirección, no por persona ([D-026]) | corto, deja fuera a quien solo se equivocó recordando su contraseña; largo, quien prueba a la fuerza tiene sitio de sobra |
| ~~A-011~~ | 2026-08-04 | ✅ **MUERTA el 2026-08-14, al TERCER intento y esta vez con la corrida delante; vive ahora en `[D-077]`.** 60 llamadas reales a `claude-opus-5`: **0 por encima del corte de 6,5 s**, peor caso 3,91 s, mediana 2,88 s. Por la regla de tres con cero cortes en 60 muestras, la tasa no pasa del **5,0%**, que es exactamente el criterio fijado ANTES de gastar (`[D-074]`, corregido por `[D-075]`). 🔑 **Y el cierre es CONDICIONADO:** vale mientras Anthropic responda como el 2026-08-14 — si vuelve la saturación de `T-087`, la tanda se repite. Los dos cierres anteriores fallaron por colgarse de un techo inexistente (`[D-070]`, `[L-054]`) y de una medida que no medía la ruta entera (`[L-043]`) | — |
| ~~A-010~~ | 2026-08-04 | ✅ **RETIRADA el 2026-08-11: `T-079` la cerró entera; vive ahora en `[D-058]`.** Cruzada con dos instrumentos que no comparten fuente — consola de Anthropic (**$0,02** por las diez llamadas) y tokens medidos × precio de lista oficial (**$0,0234**): coinciden dentro del redondeo a céntimos. **$0,00234 por práctica ⇒ $0,047 al día ⇒ $8,44 en 180 días** por una persona a tope. 🚨 **Y el saldo son $6,55: NO cubre a una sola persona a tope durante la ventana — aguanta 140 días.** Decía antes: 🔻 **ENCOGIDA el 2026-08-11 con `T-079`: la mitad de los TOKENS está medida, la de los DÓLARES no.** Diez prácticas reales gastaron **247,2 tokens de entrada y 44,3 de salida de media** (entrada muy estable, 245–250: la rúbrica pesa casi todo; la salida varía 30–59 según si la frase tenía error). ⇒ 20 prácticas ≈ **4.944 de entrada + 886 de salida** por persona y día. 🚨 **Lo que sigue sin medir es lo que la suposición dice:** eso en dólares, y contra qué presupuesto. La regla 6 impide convertirlo aquí — el precio no se calcula de memoria. 🔍 **Cómo se cierra:** leer el gasto de esta corrida en la consola de Anthropic, que ya tiene los diez consumos dentro. Es acción del usuario y cuesta $0. **20 prácticas al día por persona es el tope correcto**: predicción, no número final | o frena a quien estudia de verdad, o deja pasar una factura que duele |
| A-007 | 2026-08-04 | Entre el Paso 2b del cierre y el `git add` no se toca ningún `.ts` | se comprueba un `.js` y se commitea otro: el control da verde sobre un archivo que ya no es el del commit |
| A-006 | 2026-08-03 | La ruta de `mktemp -d` de Git Bash le sirve a `node`, que es un binario de Windows | el control del `.js` del Paso 2b no compila nunca: siempre "SIN COMPROBAR" |
| A-002 | 2026-08-02 | El archivo de **una misma persona** lo escribe un solo proceso a la vez (🔻 encogida el 2026-08-03 por el paso 4) | el candado deja de servir y los puntos de esa persona se vuelven a perder |

---

## Entradas

### [A-030] 2026-08-14 — La báscula reusó la conexión y producción no, y se supone que da igual

- **Se supone que:** el veredicto VERDE de `[D-077]` vale para producción **aunque
  la báscula midiera con la conexión ya abierta y producción la abra en cada
  práctica**.

- 🚨 **El hueco, medido en el código:**

  ```
    measure_tutor.py:396   construye `inner` UNA vez y lo reusa en las 60
    app/tools.py:481       judge_grammar con client=None construye un
                           anthropic.Anthropic NUEVO en cada llamada
    app/english_tutor.py:86  llama judge_grammar SIN cliente  ← producción
  ```

  Consecuencia: producción paga **DNS + TCP + TLS en cada práctica**; la medición
  lo pagó **una vez de sesenta**. La fase `connect` —1,5 s de los 9,0 del
  cliente— se ejerció en **1 de 60** muestras.

- ✅ **Por qué no tumba el VERDE:** hay **2,6 s de holgura** (3,91 s contra un
  corte de 6,5) contra un apretón de manos que cuesta décimas. Para voltear el
  veredicto el handshake tendría que costar más que toda la holgura.

- ⚠️ **Por qué se anota igual.** El docstring de `measure_tutor.py` enumera lo
  que la báscula tiene idéntico a producción —*mismo modelo, mismo esfuerzo,
  misma rúbrica, mismos `max_retries`, misma función `judge_grammar`*— y **esa
  lista se lee como exhaustiva**. El ciclo de vida del cliente no está en ella.
  Es la forma exacta de `[L-043]`: la báscula parecía medir lo mismo y medía un
  poco menos. 📌 Y el proyecto ya sabía la mitad: `app/tools.py:182` dice que el
  SDK trae `keepalive_expiry=5.0`, así que **con tráfico esporádico casi cada
  llamada paga handshake nuevo** — que es justo el perfil de una app con pocos
  usuarios.

- 🔍 **Cómo se comprobaría, y cuesta dinero:** correr la báscula construyendo el
  cliente **dentro** del bucle, como hace producción, y comparar las dos
  distribuciones. **No se hace hoy** (regla 5: la holgura sobra por 2,6 s). Se
  reabre si alguna vez el peor caso se acerca al corte, o si se toca la
  reutilización de conexiones.

- **A raíz de:** `T-094`, hallazgo H-3 de la auditoría externa del 2026-08-14,
  comprobado aquí en las tres líneas citadas. Relacionado: `[D-077]`, `[L-043]`.

---

### [A-029] 2026-08-14 — El trabajo local cabe en 0,07 s, y ese 0,07 es `max(N)`

- **Se supone que:** el trabajo local de `respond()` —`count_words`,
  `judge_grammar` sin la red, `add_point` escribiendo en disco con candado— no
  pasa de **0,07 s** en el peor caso.

- **De dónde salió:** de redondear hacia arriba los **56,3 ms** de
  `measure_local_parts.py`, con 40 hilos peleando por el mismo archivo.

- 🚨 **Por qué es una suposición y no un dato: es `max(N)`.** Y no de forma
  teórica — el propio guion registra **seis** corridas, no las cinco que cita
  `app/api.py`:

  ```
    44,9 → 45,9 → 49,2 → 50,6 → 56,3 → 62,4 ms      +39%, y subiendo
  ```

  La sexta ya está en 62,4 ms. Sigue cabiendo en 0,07, pero **la serie no se ha
  estabilizado**: `max(N)` estima un cuantil que crece con N, no una cota. Es
  exactamente lo que `[L-058]` prohíbe para un número que decide algo.

- 🔑 **Por qué se usa igual, y esto es lo que hace que no sea temerario: el
  margen lo domina.** En el mínimo que exige el assert de `[D-076]`:

  ```
    hueco (ruta − cliente)  >=  LOCAL_WORK_SECONDS + SURRENDER_MARGIN_SECONDS
                                       70 ms       +        500 ms
  ```

  El margen es **unas 7 veces mayor**, y es una holgura **decidida**, no una
  medida. Un error de ±10 ms en la estimación no puede voltear el assert en
  ninguna configuración realista. **Quien decide el umbral no es el número
  flojo.**

  > 🚨 **Aquí se escribió primero *"el error cae del lado seguro"*, y no
  > aguanta.** Describe el sentido del error —subestimar produce **falsos
  > negativos**, deja pasar configuraciones malas—, y para un `read` eso es
  > benigno. Pero esto es un **guardián**, y en un guardián el falso negativo es
  > la dirección **peligrosa**: da un verde que no significa nada. El argumento
  > se cae en cuanto alguien lo copie a un guardián donde el margen no domine.
  > Corregido el 2026-08-14 por la auditoría externa, que lo sitúa en LM.13 del
  > repo supervisor (sin corchetes: desde aquí no se puede abrir esa entrada).

- ⚠️ **Lo que NO se puede hacer con él: tratarlo como medido.** Al meterlo en
  código deja de parecer una estimación, y el siguiente que lo lea lo usará como
  dato. Por eso está aquí y por eso el comentario de `app/tools.py` lo dice con
  todas las letras.

- 🔍 **Cómo se comprobaría:** un **percentil decidido ANTES** de medir (no
  `max`) sobre una tanda de `measure_local_parts.py` con la carga de 40 hilos —
  o, mejor, una forma que no dependa de medir, como la resta de `[D-073]`. El
  día que exista, se sube `LOCAL_WORK_SECONDS` y el assert aprieta solo.

- **Riesgo si es falsa:** el assert del hueco pasa con un margen que no da para
  el trabajo local real. El cliente deja de rendirse antes que la ruta, salta el
  504 de `api.py` y el error de verdad de Anthropic se queda escondido detrás —
  con `[D-051]` cobrando la práctica. Hoy no muerde: el hueco real es **1,0 s**,
  contra los 0,57 que se piden. El riesgo es de mañana, no de hoy.

---

<!-- [A-028] MUERTA el 2026-08-13, el mismo dia que nacio. Resulto CIERTA
     y se fue a `[D-069]`, con los tres numeros de la corrida real. -->

### [A-026] 2026-08-12 — Nadie va a correr el guion muchas veces seguidas

- **Se supone que:** `measure_tutor.py` se lanza de vez en cuando, no muchas
  veces seguidas en la misma sesión de trabajo.
- 🚨 **Por qué importa: es el único camino al saldo que no tiene ninguna capa
  encima.** Las dos que existen se lo dejan pasar, cada una por su motivo:

  | capa | qué corta | por qué NO corta esto |
  |---|---|---|
  | `CallBudget`, `[D-060]` | `$0,25` por corrida | **el monedero se reinicia en cada arranque** |
  | tope de $2 del espacio, `[D-062]` | gasto repartido en más de 2 h | 26 corridas seguidas son **79 min**: dentro de la ventana ciega de `[A-025]` |
  | freno de velocidad 50/min, `[D-061]` | concurrencia | la báscula es secuencial: 35/min, nunca lo toca |

- **La aritmética, con números ya medidos:** `$6,48 ÷ $0,25 = 26` corridas vacían
  el saldo; `26 × 106 llamadas × 1,72 s ≈ 79 minutos`. El mismo 79 que el del
  bucle roto — **por eso confunde**: parece que si una capa tapa uno, tapa el
  otro. No es así.
- ⚠️ **El paso 9 es el día de más riesgo, y no por accidente:** consiste en
  correr el guion una vez por modelo, comparar, repetir y reafinar el prompt. Esa
  forma de trabajar **es** la forma de las 26 corridas.
- 🔍 **Cómo se cerraría:** un monedero que **sobreviva al arranque** —contador
  persistido en disco en vez de reiniciado en cada corrida—, que es lo que
  convierte un tope *por corrida* en un tope *por día*. 📌 **No se construye
  hoy** (`[PI-2]`: nada lo ha pedido todavía, y `T-078` va antes). Se anota para
  que el día que muerda no llegue como sorpresa.
- **Si es falsa:** el saldo se vacía en ~79 minutos **sin que ninguna capa avise
  ni corte**, y `[C-008]` se cumple entera — la app sigue viva devolviendo 503
  mudo. Es el fallo silencioso, que es el peor de los dos.
- **De dónde salió:** la revisión de `[D-062]` en la sesión del 2026-08-12, al
  ver que la propia entrada afirmaba cortar este flanco y escribía al lado el
  número que lo desmentía.

### [A-025] 2026-08-11 — El tope de gasto por espacio de trabajo es blando y llega tarde

- **Se supone que:** en la consola de **primera parte** —la que usa el proyecto—
  el tope de gasto de un espacio de trabajo es **blando** (avisa, no corta) y
  tarda **unas dos horas** en reflejar el gasto reciente.
- 🚨 **De dónde sale la frase, que es el problema.** Está leída literal, pero en
  la página de **Claude Platform on AWS**, que es otro producto:

  > *"The spend limits you set are **soft limits**: spend is calculated at list
  > prices and can take **about two hours** to reflect recent usage."*

  La página de espacios de trabajo de primera parte describe el tope
  (*"Cap monthly spending for a workspace"*) y **no dice nada** de cómo se hace
  cumplir. Se está extendiendo una frase de un producto al otro. Puede ser
  cierto —el mecanismo de facturación es el mismo— pero **no está comprobado**.
- **Por qué se escribe aparte de `[D-059]` y no dentro:** es la razón por la que
  ahí se eligió el corte duro en el guion en vez de fiarse del tope. Una razón
  sin comprobar metida en el cuerpo de una decisión se lee como comprobada.
- ⚖️ **Y `[D-059]` no depende de ella, conviene decirlo entero.** Aunque el tope
  resultara duro e inmediato, la decisión sigue en pie: **ningún tope reparte el
  saldo**, y el saldo compartido es el fallo. Lo que cambiaría es el papel de la
  capa 2 — de "contabilidad y velocidad" pasaría a "freno de verdad".
- ⏱️ **El número que la hace importar:** `measure_tutor.py` hizo diez llamadas en
  **menos de un minuto** (`T-079`). Un tope que reacciona en dos horas llega 119
  minutos tarde. A esa escala, blando o duro da igual: no le da tiempo.
- 🔍 **Cómo se comprobaría:** en la consola, **Settings → Workspaces**, abrir la
  pestaña **Spend limits** de un espacio de trabajo y leer lo que dice la propia
  pantalla: si aparece la palabra `soft`, si habla de **alertas por umbral** en
  vez de corte, o si menciona algún retraso. Acción del usuario — el navegador lo
  toca él (regla 1). No es urgente: nada de hoy depende del resultado.
- 🔍 **COMPROBADO el 2026-08-12 — y la pantalla salió MUDA. Sigue en pie.** Se
  abrió `Settings → Workspaces → Spend limits` tal como decía el punto anterior.
  Lo único que dice la pantalla es:

  > *"El límite de gastos mensual de tu organización es de $500,00. Puedes
  > establecer un límite de gastos inferior a esta cantidad para este espacio de
  > trabajo."*

  **Ni `soft`, ni umbrales, ni retraso.** La consola de primera parte no se
  pronuncia sobre cómo se hace cumplir el tope. 🔑 **Salir muda no es salir
  falsa:** la suposición **no asciende** ni a `decisions.md` ni a `lessons.md`,
  se queda aquí. Lo que sí quedó decidido es cómo se actúa mientras siga sin
  comprobarse — por su **rama pesimista**: lo que no se puede comprobar no cuenta
  como freno. Ver `[D-062]`, que puso el tope de `$2,00` como reserva y
  contabilidad, nunca como protección.
- **Si es falsa:** en la dirección buena, no se rompe nada — el corte duro de
  `[D-059]` está puesto justo para el caso peor, así que sobra protección.

  > 🚨 **El daño está en leerla al revés.** Si alguien concluye "hay tope por
  > espacio, luego estamos protegidos" y quita el corte duro del guion, se queda
  > **sin ninguna capa** sobre el saldo compartido. Ese es exactamente `[C-008]`.

### [A-023] 2026-08-10 — Aplazar `T-069` hasta después del paso 8 no lo encarece

- **Se supone que:** el ensayo de reconstrucción cuesta lo mismo dentro de unas
  semanas que hoy, y que `deploy/` seguirá levantando TEAPP igual.
- **Por qué está escrita aparte y no dentro de `[D-048]`:** es el **precio** que
  esa decisión acepta. Una decisión que se lleva su propio riesgo dentro del
  cuerpo lo esconde; separado, se puede vigilar y se puede matar.
- 🚨 **La pata floja está identificada, y no es la que parece.** No es que
  `deploy/` se estropee solo — es que **el paso 8 va a tocarlo**. La API key
  tiene que llegar al servidor sin pasar por el navegador (regla 1) ni por el
  código (regla 7): entra por el archivo de entorno, y `install.sh` tendrá que
  colocarla.

  > 🔑 **Lo que se ensaye en septiembre no será el `deploy/` de hoy.** Será uno
  > con una pieza nueva y sin estrenar dentro, y justo la que guarda el secreto.

- ⚖️ **Y eso corta en las dos direcciones, así que se escribe entero:** también
  es un **argumento a favor de esperar**, porque un ensayo hecho hoy dejaría sin
  probar precisamente esa pieza, y habría que repetirlo. Lo que no vale es
  cruzar creyendo que la fecha da igual.
- **Cómo se comprobaría:** corriendo `T-069` tal como está escrita en el Paso 5c
  de `deploy/console_steps.md` — el guion ya existe, no hay que volver a
  pensarlo. **Fecha tope ≈ 2026-09-01**, el cierre del primer ciclo de
  facturación: es cuando `[A-018]` deja de estar ciega y ya hay motivo para
  volver a la consola.
- ⏳ **El reloj que no se negocia:** `[C-006]` — la cuenta muere el 2027-02-06.
- **Si es falsa:** se descubre que `deploy/` no levanta **más tarde y con menos
  margen**, que es el escenario exacto del que `[D-030]` quería escapar. Y en el
  peor caso el fallo sale en la pieza de la llave, mezclado con el estreno del
  modelo: **dos sospechosos en vez de uno** — el error que el orden del roadmap
  entero existe para evitar.

### [A-022] 2026-08-09 — `OnCalendar` aceptará la zona horaria en cualquier máquina

**Qué se está dando por cierto.** Que `OnCalendar=*-*-* 23:00:00 UTC` funciona,
no solo en la máquina de hoy, sino en la que se levante cuando haya que
reconstruir.

**Por qué importa tanto.** Es **la decisión central de `[D-046]`**. `cron` se
descartó justamente porque lee la hora en la zona de la máquina; el argumento
entero era que systemd deja escribir la zona dentro de la línea, y así **la hora
viaja con la pieza**. Si esa capacidad no está, no es que la pieza quede peor
que `cron`: es que el motivo para elegirla desaparece.

**⚠️ De qué depende.** Del **soporte de zona horaria en `OnCalendar`**, que
depende de la versión de systemd. Y `install.sh` existe por `C-004`: la cuenta se
cierra a los seis meses y esto se vuelve a correr en una máquina nueva, quizá con
otra imagen. En una systemd más vieja, ese `UTC` sería un error de sintaxis.

**📌 Lo que hoy NO cubre nada.** `install.sh` comprueba que el temporizador quede
`active` y `enabled` —y desde `[L-034]`, las dos cosas—, pero **ninguna de las
dos mira cómo se interpretó la hora**. Un temporizador puede estar
perfectamente armado apuntando a la hora equivocada.

**🔍 Cómo se comprueba, y es gratis.** En la máquina:

```bash
systemd-analyze calendar '*-*-* 23:00:00 UTC'
```

Imprime cómo entiende systemd esa línea y cuándo dispararía. Si contesta
`Next elapse: … 23:00:00 UTC`, la pieza dice lo que se cree que dice —
demostrado, no supuesto.

**🧪 Se mide dos veces, y la segunda es la que vale.** Ahora en la máquina de
hoy, que cierra el caso presente. Y **otra vez en `T-069`**, el ensayo de
reconstrucción, que es donde de verdad mordería — ahí la máquina es nueva y
puede no ser la misma imagen.

**🔻 Primera mitad MEDIDA — 2026-08-10, máquina viva.**

```
$ systemctl --version | head -1
systemd 255 (255.4-1ubuntu8.16)

$ systemd-analyze calendar "*-*-* 23:00:00 UTC"
Normalized form: *-*-* 23:00:00 UTC
    Next elapse: Mon 2026-08-10 23:00:00 UTC
       From now: 8h left
```

Los dos modos de fallo que temía la entrada quedan descartados **en esta
versión**: no hubo error de sintaxis, y la forma normalizada **conserva el
`UTC`** en vez de tragárselo. Esa segunda línea es la que importa: una systemd
que ignorara la zona habría contestado sin ella, y el temporizador estaría
armado apuntando cinco horas más allá sin un solo mensaje de error.

**⚠️ Pero la suposición NO se cierra, y conviene ver por qué.** Lo que dice no es
*"funciona aquí"*, es *"funciona en cualquier máquina donde se reconstruya"*.
Medir la máquina de hoy responde una pregunta que hoy ya no corría riesgo —el
temporizador de anoche disparó, luego la línea servía— y deja intacta la que sí
muerde: **cuál es la versión mínima de systemd que entiende la zona**. Eso solo
lo contesta `T-069` sobre una imagen nueva.

🔑 Lo que cambia es el **tamaño** del riesgo, no su existencia. Antes: *"puede
que esta línea no funcione en ningún sitio"*. Ahora: *"funciona en systemd 255;
falta el suelo"*. Una suposición encogida sigue siendo una suposición.

📌 Nace de una revisión externa el 2026-08-09, la misma que produjo `[L-034]`.
🔑 Se escribe en vez de resolverse de memoria porque una versión de systemd
recordada es exactamente el número que la regla 6 prohíbe.

---

### [A-021] 2026-08-06 — La tarjeta que sobrevive a su cuenta no hace daño hoy

- **Se supone que:** que una sesión firmada siga valiendo aunque su cuenta ya no
  esté en `data/accounts.json` **no tiene consecuencia en la v1**.

- **El mecanismo NO se supone: está medido.** Corrida del 2026-08-06, con los tres
  desvíos puestos y el portero de `no_data_writes.py` delante (`data/` real sin
  cambios):

  | paso | resultado |
  |---|---|
  | `POST /register` de `efimero` | `201` |
  | `POST /practice` con la cuenta puesta | `200` |
  | se borra `efimero` del almacén, la cookie se deja intacta | quedan 0 cuentas |
  | `POST /practice` **sin cuenta** | 🚨 `200`, `score: 2` |
  | `GET /me` **sin cuenta** | 🚨 `200`, `{"user": "efimero"}` |

  La causa está a la vista en el código: `_current_user` (`app/api.py:300`) llama
  a `sessions.read`, que comprueba **firma, caducidad y forma del nombre** — y
  nada más. Nadie vuelve a mirar `accounts.json` después del login.

- **Lo que se está dando por cierto es lo OTRO: que no importa.** Se apoya en dos
  patas, y las dos hay que vigilar:
  1. **La v1 no sabe borrar cuentas.** No hay ninguna ruta que lo haga, así que
     hoy no existe el escenario "cuenta borrada, sesión viva" salvo editando el
     archivo a mano.
  2. **Firmar exige la llave**, que vive en el servidor y no sale de ahí (regla 1
     del proyecto). Sin llave no se fabrica una tarjeta para un nombre inventado.

- **Cómo se comprobaría / cuándo se muere:** esta suposición se cae sola el día
  que aparezca el borrado de cuentas, o cualquier necesidad de echar a alguien
  antes de sus 7 días. Ahí la pregunta deja de ser teórica y hay que decidir si
  `_current_user` consulta el almacén —una lectura de archivo por petición— o si
  se sostiene con la caducidad y ya está.

- 📌 **De dónde viene, porque importa.** Nació de una deducción **equivocada**: se
  dedujo de la cuenta ausente de `[L-023]` que alguien se había firmado su propia
  cookie, y no fue eso lo que pasó — el script se registró, en un archivo
  desviado. La lectura del código era correcta por su cuenta, así que se
  **re-verificó con la corrida de arriba** antes de escribir esto. La regla que
  deja: una prueba que resulta significar otra cosa no refuta la conclusión, pero
  la deja **sin sostén** hasta que se mide aparte.

- **Si es falsa** (si sí hiciera daño hoy): lo que se rompe no es la puerta —para
  entrar sigue haciendo falta la llave del servidor— sino la **revocación
  selectiva**. Y cada `/practice` con una tarjeta así **crea marcador y cuota de un
  fantasma** en `data/`, que es exactamente la clase de archivo huérfano que abrió
  `T-072`.

- 🔨 **La palanca que SÍ existe, y conviene saberla antes de necesitarla.** Cortar
  sesiones no es imposible: **cambiar `TEAPP_SECRET_KEY` las invalida todas de
  golpe**, porque una firma hecha con otra llave deja de cuadrar (`[L-032]` —antes `[A-008]`—, y está
  escrito en `.env.example`). Es tosca —echa a todo el mundo, no a uno— pero es
  inmediata y no necesita código nuevo.

  🚨 **Y por eso importa en el paso 7:** la pata sobre la que se apoya esta
  suposición es que la llave no sale del servidor. El día que se filtre, la
  respuesta es rotar la llave, y `install.sh` está escrito **para NO tocar el
  `.env` si ya existe** — regenerar a mano tira fuera a todo el mundo, que es
  justo lo que se quiere en ese momento y un desastre en cualquier otro. Saber
  cuál de los dos casos es se decide antes, no con el incendio encima.

### [A-018] 2026-08-06 — La alarma avisará el día que haga falta

- **Qué se da por cierto:** que la alarma está bien montada. Probablemente lo
  esté. **Nadie lo sabe**, porque nunca ha saltado.
- **Por qué no se puede comprobar barato:** para verla en rojo hay que gastar
  dinero de verdad y esperar a que el dato de facturación aparezca (~24 h,
  `deploy/console_steps.md` paso 5). No hay ensayo gratis.
- 🚨 **Lo que la alarma NO cubre, y es lo más importante de esta entrada:**

  | qué puede pasar | ¿avisa a tiempo? |
  |---|---|
  | máquina encendida y olvidada, goteando | ✅ sí — 24 h de retraso no importan |
  | cruzar una de las 7 puertas de `[C-005]` | ❌ **no.** Los créditos se evaporan *en el acto* |

  → Contra el acantilado **no hay aviso posible**: cuando llegue el correo, ya
  pasó ayer. El único freno que corre a la velocidad de ese riesgo es papel:
  la lista de `T-068`. **T-068 deja de ser papeleo y pasa a ser el freno.**
- ✅ **Cómo se cierra esta suposición — corregido el 2026-08-06, segunda
  auditoría.** Decía: *"el día que aparezca el primer cargo real"*. **Eso era
  esperar sentado, y encima destruía el experimento.**

  **Se cierra bajando el listón, no subiendo el riesgo:** se crea un presupuesto
  **de prueba** con el umbral **por debajo de lo ya gastado**. Dispara solo en el
  siguiente ciclo de evaluación y **el correo llega de verdad**. Prueba las tres
  cosas que importan a la vez: que la dirección es correcta, que no cae en spam,
  y que el mecanismo anda. Después se borra el presupuesto de prueba.

  🔑 **Es el sabotaje de `[S-013]`, aplicado a una alarma en vez de a una
  función.** Mismo gesto que poner el vigilante de la cuota en 15 y verlo rojo:
  un control que nunca se ha visto morder no es un control, es un adorno.
  Y de paso se mide **cuánto tardó** — ahí el "~24 h" deja de ser documentación.
- 🚨 **Y lo que se creía criterio de cierre era su contrario.** Estaba escrito que
  el silencio tras `T-059` confirmaría la alarma. **El silencio no demuestra
  nunca que un control funcione:** no llega correo si está bien, y tampoco si el
  correo está mal escrito, si la alarma se borró, o si el umbral no puede
  alcanzarse. Es `[LM.13]` en versión alarma — verde porque **no existe nada
  capaz de ponerlo rojo**.
- ⏳ **Y hay una calibración GRATIS que caduca:** hoy, con cero máquinas
  encendidas, el silencio de la alarma **significa algo** — si suena, hay algo
  que no sabemos. En cuanto exista la EC2 de `T-059`, ese silencio deja de
  distinguir "no hay gasto" de "la alarma está mal montada". Es ahora o no es.

#### 🔻 Encogida el 2026-08-06 — se añadió la alerta de coste previsto

- **Qué cambió:** el mismo presupuesto lleva ahora **dos** alertas, `Real` y
  `Previsto`, las dos a 0,01 US$ **absoluto**, al mismo correo. Guardado y visto
  en pantalla. El detalle y el porqué, en `deploy/console_steps.md` paso 1.
- **Qué encoge de la suposición:** solo la mitad del **goteo**. La alerta prevista
  proyecta, así que no espera a que el cargo exista y recorta el retraso de ~24 h.
- 🚨 **Qué NO encoge, y sigue igual de abierto:** el **acantilado**. La tabla de
  arriba no cambia ni una casilla. Contra las 7 puertas de `[C-005]` no hay
  predicción posible — no hay tendencia que proyectar, pasa de golpe. **El freno
  sigue siendo `T-068`.**
- ❓ **Sin verificar, y nace hoy:** que AWS pueda **proyectar algo sin historial**.
  La cuenta se abrió el 2026-08-06 y no tiene gasto previo. No se encontró en la
  documentación cuánto tarda la previsión en dar un número. Se ve en pantalla.

#### ❓ Suposición hermana — los créditos descuentan del cálculo

- **Qué se da por cierto:** que los $200 en créditos **descuentan** del coste que
  mide el presupuesto, y por tanto que la EC2 de `T-059`, mientras la paguen los
  créditos, **no** hará saltar la alarma.
- **De dónde sale:** de la documentación de la API — `IncludeCredit` *"Defaults to
  `true`"* (`API_budgets_CostTypes`, consultado 2026-08-06). El desplegable
  `Costes agregados por` se dejó en su valor por defecto, *costes sin combinar*.
- 🚨 **Por qué importa más de lo que parece:** si fuera falsa, la alarma saltaría
  **todos los días** en cuanto la máquina lleve horas encendida, aun estando todo
  pagado por los créditos. Y una alarma que suena siempre **se deja de mirar**:
  pasaría de control a ruido, que es peor que no tenerla, porque da falsa calma.
- ✅ **Cómo se comprueba — corregido el 2026-08-06, segunda auditoría.** Decía
  *"silencio = confirmada"*. **Falso, y por partida doble:** el silencio no
  confirma nada (ver arriba), y además aquí el silencio estaría **garantizado**
  si la métrica fuera neta, porque los créditos dejarían el coste en $0.00.

  **Se comprueba MIRANDO**, no esperando: se abre el presupuesto y se lee el
  valor literal del campo que dice qué mide — `UNBLENDED_COST` (bruto) frente a
  `NET_UNBLENDED_COST` (neto, después de créditos). Treinta segundos, cero gasto.
- ❗ **Y hay una contradicción sin resolver, por eso hay que mirar.** La auditoría
  del 2026-08-06 afirma que el valor por defecto es `NET_UNBLENDED_COST`. Pero la
  **pantalla** de ese mismo día mostró **"costes sin combinar"** —la opción
  bruta—, con "costes netos sin combinar" existiendo aparte y **sin** seleccionar.
  Las dos fuentes no coinciden y ninguna se impone sobre la otra desde el
  escritorio. **Gana la pantalla, el día que se lea.**
- 🚨 **Lo que está en juego, y es más grande de lo que parecía:** si mide **neto**,
  la alarma no vigila el goteo **en absoluto**. Una máquina encendida y olvidada
  quemaría los $200 en silencio durante meses, y el primer correo llegaría el día
  en que ya no quedara nada que salvar. La tabla de esta entrada tendría que
  cambiar: pasaría de "✅ sí" a "❌ no" también en la fila del goteo, y `[A-015]`
  —"del orden de $50", aritmética de lista de precios, **no una corrida**— se
  quedaría como única defensa, sin nadie vigilándola.
#### ✅ RESUELTO el 2026-08-06 — mide BRUTO. Leído en pantalla

- **`Costes agregados por` = "costes sin combinar"** = `UNBLENDED_COST`. La opción
  "costes netos sin combinar" existía **aparte y sin seleccionar**.
- **Ganó la pantalla.** La auditoría afirmaba `NET_UNBLENDED_COST` como valor por
  defecto; resultó ser un **ejemplo** de la documentación de la API con ese valor
  dentro. 🔑 **Un ejemplo no es un valor por defecto** — y venía presentado como
  hecho verificado, con bloque de código, que es lo que lo hizo creíble.
- **Consecuencia buena:** los créditos **no** enmascaran el gasto. La alarma sí
  puede ver el goteo. **No hace falta el segundo presupuesto** que se planteaba
  abajo.
- **Consecuencia nueva:** si mide bruto, la EC2 encendida genera coste bruto
  aunque los créditos lo paguen — y con umbral de $0.01, **la alarma tiene que
  sonar**. Eso convierte el experimento en falsable.

#### 🧪 EL EXPERIMENTO — escrito ANTES de mirar. No se toca al leer el resultado

**Disparador: reservar SOLO la Elastic IP.** Nada más — ni instancia, ni sistema
operativo. La documentación dice que cobra *"regardless of whether they are in use
… or **idle**"* (`AWSEC2/latest/UserGuide/elastic-ip-addresses-eip`), y la IP hace
falta para `T-059` de todos modos. Es el suelo mínimo imprescindible.

🚨 **Son DOS observaciones, no una.** Separan *"¿mi control está bien?"* de
*"¿el mundo está como creo?"*:

| | qué se mira | qué es |
|---|---|---|
| **Obs. 1** | ¿hubo coste bruto? → **la factura / resumen de costes** | la **premisa** |
| **Obs. 2** | ¿llegó el correo? → **la bandeja** | la **prueba** |

**Tabla de lectura:**

| coste bruto | correo | veredicto |
|---|---|---|
| > $0.01 | ✉️ llega | ✅ **`A-018` CERRADA.** Y se mide **cuánto tardó**: el "~24 h" deja de ser documentación |
| > $0.01 | 🔇 silencio | 🚨 **LA ALARMA ESTÁ ROTA.** Hallazgo grande, y a tiempo — todavía no hay nada que perder |
| = $0.00 | (da igual) | ❓ **No concluyente.** Aplican las *"750 hours of public IPv4 at no cost"*, lenguaje del plan viejo → `[C-003]` queda tocada. Se aprende algo que hoy nadie sabe |

⚠️ **Sin la Observación 1, el tercer caso se disfraza del segundo** y se saca la
conclusión contraria: se leería "alarma rota" donde solo hay "no hubo cargo".

📌 **Y el experimento mide una cosa más, gratis:** si llega **un** correo o **uno
cada día**. Ver el punto siguiente.

#### 🟢 EXPERIMENTO LANZADO — 2026-08-06, 15:29 UTC (10:29 local)

- **Qué se hizo:** se reservó **una Elastic IP** en `us-east-1` (`[D-033]`).
  **Nada más** — sin instancia, sin asociarla a nada. Es el suelo mínimo capaz de
  hacer sonar la alarma.
- **Estado de la cuenta en ese momento:** gasto acumulado **$0.00**, cero
  recursos. La IP es lo primero y lo único que existe.
- ⏱️ **Esa marca de tiempo es el `t=0` del experimento.** Sin ella no se puede
  medir el retraso, y medirlo es la mitad del valor: convierte el "~24 h" de
  documentación en un número propio.
- 📌 **Lo que NO se anota aquí:** la dirección IP concreta. No hace falta para
  nada de lo escrito, y el repo es público.
- ⏳ **Ahora se espera y se mira la tabla de arriba.** Las **dos** observaciones,
  no una: la factura *y* la bandeja.
- 🚨 **Mientras dure el experimento, esa IP es exactamente el "goteo" del que
  habla esta entrada:** un recurso reservado, sin usar, cobrando por existir. Es
  deliberado y es barato, pero **tiene que soltarse o asociarse** cuando el
  experimento termine. Si esto se queda aquí olvidado, la entrada que avisaba del
  goteo lo habrá causado.

#### 🔴 CORREGIDO — "va a sonar todos los días durante seis meses"

- **Esa frase la afirmé yo el 2026-08-06, y no está comprobada.** Sostenía que
  había que subir el umbral ya. La documentación de AWS confirma el retraso de
  notificación, pero **no dice** si una alerta se repite mientras el umbral siga
  superado o si suena una vez por período. **No lo sé.**
- 🚨 **Por eso el umbral NO se toca todavía.** Cambiarlo ahora arreglaría un
  problema **predicho** y destruiría el único experimento capaz de confirmar que
  existe. Es el mismo error del "silencio confirma" con el signo cambiado:
  **actuar sobre un razonamiento cuando había una observación disponible.**

#### 📐 De dónde saldrá el umbral definitivo — anotado hoy, se aplica DESPUÉS

- **$0.01 es el umbral correcto para PROBAR la alarma y el equivocado para VIVIR
  con ella.** Eso se mantiene, suene una vez o cien.
- **El número que lo sustituya no es un gusto, sale de una división:**
  $200 ÷ 6 meses ≈ **$33 al mes**. Un presupuesto mensual por ahí convierte la
  alarma en lo único que hoy no existe: **un vigilante del ritmo de quema**.
- 🔑 **Ese es exactamente el riesgo de `[A-015]`** —"del orden de $50", aritmética
  de lista de precios, **sin corrida**— y hoy **no lo mira nadie**.
- ⏳ Se decide **después** del correo, con el dato de si repite o no.

#### 🔻 Descartado — el segundo presupuesto sobre coste bruto

- 🔧 **Si resulta ser neto:** un **segundo** presupuesto sobre coste **bruto**
  (créditos excluidos) con umbral bajo. Salta con el primer dólar real, lo pague
  quien lo pague. Ese es el detector del goteo, que hoy no existe.
  📌 Serían **dos presupuestos y no uno**, y el porqué hay que dejarlo escrito
  para que en tres meses no parezca duplicado: **uno vigila el bolsillo, el otro
  vigila los créditos.** Son dos preguntas distintas con el mismo aspecto.

#### ⏳ Primera lectura — 2026-08-07, ~20 h después de `t=0`. NO CONCLUYENTE

**Obs. 2 (la bandeja): silencio.** Ningún correo. **Obs. 1 (la factura): no hay
dato todavía.** Y sin la Observación 1 no se lee nada — es exactamente el aviso
escrito arriba, funcionando: el silencio de la bandeja, solo, no distingue
"alarma rota" de "no hubo cargo".

Lo que mostraron las dos pantallas, literal:

| pantalla | qué dijo |
|---|---|
| *Administración de facturación y costos* | *"Estamos preparando sus datos de costos y uso. Este proceso puede tardar hasta 24 horas **después de que visite por primera vez la consola**"* |
| *Facturas*, período agosto 2026 | *"Sin datos. No hay datos para mostrar."* · Total general estimado: **0,00 USD** |

🚨 **Ese `0,00 USD` NO es la tercera fila de la tabla.** Es un total sobre **cero
renglones**, y un total de cero renglones siempre da cero. La tabla de lectura
tiene tres filas, pero existe un **cuarto estado —"aún no hay dato"— que se
disfraza de `= $0.00`**. Confundirlos habría cerrado el experimento con la
conclusión contraria. Se distinguen por el desglose: si hay servicios y fechas y
la IP no sale, eso es dato; si dice "sin datos", es que no hay nada escrito aún.

🔑 **Son DOS relojes distintos, y la entrada solo tenía escrito uno.**
Suponía ~24 h **desde el gasto**. La pantalla dice hasta 24 h **desde la primera
visita a la consola de facturación**. El `t=0` del **gasto** sigue siendo
2026-08-06 15:29 UTC —ese no cambia y es el que mide el retraso de la alarma—;
el otro reloj arranca en la primera visita a la consola, que fue el **2026-08-06
durante el día**, al crear el presupuesto del paso 1.

⚠️ **Corregido el mismo día: primero se escribió aquí que esa primera visita fue
el 2026-08-07. Era una deducción, no un dato, y estaba mal.** La lectura del
2026-08-07 se hizo a las 7:33 GMT-5 (12:33 UTC), o sea **antes** de cumplirse
24 h desde la tarde del 06. Dentro de plazo por las dos cuentas.

🔑 **Y ninguna de esas cuentas manda, porque "hasta 24 horas" es un techo, no una
promesa** — dice *hasta*, no *a las*. Lo que decide es que la pantalla informa de
su propio estado: *"estamos preparando sus datos"*. **Gana la pantalla**, otra
vez. El criterio para volver a leer no es un reloj: es que ese mensaje
desaparezca. Próxima lectura: 2026-08-08.

- ❓ **Encoge la pregunta hermana de la alerta prevista** (¿puede AWS proyectar
  sin historial?): la misma pantalla promete *"los costos previstos"* **para
  cuando los datos estén listos**. Así que hoy la alerta de coste previsto no
  puede haber disparado por falta de materia prima, no por estar mal montada.
  No la cierra —sigue sin verse funcionar—, pero explica su silencio.
- 📌 **Tampoco se anota aquí el ID de cuenta**, por lo mismo que la dirección IP:
  no hace falta para nada de lo escrito y el repo es público.
- ⚠️ **La Elastic IP sigue reservada y ociosa** mientras dure esto. El aviso de
  arriba sigue vigente: hay que soltarla o asociarla al terminar.

##### 🚨 El dólar de la tarjeta NO es el cargo del experimento. No buscarlo en la factura

AWS anunció al abrir la cuenta un movimiento de **1 US$** que nunca apareció en
el banco. **No es un cobro: es una autorización de verificación de tarjeta** —se
pide permiso por un importe pequeño y se libera. Que no se vea es lo esperado;
muchos bancos ni muestran una autorización que se revierte.

**Por qué queda escrito aquí, en el experimento, y no en otro sitio:** porque es
un **tercer reloj** que se puede confundir con los otros dos, y confundirlo
rompería la lectura de mañana.

| reloj | entre quién | qué mide |
|---|---|---|
| gasto de la Elastic IP | AWS ↔ el experimento | `t=0` 2026-08-06 15:29 UTC, mide el retraso de la alarma |
| preparación de datos de coste | cocina interna de AWS | *"hasta 24 h"*, se acaba cuando el mensaje desaparece |
| el dólar de verificación | AWS ↔ el banco | nada del experimento. Coincidió en el tiempo, nada más |

🔑 **Consecuencia operativa:** ese dólar **no va a aparecer nunca en la factura**,
porque no es un cargo. Si mañana se busca ahí y no está, eso **no** significa
"no hubo coste" — significa que se está mirando la cosa equivocada. Es el mismo
error del que salvó la Observación 1, con otro disfraz.

❓ **Sin verificar:** todo esto se escribió de memoria; la consulta a `ctx7` falló
por red el 2026-08-07. Lo que sí está observado: la cuenta abrió y la Elastic IP
se reservó, así que la tarjeta **quedó aceptada** — una verificación fallida deja
el método de pago marcado como inválido, no en silencio.

#### ⏳ Segunda lectura — 2026-08-07, 14:36 UTC (~23,1 h desde `t=0`). SIGUE NO CONCLUYENTE

**El mensaje *"estamos preparando sus datos de costos y uso" desapareció.*** Ese era
el criterio escrito para volver a leer, así que se leyó. Resultado: **el criterio
era insuficiente.**

| pantalla | qué dijo | qué vale |
|---|---|---|
| *Facturas*, agosto 2026 | *"Sin datos"* · Total general estimado **0,00 USD** | ❌ **nada.** Ver abajo |
| *Presupuestos* → `My Zero-Spend Budget` | Presupuesto 1,00 US$ · **Importe utilizado 0,00 US$** · **0.00%** · *En buen estado* | ✅ es la lectura buena |
| *Presupuestos* → mismo | **Importe previsto: `-`** | ✅ resuelve una pregunta abierta |
| la bandeja | silencio | sin premisa, ilegible |

🚨 **`Facturas` era la ventana equivocada, y se fue a ella dos días seguidos.** Una
factura **nace cuando el mes cierra**. Estamos a 7 de agosto: ahí no va a haber
nada hasta septiembre, desaparezca el mensaje o no. El *"sin datos"* de esa
pantalla no es información sobre el experimento — es información sobre el
calendario.

✅ **La pantalla correcta es el propio presupuesto, y por un motivo que vale más
que la comodidad: es el MISMO instrumento que la alarma.** Leer el gasto con una
regla distinta y suponer que ambas coinciden es meter una suposición nueva dentro
del experimento que iba a matar suposiciones. El campo *Importe utilizado* es
literalmente el número que se compara contra el umbral.

📌 **Y ahí el cero sí es un cero calculado**, no una ausencia: viene con un `0.00%`
y un veredicto *En buen estado*. Un porcentaje solo existe si hubo división. Eso
distingue por fin el cuarto estado del tercero… **pero no cierra nada**, porque
sigue faltando saber si el dato de coste ya llegó a esa cifra.

##### ✅ Resuelto de paso, gratis: AWS NO puede proyectar sin historial

**Importe previsto: `-`.** Leído en pantalla. La pregunta nacida el 2026-08-06
—*"¿puede AWS proyectar algo sin historial?"*— tiene respuesta: **no, y lo dice
con un guion, no con un cero.** Consecuencia: la alerta de **coste previsto** no
puede haber disparado, y su silencio no es prueba de nada. Queda una sola alerta
en juego, la de coste **real**.

##### 🔴 CORREGIDO EN CALIENTE — se estuvo a punto de cerrar con la fila 3, y era falso

Al ver el `0,00 US$` se dijo *"tercera fila: no concluyente porque aplican las 750
horas gratis de IPv4"*. **Se comprobó en la documentación antes de escribirlo, y
dice lo contrario:**

> *"There is a charge for all Elastic IP addresses whether they are in use … or
> **idle** (created in your account but unallocated)."*
> — `AWSEC2/latest/UserGuide/elastic-ip-addresses-eip`, consultado 2026-08-07

Y sobre el plan gratuito, el anuncio de febrero de 2024: las **750 horas** son
*"public IPv4 address usage per month free **when launching any EC2 instance with
a public IPv4 address**"*. 🔑 **El beneficio es para direcciones EN USO.** La
nuestra está **ociosa** — sin instancia, deliberadamente. **No la cubre.**

🔑 **Eso invierte el signo de la lectura.** La fila 3 decía "la IP no cobró, no se
aprende nada". Con la documentación delante, la IP **sí tiene que estar cobrando**:
~23 h × 0,005 US$/h ≈ **0,115 US$ de coste bruto**, más de **10 veces** el umbral
de 0,01 US$. El disparador es válido y el experimento **sigue siendo falsable**,
que era justo lo que se temía haber perdido.

⚠️ **Ese ≈0,115 US$ es aritmética de lista de precios, no una corrida** — el mismo
defecto que `[A-015]`. Sirve para saber que el umbral se supera con holgura, no
como cifra final. **La corrida es precisamente lo que estamos esperando.**

##### 📅 Qué queda pendiente, y con qué criterio se lee ahora

**Estamos a ~23,1 h de un retraso documentado de "hasta 24 h": el borde exacto.**
Leer aquí no distingue "el pipeline no ha escrito todavía" de "algo va mal". Por
eso **no se toca el umbral, no se suelta la IP y no se concluye nada hoy.**

🔑 **Y el criterio de relectura cambia, porque el de ayer ya falló una vez.** No es
"que desaparezca un mensaje" —eso ya pasó y no bastó—: es **que el campo *Importe
utilizado* del presupuesto deje de ser 0,00**. Próxima lectura: **2026-08-08**.

⚠️ **La ventana de "32 h" que se escribió aquí primero queda RETIRADA** — la
enmienda de más abajo la sustituye con dos retrasos en serie y un número sacado
de la documentación, no del dedo. **La tabla vigente es la de la enmienda.**

##### 🚨 ENMIENDA SELLADA 2026-08-07 — la FILA 3 de la tabla original queda ANULADA

⚠️ **No se borra. Se anula y se deja a la vista**, porque la tabla original está en
el commit `cfba50a` y quien la lea mañana la leerá con autoridad — para eso se
selló. Una tabla superada en silencio es peor que una tabla equivocada.

**Fila 3 original:** *"coste = $0.00 → No concluyente. Aplican las 750 hours of
public IPv4 at no cost"*.

🔴 **Su CAUSA está desmentida** por la comprobación de hoy: esas horas son para
direcciones **en uso**; una IP **ociosa** cobra siempre. La fila nombraba una
explicación que ahora se sabe **falsa**.

🔑 **Y es la fila que más probablemente salga mañana.** Ahí estaba el peligro: no
en el dato nuevo, sino en el **papel viejo**. Ayer se auditó si el `0,00` se
disfrazaba de la fila 3; **nadie auditó si la fila 3 seguía siendo verdad.**

**Texto que la sustituye, sellado HOY, antes de mirar nada:**

> **`Importe utilizado` = 0,00 con holgura suficiente NO significa "es gratis".**
> Quedan **dos causas vivas** y hay que distinguirlas antes de concluir:
> - **(a)** el dato de coste aún no ha aterrizado → **seguir esperando**, no es veredicto
> - **(b)** algo absorbe el cargo por una vía que no conocemos → **hallazgo**, nace suposición nueva
>
> ❌ **Los créditos ya están descartados como causa (b):** el presupuesto mide
> coste **BRUTO** (`UNBLENDED_COST`), mirado en pantalla el 2026-08-06.

##### 🚨 Guardia sobre la FILA 2 — no se dispara con el importe recién aparecido

**El reparo, y esta vez con número medido de la documentación:**

> *"AWS Budgets information is updated **up to three times a day**. Updates
> typically occur **8–12 hours** after the previous update."*
> — `cost-management/latest/userguide/budgets-managing-costs`, consultado 2026-08-07

🔑 **Eso rompe el "~24 h" que esta entrada usaba como retraso total.** Son **dos
retrasos en serie**, no uno:

| tramo | cuánto | fuente |
|---|---|---|
| gasto real → dato de coste escrito | hasta ~24 h | pantalla de la consola |
| dato de coste → refresco del presupuesto | **8–12 h** | documentación, arriba |

→ El peor caso legítimo hasta que la alarma **pueda** sonar es del orden de
**36 h**, no 24. **Las "32 horas" que se habían escrito eran documentadamente
cortas**, no solo arbitrarias.

##### 🔴 CORREGIDO el mismo día — el motivo de la guardia estaba MAL, la regla no

**Se escribió primero que la guardia de 12 h salía de ese `24 + 12 = 36`. Puede
que sobre y puede que no** — y en todo caso responde a otra pregunta:

| pregunta | respuesta |
|---|---|
| ¿cuándo **puede** sonar la alarma? | ~36 h desde `t=0`. Ahí sí valen los dos tramos en serie |
| ¿cuánto espero **después de VER el importe**? | ⚠️ **no lo sabemos** — y es lo que decide la guardia |

🚨 **Y la primera versión de ESTA corrección también afirmaba de más.** Decía
*"eso ES un doble conteo"*. **Llamarlo doble conteo ES afirmar que comparten
reloj** — justo el dato que la misma frase declaraba desconocido. Un seto y una
afirmación sin seto, sobre el **mismo** hueco.

✅ **Redacción con UN SOLO desconocido, y dos ramas, ninguna descartada:**

> ❓ **No se sabe si lo que se MUESTRA (`Importe utilizado`) y lo que se EVALÚA
> (el umbral) salen del mismo refresco.** La documentación no lo dice y no se ha
> medido.

| rama | qué implica | qué pasa con el `24 + 12` |
|---|---|---|
| **comparten reloj** | ver el importe ⇒ la evaluación **ya pasó**; falta solo la entrega del correo → **minutos** | sobraba: sería doble conteo |
| **desacoplados** — la consola calcula el campo en vivo al cargar la página y la evaluación va por su ciclo | hay que esperar de verdad → **horas** | era **aproximadamente correcto** |

✅ **La regla se queda, con el motivo corregido:** la fila 2 exige **≥12 h de
silencio DESPUÉS de que el importe sea visible y > 0,01**.
**Su motivo NO es "24 + 12 = 36". Es: no sabemos si lo que se MUESTRA y lo que se
EVALÚA comparten reloj.** Errar hacia esperar de más no produce ninguna conclusión
falsa — solo tarda. Errar hacia el otro lado declara rota una alarma que iba bien.

🔑 **Y fíjate en la forma del error, que es la que hay que reconocer la próxima
vez: una regla correcta sostenida por una razón que puede no serlo.** Es `[D-039]`
con el signo cambiado — allí la precedencia no estaba mal, estaba **muda**. Aquí
no está muda: **está hablando, y podía estar diciendo algo falso.** Peor, porque
un motivo escrito se lee como verificado.

📌 **Y el patrón se repitió DENTRO de la corrección**, que es lo que hay que
llevarse: **el texto que documenta una corrección no está exento de la corrección
que documenta.** Que `h2 − h1` vaya a resolver el hueco mañana no lo hace sabido
hoy.

##### 🎁 La espera trae una MEDICIÓN gratis — y decide la duda de arriba

**Hay que anotar DOS horas, no una:**

| marca | qué se anota |
|---|---|
| **h1** | la hora en que `Importe utilizado` se ve **> 0,01 por primera vez** |
| **h2** | la hora en que **llega el correo** |

**El hueco `h2 − h1` es un número que hoy no tiene nadie, ni la documentación**, y
contesta la pregunta abierta sin gastar un céntimo:

- **minutos** ⇒ mostrar y evaluar **comparten reloj** → la guardia de 12 h se puede
  bajar en el futuro, con dato detrás.
- **horas** ⇒ van **desacoplados** → la guardia estaba bien y ahora está medida.

🔑 **Con eso la espera deja de ser tiempo muerto y pasa a ser la SEGUNDA medición
del experimento.** Es `LM.19`: la lista decía qué falta por **construir**, no qué
falta por **saber**.

##### 📋 TABLA VIGENTE — sellada 2026-08-07, sustituye a la de `cfba50a`

**Instrumento único: el campo `Importe utilizado` de `My Zero-Spend Budget`.**
No se lee `Facturas` — esa ventana no tendrá nada hasta que cierre agosto.

| `Importe utilizado` | bandeja | veredicto |
|---|---|---|
| **> 0,01** | ✉️ correo | ✅ **`A-018` CERRADA.** Se anota el retraso real desde `t=0` |
| **> 0,01** | 🔇 silencio, **< 12 h** desde que el importe es visible | ⏳ **seguir esperando.** NO es la fila 2 |
| **> 0,01** | 🔇 silencio, **≥ 12 h** desde que el importe es visible | 🚨 **ALARMA ROTA.** Hallazgo grande y a tiempo |
| **= 0,00** | (da igual) | ⏳ **(a)** el dato no ha aterrizado → esperar · **(b)** algo absorbe el cargo → hallazgo. **NO "es gratis"** — causa desmentida |

🔑 **Hay que anotar la hora en que el importe se vea > 0,01 por primera vez (`h1`),
y la hora en que llegue el correo (`h2`).** Sin `h1` las dos filas del medio no se
distinguen —y son la diferencia entre "esperar" y "declarar rota" un control que
va bien—; y `h2 − h1` es la **segunda medición** del experimento, ver abajo.

##### 🚨 Y una línea del protocolo de lectura que NO es de la lista de puertas

> **Al abrir *Facturación y costos*: se lee UN campo — `Importe utilizado` del
> presupuesto. NO se toca NADA de la cabecera. Ahí vive "Actualizar plan".**

**Por qué esto vive aquí y no como renglón 8 de `T-068`:** las siete puertas de
`[C-005]` comparten una propiedad — **hay que ir a buscarlas**. Nadie aterriza en
Control Tower sin desviarse. Contra puertas así, una lista de "no toques esto"
funciona.

**"Actualizar plan" no es así.** Está en la cabecera de la página que hay que
abrir **todos los días** durante las próximas semanas para leer este experimento,
y **pegada al aviso tranquilizador** que sí hay que leer.

🔑 **El riesgo no se mide por lo peligrosa que es la puerta, sino por cuántas veces
vas a pasar por delante.** De las ocho, esta es la única con **tráfico
garantizado** — y garantizado *por este experimento*. Meterla como renglón 8 le
daba el mismo peso que a Control Tower, y no lo tiene.

##### ⏳ Tercera lectura — 2026-08-07, tarde. Sigue 0,00, y aparece un CUARTO RELOJ

**Estado:** `Presupuesto 1,00 US$` · **`Importe utilizado 0,00 US$`** · silencio en
la bandeja. **No es veredicto**: es la causa **(a)** de la enmienda.

📌 **Y el propio presupuesto explicó su silencio**, con un mensaje que no estaba
escrito en ninguna parte:

> *"Después de crear un presupuesto, pueden transcurrir **hasta 24 horas** para
> que se rellenen todos los datos de gastos."* — ficha del presupuesto, 2026-08-07

🔑 **Ese reloj NO es ninguno de los tres que ya teníamos.** Arranca en la
**creación del presupuesto**, no en el gasto ni en la primera visita a la consola:

| # | reloj | arranca en | estado |
|---|---|---|---|
| 1 | gasto de la Elastic IP | 2026-08-06 **15:29 UTC** | ⏱️ es el que mide el retraso de la alarma |
| 2 | preparación de datos de coste | primera visita a la consola de facturación | ✅ vencido — el mensaje desapareció |
| 3 | dólar de verificación de tarjeta | apertura de la cuenta | ❌ no es del experimento |
| 4 | **relleno del presupuesto** ← **NUEVO** | **creación del presupuesto**, 2026-08-06 durante el día (paso 1) | ⏳ vence **durante el 2026-08-07** |

❓ **Y falta un dato que nadie anotó: la HORA exacta en que se creó el presupuesto.**
Solo consta *"2026-08-06 durante el día"*, y el paso 1 va antes del paso 3, así que
fue **antes de las 15:29 UTC**. Con eso el reloj 4 **vence como muy tarde el
2026-08-07 por la tarde** — no se puede afinar más, y no hace falta: para la
lectura del **2026-08-08** ya estará vencido con holgura.

✅ **Lo que esto SÍ aporta, y no es poco:** el silencio de hoy tiene **una causa
concreta y documentada por AWS**, no una conjetura. Refuerza la causa (a) y deja la
(b) —*"algo absorbe el cargo"*— donde estaba: **abierta, pero sin motivo aún para
sospecharla.**

🚨 **Lo que NO aporta: no cierra nada.** *"Hasta 24 horas"* vuelve a ser un **techo,
no una promesa** — la misma trampa del reloj 2, que ya nos hizo leer dos veces la
pantalla equivocada. **La lectura sigue siendo el 2026-08-08.**

##### ⚖️ El precio del cambio de instrumento — qué dejó de cubrir el experimento

El paso de *Facturas* al `Importe utilizado` del presupuesto es una mejora real,
pero **hay que decir en voz alta lo que cuesta**, o el experimento promete más de
lo que prueba:

- **Antes:** premisa (factura) y prueba (bandeja) venían de **servicios distintos**.
- **Ahora:** las dos cuelgan del **servicio de presupuestos**.

✅ **El fallo cae del lado seguro:** si ese servicio está ciego, las dos callan a la
vez y se lee *"aún no hay cargo"* → se sigue esperando. No se declara nada falso.

❌ **Lo que se pierde:** el experimento **ya no detecta un fallo en la ENTRADA de
datos al presupuesto**. Solo prueba el tramo *"el presupuesto vio el dinero → mandó
el correo"*. Es menos de lo prometido, **pero es el tramo que importa y ahora lo
prueba limpio.** Queda escrito para que en tres meses nadie crea que `A-018`
cubrió más de lo que cubrió.

##### 💡 Lo que ya se aprendió sin esperar al veredicto

**Dos días seguidos se leyó la pantalla equivocada, y las dos veces el error tenía
la misma forma:** un *"sin datos"* que se parecía a un resultado. La defensa no
fue la prudencia, fue tener la **tabla de lectura escrita de antemano** — obligaba
a preguntarse *"¿esto es de verdad la Observación 1?"* en vez de dar por buena la
primera cifra que se pareciera a la esperada.

🔑 **Y la corrección de las 750 horas es la misma lección otra vez:** se
tenía una explicación cómoda que cerraba el caso —"es gratis, por eso no cobró"—
y era **de memoria**. Treinta segundos de documentación la tiraron. Una
explicación que cierra un experimento merece la misma comprobación que el
experimento.
📌 **Aquí decía `[L-013]` y se le quitó el corchete el 2026-08-09** (`[L-034]`):
esa entrada habla de huecos de concurrencia y no de esto, y **ninguna lección de
ningún repo dice exactamente esto** — no es `[LM.13]` (*no se ha visto morder*)
ni la regla 6 (*un número sin corrida detrás*), porque lo que falló aquí fue una
**explicación** de memoria, no un número. La frase se queda suelta hasta que
tenga un puntero de verdad: una frase sin puntero es honesta, un puntero falso no.

##### ✅ Cuarta lectura — 2026-08-08, 11:10 UTC (~43,7 h desde `t=0`). EL DATO ATERRIZÓ

**Por primera vez hay un número distinto de cero**, y no está donde se le
esperaba. Tres pantallas leídas el mismo minuto:

| pantalla | campo literal | valor | qué vale |
|---|---|---|---|
| *Facturas*, agosto 2026 | Total general estimado | **0,00 US$** | ❌ nada — la factura nace al cerrar el mes |
| *Presupuestos* → `My Zero-Spend Budget` | **`Importe utilizado`** | **0,00 US$** | ✅ el instrumento sellado. Sigue en cero |
| *Facturación y costos*, inicio → widget **`Resumen de Costos`** | **`Costo Acumulado Mensual`** | 🟢 **0,12 US$** | 🆕 **el hallazgo** |

🔑 **Esto MATA la causa (b) y CONFIRMA la (a).** La tabla vigente dejaba dos
causas vivas para un `Importe utilizado = 0,00`: **(a)** el dato no ha aterrizado,
**(b)** algo absorbe el cargo por una vía desconocida. **Hay 0,12 US$ de cargo,
visible en pantalla: nada lo está absorbiendo.** La (b) queda descartada por
observación, no por argumento.

⚖️ **Y esto NO es enmendar la tabla con el número delante** —lo que `[D-040]`
prohíbe—. La tabla **misma** declaró esas dos causas abiertas y **pidió
distinguirlas antes de concluir**. Una observación externa que las distingue es
lo que la tabla encargaba, no una excepción escrita a posteriori. La diferencia
importa: enmendar es cambiar el criterio; esto es **ejecutarlo**.

##### 🆕 Un QUINTO instrumento, y es el más rápido de los tres

`Costo Acumulado Mensual` no es ninguno de los dos que ya se conocían. No es la
factura (que no existe hasta septiembre) ni el `Importe utilizado` (que va por su
propio ciclo de refresco). **Es una tercera regla, y hoy va por delante de las
otras dos.**

📌 **Valor operativo, más allá del experimento:** durante los seis meses del paso
7, este widget es la **ventana de aviso temprano**. Ve el gasto antes que el
presupuesto, y por tanto antes que la alarma. No lo sustituye —no avisa solo, hay
que ir a mirarlo— pero acorta el tiempo de descubrimiento de un goteo.

❓ **Sin verificar: si ese widget mide BRUTO o NETO.** Del `Importe utilizado` sí
se sabe (`UNBLENDED_COST`, leído en pantalla el 2026-08-06); de este no se ha
mirado. 🔑 **Y la conclusión de hoy NO depende de saberlo**, que es lo que la hace
sólida: sea cual sea la base, un valor **> 0** demuestra que existe dato de coste
y que nada lo está tapando por completo. Se anota como pregunta abierta, no como
grieta.

##### ✅ Los DOS TRAMOS EN SERIE, vistos por fin al mismo tiempo

La enmienda de `[D-040]` había **leído** en la documentación que el retraso no es
uno sino dos: gasto → dato de coste escrito, y dato de coste → refresco del
presupuesto (*8–12 h*). Estaba leído, nunca observado.

**Hoy se observa, y en la misma pantalla partida en dos:** el dato de coste
**existe** (0,12) y el presupuesto **todavía no lo ha recogido** (0,00). Los dos
tramos, separados, simultáneos. 🔑 **La causa (a) deja de ser genérica y queda
LOCALIZADA:** no es que AWS no haya calculado el coste — es que **el presupuesto
no se ha refrescado**. Es el tramo 2, y es el único que queda por delante.

##### ⏳ Lo que sigue SIN poder concluirse — `h1` no ha ocurrido

🚨 **`A-018` NO se cierra hoy.** El `Importe utilizado` sigue en 0,00, así que
**`h1` no existe todavía**, y sin `h1` la guardia de las ≥12 h **ni siquiera ha
arrancado**. No hay veredicto posible sobre la alarma: no se puede decir que
funcione ni que esté rota. **Sigue sin habérsele visto morder.**

Fila de la tabla vigente que aplica: la cuarta (`= 0,00` → esperar), ahora con la
causa (a) **confirmada y localizada** en vez de ser una de dos posibilidades.

##### 📐 Aritmética de lista, marcada como tal — la pantalla va por detrás del reloj

`0,12 US$ ÷ 0,005 US$/h ≈ **24 h** de IP ociosa facturada. Desde `t=0`
(2026-08-06 15:29 UTC) hasta la lectura van **~43,7 h**.

→ **Lo que se ve en pantalla va del orden de 20 h por detrás del tiempo real.**

⚠️ **Es aritmética de lista de precios, no una corrida** —mismo defecto que
`[A-015]`—, y además el `0,005 US$/h` no se ha vuelto a comprobar hoy. Sirve como
orden de magnitud para saber qué esperar mañana, no como cifra.

❓ **Y falta un dato que no se puede recuperar:** la hora en que el 0,12 apareció
**por primera vez** en ese widget. Ayer no se miró esta pantalla —se miraba
`Facturas` y el presupuesto—, así que solo consta que es visible a las 11:10 UTC
del 08. El `t_cargo` real está en algún punto entre la última lectura del 07 y
esa hora. 🔑 **Lección barata: un instrumento que no se conoce no se puede haber
mirado.** El widget existía desde el principio.

##### 🔁 Consecuencia para `[D-041]` — las medidas que quedan NO las mata la EC2

`[D-041]` pospuso la EC2 por dos motivos. Hoy hay que decir en qué estado queda
cada uno, porque no están igual:

| motivo de `[D-041]` | estado tras la lectura del 08 |
|---|---|
| **(1)** lanzar mata `t_cargo − t=0`, medible una sola vez | ✅ **cobrado.** El cargo apareció con **una sola fuente de gasto** en la cuenta. Se midió con menos precisión de la deseable (ver el ❓ de arriba), pero se midió — y con la EC2 encendida ya no habría sido atribuible |
| **(2)** encender antes de ver morder la alarma es `[LM.13]` | 🚨 **SIGUE VIVO. La alarma no ha mordido ni una vez.** |

📌 **Y `h1` / `h2 − h1` sobreviven al lanzamiento**, que es lo que quita presión:
los 0,12 US$ **ya están bancados y ya superan el umbral por 12x**, atribuibles
solo a la Elastic IP. El próximo refresco del presupuesto cruza el umbral por ese
cargo, encienda o no la EC2. Lo que la EC2 emborrona es la **cuantía**, no el
**cruce**.

⚠️ **Recordatorio del protocolo de lectura:** el widget `Resumen de Costos` vive
en la **página de inicio** de *Facturación y costos* — la misma cuya cabecera
lleva *"Actualizar plan"*. Este hallazgo **aumenta el tráfico** por esa página, y
el riesgo de esa puerta se mide justamente por tráfico (`[L-026]`). Se lee el
widget y **no se toca la cabecera**.

#### 🟡 Quinta lectura — 2026-08-08, 15:08 UTC (~47,7 h desde `t=0`)

`Importe utilizado` = **0,00 US$**. Sin cambio respecto a la cuarta lectura,
3,9 h antes. **`h1` sigue sin ocurrir**, la guardia de las ≥12 h sigue sin
arrancar, y la alarma sigue sin habérsele visto morder. Fila vigente: la cuarta
(`= 0,00` → esperar), con la causa (a) ya localizada en el tramo 2.

🔑 **Esta lectura no se hizo para el experimento: se hizo porque `[D-041]` la
exige antes de lanzar la EC2.** Y ese orden queda **cumplido con este dato** —
el campo se leyó primero, dijo 0,00, y `[D-041]` dice explícitamente *"diga lo
que diga ese campo"*. La segunda mitad de `[T-059]` queda desbloqueada.

⚠️ **Lo que cambia a partir de aquí, y hay que escribirlo ANTES de encender:**
desde el momento en que la EC2 arranque, la cuenta tiene **dos** fuentes de
gasto. `h1` y `h2 − h1` siguen midiéndose —el cruce del umbral ya está bancado
por los 0,12 US$ de la Elastic IP—, pero **la cuantía del importe deja de ser
atribuible solo a la IP**. Cualquier lectura posterior se interpreta sabiendo
esto.

#### ⏱️ `t=0` de la EC2 — MEDIDO en la máquina, 2026-08-08 15:54:27 UTC

La segunda fuente de gasto tiene ahora su propio reloj, y **no es una deducción:
lo dijo la máquina.** Primera conexión SSH del proyecto, y el primer comando fue
leer su arranque:

    $ uptime -s
    2026-08-08 15:54:27          ← t=0 de la EC2 (10:54:27 hora local)
    $ date -u
    2026-08-08 17:50:50 UTC      ← momento de la lectura
    → 1 h 56 min encendida

🔑 **Y corrige de entrada una deducción que ya se había hecho en voz alta:** que
la máquina arrancó a las **15:08 UTC**, la hora de la quinta lectura. No. Esa es
la hora en que se leyó el presupuesto **antes** de tocar la consola, como exigía
`[D-041]`; entre leer y lanzar pasaron **46 minutos**. Sobre un tiempo
transcurrido de ~2 h, tomar las 15:08 por `t=0` infla el divisor un **~55%** y
abarata el coste por hora en la misma proporción.

📌 **Por qué esto no es un detalle de redacción:** la única aritmética que tiene
`A-018` de aquí en adelante es **dinero ÷ horas**, y ahora hay dos fuentes con
dos `t=0` distintos — la Elastic IP desde `2026-08-06 15:29 UTC`, la EC2 desde
`2026-08-08 15:54:27 UTC`. Separar las dos cuentas exige que los dos relojes
sean **medidos**, no inferidos. Es `LM.23` aplicado a la fecha: *medido no es lo
mismo que anotado*.

⚖️ **Precisión del instrumento, escrita:** `uptime -s` da cuándo arrancó el
**sistema operativo**; la facturación empieza cuando AWS **crea** la instancia,
unos segundos antes. La diferencia es irrelevante frente a los 46 min que se
acaban de corregir, y el instrumento tiene una ventaja que la consola no tiene:
**se relee cuando se quiera, sin abrir el navegador** — o sea, sin pasar por la
página que lleva *"Actualizar plan"* en la cabecera (`[L-026]`).

> 🔴 **ESA ÚLTIMA FRASE ES FALSA, corregida el 2026-08-09 → `[L-030]`.**
> `uptime -s` **se relee, sí, pero no devuelve lo mismo**: no da el nacimiento de
> la instancia, da el **último arranque del sistema**. Hoy dice
> `2026-08-08 18:11:15`, porque `T-065` la reinició esa tarde. El `15:54:27`
> **sigue siendo el `t=0` bueno** —era el primer arranque, minutos después del
> lanzamiento— pero ha pasado de **medido** a **anotado**: ya no hay forma de
> volver a comprobarlo desde la máquina, solo en la consola (*Launch time*).
> 🚨 Y con `[D-045]` esto se vuelve permanente: la máquina arranca de nuevo cada
> mañana, así que **`uptime -s` no sirve para las horas acumuladas de `[T-067]`**.

✅ **De regalo, `[D-043]` queda verificado en la máquina y no en el formulario:**
`lsb_release -ds` devuelve `Ubuntu 24.04.4 LTS`. La AMI que se decidió es la que
está corriendo — que era exactamente el riesgo que `[D-043]` nombraba, porque el
desplegable de AWS se recarga solo a la LTS más nueva.

❓ **Queda abierto, y es barato:** no se ha vuelto a leer `Importe utilizado`
después de encender. La sexta lectura dirá si `h1` ocurrió durante estas ~2 h.

#### 🟠 Sexta lectura — 2026-08-09, ~14:45 UTC (~71,3 h de IP, ~22,9 h de EC2)

Los dos instrumentos, leídos en la misma sesión:

| pantalla | campo | valor |
|---|---|---|
| Presupuesto | `Importe utilizado` | **0,00 US$** |
| *Facturación y costos* → inicio | `Costo Acumulado Mensual` | **0,37 US$** |

⚠️ **La hora es la de la sesión, no la de un instrumento.** `date -u` en la
máquina local dio `2026-08-09 14:46 UTC` al abrir el trabajo; la lectura se hizo
en esos minutos. No es un sello medido como el `uptime -s` del 08 — se anota con
esa precisión, no con más.

##### 🚨 `h1` SIGUE sin ocurrir — y ahora eso empieza a costar explicación

`Importe utilizado` lleva **cuatro lecturas seguidas en 0,00** (07 tarde, 08
11:10, 08 15:08, 09 ~14:45). La guardia de las ≥12 h **sigue sin arrancar**,
porque arranca en `h1`. Fila vigente: la cuarta (`= 0,00` → esperar).

📌 **Lo nuevo, y hay que escribirlo aunque no cambie el veredicto:** el tramo 2
—el refresco del presupuesto, documentado en *8–12 h*— tenía su reloj arrancado
como muy tarde el **08 a las 11:10 UTC**, que es cuando se vio el coste ya
calculado (0,12). De ahí a esta lectura van **~27,6 h**: más del **doble** del
techo documentado, y el presupuesto no lo ha recogido.

⚖️ **Esto NO cierra `A-018` ni declara la alarma rota**, y la tentación es
justamente esa. El criterio sellado exige ≥12 h de silencio **después** de que el
importe sea visible, y el importe **no es visible**. Lo que hay es un tramo 2 que
excede su ventana documentada — un hecho que se anota, no un veredicto que se
adelanta. Si se declarase rota aquí se estaría midiendo con un criterio distinto
del que se selló antes de mirar, que es exactamente lo que `[D-040]` prohíbe.

##### 📐 Aritmética de lista — el incremento ya NO cabe en la Elastic IP sola

De la cuarta lectura a esta: **0,12 → 0,37 US$**, es decir **+0,25 US$** en las
~27,6 h transcurridas entre ambas.

    0,37 US$ ÷ 0,005 US$/h ≈ 74 h de IP ociosa facturada
    tiempo real transcurrido desde t=0 de la IP ≈ 71,3 h

→ La cifra facturada **supera** las horas de vida de la IP. Con una sola fuente
eso sería imposible; con dos es lo esperado. 🔑 **Es la primera señal en pantalla
de que la EC2 está pesando en la factura**, y confirma en dinero lo que la quinta
lectura anunció en prosa: la **cuantía** ya no es atribuible a la IP.

⚠️ **Aritmética de lista de precios, no una corrida** — mismo defecto que
`[A-015]`. El `0,005 US$/h` viene de la lista y no se ha vuelto a comprobar; el
precio/hora de la `t3.micro` **no se usa aquí a propósito**, porque no está
medido. Sirve para saber qué esperar, no como cifra. La separación limpia de las
dos fuentes es trabajo de `[T-067]`, no de esta lectura.

📌 **Y lo que sí queda firme:** con 0,37 US$ ya bancados, el cruce del umbral de
0,01 US$ está **37 veces** cubierto. Cuando el presupuesto se refresque, tiene
que sonar. Lo que se está midiendo ya no es *si* hay dinero — es cuánto tarda el
instrumento en verlo.

##### 🔴 Corrección: son TRES fuentes de gasto, no dos — y lo son desde el 08

La quinta lectura escribió *"desde que arranque la EC2 hay **dos** fuentes de
gasto"*. **Falta una: el volumen de disco (EBS).** Un disco EBS **cobra por
existir**, esté la máquina encendida o apagada, y nació con la instancia.

| fuente | desde | ¿cobra con la máquina detenida? |
|---|---|---|
| Elastic IP | 2026-08-06 15:29 UTC | ✅ sí — es la que generó los primeros 0,12 US$ |
| Horas de instancia `t3.micro` | 2026-08-08 15:54:27 UTC | ❌ no — es lo único que ahorra `[D-045]` |
| **Volumen EBS** | 2026-08-08 15:54:27 UTC | ✅ **sí** |

🔑 **De dónde salió el error, porque tiene forma reconocible:** el dato del
volumen se descubrió hoy razonando sobre `[D-045]` —*"apagar no lleva el gasto a
cero"*— y se aplicó **solo** a esa pregunta. Nadie volvió a la fila de `A-018`
que ya decía "dos". **Un hallazgo usado en un sitio y no propagado al otro** es la
misma forma de `[L-029]`: lo que nace después no tiene dueño.

⚖️ **Qué NO cambia:** ninguna conclusión de hoy. La aritmética de las 74 h usó el
**total** de la pantalla, no la composición. `h1` y `h2 − h1` tampoco se tocan.

🚨 **Qué SÍ cambia, y es lo que obliga a corregirlo antes de mañana:** `[T-067]`
tiene que separar **tres tarifas, no dos**, y las tres tienen relojes y
comportamientos distintos bajo la ventana de `[D-045]` — solo una de ellas se
apaga de noche. Proyectar 180 días con dos fuentes daría de menos, y en la
dirección peligrosa.

### [A-017] 2026-08-05 — DuckDNS seguirá en pie los seis meses

- **Se supone que:** `teapp.duckdns.org` seguirá resolviendo durante todo el paso
  7. Lo comprobado el 2026-08-05 es que **el servicio existe y funciona hoy** —
  se entra con Google, GitHub, Reddit o Twitter y da un token. Eso **no es** lo
  mismo que suponer que durará seis meses, y la diferencia es toda la suposición.
- ⚠️ **Y hay motivo concreto para dudarlo, no es prudencia genérica.** Es
  gratuito y se sostiene con donaciones de Patreon. StatusGator registra una
  caída el **2026-06-21**, y en **agosto de 2025** hubo un episodio en que se dio
  por desaparecido. 📌 Ironía anotada porque puede importar: DuckDNS **está
  alojado en AWS**, así que no es una segunda cesta independiente de la primera.
- 🚨 **Si es falsa, no se ve feo: se cierra la app.** La cadena es corta y cada
  eslabón depende del anterior:

      DuckDNS cae → el nombre no resuelve → Caddy no renueva el certificado
      → la cookie `Secure` no viaja → NO ENTRA NADIE

  Y el fallo es de los mudos: la máquina sigue encendida, `systemctl status
  teapp` dice que todo está bien, y los tests pasan. Es la familia de `[L-031]`
  (antes `[A-009]`, retirada de aquí el 2026-08-09 al comprobarse).
- **Cómo se comprobaría:** no se puede comprobar por adelantado — es una
  predicción sobre un tercero. Lo que sí se puede es **medir la exposición**:
  anotar en `T-058` la fecha de caducidad del certificado y saber que ese es el
  plazo real que hay para reaccionar. Un certificado de Let's Encrypt dura 90
  días, así que una caída corta de DuckDNS **no tumba nada** — solo estorba si
  coincide con la ventana de renovación.
- 🔑 **Qué la haría barata de sobrevivir, y por qué no se hace hoy:** el plan B
  es otro proveedor de nombre gratuito. No se prepara ahora porque cambiar de
  nombre son dos líneas —el `Caddyfile` y un registro DNS— y prepararlo por
  adelantado sería la abstracción que PI-2 prohíbe. **Lo que sí hace falta es
  saber que existe el riesgo**, que es justo lo que hace esta entrada.

#### 🟠 2026-08-08 — Fallos de resolución OBSERVADOS (causa SIN resolver), y la exposición ya medida

Día del despliegue real. Dos datos nuevos, y van en direcciones opuestas.

**(1) 🟠 DuckDNS falló al resolver, por primera vez y delante de los ojos.** Tres
`curl` seguidos contra `https://teapp.duckdns.org/` devolvieron
`Could not resolve host`, a los ~35 min de un `nslookup` que había resuelto
correctamente a `32.199.55.191`. Un minuto después volvía a resolver, y tres
peticiones seguidas dieron `200`. **Fue un parpadeo, no una caída.**

🔑 **Lo que esto cambia y lo que no.** No convierte `A-017` en verdadera ni en
falsa — sigue siendo una predicción sobre un tercero. Lo que hace es subirla de
*riesgo leído en StatusGator* a **riesgo visto en este proyecto**: el modo de
fallo que la entrada describe ya no es hipotético, se ha manifestado en su
versión benigna. ⚠️ Y avisa de algo operativo: **un fallo de DuckDNS se disfraza
de fallo propio.** Los tres `curl` fallaron con la máquina perfectamente sana —
si esa hubiera sido la única prueba, se habría buscado el problema en Caddy.

📌 **Cómo se separó, y queda como receta:** `curl --resolve` salta el DNS pero
**mantiene la verificación del certificado**. Devolvió `200` con
`ssl_verify_result=0` mientras el nombre no resolvía → el servidor estaba bien y
el fallo era del nombre. Es la forma barata de no confundir las dos cosas.

🔴 **CORRECCIÓN, escrita el mismo día unas horas después.** Arriba se tituló
esto *"primer fallo de DuckDNS"*. **Eso afirmaba más de lo medido**, y hay que
dejarlo dicho antes de que alguien lo lea dentro de tres meses como un cargo
contra DuckDNS:

1. **Segundo episodio** hacia el final de la sesión: otras tres peticiones
   seguidas con `Could not resolve host`, y recuperación inmediata.
2. **Diagnóstico deliberado, y NO reprodujo:** 8 consultas contra el resolutor
   local (el router, `192.168.40.1`) y 8 contra uno público (`8.8.8.8`),
   **16 de 16 correctas**. No se pudo atribuir el fallo a ninguno de los dos.
3. 🔑 **Y un dato que apunta en contra de la hipótesis DuckDNS:** en la
   observación externa independiente, una petición al **puerto 80 con el mismo
   nombre** respondió `308` **en el mismo instante** en que la petición a HTTPS
   fallaba al resolver. Un servidor autoritativo caído no puede resolver una
   consulta y no la de al lado en el mismo segundo. Eso señala al **resolutor
   del cliente** (caché, timeout, límite de consultas), no a DuckDNS.

⚖️ **Veredicto honesto: el fenómeno es real y está observado tres veces desde
dos redes distintas; la CAUSA está sin resolver.** `A-017` no queda ni reforzada
ni debilitada — sigue siendo una predicción sobre un tercero, y estos fallos
**no son todavía evidencia contra DuckDNS**.

✅ **Lo que SÍ queda, y es lo aprovechable:** el modo de fallo es real y
**se disfraza de avería propia**. Falle quien falle —DuckDNS, el router, el
ISP—, el síntoma es idéntico al de un servidor caído, con la máquina sana. La
receta del `--resolve` sirve exactamente igual, y esa es la parte que hay que
recordar el día que pase de verdad.

#### 🟢 2026-08-09 — Cuarto y quinto episodio, y la causa por fin LOCALIZADA (no es DuckDNS)

Dos fallos más, en la misma sesión, con **el mejor dato hasta ahora**: esta vez
el fenómeno se dio **partido entre dos programas del mismo ordenador y en el
mismo minuto**.

    ssh teapp.duckdns.org      → ssh: Could not resolve hostname
    nslookup (router)          → 32.199.55.191   ✅
    nslookup (8.8.8.8)         → 32.199.55.191   ✅
    curl https://...           → 200 desde 32.199.55.191   ✅

🔑 **Eso cierra la pregunta que llevaba abierta desde el 08.** El 08 se pudo
decir *"apunta al cliente"* con un solo indicio (el puerto 80 respondiendo
mientras el 443 no resolvía). Hoy es directo: **el nombre resuelve y el servidor
contesta en el instante exacto en que un programa dice que no puede resolverlo.**
Un servidor autoritativo caído no le contesta a `nslookup` y a `curl` y le niega
la respuesta a `ssh`. **La causa está en la resolución del cliente, no en
DuckDNS.**

⚖️ **Y por eso `[A-017]` sigue intacta, ni reforzada ni debilitada.** Los cinco
episodios **dejan de contar como evidencia contra DuckDNS** — no lo eran antes y
ahora se sabe por qué. La suposición sigue siendo lo que era: una predicción
sobre un tercero, sin comprobar.

🔴 **Una hipótesis se propuso y murió en dos minutos, y queda escrita porque el
error es instructivo.** Al fallar `ssh` sin `-4`, se supuso que el problema era
la consulta IPv6 (`AAAA`) y que `-4` lo arreglaba. Se probó, **funcionó**, y se
dijo en voz alta. Dos minutos después **`ssh -4` falló igual**.

> 🔑 **Un intento no distingue "lo arreglé" de "esta vez no pasó".** Con un fallo
> **intermitente**, la primera corrida verde no es evidencia de nada: es la línea
> base. Es `[L-020]` otra vez —un verde que es silencio— y el error costó cero
> solo porque el fallo volvió enseguida. Si hubiera tardado un día, `-4` se
> queda escrito como "la solución".

✅ **El rodeo que SÍ es sólido, y no es una solución sino una separación:**
conectarse **por la IP fija** (`ubuntu@32.199.55.191`), que no pasa por el DNS.
Funcionó las tres veces que se usó. 📌 Es hermano de la receta del `--resolve` de
ayer: no arregla la resolución, la **saca de la ecuación** para poder trabajar y
para saber de quién es el fallo.

⚠️ **Lo que esto NO resuelve, y hay que dejar dicho:** el rodeo sirve para
**nosotros**, que tenemos la IP y una llave. **A quien use TEAPP desde su
navegador no le sirve de nada.** Si el fenómeno le pasa a quien practica inglés,
ve una página que no carga y no tiene `--resolve` ni IP que escribir.

**(2) ✅ La exposición que la entrada pedía medir, MEDIDA.** Certificado leído
con `openssl s_client` contra la máquina de verdad:

    issuer   = C=US, O=Let's Encrypt, CN=YE2
    subject  = CN=teapp.duckdns.org
    notBefore= Aug  8 16:55:35 2026 GMT
    notAfter = Nov  6 16:55:34 2026 GMT      ← 90 días exactos

🔑 **El plazo de reacción deja de ser documentación y pasa a ser una fecha:
2026-11-06.** Los "90 días de Let's Encrypt" que esta entrada citaba de memoria
quedan confirmados contra el certificado emitido. Caddy renueva alrededor del
día 60, así que la ventana peligrosa —que DuckDNS esté caído *justo* cuando toca
renovar— cae en torno a **principios de octubre de 2026**, y habrá una segunda
antes de que se acabe el plan gratuito de `[C-006]` (2027-02-06).

⚠️ **Detalle para que nadie lo lea mal dentro de tres meses:** el `notBefore` es
**una hora anterior** a la corrida de `install.sh`. No es que el certificado sea
viejo — Let's Encrypt antedata una hora a propósito, para tolerar relojes
desajustados en los clientes.

> 🗑️ **`[A-016]` se retiró el 2026-08-05, comprobada y FALSA.** Decía que las
> tres puertas al plan de pago de `[C-005]` eran todas: son **siete**. La lectura
> que la mató está en `T-068`; lo aprendido, en `[L-016]`; la lista verificada
> vive ahora en `[C-005]`.

### [A-015] 2026-08-05 — El paso 7 cabe de sobra en los $200 de créditos

- **Se supone que:** la cuenta de abajo es correcta, y por tanto el paso 7 gasta
  del orden de **$50 de los $200** en créditos:

  | concepto | estimado |
  |---|---|
  | `t3.micro`, Linux, `us-east-1`, $0.0104/hora | ~$7.59/mes |
  | 6 meses encendida 24/7 | ~$45 |
  | disco de 8 GB | ~$4 en total |
  | **total** | **~$50** |

- 🔑 **Por qué importa más de lo que parece:** sobre esta holgura —un factor de
  cuatro— se **descartó** en `[D-029]` la pieza que apagaría la máquina sola
  cuando nadie practica. Si la cuenta está mal, esa pieza vuelve.
- **Por qué es suposición y no dato:** los precios salen de una **lista de
  precios, no de una factura**. Nadie ha corrido nada todavía. La regla 6 del
  proyecto no deja pasar un número así sin marcarlo — es la misma situación del
  20 de `[A-010]` y del 5 de `[A-013]`.
- ⚠️ **Y le falta un renglón que se sabe que existe:** AWS cobra por **cada
  dirección IPv4 pública**, esté o no en uso, del orden de $3-4/mes. Cabe de
  sobra en la holgura, pero **no está sumado arriba**. Verificar el precio exacto
  antes de cerrar el presupuesto.
- **Cómo se comprobaría:** no con más aritmética. Con el **panel de facturación
  de AWS a los pocos días de encender la máquina**: multiplicar el gasto diario
  real por 180 y compararlo con $200. Esa es la única corrida que vale.
- **Si es falsa:** los créditos se acaban antes de los 6 meses y **AWS cierra la
  cuenta a media obra**. No llega una factura —eso lo impide `[C-003]`— pero el
  ejercicio se corta sin terminar. El arreglo es el que hoy se descarta: apagar
  la máquina cuando no se usa. 📌 Y ojo, **apagarla no ahorra tanto como parece**:
  la IP fija sigue cobrando con la máquina apagada.

### [A-013] 2026-08-04 — 5 fallos y 15 minutos son los números del tope de intentos

- **Se supone que:** `MAX_FAILED_ATTEMPTS = 5` y `LOCKOUT_WINDOW_SECONDS = 900`
  son un ajuste razonable: aguantan a quien se equivoca de verdad y cortan a
  quien prueba contraseñas a la fuerza.
- **Por qué nace hoy:** los dos números se escribieron en `[D-026]` sin ninguna
  corrida detrás, y la regla 6 del proyecto no deja pasar un número así sin
  marcarlo. Es la misma situación de `[A-010]` con las 20 prácticas al día.
- **Cómo se comprobaría:** no con un ataque —no lo hay—, sino con **los dos
  extremos por separado**:
  - *¿Es corto?* Mirar en el log cuántos 429 le salen a gente que sí tenía
    cuenta y acabó entrando. Si aparecen, 5 se queda corto.
  - *¿Es largo?* Con 5 intentos cada 15 minutos, quien pruebe a la fuerza saca
    **480 intentos al día**. La pregunta que decide es si una contraseña de las
    que se aceptan aquí (mínimo 8 caracteres) se adivina en ese presupuesto. Eso
    sí se puede calcular sin atacar nada.
- 🚨 **Y lo que de verdad decide si el 5 vale NO es cuánta gente ataca, sino
  cuánta gente COMPARTE ORIGEN.** Esto es lo fácil de mirar al revés. El freno no
  reparte cinco intentos por persona: reparte cinco **por dirección**. Dos
  hermanos en la misma casa se gastan el mismo cupo; un salón de clase entero
  detrás de un router se lo gasta entre todos, y basta con que unos pocos tengan
  el día torpe.
  - 🔑 Por eso el número correcto **crece con el tamaño del grupo que comparte
    salida**, y no con la amenaza. Un 5 que sobra para una casa se queda corto
    para un aula sin que nadie haya atacado nada.
  - ⚠️ Y con `[A-014]` en falso —un proxy delante— el grupo que comparte origen
    pasa a ser **todo el mundo**, y entonces no hay número que valga: el freno
    hay que rehacerlo, no reajustarlo. Ver `T-055`.
- **Lo que amortigua mientras tanto:** los dos números están donde se cambian en
  una línea, y el tope entra por parámetro en `check()`. Equivocarse aquí no
  cuesta un rediseño, que es la razón de poder aplazar la medida. Y hoy el grupo
  que comparte origen es de una casa, no de un aula.
- **Si es falsa:** por corto, se echa de la app a quien se le olvidó la
  contraseña — y como el freno cuenta por origen, se echa también a quien viva en
  su casa. Por largo, el freno tranquiliza sin frenar, que es peor que no
  tenerlo: nadie vuelve a mirar un problema que cree resuelto.

<!-- [A-011] MUERTA el 2026-08-14, al TERCER intento y esta vez con la corrida
     delante. Se fue a `[D-077]`: 60 llamadas reales a claude-opus-5, 0 por
     encima del corte de 6,5 s, peor caso 3,91 s. Los dos cierres anteriores
     fallaron por apoyarse en un techo que no existia ([D-070], [L-054]) y en
     una medida que no medía la ruta entera ([L-043]).

     🔑 Y el cierre es CONDICIONADO: vale mientras Anthropic responda como el
     2026-08-14. Si vuelve la saturacion de `T-087`, se repite la tanda. La
     condicion esta escrita DENTRO de [D-077], no en el resumen de nadie. -->

### [A-007] 2026-08-04 — Entre el Paso 2b del cierre y el `git add` no se toca ningún `.ts`

- **Se supone que:** desde que el Paso 2b compila y compara, hasta que el Paso 6
  hace `git add -A`, **nadie edita un archivo `.ts`**. Si alguien lo editara, el
  control habría dado su veredicto sobre un `.js` que ya no se corresponde con la
  fuente que entra en el commit.
- **Por qué nace hoy:** hasta el 2026-08-04 el control corría pegado al `git add`,
  con solo un paso de por medio. Al moverlo arriba ([D-019]) quedan cuatro pasos
  en medio, y esa distancia es exactamente lo que hay que suponer limpio. **La
  suposición no existía antes; la creó el arreglo.**
- **Por qué hoy es cierta:** entre los dos puntos, el `session-closer` solo
  escribe `progress.md` y `tasks.md` — archivos `.md`. Y el protocolo le prohíbe
  expresamente escribir código: *"No escribas código ni arregles nada, aunque veas
  algo roto"*. Ninguna de las dos cosas es un accidente, pero ninguna está
  comprobada por una máquina: las dos son texto que alguien tiene que seguir.
- **Cómo se comprobaría:** guardar el hash de `frontend/*.ts` en el Paso 2b y
  volver a calcularlo justo antes del `git add`. Si cambió, la suposición es
  falsa. **No se implementa hoy:** sería una pieza nueva para un problema que
  todavía no ha ocurrido — PI-2.
- **Si es falsa:** el control da **verde sobre el archivo equivocado**, que es
  peor que no tenerlo. Un rojo se ve; un verde falso se cree. Es la familia de
  [L-006]: confundir "no lo comprobé" con "está bien", solo que aquí la confusión
  es "comprobé otra cosa".
- **Qué la haría caer:** que algún día el cierre gane un paso que toque código
  —recompilar, formatear, arreglar un lint— entre el Paso 2b y el commit. 🔑 **Si
  eso se propone, esta entrada es la que hay que releer antes de aceptarlo.**

### [A-006] 2026-08-03 — La ruta de `mktemp -d` de Git Bash le sirve a `node`

- **Se supone que:** el Paso 2b de `protocol-close` hace `OUT=$(mktemp -d)` y le
  pasa esa ruta a `node`. `mktemp` devuelve algo tipo `/tmp/tmp.lu0Fzd9e5G` —una
  ruta de estilo Unix— y `node` es un **binario de Windows**, que entiende
  `C:\...`. Se supone que la traducción que hace Git Bash en medio funciona
  siempre, no solo aquí.
- **Cómo se comprobaría:** correr el Paso 2b tal cual en **otra máquina**, o con
  otra versión de Git Bash o de Node. Si sale "SIN COMPROBAR" con el compilador
  instalado y `node_modules/` en su sitio, la suposición es falsa.
- **Si es falsa:** el control no compila nunca y cae siempre en la tercera fila,
  "SIN COMPROBAR". No da falsos verdes —eso está cubierto por diseño— pero deja
  de vigilar, avisando. El arreglo sería convertir la ruta con `cygpath -w`.
- **Medido aquí el 2026-08-03:** `mktemp -d` dio `/tmp/tmp.lu0Fzd9e5G`, `node`
  lo aceptó y `tsc` compiló con `exit=0`. Funciona en esta máquina; que funcione
  en general es lo que sigue sin comprobar.

### [A-002] 2026-08-02 — El marcador lo escribe un solo proceso a la vez

- **Se supone que:** en un momento dado hay **un solo proceso** escribiendo el
  archivo de una misma persona (`data/users/<nombre>.json`). Sobre eso descansa
  el candado `_SCORE_LOCK` de `app/tools.py`, que es lo que impide que dos
  escrituras a la vez pierdan puntos ([D-009]).
- 🔻 **2026-08-03 — el paso 4 ENCOGE esta suposición, no la amplía.** Antes había
  un solo archivo para todo el mundo, así que **cualquier** par de escrituras
  simultáneas podía chocar. Con un archivo por persona, dos personas distintas
  en dos procesos distintos ya **no** se pisan nunca: escriben en archivos
  distintos. Lo que queda es **la misma persona dos veces a la vez** —dos
  pestañas, dos dispositivos, o la terminal y el servidor a la vez— cayendo en
  procesos distintos. Más raro, y exactamente igual de silencioso cuando pasa.
- **Por qué está aquí:** un `threading.Lock` solo se ve dentro de **su** proceso.
  Dos procesos son dos candados que no se enteran el uno del otro, y el fallo
  vuelve entero. El candado no avisa: sigue pareciendo que funciona.
- **Las dos formas de romperlo, y la segunda es la probable:**
  1. Arrancar uvicorn con `--workers 2` o más. Es la que se ve venir.
  2. 🚨 **Tener `python main.py` abierto en una terminal y el servidor encendido
     en otra.** También son dos procesos, y esta es la que va a pasar de verdad:
     el `README.md` presenta las dos puertas una debajo de otra.
- **Comprobado que es real:** dos procesos sumando 200 puntos cada uno sobre el
  mismo archivo. De 400 esperados, el marcador guardó **169**, y **169** llamadas
  fallaron. Es el mismo fallo de antes de [D-009], sin arreglar y sin arreglo
  posible desde memoria.
- **Cómo se sostiene mientras tanto:** escrito en `README.md`, en "Cómo se
  corre", en los dos sitios: al presentar las dos puertas y al arrancar el
  servidor.
- **Si es falsa:** el candado de memoria no basta. Haría falta un candado del
  sistema de archivos —que lo ven todos los procesos— o sacar el marcador a algo
  que sepa contar solo, como una base de datos.
- ⚠️ **Vuelve a mirarse en el paso 7:** quien decide cuántos procesos hay en la
  nube es la plataforma, no nosotros. Ahí esta suposición deja de estar en
  nuestras manos.
  - ✏️ **2026-08-05 — eso ya no es cierto, y a favor.** `[D-029]` eligió EC2: una
    máquina nuestra, con un uvicorn que arrancamos nosotros. **Los procesos los
    seguimos decidiendo nosotros**, así que la suposición no se nos escapa de las
    manos como se temía. 🔑 En App Runner o Fargate sí habría pasado: esas
    plataformas arrancan más copias solas cuando llega gente, y esta suposición
    se habría roto **sin que nadie tocara nada**. Es el mismo mecanismo que la
    cuota efímera de `[D-029]` — otro freno que se rompe por lo que lo rodea.
  - ⚠️ Lo que queda vivo es la forma 2, la de verdad probable: `create_account.py`
    corriendo en la máquina **a la vez** que el servidor. Son dos procesos.

<!-- [A-001] MUERTA el 2026-08-13. Resultó FALSA y se fue a `[D-066]`.
     La prueba que pedía corrió sin buscarla: `I cooking in these morning`
     estaba mal y el marcador subió igual. No se deja copia aquí — una
     suposición en dos sitios acaba con una de las dos mintiendo. -->

<!-- La más reciente arriba. Formato:

### [A-001] 2026-08-02 — <qué se supone, en una línea>

- **Se supone que:** <la afirmación sin comprobar>
- **Cómo se comprobaría:** <la prueba concreta>
- **Si es falsa:** <qué se rompe>

-->
