# Avance — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [S-000]`. Búscala con `grep`, no leas el archivo entero.

## Estado actual

| | |
|---|---|
| **paso** | 7 de 9 — la cuenta de AWS sigue abierta desde `T-057` (2026-08-06). Tercer tramo del mismo día: una segunda auditoría externa corrigió que la métrica del presupuesto es coste **BRUTO** (visto en pantalla, no `NET_UNBLENDED_COST` como se había afirmado), cerró `[L-018]` sobre la frase falsa duplicada en cinco sitios, y selló por escrito el experimento de `[A-018]` **antes** de actuar. `[D-033]` fija la región en `us-east-1`. **Primer gasto real del proyecto:** una Elastic IP reservada en `us-east-1` (2026-08-06, 15:29 UTC, t=0 del experimento), sin instancia y sin asociar — 🚨 cobra por existir mientras siga suelta. ⚠️ Nada de `deploy/` se ha corrido nunca — sigue sin haber máquina EC2 |
| **última sesión** | 2026-08-06 (tercer tramo) |
| **siguiente acción** | Esperar uno o dos días y mirar **las dos cosas**: la factura (¿hubo coste bruto?) y la bandeja (¿llegó el correo?), leídas contra la tabla de veredictos de `[A-018]`. Con eso: **(1)** cerrar `[A-018]` o abrir el hallazgo de alarma rota; **(2)** decidir el umbral definitivo **con datos** — candidato ya anotado, $200 ÷ 6 meses ≈ $33/mes, que convertiría la alarma en vigilante del ritmo de quema de `[A-015]`; **(3)** entonces lanzar la instancia EC2 de `T-059` (segunda mitad), con `T-068` leída **antes** de entrar a la consola. 🚨 **No perder de vista mientras tanto:** la Elastic IP reservada hay que soltarla o asociarla al terminar el experimento — está cobrando por existir. ⏳ El umbral de $0,01 no se toca hasta el punto 2 |

## Índice

| id | fecha | qué avanzó | paso |
|---|---|---|---|
| S-020 | 2026-08-06 | Tercer tramo del día, después de `[S-019]`. Segunda auditoría externa del cierre `23a1ecb`: corrigió que el presupuesto mide coste **BRUTO** (leído en pantalla), no `NET_UNBLENDED_COST` como se había afirmado por error — la propia auditoría anterior lo reconoció. Consecuencia: los créditos no enmascaran el gasto, no hace falta un segundo presupuesto, y la EC2 encendida tiene que sonar. Corregida la frase "si no llega correo, la alarma está bien montada", duplicada en cinco sitios; `[L-018]` nueva sobre la duplicación por diseño de `_persistence/`. `[A-018]` cerró con un experimento **escrito por adelantado y commiteado antes de actuar** (`cfba50a`): disparador, dos observaciones separadas, tabla de tres veredictos. `[D-033]` fija la región `us-east-1` antes de tocar el selector (`9cc1b72`). `T-059` se partió: su primera mitad quedó hecha — Elastic IP reservada en `us-east-1`, sin instancia, t=0 sellado 2026-08-06 15:29 UTC (`3ff793e`) — primer gasto real del proyecto. Tres commits de esta sesión ya subidos a `origin` antes de este cierre. Ningún código tocado; solo `_persistence/` y `deploy/console_steps.md` | 7 |
| S-019 | 2026-08-06 | Segundo tramo del día, después del cierre que dejó `[S-018]`. Auditoría externa del commit `d811295`: confirmó historial público limpio (cero `.env`, `data/`, llaves, correo personal) y no pidió arreglar nada de código. Trajo tres puntos: `A-018` nueva en `assumptions.md` — la alarma de facturación protege del goteo pero no del acantilado de las 7 puertas de `[C-005]`, contra el que el único freno sigue siendo la lista de `T-068`; se comprobó que la lista de `T-068` ya es legible antes del primer clic de `T-059` (líneas 14-39 de `deploy/console_steps.md`) y no hizo falta cambiar nada; y se añadió una segunda alerta de coste **previsto** en el mismo presupuesto de AWS (antes solo había una de coste real), verificado en pantalla y documentado en `deploy/console_steps.md` paso 1. Hallazgo nuevo, no pedido por la auditoría: se anotó dentro de `A-018` que los $200 en créditos descuentan del cálculo del presupuesto (`IncludeCredit: true` según documentación de AWS) es lectura de documentación, no visto en pantalla. Ningún código tocado; solo `_persistence/assumptions.md` y `deploy/console_steps.md`. 🔴 **CORREGIDA el mismo día por una segunda auditoría:** esta sesión escribió que `A-018` se comprobaría con *"el silencio de la alarma en los días siguientes a `T-059`"*, y eso es falso — **el silencio no demuestra nunca que un control funcione**, y `T-059` no comprueba `A-018`: la destruye. El detalle, al final de la entrada | 7 |
| S-018 | 2026-08-06 | `T-057` completada: la cuenta de AWS quedó abierta de verdad, con MFA en el root en el mismo acto y alarma de facturación de 1 USD (umbral al 1%) con correo verificado. Fin del plan gratuito leído en pantalla: 2027-02-06 (`C-006` actualizada). Desviación registrada: se usó el correo personal sin el alias `+aws` de `D-031` — impacto nulo, el alias era organización, no seguridad. Camino de vuelta del MFA resuelto y probado en un segundo dispositivo (Contraseñas de Apple / Llavero de iCloud). Sin confirmar en documentación: cuántos dispositivos MFA admite el root. `deploy/console_steps.md` ganó el retraso de facturación (~24h, con fuente) y dónde leer fecha de fin y créditos. Siguiente: `T-059`, la EC2 | 7 |
| S-017 | 2026-08-05 | Tercer tramo del día: `T-058` completada. `teapp.duckdns.org` creado en DuckDNS, token guardado fuera del repo. El nombre ya coincidía con lo escrito en `deploy/`, así que no cambió ningún archivo de código ni de `deploy/`. Siguiente: `T-057`, abrir la cuenta de AWS | 7 |
| S-016 | 2026-08-05 | Segundo tramo del día, después del cierre de `S-015`. `A-017` nueva: DuckDNS comprobado por primera vez — existe, se entra con Google/GitHub/Reddit/Twitter, es gratuito y ha tenido caídas registradas (2026-06-21 y agosto 2025); si cae, Caddy no renueva el certificado y no entra nadie con la máquina encendida. Se aclaró que no hace falta cliente de DNS dinámico ni cron: la Elastic IP es fija, se apunta una vez. `deploy/console_steps.md` actualizado. Dos revisiones seguidas de `install.sh`: la primera cerró un falso verde (`systemctl is-active` no demuestra que la app conteste; ahora son tres comprobaciones: is-active, curl local, curl al dominio) y añadió que `.env` nazca con `install -m 600`; la segunda cazó el fallo simétrico que la primera trajo (sin reintentos para el curl HTTPS que espera a Let's Encrypt) y lo corrigió con 20 intentos cada 3 s. Las dos quedan como `L-017`. Ningún código Python se tocó; 310 tests siguen pasando, `bash -n install.sh` correcto. La cuenta de AWS sigue sin abrir | 7 |
| S-015 | 2026-08-05 | `T-068` cerrada en dos mitades: `A-016` comprobada y FALSA — leídas tres fuentes de AWS (FAQ del plan gratuito, Términos, documentación de facturación), las puertas al plan de pago no son tres, son **siete** (`C-005` reescrita). A media sesión se corrigió que las cinco puertas nuevas conservaran los créditos: la doc solo se moja con las dos primeras, de las otras cinco calla — se tratan como si evaporaran, denegar por defecto (`L-016`). `T-063` escrita: `deploy/` nueva con `console_steps.md` (incluida la lista "ESTO NUNCA SE TOCA"), `install.sh`, `teapp.service`, `Caddyfile.template`, `README.md`. `D-032` nueva: TEAPP corre como `ubuntu`, no como usuario propio. Orden acordado: `T-063` → `T-058` → `T-057`, porque escribir el documento de clics no gasta el reloj de los 6 meses. 310 tests (sin cambios, no se tocó código Python). ⚠️ Nada de `deploy/` se ha corrido nunca — no hay máquina. La cuenta de AWS sigue sin abrir | 7 |
| S-014 | 2026-08-05 | Plataforma del paso 7 cerrada (`D-029`): AWS + EC2 pequeña + Caddy + DuckDNS + IP fija, decidida por el disco (`data/` son archivos, un disco efímero evaporaría la cuota del paso 6). Cierre planeado del paso 7 definido, con ensayo de reconstrucción temprano (`D-030`). Forma de abrir la cuenta decidida: alias `+aws`, MFA en el root desde el minuto uno (`D-031`). Verificado contra documentación oficial: el plan gratuito de AWS cambió el 2025-07-15 (`C-003`), hay puertas que cruzan al plan de pago sin avisar y sin vuelta atrás (`C-005`, `C-006`), Let's Encrypt no emite para `compute.amazonaws.com`. Las 5 deudas fantasma del despliegue (`T-050`, `T-051`, `T-054`, `T-055`, `T-056`) consiguieron dueño concreto, y se sumaron 14 tareas nuevas (`T-057` a `T-070`). Ningún código se tocó: la sesión entera fue diseño y registro | 7 |
| S-013 | 2026-08-04 | `T-053` y `T-033` resueltas, dos deudas del paso 7 pagadas antes de abrir la nube. `app/login_guard.py` (nuevo): tope de intentos fallidos en `/login` por origen, en memoria, con barrido y 429 con `Retry-After` (`D-026`). `/register` cerrado por defecto tras `TEAPP_REGISTRATION_OPEN` (`D-027`); `create_account.py` (nuevo) crea cuentas sin teclado — `main.py` usa `getpass`, que en Windows se cuelga sin consola. `app/config.py` gana `configure_logging()`: hora, nivel y origen en cada renglón, `INFO` por defecto (`D-028`); cuota agotada y registro cerrado bajan a `info`, los intentos fallidos se quedan en `warning`. `A-012` retirada y partida en `A-013` y `A-014` (`L-014`); `L-012` se repitió dentro de su propio arreglo y se corrigió midiendo en otro proceso (`L-015`). De 257 a **310 tests pasando** | 7 |
| S-012 | 2026-08-04 | Paso 6 completo: los cuatro frenos de producción, `T-038` resuelta. `app/quota.py` (nuevo) cobra por persona y por día, con reloj y tope inyectados. `app/api.py` suma `MAX_SENTENCE_LENGTH` (422), timeout del tutor en `ThreadPoolExecutor` (504) y el motivo del frenazo en cada 429/504. Una revisión externa encontró cinco huecos y los cinco se cerraron: la carrera de medianoche en `spend`, el cobro por trabajo que nunca salió de la cola, el marcador subiendo tras un 504 (decidido, no arreglado), un `logger.info` que el handler de último recurso silenciaba, y `/login` sin tope de intentos (anotado como deuda con dueño). De 192 a **257 tests pasando**, `tests/test_quota.py` nuevo | 6 |
| S-011 | 2026-08-04 | T-047 resuelta: `[C-001]` medida de verdad. 192 tests verdes con la red cortada, 5 controles del portero verdes. Entra `tests/no_network.py` (portero, autouse), `tests/check_no_network.py` (sus controles) y el enganche en `tests/conftest.py` (`D-022`). Hueco cerrado: `connect_ex` atravesaba el portero. `[C-001]` reescrita: no prohíbe salir a internet, prohíbe salir **a buscar algo que falta** | 6 |
| S-010 | 2026-08-04 | Paso 5 completo: identidad verificada. `app/accounts.py` (credenciales con `scrypt`), `app/sessions.py` (cookie firmada con `hmac`), `app/config.py` (`.env`). `PracticeRequest` pierde `user`; `/register`, `/login`, `/logout`, `/me` nuevas. Pantalla e `main.py` piden contraseña. 192 tests pasando, corrida real con uvicorn+curl, y un fallo real de `/logout` cazado y arreglado (`L-010`) | 5 |
| S-009 | 2026-08-04 | T-049 resuelta: el control del `.js` se mueve del Paso 5b al Paso 2b de `protocol-close` (antes de escribir `tasks.md`); el resultado del push queda escrito como imposibilidad lógica, no como pendiente. `protocol-start` pasa de `git status --short` a `-sb` — el primero no imprimía la línea de la rama | 5 |
| S-008 | 2026-08-03 | T-037 resuelta: nuevo Paso 5b en `protocol-close` comprueba que `app/static/app.js` es el compilado de `frontend/app.ts`, disparado desde `session-closer` antes del commit. `test_the_compiled_script_is_served` se renombró y ya dice qué no mide. Primera corrida real del Paso 5b: verde, `.js` al día | 3 |
| S-007 | 2026-08-03 | Paso 4 completo: marcador por persona en `data/users/<nombre>.json`, `normalize_user` con cuatro frenos, `data/score.json` global borrado, 121 tests pasando | 4 |
| S-006 | 2026-08-03 | Paso 3 completo: `index.html` + `app.ts` compilado, FastAPI sirve la pantalla en el mismo origen, CORS descartado (T-029), 57 tests pasando | 3 |
| S-005 | 2026-08-02 | Paso 2 completo: `app/api.py` con FastAPI, `respond` devuelve `TutorReply`, dos fallos de concurrencia arreglados, 53 tests pasando | 2 |
| S-004 | 2026-08-02 | Dos arreglos de robustez sobre el paso 1: marcador roto y `count_words` con no-texto, 30 tests pasando | 1 |
| S-003 | 2026-08-02 | Paso 1 completo: agente FALSO con 3 herramientas, 14 tests pasando | 1 |
| S-002 | 2026-08-02 | Cierre del paso 0: T-006 a T-009 resueltas | 0 |
| S-001 | 2026-08-02 | Repositorio y esqueleto completos | 0 |

---

## Entradas

### [S-020] 2026-08-06 — Segunda auditoría: métrica del presupuesto corregida, experimento de `A-018` sellado, `T-059` partida

- **Paso:** 7 de 9 — sigue sin haber instancia EC2. Tercer tramo del mismo día,
  después del cierre que dejó `[S-019]` (commit `23a1ecb`). Esta sesión hizo sus
  propios commits mientras trabajaba, a propósito: `cfba50a`, `9cc1b72`,
  `3ff793e`, los tres ya subidos a `origin` antes de este cierre. `git status`
  al empezar este cierre: árbol limpio.
- **Quedó funcionando (registrado, no código):**
  - Una segunda auditoría externa corrigió la primera: había afirmado que la
    métrica por defecto de un presupuesto de coste es `NET_UNBLENDED_COST`;
    era un ejemplo de la documentación de la API, no un valor por defecto. Se
    comprobó en pantalla: el presupuesto mide **coste BRUTO** (`Costes
    agregados por` = "costes sin combinar"). Consecuencia directa: los
    créditos NO enmascaran el gasto, NO hace falta un segundo presupuesto, y
    la EC2 encendida **tiene que** hacer sonar la alarma.
  - Corregida la frase falsa "si no llega correo, la alarma está bien
    montada", que vivía en cinco sitios: `progress.md` (entrada `[S-019]`, su
    fila de índice y "Estado actual"), dos puntos de `[A-018]`, y
    `deploy/console_steps.md`. La peor de las cinco era nueva, escrita por la
    sesión anterior en tono tranquilizador ("los $200 descuentan, así que el
    coste debería quedarse en cero") sobre un presupuesto que, de ser cierto,
    no podría saltar nunca.
  - `[L-018]` nueva: "en este proyecto los datos se replican solos, y corregir
    uno no corrige los demás" — tercera vez con el mismo bicho. La lección
    trae su propio control: un `grep` antes de dar la corrección por hecha,
    que aquí encontró dos copias más ya obsoletas.
  - `[A-018]` ganó el experimento escrito **por adelantado**, con disparador
    (reservar solo la Elastic IP), dos observaciones separadas (la factura =
    premisa, la bandeja = prueba) y tabla de lectura con tres veredictos.
    Sellado en `cfba50a`, antes de tocar la consola: una predicción sin
    commitear es un borrador editable después de ver el resultado.
  - Corregida otra afirmación sin comprobar de la sesión principal: "va a
    sonar todos los días durante seis meses". No está verificado si una
    alerta se repite mientras el umbral siga superado. Por eso el umbral de
    $0,01 **no se toca todavía** — cambiarlo arreglaría un problema predicho y
    destruiría el experimento capaz de confirmarlo. Anotado de dónde saldrá
    el definitivo: $200 ÷ 6 meses ≈ $33/mes.
  - `[D-033]` nueva: la región. La consola traía `us-east-2` (Ohio) por
    defecto, sin que nadie la hubiera elegido. Se decidió y se **escribió**
    `us-east-1` (Norte de Virginia) antes de tocar el selector (`9cc1b72`),
    porque es la región que `[A-015]` ya asume en su tabla de precios. Los
    precios entre regiones NO se compararon — queda dicho en la propia
    entrada.
  - `T-059` se partió y su primera mitad quedó **hecha**: se reservó una
    Elastic IP en `us-east-1`, sin instancia y sin asociar (`3ff793e`). Es el
    disparador del experimento. t=0 sellado: 2026-08-06, 15:29 UTC. La cuenta
    estaba en $0,00 y cero recursos justo antes. **Es el primer gasto real del
    proyecto.**
  - Hallazgo bueno que confirmó la auditoría: `[A-015]` ya decía desde el
    2026-08-05 que AWS cobra por cada IPv4 pública, esté o no en uso, del
    orden de $3-4/mes. La predicción de que la IP ociosa cobra es de dos días
    antes, tomada por otro motivo.
  - 🚨 **Pendiente que no se puede olvidar:** la Elastic IP está reservada y
    sin usar — cobrando por existir. Hay que soltarla o asociarla al terminar
    el experimento.
- **Verificado:** no hay tests que correr — sesión de consola de AWS y de
  documentación, no de código. Paso 2b de este cierre: `.js` compilado, al día
  (`compilar: 0`, `comparar: 0`) — no había ningún `.ts` tocado.
- **Siguiente paso concreto:** esperar uno o dos días y mirar la factura y la
  bandeja de correo, leídas contra la tabla de `[A-018]`. Después: decidir el
  umbral definitivo con datos, y solo entonces lanzar la instancia EC2 con
  `T-068` leída antes de entrar.

### [S-019] 2026-08-06 — Auditoría del cierre de `T-057`: dos alertas de coste, `A-018` nueva

- **Paso:** 7 de 9 — sigue sin lanzarse la EC2. Segundo tramo del día, después
  del cierre que dejó `[S-018]` (commit `d811295`). `git status` de esta sesión
  muestra solo dos archivos: `_persistence/assumptions.md` y
  `deploy/console_steps.md`. Ningún código tocado.
- **Quedó funcionando (registrado, no código):**
  - Una auditoría externa revisó el commit `d811295` y su ejecución: confirmó
    que el historial público está limpio (cero `.env`, `data/`, `.pem`, `.key`,
    cero llaves, cero apariciones del correo personal) y que `progress.md` y
    `tasks.md` ya daban `T-057` por cerrada. No pidió arreglar nada de código.
  - `A-018` nueva en `assumptions.md`: "la alarma de facturación avisará el día
    que haga falta" está creada pero nunca se ha visto saltar. Central de la
    entrada: la alarma protege del **goteo** pero NO del **acantilado** de las
    siete puertas de `[C-005]`, que evaporan créditos "en el acto"; contra eso
    el único freno es la lista de `T-068`. Incluye una calibración gratis que
    caduca al lanzar la EC2 de `T-059`.
  - Se comprobó la legibilidad de la lista de `T-068` antes del primer clic de
    `T-059`: ya es la primera sección de `deploy/console_steps.md` (líneas
    14-39), antes de todos los pasos. **Cero cambios** — `PI-3`.
  - Alerta de coste **previsto** añadida en la consola de AWS y verificada en
    pantalla, junto a la de coste **real** que ya existía: dos alertas en UN
    solo presupuesto (no dos presupuestos), ambas a 0,01 US$ absoluto, al
    mismo correo. Verificado en la API de AWS que un mismo `budget` admite
    `NotificationType: ACTUAL` y `FORECASTED`. Documentado en
    `deploy/console_steps.md` paso 1, con el porqué de que sean dos.
    `Costes agregados por` se dejó en el valor por defecto ("costes sin
    combinar") por `PI-3`.
  - Hallazgo nuevo, no traído por la auditoría, anotado dentro de `A-018`: se
    da por cierto que los $200 en créditos **descuentan** del cálculo del
    presupuesto (`IncludeCredit` viene en `true` según la documentación de
    AWS, consultada 2026-08-06) — lectura de documentación, no visto en
    pantalla. Si fuera falsa, la alarma sonaría a diario con la EC2 encendida
    aunque los créditos lo paguen todo. Se comprueba gratis en los días
    siguientes a `T-059`: silencio = confirmada.
  - También quedó anotado, sin verificar, si AWS puede proyectar coste
    previsto sin historial — la cuenta se abrió ayer y no tiene gasto previo;
    no se encontró en la documentación.
- **Verificado:** no hay tests que correr — sesión de consola de AWS y de
  documentación, no de código. Paso 2b de este cierre: `.js` compilado, al día
  (`compilar: 0`, `comparar: 0`) — no había ningún `.ts` tocado.
- **Siguiente paso concreto:** `T-059` — lanzar la instancia EC2 `t3.micro`
  con Elastic IP y apuntar `teapp.duckdns.org` a esa IP. Es el primer paso que
  consume créditos de verdad, y ahora también el experimento que comprueba
  `A-018` entera.

#### 🔴 CORREGIDO el 2026-08-06 por una segunda auditoría — no se borra lo de arriba

> 📌 **Se corrige el porqué, no se reescribe la historia.** Lo de arriba queda
> como se escribió; aquí está por qué estaba mal. Mismo gesto que en `[L-008]`.

- **La frase falsa:** *"se comprueba gratis en los días siguientes a `T-059`:
  silencio = confirmada"*, y su gemela del último punto, *"el experimento que
  comprueba `A-018` entera"*.
- 🚨 **Por qué es falsa:** **el silencio no demuestra nunca que un control
  funcione.** No llega correo si la alarma está bien, y tampoco llega si el
  correo está mal escrito, si la alarma se borró sin querer, o si el umbral no
  puede alcanzarse. Es `[L-013]` en versión alarma: verde porque **no existe
  nada capaz de ponerlo rojo**, no porque algo se haya comprobado.
- **Y `T-059` NO comprueba `A-018`.** Lanzar la EC2 no es el experimento: es
  justo lo que **destruye** el experimento. Hoy, con cero máquinas encendidas,
  el silencio todavía distingue "no hay gasto" de "la alarma está rota". En
  cuanto exista la instancia, deja de distinguirlo y no vuelve nunca.
- ✅ **Lo que sí comprueba `A-018`, y es gratis:** bajar el listón hasta que la
  alarma tenga que morder — un presupuesto **de prueba** con el umbral por
  debajo de lo ya gastado, que dispara solo y manda el correo de verdad. Prueba
  a la vez las tres cosas: que la dirección es correcta, que no cae en spam y
  que el mecanismo anda. Después se borra. Es el mismo sabotaje de `[S-013]`,
  aplicado a una alarma en vez de a una función.
- ⚠️ **Y queda una contradicción abierta que hay que MIRAR, no suponer:** si el
  presupuesto mide coste **neto** (después de créditos), la alarma tampoco
  vigila el goteo — una máquina olvidada quemaría los $200 en silencio y el
  primer aviso llegaría cuando ya no quede nada. La auditoría afirma que el
  valor por defecto es `NET_UNBLENDED_COST`; **la pantalla del 2026-08-06 mostró
  "costes sin combinar"**, que es la opción bruta, con "costes netos sin
  combinar" como opción distinta y no seleccionada. **No coinciden.** Se
  resuelve abriendo el presupuesto y leyendo el valor literal.
- **Orden que queda fijado, y ninguno de los tres primeros gasta un céntimo:**
  mirar la métrica → montar el presupuesto de prueba y ver el correo llegar →
  (si la métrica es neta) añadir un presupuesto sobre coste bruto → **y solo
  entonces** `T-059`.

### [S-018] 2026-08-06 — `T-057` completada: la cuenta de AWS está abierta

- **Paso:** 7 de 9 — el reloj irreversible de 6 meses (`C-006`) arrancó hoy. `git
  status` de esta sesión muestra solo tres archivos de `_persistence/` y
  `deploy/`; abrir la cuenta es una acción de navegador, no deja diff propio.
- **Quedó funcionando (registrado, no código):**
  - Cuenta de AWS abierta con plan gratuito. MFA activado en el usuario root en
    el mismo acto, como pedía `D-031`.
  - Alarma de facturación creada: presupuesto de 1 USD con alerta al 1% (= 0,01
    USD de coste real), correo destinatario configurado y verificado.
  - Fecha de fin del plan gratuito leída en la portada de la consola:
    **185 días — 2027-02-06**. Va a `C-006`, dato de pantalla, no calculado.
  - Retraso de los datos de facturación: ~24 horas, confirmado por
    documentación de AWS y por el propio aviso en la consola. Va a
    `deploy/console_steps.md`, paso 1.
  - Camino de vuelta del MFA resuelto y **probado**: la semilla está en la app
    Contraseñas de Apple, sincronizada por el Llavero de iCloud; se verificó
    que el código aparece y rota en un segundo dispositivo (iPad).
  - ⚠️ **Desviación de `D-031`:** la cuenta se abrió con el correo personal SIN
    el alias `+aws`. Impacto nulo — el alias era organización, no seguridad ni
    elegibilidad — pero queda anotado en la propia entrada de `D-031`.
  - ⚠️ **Sin confirmar:** cuántos dispositivos MFA admite el root. No salió en
    la documentación consultada; queda anotado como no verificado, no escrito
    de memoria.
  - 🚨 El correo literal de la cuenta de AWS no aparece en ningún archivo del
    repo — verificado antes de este commit.
- **Verificado:** no hay tests que correr — es una cuenta externa. Paso 2b de
  este cierre: `.js` compilado, al día (`compilar: 0`, `comparar: 0`) — no
  había ningún `.ts` tocado hoy.
- **Siguiente paso concreto:** `T-059` — lanzar la instancia EC2 `t3.micro` con
  Elastic IP y apuntar `teapp.duckdns.org` a esa IP. Es el primer paso del
  paso 7 que consume créditos de verdad.

### [S-017] 2026-08-05 — `T-058` completada: `teapp.duckdns.org` creado

- **Paso:** 7 de 9 — sigue sin abrir la cuenta de AWS (regla 4). Tercer tramo
  del día, después de `[S-016]`. Sesión de navegador, no de código: **no hay
  `git diff`** — `git status` sale limpio antes de este cierre.
- **Quedó funcionando (registrado, no código):**
  - El subdominio gratuito `teapp.duckdns.org` existe de verdad. El token de
    DuckDNS quedó guardado por el usuario fuera del repo — no se compartió en
    el chat, no está en ningún archivo y no se anota aquí ni en ningún otro
    archivo de `_persistence/`.
  - El nombre coincide **exactamente** con el que ya esperaban
    `deploy/install.sh`, `deploy/Caddyfile.template` y
    `deploy/console_steps.md`, escritos el 2026-08-05 en `[S-015]`. Por eso no
    hizo falta tocar nada de `deploy/` ni de código.
- **Verificado:** nada que correr — es una cuenta externa, no un artefacto en
  este repo. `git status` limpio de principio a fin de este tramo.
- **Siguiente paso concreto:** `T-057` — abrir la cuenta de AWS, con la alarma
  de facturación y el MFA en el root como primer clic (`D-031`). Arranca el
  reloj irreversible de 6 meses (`C-006`); el usuario prefirió no abrirla hoy
  para no gastarlo. `T-069` (ensayo de reconstrucción) sigue bloqueada hasta
  entonces: necesita la máquina encendida.

### [S-016] 2026-08-05 — DuckDNS comprobado (`A-017`); `install.sh` revisado dos veces (`L-017`)

- **Paso:** 7 de 9 — sigue sin abrir la cuenta de AWS (regla 4). Segundo tramo
  del día, después del cierre que dejó `[S-015]` y el commit `efd853a`. Tres
  commits nuevos: `732404a`, `cfe074c`, `956ac83`. Ningún código Python se
  tocó; el `git diff` es de `deploy/` y de `_persistence/`.
- **Quedó funcionando (registrado, no código):**
  - `A-017` nueva: se comprobó por primera vez, en vez de heredarlo, que
    `duckdns.org` existe de verdad — se entra con Google, GitHub, Reddit o
    Twitter y da un token. Queda anotado que es gratuito, se sostiene con
    donaciones y tiene caídas registradas (2026-06-21, y un episodio en
    agosto de 2025); si deja de resolver, Caddy no renueva el certificado, la
    cookie `Secure` no viaja y no entra nadie, con la máquina encendida y los
    tests en verde.
  - Aclarado en `deploy/console_steps.md`: no hace falta cliente de
    actualización de DNS dinámico ni cron en el servidor, porque la Elastic
    IP es fija — se apunta el nombre una vez.
  - Primera revisión de `install.sh` (`cfe074c`): el bloque final citaba
    PI-4 y solo miraba `systemctl is-active`, que demuestra que systemd lanzó
    el proceso, no que la app conteste. Arreglado con tres comprobaciones
    (is-active, curl a `127.0.0.1:8000`, curl al dominio), mensaje final de
    "Listo" a "Comprobado", y `.env` que nace con `install -m 600` en vez de
    nacer abierto.
  - Segunda revisión (`956ac83`): al arreglar el falso verde se coló el
    fallo simétrico — 10 reintentos para el curl que espera a uvicorn
    (segundos) y ninguno para el que espera a Let's Encrypt (decenas de
    segundos). Arreglado con un bucle de 20 intentos cada 3 s para el HTTPS.
    Anotado también que la ruta del curl es `/` a propósito, no `/me`
    (verificado en `app/api.py:523` y `app/api.py:517`).
  - Las tres piezas de `install.sh` quedan bajo una sola lección, `L-017`: un
    falso verde y un falso rojo son el mismo error — no haber pensado cuándo
    es válido preguntar.
- **Verificado:** 310 tests pasando (sin cambios, no se tocó código Python),
  `bash -n deploy/install.sh` correcto. ⚠️ Nada de `deploy/` se ha corrido
  nunca — no hay máquina. La cuenta de AWS sigue sin abrir; el reloj de los 6
  meses no ha arrancado.
- **Siguiente paso concreto:** `T-058` — sacar `teapp.duckdns.org` en DuckDNS
  y guardar el token. Es de navegador, no necesita cuenta de AWS y no gasta
  reloj.

### [S-015] 2026-08-05 — `T-068` cerrada: siete puertas, no tres; `deploy/` escrita (`T-063`)

- **Paso:** 7 de 9 — sigue sin abrir la cuenta de AWS (regla 4). Ningún código
  Python se tocó; el `git diff` es de `_persistence/` y de la carpeta nueva
  `deploy/`.
- **Quedó funcionando (registrado, no código):**
  - `A-016` se cerró, comprobada y **FALSA**: leídas tres fuentes de AWS (FAQ
    del plan gratuito, Términos, documentación de facturación), las puertas que
    pasan la cuenta al plan de pago no son tres: son **siete** (Organizations,
    Control Tower, Partner Network, Professional Services, Enterprise
    Agreement, Skill Builder Team, HIPAA/SEC). `C-005` reescrita con la lista
    completa y la columna 💀/❓.
  - Corrección a media sesión: se había escrito que las cinco puertas nuevas
    conservaban los créditos. La documentación no lo dice — solo se moja con
    Organizations y Control Tower; de las otras cinco calla. Corregido a "la
    doc calla" y tratadas como si evaporaran (denegar por defecto). También se
    corrigió que "las tres fuentes repiten la misma frase": cierto para la
    lista de siete, falso para el matiz de los créditos (`L-016`).
  - `deploy/` (nueva, cinco archivos): `console_steps.md` (los clics, incluida
    la lista "ESTO NUNCA SE TOCA", que es la segunda mitad de `T-068`),
    `install.sh`, `teapp.service`, `Caddyfile.template`, `README.md`.
    `bash -n install.sh` sin errores. ⚠️ **Nada de esto se ha corrido nunca**:
    no hay máquina.
  - `D-032` nueva: TEAPP corre en la nube como el usuario `ubuntu`, no como un
    usuario propio sin permisos — por el mismo `data/` que escriben
    `create_account.py` y el servidor.
  - Orden de trabajo acordado: `T-063` → `T-058` → `T-057`, en vez de abrir la
    cuenta primero — escribir el documento de clics no necesita nube y no gasta
    reloj de los 6 meses.
  - Tests: **310 pasando**, sin cambios respecto a `S-013` — no se tocó código
    Python.
  - `_persistence/constraints.md`: `C-005` reescrita.
    `_persistence/assumptions.md`: `A-016` retirada (comprobada, falsa).
    `_persistence/lessons.md`: `L-016` nueva. `_persistence/decisions.md`:
    `D-032` nueva.
  - Paso 2b de este cierre: `.js` compilado, al día (`compilar: 0`,
    `comparar: 0`) — no había ningún `.ts` tocado hoy.
- **Siguiente acción:** `T-058` — sacar el nombre gratuito en DuckDNS
  (`teapp.duckdns.org`), que no necesita cuenta de AWS.

### [S-014] 2026-08-05 — La plataforma del paso 7 queda cerrada: AWS + EC2 + Caddy + DuckDNS + IP fija

- **Paso:** 7 de 9 — sigue sin abrir la cuenta de AWS (regla 4 de `CLAUDE.md`),
  pero su diseño entero quedó decidido y registrado. Ningún código se tocó hoy;
  el `git diff` es solo de `_persistence/`.
- **Quedó funcionando (registrado, no código):**
  - `D-029`: la plataforma — AWS + EC2 `t3.micro` + Caddy + nombre gratuito de
    DuckDNS + Elastic IP —, decidida por una sola columna: `data/` son
    archivos, y solo EC2 da un disco que persiste sin cambiar una línea de
    TEAPP. Lambda y App Runner/Fargate quedaron descartados por disco efímero.
    Con esto `T-054` (tope de cuerpo) y `T-055` (origen real) dejan de ser
    deudas fantasma.
  - Verificado contra documentación oficial, no de memoria: el plan gratuito
    de AWS cambió el 2025-07-15 — 6 meses y $200 en créditos, sin las 750
    horas de EC2 (`C-003`) —; y Let's Encrypt se niega por política a emitir
    certificados para `compute.amazonaws.com`, de ahí el nombre de DuckDNS.
  - `C-005` y `C-006`: hay acciones (AWS Organization, Control Tower, Partner
    Network) que cruzan la cuenta al plan de pago sin pedir confirmación y sin
    vuelta atrás, y el regalo es uno por persona en toda la vida, no por
    cuenta ni por proyecto.
  - `D-030`: el paso 7 termina con un cierre planeado, no con la cuenta
    muriéndose sola, y con un ensayo de reconstrucción **temprano**
    (`T-069`) como única prueba real de que `deploy/` sirve.
  - `D-031`: la cuenta se abre con un alias `+aws` del correo personal y MFA
    en el root en el mismo acto — el correo literal no se escribe en el repo,
    que es público.
  - Las cinco deudas fantasma del paso 7 (`T-050`, `T-051`, `T-054`, `T-055`,
    `T-056`) pasaron de "sin dueño" a tener una pieza concreta de la
    plataforma detrás. Se sumaron 14 tareas nuevas, `T-057` a `T-070`: el paso
    7 completo queda en 19 tareas.
  - `_persistence/decisions.md`: `D-029`, `D-030`, `D-031`.
    `_persistence/constraints.md`: `C-003`, `C-004`, `C-005`, `C-006`.
    `_persistence/assumptions.md`: `A-015` y `A-016` nuevas; `A-005` encogida;
    `A-002` corregida.
  - Paso 2b de este cierre: `.js` compilado, al día (`compilar: 0`,
    `comparar: 0`) — aunque hoy no había ningún `.ts` tocado, sigue el
    procedimiento igual.
- **Siguiente acción:** `T-057` — abrir la cuenta de AWS, con la alarma de
  facturación como primer clic (umbral: cualquier cargo distinto de cero).
  ⚠️ Antes de ese clic, cerrar `A-016` con `T-068`: leer entera la
  elegibilidad de la FAQ de AWS, porque la lista de "esto nunca se toca" puede
  estar incompleta.

### [S-013] 2026-08-04 — Dos deudas del paso 7 pagadas por adelantado: tope de intentos y log configurado

- **Paso:** 7 de 9 — no ha empezado el despliegue, pero se adelantaron dos de
  sus deudas de `S-012`.
- **Quedó funcionando:**
  - `app/login_guard.py` (nuevo): tope de intentos fallidos contra `/login`,
    contado por origen de la petición (no por persona) en un `dict` en memoria,
    con candado, barrido de lo vencido y 429 con cabecera `Retry-After`. La
    contraseña correcta tampoco abre mientras el origen esté cerrado (`D-026`,
    `T-053`).
  - `/register` cerrado por defecto tras `TEAPP_REGISTRATION_OPEN` (`false` por
    defecto). `create_account.py` (nuevo): crea cuentas desde la terminal sin
    esperar teclado — `main.py` usa `getpass`, que en Windows lee de la consola
    y se cuelga con la entrada por tubería (`D-027`).
  - `app/config.py` gana `configure_logging()`, llamada al importar
    `app/api.py`: hora, nivel y origen en cada renglón, `INFO` por defecto,
    `TEAPP_LOG_LEVEL` para ajustarlo. Sin `force=True` a propósito, para no
    pisar el handler de `caplog` bajo pytest (`D-028`, `T-033`). Cuota agotada y
    registro cerrado bajan de `warning` a `info`; los intentos fallidos se
    quedan en `warning` porque es el único rastro que sobrevive a un reinicio
    del contador en memoria.
  - `A-012` se retiró al cumplirse su propia condición de cierre, y al
    retirarla se vio que eran dos suposiciones pegadas: se partió en `A-013`
    (los números del freno) y `A-014` (que el origen leído sea el real) —
    `L-014`.
  - `L-012` se repitió dentro de su propio arreglo: el primer test de
    `configure_logging` vaciaba los handlers del logger raíz en un fixture, y
    `caplog` los repone después de los fixtures — medía el estado de pytest, no
    la función. Se arregló midiendo en un subproceso nuevo — `L-015`.
  - Tests: de 257 a **310 tests pasando** (`python -m pytest`, según los
    mensajes de los dos commits de hoy).
  - `_persistence/decisions.md`: `D-026`, `D-027`, `D-028`.
    `_persistence/assumptions.md`: `A-012` retirada, `A-013` y `A-014` nuevas.
    `_persistence/lessons.md`: `L-014`, `L-015`.
- **Siguiente acción:** Empezar el paso 7 del roadmap — la nube. Alarma de
  facturación primero. Revisar antes las deudas que quedan: `T-054`, `T-046`,
  `T-050`, `T-051`, `T-052`, `T-055`, `T-056`.

### [S-012] 2026-08-04 — Paso 6 completo: los cuatro frenos de producción

- **Paso:** 6 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/quota.py` (nuevo): cuota diaria por persona en `data/quota/<nombre>.json`.
    Reloj (`now`), tope (`limit`) y carpeta (`quota_dir`) inyectados, resueltos
    dentro de cada función y no en la firma. `today()` exige zona horaria y usa
    un offset fijo −05:00 (`D-024`) — `ZoneInfo("America/Bogota")` revienta en
    Windows, comprobado. `spend()` cobra **antes** de llamar al tutor (`D-023`)
    y `refund()` devuelve solo lo que nunca llegó a empezar. Candado sobre leer
    y escribir juntos, como `add_point`.
  - `app/api.py`: `MAX_SENTENCE_LENGTH = 500` (422 con cuánto llegó y cuánto
    cabe). El tutor corre en un `ThreadPoolExecutor(max_workers=40)` propio
    (`_TUTOR_POOL`), con `TUTOR_TIMEOUT_SECONDS = 10.0` — pasado ese tiempo,
    504, y `future.cancel()` decide si se devuelve la cuota (nunca empezó) o se
    queda cobrada (ya estaba corriendo). Los 429 y 504 llevan el motivo en la
    respuesta: cuánto se gastó, el tope, el día.
  - Una revisión externa encontró cinco huecos, cerrados los cinco:
    1. La carrera de medianoche en `spend` — preguntaba el día dos veces y
       podía escribir bajo el día viejo. Arreglado preguntándolo una sola vez.
    2. El cobro por trabajo que nunca salió de la cola del pool —
       `result(timeout=)` cuenta desde que se llama, no desde que arranca.
       Medido: 23 peticiones a la vez, 20 llegaron al tutor, 3 pagaron un 504
       por nada. Arreglado con `future.cancel()` + `refund()`.
    3. El marcador sube después del 504 si el tutor ya había empezado —
       **decidido dejarlo así** (el marcador cuenta frases practicadas,
       `A-001`), ahora escrito y con test.
    4. Un `logger.info` que el handler de último recurso de Python silencia
       (`L-012`, cierra `A-003`) — se sube a `warning`.
    5. `/login` sin tope de intentos — anotado como deuda con dueño para el
       paso 7 (`D-025`, `A-012`), no arreglado hoy.
  - Tests: de 192 a **257** pasando (`python -m pytest`, corrido en este
    cierre). `tests/test_quota.py` nuevo. `tests/conftest.py` desvía
    `quota.QUOTA_DIR` a una carpeta temporal.
  - `_persistence/decisions.md`: `D-023`, `D-024`, `D-025`.
    `_persistence/assumptions.md`: `A-010`, `A-011`, `A-012`; `A-003` ascendió a
    `lessons.md` (`L-012`) y salió de aquí. `_persistence/lessons.md`: `L-012`,
    `L-013`. `_persistence/constraints.md`: `C-002`.
  - Paso 2b de este cierre: `.js` compilado, al día (`compilar: 0`,
    `comparar: 0`).
  - **Seguimiento del mismo paso 6:** el `TUTOR_POOL_SIZE = 40` de `app/api.py`
    ya no heredaba el número de la máquina, pero sí seguía heredando la RAZÓN
    del número: el 40 es correcto solo porque el limitador de hilos por defecto
    de `anyio` —el que usa FastAPI para las rutas `def`— trae 40 fichas.
    Medido: `anyio 4.14.2 -> total_tokens = 40`. Y `anyio` no está fijado en
    `requirements.txt` (comprobado: no aparece), entra de rebote con `fastapi`.
    Una subida de FastAPI podía romper en silencio el invariante "la cola del
    tutor nunca es el cuello de botella", y con él volvía el cobro por espera
    de `L-013`. Nuevo test `test_the_pool_matches_the_threads_fastapi_actually_uses`
    en `tests/test_api.py`, medido en los dos sentidos (verde con anyio en 40,
    rojo simulando 15). El comentario de `TUTOR_POOL_SIZE` en `app/api.py`
    nombra `anyio` y apunta al test. `_persistence/lessons.md`: `L-013` gana un
    bullet de cierre. De 257 a **258** tests pasando; los 5 controles del
    portero de red, verdes. Paso 2b de este cierre: `.js` compilado, al día
    (`compilar: 0`, `comparar: 0`).
- **Siguiente acción:** Empezar el paso 7 del roadmap — la nube. ⚠️ Alarma de
  facturación primero, luego subir. Revisar antes las deudas con dueño:
  `T-053`, `T-054`, `T-033`, `T-046`, `T-050`, `T-051`, `T-052`.

### [S-011] 2026-08-04 — T-047 resuelta: `[C-001]` medida de verdad, con un portero que la vigila cada día

- **Paso:** 6 (deuda de restricción, no de la app) — no mueve el paso general,
  que sigue en 5 completo.
- **Quedó funcionando:**
  - `tests/no_network.py` (nuevo): el portero. Parchea `socket` para que
    cualquier intento de salir a la red reviente en el momento, activo en
    **todos** los tests vía el enganche `autouse` de `tests/conftest.py`.
  - `tests/check_no_network.py` (nuevo): sus cinco controles, fuera de la
    corrida normal de `pytest` a propósito — salen a internet de verdad si el
    portero falla, y eso es justo lo que `C-001` prohíbe.
  - Hueco cerrado: `connect_ex` (devuelve código, no lanza) atravesaba el
    portero sin que se enterara. Parcheado y verificado con una IP literal.
  - Límite escrito en el docstring del portero: no ve subprocesos —`node` y
    `git` son otro proceso, y eso es por construcción, no un pendiente.
  - **Medición del 2026-08-04:** 192 tests verdes con la red cortada; los 5
    controles del portero, verdes. `node_modules/typescript/bin/tsc` en disco
    (v7.0.2), sin descarga.
  - `[C-001]` reescrita: la redacción vieja ("nada de lo que corre en el cierre
    toca la red") era falsa desde que el `git push` entró en el cierre
    (`D-016`) — un push va a GitHub por internet. La nueva dice lo que de
    verdad se quiso decir: "nada sale a internet a buscar algo que le falta".
  - `_persistence/decisions.md`: `D-022` (el portero entra al repo, y con sus
    controles; `C-001` se mide en dos mitades porque el portero no ve
    subprocesos). `_persistence/constraints.md`: `C-001` corregida.
- **Siguiente acción:** Empezar el paso 6 del roadmap — frenos de producción:
  tope de peticiones por persona y por día, timeouts (`T-038`).

### [S-010] 2026-08-04 — Paso 5 completo: identidad verificada

- **Paso:** 5 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/accounts.py` (nuevo): almacén de credenciales en `data/accounts.json`,
    `hashlib.scrypt` con sal por persona, `hmac.compare_digest` al comparar.
  - `app/sessions.py` (nuevo): cookie firmada con `hmac`, caducidad de una
    semana.
  - `app/config.py` (nuevo): lector de `.env`, `require_secret()` y
    `cookie_secure()`.
  - `app/api.py`: rutas nuevas `/register` (201), `/login` (200), `/logout`
    (204) y `/me`; `PracticeRequest` pierde el campo `user` — quien practica
    sale de la cookie firmada (`_current_user`), y no de ningún otro sitio.
  - `frontend/app.ts` + `app/static/index.html`: la casilla "Your name" y el
    `localStorage` del paso 4 desaparecen; entra el formulario de inicio de
    sesión (`signin-form`) y la sección "signed-in". Recompilado a
    `app/static/app.js` — comprobado al día en este cierre (Paso 2b:
    `compilar: 0`, `comparar: 0`).
  - `main.py`: la terminal pide contraseña con `getpass`, cerrando la puerta
    de atrás que creaba marcadores sin credencial.
  - `.env.example`, `README.md`: documentan `TEAPP_SECRET_KEY` y
    `TEAPP_COOKIE_SECURE`.
  - `tests/conftest.py`, `tests/test_accounts.py`, `tests/test_sessions.py`
    (nuevos) y `tests/test_api.py` ampliado: **192 tests pasando** con
    `python -m pytest` (corrido en esta sesión, y también por el usuario:
    192 passed in 5.56s).
  - Corrida real con uvicorn + `curl`, según el traspaso: practicar sin
    sesión → 401; tarjeta con una letra cambiada → 401; tarjeta fabricada a
    mano sin la llave → 401; registrar `JUAN` con `juan` ya existente → 409;
    entrado como `juan` mandando `{"user":"ana"}` en el cuerpo → el punto cae
    en `juan`; contraseña equivocada → 401; `/logout` → 204 y `/me` después →
    401. `main.sign_in` ejercitada sin teclado, seis casos correctos.
    Comprobado en disco que ningún marcador existe sin credencial.
  - Un fallo real encontrado corriendo el servidor de verdad (no lo veía la
    suite): `/logout` devolvía el `Response` inyectado con
    `status_code = None`, y uvicorn reventaba con `KeyError: None`. Arreglado
    y cubierto con `test_logout_answers_the_status_code_it_declares` — ver
    `L-010`.
  - `_persistence/decisions.md`: `D-020` (los cuatro marcadores huérfanos de
    `data/users/` se borran) y `D-021` (contraseña propia y cookie firmada;
    OAuth descartado). `_persistence/assumptions.md`: `A-008` (la llave de
    firma no cambia entre arranques) y `A-009` (la rama `secure=True` nunca se
    ha ejecutado). `_persistence/lessons.md`: `L-010`.
- **Siguiente acción:** Empezar el paso 6 del roadmap — frenos de producción:
  tope de peticiones por persona y por día, timeouts (`T-038`).

### [S-009] 2026-08-04 — T-049 resuelta: el desfase del protocolo de cierre, en dos mitades

- **Paso:** 5 (deuda de protocolo, no de la app) — no mueve el paso general, que
  sigue en 4 completo.
- **Quedó funcionando:**
  - `.claude/skills/protocol-close/SKILL.md`: el control del `.js` se renombró
    de "Paso 5b" a **Paso 2b**, y se movió de después del Paso 4 (`tasks.md`) a
    justo después del Paso 2 (el traspaso). Motivo: el control produce tareas
    —marca una hecha o añade una nueva— y corriendo al final su resultado
    llegaba tarde para anotarse. Queda escrito que va **después** de la puerta
    del Paso 1 (si `git status` está limpio, no hay nada que compilar) y
    **antes** de escribir `tasks.md`.
  - El mismo archivo deja escrito, en el Paso 4, que el resultado del `push`
    **no puede** anotarse en `tasks.md`: para saberlo, el commit —que contiene a
    `tasks.md`— ya tiene que existir. Su sitio son el reporte de hoy y el
    arranque de mañana (`D-019`).
  - `.claude/skills/protocol-start/SKILL.md`: cambió `git status --short` por
    `git status -sb`. El primero no imprime la línea de la rama, así que un
    commit sin subir le resultaba invisible — comprobado en un repo de prueba:
    `--short` no imprimió nada, `-sb` imprimió
    `## main...origin/main [ahead 1]`. La tabla de desfases pasó de dos filas a
    tres.
  - `.claude/agents/session-closer.md`: la referencia al control pasa de "Paso
    5b" a "Paso 2b", con el porqué del movimiento resumido.
  - `tests/test_api.py`: el comentario de `test_the_script_is_served` apunta
    ahora al Paso 2b.
  - `_persistence/decisions.md`: `[D-019]`. `_persistence/lessons.md`: `[L-009]`
    — una regla que vive en dos archivos se corrige en los dos, o no se
    corrigió. `_persistence/assumptions.md`: `[A-007]` — entre el Paso 2b y el
    `git add` no se toca ningún `.ts`.
  - Primera corrida real del Paso 2b en su posición nueva, en este mismo
    cierre: `compilar: 0`, `comparar: 0` — el `.js` sigue al día.
  - 121 tests pasando con `python -m pytest` (según el traspaso; no se
    re-corrieron en este cierre).
- **Siguiente acción:** Empezar el paso 5 del roadmap — identidad de verdad,
  quitando la casilla "Your name" (`D-013`).

### [S-008] 2026-08-03 — T-037 resuelta: el `.js` compilado se vigila en el cierre, no en `pytest`

- **Paso:** 3 de 9 — cierra deuda que venía del paso 3. No mueve el paso general,
  que sigue en 4 completo.
- **Quedó funcionando:**
  - `.claude/skills/protocol-close/SKILL.md`: nuevo **Paso 5b**, antes del
    `git add`. Compila `frontend/*.ts` con el `tsc` local (nunca `npx`, ver
    `C-001`) y compara cada archivo que produjo contra `app/static/`. Dos
    verdades con su propio código de salida — `COMPILAR` y `COMPARAR` — para
    que "no se pudo comprobar" nunca se confunda con "está bien" (`D-017`,
    `D-018`, `L-007`, `L-008`).
  - `.claude/agents/session-closer.md`: nuevo punto en `## Límites` que obliga
    a correr el Paso 5b antes de `git add`, y deja explícito que si falla, el
    cierre **commitea y sube igual**, y la tarea va a "Sin resolver".
  - `tests/test_api.py`: `test_the_compiled_script_is_served` se renombró a
    `test_the_script_is_served`; el comentario ahora dice qué **no** cubre
    (que el `.js` esté al día) y por qué eso no se puede ver desde un test.
  - `_persistence/decisions.md`: `D-017` (el control vive en el cierre, no en
    `pytest`) y `D-018` (un control no puede causar un daño mayor que el que
    previene: el `.js` viejo no cancela el cierre).
  - `_persistence/lessons.md`: `L-007` (la primera versión del control con
    `diff -r` gritaba "viejo" con el repo correcto) y `L-008` (se comparó la
    opción rival en su versión floja, no en la real).
  - `_persistence/constraints.md`: primera entrada del archivo, `C-001` — la
    suite y el cierre no tocan la red.
  - `_persistence/assumptions.md`: `A-006` — que la ruta de `mktemp -d` de Git
    Bash le sirva a `node` sigue sin comprobarse en otra máquina.
  - **Primera corrida real del Paso 5b**, en este mismo cierre: `compilar: 0`,
    `comparar: 0` — el `.js` está al día. Cierra T-048.
  - 121 tests siguen pasando con `python -m pytest`.
- **Siguiente acción:** Empezar el paso 5 del roadmap — identidad de verdad,
  quitando la casilla "Your name" (`D-013`).

### [S-007] 2026-08-03 — Paso 4 completo: marcador por persona en `data/users/<nombre>.json`, `normalize_user` con cuatro frenos, `data/score.json` global borrado, 121 tests pasando

- **Paso:** 4 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/tools.py`: `SCORE_FILE` desaparece, entra `USERS_DIR` (`data/users/`).
    Nueva `normalize_user` — minúsculas + `strip`, y cuatro frenos: vacío, largo
    máximo 32, lista blanca `^[a-z0-9_-]+$`, y nombres reservados de Windows
    (`con`, `prn`, `com1`…). Nueva excepción `InvalidUserError`. Nueva
    `score_file(name, users_dir)`. `read_score` y `add_point` reciben ahora el
    nombre de la persona (`D-014`).
  - `app/english_tutor.py`: `respond(sentence, user)`, sin valor por defecto a
    propósito — un `user="anonimo"` de repuesto taparía el olvido de pasarlo.
  - `app/api.py`: `PracticeRequest` gana el campo `user`; se valida lo primero,
    antes de mirar la frase, y `InvalidUserError` se traduce a 422.
  - `frontend/app.ts` + `app/static/index.html`: casilla "Your name", recordada
    en `localStorage` bajo `teapp.user` (`D-013` — identidad declarada, no
    verificada). Recompilado a `app/static/app.js`.
  - `main.py`: pide el nombre una vez al arrancar, con `input()`.
  - `data/score.json` (el marcador global de 19 puntos del paso 3) se borró, no
    se adoptó (`D-015`).
  - Tests: de 57 a **121**, todos en verde con `python -m pytest` (verificado
    en esta sesión de cierre). Nuevos: recorrido de ruta (`../../CLAUDE.md`,
    etc.), nombres reservados de Windows, normalización, memoria separada por
    persona, y concurrencia entre dos personas a la vez.
  - `README.md` al día con el paso 4.
  - Verificado corriendo de verdad, según el traspaso de la sesión: uvicorn con
    curl (juan/ana separados, `  JUAN  ` cayendo en el mismo archivo, ataques
    de ruta rechazados con 422), terminal con `main.py`, y el usuario lo probó
    en el navegador. `data/users/` en disco confirma `ana.json`, `juan.json`,
    `maria.json` y `pedro.json` — consistente con esa prueba manual.
  - Costo de la sesión: $0,00 — no hay ninguna llamada a la API en el repo.
- **Siguiente acción:** Empezar el paso 5 del roadmap — identidad de verdad.
  Tiene que **quitar** la casilla "Your name", no añadirle nada al lado
  (`D-013`).

### [S-006] 2026-08-03 — Paso 3 completo: `index.html` + `app.ts` compilado, FastAPI sirve la pantalla en el mismo origen, CORS descartado (T-029), 57 tests pasando

- **Paso:** 3 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/api.py`: monta `/static` con `StaticFiles` y sirve `index.html` en
    `GET /` con `FileResponse`. El mismo servidor atiende `/practice`, así que
    hay un solo origen (`D-011`).
  - `frontend/app.ts` (nuevo, fuente que se edita) se compila con `tsc` a
    `app/static/app.js` (generado, versionado en Git porque en la nube no hay
    Node — `D-012`). `package.json` y `tsconfig.json` nuevos en la raíz;
    `typescript` fijado en 7.0.2, `module: "es2020"` tras comprobar que
    `"none"` ya no lo acepta el compilador.
  - `app/static/index.html` (nuevo): la pantalla con el formulario de práctica.
  - Tests: de 53 a **57**, todos en verde con `python -m pytest`. Nuevos en
    `tests/test_api.py`: la pantalla se sirve (200, `text/html`), trae el
    formulario correcto, el `.js` compilado se sirve, y la llamada a
    `/practice` usa ruta relativa (sin `localhost`).
  - Servidor levantado de verdad y comprobado a mano: `GET /` → 200
    `text/html`, `GET /static/app.js` → 200, `POST /practice` → 200 con las
    tres piezas. El usuario confirmó que la pantalla funciona en un navegador
    real.
  - `README.md`: comandos de arranque reales (`npm install`, `npm run build` +
    `uvicorn`) y tabla de qué recompilar según lo que se toque.
  - `T-029` (CORS) se descarta, no queda pendiente: mismo origen, no aplica
    (`D-011`). `T-030` (pantalla) queda hecha.
  - Costo de la sesión: $0,00 — no hay ninguna llamada a la API en el repo.
- **Siguiente acción:** Empezar el paso 4 del roadmap — memoria por persona.

### [S-005] 2026-08-02 — Paso 2 completo: `app/api.py` con FastAPI, `respond` devuelve `TutorReply`, dos fallos de concurrencia arreglados, 53 tests pasando

- **Paso:** 2 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/api.py` (nuevo): ruta `POST /practice` con FastAPI. `PracticeRequest`
    valida el cuerpo (rechaza lo que no sea una frase con texto, 422).
    `ScoreFileError` responde 500 con un mensaje corto y sin ruta, y el
    detalle completo se manda al log (`D-010`); cualquier otra excepción
    también se atrapa, se registra con traceback y responde 500 sin quedar
    muda.
  - `app/english_tutor.py`: `respond` ya no devuelve un texto cocinado, sino
    `TutorReply` — un `dataclass(frozen=True)` con `verdict`, `words` y
    `score` (`D-008`). `main.py` arma el texto de la terminal a partir de esas
    tres piezas.
  - `app/tools.py`: `add_point` escribe ahora de forma atómica (temporal con
    `tempfile.mkstemp` en la misma carpeta + `os.replace`) y protegida por un
    `threading.Lock` que cubre lectura y escritura juntas (`D-007`, `D-009`).
    Resuelve dos fallos de concurrencia que una revisión externa encontró con
    50 peticiones a la vez: `PermissionError` al pelearse por un temporal de
    nombre fijo, y pérdida de puntos por el hueco entre leer y escribir.
  - `requirements.txt`: se añaden `fastapi==0.141.1`, `uvicorn==0.52.1` y
    `httpx2==2.9.1`.
  - `README.md`: documenta las dos puertas (terminal y servidor) y advierte
    que no deben correr a la vez — comparten el mismo candado, que solo vale
    dentro de un proceso (`A-002`).
  - Tests: de 30 a **53**, todos en verde con `python -m pytest`. Nuevos en
    `tests/test_api.py` (la ruta, la validación, los dos tipos de 500),
    `tests/test_tools.py` (concurrencia con hilos de verdad) y
    `tests/test_english_tutor.py` (`TutorReply`, `FrozenInstanceError`).
  - Costo de la sesión: $0,00 — no hay ninguna llamada a la API en el repo.
  - Queda pendiente: `T-029` (CORS) y `T-030` (pantalla) para el paso 3;
    `T-033` (configurar el log) para el paso 7; `T-019` (frases practicadas
    vs. correctas) para el paso 8.
- **Siguiente acción:** Empezar el paso 3 del roadmap — configurar CORS y
  crear `index.html` + `app.ts` contra `/practice` local.

### [S-004] 2026-08-02 — Dos arreglos de robustez sobre el paso 1: marcador roto y `count_words` con no-texto, 30 tests pasando

- **Paso:** 1 de 9 — sigue completo; esta sesión no avanza de paso, refuerza el
  código que ya existía.
- **Quedó funcionando:**
  - `app/tools.py`: excepción propia `ScoreFileError`. `read_score` distingue
    **ausente** (no hay archivo → 0, sigue igual) de **roto** (existe pero no
    se entiende: JSON inválido, sin clave `score`, valor no entero o booleano,
    o el JSON no es un objeto → `ScoreFileError` con mensaje en español que
    nombra el archivo). `add_point` deja subir el error sin atraparlo, y como
    lee antes de escribir, el archivo roto **no se sobrescribe**.
  - `main.py`: atrapa `ScoreFileError` y muestra el mensaje en español antes de
    salir, en vez de un traceback.
  - `app/tools.py`: `count_words` ahora comprueba que reciba un `str`; si no,
    lanza `TypeError` nombrando el tipo que llegó (antes reventaba con
    `AttributeError` ante `None`, un número o una lista).
  - `tests/test_tools.py`: 16 tests nuevos que cubren ambos arreglos. La
    corrida completa pasa de 14 a **30 tests**, todos en verde con
    `python -m pytest`.
  - Se probó a mano contra el marcador real: se corrompió `data/score.json`,
    se corrió `main.py`, salió el mensaje entendible y el archivo quedó byte a
    byte idéntico; después se restauró y la app siguió funcionando normal.
  - Costo de la sesión: $0,00 — no hay ninguna llamada a la API en el repo.
  - Queda pendiente y sin resolver (anotado en `decisions.md` D-006):
    `add_point` sigue escribiendo con `write_text`, que no es atómico. Este
    arreglo cura la lectura del archivo roto, no impide crearlo.
  - Queda sin decidir (anotado en `assumptions.md` A-001): si el marcador
    cuenta frases **practicadas** o **correctas**. Se resuelve en el paso 8,
    cuando el juez deje de ser falso.
- **Siguiente acción:** Empezar el paso 2 del roadmap — sacar `respond` de
  `main.py` y ponerla detrás de FastAPI, sin tocar `app/`.

### [S-003] 2026-08-02 — Paso 1 completo: agente FALSO con 3 herramientas, 14 tests pasando

- **Paso:** 1 de 9 — completo con esta sesión.
- **Quedó funcionando:**
  - `app/tools.py`: las tres herramientas — `count_words` (cuenta palabras en
    Python puro), `judge_grammar` (FALSA: devuelve siempre el mismo veredicto,
    sin llamar al modelo) y `read_score` / `add_point` (marcador persistido en
    `data/score.json`).
  - `app/english_tutor.py`: `respond(sentence) -> str`, el enchufe del
    proyecto — llama a las tres herramientas siempre en el mismo orden.
  - `main.py`: la terminal. Único archivo con `input()`; lee frases hasta una
    línea vacía y llama a `respond`.
  - `tests/test_tools.py` y `tests/test_english_tutor.py` + `conftest.py`: 14
    tests, todos en verde con `python -m pytest`.
  - Se corrió en terminal de verdad: el marcador persistió entre ejecuciones
    distintas (`data/score.json`), y el usuario también la corrió a mano y
    confirmó que funciona.
  - Se cerraron tres huecos que venían del paso 0: entorno virtual `.venv/`,
    `requirements.txt` con `pytest==9.1.1` fijado, y las secciones del
    `README.md` que quedaban en deuda ("Cómo se corre", estado, estructura).
  - Costo del paso: $0,00 — no hay ninguna llamada a la API en el repo.
- **Siguiente acción:** Empezar el paso 2 del roadmap — sacar `respond` de
  `main.py` y ponerla detrás de FastAPI, sin tocar `app/`.

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
