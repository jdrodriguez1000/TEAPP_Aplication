# Restricciones — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [C-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

Tipos: 💰 dinero · ⏱️ tiempo · 🔧 plataforma · 📦 alcance

| id | fecha | límite | tipo |
|---|---|---|---|
| C-006 | 2026-08-05 | **El regalo es UNO POR PERSONA, no uno por cuenta.** Atado a la identidad y a la tarjeta, no al correo. 🚨 Hay **una sola ventana de 6 meses en toda la vida** para aprender AWS, y no es renovable. Abrir una segunda cuenta para conseguir más deja inelegible **también la que ya se tenía** | 💰 |
| C-005 | 2026-08-05 | 🚨 **El plan gratuito se pierde SIN QUERER, con clics que no parecen peligrosos**, y no se puede volver. Son **siete puertas, verificadas** (Organization, Control Tower, Partner Network, Professional Services, Enterprise Agreement, Skill Builder Team, HIPAA/SEC). Con las **dos primeras los créditos se evaporan en el acto**; de las otras cinco **la doc calla, y se tratan como si también** (denegar por defecto). En las siete, la tarjeta queda viva y no hay vuelta atrás | 💰 |
| C-004 | 2026-08-05 | **Lo que solo existe porque se hizo clic a clic, está perdido de antemano.** La cuenta del plan gratuito **se va a cerrar**: todo lo que se monte allá arriba tiene que quedar escrito y reproducible desde el repo | 📦 |
| C-003 | 2026-08-05 | **El plan gratuito de AWS cambió el 2025-07-15 y ya no es el de los tutoriales:** 6 meses y $200 en créditos, sin las 750 horas de EC2. La instancia consume créditos, así que **el tamaño de la máquina dejó de ser un detalle técnico y es una decisión de presupuesto** | 💰 |
| C-002 | 2026-08-04 | **El tope de 500 caracteres protege el bolsillo, no el ancho de banda.** Medido: un cuerpo de 5 MB se sube ENTERO y luego recibe el 422. Frenarlo antes es del paso 7 | 🔧 |
| C-001 | 2026-08-03 | Nada sale a internet **a buscar algo que le falta**, ni en los tests ni en el cierre. Medida el 2026-08-04 (`T-047`) | 🔧 |

---

## Entradas

### [C-006] 2026-08-05 — El regalo es uno por persona, y la ventana no vuelve

- **Tipo:** 💰 dinero
- **El límite:** verificado en los términos de AWS — *"You are not eligible to
  receive Free Tier Credits for more than one account"*. Está atado a la
  **identidad y a la tarjeta**, no al correo. Abrir varias cuentas para conseguir
  más créditos deja inelegible para **todo, incluida la cuenta que ya se tenía**.
- **Qué permite y qué no:**

  | | ¿se puede? |
  |---|---|
  | otra app educativa en la **misma** cuenta | **sí**, comparte los $200 y los 6 meses |
  | cuenta **nueva** para otra app | **no**, y no es una regla estirable |

- 🔑 **Y aquí `[D-029]` paga por un motivo por el que no se eligió.** La misma
  máquina EC2 puede servir varias apps: Caddy está hecho justo para eso. Otro
  nombre de DuckDNS y unas líneas de configuración — **ni otra máquina, ni otra
  IP, ni otro céntimo**. Es lo mismo que pasó con el offset fijo de `[D-024]`:
  una decisión tomada por un motivo, que acaba pagando por otro.
- ⚠️ **El precio de compartir máquina, que sí hay que decir:** las apps quedan
  **acopladas**. Comparten disco, memoria y suerte. Una que se desboque tumba a
  la otra. Para un ejercicio educativo es aceptable; en un producto no lo sería.
- 🚨 **La consecuencia grande: hay UNA SOLA ventana de 6 meses en toda la vida**
  para aprender AWS. No es por proyecto y no se renueva. Empieza el día del clic.
- **Qué impide, y es contraintuitivo:** impide **abrir la cuenta a la ligera**, y
  también **dejarla parada**. Una ventana irrepetible que corre sola premia
  llegar con trabajo listo para meter dentro — que es exactamente la razón de la
  regla 4 de `CLAUDE.md`, ahora con un motivo más fuerte del que tenía escrito.

### [C-005] 2026-08-05 — El plan gratuito se pierde sin querer, y no se vuelve

- **Tipo:** 💰 dinero
- **El límite:** AWS pasa la cuenta al **plan de pago sola, sin pedir
  confirmación**, si se hace alguna de **estas siete cosas**. La **lista de
  siete** está verificada el 2026-08-05 (`T-068`): la FAQ del plan gratuito y la
  documentación de facturación traen la misma frase palabra por palabra. Antes
  eran tres **supuestas** — ver `[L-016]`.

  | # | la puerta | ¿qué pasa con los créditos? |
  |---|---|---|
  | 1 | crear o unirse a una **AWS Organization** | 💀 **se evaporan en el acto** — literal |
  | 2 | montar un **Control Tower landing zone** | 💀 **se evaporan en el acto** — literal |
  | 3 | entrar al **AWS Partner Network** | ❓ **la doc calla** |
  | 4 | firmar un contrato de **Professional Services** | ❓ **la doc calla** |
  | 5 | entrar en un **Enterprise Agreement** con AWS | ❓ **la doc calla** |
  | 6 | comprar **AWS Skill Builder Team** | ❓ **la doc calla** |
  | 7 | marcar la cuenta **HIPAA o SEC compliant** | ❓ **la doc calla** |

- 🚨 **La columna de la derecha se lee con cuidado, porque aquí ya se metió la
  pata una vez.** AWS solo se moja con las dos primeras: *"if you upgrade to paid
  plan **by joining an AWS Organization or setting up an AWS Control Tower
  landing zone**, your Free Tier credits expire immediately, and your account
  will be ineligible to earn more"*. De las otras cinco **no dice ni que se
  salvan ni que se pierden**. La frase de que los créditos siguen aplicándose a
  facturas futuras existe, pero es del **upgrade manual** — el que haces tú a
  propósito — y no de estas cinco.
- 🔑 **Y por eso las cinco desconocidas se tratan COMO SI evaporaran.** No es
  pesimismo: es **denegar por defecto**, la regla 3 de `CLAUDE.md`, la misma que
  ya está en el código desde el nivel 4 con `PERMISOS.get(nombre, "prohibir")`.
  Sin dato se asume lo caro, para que el olvido falle hacia el lado seguro.
- ⚠️ **Ojo con los Términos, que son la fuente que manda** — es la que se firma.
  Solo hablan de Organizations, ni mencionan Control Tower, y lo dicen **peor**:
  *"you will no longer be able to **use or earn** credits offered under the Free
  Tier"*. 📌 **Tres fuentes que coinciden en un párrafo no coinciden
  automáticamente en el siguiente:** la coincidencia se verifica **por
  afirmación, no por documento** (`[L-016]`).
- **Y cuando ocurre pasan tres cosas, las tres malas:**
  1. Los créditos **se dan por perdidos**. Comprobado en las puertas 1 y 2;
     asumido en las otras cinco por denegar por defecto.
  2. La tarjeta queda **viva**. Desde ese momento todo lo que corra se factura.
  3. **No se puede volver.** Del plan de pago no se baja al gratuito.
- 📌 **Y una a favor, con su letra pequeña:** el plan gratuito **bloquea de
  fábrica** servicios que podrían vaciar los créditos. AWS cita como **ejemplos**
  Savings Plans, Reserved Instances y parte del AWS Marketplace — y la frase
  empieza con *"Some service examples include"*, así que **es una muestra, no el
  inventario**: AWS no publica la lista completa de lo que bloquea. La regla 3
  está puesta por la plataforma, pero **no es inventariable** y no sustituye a la
  alarma. Lo que sí dice es dónde está el peligro: no en los servicios que usa la
  app, sino en los botones administrativos.
- 🔑 **La forma es la de siempre en este proyecto, y es su tercera aparición en el
  paso 7: el freno no se rompe tocándolo — se rompe cambiando lo que lo rodea.**
  *"AWS no puede cobrarme"* no es una propiedad de la cuenta: **es una propiedad
  del plan**. Un clic en el sitio equivocado la desactiva entera, y **desde dentro
  todo se sigue viendo igual**.

  | dónde ya pasó | qué anuló el freno sin tocarlo |
  |---|---|
  | `[D-027]` | el registro abierto anulaba la cuota |
  | `[D-029]` | el disco efímero anularía `quota.py` |
  | **aquí** | **un clic administrativo anula la protección de la tarjeta** |

- **Qué impide, en dos capas que NO se ordenan — son distintas:**
  - **Prevenir → la lista de "esto nunca se toca"** en el documento de clics, con
    los nombres escritos. Ninguno hace falta para el paso 7: **no son botones que
    se vayan a necesitar, son botones con los que uno se cruza.** Ver `T-068`.
  - **Detectar → la alarma de facturación**, con umbral en **cualquier cargo
    distinto de cero**, no en una cifra alta. 🔑 El primer cargo no nulo
    **significa que ya no se está en el plan gratuito**: es el síntoma, no el
    gasto.
- 🚨 **Y lo que hay que tener claro para no confiarse: la alarma NO es un freno,
  es un detector de humo.** No impide cruzar; avisa **después**, y el cruce es
  irreversible. Cuando suene, los créditos ya se evaporaron y no hay nada que
  deshacer. Lo único que compra es **tiempo**: enterarse en horas en vez de en
  semanas, y bajar la máquina antes de que el goteo importe.
  - ⚠️ Y compra menos tiempo del que parece: **los datos de facturación de AWS no
    son instantáneos**, van con retraso. Cuánto exactamente, verificarlo el día
    que se monte la alarma — no se escribe de memoria (regla 6).
  - 📌 **Por qué aun así la alarma vale más que la lista, incluso ahora que la
    lista está verificada.** La lista ya no está incompleta —`[A-016]` se cerró
    el 2026-08-05— pero sigue protegiendo solo de las puertas **que AWS documenta
    hoy**, y `[C-003]` es la prueba de que estas reglas cambian de un mes a otro.
    La alarma no necesita saber por qué puerta se entró: **detecta el resultado,
    venga de donde venga**. Es la regla 3 de `CLAUDE.md` al derecho — una lista
    de prohibiciones falla hacia el lado inseguro en cuanto se queda vieja; un
    detector, no.

### [C-004] 2026-08-05 — Lo que solo existe porque se hizo clic a clic, está perdido

- **Tipo:** 📦 alcance
- **El límite:** todo lo que se monte en la nube tiene que quedar **escrito y
  reproducible desde el repo**. Nada de configuración hecha a mano en la consola
  que nadie apuntó.
- **De dónde sale:** no la impone AWS — la impone **la fecha de caducidad**.
  TEAPP en internet es un ejercicio, la cuenta se cierra a los 6 meses
  (`[C-003]`) y eso **está bien**: es la mejor red de seguridad que hay para
  alguien con cero experiencia en la nube. No habrá un "se me olvidó algo
  encendido en 2027".
- 🔑 **Pero esa misma caducidad convierte cada clic en trabajo que se borra.** Si
  algo solo existe porque se hizo a mano, muere con la cuenta y no queda ni el
  aprendizaje. **Esto no es una restricción del paso 7: es lo que hace que el
  paso 7 valga algo.**
- **Qué impide:** configurar en la consola sin dejar rastro. En la práctica pide
  una carpeta `deploy/` en el repo con el guion de instalación, la configuración
  del proxy y el arranque automático. Y para lo que de verdad **no** se puede
  escribir —los clics de abrir la cuenta— un documento que los liste en orden.
- ⚠️ **Y lo que esto NO justifica: Terraform.** Sería la sexta cosa nueva del
  proyecto, y PI-2 lo prohíbe. Un guion de shell leído y entendido cumple el
  límite; una herramienta de infraestructura sin entender, no.

### [C-003] 2026-08-05 — El plan gratuito de AWS ya no es el que dicen los tutoriales

- **Tipo:** 💰 dinero
- **El límite:** verificado contra la documentación oficial. El 2025-07-15 AWS
  cambió el modelo, y **el "12 meses gratis" de todos los tutoriales YA NO EXISTE
  para cuentas nuevas**:

  | | qué hay hoy |
  |---|---|
  | créditos | $100 al abrir, y hasta $100 más por usar ciertos servicios |
  | duración | **6 meses, o hasta gastar los créditos — lo que pase primero** |
  | al terminar | AWS **cierra la cuenta**; 90 días de gracia para pasar a plan de pago, después borrado permanente |
  | siempre gratis | 30+ servicios con límites mensuales que no caducan |
  | 🚨 EC2 | **ya NO tiene las 750 horas dedicadas: consume créditos** |

- 🔑 **Y la parte buena, que es enorme: en el plan gratuito AWS NO PUEDE COBRAR
  LA TARJETA.** Su FAQ lo dice literal — *"AWS will not charge your payment method
  until you upgrade to paid plan"*. La tarjeta se pide solo para verificar
  identidad. **El escenario clásico —me dejé algo encendido y me llegó una
  factura— no puede ocurrir.** Si se acaban los créditos, la cuenta se cierra: no
  cobra, **apaga**.
- ⚠️ **La trampa que sí hay:** del plan de pago **no se puede volver** al
  gratuito. Es viaje de ida.
- **Qué impide, y son dos cosas concretas:**
  1. **Instancia pequeña.** La holgura del presupuesto es la de una `t3.micro`
     (`[A-015]`). Cuatro tallas más arriba se come los $200 antes de los 6 meses,
     y ahí sí manda la resta y no el calendario.
  2. **La IPv4 pública se cobra aparte**, esté o no en uso, y no estaba en la
     estimación inicial.
- 📌 **Esto no cancela la alarma de facturación: la RECOLOCA.** El roadmap la
  pedía para proteger la tarjeta, y la tarjeta ya está protegida por el propio
  plan. Ahora vigila **el reloj de 6 meses y los $200**. Sigue siendo el primer
  clic; lo que cambió es **qué está mirando**.

### [C-002] 2026-08-04 — El tope de la frase protege el bolsillo, no el ancho de banda

- **El límite:** `MAX_SENTENCE_LENGTH` (500) se comprueba **dentro** de la ruta
  `/practice`, y para entonces el cuerpo de la petición **ya se leyó entero**.
  Quien mande 5 MB los sube igual; lo único que se impide es que ese texto llegue
  al modelo.
- **Medido, no supuesto** (2026-08-04, uvicorn de verdad):

  | lo que se mandó | subido | respuesta |
  |---|---|---|
  | frase de 500 | — | `200` |
  | frase de 501 | — | `422`, y dice cuánto se pasó |
  | frase de 5.000.000 | **5.000.016 bytes** | `422` |

  Los 5 MB salieron enteros por el cable antes de que nadie los rechazara.
- 🔑 **Por qué se acepta así hoy.** Son dos problemas distintos con dos frenos
  distintos: el **dinero** lo frena esta línea, y el **ancho de banda** lo frena
  el servidor de delante, que todavía no existe. Escribir hoy un freno de
  tamaño de cuerpo sería inventarse una pieza que la plataforma del paso 7 trae
  hecha.
- ⚠️ **Lo que hay que hacer en el paso 7:** poner un tope de tamaño de cuerpo en
  el servidor de delante. Sin él, la puerta acepta subidas de cualquier tamaño y
  las paga quien tenga la cuenta abierta.
- **Y lo que NO se rompe:** una frase demasiado larga **no gasta cuota y no llega
  al tutor** — comprobado en la misma corrida, el contador se quedó en 1.

### [C-001] 2026-08-03 — Nada sale a internet a buscar algo que le falta

> ✏️ **Redacción corregida el 2026-08-04**, al medirla (`T-047`). Antes decía
> *"la suite no toca la red, y nada de lo que corre en el cierre tampoco"*. Esa
> frase era **falsa desde el día que el `git push` entró en el cierre** (`D-016`):
> un push va a GitHub por internet. Lo que la restricción quiere decir de verdad
> es lo de arriba. 🔑 **`npx` es el peligro; `git push` es el trabajo.** Salir a
> buscar algo que te falta te hace depender de que esté ahí y de que no haya
> cambiado; mandar tu propio código a un sitio que elegiste, no.

- **Tipo:** 🔧 plataforma
- **El límite:** ni los tests ni el protocolo de cierre salen a internet a
  **obtener** nada: ni una dependencia, ni un binario, ni una respuesta de una
  API. Sí está permitido mandar lo propio a donde se decidió mandarlo (`git push`).
- **De dónde sale:** no lo impone nadie de fuera — **es una propiedad que el
  proyecto ya tiene y de la que depende**, y estaba sin escribir. Ese era el
  problema: nadie puede respetar a sabiendas un invariante que no está anotado.
  Un `npx tsc` metido con buena intención lo habría roto sin que nadie lo notara,
  porque `npx` sale a internet a bajar lo que le falte.
- **Qué impide:**
  - Nada de `npx` ni de descargas en tests ni en el protocolo de cierre: se llama
    al binario que ya está en disco, y si no está, se reporta — ver [D-017].
  - Ninguna prueba puede llamar a la API de verdad. La que lo necesite, se marca
    y se corre a mano.
- **Cómo se comprueba — son dos comprobaciones, no una:**
  - **La mitad "tests", automática.** El portero de `tests/no_network.py` corre
    en cada `pytest` y revienta si algo intenta salir. Que el portero siga
    mordiendo se reverifica con `python -m pytest tests/check_no_network.py`
    (ver [D-022]).
  - 🚨 **La mitad "cierre", a mano y para siempre.** El portero **no ve los
    subprocesos**: `node` y `git` son otro proceso y salen por delante de sus
    narices sin que se entere. No es un arreglo pendiente, es cómo está
    construido. Se comprueba mirando que `node_modules/typescript/` esté en
    disco y que en `protocol-close` no aparezca `npx`.
- **Medición del 2026-08-04 (`T-047`):** se cumple. 192 tests verdes con la red
  cortada; los 5 controles del portero, verdes. `node_modules/typescript/bin/tsc`
  en disco (v7.0.2), sin descarga.
<!-- La más reciente arriba. Formato:

### [C-001] 2026-08-02 — <el límite, en una línea>

- **Tipo:** 💰 / ⏱️ / 🔧 / 📦
- **El límite:** <cuál es exactamente>
- **De dónde sale:** <quién o qué lo impone>
- **Qué impide:** <lo que no se puede hacer por su culpa>

-->
