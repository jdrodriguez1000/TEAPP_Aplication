# Los clics que no se pueden escribir

> 🔑 **Todo lo demás de esta carpeta es un archivo que se ejecuta. Esto no.**
> Aquí viven los pasos que solo existen dentro de la consola de AWS, donde no
> hay guion que valga. Por eso están escritos: `[C-004]` dice que **lo que solo
> existe porque se hizo clic a clic, está perdido de antemano**, y esta cuenta
> se va a cerrar.

**Se lee entero antes de tocar nada.** No es una guía de consulta: es el guion.
Se entra a la consola a **ejecutar** esta lista, no a decidir dentro de ella.

---

## 🚨 ESTO NUNCA SE TOCA

**Siete botones. Ninguno hace falta para TEAPP.** No son botones que se vayan a
necesitar: son botones con los que uno **se cruza** — aparecen en menús
laterales, en banners y en asistentes de "configura tu cuenta".

| # | no tocar | qué pasa si se toca |
|---|---|---|
| 1 | **AWS Organizations** — crear una o unirse | 💀 créditos evaporados **en el acto** |
| 2 | **AWS Control Tower** — montar un *landing zone* | 💀 créditos evaporados **en el acto** |
| 3 | **AWS Partner Network** — entrar | ❓ AWS no lo dice → se asume 💀 |
| 4 | **Professional Services** — firmar contrato | ❓ AWS no lo dice → se asume 💀 |
| 5 | **Enterprise Agreement** — enrolarse | ❓ AWS no lo dice → se asume 💀 |
| 6 | **AWS Skill Builder Team** — comprar suscripción | ❓ AWS no lo dice → se asume 💀 |
| 7 | **HIPAA / SEC compliant** — marcar la cuenta | ❓ AWS no lo dice → se asume 💀 |

**Los siete hacen lo mismo, y es lo peor:** pasan la cuenta al **plan de pago
sin pedir confirmación**, dejan la tarjeta viva, y **no tienen vuelta atrás** —
del plan de pago no se baja. Lista verificada el 2026-08-05 (`T-068`). El
detalle, las citas literales y por qué las cinco de la ❓ se tratan como 💀 está
en `_persistence/constraints.md`, entrada `[C-005]`.

⚠️ **Esta lista NO es un freno: es disciplina** (`[L-026]`). No se puede verificar
—probarla es el desastre—, y a diferencia de un freno **se degrada con la
repetición**. Se relee entera antes de cada sesión de clics, no una vez.

### 🚨 Y uno más, que NO va en la lista de arriba: **"Actualizar plan"**

**Visto en pantalla el 2026-08-07**, en la cabecera de *Facturación y costos*,
junto al aviso *"No se cobrará nada a la cuenta del plan gratuito"*. No es
"actualizar los datos": es **pasar del plan gratuito al de pago**.

🔑 **Y por eso no es la puerta número 8.** Las siete de arriba comparten algo: **hay
que ir a buscarlas**. Nadie aterriza en Control Tower sin desviarse. Esta está en
la cabecera de la página que hay que abrir **todos los días** mientras dure el
experimento de `[A-018]`, pegada al aviso tranquilizador que sí hay que leer.

**El riesgo no se mide por lo peligrosa que es la puerta, sino por cuántas veces
pasas por delante.** De las ocho, es la única con **tráfico garantizado**. Ponerla
como renglón 8 le daba el peso de Control Tower, y tiene otro. Su sitio es el
protocolo de lectura:

> 📖 **Al abrir *Facturación y costos*: se lee UN campo — `Importe utilizado` del
> presupuesto. NO se toca NADA de la cabecera.**

🔑 **La diferencia con los siete de arriba es la que lo hace peligroso.** Aquellos
están en menús a los que no se entra nunca. Este está **en la pantalla a la que
sí hay que volver**: la de facturación, la del presupuesto, la de las facturas,
la del método de pago. Es el único botón de la familia que está a centímetros de
donde el dedo tiene que ir de todos modos.

📌 **Cambiar o añadir tarjeta es seguro** y no está en esta lista — se hace en
*Preferencias de pago* / *Métodos de pago*, del mismo menú lateral. Se marca la
nueva como predeterminada **antes** de quitar la vieja: una cuenta sin método de
pago válido se puede suspender. ❓ Sin verificar en documentación: la consulta a
`ctx7` falló por red el 2026-08-07. **Gana la pantalla el día que se haga.**

---

⚠️ **Esta lista protege de las puertas conocidas HOY.** `[C-003]` es la prueba de
que estas reglas cambian de un mes a otro. **Lo que de verdad protege es la
alarma de facturación del paso 1**, porque detecta el resultado sin necesitar
saber por qué puerta se entró.

---

## Paso 1 — Abrir la cuenta, y la alarma como primer clic (`T-057`)

🚨 **El clic de "crear cuenta" arranca un reloj de 6 meses que no se para y no
se repite** (`[C-003]`, `[C-006]`). No se da hasta tener el resto de esta lista
leída y `deploy/` listo.

1. Registrarse con un **alias `+aws` del correo personal** (`[D-031]`).
   El valor literal **no se escribe aquí**: este repo es público.
2. Elegir **Free / plan gratuito**, no el de pago.
3. **Activar MFA en el usuario root en el mismo acto**, no "luego" (`[D-031]`).
   El root puede cerrar la cuenta y ver la tarjeta; es la única credencial que
   no se puede rotar.
4. 🚨 **Alarma de facturación, antes que ninguna otra cosa.** Billing and Cost
   Management → Budgets → presupuesto de coste.
   **Umbral: cualquier cargo distinto de cero.** No una cifra alta.
   🔑 El primer cargo no nulo no significa "voy gastando": significa **que ya no
   estás en el plan gratuito**. Es el síntoma, no el gasto.

   **Son DOS alertas dentro de UN solo presupuesto**, no dos presupuestos. Montado
   así el 2026-08-06:

   | desencadenador | umbral | qué mira |
   |---|---|---|
   | **Real** | 0,01 US$ absoluto | lo que ya se gastó — llega con ~24 h de retraso |
   | **Previsto** | 0,01 US$ absoluto | a dónde va la proyección — avisa antes del cargo |

   **Por qué dos y no una, para que dentro de tres meses no parezca duplicado:**
   la de coste **real** mira el retrovisor y hereda el retraso del punto 5. La de
   coste **previsto** mira hacia delante y recorta ese retraso. Se apoyan en el
   mismo presupuesto porque la API lo permite —`NotificationType: ACTUAL` y
   `FORECASTED` sobre el mismo budget— y una pieza menos es una pieza menos que
   se puede romper.

   ⚠️ **Ninguna de las dos protege del acantilado.** Contra las 7 puertas de
   `[C-005]` no hay aviso posible: los créditos se evaporan *en el acto*. Las dos
   alertas cubren el **goteo**; del acantilado solo protege la lista de arriba.
   Ver `[A-018]`.

   📌 **Umbral en valor ABSOLUTO, no en porcentaje.** Así, si algún día sube el
   importe del presupuesto, el aviso sigue saltando al primer céntimo.

   📌 **`Costes agregados por` se dejó en el valor por defecto: "costes sin
   combinar"** (`UseBlended: false`). Los créditos no se controlan ahí sino con
   `IncludeCredit`, que por documentación **viene en `true`** —
   `docs.aws.amazon.com/aws-cost-management/latest/APIReference/API_budgets_CostTypes`
   (consultado 2026-08-06). ⚠️ **Lectura de documentación, no visto en pantalla.**

   🔴 **CORREGIDO el 2026-08-06 — se escribió como buena noticia y es lo
   contrario.** Aquí decía que *"los $200 descuentan, así que el coste debería
   quedarse en cero"*, como si fuera tranquilizador. **Un presupuesto cuyo coste
   se queda en cero es un presupuesto que no puede saltar nunca**, ni cuando debe.

   | qué mide | qué significa que suene | qué NO vigila |
   |---|---|---|
   | **bruto** (`UNBLENDED_COST`) | "algo empezó a gastar" | — |
   | **neto** (`NET_UNBLENDED_COST`) | "los $200 se **terminaron**" | 🚨 el goteo: una máquina olvidada quema los créditos en silencio, y el aviso llega cuando ya no queda nada |

   ✅ **LEÍDO EN PANTALLA el 2026-08-06: mide BRUTO** (`Costes agregados por` =
   "costes sin combinar"). Los créditos **no** enmascaran el gasto, así que la
   alarma sí puede ver el goteo y **no hace falta un segundo presupuesto**.

   ⏳ **El umbral de $0,01 es PROVISIONAL y se cambia después del experimento de
   `[A-018]`.** Es el umbral correcto para *probar* la alarma y el equivocado para
   *vivir* con ella; el que lo sustituya sale de $200 ÷ 6 meses ≈ $33/mes, que es
   lo que convierte la alarma en vigilante del **ritmo de quema**.

   📌 **El experimento, sus dos observaciones y la tabla de lectura viven en
   `[A-018]` y SOLO ahí.** No se copian aquí a propósito — ver `[L-018]`: en este
   repo los datos se replican solos, y una copia es un sitio más donde mañana
   mentir.
5. Saber cuánto retraso llevan los datos de facturación, porque cambia cómo se
   lee la alarma del punto 4.

   > ⏳ **retraso: ~24 horas.** Fuente: documentación de AWS, *"The Billing and
   > Cost Management console data has a refresh time of approximately 24 hours
   > to reflect billing updates"* —
   > `docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/view-billing-dashboard`
   > (consultado 2026-08-06). ⚠️ Es dato de **documentación, no medido en
   > pantalla**.

   🔑 **La consecuencia práctica:** la alarma es de **coste real**, no previsto, y
   los datos llegan con hasta un día de retraso. Así que **la alarma es la red de
   seguridad, no el semáforo**: no sirve para hacer un experimento y ver si salta.

6. Anotar la **fecha de fin del plan** y el **saldo de créditos**. En cuentas
   creadas después del 2025-07-15 salen en la **portada de la consola**
   (fecha de expiración, créditos restantes y días que quedan) —
   `docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/tracking-free-tier-usage`.
   Se copian de pantalla, no se calculan. Van a `[C-006]`.

---

## Paso 2 — El nombre gratuito (`T-058`)

No necesita cuenta de AWS y no gasta reloj. Se puede hacer antes.

1. Entrar en `https://www.duckdns.org`. ⚠️ **No hay usuario y contraseña
   propios:** se entra con Google, GitHub, Reddit o Twitter. Comprobado el
   2026-08-05.
2. Sacar `teapp.duckdns.org`.
3. Guardar el **token**. Es un secreto: no va al repo.
4. La IP se apunta en el paso 3, cuando la Elastic IP exista.

🚨 **Sin este nombre no hay HTTPS.** Let's Encrypt se niega por política a emitir
certificados para `compute.amazonaws.com`. Y sin certificado, la cookie de
sesión —que es `Secure`— no viaja, y **no entra nadie** (`[D-029]`).

✅ **Lo que NO hay que instalar, aunque lo diga cualquier tutorial que busques.**
DuckDNS es DNS **dinámico**: existe para cuando tu IP cambia sola, y por eso todo
el mundo monta un cliente o un `cron` que la refresca cada pocos minutos.

**Aquí no hace falta ninguna de las dos cosas**, porque la Elastic IP del paso 3
**es fija**. Se apunta el nombre una vez y se acabó. El token hace falta para
configurarlo desde el navegador, pero **no vive en el servidor**.

> 🔑 Usamos DuckDNS solo como *"un nombre gratis que Let's Encrypt acepte"*. La
> mitad dinámica del servicio no la usamos — y una pieza que no se instala es una
> pieza que no se puede romper.

⚠️ **Lo que sí hay que saber:** DuckDNS es gratuito y se sostiene con donaciones,
y ha tenido caídas (`[A-017]`). Si un día deja de resolver, la app queda cerrada
aunque el servidor siga encendido. El plan B es otro proveedor de nombre
gratuito: son dos líneas —el `Caddyfile` y un registro DNS—, y por eso no se
prepara por adelantado.

---

## Paso 3 — La máquina (`T-059`)

🚨 **ANTES DE NADA: comprobar la región en el selector de arriba a la derecha.**
Tiene que decir **Norte de Virginia (`us-east-1`)** — el porqué está en `[D-033]`,
no se repite aquí. La consola trae **Ohio** por defecto, así que esto **hay que
mirarlo cada vez que se entra**, no una sola vez.

⚠️ **Se hereda sin avisar y no da error.** Una Elastic IP reservada en otra región
no sirve para una instancia en esta: hay que soltarla y pedir otra, **la nueva es
una dirección distinta**, y `teapp.duckdns.org` habría que reapuntarlo dos veces.

1. EC2 → Launch instance.
2. **Ubuntu Server LTS**, arquitectura **x86_64**.
3. Tipo **`t3.micro`**. ⚠️ El tamaño es una **decisión de presupuesto**, no
   técnica: ya no hay 750 horas gratis, la máquina consume créditos por estar
   encendida (`[C-003]`).
4. Crear un **par de llaves** y guardar el `.pem`. Es la única forma de entrar.
5. **Elastic IP**: reservarla y asociarla a la instancia. Sin ella, la IP cambia
   al apagar y encender, el nombre de DuckDNS deja de resolver, se cae el HTTPS
   y con él las sesiones.
6. Volver a DuckDNS y apuntar `teapp.duckdns.org` a esa IP.

---

## Paso 4 — El cortafuegos (`T-060a` escribirlo · `T-060b` medirlo)

Security group de la instancia. **Denegar por defecto**, como todo en este
proyecto — 🚨 **de ENTRADA. La salida es otra cosa, ver más abajo:**

| puerto | desde | para qué |
|---|---|---|
| 80 | cualquiera | que Let's Encrypt pueda validar el dominio |
| 443 | cualquiera | la app |
| 22 | **solo tu IP** | entrar a administrar |

🚨 **El 8000 NO se abre nunca.** Es donde escucha uvicorn, y `teapp.service` lo
ata a `127.0.0.1` justamente para que no se pueda llegar desde fuera. Abrirlo
sería saltarse Caddy: sin HTTPS y sin el tope de tamaño del cuerpo.

### 🚨 La SALIDA se queda abierta, y es deliberado

Las tres reglas de la tabla son de **entrada**. La **salida** viene abierta de
fábrica y **así tiene que quedarse**. La máquina necesita salir para tres cosas,
y las tres son imprescindibles:

| sale para | sin eso |
|---|---|
| bajar paquetes | `install.sh` no termina |
| que Caddy hable con Let's Encrypt | no hay certificado → no hay HTTPS |
| que la app llame a la API de Claude | el tutor no contesta |

⚠️ **Si algún día alguien "endurece" la salida, `install.sh` se muere — y se muere
pareciendo un problema de red, no una regla que alguien cambió.** Es el tipo de
avería que cuesta horas porque **el síntoma no apunta a la causa**. Queda escrito
aquí para que el día que pase, este sea el primer sitio donde se mire.

🔑 **"Denegar por defecto" es una regla sobre quién ENTRA.** Aplicarla a la salida
no es ser más estricto: es romper la máquina.

### 🔤 Las descripciones NO admiten tildes ni apóstrofos — medido el 2026-08-07

**Falló el primer intento de crear el grupo.** AWS contestó, literal:

> *Invalid rule description. Valid descriptions are strings less than 256
> characters from the following set:* `a-zA-Z0-9. _-:/()#,@[]+=&;{}!$*`

**Lo que NO está en ese conjunto y se cuela solo:** `á é í ó ú ñ ü` y el
**apóstrofo `'`**. La frase que lo tumbó fue *"que Let's Encrypt valide el
dominio"* — por el apóstrofo de `Let's`, no por una tilde.

⚠️ **Son DOS campos distintos con la misma restricción**, y el error solo nombra
el segundo: la descripción **del grupo** y la descripción **de cada regla**.

✅ **Descripciones seguras, ya limpias** (las de regla son opcionales; se pueden
dejar vacías):

| campo | texto |
|---|---|
| grupo | `Cortafuegos de TEAPP: entrada solo por 80, 443 y 22` |
| regla 80 | `Validacion del dominio por HTTP` |
| regla 443 | `La app` |
| regla 22 | `Administracion. Solo mi IP, cambia sola` |

📌 **Y lo que hizo bien AWS, que conviene saber:** al fallar, **deshizo el grupo
entero** (*"Restauración: eliminar el grupo de seguridad"*). No quedó un
cortafuegos a medias con dos reglas de tres. 🔑 Eso importa más que el error: **un
grupo incompleto tiene el mismo aspecto que uno completo**, y habría que
descubrirlo leyendo. Aquí no hizo falta.

### ⚠️ La VPC — la misma trampa de la región, un piso más abajo

El formulario va a pedir también una **VPC**, y es **exactamente el mismo animal**
que la región: un grupo creado en la VPC equivocada **no da ningún error**.
Simplemente **no aparece** al lanzar la instancia — y el reflejo vuelve a ser
coger el que sí aparece, que no tiene nada de esto escrito.

- **Si el desplegable ofrece UNA sola** (la `default` de `us-east-1`): no hay nada
  que elegir, se sigue.
- 🚨 **Si ofrece MÁS de una: parar y anotarlo antes de escoger.** Entonces hay una
  decisión que tomar, y se toma a propósito y se escribe — como se hizo con la
  región en `[D-033]`. No se coge la primera.

### ⚠️ El 22 y tu IP de casa — qué pasa el día que no puedas entrar

La consola ofrece un botón **"Mi IP"** que rellena tu dirección actual. Es cómodo,
pero **fija una dirección que probablemente cambie**: la mayoría de las conexiones
domésticas la rotan.

**El día que el SSH no entre, esa es la causa, y no es una avería.** Se arregla en
un minuto desde la consola: se edita la regla del grupo de seguridad con la IP
nueva y se vuelve a entrar.

🔑 **Queda escrito porque el instinto va a ser el equivocado.** Con la app en
producción y el SSH mudo, lo primero que se piensa es "se rompió el servidor". No
se rompió: **la instancia sigue corriendo y la app sigue atendiendo por 443
mientras tanto.** Es una molestia, no un cierre de puerta.

⚠️ **Y la regla del 22 es la única de las tres que caduca sola.** Las de 80 y 443
valen para cualquiera y no se tocan nunca.

### 🔑 Este paso son DOS, y la primera mitad no cierra nada

- **`T-060a` — escribirlo.** El grupo de seguridad existe y sus reglas dicen lo de
  la tabla. Se crea **suelto**, sin instancia, y es gratis; luego se engancha al
  lanzar la máquina.
- **`T-060b` — medirlo.** Un escaneo **desde fuera**, con la máquina viva, enseña
  el 8000 cerrado.

🚨 **Tener el grupo creado NO es tener el cortafuegos: es tenerlo escrito.** Marcar
`T-060` como hecha al terminar la primera mitad sería `LM.13` con otro traje — un
freno que nadie ha visto morder. Mismo motivo por el que `T-059` se partió en dos.

---

## Paso 5 — Instalar TEAPP

Ya no hay clics. Desde aquí manda `install.sh`; sus instrucciones están en
`deploy/README.md`.

---

## Paso 6 — Bajarlo con fecha en el calendario (`T-070`)

⚠️ **La cuenta se va a cerrar sí o sí.** A los 6 meses AWS la cierra sola y
borra los datos, con 90 días de gracia antes del borrado definitivo.

🔑 **Un cierre planeado se aprende; uno automático solo se sufre** (`[D-030]`).
Cuesta lo mismo. La diferencia es quién elige el día.

Antes de bajar nada, comprobar por última vez que `deploy/` levanta TEAPP desde
cero. 📌 **La cuenta es desechable. `deploy/` no.**
