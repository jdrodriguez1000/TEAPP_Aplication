# Decisiones — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [D-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

| id | fecha | qué se decidió | toca |
|---|---|---|---|
| D-033 | 2026-08-06 | **Todo TEAPP vive en `us-east-1` (Norte de Virginia).** La consola traía `us-east-2` (Ohio) por defecto — nadie la eligió. Se cambia **antes** de reservar la Elastic IP, cuando aún no existe nada: la región no es un ajuste, es un sitio, y las cosas de una región no se ven desde otra. Se elige `us-east-1` porque es la que `[A-015]` ya asume en su tabla de precios; quedarse en Ohio obligaba a comprobar precios y corregir esa tabla sin ganar nada | `T-059`, `[A-015]`, `[L-018]` |
| D-032 | 2026-08-05 | **TEAPP corre en la nube como el usuario `ubuntu`, el mismo que administra — y no como un usuario propio sin permisos.** Se elige contra la práctica estándar, a sabiendas: `create_account.py` lo ejecuta quien administra y escribe el MISMO `data/` que el servidor. Dos dueños distintos sobre esa carpeta es un problema de permisos que no enseña nada de lo que se está aprendiendo | `deploy/teapp.service`, `deploy/install.sh`, `T-064`, `[A-002]` |
| D-031 | 2026-08-05 | **La cuenta se abre con un alias `+aws` del correo personal, y con MFA en el root en el mismo momento de crearla** — no "cuando haya tiempo". 🚨 **El valor literal del correo NO se escribe aquí: el repo es público**, y el correo del root es media llave de recuperación. ⚠️ **Al ejecutarlo el 2026-08-06 se usó el correo personal SIN el alias** — ver la nota al final de la entrada | `T-057`, `[C-005]`, `[C-006]` |
| D-030 | 2026-08-05 | **El paso 7 termina con un CIERRE PLANEADO, no con la cuenta muriéndose sola.** Y la prueba de que `[C-004]` se cumplió es **levantar TEAPP desde cero solo con `deploy/`** — que se ENSAYA PRONTO, no al final: un paracaídas se prueba antes de saltar. 📌 La cuenta es desechable; `deploy/` no | paso 7, `T-069`, `T-070`, `[C-004]`, `[C-006]` |
| D-029 | 2026-08-05 | **La plataforma del paso 7: AWS + EC2 pequeña + Caddy + un nombre gratuito de DuckDNS + IP fija.** No lo decide la nube: lo decide **el disco**. `data/` son archivos, y un disco efímero evaporaría la cuota del paso 6 sin tocarle una línea. Con la plataforma cerrada, las cinco deudas del despliegue por fin tienen dueño | paso 7, `T-050`, `T-051`, `T-054`, `T-055`, `T-056`, `[A-005]`, `[A-014]`, `[C-002]`, `[C-003]`, `[C-004]` |
| D-028 | 2026-08-04 | **El log se configura (`T-033`): hora, nivel, origen, y `INFO` por defecto.** Lo que arregla no es la forma, es que `info` vuelva a significar algo. Dos renglones bajan de `warning` a `info`; el de los intentos fallidos **se queda** en `warning` | `app/config.py`, `app/api.py`, `tests/test_log_config.py`, `[L-012]` |
| D-027 | 2026-08-04 | **El registro de la v1 es CERRADO**, detrás de `TEAPP_REGISTRATION_OPEN` (por defecto `false`). Las invitaciones son v2 por la regla de `scope.md`. Las cuentas se crean con `create_account.py`, sin teclado — `main.py` no sirve en un servidor | `app/config.py`, `app/api.py`, `create_account.py`, paso 7 |
| D-026 | 2026-08-04 | **El contador de intentos fallidos vive en MEMORIA, y la cuota sigue en disco.** No es incoherencia: en disco, quien ataca decide cuántas veces escribe el servidor — la palanca de `[C-002]`. A cambio, el `dict` necesita barrido propio | `app/login_guard.py`, `app/api.py`, `[A-002]`, paso 7 |
| D-025 | 2026-08-04 | **`/login` se queda sin freno de intentos en el paso 6**, y se anota como deuda con dueño: es el paso 7. El freno de la cuota protege la factura; este protegería las contraseñas, y son cosas distintas | `app/api.py`, paso 7, `[D-026]` · ⏹️ **saldada** el 2026-08-04 |
| D-024 | 2026-08-04 | El "día" de la cuota se mide en **offset fijo −05:00**, escrito en el código, no en UTC ni con `ZoneInfo`. Comprobado: `ZoneInfo('America/Bogota')` **revienta en Windows** | `app/quota.py`, paso 7, `requirements.txt` |
| D-023 | 2026-08-04 | El paso 6 lleva **cuatro** frenos: cuota por persona y día, timeout, tope al tamaño del texto y motivo del frenazo. Los permisos de antemano **no entran**: ya están hechos en los pasos 4 y 5 | paso 6, `app/api.py`, `app/tools.py`, paso 8 |
| D-022 | 2026-08-04 | El portero de red entra al repo, y **con sus controles**: un vigía sin quien lo vigile no demuestra nada. Y `C-001` pasa a medirse en dos mitades, porque el portero no ve subprocesos | `tests/no_network.py`, `tests/check_no_network.py`, `tests/conftest.py`, `[C-001]` |
| D-021 | 2026-08-04 | Contraseña propia con cookie de sesión firmada; el proveedor externo se descarta por ser una pieza que no se controla | `app/api.py`, paso 5, paso 7 |
| D-020 | 2026-08-04 | Los cuatro marcadores de `data/users/` son huérfanos y se borran: sembrarlos obligaría a inventarles contraseña. El criterio no es "¿es de una prueba?" sino "¿tiene dueño?" | `data/users/`, paso 5, registro |
| D-019 | 2026-08-04 | El control del `.js` sube al Paso 2b; el resultado del push no se anota: es imposible, no un olvido | `protocol-close`, `protocol-start`, `session-closer` |
| D-018 | 2026-08-03 | Un control no puede causar un daño mayor que el que previene: el `.js` viejo no cancela el cierre | `protocol-close`, todo control futuro |
| D-017 | 2026-08-03 | Que el `.js` esté al día lo vigila el cierre, no `pytest`: es higiene del repo, no comportamiento | `protocol-close`, `session-closer`, `tests/test_api.py` |
| D-016 | 2026-08-03 | El `session-closer` hace `git push`; solo `--force` sigue prohibido | `protocol-close`, `session-closer`, todo cierre futuro |
| D-015 | 2026-08-03 | El `data/score.json` global se borra, no se adopta | `data/`, paso 4 |
| D-014 | 2026-08-03 | El nombre se normaliza y se valida con lista blanca, y se valida dos veces | `app/tools.py`, `app/api.py`, paso 5, paso 7 |
| D-013 | 2026-08-03 | En el paso 4 la identidad es **declarada, no verificada**: casilla + `localStorage` | `frontend/app.ts`, `app/api.py`, paso 5 |
| D-012 | 2026-08-03 | TypeScript con `tsc`: fuente en `frontend/`, el `.js` compilado sí va a Git | `tsconfig.json`, `package.json`, paso 3, paso 7 |
| D-011 | 2026-08-03 | FastAPI sirve la pantalla: mismo origen, y CORS se descarta (T-029) | `app/api.py`, paso 3, paso 7 |
| D-010 | 2026-08-02 | El detalle completo va al log; al navegador, un mensaje corto y sin rutas | `app/api.py`, todo error futuro |
| D-009 | 2026-08-02 | Candado en memoria + temporal con nombre propio para dos peticiones a la vez | `app/tools.py`, `[A-002]`, paso 4 |
| D-008 | 2026-08-02 | El tutor devuelve tres piezas separadas, no un texto cocinado | `app/english_tutor.py`, `app/api.py`, `main.py`, paso 3 |
| D-007 | 2026-08-02 | El marcador se escribe al lado y se renombra encima (escritura atómica) | `app/tools.py`, paso 4 |
| D-006 | 2026-08-02 | El marcador roto avisa con `ScoreFileError`; ausente sigue siendo 0 | `app/tools.py`, `main.py`, paso 2 |
| D-005 | 2026-08-02 | Nombres en inglés, contenido en español | todo el código del proyecto |
| D-004 | 2026-08-02 | El protocolo de inicio lee `_context/` siempre, no a demanda | `protocol-start`, `session-starter` |
| D-003 | 2026-08-02 | Recuperar 4 principios de ingeniería de un `CLAUDE.md` anterior | cómo se escribe el código |
| D-002 | 2026-08-02 | Los cuatro archivos del porqué los escribe la sesión principal, no el closer | `_persistence/` |
| D-001 | 2026-08-02 | La skill de inicio se llama `protocol-start`, no `protocol-close` | `.claude/skills/` |

---

## Entradas

### [D-033] 2026-08-06 — La región: todo TEAPP vive en `us-east-1`

- **Se eligió:** `us-east-1` (Norte de Virginia) como la región **única** de todo
  el paso 7 — Elastic IP, instancia EC2, y lo que venga después.
- **Contra qué:** `us-east-2` (Ohio), que era lo que la consola **traía puesto
  por defecto**. 📌 No se descartó por mala: se descartó porque **nadie la había
  elegido**, y esa es la diferencia entre una decisión y una herencia.
- **Por qué `us-east-1`:**
  - `[A-015]` ya calcula con esa región (`t3.micro`, Linux, `us-east-1`,
    $0.0104/hora). Elegir Ohio obligaba a comprobar precios y **corregir esa
    tabla en el mismo acto**, trabajo de papel a cambio de nada.
  - Virginia está geográficamente más cerca que Ohio de quien construye esto. Es
    un motivo menor y **no medido** — no se ha cronometrado nada.
- ⚠️ **Lo que NO se comparó, y se dice para que nadie lo lea como que sí:** los
  precios entre regiones. No se comprobaron. La regla 6 impide escribir un número
  sin corrida detrás, así que **el precio no fue el criterio** — lo fue la
  coherencia con `[A-015]`.
- 🚨 **Por qué se decidió AHORA y no cuando tocara lanzar la máquina:** una región
  no es una preferencia, **es un sitio**. Lo que vive en una no se ve desde otra.
  Una Elastic IP reservada en Ohio no sirve para una instancia en Virginia: hay
  que soltarla y pedir otra, **la nueva es una dirección distinta**, y
  `teapp.duckdns.org` habría que reapuntarlo dos veces.
  🔑 **Hoy el cambio es un clic porque no existe nada.** Cada cosa que se cree
  encarece ese clic.
- 🔑 **Y así es como se usa `[L-018]` en vez de solo sufrirlo.** La región estaba
  escrita en **un** sitio (la estimación de `[A-015]`) y a punto de decidirse en
  **otro** (un desplegable de la consola). **La segunda copia nace en el clic.**
  Hasta ahora las copias se cazaban *después* de divergir; esta se cazó antes de
  que la segunda existiera. Es la forma barata de usar un catálogo de fallos: no
  como anécdota, como detector.

### [D-032] 2026-08-05 — TEAPP corre como `ubuntu`, y no como un usuario propio

- **Se eligió:** que el servicio de la nube corra con el usuario `ubuntu` —el
  mismo con el que se administra la máquina— **contra** la práctica estándar de
  crear un usuario propio, sin contraseña y sin permisos, solo para la app.
- **Por qué, y es una razón concreta, no pereza:** `create_account.py` (`T-064`)
  lo ejecuta a mano quien administra, y escribe **el mismo `data/`** que el
  servidor. Con dos usuarios distintos, cada archivo que crea uno queda con
  permisos que el otro no puede tocar, y el fallo no aparece al instalar:
  aparece **días después**, la primera vez que se crea una cuenta nueva. Es
  además el terreno de `[A-002]`, donde el candado ya es delicado.
- ⚠️ **Lo que se está aceptando, dicho claro:** si alguien lograra ejecutar
  código dentro de TEAPP, lo haría con un usuario que **puede usar `sudo`**. Con
  un usuario propio, ese mismo fallo se quedaría encerrado en la carpeta de la
  app. **Es una decisión que en un producto de verdad no se tomaría así.**
- **Por qué aquí sí:** la máquina es desechable y vive 6 meses (`[C-003]`), no
  guarda nada irremplazable —`data/` son marcadores de práctica de inglés—, y el
  proyecto ya trae cinco cosas nuevas a la vez. Es PI-2: **¿hace falta para que
  esto funcione hoy?**
- 🔑 **Qué la revertiría, para que no se quede puesta por inercia:** el día que
  `data/` guarde algo que duela perder, o que el paso 8 meta la llave de Claude
  en esa máquina. Con dinero real dentro, el cálculo cambia de lado.

### [D-031] 2026-08-05 — Cómo se abre la cuenta: alias en el correo, y MFA desde el minuto uno

- **Se eligió:** registrar la cuenta con un **alias `+aws`** del correo personal
  (la forma `usuario+etiqueta@gmail.com`, que llega a la misma bandeja), y
  **activar MFA en el usuario root en el mismo acto de crear la cuenta**, no
  después.
- 🚨 **El valor literal del correo NO se escribe en este repo, y es deliberado.**
  `jdrodriguez1000/TEAPP_Aplication` es **público**, y hasta hoy el correo
  personal no aparecía en él: los commits van con la dirección `noreply` de
  GitHub. Escribirlo aquí sería meterlo en el historial de Git **para siempre**,
  porque borrarlo mañana no lo saca de los commits de ayer.
  - **Y no es solo privacidad.** El correo del root es **una de las dos mitades de
    la recuperación** de una cuenta de AWS. Publicar *"esta dirección exacta es
    el root de una cuenta de AWS"* regala media llave. El MFA cubre la otra
    mitad — razón de más para no entregar la primera.
  - 📌 **Lo que se escribe es el patrón, no el valor.** Quien lea el repo entiende
    la decisión; nadie se lleva la dirección.
- **Por qué el alias:** el correo entra igual en la bandeja de siempre, pero deja
  ver de un vistazo qué llega de AWS y permite filtrarlo. Cuesta cero.
- 🚨 **Y lo que el alias NO es, para que nadie lo lea mal dentro de tres meses:**
  no es una forma de sacar un segundo plan gratuito. `[C-006]` ata la
  elegibilidad a **la identidad y la tarjeta, no al correo**. Abrir una segunda
  cuenta con otro alias **no da más créditos: deja inelegible también la que ya
  se tenía**. El alias es organización, no un truco.
- **Por qué el MFA en el mismo momento y no "cuando haya tiempo":** el root es el
  usuario al que **no se le pueden poner límites** — es el dueño de todo, y de él
  cuelga la capacidad de cruzar al plan de pago de `[C-005]`, que no tiene vuelta
  atrás. 🔑 **Un MFA aplazado se aplaza para siempre**, porque nunca hay un día
  en que apetezca.
- ⚠️ **La trampa del MFA, que hay que resolver el mismo día:** si el segundo
  factor vive solo en el móvil y el móvil se pierde o se restablece, **el root
  queda inaccesible** — y recuperarlo con AWS es lento. Al montarlo hay que dejar
  resuelto un camino de vuelta: un segundo dispositivo de MFA, o los códigos de
  recuperación guardados fuera del móvil. **Comprobar en la documentación cuántos
  dispositivos admite el root** el día que se haga; no se escribe de memoria.

#### ⚠️ Cómo se ejecutó de verdad — 2026-08-06 (`T-057`)

- **El alias `+aws` NO se usó.** La cuenta se abrió con el correo personal tal
  cual. **El MFA en root sí se activó en el mismo acto**, como decía la decisión.
- **Impacto: ninguno donde importa.** El alias era **organización, no seguridad
  ni elegibilidad** — está dicho tres puntos más arriba. `[C-006]` ata el plan
  gratuito a la identidad y la tarjeta, así que el correo no cambia nada del
  reloj ni de los créditos.
- **Lo único que se pierde** es filtrar el correo de AWS por la dirección de
  destino. Se sustituye con un filtro por remitente, que hace lo mismo.
- 🚨 **Lo que sigue vigente y NO se relaja:** el valor literal del correo **no se
  escribe en este repo**. Ahora incluso importa un poco más: sin alias, la
  dirección del root es la dirección personal de siempre.
#### ✅ El camino de vuelta del MFA — resuelto y probado el 2026-08-06

- **Cómo quedó:** el segundo factor no vive solo en el móvil. La **semilla** del
  código está en la app **Contraseñas de Apple**, que la sincroniza por el
  Llavero de iCloud. Si el móvil se pierde, los códigos se recuperan desde otro
  dispositivo de la misma cuenta de Apple.
- **Probado de verdad, no supuesto** (`PI-4`): se abrió la app Contraseñas en el
  **iPad** y el código de AWS aparece y rota. Eso demuestra la sincronización
  mejor que leer una casilla de ajustes.
- 🔑 **El riesgo no desapareció, se movió.** Antes el punto único de fallo era el
  móvil; ahora es la **cuenta de Apple**. Lo que lo hace aceptable es que hay un
  **segundo dispositivo de confianza** (el iPad), así que no existe la trampa
  circular de "para recuperar la cuenta de Apple necesito el móvil que perdí".
- ⚠️ **Lo que NO se pudo confirmar:** cuántos dispositivos MFA admite el root. No
  salió en la documentación consultada el 2026-08-06 y **no se escribe de
  memoria**. Si algún día hace falta una segunda llave independiente de Apple, se
  mira en la propia pantalla de credenciales de seguridad de la consola.

### [D-030] 2026-08-05 — El paso 7 termina con un cierre planeado, y el ensayo va pronto

- **Se eligió:** **bajar TEAPP nosotros, con fecha en el calendario**, antes de
  que AWS cierre la cuenta sola. Y **ensayar la reconstrucción pronto**, no al
  final.
- **Contra qué — los tres finales posibles, y solo uno cuesta dinero:**

  | | qué pasa | costo |
  |---|---|---|
  | **A.** no hacer nada | AWS cierra la cuenta sola: 90 días de gracia y borrado | $0 |
  | **B.** apagar antes ✅ | se baja TEAPP con fecha, y luego igual que A | $0 |
  | **C.** pasar a plan de pago | TEAPP sigue vivo y empieza a facturar | ~$11/mes (estimado) |

- 🔑 **La razón NO es el dinero: A y B cuestan lo mismo.** Es que **un cierre
  planeado se aprende y uno automático solo se sufre.** B tiene dentro una
  comprobación que A no tiene, y esa comprobación es todo el valor.
- **La comprobación:** al apagar, **verificar que `deploy/` puede volver a
  levantarlo**. Eso convierte el cierre en la última prueba del paso 7 — y en la
  **única** que demuestra de verdad que `[C-004]` se cumplió.
  - 🔑 Mientras la máquina siga encendida, *"está todo escrito en `deploy/`"* es
    **una afirmación sin corrida detrás**, que es exactamente lo que la regla 6
    prohíbe. **Levantarlo desde cero es la corrida.**
- 🚨 **La corrección de calendario, que es la parte que faltaba.** Si esa prueba
  vive solo al final, **te enteras de que `deploy/` no funciona el día que ya no
  hay margen para arreglarlo**: cuenta muriéndose, créditos gastados y el guion
  que no levanta. Es descubrir que el paracaídas no abre mientras caes.
  - **Por eso el ensayo se hace pronto** (`T-069`): con TEAPP arriba y
    funcionando, se **borra la máquina y se reconstruye solo desde `deploy/`**.
    Una instancia pequeña cuesta céntimos por un día.
  - Así `[C-004]` deja de ser una intención y **queda medida**, con cinco meses
    por delante para arreglar lo que falte. El cierre del final (`T-070`) pasa a
    ser la **segunda** corrida, no la primera.
- 📌 **Y con esto el cierre de la cuenta deja de destruir nada: destruye una
  copia.** 🔑 **La cuenta es desechable; `deploy/` no.** Que es justo lo que
  `[C-006]` obliga a asumir, porque esa ventana de 6 meses no vuelve.

### [D-029] 2026-08-05 — La plataforma del paso 7 la decide el disco, no la nube

- **Se eligió:** **AWS + EC2** (instancia pequeña, tipo `t3.micro`) + **Caddy** de
  servidor de delante + un **nombre gratuito de DuckDNS** + una **IP fija**
  (Elastic IP).
- **Contra qué:** Lambda + API Gateway, y App Runner / Fargate.
- **Que AWS sea la nube no se comparó**, y conviene decir por qué para que nadie
  lo reabra creyendo que se olvidó: es una elección **del curso, no del
  proyecto**. Las metas de quien construye esto —agentes, un SaaS, entender la
  ingeniería por debajo— piden la plataforma donde nada está escondido. Y encaja
  con el método: aquí se escribe `pedir_json` a mano en vez de importar una
  librería. Una plataforma que esconda el proxy contradice el método entero.

#### 🔑 Lo que de verdad decide: `data/` son archivos

TEAPP guarda su estado en el disco — `data/accounts.json`, `data/quota/*.json`,
`data/users/*.json`. **En una máquina local eso no significa nada. En la nube es
el nudo entero del paso 7**, porque casi todas las plataformas modernas dan un
disco **efímero**: existe mientras el programa corre y desaparece al reiniciar.

| lo que pasaría con disco efímero | cómo se vería |
|---|---|
| reinicia el servidor → `accounts.json` desaparece | **se nota en cinco minutos**: nadie puede entrar |
| arrancan dos copias → dos `accounts.json` distintos | me registro en una y entro por la otra: no existo |
| 🚨 reinicio → **cuota nueva** | **no se nota nunca**: el sistema responde contento y habla la factura del paso 8 |

- 🚨 **La tercera es la grave, y por ser la muda.** El freno del paso 6 se
  rompería **sin que nadie le tocara una línea**, solo cambiando lo que hay a su
  alrededor. Es exactamente la forma de `[D-027]`: allí fue el registro abierto,
  aquí sería el disco.
- Por eso la comparación se hizo por una sola columna:

  | camino | disco | veredicto |
  |---|---|---|
  | Lambda + API Gateway | **no hay** | y además necesita un adaptador para FastAPI |
  | App Runner / Fargate | **efímero** | cómodo, y borra las cuentas al reiniciar |
  | **EC2** ✅ | **persiste** | TEAPP sube **sin cambiar una línea de código** |

#### El premio: las dos deudas fantasma se vuelven trabajo concreto

`[C-002]` decía que escribir hoy un tope de tamaño de cuerpo sería *"inventarse
una pieza que la plataforma del paso 7 trae hecha"*. Con el proxy en nuestra
máquina, deja de ser fantasma: `T-054` es una línea de configuración de Caddy.

Y `T-055` es el caso bonito. 🔑 **La garantía de `X-Forwarded-For` NO viene de
que el proxy sea nuestro — viene de que nadie más pueda hablar con FastAPI.** Son
dos cosas juntas, y sin las dos no hay certeza, hay costumbre:

1. uvicorn atado a `127.0.0.1`, no a todas las direcciones.
2. el cortafuegos abierto **solo** en 80 y 443.

#### HTTPS sin dominio: el agujero que casi mata el despliegue

- **Verificado, no supuesto:** Let's Encrypt **se niega por política** a emitir
  certificados para `compute.amazonaws.com`. Devuelve literalmente *"The ACME
  server refuses to issue a certificate for this domain name, because it is
  forbidden by policy"*. Hay hilos en su foro desde 2016. No es configuración: no
  hay forma de convencerlo.
- 🚨 **Sin certificado, `T-051` no se puede cumplir y NADIE ENTRA A TEAPP.**
  `TEAPP_COOKIE_SECURE=true` le dice al navegador *"no mandes esta cookie salvo
  por HTTPS"*. Sin HTTPS válido la cookie de sesión no viaja, y el fallo es mudo.
  **Un despliegue entero muerto por la política de una autoridad certificadora.**
- **Se resuelve con un nombre gratuito de DuckDNS** (`teapp.duckdns.org`): es un
  nombre público de verdad, Let's Encrypt emite sin problema y Caddy hace el
  trámite solo. 📌 **El límite de quien construye esto es el dinero, no el
  nombre**: un nombre regalado y sin tarjeta sí entra.
- **Por eso Caddy y no nginx:** saca y renueva el certificado solo. Con nginx ese
  trámite es una pieza más que montar y mantener, y `T-051` la necesita sí o sí.

#### Por qué IP fija, y no un guion que avise a DuckDNS

La IP pública de una EC2 **cambia al apagar y encender**. Si DuckDNS apunta a la
vieja, el nombre deja de resolver → se cae el HTTPS → se cae la cookie → no entra
nadie.

- 🔑 **El argumento bueno no es "es una pieza menos": es que cuesta lo mismo.**
  AWS cobra por *tener una IPv4 pública*, no por el tipo. La que asigna sola al
  arrancar y la fija se facturan igual. Entonces no se paga un extra por
  comodidad — **se elige cuál de las dos direcciones se tiene, al mismo precio**.
  Cobrando lo mismo, quedarse con la que cambia no tiene defensa.
- El guion que avisa a DuckDNS existe para el caso contrario: alguien en su casa,
  con una IP que le cambia el proveedor y sin forma de fijarla. No es este caso.
- ⚠️ **La trampa clásica:** una IP fija **sin máquina asociada también cobra**.
  Es como AWS evita que se acaparen direcciones. Aquí no aplica —la máquina no se
  va a borrar— pero queda escrito.

#### Lo que se descartó por medición, no por pereza

EC2 **consume créditos**: para cuentas nuevas ya **no existe** la franja de 750
horas. La sospecha era que entonces *"el reloj lo marca la resta, no el
calendario"*, y que habría que escribir una pieza que apagara la máquina sola.

**Al ponerle números, no aguanta:** el gasto estimado del paso 7 es del orden de
$50 de $200 (ver `[A-015]` — es estimación de lista de precios, no corrida).
🔑 **Gana el calendario, y sobra un factor de cuatro.** La pieza que apaga la
máquina queda descartada. Y apagarla por las noches "para ahorrar" ahorra las
horas de la instancia **pero la IP sigue cobrando**: complica más de lo que
rinde. **Encendida y quieta.**

#### Lo que NO arregla, y hay que llevar en la lista

- **"Sube sin cambiar una línea" vale para el código, no para el arranque.**
  Faltan: dirección de escucha, variables de entorno, arranque automático, el
  `.js` compilado, y **correr `create_account.py` allá arriba** — `data/` no va a
  Git, así que la máquina arranca **sin ninguna cuenta** (`[D-027]`).
- **El disco persiste al reiniciar, no si se borra la máquina.** ⚠️ **No hay
  copia de seguridad de nada.** El día que se cierre la cuenta, las cuentas de
  prueba se van con ella. Aceptado: es un ejercicio con fecha de caducidad.
- **`[D-024]` paga por otro lado.** El offset fijo `−05:00` de la cuota se
  escribió a mano por un problema de Windows. Resulta que también salva aquí: la
  máquina de EC2 estará en UTC y a `quota.py` le va a dar igual.

### [D-028] 2026-08-04 — El log se configura, y con él `info` vuelve a significar algo

- **Se eligió:** `configure_logging()` en `app/config.py`, llamada **lo primero**
  al importar `app/api.py`. Formato `hora nivel origen | mensaje`, nivel `INFO`
  por defecto y ajustable con `TEAPP_LOG_LEVEL`.
- 🔑 **Lo que esto arregla no es la forma, aunque sea lo que se ve.** Hasta hoy
  actuaba el handler de último recurso de Python, **que empieza en `WARNING`**:
  cualquier `logger.info(...)` no se perdía por poco, **no existía**. La única
  forma de que un renglón saliera era subirlo de nivel — y eso obliga a mentir
  sobre su importancia. 🚨 **Un log donde todo es aviso no tiene avisos.**
- **Qué renglón queda en qué nivel, y por qué:**

  | renglón | antes | ahora | por qué |
  |---|---|---|---|
  | cuota agotada (`app.api`) | `warning` | **`info`** | es el freno funcionando, no una avería |
  | registro cerrado (`app.config`) | `warning` | **`info`** | es el estado normal de la v1 |
  | **demasiados intentos** (`app.api`) | `warning` | **`warning`** | 🚨 no describe el sistema funcionando: describe a **alguien intentando entrar en una cuenta ajena**. Y el contador vive en memoria ([D-026]), así que este renglón es el único rastro que sobrevive a un reinicio |

  Los dos primeros llevaban escrito en el código *"cuando `T-033` configure el
  log, esto vuelve a `info`"*. Se cumplió: si no, quedaban dos comentarios
  mintiendo.
- **Por qué `basicConfig` y no `dictConfig`:** hace falta una línea, no un árbol
  de configuración. PI-2.
- 🚨 **Y por qué SIN `force=True`**, que era lo tentador: `basicConfig` no hace
  nada si el logger raíz ya tiene handlers, y eso aquí juega a favor.
  - **Con uvicorn** la raíz está limpia —uvicorn configura sus propios loggers,
    no el raíz—, así que la configuración sí aplica. Medido.
  - **Bajo pytest** la raíz está tomada por `caplog`, y que aquí no se pise nada
    es justo lo que se quiere. `force=True` le arrancaría a `caplog` su handler
    en mitad de la suite.
- **Medido, no supuesto** (2026-08-04, uvicorn real, puerto 8094):

  ```
  2026-08-04 19:52:14 INFO     app.config | Registro por red CERRADO (...)
  2026-08-04 19:52:18 INFO     app.api | Cuota agotada: probe-log lleva 20 de 20 el 2026-08-04
  ```

  🔑 **Ese segundo renglón es literalmente el de [L-012]**, el que se midió el
  mismo día como *"20 frenazos, cero líneas"*. Ahora sale.
- ⚠️ **En la misma corrida apareció ruido que no es nuestro:** un
  `ERROR asyncio | ConnectionResetError [WinError 10054]`, una vez. Es el cliente
  de la prueba cerrando la conexión de golpe, cosa de `asyncio` en Windows — las
  22 peticiones contestaron bien. No lo tapa nadie y no se persigue hoy; queda
  escrito para que no se investigue dos veces.
- **Lo que NO se decide aquí:** dónde se guarda el log en la nube ni cuánto se
  conserva. Eso es del paso 7, con la plataforma delante.

### [D-027] 2026-08-04 — El registro se cierra con un interruptor, y las cuentas se crean desde la terminal

- **Se eligió:** que `/register` esté **cerrado por defecto**, detrás de
  `TEAPP_REGISTRATION_OPEN`; que la ruta siga en el código porque la suite la
  usa; y que las cuentas se creen con `create_account.py`, que no espera a nadie.
- **Contra:** dejar `/register` abierto con un tope de registros por origen.
- **El problema, medido** (2026-08-04, `scrypt` con los parámetros de
  `app/accounts.py`):

  | lo que se hizo | resultado |
  |---|---|
  | 200 registros con nombres **nuevos** | 25,6 s — **128 ms cada uno** |
  | el registro nº 201, con 200 cuentas dentro | 121 ms |
  | 200 registros con un nombre **repetido** | 0,12 s — 0,6 ms cada uno |
  | `accounts.json` con 200 cuentas | 30.293 bytes, **reescrito entero cada vez** |

  🔑 **La comparación entre la primera fila y la tercera es toda la historia.**
  Un nombre repetido se rechaza *antes* de `scrypt` y sale 200 veces más barato.
  O sea: lo caro es exactamente lo que quien ataca puede pedir sin límite — un
  nombre nuevo cada vez. Sin sesión, sin cuenta y sin tope. Era una palanca peor
  que la de `/login`, porque allí al menos había un freno.
- **Por qué cerrado y no un tope por origen:**
  - `_context/scope.md` decide los casos dudosos con *"¿hace falta para que la
    tubería funcione en producción?"*. Un sistema de invitaciones no hace falta:
    es **v2**.
  - 🔑 **Cerrar hace desaparecer la palanca; un tope solo la estrecha.** Sin
    invitación no se llega a `scrypt`, y el rechazo cuesta lo que un `if`.
  - Y un tope por origen tenía un daño colateral serio: si quien usa esto es un
    salón de clase, salen todos por la misma dirección, y el tope que frena a
    quien ataca frena también a quien registra a veinte estudiantes seguidos.
- **Lo que la decisión OBLIGA a añadir:**
  - **`create_account.py`**, o el interruptor deja fuera a quien administra. ⚠️ Y
    **`main.py` no bastaba**, aunque también crea cuentas: se comprobó el
    2026-08-04 y usa `getpass`, que en Windows lee **de la consola** y no de la
    entrada estándar. Con la entrada por tubería se queda colgado esperando un
    teclado. Sirve a quien está sentado delante; **en un servidor no sirve**, y en
    el paso 7 no hay nadie sentado delante.
  - **Las dos ramas con test.** `conftest.py` abre el registro con `autouse`
    porque casi toda la suite empieza creando una cuenta, y eso deja el camino
    por defecto sin correr — la trampa de `[A-009]` y la lección de `T-052`. Los
    tests que anulan ese `setenv` están en `test_api.py`.
  - **Que abrir exija la palabra exacta `true`**, al revés que `cookie_secure`,
    que acepta cualquier cosa que no sea `false`. Allí equivocarse deja la puerta
    cerrada; aquí la abriría.
- **Comprobado de punta a punta** (2026-08-04, uvicorn real, puerto 8095): cuenta
  creada desde la terminal **sin teclado** → `POST /register` por la red contesta
  `403` → `POST /login` con esa cuenta contesta `200`. El interruptor cierra la
  puerta de la calle sin cerrar la de servicio.
- ⏳ **Caducidad:** el día que haya que registrar a **gente desconocida** — gente
  a la que no se le puede crear la cuenta a mano. Ese día esta decisión deja de
  valer y toca el sistema de invitaciones que aquí se aplazó a v2. Hasta entonces
  no hay nada que revisar.
- **Lo que NO se decide aquí:** cómo se registra esa gente desconocida. Cerrar
  hoy no elige la puerta de mañana.

### [D-026] 2026-08-04 — El tope de intentos cuenta en memoria; la cuota sigue contando en disco

- **Se eligió:** guardar los intentos fallidos de `/login` en un `dict` en
  memoria (`app/login_guard.py`), con candado y con barrido de lo vencido.
- **Contra:** guardarlos en disco, por coherencia con `quota.py`, que avisa en su
  propia cabecera de que un contador en memoria se borra en cada arranque.
- **Por qué:**
  - 🔑 **Lo que se cuenta dura cosas distintas.** La cuota dura **un día**: un
    reinicio a media tarde regala medio día de gasto real, y en la nube el
    servidor se reinicia solo. El tope de intentos dura **quince minutos**: un
    reinicio le devuelve los intentos a quien esté probando contraseñas, pero él
    no puede provocar el reinicio — le tocaría de casualidad.
  - 🚨 **Y en disco habría una palanca.** Escribir un archivo en cada intento
    fallido pone en manos de quien ataca **cuántas veces escribe el servidor**.
    Es exactamente el problema de `[C-002]`: quien manda decide lo que cuesta
    atenderle. En memoria, fallar no cuesta un archivo.
- **Lo que la decisión OBLIGA a añadir**, y sin lo cual sería mala:
  - **Barrido de lo vencido**, dentro de `record_failure` — el único sitio donde
    el `dict` crece. Sin él, la palanca del disco reaparece como memoria: mil
    direcciones distintas dejan mil entradas que no se irían nunca. Con testigo:
    `test_the_sweep_runs_by_itself_when_new_failures_arrive`.
  - **Cada frenazo al log con `warning`.** El contador se borra entero en cada
    reinicio, así que ese renglón es **el único rastro que sobrevive** de que
    alguien estuvo probando contraseñas. Con `info` no aparecería mientras
    `[T-033]` no configure el log (`[L-012]`).
  - **Un reinicio del `dict` entre tests**, en `conftest.py`. Vive en memoria: no
    ensucia datos de verdad, pero sobrevive de un test al siguiente y haría que
    los tests de login dependieran del orden en que corren.
- **Hereda `[A-002]`, y de la forma más incómoda:** un `dict` solo lo ve su
  propio proceso. Dos procesos de uvicorn son dos contadores que no se enteran el
  uno del otro, y entonces el tope real es el doble del escrito. Hoy se arranca
  un proceso; el día que se arranquen dos, este freno se afloja **en silencio**.
- **Medido, no supuesto** (2026-08-04, uvicorn de verdad, puerto 8099):

  | intento | respuesta | log |
  |---|---|---|
  | 1 a 5, contraseña mala | `401` | — |
  | 6, contraseña mala | `429`, `retry-after: 900` | `origen 127.0.0.1 lleva 5 de 5` |
  | 7, contraseña **buena** | `429` | mismo renglón |

  🔑 La tercera fila es la que dice que el freno es un freno: **la contraseña
  correcta tampoco abre** mientras el origen esté cerrado. Si abriera, quien
  prueba a la fuerza no estaría frenado — solo tendría que seguir probando.
- **Lo que NO se decide aquí:** de dónde sale el origen en la nube. Hoy es
  `request.client.host`; detrás de un proxy será la dirección del proxy y todo el
  mundo caería en el mismo cubo. Queda con dueño en `T-055`.

### [D-025] 2026-08-04 — `/login` se queda sin freno de intentos, y se anota como deuda

- **Se eligió:** **no** poner tope de intentos fallidos en `/login` dentro del
  paso 6, y dejarlo escrito como deuda del paso 7.
- **Contra:** meterlo ahora, aprovechando que `quota.py` ya sabe contar por
  persona y por día.
- **Por qué:**
  - 🔑 **Parecen el mismo freno y no lo son.** La cuota protege **la factura** y
    cuenta a quien ya demostró quién es. Un tope de intentos protege **las
    contraseñas** y tiene que contar a quien **todavía no** ha demostrado nada —
    o sea, no por persona, porque la persona es justo lo que está en duda. Se
    cuenta por origen de la petición, que es otro dato y otra estructura.
  - Reutilizar `quota.py` para esto sería doblarlo para un trabajo que no es el
    suyo, y acabaría estorbando a los dos.
  - `_context/roadmap.md` pone el paso 6 en *"tope por persona y por día,
    timeouts"*. Esto no es eso.
  - ⚠️ **Y hoy muerde menos de lo que parece:** en local el único que puede
    probar contraseñas es quien ya tiene la máquina. El riesgo nace el día que
    la app esté en internet, que es el paso 7.
- **Lo que NO se decide aquí:** que no haga falta. Hace falta. Se decide
  **cuándo**, y que quede con dueño en vez de olvidado — el mismo trato que
  [A-009] le dio al hueco de la cookie `Secure`.
- **Toca:** `app/api.py` (`/login`), el paso 7, y la suposición [A-012].
- ⏹️ **Saldada el 2026-08-04** por [D-026] (`T-053`). La deuda se pagó **antes**
  del despliegue, que era la fecha que esta entrada se puso a sí misma.
  ⚠️ [A-012] ya **no existe**: se retiró al saldarla y se partió en [A-013] y
  [A-014]. Si has llegado aquí buscándola, está contada en [L-014].

### [D-024] 2026-08-04 — El "día" de la cuota se mide en offset fijo −05:00

- **Se eligió:** una constante en el código, `timezone(timedelta(hours=-5))`, y
  el día se obtiene con `moment.astimezone(...).date()`. El `now` que se inyecta
  es un `datetime` **con zona**, no un número suelto.
- **Contra:** (a) medir el día en **UTC**, que es lo que haría el servidor del
  paso 7 por su cuenta; (b) `ZoneInfo("America/Bogota")`, que es la forma
  "correcta de libro".
- **Por qué:**
  - 🔑 **`sessions.py` mide una duración; la cuota mide un día del calendario.**
    A una duración le da igual dónde estés: siete días son siete días. Un día del
    calendario **no existe sin zona horaria**. Por eso `sessions.py:71` puede
    usar un `float` de `time.time()` y aquí no vale.
  - **UTC se descarta con una corrida, no con una opinión.** El mismo instante
    —`2026-08-05 02:30 UTC`— es día **5** en UTC y día **4** en −05:00. Esa
    ventana de 5 horas es la cuota reiniciándose a las **7pm**. Y el fallo no
    aparecería en local (donde la máquina va en −05:00): **aparecería solo en la
    nube**, que es el peor sitio para descubrirlo.
  - 🚨 **`ZoneInfo` se descarta porque se probó y falló.** En esta máquina,
    `ZoneInfo('America/Bogota')` lanza `ZoneInfoNotFoundError`: Windows no trae
    la base de datos de zonas horarias que Linux sí tiene. Funcionaría en la nube
    y no en casa — el fallo al revés, igual de malo. Arreglarlo pide añadir y
    fijar el paquete `tzdata` ([L-002]), o sea una dependencia más para algo que
    una constante resuelve.
  - **El offset fijo es correcto aquí porque Colombia no cambia la hora en
    verano.** Es lo único que un offset fijo no sabría manejar, y no aplica.
    ⚠️ Si algún día la app sirve a alguien en una zona con horario de verano,
    esta decisión se rompe y hay que volver a `ZoneInfo` **con `tzdata`**.
- **Toca:** `app/quota.py`, el paso 7 (el servidor corre en UTC y esta constante
  es lo que lo hace irrelevante) y `requirements.txt` (la dependencia que **no**
  se añade).

### [D-023] 2026-08-04 — Los cuatro frenos del paso 6, y el que se queda fuera

- **Se eligió:** cerrar el paso 6 con **cuatro** frenos:
  1. **Cuota por persona y por día.** Un contador con clave *(persona, día)*.
  2. **Timeout de la petición.** La que no contesta se corta sola.
  3. **Tope al tamaño del texto de práctica.** Hoy `PracticeRequest.sentence` es
     un `str` sin techo (`app/api.py:105`).
  4. **Motivo del frenazo.** Un 429 sin motivo es un misterio.
- **Contra:** una lista de cinco que incluía *"permisos de antemano"*, y la
  lectura de que *"tope por persona y por día"* del roadmap eran **dos** frenos
  (uno por persona, otro global de la casa).
- **Por qué:**
  - **Los permisos de antemano se quedan fuera porque ya están hechos.** Son la
    regla 3 de `CLAUDE.md`, e implementados: `normalize_user` impide que un
    nombre construya una ruta fuera de sitio ([D-014]), y desde el paso 5 la
    identidad sale de la cookie firmada, así que nadie toca el marcador de otro
    ([D-021]). 🔑 El motivo de fondo: **no tiene terminado**. Los otros cuatro
    tienen un número o una respuesta que mirar; este no, y una tarea sin
    terminado no se cierra nunca.
  - **El freno 3 (tamaño del texto) no está en el roadmap y entra igual.** El
    patrón ya vive en casa dos veces —`MAX_USER_LENGTH` (`app/tools.py:62`) y
    `MAX_PASSWORD_LENGTH` (`app/accounts.py:63`)—. No es una idea nueva: es la
    misma, olvidada justo en el sitio que más va a costar en el paso 8.
  - **Un solo contador, no dos.** *"Por persona y por día"* es una cuota que se
    reinicia cada día, no un tope por persona más un tope global. El tope global
    es el freno de la cartera y pertenece al paso 8, donde hay dólares que
    contar.
- **Cómo se construye, decidido ahora porque después cuesta:**
  - 🚨 **El reloj se inyecta.** `now` como parámetro, igual que
    `sessions.py:71` y `:89`. Un tope por día no se puede ver funcionar en una
    corrida —nadie espera a mañana—, así que si el código llama a `time.time()`
    por dentro, el freno se queda sin testigo.
    ⚠️ Con una diferencia que costó una comprobación: **el `now` de la cuota
    lleva zona horaria** y el de `sessions.py` no. Ver [D-024].
  - 🚨 **El contador sube ANTES de llamar al tutor, no después.** Hoy da igual
    —el tutor falso no falla nunca—, pero en el paso 8 una llamada que **gasta
    tokens y luego revienta** se colaría gratis: el dinero salió y el contador no
    se enteró. 🔑 Lo que se cobra es **haber intentado**, porque eso es lo que
    cuesta.
  - **El tope se inyecta igual que el reloj.** Un `20` incrustado obliga a
    mandar 21 peticiones —a mano y en cada test— para ver el freno morder. Con el
    tope inyectado, un test pone 1 y lo ve morder a la segunda. Y el número es
    una predicción sin medir ([A-010]): cambiarlo no puede costar una reescritura.
  - **El contador cuenta peticiones, pero se diseña para que en el paso 8 se le
    cambie la unidad a dólares sin rediseñarlo.** Hoy es gratis; descubrirlo en
    el 8 no.
  - 🚨 **El contador escribe en disco, y ese terreno ya costó sangre.** Es el
    mismo problema de [T-020], [T-021] y [T-022]: candado, más escribir al lado
    y renombrar encima ([D-007], [D-009]). Hereda [A-002]: solo vale con un
    proceso de uvicorn. Un freno que pierde cuentas con dos peticiones a la vez
    no frena.
  - **El motivo del frenazo viaja en la respuesta, no en el log** — o hay que
    subir [T-033] al paso 6. Escribirlo en el log antes de configurarlo lo manda
    al handler de último recurso de Python ([A-003]): sale por pantalla porque
    Python no sabe qué otra cosa hacer, no porque nadie lo decidiera.
- **Toca:** el paso 6 entero, `app/api.py`, `app/tools.py`, y el paso 8 (la
  unidad del contador y el tope global de la casa).

### [D-022] 2026-08-04 — El portero de red entra al repo, y con sus controles

- **Qué se decidió:** meter el portero de red (`tests/no_network.py`) al repo,
  activo en **todos** los tests vía `conftest.py`, y meter con él sus cinco
  controles (`tests/check_no_network.py`), fuera de la corrida normal.
- **Contra qué:** dejarlo como medición de una sola vez — comprobar hoy que
  `C-001` se cumple, anotarlo, y repetir a mano cuando alguien se acuerde.
- **Por qué:**
  - Medir una vez dice *"el 4 de agosto se cumplía"*. El portero dice *"se
    cumple hoy"*, en cada corrida. El día que alguien meta una llamada de verdad
    a la API, la suite se pone roja **en ese momento**, no meses después.
  - 🔑 **Los controles van o no va nada.** El verde de la suite no demuestra que
    el portero funcione: si el portero se rompe en silencio, los 192 tests pasan
    exactamente igual, porque ninguno intenta salir. Solo los controles — que
    salen a internet a propósito — distinguen *"nadie salió"* de *"y si alguien
    lo intentara, se le vería"*. Un portero en el repo sin sus controles es la
    misma trampa que venía a evitar, un piso más abajo.
  - Los controles **no** se llaman `test_*.py` a propósito: salen a internet de
    verdad si el portero falla, y eso es justo lo que `C-001` prohíbe. Se piden
    por su nombre para reverificar.
- **Lo que esta decisión NO puede dar:** el portero solo parchea el `socket` de
  su propio proceso. `node`, `git` y `npx` son otro proceso: **nunca** los verá.
  Por eso `C-001` queda partida en dos mitades, una automática y otra a mano.
- **Toca:** `tests/no_network.py`, `tests/check_no_network.py`,
  `tests/conftest.py`, `[C-001]`, todo test futuro.

### [D-021] 2026-08-04 — Contraseña propia y cookie de sesión firmada; el proveedor externo se descarta

- **Se eligió:** que el paso 5 pruebe la identidad con **usuario y contraseña
  propios**, guardada como *hash* (cifrado de ida: se comprueba, no se desanda),
  y que la sesión se recuerde con una **cookie firmada por el servidor**,
  `HttpOnly` y `Secure`. Todo con librería estándar: `hashlib.scrypt` para la
  contraseña, `hmac` para la firma, `secrets` para generar. **Cero paquetes
  nuevos**, así que la suite sigue sin tocar la red ([C-001]) sin nada que pensar.
  - **`scrypt`, no `sha256`.** Un hash de contraseña es **lento a propósito**:
    lo que protege es que probar millones de contraseñas cueste caro. `sha256`
    es rápido, que aquí es exactamente el defecto.
  - **`hmac.compare_digest`, no `==`.** Comparar con `==` corta en cuanto
    encuentra la primera diferencia, y ese tiempo se puede medir desde fuera
    para adivinar la firma letra a letra.
- **Contra:** "entrar con Google" (OAuth) y el enlace por correo.
- **Por qué:** el argumento bueno es del propio roadmap — *"el paso 8 cae casi
  al final... el sospechoso queda solo"*. 🔑 **Un proveedor de identidad externo
  es una pieza que no controlo y que no responde igual dos veces: la misma clase
  de ruido que el modelo.** Meterla en el paso 5 es meter en la tubería justo lo
  que el roadmap saca de ella hasta el paso 8. No se descarta por ser "más
  difícil" ni la contraseña se elige por ser "lo básico".
  El enlace por correo, además, necesita un servicio que mande correos: red,
  cuenta y probablemente factura. Choca con la regla 5 y con [C-001].
- ⚠️ **Un argumento que se usó y era falso, anotado para que no vuelva:** se dijo
  que OAuth exige una dirección pública de vuelta que no existe hasta desplegar,
  y por tanto ataba el paso 5 al 7. **No es cierto: Google admite
  `http://localhost` para desarrollo.** El costo real de OAuth es otro —cuenta de
  Google Cloud, pantalla de consentimiento y un secreto de cliente—. La
  conclusión no cambia; el argumento sí. Queda escrito porque una decisión
  correcta sostenida por un motivo falso se cae en cuanto alguien comprueba el
  motivo.
- **Toca:** `app/api.py`, `frontend/app.ts`, `.env.example` (una línea nueva para
  la llave de firma), el paso 5 entero, y el paso 7, que tiene que llevar esa
  llave a la nube.

### [D-020] 2026-08-04 — Los cuatro marcadores de `data/users/` son huérfanos: se borran, no se siembran

- **El problema:** `data/users/` tiene cuatro marcadores sin contraseña —`ana`
  (2), `juan` (4), `maria` (1), `pedro` (3)—. Con un registro abierto, cualquiera
  se registra como `juan` y hereda su marcador. 🔑 **Verificar la identidad no
  sirve de nada si cualquiera puede reclamar una identidad que ya existía:** es
  el agujero de [D-013] con un formulario delante.
- **Se eligió:** declararlos **huérfanos y borrarlos**, dejando `data/users/`
  vacío antes de que exista el registro.
- **Contra:** sembrar las cuatro cuentas a mano con una contraseña cada una.
- **Por qué:** esos cuatro nombres salieron de probar el paso 4, no de cuatro
  personas. Lo dice [S-007] —*"uvicorn con curl (juan/ana separados)"*— y lo
  confirma el disco: los cuatro archivos pesan 12 bytes y están escritos **el
  mismo minuto**, el 2026-08-03 a las 10:44.
  Es el mismo criterio de [D-015] con el `score.json` global, y aquí pesa más:
  🔑 **sembrarlos no obligaría a inventarles un dueño, sino una contraseña.** Una
  contraseña es la prueba de que alguien es quien dice; fabricar cuatro es crear
  cuatro credenciales válidas sin nadie detrás, lo contrario de lo que este paso
  viene a construir.
- **Lo que el vaciado gana, y es la razón de fondo:** restablece una regla que
  hoy está rota — **todo marcador nace junto a su credencial; no existe marcador
  sin dueño**. Con esa regla en pie el agujero se cierra por estructura: el
  registro rechaza un nombre que ya existe, y como ya no queda ningún nombre sin
  credencial, no hay nada que reclamar. Sembrarlos, en cambio, obligaría a una
  regla especial para esas cuatro cuentas, y las reglas especiales son donde se
  cuelan los errores.
- **No se pierde historial:** `data/` está en `.gitignore` y nunca fue a Git, así
  que ahí no había nada que conservar. Y no se hace copia de seguridad: los
  cuatro nombres, los cuatro números y la hora quedan escritos aquí arriba. Se
  pierden 48 bytes; lo que significaban ya está en prosa.

**Dos consecuencias que costó ver, y sin las cuales el borrado no sirve:**

1. 🔑 **Vaciar `data/users/` no es una tarea que se complete hoy: es una
   condición que solo se vuelve estable el día que el registro existe.**
   `add_point` crea el archivo —y la carpeta— la primera vez que alguien
   practica. Hoy cualquier petición a `/practice` fabrica un marcador sin
   credencial: es el agujero de [D-013] visto desde el disco. Así que se borra,
   y el primer `curl` de prueba del paso 5 con `{"user": "juan"}` lo resucita.
   ⚠️ **Por eso no se anota como hecho consumado, sino como condición con punto
   de verificación:** la carpeta se comprueba vacía **después** de que la
   credencial funcione, no ahora. Darlo por hecho hoy significa que esta noche el
   cierre encuentre un `juan.json` y nadie pueda distinguir si es el viejo o uno
   de prueba — y la evidencia del 10:44 ya no estará para desempatar.

2. 🔑 **La lista de quién existe y la lista de quién tiene puntos no son la
   misma lista, aunque hoy se parezcan.** La regla "el registro rechaza un
   nombre que ya existe" está incompleta si no dice **según qué archivo**. Si el
   registro mirara `data/users/`, le estaría preguntando *"¿quién existe?"* a una
   carpeta que cualquiera puede llenar practicando. **La autoridad sobre quién
   existe es el almacén de credenciales, y solo ese.** `data/users/` pasa a ser
   un **derivado**: un marcador solo nace cuando la credencial ya existía.

**El residuo del 2026-08-04 NO es este caso, y la distinción vale más que los
archivos.**

Al terminar el paso 5 quedaron en disco un `juan` (1 punto) y una `ana` (sin
marcador), de las pruebas de esa tarde. Se **conservan**, y eso no contradice
nada de lo de arriba:

| | los cuatro del 2026-08-03 | `juan` y `ana` del 2026-08-04 |
|---|---|---|
| ¿tienen credencial? | **no** | **sí**, nacieron con ella |
| ¿cumplen la regla? | la rompían | la cumplen |
| borrarlos es… | **integridad** | **higiene** |

> 🔑 **Aquellos había que borrarlos; estos se pueden borrar.** No es la misma
> frase. Un marcador sin dueño es una identidad reclamable y hay que quitarla de
> en medio. Un marcador con su credencial detrás es solo desorden, y el desorden
> se limpia cuando apetece.

⚠️ Esto es lo que hay que mirar antes de aplicar `[D-020]` otra vez: **la
pregunta no es "¿esto es de una prueba?", es "¿tiene dueño?".** Confundirlas
llevaría a borrar cuentas reales por parecer de prueba, o a conservar marcadores
huérfanos por parecer datos.

- **Toca:** `data/users/`, el registro del paso 5, `app/accounts.py`, y el
  criterio de cualquier migración futura de datos de personas.

### [D-019] 2026-08-04 — El control del `.js` sube al Paso 2b; el resultado del push no se anota porque no se puede

**El problema (T-049):** `protocol-close` escribía `tasks.md` en el Paso 4, y
**después** corría el control del `.js` (Paso 5b) y el push (Paso 6b). Lo que esas
dos corridas demostraban llegaba tarde: no había dónde anotarlo. Pasó de verdad
con T-048 el 2026-08-03 — la tarea pedía ver el control funcionando en un cierre
real, el control funcionó, y nadie pudo marcarla.

🔑 **Al mirarlo de cerca eran dos problemas distintos con la misma cara.** Uno se
arregla moviendo un paso; el otro no se arregla nunca.

**Mitad 1 — el control del `.js`: se eligió MOVERLO al Paso 2b.**

- **Contra:** dejarlo donde estaba y añadir un repaso de `tasks.md` después del
  push.
- **Por qué:** el control no necesitaba estar abajo. Su única exigencia real es
  ser **antes del `git add`**, y entre "después del traspaso" y "antes del `git
  add`" hay sitio de sobra. Movido arriba, su resultado llega antes de escribir
  `tasks.md` y se anota como cualquier otra evidencia.
- **Por qué se descartó el repaso posterior:** obligaría a un segundo commit cada
  noche, y ese segundo commit tendría el mismo problema con su propio push. Se
  cambiaba un hueco por un bucle.
- **Va después del Paso 2, no dentro del Paso 1:** el Paso 1 tiene una puerta
  —*"si `git status` sale limpio, detente"*— y compilar antes de esa puerta gasta
  trabajo las noches en que no hay nada que cerrar.
- ⚠️ **El movimiento crea una suposición nueva**, anotada como `[A-007]`: entre el
  control y el `git add` no se toca ningún `.ts`.

**Mitad 2 — el push: se eligió TRATARLO COMO IMPOSIBILIDAD, no como pendiente.**

- **Se decidió:** dejar escrito en el protocolo que el resultado del push **no
  puede** vivir en `tasks.md`, con el porqué, y que su sitio son el reporte de hoy
  y el arranque de mañana.
- **Contra:** seguir intentando encajarlo en el commit con más pasos.
- **Por qué:** es una pescadilla que se muerde la cola. Para saber si el push
  funcionó, el commit tiene que existir ya — y `tasks.md` va dentro de ese commit.
  Ninguna reordenación lo resuelve. 🔑 **Un límite lógico escrito como límite
  deja de parecer un olvido**, y nadie vuelve a intentar arreglarlo.

**Lo que casi se queda a medias, y es la parte que más enseña:** la mitad 2 se
apoyaba en que el arranque de mañana lee `git status -sb` y ve la línea `ahead`.
Al comprobarlo, `protocol-start` leía **`git status --short`**, que no imprime la
línea de la rama: un commit sin subir le resultaba **invisible**. La promesa
existía y nadie la cumplía. Por eso la mitad 2 son **dos escrituras**, en dos
archivos, y sin la segunda la primera es papel. Ver `[L-009]`.

- **Toca:** `.claude/skills/protocol-close/SKILL.md` (Pasos 2b, 4 y 6b),
  `.claude/skills/protocol-start/SKILL.md` (Paso 1 y la tabla de desfases, ahora
  de tres filas), `.claude/agents/session-closer.md`, `tests/test_api.py`
  (comentario), `[A-007]`, `[L-009]`.
- ⚠️ **El control se llamaba "Paso 5b" hasta hoy.** Las anotaciones anteriores al
  2026-08-04 —`[D-017]`, `[D-018]`, `[S-008]`, T-037, T-046, T-048— lo nombran
  así. Es el mismo control; no se reescribieron por ser historia.

### [D-018] 2026-08-03 — Un control no puede causar un daño mayor que el que previene: el `.js` viejo no cancela el cierre

- **Se eligió:** que el control del Paso 5b **reporte y siga**. Si el `.js` está
  viejo, o si no se pudo comprobar, el cierre commitea y sube igual, y el aviso
  va a "Sin resolver" con su tarea.
- **Contra:** que el cierre se plante y no commitee hasta que se recompile a mano.
- **Por qué:** un `.js` desactualizado y **señalado** es una molestia: el
  despliegue no es hoy, es el paso 7. Un cierre que se niega a guardar deja el
  día entero solo en este disco, que es exactamente la catástrofe de [L-006] —
  la que el protocolo existe para evitar. 🔑 **Un control no debe poder causar un
  daño mayor que el que previene.** Cambiar una molestia por la pérdida del día
  es un mal negocio aunque el control tenga razón.
- **También se decidió que el closer NO recompile.** Podría dejar el repo
  correcto en el acto, pero borraría la señal de que se olvidó, y mañana se
  olvidaría igual. **El olvido es la información.** Además el `.ts` podría estar
  a medias: recompilar sería commitear código sin terminar.
- **Toca:** `protocol-close` Paso 5b, y cualquier control que se escriba después.

### [D-017] 2026-08-03 — Que el `.js` esté al día lo vigila el cierre, no `pytest`

- **Se eligió:** poner la comprobación en `protocol-close` (Paso 5b), disparada
  por el `session-closer` antes del `git add`.
- **Contra:** un test más en `pytest`, que se dispararía con los otros 121.
- **Por qué:** los 121 tests preguntan *¿el código se porta bien?*. Este pregunta
  *¿lo que commiteaste es lo que hiciste?*. Son cosas distintas, y hay dos
  señales que lo demuestran:
  - 🔑 **Si el arreglo no toca el código, la comprobación no estaba mirando el
    código.** Cuando este control se pone rojo, los dos archivos son correctos
    por separado; lo que falta es correr `npm run build` y commitear. Es una
    acción sobre el repositorio.
  - **En producción no se puede ni formular.** En el servidor solo está el `.js`;
    el `.ts` no viajó. Una comprobación que se evapora al desplegar no hablaba
    del producto, hablaba de la mesa de trabajo.
  - Es la **misma familia** que [L-006]: "¿el commit llegó a `origin`?" y "¿el
    `.js` es el de su `.ts`?" preguntan lo mismo. Esa pregunta ya tenía dueño.
  - **Y mantiene la suite sin red** ([C-001]): meter `tsc` en `pytest` ataría los
    tests de Python a Node, y con `npx` de por medio, a internet.
- **El argumento que se descartó, y por qué era malo:** se recomendó `pytest`
  diciendo "un freno que depende de tu memoria no es un freno". El principio es
  correcto; la aplicación estaba mal. El closer se dispara solo, igual que el
  push — no depende de la memoria de nadie. Ver [L-008].
- **Toca:** `protocol-close`, `session-closer`, `tests/test_api.py` (el test se
  renombró a `test_the_script_is_served` y su comentario dice qué **no** mide).

### [D-016] 2026-08-03 — El `session-closer` hace `git push`; solo `--force` sigue prohibido

- **Se eligió:** darle el `git push` al closer, como Paso 6b del protocolo, y
  obligarlo a comprobar después con `git status -sb` que ya no dice `ahead`.
- **Contra:** dejar la prohibición como estaba y que el closer solo **detectara**
  el `ahead` y lo reportara en "Sin resolver", para que el push lo hiciera una
  persona. Fue lo que se implementó primero, y el usuario decidió lo otro.
- **Por qué:** la prohibición original decía *"tu trabajo es añadir historia,
  nunca reescribir ni borrar la que hay"*, y metía `git push` en la misma lista
  que `--amend`, `reset` y `--force`. Pero 🔑 **un `git push` a secas solo añade:
  encajaba con la razón de la regla y estaba prohibido por su letra.** Lo que
  reescribe historia es `--force`, y ese se queda fuera junto a los demás.
  La alternativa —detectar y avisar— dejaba el cierre dependiendo de que alguien
  leyera el aviso, que es justo el eslabón que fallo en [L-006].
- **Toca:** `.claude/skills/protocol-close/SKILL.md` (Paso 6b nuevo y lista de
  prohibidos), `.claude/agents/session-closer.md` (sus límites, que repetían la
  lista por su cuenta y se habrían contradicho) y todo cierre de sesión futuro.

### [D-015] 2026-08-03 — El `data/score.json` global se borra, no se adopta

- **Se eligió:** borrar el marcador global de 19 puntos que dejó el paso 3.
- **Contra:** adoptarlo como marcador de la primera persona que se registrara, o
  dejarlo huérfano en `data/` junto a la carpeta nueva `data/users/`.
- **Por qué:** esos 19 puntos salieron de probar los pasos 1, 2 y 3, y no son de
  nadie que estuviera practicando inglés. **Adoptarlo obligaría a inventarle un
  dueño**, y eso es escribir una mentira dentro de los datos: mañana ese "juan"
  con 19 puntos parecería historia real. Dejarlo huérfano es peor todavía — un
  archivo con pinta de significar algo que ya no significa nada. Y como `data/`
  no va a Git, no se pierde ningún historial al borrarlo.
- **Toca:** `data/`, y el criterio para cualquier migración futura de datos.

### [D-014] 2026-08-03 — El nombre se normaliza y se valida con lista blanca, y se valida dos veces

- **Se eligió:** `normalize_user` en `app/tools.py` hace las dos cosas —bajar a
  minúsculas y quitar espacios, luego rechazar lo que no sirva— con **cuatro
  frenos**: vacío, largo máximo (32), lista blanca `^[a-z0-9_-]+$` y nombres que
  Windows reserva (`con`, `prn`, `aux`, `nul`, `com1`–`com9`, `lpt1`–`lpt9`).
  Y se llama en **dos sitios**: en `app/api.py` para rechazar pronto con un 422
  explicado, y dentro de `score_file` porque es quien toca el disco.
- **Contra:** una lista negra de caracteres peligrosos; validar solo en la puerta
  de red; validar solo en `tools.py`; y dejar que el navegador validara.
- **Por qué:** con este nombre se construye una **ruta de archivo**, y el nombre
  lo escribe cualquiera desde el navegador. Una lista negra siempre deja algo
  fuera; la lista blanca hace que el olvido falle hacia el lado seguro, que es lo
  que pide `_context/architecture.md`. Tres matices que costaron entenderse:
  - **Normalizar no es validar.** Windows no distingue mayúsculas y Linux sí:
    sin normalizar, `Juan` y `juan` serían **una** persona en local y **dos** en
    la nube del paso 7, sin ningún error y con todos los tests en verde.
  - **Validar los caracteres no es validar el nombre.** `con` es solo letras,
    pasa la lista blanca entera, y Windows lo reserva incluso con extensión.
    El vacío y los nombres larguísimos también se cuelan por ahí.
  - **Validar dos veces no es duplicar.** La puerta rechaza *pronto y con
    explicación*; `score_file` rechaza porque no puede fiarse de quien la llame.
- **Toca:** `app/tools.py`, `app/api.py`, `main.py`, y todo lo que en el paso 5
  y el paso 7 vuelva a convertir texto de fuera en una ruta.

### [D-013] 2026-08-03 — En el paso 4 la identidad es declarada, no verificada

- **Se eligió:** una casilla "Your name" en la pantalla, que el navegador
  recuerda en `localStorage` bajo la clave `teapp.user`, y que el servidor se
  cree sin comprobar nada.
- **Contra:** adelantar el paso 5 y hacer la identidad de verdad antes que la
  memoria.
- **Por qué:** es el mismo truco que `judge_grammar`, y por la misma razón. Se
  construye la tubería con la pieza falsa y **luego se sustituye la pieza, no la
  tubería**: si algo falla en el paso 5, la memoria por persona ya funcionaba
  ayer y el sospechoso queda solo. El roadmap pone memoria en el 4 e identidad en
  el 5 a propósito.
- ⚠️ **Lo que esto significa hoy:** cualquiera puede escribir el nombre de otra
  persona y ver —y sumar a— su marcador. Es **conocido y aceptado hasta el paso
  5**, no un descuido. `localStorage` es una comodidad para no reescribir el
  nombre, nunca una prueba de identidad.
- **Toca:** `frontend/app.ts`, `app/static/index.html`, `app/api.py`, y el paso 5,
  que tiene que **quitar** la casilla, no añadirle nada al lado.

### [D-012] 2026-08-03 — TypeScript con `tsc`: fuente en `frontend/`, el `.js` compilado sí va a Git

- **Se eligió:** escribir la pantalla en TypeScript de verdad y compilarla con
  `tsc`, como dice `_context/architecture.md`. Tres detalles concretos:
  - **El fuente vive en `frontend/`, la salida en `app/static/`.** Se editan solo
    los `.ts` de `frontend/`; los `.js` de `app/static/` los escribe el
    compilador. Dos carpetas y no una para que sea imposible confundirse sobre
    cuál se edita.
  - **`strict: true`.** Todos los avisos encendidos. Apagarlos sería pagar el
    costo de TypeScript sin llevarse lo comprado.
  - **`module: "es2020"`.** Un archivo suelto, sin `import` ni `export`, que el
    HTML carga con un `<script>` normal. Los módulos son un tema entero y no
    hacen falta hoy (PI-2). Se escribió primero `"none"` y **el compilador lo
    rechazó**: TypeScript 7 ya no acepta ese valor. Vale la pena anotarlo porque
    la documentación consultada no lo decía — 🔑 **el compilador es la única
    fuente que no se queda desactualizada.**
  - **Versión fija: `typescript` 7.0.2**, sin `^`. Misma razón que [L-002]: sin
    fijar, dos máquinas instalan compiladores distintos. Se consultó la
    documentación actual antes de escribir el `tsconfig.json` en vez de sacarlo
    de memoria — 7.0.2 es el compilador nativo, muy posterior a lo que el modelo
    recordaba.
- **Contra:** dos alternativas reales, no de paja.
  - **Escribir `app.js` a mano** y saltarse TypeScript en el paso 3.
  - **`app.js` con `// @ts-check` y JSDoc**, que da buena parte de los avisos sin
    compilar ni instalar nada.
  Se descartaron porque la elección de TypeScript **ya estaba tomada** en
  `architecture.md`. Cambiarla aquí habría sido decidir arquitectura de refilón,
  en medio de otra tarea. El costo previsto —instalar Node— resultó ser cero:
  ya estaba instalado (v25.8.1, npm 11.11.0), comprobado antes de proponer nada.
  📌 `// @ts-check` queda anotado como la salida buena si `tsc` diera problemas.
- **Por qué:** el aviso que se compra es concreto. El contrato de [D-008] es
  `verdict`, `words`, `score`; escribir `reply.verdcit` en JavaScript no es un
  error, vale `undefined`, y la pantalla muestra "undefined" sin explotar. Ese
  fallo miente en silencio y se busca en el sitio equivocado. TypeScript lo
  subraya al escribirlo.
  🔑 **Lo que el navegador lee es el `.js`, siempre.** El `.ts` no es una
  alternativa al `.js`: es su original. ⚠️ De ahí el riesgo real y previsible de
  esta decisión: **editar el `.ts` y olvidar compilar** deja el navegador
  comportándose como antes, con el código correcto delante. Queda escrito aquí
  para que el día que pase se busque en el sitio correcto.
  Y el `.js` compilado **se versiona** —contra la costumbre de ignorar lo
  generado— porque en la nube corre **un solo servicio, en Python**: allí no hay
  Node que compile nada. Si el `.js` no está en Git, el paso 7 sube una pantalla
  que no existe. `dist/` sigue en `.gitignore` de cuando se pensó compilar
  aparte; ya no aplica, pero no estorba y no se toca (PI-3).
- **Toca:** `package.json` y `tsconfig.json` (nuevos), `frontend/app.ts`,
  `app/static/app.js` (generado, versionado), y el paso 7, que debe subir
  `app/static/` con el `.js` ya compilado. `node_modules/` ya estaba ignorado.

### [D-011] 2026-08-03 — FastAPI sirve la pantalla: mismo origen, y CORS se descarta (T-029)

- **Se eligió:** que el mismo FastAPI que atiende `/practice` sirva también el
  `index.html` y el `.js` de la pantalla. Un solo servidor, un solo origen, desde
  el primer día de desarrollo y no solo en el despliegue. En consecuencia
  **T-029 (configurar CORS) se descarta**: no se hará, ni ahora ni en el paso 7.
- **Contra:** servir la pantalla aparte —en otro puerto local, o abriendo el HTML
  con doble clic— y configurar CORS con una lista explícita de orígenes, que era
  el plan de T-029 y estuvo a punto de escribirse hoy.
- **Por qué:** CORS solo existe cuando hay **dos orígenes**. Con la pantalla
  servida por el mismo FastAPI, el navegador ve un único edificio y no tiene nada
  que bloquear. 🔑 **La mejor configuración de CORS es no necesitar CORS.**
  T-029 no salía de ningún archivo del proyecto: se revisó `_context/
  architecture.md` y `_context/roadmap.md` a propósito antes de descartarla, y
  ninguno la pide. Al contrario, los dos empujan a un solo origen —arquitectura
  dice que la pantalla son *"archivos quietos"* y que con Next.js serían **dos**
  servidores encendidos en la nube "en vez de uno"; el roadmap describe el paso 2
  como *"una ruta, local"* y el 7 como subir *"la tubería entera"*—. La tarea
  venía de una previsión razonable ("navegador y servidor, seguro hacen falta
  permisos de origen") que no aplica a esta forma de montarlo. Es PI-2 en su
  forma más literal: **la pieza que no se añade no puede fallar, ni hay que
  entenderla, ni mantenerla, ni rehacerla en el paso 5.**
  Y mismo origen en local que en la nube quita una diferencia entre desarrollo y
  producción — de esas que solo se descubren el día del despliegue.
  ⚠️ **Si algún día vuelve a hacer falta CORS** —una pantalla servida aparte, u
  otro cliente— la regla ya está pensada y no se rediscute: **lista de orígenes
  explícita, nunca `allow_origins=["*"]`**. Tres razones. La que no es opinable:
  🚨 con `*` el navegador **se niega a enviar credenciales**, así que la
  identidad del paso 5 no viajaría. Las otras dos: con `*` cualquier página del
  mundo puede montar su pantalla encima de `/practice` y gastar la llave (regla
  5, minimizar factura), y contradice la regla 3, denegar por defecto.
  ⚠️ Y un límite que no hay que confundir después: **CORS nunca protege el
  servidor.** `curl` o un script de Python entran igual, porque no hay navegador
  que obedezca la cabecera. Lo que protege el servidor es la autenticación del
  paso 5.
- **Toca:** `app/api.py` (servir los archivos de la pantalla), el paso 3 entero
  —`index.html` y `app.ts` llamarán a `/practice` con ruta relativa, sin nombrar
  host ni puerto— y el paso 7, que sube un solo servicio. Cierra T-029 como
  descartada, no como pendiente.

### [D-010] 2026-08-02 — El detalle completo va al log; al navegador, un mensaje corto y sin rutas

- **Se eligió:** una sola regla para los dos lados del mismo problema en
  `app/api.py`. El `ScoreFileError` se registra **entero** con `logger.error` y
  se contesta un texto fijo sin ruta. Cualquier otro fallo se atrapa también, se
  registra con `logger.exception` —que guarda el traceback— y se contesta otro
  texto fijo. `Exception` y no `BaseException`, para que un Ctrl-C siga apagando
  el servidor en vez de acabar convertido en una respuesta HTTP.
- **Contra:** lo que había, que fallaba por los dos extremos a la vez. `detail=
  str(error)` **contaba de más**: devolvía la ruta absoluta del servidor, medida
  de verdad en la respuesta. Y un `PermissionError` **contaba de menos**: subía
  sin atrapar y salía como un 500 mudo, sin quedar apuntado en ningún sitio.
- **Por qué:** son dos públicos distintos, igual que el idioma en [D-005]. El
  mensaje de `ScoreFileError` se escribió para la terminal, donde saber qué
  archivo abrir es **ayuda**. Fuera del servidor esa misma frase es información
  regalada sobre cómo está organizado por dentro, y quien pregunta no puede
  hacer nada con ella. 🔑 **Quitar el detalle de la respuesta solo vale si el
  detalle queda escrito en otro sitio**; si no, se cambia un problema por otro.
- **Toca:** `app/api.py` y todo error que se añada de aquí en adelante — la
  regla es del proyecto, no de esta ruta. Cuatro tests nuevos en
  `tests/test_api.py`: dos comprueban que la respuesta no lleva la ruta, y dos
  que el detalle sí llegó al log (con `caplog`).

### [D-009] 2026-08-02 — Candado en memoria + temporal con nombre propio para dos peticiones a la vez

- **Se eligió:** dos arreglos distintos en `add_point`, porque son dos fallos
  distintos que el servidor destapó juntos.
  - **Un temporal por escritura**, con `tempfile.mkstemp(dir=path.parent)`. El
    `dir=` es obligatorio: fuera de la carpeta del definitivo, renombrar deja de
    ser atómico. Si el renombrado falla, el temporal se borra antes de dejar
    subir el error.
  - **Un `threading.Lock` que abarca la lectura Y la escritura juntas.**
- **Contra:** el nombre fijo `score.json.tmp` que puso [D-007], y un candado que
  abarcara solo la escritura. Lo segundo parecía suficiente y no lo es.
- **Por qué:** se midió con el servidor levantado y 50 peticiones simultáneas.
  Con el nombre fijo, entre 31 y 39 de 50 devolvían 500: una petición renombraba
  el temporal mientras otra lo sobrescribía, y Windows lo cortaba con
  `PermissionError: Acceso denegado`. Y de 50 puntos esperados el marcador
  guardaba 8, 10 o 12, con hasta 7 personas recibiendo el mismo número — porque
  entre `read_score` y `os.replace` había un hueco donde otra petición leía el
  mismo total.
  🔑 **La escritura atómica y el candado resuelven cosas distintas.** La primera
  protege de UNA escritura cortada por la mitad; el segundo, de DOS escrituras
  pisándose. [D-007] resolvió la primera y no tocaba la segunda. Un candado que
  abarcara solo la escritura tampoco: el problema no está en escribir, está en
  el hueco entre leer y escribir.
  Nada de esto se veía en la terminal, donde escribía una persona sola, ni en
  los tests, porque `TestClient` manda las peticiones de una en una.
- **Toca:** `app/tools.py` (`_SCORE_LOCK`, `add_point`) y cuatro tests nuevos con
  hilos de verdad en `tests/test_tools.py`. Deja la suposición [A-002]: el
  candado vale dentro de **un solo proceso**. El mismo patrón vuelve en el paso
  4, cuando el marcador pase a ser uno por persona.

### [D-008] 2026-08-02 — El tutor devuelve tres piezas separadas, no un texto cocinado

- **Se eligió:** que `respond` devuelva un `TutorReply` —un `dataclass` congelado
  con `verdict`, `words` y `score`— en vez de la cadena `"veredicto\nWords: 3\n
  Score: 7"` que devolvía antes. La ruta `POST /practice` publica esas mismas
  tres claves en su JSON. Quien junta las piezas en un texto es quien las va a
  mostrar: hoy `main.py`, mañana la pantalla del paso 3.
- **Contra:** dejar la cadena ya armada, que era lo que había y funcionaba
  perfectamente para la terminal.
- **Por qué:** el destinatario cambia en el paso 3. Un texto cocinado solo le
  sirve a quien va a imprimirlo tal cual; a `app.ts` lo deja sin opciones —no
  puede pintar el marcador en su sitio, ni resaltar el veredicto, solo volcarlo
  entero—. 🔑 **El agente manda los ingredientes, no el plato servido:** la
  presentación es de quien tiene delante a la persona, no del que calcula.
  Se hizo ahora y no en el paso 3 porque cambiar el contrato con la pantalla ya
  escrita cuesta el doble. El `frozen=True` es aparte: una vez contestado, nadie
  cambia el veredicto por el camino.
- **Toca:** `app/english_tutor.py` (`TutorReply`, `respond`), `app/api.py`
  (`PracticeResponse`), `main.py` (que ahora arma el texto él), y los tests de
  ambos. Fija el contrato que leerá `app.ts` en el paso 3.

### [D-007] 2026-08-02 — El marcador se escribe al lado y se renombra encima (escritura atómica)

- **Se eligió:** que `add_point` escriba el total en un archivo temporal de la
  misma carpeta (`score.json.tmp`) y luego lo mueva encima del bueno con
  `os.replace`. El temporal va **en la misma carpeta**, no en la de temporales
  del sistema, y se usa `os.replace` y no `Path.rename`.
- **Contra:** dejar el `write_text` de siempre, que era lo que había. También se
  descartó envolver la escritura en un `try/except` que restaurara el archivo
  viejo: eso no cubre el caso que importa —un corte de luz no ejecuta el
  `except`—, y añade código para no resolver nada.
- **Por qué:** `write_text` hace dos cosas seguidas, vaciar el archivo y luego
  llenarlo, y entre las dos hay un instante. Un Ctrl-C o un corte justo ahí deja
  el marcador partido. Esto cierra la causa de raíz que [D-006] dejó abierta:
  aquel arreglo enseña a **leer** un archivo roto sin pisarlo, pero el archivo
  roto lo estábamos creando nosotros. Renombrar es **una sola** operación del
  sistema de archivos: o pasó entera o no pasó, así que ante un corte queda el
  marcador viejo entero o el nuevo entero, nunca un pedazo.
  Los dos detalles finos tienen su razón: renombrar solo es atómico **dentro
  del mismo disco** —cruzar de disco lo convierte en copiar y borrar, que es
  justo lo que se evita—, y `Path.rename` revienta en Windows si el destino ya
  existe, mientras que `os.replace` pisa igual en Windows y en Linux.
- **Toca:** `app/tools.py` (`add_point`) y dos tests nuevos en
  `tests/test_tools.py`: uno comprueba que no queda basura `.tmp`, y el otro
  simula el corte de luz reventando `os.replace` con `monkeypatch` y verifica
  que el marcador viejo sigue legible. El mismo patrón se repetirá en el paso 4,
  cuando el marcador pase a ser uno por persona.
  ⚠️ Un corte real sí puede dejar un `.tmp` huérfano en disco. Es inofensivo: la
  siguiente escritura lo pisa, y `read_score` ni lo mira.

### [D-006] 2026-08-02 — El marcador roto avisa con `ScoreFileError`; ausente sigue siendo 0

- **Se eligió:** separar los dos casos que hasta hoy se confundían.
  - **Ausente** (no hay archivo) → `0`, y a seguir. Es el primer día.
  - **Roto** (existe pero no se entiende) → excepción propia `ScoreFileError`,
    con mensaje en español que nombra el archivo y dice qué le pasa.
  - `read_score` valida tres cosas: que sea JSON, que tenga la clave `score`, y
    que su valor sea un entero de verdad — descartando `bool`, que en Python
    hereda de `int` y colaría un `true` por un `1`.
  - `add_point` **no atrapa** el error: lo deja subir. Como lee antes de
    escribir, la escritura ni se intenta y el archivo roto queda intacto.
  - `main.py` sí lo atrapa, imprime el mensaje y sale. Es la única lógica que
    le corresponde, porque presentar errores a una persona es su trabajo.
- **Contra:** devolver `0` cuando el archivo no se puede leer, que era el camino
  fácil y el que no habría necesitado excepción ninguna. También se descartó
  dejar subir el `JSONDecodeError` de la librería estándar tal cual.
- **Por qué:** devolver `0` en silencio le diría "tienes cero puntos" a alguien
  que tenía seis, y encima le pisaría el archivo con un `1` en el siguiente
  intento. 🔑 **Nunca sobrescribas un dato que no lograste entender:** mientras
  el archivo roto siga entero, su marcador es recuperable a mano; en cuanto se
  pisa, ya no. Se comprobó de verdad — con el archivo partido a la mitad
  todavía se lee `"score": 6` dentro.
  Y la excepción es propia, no la de `json`, porque en el paso 2 FastAPI tiene
  que distinguir "el marcador está roto" —que es un 500 con su mensaje— de
  cualquier otro fallo. `JSONDecodeError` solo dice que algún JSON, en algún
  sitio, no se pudo leer.
- **Toca:** `app/tools.py` (`ScoreFileError`, `read_score`, `add_point`),
  `main.py` (el `try/except`), los 8 tests nuevos de `tests/test_tools.py`, y el
  manejo de errores del paso 2. La causa de raíz —`write_text` no es atómico, así
  que este arreglo curaba la lectura del archivo roto pero no impedía crearlo—
  quedó cerrada el mismo día en [D-007].

### [D-005] 2026-08-02 — Nombres en inglés, contenido en español

- **Se eligió:** partir el idioma por su función, no por el archivo.
  - **En inglés** lo que es *identificador*: funciones, variables, archivos,
    carpetas, ramas y mensajes de commit. Y los textos que ve quien usa la app,
    porque es una app para practicar inglés.
  - **En español** lo que es *explicación*: comentarios, docstrings, la
    conversación del chat, y los mensajes de error o de sistema.
  - Consecuencia inmediata: el agente es `english_tutor`, con guion bajo. Con
    guion no se puede importar — `import english-tutor` es un error de sintaxis,
    porque Python lee el guion como una resta.
- **Contra:** nombrar todo en español, que era el camino por defecto viniendo de
  un `CLAUDE.md` y un `_context/` escritos enteros en español.
- **Por qué:** son dos públicos distintos. El identificador lo lee Python, lo leen
  las librerías y lo lee cualquiera que abra el repo; ahí el inglés es el idioma
  franco y evita el híbrido feo (`contar_words`, `leer_score`). La explicación la
  lee quien está aprendiendo, y en su idioma se entiende mejor. El error de
  sistema es explicación, no interfaz: cuando algo se rompe, tiene que entenderse
  rápido y sin traducir.
- **Toca:** todo el código que se escriba desde el paso 1. Renombra los contratos
  acordados: `count_words`, `judge_grammar`, `read_score`, `add_point`,
  `respond`, y los archivos `app/english_tutor.py`, `app/tools.py`,
  `data/score.json`. Queda escrito en `CLAUDE.md`, sección "Cómo se escribe el
  código", como principio **PI-5**.

### [D-004] 2026-08-02 — El protocolo de inicio lee `_context/` siempre, no a demanda

- **Se eligió:** añadir `_context/scope.md` y `_context/roadmap.md` a la lectura
  obligatoria del Paso 1 de `protocol-start`, junto a `progress.md` y `tasks.md`.
  Encima, una regla que manda sobre todas: lo que el reporte diga sobre **qué es**
  el proyecto tiene que salir de un archivo abierto en esa misma corrida; si no
  está escrito, se dice "no está registrado". En `session-starter` se partió el
  límite de "no inventes" en tres: no inventar el proyecto, no dar un paso por
  completado con tareas abiertas de ese paso, y no recomendar prioridades.
- **Contra:** dejar `_context/` fuera del protocolo, como estaba, y confiar en que
  el agente lo abriera si lo necesitaba.
- **Por qué:** el agente arranca en frío y solo veía el *relato* del avance, nunca
  la *definición* del proyecto. Sin el ancla, el hueco lo rellena con lo que suele
  llevar un proyecto de este tipo — y suena convincente, que es lo peligroso. Los
  dos archivos son cortos: leerlos siempre cuesta poco y el reporte pasa a ser
  verificable. Lo de las prioridades venía de la corrida real de hoy, donde el
  reporte recomendó saltarse cuatro tareas abiertas: esa llamada es del usuario.
- **Toca:** `.claude/skills/protocol-start/SKILL.md` (Paso 1) y
  `.claude/agents/session-starter.md` (Límites). Las descripciones del frontmatter
  de ambos se actualizaron el mismo día para nombrar las tres fuentes reales —`git`,
  `_persistence/` y `_context/`— cerrando la T-009.

### [D-003] 2026-08-02 — Recuperar 4 principios de ingeniería de un `CLAUDE.md` anterior

- **Se eligió:** llevar a `CLAUDE.md`, en una sección propia "Cómo se escribe el
  código", cuatro principios de un `CLAUDE.md` genérico de proyectos IA/DS:
  razonar sin decidir en silencio, simplicidad primero, cambios quirúrgicos y
  "terminado = visto funcionando".
- **Contra:** copiar los seis originales tal cual.
  - Se descartó **"slices verticales / tracer bullet"**: el roadmap ya *es* eso
    —tubería completa con agente falso, modelo en el paso 8, "córrelo antes de
    seguir"—. Repetirlo sería duplicar.
  - Se descartó **"sin decisiones silenciosas"** como principio aparte: decía lo
    mismo que "razona antes de actuar", y su parte de documentar ya la cubre este
    archivo.
  - Se reescribió **"toda tarea tiene un test, sin excepción"**: la pantalla del
    paso 3 no se prueba con un test unitario. Quedó como "donde hay lógica, un
    test; donde hay pantalla, correrla".
- **Por qué:** `CLAUDE.md` prometía "la FORMA es de producto: estructura,
  commits, tests, frenos" sin ninguna regla detrás. Era una promesa sin cobrar.
  Y nada frenaba el refactor no pedido, que es justo lo que ensucia el `git diff`
  del que vive `session-closer`.
- **Toca:** todo el código que se escriba desde el paso 1.

### [D-002] 2026-08-02 — Los cuatro archivos del porqué los escribe la sesión principal, no el closer

- **Se eligió:** partir `_persistence/` por origen de la información.
  `progress.md` y `tasks.md` los escribe `session-closer` al cerrar; `decisions`,
  `assumptions`, `constraints` y `lessons` los escribe la sesión principal, en el
  momento en que las cosas pasan. El closer solo los **revisa** y señala huecos.
- **Contra:** que el closer actualizara los seis al final del día, como estaba
  planteado al principio.
- **Por qué:** lo que se hizo queda en el `git diff` y se puede reconstruir sin
  haber estado presente. Lo que se **decidió** no queda en ningún lado: nace en la
  conversación y ahí se muere. El closer arranca en frío, así que escribir esos
  cuatro sería inventar. Además, el porqué es lo primero que se evapora: anotarlo
  tres horas después es anotarlo a medias.
- **Toca:** `CLAUDE.md` (sección Persistencia), `protocol-close` (Paso 5) y el
  reparto de trabajo entre la sesión principal y `session-closer`.

### [D-001] 2026-08-02 — La skill de inicio se llama `protocol-start`, no `protocol-close`

- **Se eligió:** `protocol-start` para el protocolo de inicio de sesión.
- **Contra:** `protocol-close`, que fue el nombre con el que se creó.
- **Por qué:** el nombre describía un cierre y el contenido era el arranque. El
  nombre quedó libre para lo que de verdad lo necesitaba: el protocolo de cierre,
  creado después. Hoy el par es simétrico —`protocol-start` / `protocol-close`—
  y cada agente tiene el suyo.
- **Toca:** `.claude/skills/`, y el cuerpo de `session-starter`, que invoca la
  skill por su nombre.

<!-- La más reciente arriba. Formato:

### [D-001] 2026-08-02 — <qué se decidió, en una línea>

- **Se eligió:** <la opción>
- **Contra:** <las alternativas descartadas>
- **Por qué:** <la razón, no el resumen>
- **Toca:** <qué parte del proyecto condiciona>

-->
