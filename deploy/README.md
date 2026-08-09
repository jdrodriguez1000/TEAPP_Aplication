# `deploy/` — cómo se levanta TEAPP en la nube

> 🚨 **Esta carpeta es lo único que sobrevive.** La cuenta de AWS del plan
> gratuito **se va a cerrar** a los 6 meses (`[C-003]`), y con ella la máquina y
> todo lo que se hubiera configurado a mano. `[C-004]` lo dice sin rodeos: lo
> que solo existe porque se hizo clic a clic, está perdido de antemano.
>
> 📌 **La cuenta es desechable. Esto no.**

## Qué hay aquí

| archivo | qué es |
|---|---|
| `console_steps.md` | 🚨 **los clics que no se pueden escribir**, en orden. Incluye la lista de **ESTO NUNCA SE TOCA** |
| `install.sh` | instala todo en una Ubuntu recién creada. No pregunta nada |
| `teapp.service` | el arranque automático, para que la app vuelva sola tras un reinicio |
| `Caddyfile.template` | el servidor de delante: HTTPS y tope de tamaño del cuerpo |
| `teapp-shutdown.service` | 🚨 apaga la **máquina entera** — no la app. La orden, sin hora |
| `teapp-shutdown.timer` | la hora del apagado: **23:00 UTC**, escrita con su zona |

### 🌙 El apagado automático, en dos líneas

`[D-045]` dice que la máquina no vive de noche: ventana **12:00–23:00 UTC**
(07:00–18:00 en Colombia). El apagado es **automático**; el encendido es
**manual, desde la consola de AWS**.

> 🔑 El reparto es asimétrico a propósito: el olvido tiene que caer del lado que
> **no** cobra. Se olvida encender y no pasa nada; se olvida apagar y corre el
> reloj toda la noche.

⚠️ **Apagar no lleva el gasto a cero.** La Elastic IP y el disco cobran igual;
lo único que se ahorra son las horas de instancia. Ver `[D-046]` para por qué es
un temporizador de systemd y no una entrada de `cron`, y `tests/test_deploy_shutdown.py`
para los cuatro fallos mudos que tiene vigilados.

## El orden

1. **Leer `console_steps.md` entero.** Se entra a la consola de AWS a
   **ejecutar** esa lista, no a decidir dentro de ella.
2. Hacer sus pasos 1 a 4 (cuenta + alarma, DuckDNS, máquina, cortafuegos).
3. Copiar el repo a `/opt/teapp` en la máquina.
4. Correr el instalador:

   ```bash
   sudo TEAPP_DOMAIN=teapp.duckdns.org bash deploy/install.sh
   ```

5. Crear la primera cuenta — el instalador imprime cómo. ⚠️ Con el servidor
   **parado**: el script y el servidor a la vez son dos procesos escribiendo
   `data/`, y el candado no los ve (`[A-002]`).

## El dibujo

```
   internet ──HTTPS(443)──►  Caddy  ──HTTP──►  uvicorn (127.0.0.1:8000)
                               │                    │
                          certificado          TEAPP (FastAPI)
                          de Let's Encrypt          │
                                                  data/
```

🔑 **Dos servidores y no uno, por una razón concreta:** uvicorn sabe contestar
peticiones pero no sabe de certificados. Caddy sí, y los saca y renueva solo.

## El instalador comprueba, no anuncia

Al final, `install.sh` hace **tres** comprobaciones, y son tres cosas distintas:

| qué mira | qué demuestra |
|---|---|
| `systemctl is-active` | que systemd **lanzó** el proceso |
| `curl` a `127.0.0.1:8000` | que **la app contesta** |
| `curl` a `https://<dominio>` | que **se llega desde fuera, con certificado** |

🚨 **La primera sola no basta, y por poco se quedó sola.** Si uvicorn arranca y
revienta medio segundo después —un `.env` que no puede leer—, `Restart=always`
lo relanza y `is-active` lo ve `active`. El guion habría dicho "Listo" sobre una
app muerta. Ver `[L-017]`.

⚠️ **El último `curl` sale a internet, y está bien que salga.** `[C-001]` habla
de la suite de tests y del cierre, no de un despliegue a mano. **No lo quites
"por coherencia"**: sin él, el mensaje final vuelve a ser una promesa en vez de
un resultado.

## Lo que hay que mirar cuando algo falle

```bash
sudo systemctl status teapp        # ¿está viva?
sudo journalctl -u teapp -f        # el log de TEAPP, en directo
sudo journalctl -u caddy -n 50     # el log de Caddy (certificados)
```

## Ensayo sin nube — el contenedor, y hasta dónde llega

**La receta, que es lo único irrecuperable.** El contenedor es desechable; esto no:

```bash
docker run -d --name teapp-test ubuntu:24.04 sleep infinity
docker exec teapp-test sh -c 'comando aqui dentro'
```

Sin puertos publicados y sin volúmenes: **todo entra por `docker exec`**.

🚨 **Un contenedor que YA corrió `install.sh` no sirve para volver a probarlo.**
El estado ya existe: el `.venv`, el `.env`, los paquetes. Una segunda corrida daría
verde **porque las cosas ya estaban**, no porque el guion las haga. Es un
instrumento trucado, y el verde que devuelve no significa nada — el mismo bicho que
costó `T-072`. **Para probar una instalación limpia hay que crear uno nuevo**, y
para eso está la receta de arriba.

⚠️ **La trampa de Git Bash en Windows, que falla MUDA.** Git Bash convierte las
rutas absolutas: `docker exec teapp-test ls /opt/teapp` se le entrega a Linux como
`C:/Program Files/Git/opt/teapp`, y no hay mensaje que lo explique. **La defensa es
la de la receta:** meter el comando dentro de `sh -c '...'`, donde la ruta viaja
como texto y nadie la toca.

### 🚨 `install.sh` NO llega al final en un contenedor. Muere en la línea 223

**Ya estaba medido en `[L-024]`; aquí queda a la vista de quien despliega**, que es
donde hace falta. Corre hasta la 222 —copia `teapp.service`, archivo presente con
su fecha— y muere en la siguiente:

```
systemctl daemon-reload   ->  sh: 1: systemctl: not found
PID 1 del contenedor      ->  sleep
```

Un contenedor normal no tiene systemd. 🔑 **Consecuencia: todo lo que hay después
de la 223 no se ha ejecutado NUNCA, ni aquí ni en EC2** — porque EC2 todavía no
existe. Eso incluye la sección 5 entera (Caddy) y las comprobaciones finales.

**Lo que sí queda medido de verdad** (ocurre antes de la 223): la `SECRET_KEY` que
no se pisa entre corridas, el `.env` que respeta el valor preexistente, y
`TEAPP_DATA_DIR`.

📌 **Y por eso Caddy y uvicorn de `teapp-test` NO se hablan:** los levantó a mano la
sesión que midió el tope de 16 KB. El `/etc/caddy/Caddyfile` de ahí dentro es **el
de fábrica**, con `reverse_proxy` comentado. No es un aparejo, son dos procesos
sueltos. ⚠️ **El aparejo de verdad es otro y se monta aparte** — ver abajo.

### 🔧 El aparejo de DOS contenedores, y por qué no vale con uno

**La receta, que es lo irrecuperable.** Los contenedores son desechables:

```bash
docker run -d --name teapp-proxy  teapp-rig sleep infinity   # Caddy + uvicorn
docker run -d --name teapp-client teapp-rig sleep infinity   # solo curl
docker inspect -f '{{.Name}} {{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' \
	teapp-proxy teapp-client
```

🚨 **Un solo contenedor no sirve para medir `X-Forwarded-For`.** Si el cliente y el
proxy comparten dirección, la cabecera diría `127.0.0.1` — y ese valor **no
distingue** "Caddy escribió la dirección real" de "Caddy se la inventó". Es
`[L-019]` otra vez: el montaje mediría lo contrario de lo que dice medir. Con dos
contenedores el cliente es `172.17.0.4` y el proxy `172.17.0.3`, y el número
delata de dónde salió.

⚠️ **El backend de la medida se ata a `0.0.0.0`, al revés que en producción, y es
a propósito:** si se atara a `127.0.0.1` el control no se podría hacer, porque el
cliente no podría hablarle **sin** Caddy y no habría con qué comparar.

### ✅ Caddy SÍ escribe la cabecera — medido el 2026-08-07

Renderizando la **plantilla versionada** con el mismo `sed` de `install.sh`
(`DOMAIN_PLACEHOLDER` → `:80`). Lo que le llega al backend:

| corrida | cliente manda | llega `X-Forwarded-For` |
|---|---|---|
| **control** — directo al 8000, sin Caddy | nada | *(no llega la cabecera)* |
| **control del montaje** — directo + forja | `9.9.9.9` | `9.9.9.9`, intacta |
| **medida** — por Caddy | nada | **`172.17.0.4`** ← la real |
| **forja** — por Caddy | `9.9.9.9` | **`172.17.0.4`** ← la falsa desaparece |
| **forja doble** — por Caddy | `9.9.9.9, 8.8.8.8` | **`172.17.0.4`** ← las dos |

🔑 **Caddy no añade a la cabecera falsa: la reescribe.** Y no es casualidad de
versión — es política documentada: *"By default, no proxies are trusted"*. Como el
`Caddyfile` **no** declara `trusted_proxies`, lo que traiga el cliente es no
confiable y se descarta. 🚨 **Si algún día alguien añade `trusted_proxies` a la
plantilla, esta garantía se cae** — y el síntoma sería silencioso: la app sigue
contestando 200 y el freno de `/login` deja de frenar.
✅ **Ya no depende de que alguien se acuerde:** lo vigila
`tests/test_deploy_limits.py`, y el guardián se vio **rojo sobre esta plantilla
de verdad** antes de darlo por bueno, no solo sobre archivos de mentira.

**Y la cadena entera, con TEAPP de verdad detrás:** seis logins fallidos, cada uno
haciéndose pasar por una dirección distinta (`10.0.0.1` … `10.0.0.6`). Si la forja
funcionara, cada intento caería en un cubo distinto y el freno **no saltaría
nunca**. Saltó en el sexto, y el log escribió:

```
Demasiados intentos: el origen 172.17.0.4 lleva 5 de 5 (faltan 900 s)
```

| uvicorn arrancado con | origen en el log |
|---|---|
| `--proxy-headers --forwarded-allow-ips 127.0.0.1` (lo de `teapp.service`) | **`172.17.0.4`** — la real ✅ |
| sin banderas | `172.17.0.4` — ⚠️ **control CIEGO**: en uvicorn 0.52.1 ya vienen por defecto |
| `--forwarded-allow-ips 203.0.113.5` | **`127.0.0.1`** — 🔴 el fallo de `[A-014]`, todos en el mismo cubo |

⚠️ **Lo que esto NO mide, y estaba escrito antes de medir:** ese Caddy sirve por
**HTTP**, así que `X-Forwarded-Proto` dice `http`, no `https`. Queda medido el
**mecanismo**, no el valor final. El propio Caddy lo avisa al validar: *"server is
listening only on the HTTP port, so no automatic HTTPS will be applied"*.
📌 Siguen necesitando máquina: el HTTPS real (`T-061`), el 8000 cerrado desde
fuera (`T-060b`) y los dos dispositivos de `T-066`.

### ✅ `Caddyfile.template` validado — primera vez, 2026-08-07

La línea 237 (`caddy validate`) vive detrás de la que muere, así que nunca había
corrido. Se ejecutó a mano, con el mismo `sed` de la 232:

```
Valid configuration          (salida 0)
DOMAIN_PLACEHOLDER           ninguno sin sustituir
```

Directivas efectivas, quitados los comentarios:

```
teapp.duckdns.org {
        request_body { max_size 16KB }
        reverse_proxy 127.0.0.1:8000
}
```

Y el propio validador confirmó por su cuenta lo que la plantilla promete:
*"enabling automatic HTTP->HTTPS redirects"* y el puerto 443 con política TLS.

⚠️ **Esto mide la SINTAXIS, no el comportamiento.** Que la configuración sea válida
no dice que Caddy escriba `X-Forwarded-For`, ni que el 413 llegue: eso sigue siendo
`T-055` y `T-060b`, y sigue necesitando la máquina.

## Lo que todavía no está probado

⚠️ **Casi nada de esta carpeta se ha corrido entero** — no hay máquina. Lo que sí
está medido, y lo que no, está arriba. Hasta `T-069`, **"está todo escrito" es una
afirmación sin medir** (`[D-030]`).

`T-069` es la prueba, y va **pronto, no al final**: con TEAPP arriba y
funcionando, borrar la máquina y levantarla otra vez **solo desde aquí**. Cuesta
céntimos y deja meses de margen para arreglar lo que falte.
