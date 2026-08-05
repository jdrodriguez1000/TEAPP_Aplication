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
| T-019 | Decidir si el marcador cuenta frases practicadas o correctas (ver `assumptions.md` A-001) | 🔲 | 8 |
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
| T-050 | Que `TEAPP_SECRET_KEY` exista en la nube y sea **estable entre despliegues**: si cambia, todas las sesiones mueren de golpe sin ningún error que lo explique (`A-008`). Con `D-029` ya tiene dueño: un archivo de entorno en la máquina, con permisos cerrados, generado **una sola vez**. 🚨 La dificultad no es ponerla — es que el guion de instalación **no la sobrescriba** al volver a correr. Ver entrada | 🔲 | 7 |
| T-051 | Poner `TEAPP_COOKIE_SECURE=true` en la nube. En local va en `false` porque el navegador descarta en silencio una cookie `Secure` sobre `http://localhost`. Con `D-029` es **una línea** en el mismo archivo de entorno: toda su dificultad era el certificado, y la resuelve Caddy con el nombre de DuckDNS (`T-058`). Se comprueba entrando por `https://` y mirando que la cookie lleve `Secure` — con eso muere también `A-009` | 🔲 | 7 |
| T-052 | Escribir un test que anule el `autouse` de `tests/conftest.py`, ponga `TEAPP_COOKIE_SECURE=true` y compruebe que `set_cookie` recibe `secure=True`: la rama por defecto no corre en ningún test hoy (`A-009`) | 🔲 | 7 |
| T-053 | Tope de intentos fallidos contra `/login`, contado por origen de la petición, no por persona. Hecho en `app/login_guard.py`: contador en memoria con barrido, 429 con `Retry-After` y motivo al log. Visto con uvicorn real (`D-026`) | ✅ | 7 |
| T-054 | Tope de tamaño de cuerpo en el servidor de delante (el reverse proxy de la nube). `MAX_SENTENCE_LENGTH` frena el gasto, no la subida: un cuerpo de 5 MB se sube entero antes del 422 (`C-002`). Con `D-029` deja de ser fantasma: **una directiva en la configuración de Caddy** (`T-061`). El tamaño sale de los 500 caracteres más el JSON y las cabeceras — unos pocos KB. ⚠️ Número por criterio, no por medida: hay que probar que una frase legítima de 500 pasa | 🔲 | 7 |
| T-055 | Que el origen que lee `_request_origin` sea el REAL cuando haya un proxy delante. Hoy es `request.client.host`; tras el despliegue será la dirección del proxy y el freno de `/login` dejaría fuera a todo el mundo a la vez (`A-014`). ⚠️ Leer `X-Forwarded-For` **sin** proxy de confianza delante es peor que no tener freno: la cabecera la escribe cualquiera. 🔑 **La garantía NO viene de que el proxy sea nuestro: viene de que nadie más pueda hablar con FastAPI.** Ver entrada | 🔲 | 7 |
| T-056 | Decidir y poner `TEAPP_REGISTRATION_OPEN` en la nube. Por defecto vale `false`, que es lo que se quiere (`D-027`), pero **conviene ponerlo explícito**: un ajuste de seguridad que depende de que nadie lo escriba es un ajuste que alguien abre 'un momentito'. Y comprobar que `create_account.py` corre en la plataforma: sin él no hay forma de crear la primera cuenta allí — ver `T-064` | 🔲 | 7 |
| T-057 | **Abrir la cuenta de AWS, y la alarma de facturación como PRIMER clic.** Arranca el reloj de 6 meses (`C-003`) y esa ventana **no vuelve nunca** (`C-006`), así que no se abre hasta tener todo lo demás decidido. 🚨 **Umbral: CUALQUIER cargo distinto de cero**, no una cifra alta — el primer cargo no nulo significa que ya se cruzó al plan de pago (`C-005`). ⚠️ Verificar de paso cuánto retraso llevan los datos de facturación. **Se registra con un alias `+aws` del correo personal y se activa MFA en el root en el mismo acto** (`D-031`) — el valor literal del correo no va al repo, que es público | 🔲 | 7 |
| T-058 | Sacar un nombre gratuito en DuckDNS (`teapp.duckdns.org`). 🚨 **Sin él no hay HTTPS**: Let's Encrypt se niega por política a emitir para `compute.amazonaws.com`, y sin certificado la cookie de sesión no viaja y no entra nadie (`D-029`) | 🔲 | 7 |
| T-059 | Lanzar la instancia EC2 **pequeña** (`t3.micro`) con una **IP fija** (Elastic IP) asociada, y apuntar el nombre de DuckDNS a esa IP. La IP de una EC2 cambia al apagar y encender; si el nombre deja de resolver, se cae el HTTPS y con él la sesión. ⚠️ El tamaño de la máquina es decisión de presupuesto, no técnica (`C-003`) | 🔲 | 7 |
| T-060 | Cortafuegos (grupo de seguridad) abierto **solo** en 80 y 443. Es la mitad de `T-055` que no está en el código: sin esto, cualquiera puede saltarse el proxy y hablarle a uvicorn de tú a tú | 🔲 | 7 |
| T-061 | Instalar y configurar **Caddy**: HTTPS automático contra el nombre de `T-058`, proxy hacia `127.0.0.1`, y el tope de cuerpo de `T-054`. Se eligió Caddy sobre nginx porque saca y renueva el certificado solo, y `T-051` lo necesita sí o sí (`D-029`) | 🔲 | 7 |
| T-062 | Arranque automático de uvicorn en la máquina, **atado a `127.0.0.1`** y leyendo el archivo de entorno. Que sobreviva a un reinicio sin que nadie entre a encenderlo a mano | 🔲 | 7 |
| T-063 | Carpeta `deploy/` en el repo: guion de instalación, configuración de Caddy y arranque automático. Más un documento con **los clics que no se pueden escribir**, en orden. Lo exige `C-004`: la cuenta se va a cerrar, y lo que solo exista porque se hizo a mano se pierde. ⚠️ **Sin Terraform** — sería la sexta cosa nueva, PI-2. Hecha: `deploy/console_steps.md`, `install.sh`, `teapp.service`, `Caddyfile.template`, `README.md`. Revisada dos veces el 2026-08-05: `install.sh` pasó de un solo `is-active` a tres comprobaciones (`L-017`), y `console_steps.md` ganó la comprobación real de DuckDNS (`A-017`). ⚠️ **Nada de esto se ha corrido nunca** — no hay máquina; `bash -n install.sh` sin errores es lo único verificado | ✅ | 7 |
| T-064 | Subir TEAPP y crear la primera cuenta con `create_account.py` en la máquina. `data/` no va a Git, así que arranca **sin ninguna cuenta**. ⚠️ Con el servidor **parado**: el script y el servidor a la vez son dos procesos escribiendo `data/`, y el candado no los ve (`A-002`) | 🔲 | 7 |
| T-065 | Comprobar `A-005` de verdad: sumar puntos, **reiniciar la máquina**, y mirar el marcador. Elegir un disco que persiste no es medirlo — hasta esta corrida es una promesa de la documentación | 🔲 | 7 |
| T-066 | Comprobar `A-014` resuelto: entrar desde dos dispositivos distintos y mirar qué dirección escribe el log en `Demasiados intentos`. Si es la misma para los dos, `T-055` no quedó hecha | 🔲 | 7 |
| T-067 | Comprobar `A-015` con el panel de facturación a los pocos días: gasto diario real × 180 contra los $200. Es la única corrida que vale — hoy el presupuesto es aritmética de lista de precios. Si no cabe, vuelve la pieza que apaga la máquina sola | 🔲 | 7 |
| T-068 | Lista de **"ESTO NUNCA SE TOCA"** en el documento de clics de `deploy/`, con los nombres escritos. 🚨 Cruzan al plan de pago **sin pedir confirmación** y **no tienen vuelta atrás** (`C-005`). No son botones que se vayan a necesitar: son botones con los que uno **se cruza**. Hecha en dos mitades: `A-016` se cerró leyendo tres fuentes de AWS (FAQ, Términos, facturación) — la lista de tres estaba INCOMPLETA, son **siete** puertas, no tres (`L-016`); y la lista de siete quedó escrita en `deploy/console_steps.md`, con las cinco desconocidas marcadas ❓ y tratadas como si evaporaran (denegar por defecto) | ✅ | 7 |
| T-069 | 🚨 **Ensayo de reconstrucción, y va PRONTO — no al final.** Con TEAPP arriba y funcionando: borrar la máquina y levantarla otra vez **solo desde `deploy/`**. Es la única corrida que demuestra `C-004`; hasta entonces "está todo escrito" es una afirmación sin medir (`D-030`). Cuesta céntimos y deja cinco meses de margen para arreglar lo que falte | 🔲 | 7 |
| T-070 | **Cierre planeado del paso 7:** bajar TEAPP con fecha en el calendario, antes de que AWS cierre la cuenta sola, verificando otra vez que `deploy/` lo levanta. Cuesta lo mismo que no hacer nada — 🔑 la diferencia es que **un cierre planeado se aprende y uno automático solo se sufre** (`D-030`). 📌 La cuenta es desechable; `deploy/` no | 🔲 | 7 |

⚠️ T-031 y T-032 son el trabajo central del paso 2 y se hicieron **antes** que
T-021…T-029, aunque lleven número mayor. Los números de T-021 en adelante venían
ya puestos en la revisión externa que los encontró, y se respetaron para que las
referencias no mintieran.

⚠️ **T-037 lleva paso 3 a propósito**, aunque se haga después: es **deuda del
paso 3**, no trabajo del 6. La columna dice de dónde viene la tarea, no cuándo
toca hacerla.

---

## Entradas

### [T-055] El origen real detrás del proxy

- **Estado:** 🔲 pendiente
- 🔑 **La corrección que hay que respetar al escribirla.** El primer argumento
  fue *"sé quién escribe `X-Forwarded-For` porque el proxy es mío"*, y **es
  falso**. Ser dueño del proxy no impide que alguien hable con FastAPI **por otro
  lado** y escriba la cabecera que quiera. La garantía viene de que **nadie más
  pueda alcanzar a FastAPI**, y son **dos cosas juntas**:
  1. **uvicorn atado a `127.0.0.1`**, no a todas las direcciones (`T-062`).
  2. **el cortafuegos abierto solo en 80 y 443** (`T-060`).
  ⚠️ **Sin las dos no hay certeza, hay costumbre.** Con una sola, el freno de
  `/login` se convierte en el ataque: quien lo intenta cambia de origen en cada
  intento y no se frena nunca.
- **Pista buena: puede que no haya que tocar código.** Uvicorn trae una opción
  para leer las cabeceras del proxy y sustituir el origen él mismo, diciéndole de
  qué dirección se fía. Si funciona, `_request_origin` se queda como está y
  `A-014` se cierra **sin tocar `app/api.py`**.
  🚨 **El nombre exacto de la opción se consulta en la documentación de uvicorn el
  día que se haga** — no se escribe de memoria (regla 6).
- **Cómo se sabe que quedó hecha:** `T-066`.

### [T-050] La llave de firma, estable entre despliegues

- **Estado:** 🔲 pendiente
- **Dónde vive:** un archivo de variables de entorno **en la máquina**, con
  permisos cerrados, que lee el arranque automático (`T-062`). No en Git, no en
  un servicio aparte — en EC2 es un archivo y ya (`D-029`).
- 🚨 **La dificultad no es ponerla: es que el guion no la pise.** Un guion de
  instalación que genere la llave **cada vez que corre** produce exactamente el
  fallo de `A-008` — todas las sesiones muertas de golpe, todo el mundo fuera, y
  **ni un error en el log que lo explique**. El síntoma lleva derecho a sospechar
  del navegador o de las cookies, que es donde no está el problema.
- **Entonces la tarea es:** generar la llave **solo si el archivo no existe**, y
  que volver a correr el guion de `T-063` sea inofensivo.
- **Cómo se comprueba:** entrar, correr el guion de instalación otra vez,
  recargar la página. **Si sigue dentro, la deuda está pagada.**

<!-- Solo las tareas que necesitan detalle. Las que se entienden en una línea
     se quedan en el índice y no bajan aquí. Formato:

### [T-001] <título corto>

- **Estado:** 🔲 / 🔄 / ✅
- **Dónde quedó:** <solo si está a medias: en qué punto exacto>
- **Notas:** <lo que haga falta para retomarla sin releer nada>

-->
