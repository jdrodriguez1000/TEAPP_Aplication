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
# todo el mundo de golpe, sin decir por que ([A-008]).
# ─────────────────────────────────────────────────────────────────────

ENV_FILE="${INSTALL_DIR}/.env"

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
systemctl daemon-reload
systemctl enable --quiet "${SERVICE_NAME}"
systemctl restart "${SERVICE_NAME}"

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
