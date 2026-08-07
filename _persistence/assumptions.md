# Suposiciones sin comprobar — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [A-000]`. Búscala con `grep`, no leas el archivo entero.

⚠️ Aquí vive **solo lo que no se ha comprobado**. Cuando una suposición se
comprueba o se decide, **sale de aquí** y entra en `decisions.md` o `lessons.md`.

## Índice

| id | fecha | qué se está dando por cierto | riesgo si es falsa |
|---|---|---|---|
| A-021 | 2026-08-06 | **Que una tarjeta firmada valga aunque su cuenta no exista no hace daño en la v1.** El mecanismo está **MEDIDO, no leído** (corrida del 2026-08-06): se registró una cuenta, se practicó, se borró la cuenta del almacén dejando la cookie intacta — y `/practice` siguió contestando `200` y `/me` siguió diciendo `efimero`. La identidad sale solo de la firma (`app/api.py:554` → `_current_user` → `sessions.read`); **nadie consulta `accounts.json` después del login**. ⚠️ Lo que NO está comprobado es que sea inofensivo. Se sostiene sobre dos patas: la v1 **no tiene forma de borrar una cuenta** (no hay ruta que lo haga), y **firmar exige la llave**, que vive en el servidor. 📌 Nació de una deducción equivocada —ver `[L-023]`— y se re-verificó por su cuenta antes de escribirla | si aparece el borrado de cuentas, o si la llave se filtra, **no hay revocación SELECTIVA**: cortar una sola sesión es imposible, y cada `/practice` con una tarjeta así **crea marcador y cuota de un fantasma** en `data/` — la misma clase de archivo huérfano que abrió `T-072`. 🔨 La palanca que sí existe es tosca y hay que tenerla pensada de antemano: **cambiar `TEAPP_SECRET_KEY` invalida TODAS las sesiones de golpe** (`[A-008]`), incluida la que sobra |
| A-018 | 2026-08-06 | **La alarma de facturación avisará el día que haga falta.** Están creadas **dos** alertas en un mismo presupuesto —coste **real** y coste **previsto**, ambas a 0,01 US$ absoluto— y el correo está verificado, pero **ninguna se ha visto saltar**. 🔴 Corregida dos veces el 2026-08-06. **El silencio NUNCA la confirma.** ✅ Resuelto que el presupuesto mide coste **BRUTO** (leído en pantalla): los créditos no enmascaran nada, no hace falta un segundo presupuesto, y la EC2 encendida **tiene que** hacerla sonar. 🧪 **Experimento escrito por adelantado, con tabla de lectura y DOS observaciones** (la factura = premisa, la bandeja = prueba); disparador: reservar **solo la Elastic IP**, que cobra estando ociosa. ⏳ El umbral de $0,01 **no se toca hasta después** — cambiarlo destruiría el experimento. 🔄 **Dos lecturas el 2026-08-07, las dos NO CONCLUYENTES.** La 2ª (14:36 UTC, ~23,1 h desde `t=0`) encontró tres cosas: (a) `Facturas` **era la ventana equivocada las dos veces** — una factura nace al cerrar el mes, su *"sin datos"* habla del calendario, no del gasto; la lectura buena es el campo *Importe utilizado* del **propio presupuesto**, que es el **mismo instrumento** que la alarma → hoy **0,00 US$ con un `0.00%` calculado**, un cero de verdad y no una ausencia, pero aún dentro del retraso; (b) ✅ **AWS no puede proyectar sin historial** — *Importe previsto* = `-`, leído en pantalla: la alerta de coste **previsto** no pudo disparar y su silencio no prueba nada; (c) 🔴 **corregido en caliente**: se iba a cerrar con "aplican las 750 h gratis de IPv4" y la documentación dice lo contrario — esas horas son para direcciones **EN USO**, y la nuestra está **ociosa**, así que **sí cobra** (~23 h × 0,005 US$/h ≈ 0,115 US$ bruto, >10× el umbral; aritmética de lista, no corrida). El disparador es válido y el experimento **sigue siendo falsable**. 🚨 **ENMIENDA SELLADA el 2026-08-07, antes de mirar nada: la FILA 3 de la tabla original de `cfba50a` queda ANULADA** (no borrada — se lee con autoridad y nombraba una causa hoy desmentida). `= 0,00` ya **no** significa "es gratis": quedan dos causas vivas, **(a)** el dato no aterrizó → esperar, **(b)** algo absorbe el cargo → hallazgo; los créditos ya están descartados porque mide bruto. 🚨 **Y guardia nueva sobre la FILA 2**: los presupuestos se refrescan *"up to three times a day … 8–12 hours after the previous update"* (documentación, 2026-08-07) → **"alarma rota" exige ≥12 h de silencio DESPUÉS de que el importe sea visible**. 🔴 **El motivo se corrigió DOS veces:** ni *"son dos retrasos en serie, ~24 h + 8–12 h ≈ 36 h"*, ni *"eso era doble conteo"* —**la segunda afirmaba de más**, porque llamarlo doble conteo **es** afirmar que comparten reloj, el mismo dato que la frase declaraba desconocido. ✅ Queda **un solo desconocido**: *no se sabe si lo que se MUESTRA y lo que se EVALÚA salen del mismo refresco*; si lo comparten faltan **minutos**, si van desacoplados faltan **horas**. La regla se queda porque esperar de más no produce conclusión falsa en **ninguna** rama. 🎁 Y hay **medición gratis**: se anotan `h1` (importe visible > 0,01) y `h2` (llega el correo); `h2 − h1` es un número que no tiene ni la documentación y **resuelve el desconocido** — la espera pasa a ser la **segunda medición** (`LM.19`). ⚖️ **Precio del cambio de instrumento, escrito:** premisa y prueba ahora cuelgan las dos del servicio de presupuestos — falla del lado seguro, pero el experimento **ya no cubre** un fallo en la entrada de datos, solo el tramo "el presupuesto vio el dinero → mandó el correo". ⏳ **Tercera lectura 2026-08-07 tarde: sigue 0,00**, y el presupuesto **explicó su propio silencio** con un **CUARTO reloj** que no estaba escrito — *"después de crear un presupuesto, pueden transcurrir hasta 24 h para que se rellenen todos los datos de gastos"*, que arranca en la **creación del presupuesto** (06 durante el día, antes de las 15:29 UTC) y vence **durante el 07**. Refuerza la causa (a) con motivo documentado, **no cierra nada** —*"hasta"* vuelve a ser techo, no promesa—. Próxima lectura **2026-08-08**, con el reloj 4 ya vencido; el criterio ya **no** es "que desaparezca un mensaje" —eso falló— sino que *Importe utilizado* deje de ser 0,00 | 🚨 el día del gasto no avisa nadie, y se descubre por el saldo. Y aunque avise bien, **con ~24 h de retraso no puede frenar las 7 puertas de `[C-005]`**, que evaporan los créditos *"en el acto"*: protege del goteo, no del acantilado |
| A-017 | 2026-08-05 | **DuckDNS seguirá en pie los 6 meses del paso 7.** Comprobado que existe y funciona hoy, **no que vaya a durar**: es gratuito, se sostiene con donaciones y tiene caídas registradas — una el 2026-06-21 y un episodio en agosto de 2025 en que se dio por desaparecido | 🚨 **no es que se vea feo: es que no entra nadie.** Sin nombre no resuelve, sin resolver Caddy no renueva el certificado, sin certificado la cookie `Secure` no viaja. El servidor sigue encendido y la app cerrada |
| A-015 | 2026-08-05 | **El paso 7 cabe de sobra en los $200: gasta del orden de $50.** Es aritmética de lista de precios, **no una corrida**, y le falta el costo de la IPv4 pública. Sobre esta holgura se descartó la pieza que apaga la máquina sola (`[D-029]`) | se acaban los créditos antes de los 6 meses y AWS cierra la cuenta a media obra |
| A-014 | 2026-08-04 | **`request.client.host` es el origen REAL de quien pregunta** (🔻 **encogida el 2026-08-06**: el mecanismo ya está MEDIDO — uvicorn 0.52.1 reescribe esa dirección desde `X-Forwarded-For` y solo se fía si la petición llega por loopback, ver `[D-034]`. Lo que queda sin comprobar **no es Python**: que Caddy escriba de verdad esa cabecera, y que el cortafuegos de `T-060` deje el 8000 cerrado para que nadie más pueda hablarle a uvicorn) | detrás de un proxy todo el mundo llega con la misma dirección: el primero que falle 5 veces deja fuera a todos los demás |
| A-013 | 2026-08-04 | **5 fallos y 15 minutos son los números correctos** para el tope de intentos de `/login`. Predicción, no medida. 🔑 Y lo que decide el número no es cuánta gente ataca, sino **cuánta comparte origen**: el freno reparte 5 por dirección, no por persona ([D-026]) | corto, deja fuera a quien solo se equivocó recordando su contraseña; largo, quien prueba a la fuerza tiene sitio de sobra |
| A-011 | 2026-08-04 | **10 segundos es lo que hay que esperar al tutor.** Predicción: hoy no hay nada que tarde, así que no hay nada que cronometrar | corto, se corta a quien iba a contestar bien; largo, la petición cuelga y el hilo con ella |
| A-010 | 2026-08-04 | **20 prácticas al día por persona es el tope correcto**: predicción, no número final. Se mide en el paso 8, cuando haya facturas | o frena a quien estudia de verdad, o deja pasar una factura que duele |
| A-009 | 2026-08-04 | La cookie con `secure=True` funciona — nunca se ha ejecutado esa rama: los 192 tests la apagan (🔻 **encogida el 2026-08-06** por `T-052`: la rama **ya tiene testigo** — cuatro tests miran la cabecera `Set-Cookie` en crudo con el ajuste por defecto, en registro, login y logout. Lo que sigue sin comprobar es lo de fuera de Python: que un navegador de verdad, por `https://`, guarde esa cookie y la devuelva. Eso es `T-051`) | el inicio de sesión no funciona en la nube, y el fallo es mudo: el navegador descarta la cookie sin decir nada |
| A-008 | 2026-08-04 | `TEAPP_SECRET_KEY` es la MISMA en cada arranque, y sigue siéndolo tras redesplegar (🔻 **encogida el 2026-08-07**: el guion de instalación **ya no la pisa, y está MEDIDO sin EC2** — dos corridas reales en contenedor Ubuntu, misma huella `7915abd41bf6`; y el sabotaje de borrar el `.env` la cambió a `e3f588ea2399`, así que la medida **puede ponerse roja**. Lo que queda sin comprobar **no es el guion**: que `teapp.service` lea ese `.env` bajo systemd, que el disco sobreviva a un reinicio, y que una sesión viva aguante el redespliegue — el enunciado literal de `T-050`) | todas las sesiones mueren de golpe y todo el mundo queda fuera, sin ningún error que lo explique |
| A-007 | 2026-08-04 | Entre el Paso 2b del cierre y el `git add` no se toca ningún `.ts` | se comprueba un `.js` y se commitea otro: el control da verde sobre un archivo que ya no es el del commit |
| A-006 | 2026-08-03 | La ruta de `mktemp -d` de Git Bash le sirve a `node`, que es un binario de Windows | el control del `.js` del Paso 2b no compila nunca: siempre "SIN COMPROBAR" |
| A-005 | 2026-08-03 | `data/` vive en el **disco del servidor**, y ese disco sigue ahí mañana (🔻 encogida el 2026-08-05: `[D-029]` ya **eligió** el disco; lo que queda sin comprobar es que se comporte) | el marcador se borra solo al redesplegar: `scope.md` promete lo contrario |
| A-002 | 2026-08-02 | El archivo de **una misma persona** lo escribe un solo proceso a la vez (🔻 encogida el 2026-08-03 por el paso 4) | el candado deja de servir y los puntos de esa persona se vuelven a perder |
| A-001 | 2026-08-02 | El marcador cuenta frases **practicadas**, no correctas | hay que cambiar el contrato de `judge_grammar` |

---

## Entradas

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
  golpe**, porque una firma hecha con otra llave deja de cuadrar (`[A-008]`, y está
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
  alcanzarse. Es `[L-013]` en versión alarma — verde porque **no existe nada
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

🔑 **Y la corrección de las 750 horas es la lección de `[L-013]` otra vez:** se
tenía una explicación cómoda que cerraba el caso —"es gratis, por eso no cobró"—
y era **de memoria**. Treinta segundos de documentación la tiraron. Una
explicación que cierra un experimento merece la misma comprobación que el
experimento.

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
  teapp` dice que todo está bien, y los tests pasan. Es la familia de `[A-009]`.
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

### [A-014] 2026-08-04 — La dirección que lee el servidor es la de quien pregunta

- **Se supone que:** `request.client.host` —lo que `_request_origin` lee en
  `app/api.py`— es de verdad **quien está al otro lado**, y no un intermediario.
- **Por qué nace hoy:** es la mitad de `[A-012]` que `T-053` **no** resolvió. El
  freno de intentos existe, sí; pero un freno que cuenta por origen no vale más
  que el dato con el que separa un origen de otro. Ver `[L-014]`.
- 🔑 **Hoy es cierta y el día del despliegue deja de serlo de golpe**, exactamente
  como le pasaba a `A-012`. No se degrada poco a poco: cambia el día que haya un
  servidor de delante — el mismo que va a poner el tope de tamaño de cuerpo de
  `[C-002]`. A partir de ahí, **todas** las peticiones llegan aquí con la
  dirección del proxy.
- **Cómo se comprobaría:** desplegar, entrar desde dos dispositivos distintos y
  mirar qué dirección escribe el log en el renglón `Demasiados intentos`. Si es
  la misma para los dos, la suposición ya es falsa.
- **Si es falsa:** el freno se convierte en el ataque. Todo el mundo comparte
  cubo, así que **cinco fallos de cualquiera dejan fuera a todos los demás
  durante quince minutos** — y quien quiera tumbar la app solo tiene que fallar
  cinco veces cada cuarto de hora.
- ⚠️ **Y el arreglo tiene su propia trampa**, por eso queda con dueño en `T-055`
  y no se hace hoy: la dirección real viaja en una cabecera (`X-Forwarded-For`) y
  **esa cabecera la puede escribir cualquiera**. Leerla sin un proxy de confianza
  delante que la reescriba es peor que no tener freno: quien ataca cambia de
  origen en cada intento y no se frena nunca.

---

🔻 **ENCOGIDA el 2026-08-06 — la mitad de Python ya está medida.** Se levantó
uvicorn 0.52.1 de verdad (no `TestClient`) y se le mandaron logins fallidos hasta
el 429, mirando qué origen escribía el log. Resultado: **con `--proxy-headers` y
`--forwarded-allow-ips 127.0.0.1` el freno cuenta la dirección real, y descarta
la cabecera de quien no llega por loopback.** La tabla de los cuatro escenarios
está en `[D-034]` y **solo ahí** — no se copia (`[L-018]`). `_request_origin` no
se toca.

**Lo que sigue vivo en esta entrada, y por qué no es lo mismo:**

| lo que falta | por qué no lo resuelve la medición de hoy |
|---|---|
| que **Caddy escriba** `X-Forwarded-For` | hoy la cabecera la puso a mano el guion de prueba. Que Caddy la ponga es documentación, no corrida |
| que el **8000 esté cerrado** (`T-060`) | es un clic en la consola de AWS. Sin eso, cualquiera se salta Caddy entero — sin HTTPS y sin tope de cuerpo |

🔑 **Y por eso `T-066` no sobra.** Sigue siendo la corrida que cierra esto:
entrar desde dos dispositivos y mirar el renglón `Demasiados intentos`. Si los
dos escriben la misma dirección, algo de la cadena real no hace lo que hoy se
midió por piezas.

⚠️ **La lección de por qué esta medición estuvo a punto de mentir está en
`[L-019]`.**

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

### [A-011] 2026-08-04 — 10 segundos es lo que hay que esperar al tutor

- **Se supone que:** `TUTOR_TIMEOUT_SECONDS = 10.0` deja contestar a una llamada
  sana al modelo y corta las que se han quedado colgadas.
- 🔑 **Es una predicción, igual que el 20 de [A-010].** Hoy el tutor es falso y
  contesta al instante: **no hay nada que cronometrar**. El número no sale de
  ninguna corrida.
- **Cómo se comprobaría:** en el paso 8, midiendo cuánto tarda de verdad una
  llamada al modelo con una frase de nivel A1. El tope tiene que quedar
  cómodamente por encima de la llamada lenta normal, no de la media.
- **Si es falsa:**
  - **Corto de más:** se corta a quien iba a contestar bien. Se ve como 504 con
    el modelo funcionando — desconcertante, porque no hay nada roto.
  - **Largo de más:** quien pregunta espera de balde, y el hilo sigue ocupado
    todo ese rato.
- 🚨 **Lo que este freno NO arregla, y no es una suposición sino un hecho:**
  libera a quien pregunta, no al hilo. Python no sabe matar un hilo. Comprobado
  el 2026-08-04 con uvicorn: 504 a los 10,02 s contra un tutor de 30 s, y el
  hilo siguió durmiendo sus 30. ⚠️ **Por eso en el paso 8 la llamada al modelo
  necesita su propio timeout**, además de este: uno acota lo que espera quien
  pregunta, el otro lo que espera el servidor.

### [A-010] 2026-08-04 — 20 prácticas al día es el tope correcto

- **Se supone que:** 20 prácticas diarias por persona es un tope que deja
  estudiar de verdad y a la vez frena una factura antes de que duela.
- 🔑 **Es una predicción, no un número final.** Sale de un criterio razonado
  —"una sesión de estudio larga cabe, un bucle automático no"— pero **no de
  ninguna corrida**: hoy el tutor es falso y no cuesta nada, así que no hay nada
  que medir. Entra al código como valor por defecto, no como verdad.
- **Cómo se comprobaría:** en el **paso 8**, con el modelo enchufado y facturas
  de verdad. Dos medidas, no una:
  1. **Por arriba:** 20 prácticas × el costo real de una llamada = el techo de
     gasto diario de una persona. Si ese número asusta, 20 es demasiado.
  2. **Por abajo:** cuántas prácticas hace de verdad alguien en una sesión. Si
     nadie llega a 20 nunca, el freno no frena nada y da falsa tranquilidad;
     si todo el mundo choca contra él, estorba.
- **Si es falsa:** en un sentido, el freno estorba a quien estudia y hay que
  subirlo. En el otro, deja pasar 20 llamadas al modelo por persona y día, y esa
  cuenta la paga quien abrió la cuenta.
- **Por eso el tope se inyecta** ([D-023]): cambiar el número no puede obligar a
  tocar la lógica ni a reescribir tests.

### [A-009] 2026-08-04 — La cookie con `secure=True` funciona, y nunca se ha ejecutado esa rama

- **Se supone que:** cuando `cookie_secure()` devuelve `True`, `set_cookie` marca
  la cookie como `Secure` y el inicio de sesión sigue funcionando.
- **Por qué nace hoy:** `tests/conftest.py` pone `TEAPP_COOKIE_SECURE=false` con
  `autouse=True`, así que vale en **los 192 tests**. Se buscó en toda la suite el
  2026-08-04 y no hay ni un test que lo ponga en `true`. Y `cookie_secure()`
  devuelve `True` **cuando la variable no está puesta**, que es el valor por
  defecto y el seguro.
- 🔑 **El camino por defecto es el que menos se prueba, precisamente porque las
  pruebas lo apagan para poder trabajar.** El `false` no está ahí por capricho:
  sin él, el cliente de pruebas —que habla por `http://`— descartaría la cookie y
  fallarían todos los tests de sesión. La suite tiene que apagarlo para funcionar,
  y al apagarlo deja de mirar el otro lado.
- **De la familia de `[L-010]`, con otra cara.** Allí un test miraba el efecto y
  no la respuesta; aquí la suite mide un modo y da por bueno el otro. Las dos
  veces el hueco no estaba en lo que el test afirmaba, sino en lo que ni se
  planteaba.
- **Qué pasa si es falsa:** en el paso 7 se pone `true` **en producción**, y esa
  rama correría por primera vez en la nube. Si algo estuviera mal, el fallo es
  mudo: el navegador descarta la cookie sin ningún error, ni en pantalla ni en el
  log del servidor. Se parecería a "el inicio de sesión no hace nada".
- **Cómo se comprobaría:** un test que **anule el `autouse`**, ponga
  `TEAPP_COOKIE_SECURE=true` y compruebe que `set_cookie` recibe `secure=True`.
  📌 Queda como tarea del paso 7 en `tasks.md`, no de hoy.
- ⚠️ **Es un hueco conocido, no un descuido.** Se encontró y se midió el mismo
  día que se escribió el código; lo que se decidió fue **cuándo** taparlo.

---

🔻 **ENCOGIDA el 2026-08-06 — la rama ya tiene testigo (`T-052`).** Cuatro tests
nuevos en `tests/test_api.py`, bajo "El interruptor de la cookie segura": el
valor por defecto, la cookie del registro, la del login y el borrado de
`/logout`. De 310 a **314 tests**.

**Dos ajustes sobre cómo estaba enunciada la comprobación aquí arriba**, y los
dos hacen el test más fiel, no más cómodo:

| decía | se hizo | por qué |
|---|---|---|
| poner `TEAPP_COOKIE_SECURE=true` | **borrar** la variable | así se mide el defecto **de verdad** — el que correrá en la nube si nadie escribe nada— y no una copia nuestra de lo que creemos que es |
| comprobar que `set_cookie` recibe `secure=True` | mirar la cabecera `Set-Cookie` **en crudo** | el tarro de galletas de `TestClient` descarta la cookie, y hace bien: habla por `http://`. Lo que hay que medir es lo que el servidor **envió** |

🚨 **Y cubre los DOS sitios donde vive `cookie_secure()`**, no uno: `_start_session`
—por donde salen registro y login— y el `delete_cookie` de `/logout`. El segundo
es el que se olvida: un borrado que no case con la cookie entregada es un
"cerrar sesión" que no cierra nada, otra vez sin error.

**Sabotaje doble, siguiendo `[L-019]`** — resultado *y* montaje:

1. Invertido el valor por defecto en `config.py` (`"true"` → `"false"`): **los
   cuatro en rojo**. Miden lo que dicen medir.
2. Quitado el fixture a uno de los tests: **rojo también**, y con la cabecera sin
   `Secure` a la vista. El fixture es quien hace el trabajo, no la suerte.

⚠️ **Lo que NO cierra esto, y por eso la entrada sigue viva:** que un navegador
de verdad, por `https://`, guarde esa cookie y la devuelva. Eso es Python
hablando consigo mismo hasta que haya máquina. **`A-009` muere con `T-051`.**

### [A-008] 2026-08-04 — La llave de firma es la misma en cada arranque

- **Se supone que:** el valor de `TEAPP_SECRET_KEY` **no cambia** entre un
  arranque del servidor y el siguiente, ni al redesplegar en el paso 7.
- **Por qué nace hoy:** el paso 5 firma las sesiones con esa llave
  (`app/sessions.py`). Una firma solo se reconoce con la misma llave que la hizo.
- **Qué pasa si es falsa:** 🚨 **todas las sesiones abiertas mueren de golpe y
  todo el mundo queda fuera.** Nadie pierde su cuenta ni su marcador —eso vive en
  disco—, pero todos tienen que volver a escribir su contraseña.
  ⚠️ **Esto no es un fallo: es cómo funciona una firma.** Se anota justamente
  para que el día que pase no se busque un error que no existe. El síntoma es
  desconcertante —todo el mundo desconectado a la vez, sin nada en el log— y
  lleva derecho a sospechar de las cookies o del navegador.
- **Cómo se comprobaría:** arrancar, entrar, parar el servidor, cambiar la llave
  del `.env`, arrancar otra vez y recargar la página. Tiene que pedir la
  contraseña de nuevo. El caso contrario —misma llave, sesión que sobrevive al
  reinicio— **sí está comprobado hoy**, en la corrida real del 2026-08-04.
  📌 Está probado desde el otro lado en `test_a_card_signed_with_another_key_is_rejected`:
  ahí se ve que cambiar la llave invalida la tarjeta. Lo que queda sin comprobar
  es que la llave **no** cambie sola en la nube del paso 7.
- **Dónde muerde de verdad:** en el paso 7, cada vez que se redespliega.
  ⚠️ **Reescrito el 2026-08-07.** Decía *"si la **plataforma** genera la variable
  al desplegar"*, y eso ya no describe nada: `[D-029]` eligió EC2, donde no hay
  plataforma que inyecte nada. Quien puede generar la variable de más es **el
  guion**, `deploy/install.sh`, y por eso el riesgo se concentró ahí — ver el
  encogimiento de abajo. `[L-025]`.

#### 🔻 Encogida el 2026-08-07 — el guion de instalación ya NO la pisa, y está MEDIDO

**Sin EC2.** El guion real corrió **dos veces** en un contenedor Ubuntu 24.04
(montaje en `[L-024]`). De la llave se guardó **huella `sha256`, nunca el valor**
— regla 7.

| corrida | qué dijo el guion | huella de la llave |
|---|---|---|
| 1ª | `==> Creando .env` | `7915abd41bf6` |
| 2ª | `==> .env ya existe, no se toca` | `7915abd41bf6` — **idéntica** |
| 🧪 sabotaje: se borra el `.env` | `==> Creando .env` | `e3f588ea2399` — **cambió** |

🔑 **El sabotaje es la mitad que vale.** Sin él, dos huellas iguales podrían
significar "la llave es estable" o "el montaje no sabe ver un cambio" —`[L-013]`,
verde porque nada puede ponerlo rojo. La tercera fila demuestra que la medida
**sí distingue**. Es `[L-019]`: se verifica el montaje, no solo el resultado.

🚨 **Y ese sabotaje prueba el INSTRUMENTO, no el FRENO. Son cosas distintas y al
principio se confundieron.** Borrar el `.env` demuestra que el montaje sabe ver
un cambio de llave. No ejerce el `if`. El que sí lo ejerce se corrió después, el
mismo día: se anuló la guarda (`if [[ -f "${ENV_FILE}" ]]` → `if false`) dejando
la generación siempre en juego, y se corrió dos veces sobre base limpia.

| guion | huella tras la 2ª corrida |
|---|---|
| íntegro | `24dd6bc2520f` — igual que la 1ª |
| con la guarda anulada | `6ded9368fe44` — **cambió** |

**Eso es ver al freno morder:** con el `if` puesto la llave se conserva, sin él se
regenera. Queda demostrado que lo que la protege es esa línea y no una casualidad
del montaje. 📌 Sustituye al test de forma —leer el texto del guion y comprobar
que unas líneas siguen dentro de un `if`— que se descartó por ruidoso y ciego
(`[L-024]`): esto mide comportamiento, no dónde están las líneas.

De paso quedó visto en la misma corrida: `.env` con permisos `600 ubuntu:ubuntu`,
llave de 64 caracteres hex, y `TEAPP_COOKIE_SECURE=true` /
`TEAPP_REGISTRATION_OPEN=false` escritos — la mitad de fichero de `T-051` y
`T-056`.

🚨 **Lo que NO se midió, y por qué la suposición no muere:**
1. **Un contenedor no es EC2.** No hubo systemd —el guion muere en `systemctl:
   command not found`—, así que **nadie ha visto a `teapp.service` leer ese
   `.env`**. Que el archivo sea correcto no prueba que el servicio lo use.
2. **Ni un reinicio de máquina, ni un disco de verdad** (`[A-005]`, `T-065`).
3. **Ni una sesión viva sobreviviendo al redespliegue**, que es el enunciado
   literal de `T-050`. Aquí se midió el **mecanismo** (la llave no cambia), no el
   **efecto** (nadie queda fuera).

⏳ **Muere del todo con `T-050` corrida en EC2 más `T-065`.** Hasta entonces está
encogida: el riesgo que quedaba era *"el guion la regenera al reinstalar"*, y ese
ya está descartado con una corrida.

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

### [A-005] 2026-08-03 — `data/` vive en el disco del servidor, y ese disco sigue ahí mañana

- **Se supone que:** los marcadores `data/users/<nombre>.json` —uno por persona
  desde el paso 4— viven como **archivos en el disco del servidor**, y ese disco
  es el mismo mañana que hoy. Sobre eso descansa la promesa de `_context/scope.md`: un
  marcador "que sigue ahí mañana".
- **Por qué está aquí:** `_context/architecture.md` dice de `data/` **dónde no
  va** (a Git, no) pero **no dice dónde vive**. En todo el documento no aparece la
  palabra "base de datos", ni para elegirla ni para descartarla. Hoy son archivos
  porque es lo que salió del paso 1, no porque se haya decidido.
- 🔻 **2026-08-05 — `[D-029]` la ENCOGE, no la mata.** Esta entrada llevaba dos
  preguntas pegadas, y la elección de plataforma solo contesta una:
  - *¿Dónde vive el disco?* **Ya está decidido**: en el volumen de una máquina
    EC2. Y es más: 🔑 **esta suposición es la que decidió la plataforma entera.**
    Fue leerla al derecho —"casi todas las plataformas modernas dan un disco
    efímero"— lo que descartó Lambda, App Runner y Fargate.
  - *¿Ese disco sigue ahí mañana?* **Sigue sin comprobarse.** Elegir bien no es
    medir. Hasta que no se despliegue y se reinicie de verdad, es una promesa de
    la documentación, no una corrida. **Por eso la entrada se queda aquí.**
  - 📌 Y baja de riesgo por otro lado: `[D-029]` deja escrito que el disco
    **persiste al reiniciar, pero se va si se borra la máquina**, y que no hay
    copia de seguridad de nada. Eso ya no es suposición: es un límite aceptado.
- **Por qué hoy no se nota:** en local el disco es el mismo siempre. Se apaga el
  servidor, se enciende, y el archivo sigue ahí. La suposición es **cierta en
  local** y por eso no molesta hasta el paso 7.
- **Cómo se comprobaría:** en el paso 7, sumar puntos, **volver a desplegar** la
  aplicación, y mirar el marcador. Si volvió a cero, la suposición era falsa.
- **Si es falsa:** el marcador y la memoria de cada persona se borran solos, sin
  error y sin aviso, cada vez que se actualice o se reinicie la aplicación.
  Es el peor tipo de fallo: **no rompe nada, solo olvida.** Y el arreglo no es un
  parche — es sacar `data/` a algo que viva fuera del servidor (una base de datos
  o un almacenamiento aparte), lo que toca `app/tools.py` entero.
- **Relación con [A-002] — son hermanas, no la misma:**
  - `A-002` pregunta **quién escribe a la vez** → el candado.
  - `A-005` pregunta **dónde está lo escrito** → el disco.
  Se pueden romper por separado: un disco que sobrevive no arregla dos procesos
  pisándose, y un candado perfecto no sirve si el archivo desaparece al
  redesplegar.
- ⚠️ **Se mira en el paso 7, no antes.** Elegir almacenamiento hoy sería una
  pieza nueva sin problema que resolver. Lo que valía era **dejarlo escrito**: la
  decisión es cara de deshacer, y aplazarla en silencio era la única forma mala
  de aplazarla.

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

### [A-001] 2026-08-02 — El marcador cuenta frases practicadas, no correctas

- **Se supone que:** el marcador mide **esfuerzo**, no acierto. `respond()` llama
  a `add_point()` siempre, sin mirar el veredicto, y eso se queda así.
- **Por qué está aquí y no en `decisions.md`:** la pregunta se planteó hoy y no
  se eligió entre las dos lecturas. Se anota como suposición —que es lo que
  es— en vez de dejarla sin escribir. **Está sin decidir.**
- **Por qué hoy no se nota:** el juez es falso y aprueba todo. Con `judge_grammar`
  devolviendo siempre el mismo veredicto, "practicadas" y "correctas" dan
  exactamente el mismo número. Las dos lecturas son indistinguibles hasta el
  paso 8.
- **Cómo se comprobaría:** en el paso 8, con el modelo enchufado, escribir una
  frase claramente incorrecta —`me likes coffees`— y mirar el marcador.
  - Si sube y eso es lo que se quería → la suposición era cierta. Sale de aquí y
    entra en `decisions.md`.
  - Si sube y chirría → era falsa. Sale de aquí y entra en `lessons.md`.
- **Si es falsa:** no basta con un `if` en `respond()`. Hoy el contrato es
  `judge_grammar(sentence) -> str`: devuelve **texto libre**, y nada dentro de
  esa cadena le dice a `respond` si la frase estaba bien. Contar aciertos obliga
  a cambiar el contrato de la herramienta para que devuelva algo que una máquina
  pueda leer —un aprobado/suspenso junto al mensaje—, y eso arrastra a `respond`
  y a lo que se le pida al modelo en el paso 8.
  🔑 El coste de equivocarse crece con el tiempo: hoy es un contrato que nadie
  usa todavía; en el paso 8 sería rediseñar la herramienta el mismo día que se
  enchufa el modelo, con dos sospechosos en vez de uno.
- **A favor de dejarlo así:** `_context/scope.md` pide que el agente "responda en
  tono positivo", y la v1 es de nivel A1. Un marcador que solo sube al acertar
  castiga justo a quien más se está esforzando.

<!-- La más reciente arriba. Formato:

### [A-001] 2026-08-02 — <qué se supone, en una línea>

- **Se supone que:** <la afirmación sin comprobar>
- **Cómo se comprobaría:** <la prueba concreta>
- **Si es falsa:** <qué se rompe>

-->
