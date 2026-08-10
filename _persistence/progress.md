# Avance — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [S-000]`. Búscala con `grep`, no leas el archivo entero.

## Estado actual

| | |
|---|---|
| **paso** | 8 de 9 — 🔄 **`T-076` ARRANCADA y A MEDIAS: `judge_grammar` ya llama a Claude de verdad, pero la suite NO ARRANCA.** Vigésimo tramo (`[S-037]`), después del cierre que dejó `[S-036]`. `app/tools.py` reescrito: se borró `FAKE_VERDICT`, `judge_grammar` llama a `claude-opus-5` con `effort: "low"` y la rúbrica A1 (`[D-049]`), nueva excepción `TutorUnavailableError` con `request_sent` (`[D-051]`), cliente construido dentro de la función con `client=None` opcional (`[D-052]`) y `max_retries=0` (`[D-053]`). `app/config.py` gana `require_anthropic_key()` y `log_tutor_mode()`. `requirements.txt` suma `anthropic==0.121.0`. `.env.example` deja de decir "todavía no se usa". Verificado hoy con un guion suelto (cliente falso, no test de la suite): camino feliz, `APITimeoutError`→`request_sent=True`, `APIConnectionError`→`request_sent=False` pese a que hereda de la primera, respuesta vacía lanza, `TypeError` con no-`str`. 🚨 **`python -m pytest -q` termina en `Interrupted: 3 errors during collection`:** `tests/test_tools.py`, `tests/test_english_tutor.py` y `tests/test_api.py` (11 referencias en total) importan `FAKE_VERDICT`, que ya no existe. Confirmado en este cierre, corriendo la suite de verdad. Los 362 tests verdes del 09 hoy NO se pueden correr, ni siquiera los que no tocan esto |
| **última sesión** | 2026-08-10 (vigésimo tramo) |
| **siguiente acción** | 🚨 **PRIMERO arreglar la suite, antes de cualquier otra cosa: reescribir `tests/test_tools.py`, `tests/test_english_tutor.py` y `tests/test_api.py` para que dejen de importar `FAKE_VERDICT`.** Añadir de camino los tres tests nuevos que exige `T-076`: (1) el fallo de Claude no suma punto, (2) el orden de las tres líneas de `TutorReply` en `app/english_tutor.py:53` no se puede reordenar sin ponerse rojo, (3) el fallo que nunca salió devuelve cuota y el que sí salió no. Después: `app/api.py` tiene que cazar `TutorUnavailableError`, mirar `request_sent` y llamar a `quota.refund` — sin tocar todavía. Y después de eso, `T-077`, `T-078`, `T-079`. ⚠️ **Sobre el estado de la máquina de producción: no se afirma aquí sin comprobarlo** (`[L-038]`) |

## Índice

| id | fecha | qué avanzó | paso |
|---|---|---|---|
| S-037 | 2026-08-10 | Vigésimo tramo, después del cierre que dejó `[S-036]`. `T-076` arrancada y **a medias**: `app/tools.py` reescrito con la llamada real a `claude-opus-5` (`effort: "low"`), `TutorUnavailableError`/`request_sent` (`[D-051]`), `client=None` inyectable (`[D-052]`), `max_retries=0` (`[D-053]`); `app/config.py` gana `require_anthropic_key()`/`log_tutor_mode()`; `requirements.txt` suma `anthropic==0.121.0`; `.env.example` al día. Verificado con guion suelto (cliente falso), no con la suite. 🚨 **`python -m pytest -q` da `Interrupted: 3 errors during collection`:** `tests/test_tools.py`, `tests/test_english_tutor.py`, `tests/test_api.py` importan `FAKE_VERDICT` (borrado hoy), 11 referencias — confirmado corriendo la suite en este cierre. `app/api.py` sin tocar todavía (falta cazar `TutorUnavailableError` y llamar a `quota.refund`). `T-077`/`T-078`/`T-079` sin empezar. `[D-050]`-`[D-053]` nuevas en `decisions.md`, escritas por la sesión principal, revisadas en este cierre. Paso 2b: `.js` compilado, al día (`compilar: 0`, `comparar: 0`) — no había ningún `.ts` tocado | 8 |
| S-036 | 2026-08-10 | Decimonoveno tramo, después del cierre que dejó `[S-035]`. Sesión de decisión, verificación por SSH y planeación: el único archivo del repo modificado es `_persistence/decisions.md` (`[D-049]`); ningún archivo de `app/`, `tests/` ni `deploy/` tocado. **`T-075` CERRADA:** API key de Anthropic en el `.env` LOCAL, verificada sin imprimirla (empieza `sk-ant-`, 108 caracteres, `.gitignore:3` la protege) — acción del usuario, sin cambio en el repo. **`T-056` CERRADA** (según traspaso, sin rastro en `git diff`): corrida real por SSH contra la EC2 — `TEAPP_REGISTRATION_OPEN = false` explícito en `/opt/teapp/.env` (permisos 600, dueño `ubuntu`), y `create_account.py` corriendo en el servidor (sin argumentos, mensaje de uso, código 1). De paso se confirmó que `ANTHROPIC_API_KEY` existe en el servidor pero está VACÍA — abre `T-078`. **`[D-049]` nueva:** el paso 8 arranca con `claude-opus-5` a `effort: "low"` — el modelo MÁS caro, no el más barato — porque arrancar por Haiku reintroduciría dos sospechosos posibles (modelo o rúbrica) el día que se estrena el veredicto real; el descenso a Sonnet 5 y Haiku 4.5 pasa a ser trabajo MEDIDO del paso 9. Plan de archivos de `T-076` hecho y sin ejecutar (`app/tools.py`, `app/config.py`, `app/english_tutor.py`/`app/api.py`, tres archivos de tests, `requirements.txt`, `.env.example`, `deploy/install.sh`); hallazgo de camino: `tests/no_network.py` obliga a que los tests nuevos inyecten un cliente falso. Precisión sobre `T-077`: "borrar el agente falso" solo borra media falsedad — `respond()` sigue llamando a las tres herramientas siempre y en el mismo orden. **Verificado en este cierre:** `git status` mostraba un solo archivo modificado, ningún `.env` en la lista. Paso 2b: `.js` compilado, al día (`compilar: 0`, `comparar: 0`) — no había ningún `.ts` tocado | 8 |
| S-035 | 2026-08-10 | Decimoctavo tramo, después del cierre que dejó `[S-034]`. Sesión de decisión y documentación pura, sin tocar `app/` ni `tests/` ni la consola de AWS. El usuario objetó el ritmo del proyecto; contado sobre este índice (regla 6): pasos 0–6 = 12 sesiones/3 días, paso 7 solo = 22 sesiones/6 días. Se corrigió un error de la misma sesión — `T-069` NO bloqueaba el paso 8, `[D-030]` mide "pronto" contra `[C-006]`, no contra el paso 8. **`[D-048]`: se cruza al paso 8** con `T-046`, `T-067`, `T-069`, `T-070` abiertos, cada uno con motivo y dueño; `T-056` se hace de camino, era lo único que bloqueaba de verdad. **`[D-047]`** (antes de la corrección): ensayo de `T-069` sobre instancia y subdominio nuevos (`teapp-rehearsal.duckdns.org`), producción viva y sin Elastic IP — `deploy/console_steps.md` gana el Paso 5c con el guion completo; no hizo falta tocar una línea de `deploy/`, `TEAPP_DOMAIN` ya era variable de entrada. Tras `[D-048]`, `[D-047]` queda anotada como APLAZADA, no anulada. **`[A-023]`** nueva: el precio de aplazar `T-069` — el paso 8 va a tocar `deploy/` (la llave entra por el archivo de entorno), fecha tope ≈ 2026-09-01. **`[L-037]`** nueva: el andamio se volvió el trabajo, ninguna sesión individual falló y aun así el conjunto no avanzó; lo detectó el usuario. Suite no corrida hoy, sigue en 362 (última corrida del 09, sin cambios en tests) | 7→8 |
| S-034 | 2026-08-10 | Decimoséptimo tramo, después del cierre que dejó `[S-033]`. **`T-074` CERRADA con testigo directo:** el temporizador de `[D-045]` disparó anoche, medido en el journal (que en Ubuntu 24.04 sobrevive al reinicio) — `Aug 09 23:00:00 Starting teapp-shutdown.service … ([D-045])` seguido en el mismo segundo de `systemd-logind: The system will power off now!`, cadena causal con nombre propio, no inferencia por descarte. `[L-035]` nueva: el testigo que se propuso primero, `systemctl list-timers`, salió con `LAST`/`PASSED` vacíos y no por avería — `Persistent=false` (puesto a propósito en `[D-046]`) le dice a systemd que no lleve libreta de disparos pasados, así que ese instrumento nunca podía contestar "¿disparó ayer?". De regalo: Caddy se apagó limpio (`exit_code: 0`) y la máquina volvió con otro núcleo (`6.17.0-1017-aws` → `7.0.0-1010-aws`). **`T-066` CERRADA DEL TODO:** las dos mitades medidas en el servidor real — la real (computador `181.58.39.253` y celular por datos móviles `191.153.227.163`, cada uno coincidiendo con su propio `ipify`) y la falsa (cuatro peticiones con `X-Forwarded-For`/`X-Real-IP: 9.9.9.9` contra el cubo ya agotado, las cuatro `429`, ni un `9.9.9.9` en el log). `[A-014]` retirada de `assumptions.md`, vive ahora en `[L-036]`. **`[A-022]` ENCOGIDA, no cerrada:** `systemd 255 (255.4-1ubuntu8.16)` en la máquina viva confirma `Normalized form: *-*-* 23:00:00 UTC` — pero la suposición habla de "cualquier máquina donde se reconstruya", y eso solo lo mide `T-069` sobre imagen nueva, que queda 🔄 a medias. `[A-018]` ampliada: el `-` de *Importe previsto* pasa de observado a documentado (menos de un ciclo de facturación), y se descarta el experimento de bajar el umbral — ya está 37× por debajo del gasto sin saltar. Corregido en tres sitios un puntero desfasado que mandaba a `T-060b` (cerrada desde el 08). Paso 5b de `deploy/console_steps.md` corrido entero: cinco controles en verde (servicios `active`, `200` por el nombre, certificado sin reemitir hasta noviembre, marcador `{"score": 5}` intacto, temporizador rearmado solo). Ningún archivo de `app/` ni `tests/` tocado; suite no corrida hoy, sigue en 362 (última corrida conocida, del 09). Solo `_persistence/assumptions.md` y `_persistence/lessons.md` en el diff — el resto (journal, Paso 5b, dos dispositivos) es trabajo en la máquina real, registrado según el traspaso de cierre | 7 |
| S-033 | 2026-08-09 | Decimosexto tramo, después del cierre que dejó `[S-032]` (`094f0e9`). Revisión externa sobre `install.sh`: comprobaba el temporizador solo con `systemctl is-active`, que no ve el estado `activo pero NO habilitado` — el mismo modo de fallo que `T-074` no puede medirse a sí misma. Arreglo: `is-enabled` al lado de `is-active`, más el quinto guardián en `tests/test_deploy_shutdown.py`, control rojo con el guion tal como estaba antes de la revisión. De 360 a **362** tests. `[L-034]` nueva: un control que mide el ahora no mide el mañana, y es la SEGUNDA vez el mismo día que un guardián nace incapaz de ponerse rojo en el fallo que su propio comentario nombra como el peor (el cuarto guardián de `tests/test_deploy_shutdown.py`, horas antes, tenía la misma forma). Gana su antepasado real: `[L-017]` (2026-08-05) es el MISMO archivo, MISMO bloque, MISMA orden `is-active` — arreglar un bloque no lo inmuniza, lo deja más peligroso, porque hereda la cicatriz de haber sido auditado. `[A-022]` nueva: la zona horaria dentro de `OnCalendar` (`*-*-* 23:00:00 UTC`) depende de la versión de systemd y no está comprobada en ningún sitio — se mide gratis con `systemd-analyze calendar`, hoy en la máquina y otra vez en `T-069`. Corregida una colisión detectada por la misma revisión: la primera versión de `[L-034]` citó mal una lección de este propio repo (heredada sin abrirla de `[D-041]`/`[L-028]`) — resultó ser colisión de identificadores entre esa lección local y su homóloga del repo supervisor (`Edu_TripleS/PROGRESO.md`), no un error de sentido. 16 citas corregidas (15 en `_persistence`, 1 en `tests/test_config.py`) y el prefijo (`[LM.nn]` doble letra para el supervisor, `[L-nnn]` guion para este repo) escrito por primera vez en `CLAUDE.md` — la convención ya existía de hecho pero no protegía de nada sin estar escrita. Dos de las 16 correcciones cayeron en este mismo `progress.md` (sección `[S-032]`), y quedan marcadas como deliberadas con su control de verificación descrito en `[L-034]`, para que un cierre futuro no las arrastre de vuelta. `[L-034]` amplíada con un riesgo y un antepasado más: el riesgo de que ese arreglo de `progress.md` se deshaga solo si un cierre regenera la sección arrastrando texto viejo (por eso el control queda escrito, no solo corrido una vez); y el antepasado de la lección del recuento, del lado supervisor (sesión 7 de `Edu_TripleS`, un costo estimado ~0,02 US$ contra 0,038 medido) — reapareció hoy contando archivos (9→13→15→16) en vez de dinero. Ningún archivo de `app/` tocado; suite corrida de verdad en este cierre: **362 passed**. 🚨 `T-074` sigue PENDIENTE, vence hoy 2026-08-09 a las 23:00 UTC (18:00 Colombia) — nada de este tramo la mide | 7 |
| S-032 | 2026-08-09 | Decimoquinto tramo, después del cierre que dejó `[S-031]`. **`T-073` CERRADA:** la pieza de apagado automático de `[D-045]` deja de ser un disparo único y pasa a systemd — `deploy/teapp-shutdown.service` (`shutdown -P now`) y `deploy/teapp-shutdown.timer` (`OnCalendar=23:00:00 UTC`), instalados por `install.sh` sección 4b, con `Persistent=false` explícito y sin sección `[Install]` (para que `install.sh` no la arranque a mitad de instalación). `[D-046]` nueva: systemd sobre `cron`, porque `cron` lee la hora en la zona de la máquina, un ajuste fuera del repo; escrita primero como "no medida" y actualizada una hora después con la corrida real en la máquina (17:37–17:50 UTC): `git pull` `0dfdbba`→`afe2eab`, `install.sh` código 0, temporizador armado (`Sun 2026-08-09 23:00:00 UTC`, `LAST`/`PASSED` vacíos, armado sin usar), disparo único desarmado con medición antes y después (`USEC` traducido, no dado por bueno), `list-timers` releído después de cancelar para confirmar que el temporizador nuevo sigue en pie. `[L-033]` nueva: el rodeo del DNS de `deploy/console_steps.md` perdió la palabra `SSH` al recontarse — por la IP fija se entra por SSH, por navegador y `curl` por el nombre de DuckDNS. `deploy/console_steps.md` gana el Paso 5b: el guion de encender la máquina cada mañana, con cinco controles, el quinto (que el temporizador se haya rearmado solo) sin síntoma si falla. De 351 a **360** tests: `tests/test_deploy_shutdown.py` nuevo, cuatro guardianes, cada uno visto ROJO con su fallo puesto. 🚨 **`T-074` queda PENDIENTE y vence hoy 2026-08-09 a las 23:00 UTC (18:00 Colombia):** es lo único de la pieza que sigue sin medir — que el temporizador dispare de verdad y la instancia pase a `stopped` en la consola de AWS. Mañana la máquina hay que encenderla a mano. Ningún archivo de `app/` tocado hoy | 7 |
| S-031 | 2026-08-09 | Decimocuarto tramo, después del cierre que dejó `[S-030]`. **`T-051` CERRADA:** cookie `Secure`/`HttpOnly`/`SameSite=Lax` medida en NAVEGADOR REAL sobre `https://teapp.duckdns.org`, y F5 sin recredenciales → "Signed in as jorge" — las dos mitades del contrato (guardar y devolver). **`T-050` CERRADA:** redespliegue en la máquina viva, `git pull` `aff4350`→`0dfdbba`, `install.sh` código 0; huella del `.env` idéntica antes/después (`1f0365563d…`), `accounts.json` idéntica, `data/users/jorge.json` con fecha 2026-08-08 18:25:15 y `{"score": 5}` intacto, servicios `active`, 200 en local, sesión del navegador sobrevivió al F5. Ascienden `[A-005]`/`[A-008]` → `[L-032]`, `[A-009]` → `[L-031]`; los punteros se reetiquetan en `assumptions.md`, `decisions.md`, `lessons.md`, `app/config.py`, `app/sessions.py`, `tests/conftest.py`, `tests/test_api.py`, `tests/test_config.py`, `tests/test_sessions.py` y `deploy/install.sh`. **`[D-045]` nueva:** ventana de uso 07:00–18:00 Colombia = 12:00–23:00 UTC, apagado automático desde dentro / encendido manual, arranca hoy a las 23:00 UTC; reabre `[D-029]` y deja caducada `[D-044]`. Ajuste "comportamiento de apagado iniciado por la instancia" leído en consola: `Detener` (no `Terminar`) — condición dura cumplida antes de escribir la pieza. Temporizador único `sudo shutdown -P 23:00` armado y verificado (`timedatectl`, `MODE=poweroff`); no sobrevive a un `stop`/`start`, así que no es la pieza definitiva. `[A-018]` sexta lectura (~14:45 UTC): `Importe utilizado` sigue 0,00 (cuarta lectura seguida en cero), `Costo Acumulado Mensual` sube a 0,37 US$ — el incremento ya no cabe solo en la Elastic IP, primera señal en pantalla de que la EC2 pesa; corregido: son **tres** fuentes de gasto (Elastic IP, horas de instancia, volumen EBS), no dos como decía la quinta lectura. `[A-017]` episodios 4 y 5: fenómeno partido entre `ssh` (falla), `nslookup` y `curl` (aciertan) en el mismo minuto — causa localizada en la resolución del cliente, no en DuckDNS; una hipótesis (`-4` de IPv4) murió en dos minutos. `[L-030]` nueva: `uptime -s` no es un registro, se reinicia — el `t=0` de la EC2 pasó de medido a anotado tras el `reboot` de `T-065`. `[L-029]` nueva (de sesión previa, commiteada hoy): lo que nace después del cierre no tiene dueño. Ningún archivo de `app/` o `tests/` cambia de comportamiento — los siete tocados son solo comentarios re-etiquetando anclas retiradas. Suite no corrida hoy, sigue en 351 | 7 |
| S-030 | 2026-08-08 | Decimotercer tramo, después del cierre que dejó `[S-029]`. **TEAPP quedó DESPLEGADO EN PRODUCCIÓN.** Primera conexión SSH del proyecto y primera corrida real de `deploy/install.sh` en máquina de verdad. `T-061` (Caddy+HTTPS): `200` con `ssl_verify_result=0` desde fuera, `80→443` con `308`, certificado Let's Encrypt `CN=teapp.duckdns.org` válido hasta 2026-11-06. `T-062` (arranque automático): reinicio real verificado con `uptime -s`, `teapp`/`caddy` en `active` sin que nadie los encienda, uvicorn solo en `127.0.0.1:8000`. `T-060b` (cortafuegos medido): con Python escuchando de verdad en el 8000, la petición desde fuera dio timeout — ya no es el control ciego de `[L-020]`. `T-064` (primera cuenta): `jorge` creada con el servidor parado (`A-002`), contraseña generada con `openssl rand`, nunca escrita en el repo; `/login`, `/me` y el rechazo con contraseña mala verificados desde fuera. `T-065` (el disco persiste): marcador a 3 puntos, `reboot`, la frase siguiente dio `score = 4`. `T-050` y `T-051` avanzan a 🔄, no se cierran: falta el redespliegue en el primero y un navegador real en el segundo (`curl` no es un navegador). `T-066` sigue sin hacerse. `[C-007]` nueva: repositorio público, verificado con `git clone` sin credenciales — ningún secreto ha entrado nunca, pero `_persistence/`, `_context/` y `deploy/console_steps.md` los lee cualquiera. `[A-018]` gana el `t=0` MEDIDO de la EC2 (`uptime -s` → 15:54:27 UTC), corrigiendo una deducción previa que tomaba por `t=0` la hora de leer el presupuesto (46 min antes de lanzar). `[A-017]` gana tres episodios OBSERVADOS de `Could not resolve host` desde dos redes, con corrección explícita de que la causa NO está resuelta (16/16 correctas en el diagnóstico, apunta al resolutor del cliente, no a DuckDNS) y la exposición del certificado medida. `[A-005]` se encoge otra vez: el reinicio queda medido, el redespliegue sigue vivo. ⚠️ **Todo el trabajo de despliegue ocurrió en la máquina y se registra según el traspaso de cierre** — no deja rastro en `git diff`; lo único que el diff respalda directamente es `_persistence/assumptions.md` y `_persistence/constraints.md`. Ningún archivo de `app/` ni `tests/` tocado; suite no corrida hoy, sigue en 351 (última corrida del 07) | 7 |
| S-029 | 2026-08-08 | Duodécimo tramo, después del cierre que dejó `[S-028]`. Quinta lectura de `[A-018]` (15:08 UTC): `Importe utilizado` sigue 0,00, sin cambio en 3,9 h — cumple el orden de `[D-041]` (leer antes de lanzar, diga lo que diga el campo). Revisión externa antes del primer clic corrigió dos huecos en `deploy/console_steps.md`: el punto 5 del paso 3 decía "reservar y asociar" la Elastic IP cuando ya solo tocaba asociar (la reserva se ejecutó el 06 al partirse `T-059`), y el paso del grupo de seguridad no estaba escrito en ningún sitio, solo en el chat — `[L-028]` nueva. `T-059` reportada CERRADA DEL TODO: instancia `t3.micro` (`Ubuntu Server 24.04 LTS`, `[D-043]`) en `us-east-1`, grupo `teapp-sg` de `T-060a` puesto de verdad, Elastic IP ya reservada asociada (no una segunda), `teapp.duckdns.org` resolviendo desde fuera, llave `teapp-key` fuera del repo. `[D-043]` nueva: la AMI es 24.04, no la 26.04 (`install.sh` solo medido en esa versión, `[L-024]`) ni `Ubuntu Pro` (cargo por hora sin beneficio). Dos trampas del formulario de lanzamiento medidas y escritas: el desplegable de AMI se recarga solo a la LTS más nueva, y cambiar la AMI reinicia el grupo de seguridad y los volúmenes. `T-060b` sigue sin hacerse — bloqueada por `T-062` (nada escuchando en el 8000 todavía), no por `T-059`. 🚨 Desde hoy la máquina está encendida y facturando por hora: dos fuentes de gasto en la cuenta. ⚠️ La verificación de la EC2 en consola (SG, IP, DNS, llave) se registra según el traspaso — no deja rastro en `git diff`; lo que el diff respalda directamente es `[D-043]` y `deploy/console_steps.md`. Ningún archivo de `app/`/`tests/` tocado; suite no corrida hoy, sigue 351 (última corrida del 07) | 7 |
| S-028 | 2026-08-08 | Undécimo tramo, sesión corta de solo lectura, después del cierre que dejó `[S-027]`. Cuarta lectura de `[A-018]` (11:10 UTC, ~43,7 h desde `t=0`): primer cargo distinto de cero, visto en un instrumento nuevo — widget `Resumen de Costos` de la página de inicio de *Facturación y costos*, `Costo Acumulado Mensual` = 0,12 US$ — mientras `Importe utilizado` del presupuesto sigue en 0,00. Mata la causa (b) de la enmienda de `[D-040]` y confirma/localiza la causa (a) en el tramo 2 (refresco del presupuesto, 8–12 h): los dos tramos en serie observados por primera vez a la vez. `A-018` NO se cierra: `h1` no ha ocurrido. `[D-041]` sigue sellado; su segunda mitad (lanzar la EC2) **no se ejecutó** — el usuario cerró la sesión antes, queda como primera acción de mañana. Elastic IP sigue reservada y ociosa. Ningún archivo de código tocado; solo `_persistence/assumptions.md` | 7 |
| S-027 | 2026-08-07 | Décimo tramo del día, después del cierre que dejó `[S-026]`. `[D-041]` sellado: la segunda mitad de `T-059` (lanzar la EC2) se pospone al 2026-08-08, después de leer `Importe utilizado`, para no matar la medida irrepetible `t_cargo − t=0` y no encender la máquina con la alarma sin habérsela visto morder — la Elastic IP no se suelta. Trabajo del día: `T-055`, mitad de Caddy, medida en contenedor. Caddy escribe `X-Forwarded-For` real (aparejo de dos contenedores) y descarta la cabecera forjada por no declarar `trusted_proxies` — cadena entera probada con seis logins fallidos y seis orígenes falsos, el freno saltó contra el real. `[L-027]`: el primer control salió ciego (uvicorn ya trae `--proxy-headers` por defecto en 0.52.1), no rojo. `[D-042]`: guardián nuevo en `tests/test_deploy_limits.py` que impide que la plantilla declare `trusted_proxies`. Tercera lectura de `[A-018]`, sigue 0,00. De 348 a **351** tests | 7 |
| S-026 | 2026-08-07 | Noveno tramo del día, después del cierre que dejó `[S-025]`. Segunda lectura de `[A-018]` (~23,1 h desde `t=0`): sigue NO CONCLUYENTE, con tres hallazgos — `Facturas` era la ventana equivocada dos días seguidos (una factura nace al cerrar el mes; la lectura buena es `Importe utilizado` del propio presupuesto, mismo instrumento que la alarma, hoy `0,00 US$` con `0.00%` calculado); resuelto gratis que AWS no puede proyectar sin historial (`Importe previsto` = `-`); y corregido en caliente que las 750 h gratis de IPv4 cubren direcciones EN USO, no una ociosa — la nuestra cobra (~0,115 US$ bruto, aritmética de lista), así que el experimento sigue siendo falsable. Enmienda sellada antes de mirar nada mañana: la FILA 3 de la tabla original (`cfba50a`) queda ANULADA, no borrada, porque nombraba una causa hoy desmentida; guardia nueva sobre la FILA 2 (`[D-040]`) exige ≥12 h de silencio tras hacerse visible el importe, con el motivo corregido dos veces el mismo día hasta quedar en un solo desconocido (si mostrar y evaluar comparten reloj o no); se anotan dos horas, `h1`/`h2`, como segunda medición gratis. `[L-026]` nueva: `T-068` es el único control estructuralmente inverificable del proyecto —probarlo ES el desastre—, no es un freno sino disciplina, y la disciplina se degrada con la repetición; "Actualizar plan" sale de la lista de puertas y pasa al protocolo de lectura diario, por tráfico y no por peligrosidad. `T-060` partida en `T-060a`/`T-060b` (`LM.13`: tener el grupo creado no es tener el cortafuegos, es tenerlo escrito). **`T-060a` HECHA:** grupo de seguridad `teapp-sg` creado en `us-east-1`, VPC `default` (única ofrecida), reglas leídas desde la ficha —`80/tcp` y `443/tcp` desde `0.0.0.0/0`, `22/tcp` desde una sola dirección `/32`, sin 8000 y sin IPv6, salida intacta—; el primer intento falló por el apóstrofo de "Let's" en una descripción de regla y AWS deshizo el grupo entero. `deploy/console_steps.md` ampliado: la salida abierta a propósito (y por qué endurecerla rompería `install.sh` en silencio), la VPC como el mismo tipo de trampa que la región, y el aviso del puerto 22 con la IP de casa. Ningún archivo de código tocado; solo `_persistence/` y `deploy/console_steps.md`. 🔻 **Ampliada tras un segundo tramo el mismo día (commits `c0f0201`, `7630862`, ya en `origin` antes de este cierre):** `[L-024]` ampliada, no `[L-026]` nueva — la sección 5 de `install.sh` nunca corrió, en ningún sitio; `caddy validate` sobre `Caddyfile.template` renderizado dio `Valid configuration` por primera vez en la vida del proyecto (mide sintaxis, no comportamiento); cayó la suposición de que el contenedor tenía Caddy↔uvicorn aparejados (no la tenía, `Caddyfile` de fábrica); receta del contenedor escrita en `deploy/README.md`; imagen local `teapp-rig` congelada (no va a Git); `T-055` reclasificada — su mitad de Caddy ya no espera máquina, es gratis y se mide en contenedor, con el límite HTTP-no-HTTPS escrito antes de medir. Detalle completo al final de la entrada | 7 |
| S-025 | 2026-08-07 | Octavo tramo del día, después del cierre que dejó `[S-024]`. Primera lectura del experimento de `[A-018]`: NO CONCLUYENTE — silencio en la bandeja pero la factura sin dato todavía ("estamos preparando sus datos de costos y uso"); registrado el cuarto estado ("aún no hay dato" se disfraza de `$0.00`) y tres relojes distintos, incluido el dólar de verificación de tarjeta que no aparecerá nunca en la factura. Próxima lectura 2026-08-08; la Elastic IP sigue reservada y ociosa. Hallazgo grande fuera de la nube: `deploy/install.sh` se pudo correr entero (menos systemd) en un contenedor Ubuntu 24.04 sin gastar un céntimo (`[L-024]`) — con eso `[A-008]` (la llave sobrevive a reinstalar) quedó MEDIDO sin EC2, con el freno visto morder al anular la guarda, y `[A-019]` murió del todo, ascendida a `[D-035]`: `caddy adapt` → 16000 de verdad, borde HTTP exacto (16000 pasa, 16001 → 413), retirando la salvedad de `T-054`. Dos arreglos de código nacidos de revisar el guion: `install.sh` leía el `.env` **después** de crear la carpeta de datos por defecto, fabricando el señuelo vacío que `[D-037]` existe para evitar — corregido y medido con el guion viejo como control rojo (`[D-038]`); y la precedencia `.env`/entorno no se invierte pero se hace audible con `config.value_origin` y un renglón de log nuevo, seis tests saboteados por los dos lados (`[D-039]`). `[L-025]` nueva: dos menciones muertas en código (`app/config.py`, `app/api.py:40-42`) describiendo una plataforma descartada en `[D-029]` hacía dos días. De 342 a **348** tests verdes, `data/` sin un solo cambio. Queda un contenedor Docker `teapp-test` encendido con uvicorn y Caddy dentro, sin borrar — decisión pendiente del usuario | 7 |
| S-024 | 2026-08-06 | Séptimo tramo del día, después del cierre que dejó `[S-023]`. `T-072` cerrada: el culpable era `measure_body.py`, la báscula de `T-054`, ejecutada esa misma tarde (2026-08-06 14:48:32 local) — se registró como `otronombrelargo`, practicó los 5 casos de `CASES` (`{"score": 5}`, `{"used": 5}`), y desvió `accounts.ACCOUNTS_FILE` a un temporal pero se olvidó de `USERS_DIR` y `QUOTA_DIR`: el aislamiento necesitaba tres desvíos y se acordó de uno. Eso explica la contradicción de `[A-020]` — la cuenta no aparecía en `accounts.json` porque ese fue el único archivo que sí se desvió. Segundo caso del mismo patrón: `probe-log.json`, del 2026-08-05. Arreglo estructural (`[D-037]`): la raíz de `data/` sale de `TEAPP_DATA_DIR`, ruta absoluta obligatoria, sin valor por defecto, carpeta que debe existir (la app no la crea), con una línea de log en `INFO` al arrancar. Tocó `app/config.py`, `app/tools.py`, `app/quota.py`, `app/accounts.py`, `app/api.py`, `create_account.py`, `main.py`, `tests/conftest.py`, `tests/no_data_writes.py`, `tests/check_no_data_writes.py`, más los tests de cada módulo y `tests/test_config.py` (nuevo). `.env.example`, `README.md` y `deploy/install.sh` (crea la carpeta y escribe la variable) al día. De 329 a **342** tests verdes: el freno se midió con sabotaje puesto y quitado, que reveló que un test medía otra cosa y se corrigió. Arranque comprobado con uvicorn real: `GET /` → 200, `/practice` sin sesión → 401, log con la ruta resuelta; sin la variable, el import de `app/api.py` se niega. `data/` sin tocar. `[A-020]` retirada (comprobada), `[A-021]` nueva (la tarjeta firmada sobrevive a su cuenta, medido no supuesto), `[D-037]` y `[L-023]` nuevas | 7 |
| S-023 | 2026-08-06 | Sexto tramo del día, después del cierre que dejó `[S-022]`. `T-071` cerrada: `app/tools.py` deja de congelar `USERS_DIR` en la firma de `score_file`/`read_score`/`add_point` (`users_dir: Path = USERS_DIR` → `Path \| None = None`, resuelto dentro, igual que `app/quota.py:139`); `conftest.py` gana un `monkeypatch.setattr(tools, "USERS_DIR", ...)` y un fixture autouse `no_data_writes_allowed`. Los tres maniquíes `autouse` que tapaban el marcador (`test_api.py`, `test_deploy_limits.py`, `test_english_tutor.py` — eran **tres**, no dos como decía `T-071` original) se borraron; los tests que dependían de `score == 7` pasan a `score == 1` (carpeta nueva por test). `tests/no_data_writes.py` (nuevo): portero al estilo `no_network.py`, huella `md5` del contenido de `data/` antes/después de cada test. `tests/check_no_data_writes.py` (nuevo): 6 controles fuera de `test_*.py`. Test nuevo `test_practice_writes_the_score_inside_the_temporary_folder` que caza un maniquí futuro que el portero no vería. Suite de 328 a **329** verdes. Sabotaje: quitar la línea del `conftest.py` pone `DataTouched` en 5 tests más el test del inquilino. `[D-036]`, `[A-020]`, `[L-021]`, `[L-022]` nuevas. `T-072` nueva: un camino fuera de pytest sigue escribiendo en `data/` real, con evidencia física (`[A-020]`) — no se mezcla con `T-071` | 7 |
| S-022 | 2026-08-06 | Quinto tramo del día, después del cierre que dejó `[S-021]`. `T-054` cerrada en la mitad que no necesita nube: la directiva `request_body { max_size 16KB }` ya estaba escrita en `deploy/Caddyfile.template` desde `T-063`; faltaba la báscula. Medido con la app real (`TestClient`, sin red): frase de 500 caracteres en cinco alfabetos, todas 200. Peor caso legítimo = 6016 bytes (emoji escapado `\uXXXX\uXXXX`, 12 bytes por carácter) — el criterio anterior ("no llegan a 2 KB") era falso por 3x. Corrección de una auditoría externa: en go-humanize `KB`=1000, no 1024 — el techo real es 16000, no 16384, margen 2,66x (`[A-019]`, leído en documentación, no medido con `caddy adapt`). `tests/test_deploy_limits.py` nuevo: 14 tests, primero de TEAPP que lee un archivo de `deploy/`, parseando el número del Caddyfile en vez de copiarlo. Suite de 314 a **328** verdes. Cinco sabotajes hechos, el más importante aportado por la auditoría (`MAX_SENTENCE_LENGTH` 500→5000, único que ataca el escenario que el test dice cazar). `[D-035]`, `[A-019]`, `[L-020]` nuevas. `T-071` nueva: el aislamiento de datos de los tests está duplicado en dos `fixture` locales, no en `conftest.py` — el marcador (`USERS_DIR`) no está cubierto por el `conftest.py` general | 7 |
| S-021 | 2026-08-06 | Cuarto tramo del día, después del cierre que dejó `[S-020]` (`cd20c4d`). Sesión de espera: el experimento de `[A-018]` no puede leerse aún (t=0 fue hoy mismo a las 15:29 UTC), así que se adelantó trabajo que no toca la nube. Leída entera la lista "ESTO NUNCA SE TOCA" de `T-068` — no cambió nada, ya estaba correcta. **`T-055` resuelta en su mitad de Python, y sin tocar `app/api.py`**: se midió con uvicorn 0.52.1 **real** (no `TestClient`, `[L-010]`) que `--proxy-headers` y `--forwarded-allow-ips 127.0.0.1` hacen exactamente lo que la tarea pedía — cuatro escenarios, incluido el suplantador, todos verdes; tabla en `[D-034]`. Las dos banderas se escriben **explícitas** en `deploy/teapp.service` aunque ya sean el valor por defecto, por el argumento de `[D-027]`. `[L-019]` nueva: el escenario del suplantador salió rojo y **el rojo era del montaje, no de uvicorn** — Windows pone `127.0.0.1` como origen aunque el destino sea `127.0.0.2`, así que el "atacante" entraba por la puerta de Caddy; de un sabotaje se verifica el montaje, no solo el resultado. `[A-014]` **encogida, no muerta**: medida la mitad de Python, siguen sin comprobar que Caddy escriba la cabecera y `T-060`. Revisión externa del tramo añadió: `T-060` recategorizada (ya no es "un clic", es la mitad que sostiene a la otra), y un aviso en `Caddyfile.template` de que `127.0.0.1` va literal y **no** `localhost` — que puede resolverse a `::1` y haría descartar la cabecera **en silencio**. En un segundo commit, `T-052`: cuatro tests nuevos para la cookie `Secure` —la rama por defecto, que es **producción**, no corría en ningún test—, cubriendo `_start_session` (registro y login) y el `delete_cookie` de `/logout`. Sabotaje doble: invertir el defecto pone los cuatro en rojo, y quitar el fixture también — se verificó el montaje, no solo el resultado. `[A-009]` encogida: muere con `T-051`, cuando un navegador de verdad guarde la cookie por `https://`. **De 310 a 314 tests** | 7 |
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

### [S-036] 2026-08-10 — Los dos prerrequisitos del paso 8 quedan resueltos; `[D-049]` fija el modelo de arranque

- **Paso:** 8 de 9. Decimonoveno tramo, después del cierre que dejó `[S-035]`.
  Sesión de decisión, verificación por SSH y planeación pura: **el único
  archivo del repo modificado es `_persistence/decisions.md`** — ningún
  archivo de `app/`, `tests/` ni `deploy/` tocado.
- **`T-075` CERRADA:** la API key de Anthropic vive en el `.env` LOCAL.
  Verificada **sin imprimirla**: empieza por `sk-ant-`, 108 caracteres, y
  `.env` está ignorado por git (`.gitignore:3`). Acción del usuario, sin
  cambio en el repo.
- **`T-056` CERRADA**, reportada según el traspaso de cierre — trabajo por
  SSH contra la EC2 de producción, no deja rastro en `git diff`:
  1. `TEAPP_REGISTRATION_OPEN = false` explícito en `/opt/teapp/.env`,
     permisos `600`, dueño `ubuntu`.
  2. `create_account.py` corre en el servidor — llamado sin argumentos,
     contestó su mensaje de uso y salió con código 1.
  - **De paso, un hallazgo que abre trabajo:** `ANTHROPIC_API_KEY` existe en
    el servidor pero está **vacía** — es el hueco que llena `T-078`.
- **`[D-049]` nueva (en el diff, revisada en el Paso 5 de este cierre, no
  escrita por `session-closer`):** el paso 8 arranca con `claude-opus-5` a
  `effort: "low"` — el modelo MÁS caro, no el más barato. El argumento que
  decide: arrancar por Haiku reintroduce dos sospechosos posibles (modelo o
  rúbrica) el día que se estrena el veredicto real, contra el argumento del
  roadmap de que el modelo debe quedar fuera del camino. `effort: "low"` es
  obligatorio porque Opus 5 piensa por defecto y ese pensamiento se cobra
  como salida y se come el timeout de 10 s de `[A-011]`. El descenso a
  Sonnet 5 y Haiku 4.5 pasa a ser trabajo **medido** del paso 9.
- **Plan de archivos de `T-076`, hecho y SIN EJECUTAR** — ningún archivo
  nuevo, ninguno eliminado: `app/tools.py` (borra `FAKE_VERDICT`, reescribe
  el cuerpo), `app/config.py` (entrada `ANTHROPIC_API_KEY`),
  `app/english_tutor.py`/`app/api.py` (solo comentarios/docstring),
  `tests/test_tools.py`, `tests/test_english_tutor.py`, `tests/test_api.py`,
  `requirements.txt`, `.env.example`, `deploy/install.sh`.
- ⚠️ **Hallazgo de camino:** `tests/no_network.py` bloquea la red en toda la
  suite (`C-001`) — los tests nuevos de `judge_grammar` tienen que inyectar
  un cliente falso, no pueden llamar a Claude de verdad.
- **Precisión sobre `T-077`:** "borrar el agente falso" solo borra media
  falsedad. `respond()` seguirá llamando a las tres herramientas siempre y
  en el mismo orden, porque `scope.md` no pide que el agente elija. El
  docstring de `app/english_tutor.py` se reescribe con precisión, no se
  borra sin más.
- **Verificado en este cierre:** `git status` mostraba un solo archivo
  modificado (`_persistence/decisions.md`); ningún `.env` en la lista.
  Paso 2b: `.js` compilado, al día (`compilar: 0`, `comparar: 0`) — no había
  ningún `.ts` tocado.
- **Siguiente paso concreto:** arrancar `T-076` — sustituir el cuerpo de
  `judge_grammar` por la llamada real a Claude, siguiendo el plan de
  archivos ya escrito. ⚠️ Sobre el estado de la máquina de producción: no se
  afirma aquí sin comprobarlo (`[L-038]`) — mirar el Paso 5b de
  `deploy/console_steps.md` antes de dar por hecho que está encendida o
  apagada.

### [S-035] 2026-08-10 — Se cruza al paso 8 con pendientes del 7 nombrados uno a uno

- **Paso:** 7 → 8. Decimoctavo tramo, después del cierre que dejó `[S-034]`.
  Sesión de decisión y documentación: **ningún archivo de `app/` ni `tests/`
  tocado, nada corrido en la consola de AWS** (ni instancia lanzada, ni
  subdominio creado, ni `install.sh` corrido). Todo lo de hoy está en el
  `git diff` de `_persistence/` y `deploy/console_steps.md`.
- **De dónde salió:** una objeción del usuario, no una revisión —
  *"sentimos que invertimos mucho tiempo en esta aplicación y no hemos
  podido avanzar al siguiente paso"*. La respuesta fue contar, no recordar
  (regla 6), sobre este mismo índice:

  | | sesiones | días |
  |---|---|---|
  | pasos 0 a 6 (siete pasos) | 12 (`S-001`…`S-012`) | 3 |
  | paso 7 (uno solo) | 22 (`S-013`…`S-034`) | 6 |

- 🔴 **Corrección dentro de la propia sesión:** horas antes, en este mismo
  chat, se afirmó que `T-069` frenaba el paso 8. Es falso — `[D-030]` mide
  "pronto" contra el cierre de la cuenta (`[C-006]`, 2027-02-06), no contra
  el paso 8. Lo único que de verdad bloqueaba era `T-056` (dos minutos).
- **`[D-047]` (primera decisión de la sesión):** el ensayo de reconstrucción
  de `T-069` se hace sobre una instancia **nueva**, dejando viva la de
  producción, con un **segundo subdominio** de DuckDNS
  (`teapp-rehearsal.duckdns.org`, sin Elastic IP) — `teapp.duckdns.org`
  resuelve a la Elastic IP de la máquina viva, así que reutilizar ese nombre
  en la máquina nueva hace fallar el certificado en `install.sh:378`.
  `deploy/console_steps.md` gana el **Paso 5c** con el guion completo (seis
  puntos: subdominio, lanzar, apuntar DNS, correr el guion, qué medir,
  borrarla). No hizo falta tocar una línea de `deploy/`: `TEAPP_DOMAIN` ya
  era una variable de entrada.
- **`[D-048]` (segunda decisión, corrige el error de arriba):** se cruza al
  paso 8 ahora, dejando abiertos `T-046`, `T-067`, `T-069` y `T-070` del
  paso 7 — cada uno con su motivo escrito, no en silencio. `T-056` se hace
  de camino. El argumento que decide: lo que corre es el calendario de
  `[C-006]` y los créditos de `[C-003]`, y hoy se gastan en infraestructura
  para una app cuyo corazón sigue siendo el maniquí del paso 1. `[D-047]`
  sigue VÁLIDA — queda anotada como **aplazada**, no anulada: el ensayo se
  hace igual, después del paso 8.
- **`[A-023]` nueva:** el precio de aplazar `T-069`, escrito aparte para
  que no viaje escondido dentro de `[D-048]`. El paso 8 va a tocar
  `deploy/` de verdad — la API key entra por el archivo de entorno, e
  `install.sh` tendrá que colocarla — así que lo que se ensaye en
  septiembre no será el `deploy/` de hoy. Fecha tope ≈ 2026-09-01 (cierre
  del primer ciclo de facturación, cuando `[A-018]` deja de estar ciega).
- **`[L-037]` nueva:** el andamio se volvió el trabajo. Ninguna sesión
  individual del paso 7 estuvo mal — el fallo es de suma, no de sumandos:
  cada cierre preguntaba "¿lo que hice hoy está bien hecho?" y ninguno
  "¿lo que llevo hecho me acerca a lo que vine a construir?". Lo detectó el
  usuario, no `_persistence/` ni ninguna auditoría externa.
- **Verificado en este cierre:** `git status` mostraba cuatro archivos
  modificados (`_persistence/assumptions.md`, `_persistence/decisions.md`,
  `_persistence/lessons.md`, `deploy/console_steps.md`); ningún `.env` en
  la lista. Ningún archivo de `app/` ni `tests/` tocado; suite no corrida
  hoy, sigue en 362 (última corrida conocida, del 09, sin cambios en tests
  hoy). Paso 2b: `.js` compilado, al día (`compilar: 0`, `comparar: 0`) —
  no había ningún `.ts` tocado.
- **Siguiente paso concreto:** arrancar el paso 8, empezando por `T-056`.
  ⚠️ **La máquina amanece APAGADA** — `[D-045]` la apaga sola a las 23:00
  UTC y el encendido es MANUAL a propósito, para que el olvido caiga del
  lado que no cobra. `T-056` necesita SSH: primero encenderla en la
  consola de AWS (Paso 5b de `deploy/console_steps.md`).
- 🔧 **Ampliación del mismo tramo, tras revisión de la sesión principal:**
  `tasks.md` tenía un hueco — el paso 8 solo traía `T-019` (una decisión de
  producto) y ninguna tarea para el trabajo real del paso, enchufar el
  modelo. Añadidas `T-075`…`T-079`: conseguir la API key de Anthropic
  (`.env` local, acción del usuario, primer gasto real), sustituir el
  cuerpo de `judge_grammar` por la llamada real a Claude con rúbrica
  (`app/tools.py:128`, firma ya definitiva), borrar `FAKE_VERDICT` y el
  agente falso, que `install.sh` coloque `ANTHROPIC_API_KEY` en el
  servidor (enlaza con `[A-023]`: es la pieza que hace que el `deploy/` de
  septiembre no sea el de hoy), y medir de verdad `[A-010]`/`[A-011]`
  (hoy son predicción). `T-019` deja de estar bloqueada, referenciando a
  `T-076`. Ninguna tarea inventada fuera de lo verificado en el repo
  (`app/tools.py`, `app/english_tutor.py`, `_context/scope.md`,
  `.env.example`).
- ⚠️ **La `siguiente acción` de arriba lleva DOS prerrequisitos nombrados,
  no escondidos:** encender la máquina y conseguir la API key. Ninguno de
  los dos está cumplido a este cierre.

### [S-030] 2026-08-08 — TEAPP desplegado en producción: Caddy, arranque automático, cortafuegos medido, primera cuenta, disco que persiste

- **Paso:** 7 de 9 — TEAPP responde en `https://teapp.duckdns.org`.
  Decimotercer tramo del día, después del cierre que dejó `[S-029]`.
- ⚠️ **Advertencia de origen, antes de leer nada más:** todo lo de esta
  entrada, salvo lo marcado aparte, se registra **según el traspaso de
  cierre de la sesión principal** — es trabajo en la EC2 (SSH, consola,
  `curl` contra el dominio real) y por su naturaleza **no deja rastro en
  `git diff`**. Lo único que el diff del día respalda directamente es
  `_persistence/assumptions.md` y `_persistence/constraints.md`.
- **Quedó funcionando (según el traspaso):**
  - **Primera conexión SSH del proyecto** y **primera corrida real de
    `deploy/install.sh` en una máquina de verdad** — hasta hoy solo se
    había corrido en contenedor (`[L-024]`).
  - `T-061`: Caddy sirviendo HTTPS. `200` con `ssl_verify_result=0` desde
    fuera, puerto 80 redirige con `308`. Certificado Let's Encrypt real,
    `CN=teapp.duckdns.org`, `Aug 8 16:55:35` → `Nov 6 16:55:34 2026`.
  - `T-062`: arranque automático. Reinicio real (`uptime -s`: `15:54:27`
    → `18:11:15`), `teapp` y `caddy` en `active` sin que nadie los
    encendiera, uvicorn escuchando SOLO en `127.0.0.1:8000`.
  - `T-060b`: cortafuegos medido, no solo escrito. Con Python escuchando
    de verdad en el 8000, la petición desde fuera dio **timeout** — ya no
    es el control ciego de `[L-020]`.
  - `T-064`: primera cuenta. `jorge` creada con `systemctl stop teapp`
    (para no violar `[A-002]`), contraseña generada en la máquina con
    `openssl rand`, nunca escrita en el repo ni pasada por argumento.
    Verificado desde fuera: `/login` → 200, `/me` con cookie →
    `{"user":"jorge"}`, sin cookie → 401, contraseña mala → 401. Solo se
    escribió `data/accounts.json`.
  - `T-065`: el disco persiste. Marcador de `jorge` a 3 puntos,
    `sudo systemctl reboot`, la frase siguiente devolvió `score = 4`.
- **Medido, pero NO cerrado del todo:**
  - `T-050` (llave estable): la MISMA cookie emitida antes del reinicio
    siguió valiendo después → la llave no se regeneró; `.env` en `600`,
    propiedad de `ubuntu`. Sigue 🔄: lo medido es el **reinicio**, y el
    criterio propio de la tarea pide un **redespliegue** (`install.sh`
    otra vez), que no se ha corrido.
  - `T-051` (cookie `Secure`): el servidor emite
    `Set-Cookie ... HttpOnly; Path=/; SameSite=lax; Secure` sobre HTTPS
    real. Falta la otra mitad — que la guarde un **navegador** de verdad;
    `curl` no es un navegador. Queda para el usuario.
  - `T-066` (dos dispositivos): sigue sin hacerse.
- **Registrado por la sesión principal antes de este cierre** (ya en el
  diff, revisado en el Paso 5, no escrito por `session-closer`):
  - `[C-007]` nueva en `constraints.md`: el repositorio de GitHub es
    **público** — verificado con `git clone` sin credenciales
    (`GIT_TERMINAL_PROMPT=0`). Ningún secreto ha entrado nunca; lo
    expuesto es `_persistence/`, `_context/` y `deploy/console_steps.md`.
  - `[A-018]` ampliada: `t=0` de la EC2 **MEDIDO** en la máquina
    (`uptime -s` → `2026-08-08 15:54:27 UTC`), corrigiendo una deducción
    previa que tomaba las 15:08 UTC por `t=0` — esa era la hora de leer
    el presupuesto, 46 min antes de lanzar.
  - `[A-017]` ampliada: tres episodios de `Could not resolve host` desde
    dos redes, **con corrección explícita** de que la causa está SIN
    resolver — el diagnóstico no reprodujo (16/16 correctas contra el
    resolutor local y `8.8.8.8`), y un episodio con el puerto 80
    resolviendo el mismo nombre en el mismo instante en que HTTPS no,
    señal contra la hipótesis DuckDNS. Exposición medida: certificado
    caduca 2026-11-06.
  - `[A-005]` encogida otra vez: el **reinicio** queda medido (`T-065`),
    el **redespliegue** —lo que su propio criterio pedía— sigue vivo.
- ⚠️ **Discrepancia con una revisión externa, anotada y no tapada:** dos
  afirmaciones dijeron que existe un archivo `PROGRESO.md` — una para dar
  por hecha `T-060b`, otra para decir que lo de `C-007` ya estaba anotado
  desde la sesión 41. **Ese archivo no existe** — el del proyecto es
  `_persistence/progress.md` — y ninguna de las dos afirmaciones estaba
  escrita en el repo antes de hoy. El hecho de `C-007` es correcto; la
  anotación previa que se le atribuía, no.
- **Verificado en este cierre:** `git status` mostraba dos archivos
  modificados (`_persistence/assumptions.md`, `_persistence/constraints.md`);
  ningún `.env` en la lista. Ningún archivo de `app/` ni `tests/` tocado;
  suite no corrida hoy, sigue en 351 (última corrida conocida, del 07).
  Paso 2b: `.js` compilado, al día (`compilar: 0`, `comparar: 0`) — no
  había ningún `.ts` tocado.
- **Siguiente paso concreto:** `T-051` necesita un navegador real entrando
  a `https://teapp.duckdns.org` — es del usuario. `T-050` se cierra con un
  redespliegue sobre la máquina ya viva, mirando que la sesión sobreviva.
  `T-066` (dos dispositivos) sigue pendiente. `T-067` (gasto real × 180)
  ya se puede leer con la EC2 encendida varios días.

### [S-029] 2026-08-08 — `T-059` cerrada del todo: la EC2 existe, quinta lectura de `[A-018]` cumple `[D-041]`, `D-043` decide la AMI

- **Paso:** 7 de 9 — la EC2 ya existe y está encendida. Duodécimo tramo del
  día, después del cierre que dejó `[S-028]`.
- **Quinta lectura de `[A-018]`, 15:08 UTC (~47,7 h desde `t=0`):** `Importe
  utilizado` sigue en 0,00, sin cambio en 3,9 h desde la cuarta lectura.
  `h1` sigue sin ocurrir. Se hizo por `[D-041]`, no por el experimento: ese
  orden queda cumplido con este dato — el campo se leyó primero, dijo 0,00,
  y `[D-041]` decía explícitamente "diga lo que diga ese campo". Con eso la
  segunda mitad de `T-059` quedó desbloqueada.
- **Revisión externa antes del primer clic, dos huecos corregidos en
  `deploy/console_steps.md` (commit `5075762`, ya en `origin`):**
  - El punto 5 del paso 3 decía *"Elastic IP: reservarla y asociarla"*,
    escrito cuando la IP no existía. Al partirse `T-059` el 06 se ejecutó
    solo reservar y el texto se quedó igual — seguirlo al pie de la letra
    habría alquilado una **segunda** dirección. Ahora dice solo asociar.
  - El paso del grupo de seguridad no estaba escrito en ninguna parte: el
    aviso del `launch-wizard` (22 abierto al mundo, grupo de `T-060a` sin
    usar) vivía solo en el chat. `[L-028]` nueva.
- **`T-059` reportada CERRADA DEL TODO**, cadena verificada eslabón a
  eslabón según el traspaso de cierre de la sesión principal (ver detalle
  en `_persistence/tasks.md`, entrada `[T-059]`): instancia `i-0faa249…`
  `t3.micro`, `Ubuntu Server 24.04 LTS`, grupo `teapp-sg` de `T-060a`
  realmente puesto, Elastic IP ya reservada asociada, `teapp.duckdns.org`
  resolviendo desde fuera, llave `teapp-key` guardada fuera del repo.
- **`[D-043]` nueva:** la AMI es `Ubuntu Server 24.04 LTS`, x86_64 — ni la
  26.04 (`install.sh` solo medido contra 24.04, `[L-024]`, queda sin medir
  si cambia) ni `Ubuntu Pro` (suscripción con cargo por hora, sin beneficio
  para una máquina que se cierra en seis meses).
- **Dos trampas del formulario de lanzamiento, medidas en pantalla y
  escritas en `console_steps.md` junto con `D-043` (AÚN SIN COMMITEAR al
  cierre de esta sesión):** el desplegable de AMI se recarga solo a la LTS
  más nueva (se eligió 24.04, el resumen final decía 26.04 — cazado leyendo
  el resumen entero antes de lanzar, `LM.15`); y cambiar la AMI reinicia el
  grupo de seguridad y los volúmenes — regla nueva: la AMI se elige PRIMERO
  y no se vuelve a tocar.
- **`T-060b` sigue sin hacerse, y no por falta de tiempo:** no hay nada
  escuchando en el 8000 todavía, así que un escaneo saldría cerrado igual
  con el cortafuegos abierto — sería `[L-020]` otra vez. Queda bloqueada por
  `T-062`, no por `T-059`.
- 🚨 **Desde el lanzamiento, la máquina está encendida y facturando por
  hora.** La cuenta tiene ahora dos fuentes de gasto (Elastic IP + EC2):
  `h1` y `h2 − h1` de `[A-018]` siguen midiéndose, pero la cuantía del
  importe deja de ser atribuible solo a la IP.
- ⚠️ **Discrepancia anotada, no tapada:** el diff de esta sesión solo
  respalda directamente `[D-043]` y las correcciones de
  `deploy/console_steps.md`. La cadena de verificación de la EC2 en la
  consola de AWS (grupo de seguridad, IP asociada, DNS, llave guardada) no
  puede dejar rastro en `git diff` por su propia naturaleza — se registra
  según el traspaso de cierre, con el detalle que trajo (IDs, direcciones,
  resultado de `nslookup`).
- **Verificado en este cierre:** ningún archivo de `app/` ni `tests/`
  tocado; la suite **no se corrió hoy** — sigue en 351, la última corrida
  conocida es del 2026-08-07, no declarada verificada hoy. Paso 2b: `.js`
  compilado, al día (`compilar: 0`, `comparar: 0`) — no había ningún `.ts`
  tocado.
- **Siguiente paso concreto:** entrar por SSH con `teapp-key` y correr
  `deploy/install.sh` — nunca se ha corrido en una máquina de verdad, solo
  en contenedor (`[L-024]`).

### [S-028] 2026-08-08 — Cuarta lectura de `[A-018]`: aparece el primer cargo, en un instrumento nuevo

- **Paso:** 7 de 9 — sigue sin haber instancia EC2. Undécimo tramo del día,
  después del cierre que dejó `[S-027]`. Sesión corta, de solo lectura: no se
  tocó ningún archivo de `app/`, `tests/` ni `deploy/`.
- **Quedó funcionando (leído, no medido con corrida):**
  - Cuarta lectura del experimento de `[A-018]`, 2026-08-08 11:10 UTC (~43,7 h
    desde `t=0`). Tres pantallas leídas el mismo minuto: *Facturas* de agosto
    en 0,00 US$ (irrelevante, nace al cerrar el mes); `Importe utilizado` del
    presupuesto sellado sigue en 0,00 US$; y **un widget no previsto en
    ninguna tabla** — `Resumen de Costos`, en la página de inicio de
    *Facturación y costos*, campo `Costo Acumulado Mensual` = **0,12 US$**.
  - **Mata la causa (b)** de la enmienda de `[D-040]` (nada absorbe el
    cargo — hay cargo visible) y **confirma y localiza la causa (a)**: el
    dato de coste sí existe, lo que falta es el refresco del presupuesto
    (el tramo 2, *8–12 h*). Primera vez que se observan los dos tramos en
    serie a la vez, en la misma pantalla partida en dos.
- **NO ocurrió (y no se tapa):**
  - 🚨 `A-018` **sigue sin cerrarse**: `Importe utilizado` sigue en 0,00, así
    que `h1` no ha ocurrido, la guardia de ≥12 h ni ha arrancado, y la alarma
    sigue sin habérsele visto morder.
  - 🚨 `[D-041]` sigue sellado, pero **su segunda mitad NO se ejecutó hoy**: la
    `t3.micro` no se lanzó ni se asoció la Elastic IP — el usuario cerró la
    sesión antes de llegar a esa parte. El motivo 1 de `[D-041]` (medir
    `t_cargo − t=0` sin mezclar dos fuentes de gasto) ya está cobrado con la
    lectura de hoy; el motivo 2 (no encender con la alarma sin habérsela
    visto morder) sigue vivo tal cual. La Elastic IP sigue reservada y
    ociosa, cobrando.
- **Registrado:** la sesión principal ya amplió `[A-018]` en
  `_persistence/assumptions.md` antes de este cierre (subsección "Cuarta
  lectura"), con la aritmética de lista (0,12 ÷ 0,005 ≈ 24 h facturadas
  contra ~43,7 h transcurridas) marcada como tal, no como corrida.
- **Verificado en este cierre:** `git status` mostraba un solo archivo
  modificado (`_persistence/assumptions.md`); 351 tests siguen siendo el
  número vigente, sin recorrer la suite porque no se tocó código. Paso 2b:
  `.js` compilado, al día (`compilar: 0`, `comparar: 0`) — no había ningún
  `.ts` tocado.
- **Siguiente paso concreto:** lanzar la segunda mitad de `T-059` (la EC2,
  con la Elastic IP ya reservada) — es la primera acción pendiente, quedó
  sin hacer hoy. En paralelo, seguir leyendo `[A-018]` hasta que `Importe
  utilizado` deje de ser 0,00.

### [S-027] 2026-08-07 — `T-055` medida entera en contenedor: Caddy SÍ escribe (y descarta la forja), guardián nuevo, EC2 pospuesta

- **Paso:** 7 de 9 — sigue sin haber instancia EC2. Décimo tramo del mismo día,
  después del cierre que dejó `[S-026]`.
- **Decisión sellada antes de tocar nada (`[D-041]`):** la segunda mitad de
  `T-059` —lanzar la `t3.micro` y asociarle la Elastic IP— NO se lanza hoy.
  Se lanza el **2026-08-08**, después de leer `Importe utilizado`, diga lo
  que diga ese campo — no es una condición, es un orden. Dos motivos: lanzar
  hoy mete una segunda fuente de gasto en la factura y mata la medida
  irrepetible `t_cargo − t=0`; y encender la EC2 con la alarma sin habérsele
  visto morder es `[LM.13]` exacto. La Elastic IP no se suelta — se asocia
  mañana, como parte de esa misma mitad.
- **Quedó funcionando (medido, en contenedor, sin EC2):**
  - **Caddy SÍ escribe `X-Forwarded-For`** con la dirección real. Medido con
    aparejo de **dos** contenedores (cliente `172.17.0.4` ≠ proxy
    `172.17.0.3`) — con uno solo el valor no distingue "la real" de "la
    inventada". Plantilla renderizada desde `deploy/Caddyfile.template`
    versionada, no desde estado acumulado de la caja.
  - **Y descarta la cabecera forjada**, hallazgo no pedido: quien manda
    `X-Forwarded-For: 9.9.9.9` llega al backend como `172.17.0.4`. Caddy
    reescribe, no añade, porque la plantilla no declara `trusted_proxies` —
    política documentada *"By default, no proxies are trusted"*.
  - **Cadena entera con TEAPP real detrás:** seis logins fallidos con seis
    orígenes falsos distintos, el freno de `/login` saltó igual, contra el
    origen real. Control rojo hecho: arrancar uvicorn con
    `--forwarded-allow-ips 203.0.113.5` (excluye loopback) → el log escribe
    `127.0.0.1`, todos en el mismo cubo — `[A-014]` en falso, a la vista.
  - ⚠️ **Límite escrito antes de medir, y se cumplió:** ese Caddy sirve por
    HTTP, así que `X-Forwarded-Proto` dice `http`. Medido el mecanismo, no
    el valor final. Siguen necesitando máquina: `T-061` (HTTPS real),
    `T-060b` (8000 cerrado desde fuera) y `T-066` (dos dispositivos).
- **`[L-027]` nueva:** el primer control que se intentó —arrancar uvicorn
  **sin** `--proxy-headers`, para verlo fallar— salió **ciego**, no rojo:
  esa bandera ya viene puesta por defecto en uvicorn 0.52.1, dato que
  `[D-034]` tenía escrito desde el 2026-08-06 y se olvidó al diseñar el
  control. El ciego fue el control, no la medida: un control ciego no da un
  falso negativo, da permiso para creerse el verde.
- **`[D-042]` nueva, a petición del usuario:** guardián en
  `tests/test_deploy_limits.py` que falla si `deploy/Caddyfile.template`
  declara `trusted_proxies`. Visto ROJO sobre la plantilla de verdad (se
  saboteó, falló solo ese test, se deshizo), rojo en las dos formas en que
  Caddy acepta la directiva (bloque global y dentro de `reverse_proxy`), y
  ciego a los comentarios que nombran la directiva para explicar por qué no
  está. Plantilla revalidada con Caddy 2.11.4 real tras el cambio: `Valid
  configuration`, salida 0.
- **De 348 a 351 tests verdes** (verificado en este cierre).
- **Correcciones al informe de inicio de esta sesión:** eran **348** tests
  antes del guardián, no 342; y la de hoy es la **tercera** lectura de
  `[A-018]` (commit `1c3118d`), no la segunda.
- **Registrado:** `[D-041]`, `[D-042]`, `[L-027]`, `[A-014]` encogida otra
  vez (queda una sola cosa sin comprobar: `T-060b`).
- **Verificado en este cierre:** 351 tests pasando (`python -m pytest`).
  Paso 2b: `.js` compilado, al día (`compilar: 0`, `comparar: 0`) — no había
  ningún `.ts` tocado.
- **Siguiente paso concreto:** releer `[A-018]` el 2026-08-08; si el criterio
  se cumple, lanzar la segunda mitad de `T-059` (orden ya sellado, no
  condicionado al número) y con la EC2 arriba avanzar `T-060b`, `T-061` y
  `T-066`.

### [S-026] 2026-08-07 — Segunda lectura de `A-018` (sigue sin concluir), enmienda sellada, `T-060a` hecha

- **Paso:** 7 de 9 — sigue sin haber instancia EC2. Noveno tramo del mismo día,
  después del cierre que dejó `[S-025]`.
- **Quedó funcionando (medido/registrado, sin código):**
  - Segunda lectura del experimento de `[A-018]`, ~23,1 h desde `t=0` (14:36
    UTC). **Sigue NO CONCLUYENTE.** `Facturas` resultó ser la ventana
    equivocada dos días seguidos — una factura nace al cerrar el mes. La
    lectura buena es el campo `Importe utilizado` del propio presupuesto,
    el mismo instrumento que la alarma: hoy 0,00 US$ con un `0.00%`
    calculado.
  - Resuelto gratis: `Importe previsto` = `-` — AWS no puede proyectar sin
    historial, la alerta de coste previsto no pudo disparar.
  - Corregido en caliente antes de cerrar: se iba a escribir que aplicaban
    las 750 h gratis de IPv4, y la documentación dice lo contrario — esas
    horas cubren direcciones **en uso**, la nuestra está ociosa y cobra
    (~0,115 US$ bruto, aritmética de lista de precios, no corrida). El
    disparador sigue siendo válido y el experimento sigue siendo falsable.
  - **Enmienda sellada** antes de la lectura del 2026-08-08: la FILA 3 de la
    tabla original (`cfba50a`) queda **ANULADA, no borrada** — nombraba una
    causa hoy desmentida. Guardia nueva sobre la FILA 2: "alarma rota" exige
    ≥12 h de silencio **después** de que el importe sea visible. El motivo de
    esa guardia se corrigió dos veces el mismo día — ni "24+12=36", ni "eso
    era doble conteo" (afirmaba de más: llamarlo doble conteo es afirmar que
    comparten reloj, el mismo dato declarado desconocido) — hasta quedar con
    un solo desconocido sin descartar ninguna rama. Se anotan dos horas,
    `h1` (importe visible) y `h2` (correo): `h2 − h1` decide el desconocido
    gratis, como segunda medición del experimento.
  - `T-060` partida en `T-060a`/`T-060b` (`LM.13`: tener el grupo creado no es
    tener el cortafuegos, es tenerlo escrito). **`T-060a` HECHA:** grupo de
    seguridad `teapp-sg` creado en `us-east-1`, VPC `default` (única
    ofrecida). Reglas leídas desde la ficha, no desde lo tecleado: `80/tcp` y
    `443/tcp` desde `0.0.0.0/0`, `22/tcp` desde una sola dirección `/32`, sin
    8000 y sin IPv6, salida intacta. El primer intento falló por el
    apóstrofo de "Let's" en una descripción de regla — AWS deshizo el grupo
    entero, no dejó uno a medias.
  - `deploy/console_steps.md` ampliado: por qué la salida se queda abierta a
    propósito, la VPC como el mismo tipo de trampa muda que la región, y el
    aviso del puerto 22 con la IP de casa cuando rote.
- **Registrado:** `[D-040]` (el criterio de lectura sellado hoy, no mañana),
  `[L-026]` (`T-068` es disciplina, no freno, y se degrada con la repetición).
- **Verificado en este cierre:** no hay tests que correr — sesión de consola
  de AWS y de documentación, no de código. Paso 2b: `.js` compilado, al día
  (`compilar: 0`, `comparar: 0`) — no había ningún `.ts` tocado.
- **Sin resolver, con dueño explícito del usuario:** dos menciones muertas de
  `[L-025]` en `app/config.py` y `app/api.py` — el usuario NO autorizó
  tocarlas hoy. El contenedor `teapp-test` sigue encendido.
- **Siguiente paso concreto:** releer `[A-018]` el 2026-08-08 con el criterio
  nuevo — que `Importe utilizado` deje de ser 0,00 — anotando `h1`. En
  paralelo, soltar o asociar la Elastic IP ociosa al terminar el experimento,
  y `T-060b` (escaneo desde fuera) sigue esperando la EC2 de `T-059`.

#### 🔻 Ampliada el 2026-08-07 — segundo tramo tras el cierre que dejó esta
entrada escrita antes de que ocurriera (`c0f0201`, `7630862`, ya en `origin`)

- **`install.sh` nunca ha ejecutado su sección 5, en ningún sitio.** Muere en
  la línea 223 (`systemctl: not found`, PID 1 del contenedor es `sleep`) —
  amplía `[L-024]` en vez de corregirlo. Dentro vivía `caddy validate`
  (línea 237), sin correr nunca ni en contenedor ni en EC2, que no existe.
- **`caddy validate` corrido a mano sobre `Caddyfile.template` renderizado,
  primera vez en la vida del proyecto:** `Valid configuration`, salida 0, sin
  `DOMAIN_PLACEHOLDER` sin sustituir. Directivas efectivas: `request_body
  { max_size 16KB }` y `reverse_proxy 127.0.0.1:8000`, más los redirects
  HTTP→HTTPS automáticos y el 443 con política TLS. Mide sintaxis, no
  comportamiento — `T-055` (mitad de Caddy) y `T-060b` lo siguen pidiendo con
  máquina.
- **Cayó una suposición sobre el contenedor:** no hay aparejo Caddy↔uvicorn
  ahí dentro. Su `/etc/caddy/Caddyfile` es el de fábrica, con `reverse_proxy`
  comentado — dos procesos sueltos levantados a mano, no un aparejo.
- **La receta del contenedor quedó escrita en `deploy/README.md`** — vivía
  solo en un scrollback: `docker run -d --name teapp-test ubuntu:24.04 sleep
  infinity`, sin puertos ni volúmenes, todo por `docker exec ... sh -c '...'`,
  con la trampa de rutas de Git Bash y el aviso de que un contenedor que ya
  corrió `install.sh` es un instrumento trucado.
- **`teapp-rig:latest` (1,05 GB):** imagen congelada desde `teapp-test` con
  `docker commit`, para no pagar el `apt-get` dos veces. Artefacto local, NO
  va a Git.
- **`T-055` reclasificada** (`tasks.md`, commit `7630862`): la mitad de Caddy
  ya no espera máquina — es gratis y se mide en contenedor. Límite escrito
  antes de medir: ese Caddy sirve por HTTP, así que `X-Forwarded-Proto` dirá
  `http` — mide el mecanismo, no el valor final. Regla de diseño: lo medido
  ahí debe colgar de entradas reproducibles (la plantilla versionada sí, el
  estado acumulado de la caja no).
- **Registrado:** `[L-024]` ampliada (no `[L-026]` nueva) — ver
  `_persistence/lessons.md`.
- ⚠️ **Sin artefacto en el repo, solo en el traspaso de cierre:** se reporta
  que se comprobó la longitud (no el valor) de `ANTHROPIC_API_KEY` dentro del
  contenedor `teapp-test` — vacía, longitud 0, igual que la escribe
  `install.sh:188` — y que el `.env` que produce el guion coincide con el que
  el guion dice que produce. Ningún archivo del diff lo registra; queda dicho
  aquí porque el `git diff` no puede confirmarlo ni desmentirlo.
- **Verificado en este cierre:** `git status` limpio, sin `ahead` — los dos
  commits de este tramo ya estaban subidos a `origin` antes de este cierre.
  Paso 2b: no había ningún `.ts` tocado (sesión de documentación y consola).

### [S-023] 2026-08-06 — `T-071` cerrada: el marcador se aísla en el origen, con portero

- **Paso:** 7 de 9 — sigue sin haber instancia EC2. Sexto tramo del mismo día,
  después del cierre que dejó `[S-022]`. `git status` al empezar: seis archivos
  modificados (`app/tools.py`, `tests/conftest.py`, `tests/test_api.py`,
  `tests/test_deploy_limits.py`, `tests/test_english_tutor.py`,
  `_persistence/assumptions.md|decisions.md|lessons.md`) y dos nuevos
  (`tests/no_data_writes.py`, `tests/check_no_data_writes.py`).
- **Punto de partida:** `score_file`, `read_score` y `add_point` en
  `app/tools.py` llevaban `users_dir: Path = USERS_DIR` como valor por
  defecto en la firma — congelado al **importar** el módulo. Un
  `monkeypatch.setattr(tools, "USERS_DIR", ...)` en `conftest.py` no cambiaba
  nada, así que se tapaba con un maniquí `autouse` que sustituía `add_point`
  entera y devolvía siempre `7` sin tocar disco.
- **Quedó funcionando (medido):**
  - Las tres funciones resuelven la carpeta **dentro**, igual que ya hacía
    `app/quota.py:139` — `directory = USERS_DIR if users_dir is None else users_dir`.
  - `conftest.py` desvía `tools.USERS_DIR` a `tmp_path / "users"`, junto a los
    desvíos ya existentes de cuentas y cuota.
  - Se borraron **tres** maniquíes `autouse` idénticos
    (`monkeypatch.setattr(english_tutor, "add_point", lambda user: 7)`), no
    dos como decía el texto original de `T-071`: estaban en `test_api.py`,
    `test_deploy_limits.py` y `test_english_tutor.py`.
  - `tests/no_data_writes.py` (nuevo): portero al estilo `no_network.py`.
    Huella `md5` del **contenido** de `data/` antes y después de cada test
    (fixture autouse `no_data_writes_allowed` en `conftest.py`).
  - `tests/check_no_data_writes.py` (nuevo): 6 controles, fuera de
    `test_*.py` como `check_no_network.py` — no corren en la suite normal,
    demuestran que el portero muerde.
  - Test nuevo `test_practice_writes_the_score_inside_the_temporary_folder`
    en `test_api.py`: exige ver el archivo del marcador aparecer en la
    carpeta temporal. Caza un maniquí futuro que el portero no vería —el
    portero solo detecta escritura, y un maniquí hace que nadie escriba nada.
  - Ajustes derivados: el marcador esperado pasa de `7` a `1` en
    `test_api.py` y `test_english_tutor.py` (cada test estrena carpeta);
    `BROKEN_SCORE_PATH` (constante calculada al importar, rancia desde que
    `conftest.py` empezó a desviar el marcador) se convierte en el valor que
    devuelve el fixture `broken_score`; `test_the_api_gives_the_same_result_as_the_terminal`
    congela `add_point` localmente porque llama dos veces y el marcador real
    avanzaría entre ellas.
  - Suite de 328 a **329** tests verdes (verificado en este cierre).
  - Sabotaje: quitar la línea del `setattr` en `conftest.py` pone
    `DataTouched: cambio el contenido de users\juan.json` en 5 tests, más el
    test del inquilino en rojo. Los 6 controles de `check_no_data_writes.py`,
    verdes.
- **Registrado:** `[D-036]` (la decisión y las dos alternativas descartadas),
  `[A-020]` (el camino de escritura fuera de pytest, con la tabla de fechas),
  `[L-021]` (el titular que contradecía su propia salvedad) y `[L-022]` (un
  `md5` no dice "todo igual", dice "los bytes, iguales" — perdida la prueba
  del `mtime` al restaurar `data/` con `cp -r`).
- **`T-072` nueva:** investigar y cerrar el camino que escribe en `data/`
  real sin pasar por `conftest.py` — el portero de `T-071` vive dentro de
  pytest y no lo ve ni lo verá. Evidencia física en `[A-020]`. No se mezcla
  con `T-071`.
- **Verificado en este cierre:** 329 tests pasando (`python -m pytest`).
  Paso 2b: `.js` compilado, al día (`compilar: 0`, `comparar: 0`) — no había
  ningún `.ts` tocado.
- **Siguiente paso concreto:** el mismo de `[S-022]` — esperar el resultado
  del experimento de `[A-018]` (factura + bandeja) antes de tocar la nube de
  nuevo. En paralelo, `T-072` puede avanzar sin tocar la nube.

### [S-022] 2026-08-06 — `T-054` cerrada en su mitad medible: la báscula que faltaba

- **Paso:** 7 de 9 — sigue sin haber instancia EC2. Quinto tramo del mismo día,
  después del cierre que dejó `[S-021]`. `git status` al empezar: cuatro
  archivos modificados (`_persistence/assumptions.md`, `decisions.md`,
  `lessons.md`, `deploy/Caddyfile.template`) y un archivo nuevo
  (`tests/test_deploy_limits.py`).
- **Punto de partida:** la directiva `request_body { max_size 16KB }` ya
  estaba escrita en `deploy/Caddyfile.template` desde `T-063` (2026-08-05).
  Lo que faltaba de `T-054` no era el freno: era la báscula que probara que
  el número no rompe el uso normal.
- **Quedó funcionando (medido):**
  - Medición con la app real, vía `TestClient` (sin red — `[C-001]`): frase
    de 500 caracteres (el máximo de `MAX_SENTENCE_LENGTH`) en cinco
    alfabetos — inglés, español con tildes, chino, emoji en UTF-8 crudo, y
    emoji escapado `\uXXXX\uXXXX`. Los cinco contestan **200**.
  - **Peor caso legítimo: 6016 bytes**, no los "menos de 2 KB" que decía el
    comentario anterior — un emoji escapado en JSON cuesta 12 bytes ASCII por
    carácter, y `MAX_SENTENCE_LENGTH` acota caracteres, no bytes. El criterio
    viejo era falso por 3x.
  - Corrección aportada por una auditoría externa: en go-humanize —lo que usa
    Caddy para leer estos tamaños— `KB` = 1000, no 1024. El techo real de
    `max_size 16KB` es **16000**, no 16384. Contra 6016, quedan 2,66x de
    margen.
  - `tests/test_deploy_limits.py` (nuevo, 14 tests): **el primer test de
    TEAPP que lee un archivo de `deploy/`**. Parsea el número de
    `max_size` directamente del Caddyfile — no lo copia — para que no exista
    una tercera copia del mismo número (Caddyfile, test, máquina) capaz de
    desalinearse. Suite de 314 a **328** tests verdes.
  - Cinco sabotajes hechos: cuatro del montaje (unidad `KiB` vs `KB`,
    directiva comentada, conversor sin aplicar la unidad, `max_size 4KB`) y
    uno del escenario que el test dice cazar — subir `MAX_SENTENCE_LENGTH` de
    500 a 5000, que puso 4 tests en rojo. Este último lo aportó la auditoría,
    no quien escribió el test — es el único de los cinco que ataca la
    dirección real del control, no solo su instrumento.
  - `deploy/Caddyfile.template`: solo cambió el comentario (de "por criterio"
    a "medido", con la tabla de pesos). Cero cambios de lógica.
- **Lo que sigue faltando, y por qué se acepta cerrar igual:** que Caddy
  devuelva el 413 de verdad contra ese número — eso necesita el binario de
  Caddy, y llega gratis con `T-061`. La deuda del entero real de `16KB`
  (vía `caddy adapt`, en vez del leído en documentación) queda anotada en
  `[A-019]`.
- **Registrado:** `[D-035]` (el número medido y el test que cruza a
  `deploy/`), `[A-019]` (16KB son 16000, leído no medido), `[L-020]` (el
  modo de fallo característico del proyecto: un verde producido por algo
  distinto de lo que el verde afirma — con su propia tabla de tres casos en
  dos sesiones).
- **`T-071` nueva:** el aislamiento de datos de los tests no vive en
  `tests/conftest.py` — vive duplicado en dos `fixture` locales
  (`test_api.py` y `test_deploy_limits.py`). `conftest.py` desvía cuentas y
  cuota, pero no el marcador (`USERS_DIR`). La trampa sigue armada: el
  próximo archivo de tests que llame a `/practice` puede escribir en
  `data/` real sin que `git status` lo note (`data/` está en
  `.gitignore`) — es la misma familia de fallo que `[L-020]`.
- **Verificado en este cierre:** 328 tests pasando (`python -m pytest`).
  Paso 2b: `.js` compilado, al día (`compilar: 0`, `comparar: 0`) — no había
  ningún `.ts` tocado.
- **Siguiente paso concreto:** el mismo de `[S-021]` — esperar el resultado
  del experimento de `[A-018]` (factura + bandeja) antes de tocar la nube de
  nuevo.

### [S-021] 2026-08-06 — `T-055` medida con uvicorn real: la mitad de Python, sin tocar `app/api.py`

- **Paso:** 7 de 9 — sigue sin haber instancia EC2. Cuarto tramo del mismo día,
  después del cierre que dejó `[S-020]` (commit `cd20c4d`). `git status` al
  empezar: árbol limpio.
- **Por qué esta sesión existe:** el experimento de `[A-018]` **no se puede leer
  todavía**. Su t=0 fue hoy a las 15:29 UTC y el dato de facturación llega con
  ~24 h de retraso. Mirarlo hoy no diría nada, así que se adelantó trabajo que no
  toca la nube ni gasta el reloj de los 6 meses.
- **Lo primero, que no cambió nada:** se leyó entera la lista "ESTO NUNCA SE
  TOCA" de `T-068` (`deploy/console_steps.md`, líneas 14-39). Las siete puertas
  siguen bien escritas y las cinco de la ❓ siguen tratadas como 💀. No hizo
  falta corregir nada — se registra **porque leerla es el requisito previo de
  `T-059`**, no porque haya producido cambios.
- **Quedó funcionando (medido):**
  - **`T-055`, mitad de Python.** `_request_origin` (`app/api.py:394`) **no se
    toca**. La resuelve uvicorn con `--proxy-headers` y
    `--forwarded-allow-ips 127.0.0.1`, que en 0.52.1 ya vienen puestas.
  - 🔑 **Se midió con uvicorn de verdad, no con `TestClient`** — es exactamente
    la trampa de `[L-010]`. Se levantó el servidor como lo levanta
    `teapp.service`, se le mandaron logins fallidos hasta provocar el 429 y se
    leyó qué origen escribía el renglón `Demasiados intentos`. Cada escenario
    con servidor recién arrancado, porque el contador de `login_guard` vive en
    memoria (`[D-026]`) y no se puede vaciar de otra forma.
  - Cuatro escenarios, los cuatro verdes. **La tabla vive en `[D-034]` y solo
    ahí** — no se copia aquí a propósito (`[L-018]`).
  - El escenario que importaba y no era obvio: uvicorn recorre la cadena de
    `X-Forwarded-For` **al revés**, y como Caddy **añade** la dirección real al
    final, la cabecera que traiga quien ataca queda delante y se descarta sola.
    Leído en `uvicorn/middleware/proxy_headers.py`, no supuesto.
- **El susto, que es lo que más vale de este tramo:**
  - El escenario del suplantador salió **rojo**. El rojo era **del montaje, no
    de uvicorn**: se había fingido ser un extraño hablando por `127.0.0.2`, y
    Windows pone `127.0.0.1` como dirección de origen aunque el destino sea
    `127.0.0.2` (comprobado aparte, con dos sockets). La petición llegaba
    **disfrazada de Caddy**. Se rehízo con la IP de la red local y salió verde.
  - `[L-019]` nueva. 🔑 **Lo grave es la simetría:** aquí el error se delató
    porque el resultado pedía explicación; el mismo montaje en cualquiera de los
    otros tres escenarios habría salido **verde por la razón falsa**, y `T-055`
    se habría cerrado sobre una medición que no midió nada.
- **Registrado:**
  - `[D-034]`: el origen real lo resuelve uvicorn, no `app/api.py`, y las
    banderas se escriben **explícitas** aunque ya sean el valor por defecto —
    mismo argumento que `[D-027]` con `TEAPP_REGISTRATION_OPEN`. Un valor por
    defecto no es una decisión: es una coincidencia que hoy conviene.
  - `[A-014]` **encogida, no retirada.** Lo medido es la mitad de Python. Siguen
    sin comprobar dos cosas que no son código: que **Caddy escriba** de verdad la
    cabecera, y que el **8000 esté cerrado** (`T-060`). `T-066` sigue siendo la
    corrida que lo cierra.
- **Lo que trajo la revisión externa del tramo** (cuatro faltas, ninguna
  corrección de lo medido):
  1. `tasks.md` contradecía a `decisions.md`: `T-055` en 🔲 mientras `[D-034]`
     la daba por resuelta. Pasada a ✅ en índice y entrada, **con lo que quedó
     fuera escrito al lado** — la marca honesta no es la ✅, es la letra pequeña.
  2. `T-060` **recategorizada**: deja de ser "un clic de la consola" y pasa a ser
     **la mitad que sostiene a la otra**. Sin ella, `--forwarded-allow-ips` no
     protege de nada.
  3. 🚨 **El acoplamiento mudo entre `teapp.service` y el `Caddyfile`.** Los dos
     dependen de que la dirección sea `127.0.0.1` **literal**. El día que alguien
     escriba `localhost:8000` —que parece lo mismo y se lee mejor— puede
     resolverse a `::1`, uvicorn no se fiaría de esa dirección y descartaría la
     cabecera **en silencio**: todo el mundo al mismo cubo, sin un solo error que
     lo explique. Es el fallo mudo de `[L-032]` (antes `[A-008]`) con otro disfraz. Queda avisado
     junto al `reverse_proxy`.
  4. Este tramo estaba **sin commitear** — cuatro archivos modificados y cero
     commits. Mismo principio que sellar la predicción de `[A-018]` antes del
     clic: lo que no está en Git no ocurrió.
- **Comprobado:** 310 tests pasando. `bash -n deploy/install.sh` correcto.
  `install.sh` copia el `.service` **literal** (línea 167), así que el cambio del
  `ExecStart` sí llega a la máquina.
- **Ninguna línea de lógica tocada.** De `app/api.py` solo cambió el docstring de
  `_request_origin` — y esa fue **una quinta copia obsoleta encontrada aplicando
  `[L-018]`**, la peor de todas porque vivía en el código: seguía diciendo *"ahí
  hay que leer la dirección real de la cabecera"*, en presente y como pendiente.
  Quien lo leyera mañana implementaría a mano justo el arreglo peligroso que
  `[D-034]` descartó. Ahora dice lo contrario y explica por qué.
- **Segundo commit del tramo — `T-052`, y esto sí es código:** cuatro tests
  nuevos en `tests/test_api.py` ("El interruptor de la cookie segura"), gemelos
  del bloque del registro. **De 310 a 314 tests.**
  - Dos ajustes sobre el enunciado, los dos hacia un test más fiel: el fixture
    **borra** la variable en vez de ponerla a `"true"` (así mide el defecto de
    verdad, no una copia nuestra), y se mira la cabecera `Set-Cookie` **en
    crudo** en vez del tarro del cliente, que descarta la cookie con razón al
    hablar por `http://`.
  - 📌 **Corrección de un dato de la revisión:** los dos sitios de
    `cookie_secure()` no son "registro y login". Son `_start_session`
    —compartido por registro y login— y el **`delete_cookie` de `/logout`**.
    Los tres caminos quedan cubiertos igualmente, y el de `/logout` era el que
    de verdad se podía olvidar.
  - **Sabotaje doble, aplicando `[L-019]` recién escrita:** invertido el valor
    por defecto de `config.py`, los cuatro en rojo (miden lo que dicen); quitado
    el fixture a uno, rojo también (el fixture es quien hace el trabajo). Se
    verificó **el montaje, no solo el resultado**.
  - `[A-009]` **encogida**: la rama ya tiene testigo. Sigue viva porque nadie ha
    visto un navegador de verdad guardar esa cookie por `https://` — muere con
    `T-051`.
- ⚠️ **Sigue sin correrse nada de `deploy/`** — no hay máquina EC2. Y la Elastic
  IP sigue reservada y suelta, cobrando por existir.

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
  puede alcanzarse. Es `[LM.13]` en versión alarma: verde porque **no existe
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
