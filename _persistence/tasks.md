# Tareas — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [T-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

Estados: 🔲 pendiente · 🔄 a medias · ✅ hecha · ❌ descartada

| id | tarea | estado | paso |
|---|---|---|---|
| T-001 | Inicializar repo y conectarlo al remoto de GitHub | ✅ | 0 |
| T-002 | Llenar `.gitignore`, `.env.example`, `README.md`, `CLAUDE.md` | ✅ | 0 |
| T-003 | Llenar los tres archivos de `_context/` | ✅ | 0 |
| T-004 | Llenar los seis archivos de `_persistence/` con formato índice + entradas | ✅ | 0 |
| T-005 | Crear agentes `session-starter` y `session-closer` con sus skills | ✅ | 0 |
| T-006 | Corregir incoherencia: `protocol-close` (descripción vs. Paso 5) dice que actualiza `decisions/assumptions/constraints/lessons`, pero el Paso 5 dice que solo los revisa | ✅ | 0 |
| T-007 | Añadir a los límites de `session-closer` que los cuatro archivos de porqué no son suyos para escribir | ✅ | 0 |
| T-008 | Revisar que el Paso 7 (reporte) de `protocol-close` deje explícito el resultado de revisar los cuatro archivos | ✅ | 0 |
| T-009 | Actualizar descripciones de `session-starter` / `protocol-start` para que mencionen que también leen `git` | ✅ | 0 |
| T-010 | Crear `app/tools.py`: `count_words`, `judge_grammar` (falsa), `read_score`, `add_point` | ✅ | 1 |
| T-011 | Crear `app/english_tutor.py` con `respond(sentence) -> str` | ✅ | 1 |
| T-012 | Crear `main.py`, la terminal (único archivo con `input()`) | ✅ | 1 |
| T-013 | Escribir tests: `tests/test_tools.py`, `tests/test_english_tutor.py`, `conftest.py` — 14 pasando | ✅ | 1 |
| T-014 | Correr la app en terminal y verificar que el marcador persiste entre ejecuciones | ✅ | 1 |
| T-015 | Crear entorno virtual `.venv/` y `requirements.txt` con `pytest==9.1.1` fijado | ✅ | 1 |
| T-016 | Completar en `README.md` las secciones "Cómo se corre", estado y estructura | ✅ | 1 |
| T-017 | Arreglar `read_score`/`add_point`: distinguir marcador ausente (0) de roto (`ScoreFileError`), sin sobrescribir el archivo roto | ✅ | 1 |
| T-018 | Arreglar `count_words`: lanzar `TypeError` si no recibe un `str`, en vez de reventar con `AttributeError` | ✅ | 1 |
| T-019 | Decidir si el marcador cuenta frases practicadas o correctas (ver `assumptions.md` A-001). 📌 **Deja de estar bloqueada el 2026-08-10 (`[D-048]`):** con el veredicto real de `T-076` el contrato de `judge_grammar` cambia de verdad — es el momento en que esta decisión deja de ser prematura y pasa a tocar | 🔲 | 8 |
| T-020 | Hacer atómica la escritura de `add_point`: escribir al lado y renombrar encima (ver `decisions.md` D-007) | ✅ | 2 |
| T-021 | Arreglar que dos peticiones a la vez revienten con `PermissionError`: un temporal con nombre propio por escritura (D-009) | ✅ | 2 |
| T-022 | Arreglar que dos peticiones a la vez pierdan puntos y repitan el marcador: candado sobre lectura + escritura (D-009) | ✅ | 2 |
| T-023 | Registrar que el candado solo vale con un proceso de uvicorn (`assumptions.md` A-002) y anotarlo en `README.md` | ✅ | 2 |
| T-024 | Dejar de devolver la ruta del servidor en el 500, y que un fallo inesperado no salga mudo (D-010) | ✅ | 2 |
| T-025 | Levantar uvicorn a mano y ver la ruta contestar: `/docs`, una frase, un 422 y el 500 sin ruta | ✅ | 2 |
| T-026 | Poner el `README.md` al día con el paso 2: uvicorn, `/docs`, `app/api.py`, y arrancar sin `--workers` | ✅ | 2 |
| T-027 | Poner `tasks.md` al día con las tareas del paso 2 | ✅ | 2 |
| T-028 | Afinar `test_the_reply_cannot_be_modified`: esperar `FrozenInstanceError`, no `Exception` | ✅ | 2 |
| T-029 | Configurar CORS: la pantalla se abrirá desde otro origen y el navegador bloqueará la llamada | ❌ descartada | 3 |
| T-030 | Crear `index.html` y `app.ts` contra la ruta `/practice` local | ✅ | 3 |
| T-031 | Cambiar `respond` para que devuelva `TutorReply` —tres piezas sueltas— en vez de un texto cocinado (D-008) | ✅ | 2 |
| T-032 | Crear `app/api.py` con FastAPI: `POST /practice`, validación del cuerpo y `requirements.txt` al día | ✅ | 2 |
| T-033 | Configurar el log (hora, nivel y origen). Hecho en `config.configure_logging()`, con `INFO` por defecto y `TEAPP_LOG_LEVEL` para bajarlo. Con él, la cuota agotada y el registro cerrado vuelven a `info`; los intentos fallidos se quedan en `warning` (`D-028`). Medido con uvicorn: el renglón de `L-012` ya sale | ✅ | 7 |
| T-034 | Ampliar `A-002` y el `README.md`: el candado también se rompe con `main.py` y el servidor a la vez, no solo con `--workers` | ✅ | 2 |
| T-035 | Servir la pantalla desde FastAPI: `StaticFiles` en `/static`, `GET /` con `index.html` | ✅ | 3 |
| T-036 | Compilar `frontend/app.ts` a `app/static/app.js` con `tsc`, versionado en Git | ✅ | 3 |
| T-037 | Comprobar que `app/static/*.js` está **al día**, no solo que existe. Resuelta en el cierre, no en `pytest` ([D-017]): Paso 5b de `protocol-close`. El test se renombró a `test_the_script_is_served` y su comentario ya dice qué **no** mide | ✅ | 3 |
| T-038 | Tope de peticiones por persona en el **servidor**. El `sendButton.disabled` de `app.ts` solo frena clics en el navegador: diez peticiones mandadas a mano siguen sumando diez puntos | ✅ | 6 |
| T-039 | Crear `app/tools.py`: `normalize_user`, `InvalidUserError`, `score_file`; `read_score`/`add_point` reciben el nombre de la persona | ✅ | 4 |
| T-040 | Cambiar `respond(sentence, user)` sin valor por defecto; `main.py` pide el nombre una vez al arrancar | ✅ | 4 |
| T-041 | `app/api.py`: `PracticeRequest` gana `user`, validado primero y traducido a 422 | ✅ | 4 |
| T-042 | `frontend/app.ts` + `index.html`: casilla "Your name" recordada en `localStorage`; recompilar a `app/static/app.js` | ✅ | 4 |
| T-043 | Borrar `data/score.json`, el marcador global que dejó el paso 3 (`D-015`) | ✅ | 4 |
| T-044 | Tests del paso 4: recorrido de ruta, nombres reservados de Windows, normalización, memoria por persona, concurrencia entre dos personas — de 57 a 121 pasando | ✅ | 4 |
| T-045 | Quitar la casilla "Your name" de la pantalla en el paso 5, sustituyéndola por identidad de verdad, no añadiéndole nada al lado (`D-013`) | ✅ | 5 |
| T-046 | Comprobar `[A-006]` en otra máquina: que la ruta de `mktemp -d` le sirva a `node`. Si falla, el Paso 5b cae siempre en "SIN COMPROBAR" y el arreglo es `cygpath -w` | 🔲 | 7 |
| T-047 | Comprobar `[C-001]` de verdad. **Medida y se cumple:** 192 tests verdes con la red cortada, y los 5 controles del portero verdes. El motivo real es más fuerte que el verde: en `app/` y `tests/` hay **cero** `requests`/`httpx`/`urllib`/`socket`/`aiohttp`/`subprocess` — los tests usan `TestClient`, que llama la app en el mismo proceso sin abrir un socket. No pasaron porque el portero los dejara pasar: pasaron porque **no había nada que interceptar**. El portero (`D-022`) es el vigía de que siga siendo así mañana. La redacción de `C-001` se corrigió al medirla: el `git push` del cierre la contradecía | ✅ | 6 |
| T-049 | `protocol-close` escribía `tasks.md` (Paso 4) **antes** de correr el Paso 5b y el push (Pasos 5b y 6b). Resuelta: el control del `.js` sube al Paso 2b (antes de escribir `tasks.md`), y el resultado del push queda escrito como imposibilidad lógica, no como pendiente (`D-019`) | ✅ | 5 |
| T-048 | Correr el Paso 5b de punta a punta en un cierre real, con el `session-closer` haciéndolo. Estrenado en el cierre del 2026-08-03 (commit `6af7597`): `compilar: 0`, `comparar: 0`, y la línea salió en el reporte | ✅ | 5 |
| T-050 | Que `TEAPP_SECRET_KEY` exista en la nube y sea **estable entre despliegues**: si cambia, todas las sesiones mueren de golpe sin ningún error que lo explique (`[L-032]`, antes `A-008`). Con `D-029` ya tiene dueño: un archivo de entorno en la máquina, con permisos cerrados, generado **una sola vez**. ✅ **CERRADA el 2026-08-09:** redespliegue real sobre la máquina viva — `git pull` `aff4350`→`0dfdbba`, `install.sh` código 0. Huella del `.env` idéntica antes/después (`1f0365563d…`), `data/users/jorge.json` con fecha 2026-08-08 18:25:15 y `{"score": 5}` intacto, servicios `active`, 200 en local, y la sesión del navegador sobrevivió al F5. Ver entrada | ✅ | 7 |
| T-051 | Poner `TEAPP_COOKIE_SECURE=true` en la nube. En local va en `false` porque el navegador descarta en silencio una cookie `Secure` sobre `http://localhost`. Con `D-029` es **una línea** en el mismo archivo de entorno: toda su dificultad era el certificado, y la resuelve Caddy con el nombre de DuckDNS (`T-058`). ✅ **CERRADA el 2026-08-09:** cookie `Secure` medida en NAVEGADOR REAL sobre `https://teapp.duckdns.org` — `Secure ✓`, `HttpOnly ✓`, `SameSite Lax`, y F5 sin recredenciales → "Signed in as jorge". Con eso muere también `[L-031]` (antes `A-009`): las dos mitades del contrato, guardar y devolver | ✅ | 7 |
| T-052 | Escribir un test que anule el `autouse` de `tests/conftest.py` y compruebe que la cookie sale con `Secure`: la rama por defecto no corría en ningún test (`[L-031]`, antes `A-009`). ✅ Hecha el 2026-08-06 — **cuatro** tests en `tests/test_api.py` ("El interruptor de la cookie segura"). 📌 Dos ajustes sobre el enunciado: el fixture **borra** la variable en vez de ponerla a `"true"`, para medir el defecto de verdad y no una copia nuestra; y se mira la cabecera `Set-Cookie` **en crudo**, no el tarro del cliente, que descarta la cookie con razón al hablar por `http://`. Los dos sitios cubiertos: `_start_session` (registro y login) y el `delete_cookie` de `/logout`. Sabotaje doble hecho (`L-019`): resultado **y** montaje | ✅ | 7 |
| T-053 | Tope de intentos fallidos contra `/login`, contado por origen de la petición, no por persona. Hecho en `app/login_guard.py`: contador en memoria con barrido, 429 con `Retry-After` y motivo al log. Visto con uvicorn real (`D-026`) | ✅ | 7 |
| T-054 | Tope de tamaño de cuerpo en el servidor de delante (el reverse proxy de la nube). `MAX_SENTENCE_LENGTH` frena el gasto, no la subida: un cuerpo de 5 MB se sube entero antes del 422 (`C-002`). ✅ Hecha el 2026-08-06 en su mitad medible: `deploy/Caddyfile.template` ya tenía `max_size 16KB` desde `T-063`, y la báscula que faltaba quedó hecha — 500 caracteres en cinco alfabetos, peor caso legítimo 6016 bytes, contra un techo real de 16000 (`[D-035]`, `tests/test_deploy_limits.py`). ✅ **Salvedad retirada el 2026-08-07:** Caddy 2.11.4 medido de verdad en contenedor — `caddy adapt` → `16000` (control `16KiB` → `16384`) y el borde HTTP exacto (16000 pasa, 16001 → 413). Con eso muere `[A-019]` y `T-054` queda cerrada sin deuda pendiente | ✅ | 7 |
| T-055 | Que el origen que lee `_request_origin` sea el REAL cuando haya un proxy delante. Hoy es `request.client.host`; tras el despliegue será la dirección del proxy y el freno de `/login` dejaría fuera a todo el mundo a la vez (`A-014`). ⚠️ Leer `X-Forwarded-For` **sin** proxy de confianza delante es peor que no tener freno: la cabecera la escribe cualquiera. 🔑 **La garantía NO viene de que el proxy sea nuestro: viene de que nadie más pueda hablar con FastAPI.** ✅ **La mitad de Python, hecha el 2026-08-06 (`D-034`): no hizo falta tocar `app/api.py`** — uvicorn ya lo resuelve con `--proxy-headers` y `--forwarded-allow-ips`, medido con servidor real. ⚠️ **Faltan las dos mitades que NO son código:** que Caddy escriba de verdad la cabecera, y `T-060`. Se cierra del todo con `T-066`. Ver entrada | ✅ | 7 |
| T-056 | Decidir y poner `TEAPP_REGISTRATION_OPEN` en la nube. Por defecto vale `false`, que es lo que se quiere (`D-027`), pero **conviene ponerlo explícito**: un ajuste de seguridad que depende de que nadie lo escriba es un ajuste que alguien abre 'un momentito'. Y comprobar que `create_account.py` corre en la plataforma: sin él no hay forma de crear la primera cuenta allí — ver `T-064`. 📌 **Es lo primero que toca del paso 8 (`[D-048]`):** de todo el paso 7 abierto, era lo único que de verdad bloqueaba cruzar — dos minutos. ✅ **CERRADA el 2026-08-10 (según traspaso, sin rastro en `git diff`):** las dos mitades verificadas por SSH en la máquina real — `TEAPP_REGISTRATION_OPEN = false` explícito en `/opt/teapp/.env` (permisos 600, dueño `ubuntu`), y `create_account.py` corriendo en el servidor (sin argumentos, mensaje de uso, código de salida 1 — correcto). Ver entrada | ✅ | 7 |
| T-057 | **Abrir la cuenta de AWS, y la alarma de facturación como PRIMER clic.** Hecha el 2026-08-06: cuenta abierta, MFA en el root activado en el mismo acto, alarma de 1 USD con umbral al 1% creada y correo verificado. Fin del plan gratuito leído en la portada: **2027-02-06** (`C-006`). ⚠️ Desviación de `D-031`: se usó el correo personal SIN el alias `+aws` — impacto nulo, anotado en `D-031`. El camino de vuelta del MFA quedó resuelto y probado (Contraseñas de Apple / Llavero de iCloud, verificado en un segundo dispositivo) | ✅ | 7 |
| T-058 | Sacar un nombre gratuito en DuckDNS (`teapp.duckdns.org`). 🚨 **Sin él no hay HTTPS**: Let's Encrypt se niega por política a emitir para `compute.amazonaws.com`, y sin certificado la cookie de sesión no viaja y no entra nadie (`D-029`). Hecha: el subdominio existe y el token quedó guardado fuera del repo — coincide con el nombre que ya esperaban `deploy/install.sh`, `deploy/Caddyfile.template` y `deploy/console_steps.md`, así que no hubo que tocar `deploy/` | ✅ | 7 |
| T-059 | Lanzar la instancia EC2 **pequeña** (`t3.micro`) con una **IP fija** (Elastic IP) asociada, y apuntar el nombre de DuckDNS a esa IP. La IP de una EC2 cambia al apagar y encender; si el nombre deja de resolver, se cae el HTTPS y con él la sesión. ⚠️ El tamaño de la máquina es decisión de presupuesto, no técnica (`C-003`). Ver entrada | ✅ | 7 |
| T-060a | Cortafuegos, **la mitad ESCRITA**: el grupo de seguridad existe y sus reglas dicen 80 y 443, nada más. Se crea suelto, sin instancia, y es gratis. 🚨 **Ya no es "un clic de la consola": desde `D-034` es la mitad que SOSTIENE a la otra.** `--forwarded-allow-ips 127.0.0.1` solo vale mientras nadie pueda hablarle a uvicorn desde fuera; con el 8000 abierto, quien quiera se salta Caddy entero —sin HTTPS y sin tope de cuerpo— y la mitad de Python de `T-055` no protege de nada. Las dos capas o ninguna. ⚠️ **Antes del primer clic se lee `T-068`** (siete puertas): fue el primer clic en la consola desde que se abrió la cuenta, y esa lista es el único freno que corre a la velocidad del acantilado. ✅ **HECHA el 2026-08-07**, en `us-east-1` (`[D-033]`) y en la VPC `default` —única ofrecida, así que no había decisión que tomar—. **Leído desde la ficha, no desde lo tecleado** (`LM.15`): `80/tcp` y `443/tcp` desde `0.0.0.0/0`, `22/tcp` desde **una sola dirección (`/32`)**, **sin 8000 y sin IPv6**; el grupo existe en la lista con su `sg-`. Salida intacta. 📌 Falló el primer intento por el **apóstrofo de `Let's`** en una descripción de regla — AWS **deshizo el grupo entero**, no dejó uno a medias; el conjunto de caracteres permitido y los textos ya limpios quedaron en `deploy/console_steps.md` | ✅ | 7 |
| T-060b | Cortafuegos, **la mitad MEDIDA**: un escaneo **desde fuera** enseña el 8000 cerrado, con la máquina viva. ✅ **HECHA el 2026-08-08 (según traspaso, sin rastro en `git diff`):** con `python` escuchando de verdad en el 8000, la petición desde fuera dio **timeout**. 🔑 **Se parte de `T-060a` por `LM.13`: tener el grupo creado NO es tener el cortafuegos, es tenerlo escrito.** Ya no es el control ciego de `[L-020]` — había algo real que morder | ✅ | 7 |
| T-061 | Instalar y configurar **Caddy**: HTTPS automático contra el nombre de `T-058`, proxy hacia `127.0.0.1`, y el tope de cuerpo de `T-054`. Se eligió Caddy sobre nginx porque saca y renueva el certificado solo, y `T-051` lo necesita sí o sí (`D-029`). ✅ **HECHA el 2026-08-08 (según traspaso, sin rastro en `git diff`):** `200` con `ssl_verify_result=0` desde fuera, puerto 80 redirige `308`. Certificado Let's Encrypt real, `CN=teapp.duckdns.org`, válido `Aug 8 16:55:35` → `Nov 6 16:55:34 2026` | ✅ | 7 |
| T-062 | Arranque automático de uvicorn en la máquina, **atado a `127.0.0.1`** y leyendo el archivo de entorno. Que sobreviva a un reinicio sin que nadie entre a encenderlo a mano. ✅ **HECHA el 2026-08-08 (según traspaso, sin rastro en `git diff`):** reinicio real verificado con `uptime -s` (`15:54:27` → `18:11:15`); `teapp` y `caddy` en `active` sin que nadie los encendiera; uvicorn escuchando SOLO en `127.0.0.1:8000` | ✅ | 7 |
| T-063 | Carpeta `deploy/` en el repo: guion de instalación, configuración de Caddy y arranque automático. Más un documento con **los clics que no se pueden escribir**, en orden. Lo exige `C-004`: la cuenta se va a cerrar, y lo que solo exista porque se hizo a mano se pierde. ⚠️ **Sin Terraform** — sería la sexta cosa nueva, PI-2. Hecha: `deploy/console_steps.md`, `install.sh`, `teapp.service`, `Caddyfile.template`, `README.md`. Revisada dos veces el 2026-08-05: `install.sh` pasó de un solo `is-active` a tres comprobaciones (`L-017`), y `console_steps.md` ganó la comprobación real de DuckDNS (`A-017`). ⚠️ **Nada de esto se ha corrido nunca** — no hay máquina; `bash -n install.sh` sin errores es lo único verificado | ✅ | 7 |
| T-064 | Subir TEAPP y crear la primera cuenta con `create_account.py` en la máquina. `data/` no va a Git, así que arranca **sin ninguna cuenta**. ⚠️ Con el servidor **parado**: el script y el servidor a la vez son dos procesos escribiendo `data/`, y el candado no los ve (`A-002`). ✅ **HECHA el 2026-08-08 (según traspaso, sin rastro en `git diff`):** cuenta `jorge` creada con `systemctl stop teapp`, contraseña generada en la máquina con `openssl rand`, nunca escrita en el repo ni pasada por argumento. Verificado desde fuera: `/login` → 200, `/me` con cookie → `{"user":"jorge"}`, sin cookie → 401, contraseña mala → 401 | ✅ | 7 |
| T-065 | Comprobar `A-005` de verdad: sumar puntos, **reiniciar la máquina**, y mirar el marcador. Elegir un disco que persiste no es medirlo — hasta esta corrida es una promesa de la documentación. ✅ **HECHA el 2026-08-08:** marcador de `jorge` a 3 puntos, `reboot`, siguiente frase devolvió `score = 4`. ⚠️ Mide el **reinicio**, no el **redespliegue** — el redespliegue se cerró el 09 con `T-050`, ver `[L-032]` (antes `[A-005]`) | ✅ | 7 |
| T-066 | Comprobar `A-014` resuelto: entrar desde dos dispositivos distintos y mirar qué dirección escribe el log en `Demasiados intentos`. Si es la misma para los dos, `T-055` no quedó hecha. ✅ **CERRADA el 2026-08-10** — medida en el servidor real desde computador (`181.58.39.253`) y celular por datos móviles (`191.153.227.163`), coincidiendo cada una con su `ipify`; y la mitad de la cabecera forjada (`X-Forwarded-For`/`X-Real-IP: 9.9.9.9`) descartada con el cubo ya agotado — cuatro `429`, las cuatro registradas como `181.58.39.253`. `[A-014]` retirada de `assumptions.md`, vive en `[L-036]` | ✅ | 7 |
| T-067 | Comprobar `A-015` con el panel de facturación a los pocos días: gasto diario real × 180 contra los $200. 🔁 **Reescrita el 2026-08-09 por `[D-045]`:** se mide **bajo la ventana de uso** (12:00–23:00 UTC, máquina apagada de noche), no con la EC2 encendida 24 h — proyectar 180 días desde un régimen que no existe daría un número falso. Y separa **tres tarifas, no dos** (corrección de la sexta lectura de `[A-018]`): Elastic IP, horas de instancia `t3.micro`, y volumen EBS — solo la segunda se apaga de noche. Si no cabe, la ventana ya está puesta; lo que faltaría es acortarla más | 🔲 | 7 |
| T-073 | Escribir la pieza de apagado automático **desde dentro de la máquina** que exige `[D-045]`. ✅ **HECHA el 2026-08-09:** `deploy/teapp-shutdown.service`/`.timer` (systemd, `[D-046]`), instalados por `install.sh` sección 4b. Desplegada y medida en la máquina real (17:37–17:50 UTC): `install.sh` código 0, temporizador armado (`Sun 2026-08-09 23:00:00 UTC`), disparo único viejo desarmado, `list-timers` confirmando. 🔧 **Ampliada el mismo día tras revisión externa:** `install.sh` solo comprobaba `is-active`, que no ve el estado "activo pero no habilitado" — el mismo modo de fallo que `T-074` no mide. Se añadió `is-enabled` al lado, más un quinto guardián en `tests/test_deploy_shutdown.py`. De 351 a **362** tests. Ver entrada de `[L-034]` | ✅ | 7 |
| T-074 | Mirar el temporizador de `T-073` disparar de verdad: la instancia pasa a `stopped` en la consola de AWS, con la hora exacta anotada. `T-065` cubrió el **reinicio** (`reboot`), que no es lo mismo — apagar y encender es otra prueba, y es la única parte de la pieza que es comportamiento, no configuración. ✅ **CERRADA el 2026-08-10, con testigo directo, no por descarte:** el testigo recomendado primero (`systemctl list-timers`) salió ciego a propósito —`Persistent=false` no lleva libreta de disparos, `[L-035]`—; el testigo real es el journal, que sobrevive al reinicio: `Aug 09 23:00:00 Starting teapp-shutdown.service … ([D-045])` seguido en el mismo segundo de `systemd-logind: The system will power off now!` | ✅ | 7 |
| T-068 | Lista de **"ESTO NUNCA SE TOCA"** en el documento de clics de `deploy/`, con los nombres escritos. 🚨 Cruzan al plan de pago **sin pedir confirmación** y **no tienen vuelta atrás** (`C-005`). No son botones que se vayan a necesitar: son botones con los que uno **se cruza**. Hecha en dos mitades: `A-016` se cerró leyendo tres fuentes de AWS (FAQ, Términos, facturación) — la lista de tres estaba INCOMPLETA, son **siete** puertas, no tres (`L-016`); y la lista de siete quedó escrita en `deploy/console_steps.md`, con las cinco desconocidas marcadas ❓ y tratadas como si evaporaran (denegar por defecto) | ✅ | 7 |
| T-069 | 🚨 **Ensayo de reconstrucción.** Con TEAPP arriba y funcionando: borrar la máquina y levantarla otra vez **solo desde `deploy/`**. Es la única corrida que demuestra `C-004`; hasta entonces "está todo escrito" es una afirmación sin medir (`D-030`). Cuesta céntimos y deja margen para arreglar lo que falte. 🔄 **A MEDIAS el 2026-08-10:** la mitad de `[A-022]` que se puede medir sin reconstruir ya está hecha en la máquina viva — `systemd 255 (255.4-1ubuntu8.16)` responde `Normalized form: *-*-* 23:00:00 UTC`. Falta la mitad que da nombre a la tarea: correr el ensayo sobre una **imagen nueva** y medir el suelo de versión de systemd que entiende la zona. Guion ya escrito, Paso 5c de `deploy/console_steps.md` (`[D-047]`, aún válida). ⏸️ **APLAZADA el mismo día por `[D-048]`, no cancelada: no está "en marcha", está a la espera de fecha.** Se aplaza a propósito hasta después del paso 8, con dueño de calendario — fecha tope ≈ 2026-09-01 (`[A-023]`, cierre del primer ciclo de facturación). El precio de esperar está escrito ahí, no aquí: el paso 8 va a tocar `deploy/` (la llave entra por el archivo de entorno), así que lo que se ensaye en septiembre no será exactamente el `deploy/` de hoy | 🔄 | 7 |
| T-070 | **Cierre planeado del paso 7:** bajar TEAPP con fecha en el calendario, antes de que AWS cierre la cuenta sola, verificando otra vez que `deploy/` lo levanta. Cuesta lo mismo que no hacer nada — 🔑 la diferencia es que **un cierre planeado se aprende y uno automático solo se sufre** (`D-030`). 📌 La cuenta es desechable; `deploy/` no | 🔲 | 7 |
| T-071 | El aislamiento de datos vive en un `fixture` local, no en `conftest.py`. `conftest.py` desvía cuentas (`ACCOUNTS_FILE`) y cuota (`QUOTA_DIR`), **pero no el marcador** (`USERS_DIR`). Ese aislamiento estaba duplicado como maniquí `autouse` en **tres** archivos de tests: `test_api.py`, `test_deploy_limits.py` y `test_english_tutor.py` (no dos, como decía este texto — corregido al cerrar). ✅ Hecha el 2026-08-06 (`[D-036]`): `app/tools.py` resuelve `USERS_DIR` dentro de la función, `conftest.py` desvía con un `setattr`, los tres maniquíes se borraron, y un portero nuevo (`tests/no_data_writes.py`, `[L-020]`/`[L-021]`) vigila que ningún test escriba en `data/` real. 329 tests verdes | ✅ | 7 |
| T-072 | 🚨 Existe un camino que escribe en `data/` real **sin pasar por `conftest.py`** — evidencia en `[A-020]`: el 2026-08-06 a las 14:48:33 aparecieron `data/users/otronombrelargo.json` y `data/quota/otronombrelargo.json` con el mismo nanosegundo, de una cuenta que no existe en `data/accounts.json`. ✅ Hecha el 2026-08-06 (`[L-023]`, `[D-037]`): el culpable era `measure_body.py`, la báscula de `T-054` — desvió `accounts.ACCOUNTS_FILE` y se olvidó de `USERS_DIR` y `QUOTA_DIR`. Arreglo estructural: `TEAPP_DATA_DIR`, ruta absoluta obligatoria sin valor por defecto, la app se niega a arrancar si falta o si la carpeta no existe. 342 tests verdes | ✅ | 7 |
| T-075 | 🚨 **Conseguir la API key de Anthropic y ponerla en el `.env` LOCAL.** `.env.example` ya la espera (`ANTHROPIC_API_KEY=`, vacía a propósito). Regla 1: jamás toca el navegador. Regla 7: jamás entra en un archivo de código, nunca se imprime completa. Acción del usuario, no del agente — y es 💰 **el primer gasto real del proyecto** (`_context/roadmap.md`). Sin ella el paso 8 no arranca. ✅ **CERRADA el 2026-08-10 (acción del usuario, sin cambio en el repo):** verificado sin imprimirla — empieza por `sk-ant-`, 108 caracteres, `.env` ignorado por git (`.gitignore:3`). 🚨 **Distinto de `T-078`:** esto es la llave en local; que llegue al servidor sigue pendiente, y de paso se confirmó que en el servidor `ANTHROPIC_API_KEY` existe pero está VACÍA — ese es el hueco que llena `T-078` | ✅ | 8 |
| T-076 | Sustituir el cuerpo de `judge_grammar` (`app/tools.py:128`) por la llamada real a Claude, con rúbrica. 🔑 **La firma se amplió sobre la marcha** (`[D-052]`: gana `client=None`) contra lo que este texto decía "definitiva". 🔄 **A MEDIAS el 2026-08-10 — ver entrada: la cuota del rechazo vacío se decide por `usage`, no por la forma de `content` (`[D-055]`, corrige `[D-054]`); 381 pasando; solo falta `app/api.py`** | 🔄 | 8 |
| T-077 | Borrar `FAKE_VERDICT` y el agente falso, y los tests que lo dan por bueno. `app/english_tutor.py` se declara falso en su propio docstring (línea 1); `judge_grammar` anuncia su propia muerte en la línea 136. ⚠️ **Precisión de esta sesión, sin ejecutar todavía:** "borrar el agente falso" solo borra MEDIA falsedad — `respond()` seguirá llamando a las tres herramientas siempre y en el mismo orden, porque `scope.md` no pide que el agente elija. El docstring de `app/english_tutor.py` se reescribe con precisión, no se borra sin más | 🔲 | 8 |
| T-078 | Que `ANTHROPIC_API_KEY` llegue al servidor: `install.sh` tiene que colocarla en el archivo de entorno de la máquina, con permisos cerrados, sin escribirla nunca en el repo. ⚠️ **Enlaza con `[A-023]`:** es exactamente la pieza que hace que el `deploy/` de septiembre no sea el de hoy, y por tanto condiciona el ensayo de `T-069` | 🔲 | 8 |
| T-079 | Medir de verdad los dos frenos que hoy son predicción, con el modelo real y facturas encima: `[A-010]` (20 prácticas/día por persona) y `[A-011]` (10 s de timeout al tutor). Las dos dicen en `assumptions.md` que se miden en el paso 8 — con `T-076` hecho dejan de ser suposiciones | 🔲 | 8 |

⚠️ T-031 y T-032 son el trabajo central del paso 2 y se hicieron **antes** que
T-021…T-029, aunque lleven número mayor. Los números de T-021 en adelante venían
ya puestos en la revisión externa que los encontró, y se respetaron para que las
referencias no mintieran.

⚠️ **T-037 lleva paso 3 a propósito**, aunque se haga después: es **deuda del
paso 3**, no trabajo del 6. La columna dice de dónde viene la tarea, no cuándo
toca hacerla.

---

## Entradas

### [T-076] La llamada real a Claude en `judge_grammar`

- **Estado:** 🔄 a medias
- **Dónde quedó:** la suite VOLVIÓ A ARRANCAR el `[S-038]` (380 passed) y este
  tramo (`[S-039]`) la deja en **381 passed**, confirmado corriendo
  `python -m pytest -q` en este cierre. `tests/fake_tutor.py` es lo que finge
  ser Claude — veredicto de mentira (`STUB_VERDICT`), `FakeClient`, bloques
  falsos, excepciones del SDK ya fabricadas (`connection_error`,
  `auth_error`, `rate_limit_error`, `server_error`, `timeout_error`,
  `refusing_before_output`, `refusing_after_output`,
  `refusing_mid_output_without_partial`). `conftest.py` tiene un fixture
  `autouse` (`tutor_does_not_call_claude`) que lo instala en toda la suite,
  porque más de 40 tests de `test_api.py` pasan por `/practice`.
- 🚨 **Segunda auditoría externa del mismo día, sobre la primera: el proxy de
  `[D-054]` tenía un agujero comprobado.** Decidir con
  `stop_reason == "refusal"` **y** `content` vacío confunde dos respuestas
  distintas: sin streaming (como llama `judge_grammar`), un rechazo a MITAD
  omite el parcial y llega calcado por fuera al rechazo gratis, con los
  tokens ya pagados. `[D-055]` corrige: `app/tools.py` decide ahora con
  `answer.usage.input_tokens > 0 or answer.usage.output_tokens > 0` — el
  contador de la propia respuesta, no una forma inferida. `tests/fake_tutor.py`
  gana `FakeUsage` y el campo `usage` en `FakeAnswer` con defecto
  **facturado** (regla 3 metida en el valor por defecto), más el constructor
  `refusing_mid_output_without_partial()`.
- **Verificado con sabotaje, no solo con la suite en verde:** el guardián
  nuevo `test_a_billed_refusal_with_no_partial_still_charges`
  (`tests/test_tools.py`) fue visto en ROJO reponiendo el proxy viejo de
  `[D-054]` — falla con `request_sent = False`, cuota regalada, y solo ese
  falla. Se suma a los cinco guardianes ya vistos en ROJO en `[S-038]`:
  quitar el timeout, cobrar siempre el veredicto vacío, la regla corta del
  auditor original, reordenar los `except`, reordenar `TutorReply` en
  `app/english_tutor.py:53` (`[D-050]`).
- 🚨 **`app/api.py` sigue SIN TOCAR — es lo único que falta para cerrarla.**
  Tiene que cazar `TutorUnavailableError`, mirar `request_sent` y llamar a
  `quota.refund`. Toda la maquinaria que decide si la cuota se devuelve ya
  existe y está probada en `tests/test_tools.py`; hoy nadie la conecta con
  `api.py`, así que la cuota **nunca** se devuelve, ni siquiera cuando la
  petición nunca salió.
- **Notas:** `[D-050]` a `[D-055]` en `decisions.md` explican el porqué de
  cada pieza — leerlas antes de tocar `api.py`. `[D-054]` queda marcada como
  revisada por `[D-055]` en su propia entrada, no borrada: su mitad (1) —el
  `timeout=8.0`— sigue vigente. `[L-039]` documenta un hallazgo aparte, del
  guion de sabotaje (CRLF en Windows), no del código de producto. `[L-040]`
  documenta la lección de fondo de esta corrección: inferir un dato de la
  forma de la respuesta cuando el instrumento trae su propio contador al
  lado.

### [T-056] `TEAPP_REGISTRATION_OPEN` y `create_account.py` en la nube

- **Estado:** ✅ hecha del todo
- ⚠️ **Reportada según el traspaso de cierre de la sesión principal — trabajo
  por SSH contra la máquina real, no deja rastro en `git diff`.**
- **Verificado el 2026-08-10, dos mitades:**
  1. `TEAPP_REGISTRATION_OPEN = false` explícito en `/opt/teapp/.env`, con
     permisos `600` y dueño `ubuntu`.
  2. `create_account.py` corre en el servidor — llamado sin argumentos,
     contestó su mensaje de uso y salió con código 1, que es lo correcto.
- **De paso, un hallazgo que abre trabajo:** `ANTHROPIC_API_KEY` existe en el
  servidor pero está **vacía** — es el hueco que llena `T-078`.

### [T-059] Lanzar la EC2 con Elastic IP, apuntar DuckDNS

- **Estado:** ✅ hecha del todo
- **Primera mitad HECHA** el 2026-08-06: Elastic IP reservada en `us-east-1`
  (`[D-033]`), sin instancia y sin asociar, t=0 sellado a las 15:29 UTC
  (`3ff793e`). Es el disparador del experimento de `[A-018]` y el primer
  gasto real del proyecto.
- **Segunda mitad HECHA el 2026-08-08**, después de la quinta lectura de
  `[A-018]` (15:08 UTC, `Importe utilizado` sigue 0,00 → `[D-041]` cumplido,
  commit `5075762`). Cadena verificada **eslabón a eslabón, leída desde la
  ficha y no desde lo tecleado** (`LM.15`):
  - Instancia `i-0faa249…` en `us-east-1`, `t3.micro`, `Ubuntu Server 24.04
    LTS` (`ami-0f8a61b66d1accaee`, decidida en `[D-043]`), disco 8 GiB gp3,
    1 instancia.
  - Grupo `teapp-sg` de `T-060a` REALMENTE puesto — verificado en la pestaña
    Seguridad de la instancia: 80 y 443 desde `0.0.0.0/0`, 22 desde una sola
    dirección `/32`, sin 8000 y sin IPv6.
  - Elastic IP ya reservada, ASOCIADA (no se alquiló una segunda) —
    verificado en el campo `IPv4 pública` de la ficha, coincide.
  - `teapp.duckdns.org` RESOLVIENDO desde fuera (`nslookup` contra `8.8.8.8`
    → `32.199.55.191`, registro A) y sin registro AAAA huérfano.
  - Par de claves `teapp-key` (RSA, `.pem`) guardado fuera del árbol del
    repo, junto al token de DuckDNS de `T-058`; la ruta no se escribe aquí
    (repo público).
- **Trampas cazadas en pantalla el 2026-08-08, escritas en
  `deploy/console_steps.md`** (junto con `[D-043]`): el desplegable de AMI se
  recarga solo a la LTS más nueva (se seleccionó 24.04 y el resumen decía
  26.04 — cazado leyendo el resumen entero antes de lanzar), y cambiar la AMI
  reinicia el grupo de seguridad y los volúmenes — regla nueva: la AMI se
  elige PRIMERO y no se vuelve a tocar.
- 🚨 **Desde el lanzamiento, la máquina está encendida y facturando por
  hora.** La cuenta tiene ahora dos fuentes de gasto (Elastic IP + EC2): `h1`
  y `h2 − h1` de `[A-018]` siguen midiéndose, pero la cuantía del importe deja
  de ser atribuible solo a la IP.
- ⚠️ **Esta cadena de verificación se reporta según el traspaso de cierre de
  la sesión principal — es trabajo en la consola de AWS, que por su
  naturaleza no deja rastro en `git diff`.** Lo único que el diff del día
  respalda directamente es `[D-043]` y las dos trampas en
  `deploy/console_steps.md`.

### [T-055] El origen real detrás del proxy

- **Estado:** ✅ **hecha la mitad de Python** el 2026-08-06 (`D-034`), ✅
  **hecha la mitad de Caddy** el 2026-08-07 (medida en contenedor, sin EC2 —
  ver abajo), y ✅ **`T-060b` hecha el 2026-08-08** (según traspaso: el 8000
  da timeout desde fuera con Python escuchando de verdad). **Falta solo
  `T-066`** (dos dispositivos, con `X-Forwarded-Proto` real por HTTPS).
- ✅ **Mitad de Caddy MEDIDA el 2026-08-07, en contenedor con aparejo de dos
  cajas (cliente `172.17.0.4` ≠ proxy `172.17.0.3`).** Caddy escribe
  `X-Forwarded-For` con la dirección real, y de regalo **descarta** la
  cabecera forjada — sin `trusted_proxies` en la plantilla, política *"By
  default, no proxies are trusted"*. Cadena entera con TEAPP real: seis
  logins fallidos con seis orígenes falsos distintos, el freno saltó igual
  contra el origen real; control rojo con `--forwarded-allow-ips
  203.0.113.5` → log escribe `127.0.0.1` (`A-014` en falso, a la vista).
  ⚠️ **Límite escrito antes de medir:** ese Caddy sirve por HTTP, así que
  `X-Forwarded-Proto` da `http`, no `https` — medido el mecanismo, no el
  valor final. `[L-027]` nueva: el primer control (uvicorn sin
  `--proxy-headers`) salió ciego, no rojo, porque esa bandera ya viene por
  defecto en uvicorn 0.52.1. `[D-042]` nueva: guardián en
  `tests/test_deploy_limits.py` que falla si la plantilla declara
  `trusted_proxies`. Tabla completa en `deploy/README.md`.
- 🔄 **RECLASIFICADA el 2026-08-07: la mitad de Caddy YA NO espera máquina.**
  Estaba en la lista como "necesita EC2" y **es gratis**. Se mide en contenedor:
  renderizar `Caddyfile.template` a `:80`, arrancar Caddy con esa configuración, y
  ver qué cabecera le llega a uvicorn. 🔑 **No apareció trabajo nuevo — apareció
  que un trabajo conocido costaba mucho menos que su etiqueta** (`LM.19`).
  ⚠️ **Y el límite se escribe ANTES de medir, no después:** ese Caddy sirve por
  **HTTP**, así que `X-Forwarded-Proto` dirá `http`, no `https`. Mide el
  **mecanismo**, no el valor final. Al cerrar hay que decir cuál de las dos cosas
  quedó medida.
  📌 **Se mide sobre `teapp-rig`**, la imagen congelada el 2026-08-07 desde
  `teapp-test` (Caddy 2.11.4 + `venv` + código ya dentro). 🚨 **Esa caja NO es
  reproducible** —corrió `install.sh` y se toqueteó a mano—, así que la regla de
  diseño es: **lo que se mida ahí tiene que colgar de entradas reproducibles**.
  Renderizar desde la plantilla versionada cumple; leer estado acumulado, no.
- 🔑 **La corrección que hay que respetar al escribirla.** El primer argumento
  fue *"sé quién escribe `X-Forwarded-For` porque el proxy es mío"*, y **es
  falso**. Ser dueño del proxy no impide que alguien hable con FastAPI **por otro
  lado** y escriba la cabecera que quiera. La garantía viene de que **nadie más
  pueda alcanzar a FastAPI**, y son **dos cosas juntas**:
  1. **uvicorn atado a `127.0.0.1`**, no a todas las direcciones (`T-062`).
  2. **el cortafuegos abierto solo en 80 y 443**, y **medido desde fuera**
     (`T-060b`; `T-060a` solo lo deja escrito).
  ⚠️ **Sin las dos no hay certeza, hay costumbre.** Con una sola, el freno de
  `/login` se convierte en el ataque: quien lo intenta cambia de origen en cada
  intento y no se frena nunca.
- ✅ **La pista era buena y se midió el 2026-08-06.** Las opciones son
  `--proxy-headers` y `--forwarded-allow-ips`, y en uvicorn 0.52.1 **ya vienen
  puestas con el valor que hacía falta**. Se escriben igual de explícitas en
  `deploy/teapp.service`, porque un ajuste de seguridad que depende de un valor
  por defecto cambia el día que alguien actualice la librería. Los cuatro
  escenarios medidos están en `[D-034]` y **solo ahí** (`[L-018]`).
- ⚠️ **Y la medición estuvo a punto de mentir:** el escenario del suplantador
  llegaba disfrazado de Caddy. Ver `[L-019]`.
- **Cómo se sabe que quedó hecha del todo:** `T-066`. La marca ✅ de arriba cubre
  el código, **no la cadena real**.

### [T-050] La llave de firma, estable entre despliegues

- **Estado:** ✅ hecha del todo
- **Dónde vive:** un archivo de variables de entorno **en la máquina**, con
  permisos cerrados, que lee el arranque automático (`T-062`). No en Git, no en
  un servicio aparte — en EC2 es un archivo y ya (`D-029`).
- 🚨 **La dificultad no era ponerla: era que el guion no la pisara.** Un guion de
  instalación que genere la llave **cada vez que corre** produce exactamente el
  fallo de `[L-032]` (antes `A-008`) — todas las sesiones muertas de golpe, todo el mundo fuera, y
  **ni un error en el log que lo explique**. El síntoma lleva derecho a sospechar
  del navegador o de las cookies, que es donde no está el problema.
- 🔄 **Avance del 2026-08-07, sin EC2 (`[L-024]`):** el **mecanismo** ya está
  medido en contenedor Ubuntu — dos corridas reales dan la misma huella de
  llave (`7915abd41bf6`), y el freno se vio morder (anulando el `if` de guarda,
  la llave cambia a `24dd6bc2520f` → `6ded9368fe44`). Sigue 🔄 porque falta el
  **efecto**, no el mecanismo: que `teapp.service` lea ese `.env` bajo systemd
  de verdad, que el disco sobreviva a un reinicio real, y que una sesión viva
  aguante un redespliegue en EC2. Eso solo se mide con la máquina encendida
- 🔄 **Avance del 2026-08-08:** dos de los tres pendientes se midieron en la EC2
  de verdad. Con el servidor arriba bajo `systemd`, se generó una cookie, se
  hizo `sudo systemctl reboot`, y la MISMA cookie (emitida antes del reinicio)
  siguió siendo válida después — la llave no se regeneró y `teapp.service` sí
  lee el `.env`. `.env` quedó en `600`, propiedad de `ubuntu`.
- ✅ **CERRADA el 2026-08-09 — el redespliegue, lo único que faltaba, medido:**
  `git pull` `aff4350`→`0dfdbba`, `install.sh` código 0. Huella del `.env`
  idéntica antes/después (`1f0365563d…`, nunca impresa entera), `accounts.json`
  idéntica, `data/users/jorge.json` con fecha 2026-08-08 18:25:15 y
  `{"score": 5}` intacto, servicios `active`, 200 en local, y la sesión del
  navegador sobrevivió al F5. Detalle completo en `[L-032]`.

<!-- Solo las tareas que necesitan detalle. Las que se entienden en una línea
     se quedan en el índice y no bajan aquí. Formato:

### [T-001] <título corto>

- **Estado:** 🔲 / 🔄 / ✅
- **Dónde quedó:** <solo si está a medias: en qué punto exacto>
- **Notas:** <lo que haga falta para retomarla sin releer nada>

-->
