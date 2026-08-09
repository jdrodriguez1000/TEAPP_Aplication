#!/usr/bin/env bash
#
# Instala TEAPP en una máquina Ubuntu recién creada.
#
# 🔑 **Por qué existe este archivo y no una lista de comandos en un cuaderno.**
# [C-004]: la cuenta de AWS se va a cerrar. Todo lo que solo exista porque
# alguien lo tecleó una vez está perdido de antemano. Esto se vuelve a correr
# en una máquina nueva y deja lo mismo.
#
# 🚨 **No pregunta nada** — regla 2 del proyecto. En un servidor no hay teclado:
# lo que espera a un humano se cuelga para siempre. Lo que necesita saber entra
# por variable de entorno, y si falta, se niega a seguir.
#
# Uso:
#     sudo TEAPP_DOMAIN=teapp.duckdns.org bash deploy/install.sh
#
# Antes de esto: los pasos 1 a 4 de `deploy/console_steps.md`, y el repo
# copiado en /opt/teapp.

# -e: a la primera que falle, se para. Sin esto, un fallo a mitad seguiría
#     adelante y dejaría la máquina a medio instalar, que es peor que no
#     instalada — porque parece que funcionó.
# -u: usar una variable que no existe es un error, no una cadena vacía.
# -o pipefail: en una tubería manda el primero que falle, no el último.
set -euo pipefail

INSTALL_DIR="/opt/teapp"
SERVICE_NAME="teapp"
APP_USER="ubuntu"

# ─────────────────────────────────────────────────────────────────────
# Comprobaciones antes de tocar nada
#
# 🔑 Denegar por defecto, igual que en el código: lo que no esté puesto
# explícitamente, se rechaza. Y todas las comprobaciones van JUNTAS y AL
# PRINCIPIO, para que el guion no se caiga a mitad dejando la máquina rara.
# ─────────────────────────────────────────────────────────────────────

if [[ "${EUID}" -ne 0 ]]; then
	echo "[Error] Esto instala paquetes y servicios: hace falta sudo." >&2
	echo "        sudo TEAPP_DOMAIN=... bash deploy/install.sh" >&2
	exit 1
fi

if [[ -z "${TEAPP_DOMAIN:-}" ]]; then
	echo "[Error] Falta TEAPP_DOMAIN (el nombre de DuckDNS, ver T-058)." >&2
	echo "        Sin nombre no hay certificado, y sin certificado no entra nadie." >&2
	exit 1
fi

if [[ ! -d "${INSTALL_DIR}" ]]; then
	echo "[Error] No existe ${INSTALL_DIR}." >&2
	echo "        Copia el repo ahi primero. Por ejemplo:" >&2
	echo "        sudo git clone <url-del-repo> ${INSTALL_DIR}" >&2
	exit 1
fi

DEPLOY_DIR="${INSTALL_DIR}/deploy"

echo "==> Instalando TEAPP en ${INSTALL_DIR} para ${TEAPP_DOMAIN}"

# ─────────────────────────────────────────────────────────────────────
# 1. Paquetes del sistema
# ─────────────────────────────────────────────────────────────────────

echo "==> Paquetes base"
# DEBIAN_FRONTEND=noninteractive: sin esto, algun paquete abre un menu de
# configuracion a pantalla completa y se queda esperando — regla 2 otra vez.
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv python3-pip curl debian-keyring \
	debian-archive-keyring apt-transport-https

# Caddy no esta en los repositorios de Ubuntu: hay que anadir el suyo.
if ! command -v caddy >/dev/null 2>&1; then
	echo "==> Instalando Caddy"
	curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' |
		gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
	curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' \
		>/etc/apt/sources.list.d/caddy-stable.list
	apt-get update -qq
	apt-get install -y -qq caddy
else
	echo "==> Caddy ya estaba instalado"
fi

# ─────────────────────────────────────────────────────────────────────
# 2. El entorno de Python
#
# ⚠️ Un entorno virtual y no los paquetes del sistema: `requirements.txt` fija
# versiones exactas ([L-002]), y pisar las del sistema rompe herramientas de
# Ubuntu que tambien usan Python.
# ─────────────────────────────────────────────────────────────────────

echo "==> Entorno de Python"
if [[ ! -d "${INSTALL_DIR}/.venv" ]]; then
	python3 -m venv "${INSTALL_DIR}/.venv"
fi
"${INSTALL_DIR}/.venv/bin/pip" install --quiet --upgrade pip
"${INSTALL_DIR}/.venv/bin/pip" install --quiet -r "${INSTALL_DIR}/requirements.txt"

# ─────────────────────────────────────────────────────────────────────
# 3. El `.env` de produccion
#
# 🚨 **No se copia el `.env.example` y ya.** Los valores de produccion son casi
# los contrarios a los de local: la cookie exige HTTPS y el registro por red
# esta cerrado.
#
# 🚨 **La llave se genera AQUI, en la maquina, y no se imprime nunca** — regla
# 7. Escribirla en el repo o pasarla por el historial de la terminal seria
# dejarla donde cualquiera la lea.
#
# ⚠️ Si el archivo ya existe NO se toca. Regenerar la llave tiraria fuera a
# todo el mundo de golpe, sin decir por que ([L-032], antes [A-008]).
# ─────────────────────────────────────────────────────────────────────

ENV_FILE="${INSTALL_DIR}/.env"

# 🚨 **La carpeta de los datos se crea AQUI, y solo aqui.** La app se niega a
# crearla: una ruta mal escrita se convertiria en una carpeta vacia y quien use la
# app pareceria haber perdido su marcador, sin un solo error ([D-037]). Crearla es
# un acto de instalacion, deliberado, y este es el sitio donde vive.
#
# ⚠️ `mkdir -p` no toca la carpeta si ya existe, asi que reinstalar NO borra los
# datos de nadie. Es la misma cautela que el `.env` de abajo.
# 🚨 **El destino lo manda el `.env` que ya existe, no este guion.** Fijar aqui
# `${INSTALL_DIR}/data` a ciegas y crearlo antes de mirar el `.env` fabrica **el
# senuelo que [D-037] existe para evitar**: si una instalacion anterior movio los
# datos a otro disco, aparece una carpeta vacia al lado de la app, no la usa
# nadie, y quien la vea concluye que se perdio el marcador de todo el mundo.
#
# 🔑 El guion no puede crear con la mano la trampa que el resto del proyecto
# esquiva. Se lee primero, se crea despues.
DATA_DIR="${INSTALL_DIR}/data"

if [[ -f "${ENV_FILE}" ]] && grep -q '^TEAPP_DATA_DIR=' "${ENV_FILE}"; then
	# `tail -n 1` porque si la variable estuviera repetida, al leer el archivo
	# manda la ultima. `cut -f2-` porque una ruta puede llevar un `=` dentro.
	DATA_DIR=$(grep '^TEAPP_DATA_DIR=' "${ENV_FILE}" | tail -n 1 | cut -d= -f2-)

	# Denegar por defecto: si lo que hay escrito no sirve, se para en seco. Antes
	# de esto, una linea vacia habria reventado el `mkdir` con un error del
	# sistema, ilegible; y una ruta relativa habria creado la carpeta en donde
	# tocara estar parado. Las dos son [D-037] otra vez.
	if [[ -z "${DATA_DIR}" || "${DATA_DIR}" != /* ]]; then
		echo "ERROR: el .env existente tiene TEAPP_DATA_DIR vacia o relativa." >&2
		echo "       Tiene que ser una ruta ABSOLUTA. Arreglalo a mano: ${ENV_FILE}" >&2
		exit 1
	fi

	echo "==> Manda el .env que ya existe, no el valor por defecto"
fi

echo "==> Carpeta de datos: ${DATA_DIR}"
mkdir -p "${DATA_DIR}"

if [[ -f "${ENV_FILE}" ]]; then
	echo "==> .env ya existe, no se toca (la llave de firma se conserva)"
else
	echo "==> Creando .env"

	# 🔑 **El archivo nace ya cerrado, vacio, ANTES de tener nada dentro.**
	# Escribir primero y hacer el `chmod` despues deja una ventana —corta, pero
	# real— en la que la llave existe en disco con los permisos que toque el
	# `umask` de root: legible por cualquier usuario de la maquina.
	# Son milisegundos y aqui solo hay un usuario. Se cierra igual, porque
	# cuesta una linea: el descuido tiene que caer del lado seguro.
	install -m 600 -o "${APP_USER}" -g "${APP_USER}" /dev/null "${ENV_FILE}"

	SECRET=$("${INSTALL_DIR}/.venv/bin/python" -c \
		"import secrets; print(secrets.token_hex(32))")

	cat >"${ENV_FILE}" <<-EOF
		# Generado por deploy/install.sh. NO se sube a Git.
		TEAPP_SECRET_KEY=${SECRET}

		# Donde viven los datos de las personas. Ruta ABSOLUTA y carpeta que ya
		# existe: el guion la acaba de crear. Sin esto la app no arranca ([D-037]).
		TEAPP_DATA_DIR=${DATA_DIR}

		# En la nube hay HTTPS de verdad: la cookie viaja solo cifrada.
		TEAPP_COOKIE_SECURE=true

		# Cerrado. Las cuentas se crean con create_account.py (ver [D-027]).
		TEAPP_REGISTRATION_OPEN=false

		# La llave de Claude entra en el paso 8, todavia no se usa.
		ANTHROPIC_API_KEY=
	EOF

	# La variable deja de existir en cuanto acabe el guion, pero se borra ya:
	# mientras viva, esta en la memoria del proceso.
	unset SECRET
fi

# 🚨 **El `.env` de una instalacion anterior no conoce `TEAPP_DATA_DIR`.** Si se
# deja asi, la app no arranca tras redesplegar — falla ruidosamente, que es lo
# querido, pero aqui se sabe el valor correcto y arreglarlo cuesta tres lineas.
#
# ⚠️ Solo se AÑADE si falta. Si ya esta, no se pisa: alguien pudo haberla movido a
# otro disco a proposito, y sobrescribirla dejaria los datos de las personas
# huerfanos en la carpeta vieja sin que nadie se entere.
if ! grep -q '^TEAPP_DATA_DIR=' "${ENV_FILE}"; then
	echo "==> Anadiendo TEAPP_DATA_DIR al .env existente"
	printf '\n# Anadida por install.sh: sin esto la app no arranca ([D-037]).\nTEAPP_DATA_DIR=%s\n' \
		"${DATA_DIR}" >>"${ENV_FILE}"
fi

# Solo su dueno puede leerlo. Dentro hay una llave.
chown "${APP_USER}:${APP_USER}" "${ENV_FILE}"
chmod 600 "${ENV_FILE}"

# El resto del proyecto tambien: el servicio corre como `ubuntu` y necesita
# poder escribir `data/`.
chown -R "${APP_USER}:${APP_USER}" "${INSTALL_DIR}"

# ─────────────────────────────────────────────────────────────────────
# 4. Arranque automatico
# ─────────────────────────────────────────────────────────────────────

echo "==> Servicio de systemd"
cp "${DEPLOY_DIR}/${SERVICE_NAME}.service" "/etc/systemd/system/${SERVICE_NAME}.service"

# ─────────────────────────────────────────────────────────────────────
# 4b. Apagado automatico de la MAQUINA ([D-045], T-073)
#
# 🔑 Esto no apaga TEAPP: apaga la maquina entera a las 23:00 UTC, que es donde
# cierra la ventana de uso. Sin esto, el apagado depende de que alguien se
# acuerde a las 18:00 hora de Colombia — y asi es como murio [D-041].
#
# 🚨 **Se copia la orden pero NO se arranca.** Al temporizador se le hace
# `enable --now`; a `teapp-shutdown.service` jamas. Un `systemctl start` sobre
# esa orden apaga la maquina AQUI MISMO, a mitad de la instalacion.
# ─────────────────────────────────────────────────────────────────────

echo "==> Apagado automatico (23:00 UTC)"
cp "${DEPLOY_DIR}/${SERVICE_NAME}-shutdown.service" \
	"/etc/systemd/system/${SERVICE_NAME}-shutdown.service"
cp "${DEPLOY_DIR}/${SERVICE_NAME}-shutdown.timer" \
	"/etc/systemd/system/${SERVICE_NAME}-shutdown.timer"

systemctl daemon-reload
systemctl enable --quiet "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

# Solo el temporizador. Repetido aqui porque es la linea que hay que leer dos
# veces antes de tocarla.
systemctl enable --quiet --now "${SERVICE_NAME}-shutdown.timer"

# ─────────────────────────────────────────────────────────────────────
# 5. Caddy delante
# ─────────────────────────────────────────────────────────────────────

echo "==> Configurando Caddy"
sed "s/DOMAIN_PLACEHOLDER/${TEAPP_DOMAIN}/" \
	"${DEPLOY_DIR}/Caddyfile.template" >/etc/caddy/Caddyfile

# Que Caddy valide su propia configuracion ANTES de recargar. Si esta mal, se
# para aqui con el servidor viejo todavia en pie, en vez de dejarlo caido.
caddy validate --config /etc/caddy/Caddyfile
systemctl reload caddy

# ─────────────────────────────────────────────────────────────────────
# 6. Comprobar que de verdad esta arriba
#
# 🔑 PI-4: terminado = visto funcionando. Un guion que acaba sin error no
# demuestra que la app conteste — solo que el guion acabo.
#
# 🚨 **Y `systemctl is-active` NO demuestra que conteste: demuestra que systemd
# lanzo el proceso.** No es un matiz, es un fallo alcanzable y mudo:
#
#     uvicorn arranca → medio segundo despues `require_secret` revienta porque
#     `ubuntu` no puede leer el `.env` → `Restart=always` lo relanza → y
#     `systemctl restart` ya habia vuelto, asi que el `is-active` de la linea
#     siguiente lo ve **`active`** y el guion imprime "Listo".
#
# Una afirmacion que el guion nunca comprobo, sobre una app muerta. Ver [L-017].
# Lo que se arregla no es "faltaba un curl": es que **el mensaje final deje de
# ser una promesa y pase a ser un resultado.**
# ─────────────────────────────────────────────────────────────────────

echo "==> Comprobando que los servicios esten vivos"
systemctl is-active --quiet "${SERVICE_NAME}" ||
	{ echo "[Error] ${SERVICE_NAME} no esta corriendo. Mira: journalctl -u ${SERVICE_NAME} -n 50" >&2; exit 1; }
systemctl is-active --quiet caddy ||
	{ echo "[Error] caddy no esta corriendo. Mira: journalctl -u caddy -n 50" >&2; exit 1; }

# 🚨 **El temporizador tambien se comprueba, y su fallo es el mas mudo de los
# tres.** Si `teapp` o `caddy` no arrancan, la app no contesta y se nota en un
# minuto. Si el temporizador no queda armado NO PASA NADA VISIBLE: la app
# funciona igual, nadie se entera, y la factura corre toda la noche. El unico
# sintoma llegaria semanas despues, en el panel de facturacion.
#
# 🔑 Por eso se imprime la HORA DEL PROXIMO DISPARO y no un "listo". Un
# `is-active` en verde dice que el temporizador existe; la hora dice que
# apuntara donde tiene que apuntar. Es la diferencia de [L-017] otra vez.
systemctl is-active --quiet "${SERVICE_NAME}-shutdown.timer" ||
	{ echo "[Error] El apagado automatico NO quedo armado ([D-045])." >&2
		echo "        La maquina viviria toda la noche cobrando, sin ningun sintoma." >&2
		echo "        Mira: systemctl status ${SERVICE_NAME}-shutdown.timer" >&2; exit 1; }

# 🚨 **Y `is-active` NO basta, aunque el comentario de arriba diga que este es el
# fallo mas mudo de los tres. Hacen falta LAS DOS preguntas.**
#
#   is-active   → ¿esta corriendo AHORA?
#   is-enabled  → ¿va a volver MAÑANA, despues de apagar y encender?
#
# Son estados distintos y hay uno que solo ve la segunda:
#
#   | estado real                 | is-active | is-enabled |
#   |-----------------------------|-----------|------------|
#   | habilitado y activo         | active    | enabled    |  ← el bueno
#   | ni habilitado ni activo     | inactive  | disabled   |  ← lo ven las dos
#   | activo pero NO habilitado   | active    | disabled   |  ← SOLO la segunda
#
# 🔑 **La tercera fila es exactamente el fallo de esta pieza**, y es peor que no
# tener apagado: esta noche apaga puntual, el testigo de `T-074` sale VERDE, y
# al encender pasado manana el temporizador ya no vuelve. El control habria
# certificado justo lo contrario de lo que pasa.
#
# ⚠️ Hoy no muerde, porque la linea del `enable --now` esta unas lineas arriba.
# Este control existe para el dia en que alguien la toque — cambiar `enable
# --now` por `start` deja todo verde y rompe la pieza a partir del siguiente
# encendido.
#
# 📌 Anadido tras una revision externa. Es la MISMA forma de error que el cuarto
# guardian de `tests/test_deploy_shutdown.py` cometio y corrigio el mismo dia:
# un control incapaz de ponerse rojo justo en el modo de fallo que su propio
# comentario declara el mas peligroso. Ver [L-034].
systemctl is-enabled --quiet "${SERVICE_NAME}-shutdown.timer" ||
	{ echo "[Error] El temporizador esta ACTIVO pero NO habilitado ([D-045])." >&2
		echo "        Esta noche apaga; manana, tras encender a mano, ya no vuelve." >&2
		echo "        Arreglo: systemctl enable ${SERVICE_NAME}-shutdown.timer" >&2; exit 1; }

echo "==> Proximo apagado automatico:"
systemctl list-timers --no-pager "${SERVICE_NAME}-shutdown.timer"

# a) ¿La app contesta de verdad? Por dentro, sin pasar por Caddy: asi un fallo
#    aqui senala a uvicorn y no al proxy.
#    Con reintentos porque uvicorn tarda un poco en levantar, y preguntar
#    demasiado pronto daria un rojo falso.
#
#    🚨 **La ruta es `/` a proposito y no es intercambiable.** `/` entrega
#    index.html sin pedir sesion (200). Cualquier ruta con sesion —`/me`, por
#    ejemplo— devolveria 401 aqui, `curl -f` lo tomaria por fallo, y CADA
#    instalacion se pararia en rojo estando todo bien. Comprobado el 2026-08-05.
echo "==> Comprobando que la app conteste"
for intento in $(seq 1 10); do
	if curl -fsS -o /dev/null http://127.0.0.1:8000/; then
		break
	fi
	if [[ "${intento}" -eq 10 ]]; then
		echo "[Error] La app NO contesta en 127.0.0.1:8000 tras 10 intentos." >&2
		echo "        systemd la da por viva, pero no responde. Mira:" >&2
		echo "        journalctl -u ${SERVICE_NAME} -n 50" >&2
		exit 1
	fi
	sleep 2
done

# b) ¿Se llega desde fuera CON certificado? Es lo que de verdad falla el dia
#    real: el DNS sin propagar, el puerto 80 cerrado, o los limites de emision
#    de Let's Encrypt. Y su fallo es mudo: sin certificado la cookie `Secure`
#    no viaja y no entra nadie, con todo lo demas aparentemente bien ([D-029]).
#
#    ⚠️ Este `curl` SI sale a internet, y no rompe [C-001]: aquella regla habla
#    de la suite de tests y del cierre, no de un despliegue a mano. Quitarlo
#    "por coherencia" seria devolver el guion a prometer en vez de comprobar.
#
# 🔑 **Y por que aqui hay MAS margen que en (a), no menos.** En (a) se espera a
#    que arranque un proceso local: segundos. Aqui se espera a que Let's
#    Encrypt emita un certificado de verdad, con una validacion por el puerto
#    80 de por medio. Preguntar una sola vez daria un ROJO por haber mirado
#    demasiado pronto — el mismo fallo de [L-017] con el signo cambiado: un
#    control que no mide lo que promete.
echo "==> Comprobando el HTTPS (Caddy puede tardar en sacar el certificado)"
for intento in $(seq 1 20); do
	if curl -fsS -o /dev/null "https://${TEAPP_DOMAIN}/"; then
		break
	fi
	if [[ "${intento}" -eq 20 ]]; then
		echo "[Error] No se llega por https://${TEAPP_DOMAIN}/ tras 60 segundos." >&2
		echo "        Casi siempre es el certificado. Mira: journalctl -u caddy -n 50" >&2
		echo "        Comprueba tambien que el nombre de DuckDNS apunte a esta IP" >&2
		echo "        y que el puerto 80 este abierto (lo usa Let's Encrypt)." >&2
		echo "        Si el log dice que el certificado SI esta, prueba:" >&2
		echo "          curl -k https://127.0.0.1 -H \"Host: ${TEAPP_DOMAIN}\"" >&2
		echo "        Si eso contesta y lo otro no, es que la maquina no se" >&2
		echo "        alcanza a si misma por su IP publica, no el certificado." >&2
		exit 1
	fi
	sleep 3
done

echo
echo "Comprobado: TEAPP contesta en https://${TEAPP_DOMAIN}"
echo
echo "Todavia NO hay ninguna cuenta: data/ no viaja en Git."
echo "Creala con el servidor PARADO (ver T-064):"
echo "  sudo systemctl stop ${SERVICE_NAME}"
echo "  cd ${INSTALL_DIR} && sudo -u ${APP_USER} TEAPP_NEW_PASSWORD='...' .venv/bin/python create_account.py <nombre>"
echo "  sudo systemctl start ${SERVICE_NAME}"
