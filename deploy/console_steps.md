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
5. Mirar y **anotar aquí** cuánto retraso llevan los datos de facturación. Sale
   escrito en la propia consola. No se escribe de memoria — regla 6.

   > ⏳ **retraso medido:** _(pendiente — se rellena el día que se abra)_

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

## Paso 4 — El cortafuegos (`T-060`)

Security group de la instancia. **Denegar por defecto**, como todo en este
proyecto:

| puerto | desde | para qué |
|---|---|---|
| 80 | cualquiera | que Let's Encrypt pueda validar el dominio |
| 443 | cualquiera | la app |
| 22 | **solo tu IP** | entrar a administrar |

🚨 **El 8000 NO se abre nunca.** Es donde escucha uvicorn, y `teapp.service` lo
ata a `127.0.0.1` justamente para que no se pueda llegar desde fuera. Abrirlo
sería saltarse Caddy: sin HTTPS y sin el tope de tamaño del cuerpo.

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
