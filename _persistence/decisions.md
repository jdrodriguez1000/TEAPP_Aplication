# Decisiones — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [D-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

| id | fecha | qué se decidió | toca |
|---|---|---|---|
| D-055 | 2026-08-10 | 🧾 **Si se devuelve la cuota lo dice `answer.usage`, no la forma de `content`.** Corrige la mitad (2) de `[D-054]`, del mismo día, tras una segunda auditoría externa. `[D-054]` decidía con un **proxy**: `content` vacío ⇒ no se facturó. 🚨 **Y el proxy tenía un agujero comprobado en la documentación de Anthropic el 2026-08-10 (regla 6): sin streaming —que es como llama `judge_grammar`— un rechazo a MITAD omite el parcial.** Esa respuesta llega con `content` vacío y `stop_reason="refusal"`, **calcada por fuera** al rechazo gratis, pero con los tokens ya pagados: el proxy devolvía cuota justo en el caso que `[D-051]` manda cobrar. 🔑 **El instrumento trae su propio contador y la pregunta se le hace a él:** `usage.input_tokens` / `usage.output_tokens` responden *¿esto costó dinero?* literalmente, en vez de inferirlo de una forma. `stop_reason` sale de la decisión y se queda solo en el mensaje de error. 📌 **Dos respuestas indistinguibles por su forma con decisión contraria** — eso es exactamente lo que un proxy no puede hacer y un contador sí; lo vigila `test_a_billed_refusal_with_no_partial_still_charges`, verificado en ROJO por sabotaje (el proxy devolvía `False`). ⚠️ Los dos campos son la factura entera **porque el proyecto no usa cache**; con cache habría que sumar los tokens de cache | `app/tools.py`, `tests/fake_tutor.py`, `tests/test_tools.py`, `[D-051]`, `[D-054]`, `T-076`, regla 3, regla 6 |
| D-054 | 2026-08-10 | 📌 **Su mitad (2) queda revisada por `[D-055]`: el discriminador ya no es `content` vacío, es `usage`.** ⏱️ **El cliente de Anthropic lleva `timeout=8.0`, y la cuota se devuelve cuando el rechazo llega SIN contenido.** Dos arreglos que salen de una auditoría externa, los dos comprobados en la documentación del SDK el mismo día (regla 6). **(1) El reloj que faltaba.** El timeout por defecto del cliente de Python son **diez minutos** — sesenta veces el presupuesto de `[A-011]`. 🚨 Y el aviso estaba escrito **por nosotros** en `app/api.py:130` desde el 4 de agosto: *"en el paso 8 la llamada al modelo necesita SU PROPIO timeout"*. `[D-053]` quitó los reintentos razonando tres veces sobre esos 10 s, y **el reloj al que se ajustaba nunca se puso**: intento único con 600 s. 🔑 Son **dos frenos que no se sustituyen** — el de `api.py` libera a quien pregunta; este libera al hilo. Sin el segundo, a los 10 s llega el 504 y el hilo sigue secuestrado hasta diez minutos: con Anthropic atascado los hilos se acumulan y el servidor deja de atender **sin que haya fallado nada**, que es literalmente la frase con la que abre ese bloque. ⚠️ **8.0 es ESTIMACIÓN sin corrida detrás**: va por debajo de los 10 s a propósito, mismo motivo que `MAX_RETRIES = 0` —que el primero en rendirse sea el cliente, para que llegue el error de verdad—; el riesgo aceptado es que Opus 5 tarde más y falle todo, riesgo que `[A-011]` ya tenía y que esto hace **visible** en vez de mudo. Se mide en `T-079`. **(2) El rechazo que se cobraba de más.** La rama del veredicto vacío mandaba `request_sent=True` **siempre**, juntando dos causas que `[D-051]` cobra distinto: cortarse contra `MAX_TOKENS` (sí gastó) y el rechazo del clasificador de seguridad (**cero tokens: ni entrada, ni salida, ni cuota** — documentado). 🔑 **El discriminador NO es solo `stop_reason`**, y aquí se corrige al auditor: un rechazo *a mitad* sí factura lo generado, así que se exige además **`content` vacío**, que es exactamente el caso documentado como gratis. En cualquier otro se cobra — denegar por defecto (regla 3) aplicado al dinero. 📌 Misma forma que el hallazgo del que salió bien parado el día anterior (`APITimeoutError` heredando de `APIConnectionError`): dos causas por la misma puerta, y una devolvía cuota mal — cazada en los `except` y escapada doce líneas más abajo | `app/tools.py`, `app/api.py`, `[A-011]`, `[D-051]`, `[D-053]`, `T-076`, `T-079`, regla 3, regla 6 |
| D-053 | 2026-08-10 | ⏱️ **El cliente de Anthropic se construye con `max_retries=0`: los reintentos los manda `api.py`, no el SDK.** Hallazgo de la documentación leída hoy: el SDK reintenta **dos veces por su cuenta** ante 429 y 500, con esperas crecientes. 🚨 **Tres intentos no caben en los 10 s de `[A-011]`**, así que el síntoma visible sería el 504 del timeout con el error de verdad —llave mala, saturación— **escondido detrás**: se diagnosticaría un problema de lentitud donde hay un problema de credenciales. 🔑 **El criterio general: el reloj tiene un solo dueño.** `api.py:673` ya decide cuánto se espera y qué pasa al agotarse; un segundo temporizador dentro del SDK no coordina con el primero, solo lo consume. ⚖️ **Precio aceptado:** un 429 aislado que el SDK habría absorbido en silencio ahora llega como error. Es lo correcto — con `[D-051]` ese caso devuelve la cuota, así que no le cuesta nada a quien practica. 📌 Si algún día se quieren reintentos, se escriben en `api.py`, donde vive el presupuesto de tiempo | `app/tools.py`, `app/api.py`, `[A-011]`, `[D-051]`, `T-076`, `T-079` |
| D-052 | 2026-08-10 | 🔌 **`judge_grammar` gana un parámetro opcional `client=None` — se amplía la firma que `T-076` había declarado definitiva.** Decisión del usuario, con la tensión puesta encima de la mesa antes de escribir: `T-076` dice *"la firma ya es la definitiva"* (`judge_grammar(sentence: str) -> str`), y esto la amplía. **Contra:** dejarla intacta y desviar el cliente por otro camino (variable de módulo, parche del entorno). 🔑 **El argumento que decide es que la casa ya tiene esta forma y por esta misma razón:** `score_file(name, users_dir=None)` y `read_score(name, users_dir=None)` llevan un parámetro opcional resuelto **dentro** de la función, no en la firma — es `[D-036]`, y sin él los tests no podían desviar el marcador. Aquí el problema es idéntico: `tests/no_network.py` cierra la red en TODA la suite (`[C-001]`), así que un test **no puede** llamar a Claude; tiene que inyectar un cliente falso por alguna puerta. ✅ **Y no viola PI-2**, aunque lo parezca: no es configurabilidad que nadie pidió, es lo único que hace la función comprobable — sin ella, `T-076` no se puede terminar según PI-4. 📌 **Ningún código existente se rompe:** `respond()` la sigue llamando con un solo argumento. 🚨 **El cliente por defecto se construye DENTRO, nunca en la firma** — un `client=Anthropic()` en la firma se evaluaría una sola vez al importar y congelaría la llave de aquel momento, que es exactamente el defecto que `[D-036]` vino a matar | `app/tools.py`, `tests/test_tools.py`, `T-076`, `[D-036]`, `[C-001]`, PI-2, PI-4 |
| D-051 | 2026-08-10 | ⚖️ **La cuota se devuelve PARTIDA cuando falla Claude: se devuelve si la petición nunca salió, se cobra si llegó a salir.** Cierra la pregunta que `[D-050]` dejó abierta. **Contra:** devolver siempre —era la respuesta inicial del usuario, y es la intuitiva: si no hubo veredicto, no hubo práctica— y contra no devolver nunca, que es lo que `app/quota.py:249` dice hoy por escrito. 🔑 **El argumento que decide no es nuevo, es el del paso 6 aplicado a otro sitio:** la cuota no cuenta veredictos recibidos, cuenta **dinero gastado** (`spend`: *"lo que se cobra es haber intentado, porque intentar es lo que cuesta dinero"*), y `refund` avisa de que *"devolver de más sería peor que no devolver: regalaría cuota"*. Devolver siempre abre un agujero real: con Claude saturado, reintentar cuesta tokens de entrada en cada intento y **ninguno gastaría cuota** — el freno de facturación dejaría de frenar justo el día que va mal, que es cuando existe. 🪞 **Y la forma ya estaba inventada en la casa:** `api.py:673` no decide a ojo si el timeout se cobra, se lo pregunta a `future.cancel()`; esto es la misma pregunta hecha al SDK en vez de al pool. 📐 **Dónde cae la línea:** *nunca salió* → falta la llave, llave inválida, conexión rechazada, límite de peticiones — cero tokens, se devuelve; *sí salió* → error del servidor de Anthropic, saturación, corte después de mandar la frase — los tokens de entrada ya se pagaron, se cobra. ⚠️ **Los nombres exactos de las excepciones del SDK NO están comprobados todavía** (regla 6): las familias son las de arriba, pero qué clase corresponde a cada una se fija leyendo la documentación de `anthropic` al escribir `T-076`, no de memoria. 🚨 **Y ante la duda se COBRA, no se devuelve** — es denegar por defecto (regla 3) aplicado al dinero: equivocarse cobrando le cuesta a alguien una práctica de 20; equivocarse devolviendo deja el freno abierto. 📌 `T-076` gana un tercer test: que el fallo "nunca salió" devuelva y el fallo "sí salió" no | `app/tools.py`, `app/api.py`, `app/quota.py`, `T-076`, `[D-050]`, `[D-023]`, `[A-010]`, `[L-013]`, regla 3, regla 6 |
| D-050 | 2026-08-10 | 🚫 **Si Claude no contesta, la práctica NO suma punto: mensaje de error y marcador quieto.** Decisión del usuario, con la pregunta puesta antes de escribir una línea de `T-076`. **Contra:** sumar el punto igual —defendible, porque `[A-001]` dice que el marcador cuenta frases **practicadas**, no correctas, y la frase se escribió—, y contra devolver un veredicto de repuesto ("no pudimos revisarla, sigue practicando"). 🔑 **El veredicto de repuesto se descarta por lo que ES, no por lo que dice:** sería `FAKE_VERDICT` volviendo a entrar por la puerta de atrás el mismo día que se le echa por la de delante, y con el agravante de que ahora sí habría un modelo detrás — o sea, un fallo **mudo**, que es la familia que este proyecto persigue desde `[L-032]`. 🔑 **Y el punto no se suma porque `[A-001]` deja de cubrir el caso:** "practicada" supone que hubo tutor; una petición que no obtuvo veredicto no es una práctica floja, es una práctica que no ocurrió. La propia `[A-001]` avisa de que el contrato de `judge_grammar` cambia en el paso 8. ✅ **Hallazgo: el código YA lo cumple, por el orden.** En `app/english_tutor.py:53` los argumentos de `TutorReply(...)` se evalúan en el orden escrito —`count_words`, `judge_grammar`, `add_point`—, así que una excepción en el juez corta antes de tocar el marcador; y `app/api.py:708` ya traduce cualquier `Exception` a un 500 con mensaje. 🚨 **Consecuencia que cambia el trabajo de `T-076`: ese orden deja de ser cosmético y pasa a ser lo que sostiene esta decisión.** Reordenar las tres líneas —algo que hoy parece inocuo— cobraría el punto de una práctica sin veredicto **sin romper ningún test**. Se vigila con un test propio, mismo criterio que `[D-042]` con `trusted_proxies`. ❓ **Lo que esta decisión NO resuelve, escrito para no darlo por zanjado:** la cuota del día ya se gastó antes de llamar al tutor (`app/api.py:607`), así que hoy un fallo de Claude cuesta una práctica de las 20. `[D-023]` y el timeout de `api.py:673` sí distinguen "nunca empezó" (se devuelve) de "ya corría" (se cobra); para el fallo del modelo esa distinción está sin decidir | `app/tools.py`, `app/english_tutor.py`, `app/api.py`, `T-076`, `[A-001]`, `[A-010]`, `[D-023]`, `[D-042]`, paso 8 |
| D-049 | 2026-08-10 | 🎯 **El paso 8 arranca con `claude-opus-5` y `effort: "low"` — el modelo MÁS caro, no el más barato — y el descenso a Sonnet 5 y a Haiku 4.5 se convierte en trabajo medido del paso 9.** Propuesta del usuario contra la mía, que era arrancar por Haiku 4.5 apoyándome en la regla 5. 🔑 **El argumento que gana es el del roadmap, un nivel más adentro:** el agente es falso hasta hoy porque *"el modelo es la única pieza que no responde igual dos veces"* y sacarlo del camino deja al sospechoso solo. Arrancar por Haiku reintroduce esa ambigüedad justo cuando se estrena la rúbrica — un veredicto malo tendría **dos** culpables posibles, la rúbrica o el modelo, y averiguar cuál obligaría a probar Opus igual, más tarde. Con Opus, un veredicto malo solo puede acusar a la rúbrica. 💰 **Y la regla 5 muerde menos de lo que parecía, porque muerde con VOLUMEN y en desarrollo no hay volumen.** ⚠️ Estimación **sin corrida detrás** (regla 6), suponiendo ~400 tokens de entrada y ~100 de salida: ~$0,0045 por práctica con Opus 5 contra ~$0,0009 con Haiku 4.5 — unos **$0,90 contra $0,18** en doscientas prácticas de prueba. Menos de un dólar por quitar una variable de la investigación. Los números reales se miden en `T-079`. 🚨 **`effort: "low"` NO es un adorno de ahorro, es lo que hace viable la decisión:** Claude Opus 5 **piensa por defecto** —cambio reciente respecto de Opus 4.8— y esos tokens de razonamiento se cobran **como salida, a $25 el millón** y consumen reloj; sin acotarlos, la estimación se multiplica y el pensamiento **se come el timeout de 10 s de `[A-011]`**, convirtiendo veredictos correctos en peticiones perdidas. Se descarta apagar el pensamiento del todo (`thinking: {type: "disabled"}`): la documentación de Anthropic registra que en Opus 5 se le escapan etiquetas `<thinking>` dentro de la respuesta visible, y ese texto llegaría al navegador. 🧭 **El paso 9 hereda un trabajo concreto, no una intención:** con evals y rúbrica montados, bajar a Sonnet 5 y a Haiku 4.5 deja de ser adivinanza y pasa a ser medición — que es la regla 6 aplicada al pie de la letra. ⚠️ **Trampa anotada de antemano para ese descenso:** una rúbrica escrita contra un modelo fuerte tiende a ser corta, porque se da por hecho lo que ese modelo rellena solo; la documentación de Anthropic avisa de que un prompt afinado para un modelo hay que reafinarlo para otro. Así que *"Haiku falló"* solo vale como conclusión **después** de reintentar con la rúbrica ampliada — con la rúbrica tal cual, `modelo` y `rúbrica` vuelven a ser dos variables a la vez. 📌 Cambiar de modelo después es una línea: el resto del proyecto solo ve `judge_grammar(sentence) -> str` | `app/tools.py`, `requirements.txt`, paso 8, paso 9, `T-076`, `T-079`, `[A-010]`, `[A-011]`, regla 5, regla 6 |
| D-048 | 2026-08-10 | 🚦 **Se pasa al paso 8 con cuatro tareas del paso 7 abiertas (`T-046`, `T-067`, `T-069`, `T-070`), y eso NO es abandonarlas: es reordenarlas.** Sale de una objeción del usuario, no de una revisión — *"sentimos que invertimos mucho tiempo y no avanzamos"*. 📊 **Contada, no recordada** (regla 6), en `progress.md`: pasos 0–6 = **12 sesiones / 3 días**; paso 7 solo = **22 sesiones / 6 días**. Un paso costó casi el doble que los otros siete juntos. 🔴 **Y corrige un error mío de esta misma sesión: dije que `T-069` frenaba el paso 8, y es FALSO.** `[D-030]` pide el ensayo "pronto", pero *pronto* está medido **contra el cierre de la cuenta** (2027-02-06, `[C-006]`), no contra el paso 8 — que no toca `deploy/` para arrancar. Lo único que de verdad bloqueaba era `T-056`, de dos minutos. 🔑 **El argumento que decide es de recurso escaso, y apunta al revés de lo que parecía:** lo que corre es el calendario de `[C-006]` y los créditos de `[C-003]`, y **hoy se están gastando en infraestructura para una app cuyo corazón es el maniquí del paso 1** — hay HTTPS, identidad, cuota y apagado automático encima de una función que devuelve siempre lo mismo. Cada día de pulido del paso 7 compra robustez para algo que todavía no hace lo que existe para hacer. ⚖️ **Contra, y es real:** `deploy/` sin ensayar es una promesa (`[C-004]`), y `[D-030]` avisa de que enterarse tarde es enterarse sin margen. Se acepta a sabiendas, y por eso **`T-069` no se cancela ni se despriorizaza en silencio**: se le pone dueño de calendario (antes del cierre del primer ciclo, ~2026-09-01) y queda escrita `[A-023]`, que es el precio de aplazarla. 📌 **`T-056` se hace de camino** — dos minutos, y es lo único que sí bloqueaba. 📌 `T-067` no la bloquea nadie de este lado: espera a que AWS enseñe el dato. 🧭 **Regla que queda:** un paso se puede dejar con pendientes, pero **los pendientes se nombran uno a uno con su motivo**; lo que no se puede es cruzar de paso sin saber qué se dejó atrás — eso no es avanzar, es perder la cuenta | paso 7, paso 8, `T-046`, `T-056`, `T-067`, `T-069`, `T-070`, `[D-030]`, `[D-047]`, `[A-023]`, `[L-037]`, `[C-003]`, `[C-004]`, `[C-006]` |
| D-047 | 2026-08-10 | 🔻 **APLAZADA el mismo día por `[D-048]`: la decisión sigue VÁLIDA, lo que cambia es CUÁNDO** — el ensayo se hace después del paso 8, no antes. **El ensayo de reconstrucción de `T-069` se hace sobre una instancia NUEVA, con la de producción viva — y con un SEGUNDO subdominio de DuckDNS, no con el de producción.** 🔑 La segunda mitad no es un detalle de comodidad: es lo que hace posible la primera. `teapp.duckdns.org` resuelve a la Elastic IP de la máquina viva, así que una segunda instancia con ese mismo `TEAPP_DOMAIN` **no puede sacar certificado** —Let's Encrypt va a comprobar el nombre y llama a la máquina vieja— y `install.sh` se para en la sección 5 (`install.sh:378`). Se saca `teapp-rehearsal.duckdns.org` (DuckDNS regala varios, gratis) apuntando a la IP de la nueva. ✅ **No se toca una línea de `deploy/`**: el nombre ya era una variable de entrada (`TEAPP_DOMAIN`), y eso mismo es un resultado del ensayo — el guion no tenía el dominio incrustado. **Contra: borrar la de producción**, que es lo que `[D-030]` describe literalmente. Se descarta porque `[D-030]` compra **margen de calendario**, y ese margen se consigue igual sin apagar lo que hoy funciona; borrar primero convierte cada fallo del ensayo en una caída de producción, que es exactamente el apuro del que `[D-030]` quería escapar. 📌 **La instancia de ensayo NO lleva Elastic IP:** la IP fija existe para que el nombre siga resolviendo entre apagados, y esta máquina vive una vez y muere — su IPv4 pública normal basta, y es una tarifa menos. ⚠️ **Precio aceptado, y no es cero:** con `[C-003]` la EC2 consume créditos (ya no hay 750 h gratis), así que mientras las dos máquinas convivan el gasto por horas de instancia va al doble. La cuantía **no está medida** y se acota apagando la de ensayo en cuanto termine. 🚨 **Se borra la instancia de ensayo al acabar, el mismo día** — una máquina de usar y tirar que sobreviva a su ensayo es gasto puro, y su nombre en la consola no dice que sobra. ⚖️ Lo que este ensayo NO mide y se anota antes de correrlo: la Elastic IP asociada y el nombre de producción, porque los dos se quedan donde están | `T-069`, `T-070`, `[D-030]`, `[A-022]`, `[C-003]`, `deploy/install.sh`, `deploy/console_steps.md` |
| D-046 | 2026-08-09 | **La pieza de apagado de `[D-045]` es un TEMPORIZADOR DE SYSTEMD, no una entrada de `cron`.** Dos archivos en `deploy/`: `teapp-shutdown.service` (qué hacer) y `teapp-shutdown.timer` (cuándo), instalados por `install.sh` para que sobrevivan al redespliegue y no dependan de que nadie los teclee (`C-004`). **Contra `cron`**, que era la opción más corta y por eso la primera candidata (PI-2): 🔑 **`cron` interpreta la hora en la zona horaria de la MÁQUINA**, un ajuste que vive fuera de este repo y que nadie vuelve a mirar — el día que cambie, el apagado se muda de hora **sin un solo error**. `OnCalendar` acepta la zona escrita dentro (`23:00:00 UTC`), así que la hora **viaja con la pieza** y `[D-045]` deja de depender de algo invisible. Se acepta el coste: dos archivos en vez de uno. ⚖️ Y se descarta el argumento de "systemd porque ya lo usamos": `teapp.service` existe, pero eso es familiaridad, no un motivo — el motivo es la zona horaria. 🚨 **`Persistent=false`, escrito explícito aunque ya sea el valor por defecto.** `Persistent=true` recupera disparos perdidos, y aquí la máquina se pierde el de las 23:00 **todas las noches a propósito**: encenderla a las 07:00 la apagaría en la cara de quien la encendió, con un síntoma que parece *"no arranca bien"* y no señala a este archivo. 🚨 **La orden NO lleva sección `[Install]` y `install.sh` NO la arranca** — un `systemctl start` sobre ella apagaría la máquina **a mitad de la instalación**. 🛡️ Los cuatro modos de fallo son **mudos** (la app funciona igual con la pieza rota), así que se vigilan con tests y no con comentarios — `tests/test_deploy_shutdown.py`, mismo criterio que `[D-042]`. Es el **tercer** test que cruza a `deploy/`. 351 → **360**. ⚠️ **Lo que NO está medido:** los archivos no se han cargado nunca en un systemd de verdad — no hay Linux en la máquina de trabajo. Se cierra en la máquina real, con `T-074` | `deploy/teapp-shutdown.{service,timer}`, `deploy/install.sh`, `tests/test_deploy_shutdown.py`, `[D-045]`, `T-073`, `T-074` |
| D-045 | 2026-08-09 | **La máquina no vive de noche. Ventana de uso 07:00–18:00 Colombia = 12:00–23:00 UTC; fuera de ella, apagada.** Arranca **hoy 2026-08-09 a las 23:00 UTC** — 11 h encendida, 13 h apagada. 🔁 **Reabre `[D-029]`, que descartó la pieza que apaga la máquina sola** apoyándose en la holgura de `[A-015]` (*"del orden de $50 de $200"*, aritmética de lista **nunca corrida**): hoy hay dinero medido en pantalla y el argumento ya no se sostiene solo. ⚙️ **Reparto asimétrico a propósito: el apagado es automático desde dentro de la máquina; el encendido es manual.** 🔑 El olvido tiene que caer del lado que **no** cobra — se olvida encender y no pasa nada, se olvida apagar y corre el reloj. 🔴 **Corregida en el momento: la versión de hace diez minutos decía "no arranca hasta que suene la alarma de `[A-018]`", y el motivo era FALSO** — se le atribuyó a `[A-018]` un daño que es de `[T-067]`. Lo que le queda a `[A-018]` son **relojes** (`h1`, `h2 − h1`), y no dependen de que la máquina esté viva: los 0,37 US$ ya están bancados y la Elastic IP cobra igual de noche. La cuantía dejó de ser atribuible el **08 a las 15:54 UTC**, no hoy. 🎁 **Y la ventana le REGALA algo a `[A-018]`:** las 23:00 y las 12:00 UTC pasan a ser **dos lecturas ancladas** del presupuesto que **acotan `h1`** — el correo se fecha solo, `h1` no. ⏱️ La hora del primer apagado es el nuevo **`t=0` de horas-encendida**. 📌 **`[T-067]` se mide BAJO esta ventana, no antes:** proyectar 180 días desde una máquina de 24 h sería proyectar un régimen que no existe. 🧪 El primer `stop`/`start` **se mide** —marcador vivo, 200 sin tocar nada, certificado sin reemitir—: `T-065` cubrió el **reinicio**, que no es lo mismo. ⚠️ **Apagar NO lleva el gasto a cero:** la Elastic IP y el volumen cobran igual; lo único que se ahorra son las horas de instancia, y **cuántas son no está medido**. 🚨 **"Detener", nunca "Terminar"** — y el mismo par existe como **ajuste** (*comportamiento de apagado iniciado por la instancia*: `stop` o `terminate`), donde **no hay ningún humano leyendo el menú**: si estuviera en `terminate`, la pieza automática **destruye instancia y disco la primera noche que funcione, por funcionar bien**. Por defecto es `stop`, pero *"probablemente"* no es *"comprobado"* → ✅ **LEÍDO EN PANTALLA el 2026-08-09: `Detener`.** Condición dura cumplida, la pieza se puede escribir. 📌 Vive en `Acciones` → `Configuración de la instancia` → **`Cambiar comportamiento de CIERRE`** (la consola en español no dice "apagado"), y **no** en la pestaña *Detalles*. 🌙 Y como la pieza **no existe esta noche**, el estreno se cubre con un disparo único (`sudo shutdown -P 23:00`), que sobrevive al redespliegue de `T-050` por ser del sistema y no de la app. 🚨 **`-P` y NO `-h`:** la documentación de AWS dice que `halt` **no** dispara el comportamiento —*"only places the CPU into a HLT state while the instance continues to run"*—, o sea máquina muerta por dentro y **viva para la factura**, con un fallo **mudo** (desde fuera se parece a estar detenida; la diferencia solo se ve en `running`/`stopped` o en la factura). Por eso el primer apagado se hace **con alguien mirando la consola**, no a las 23:00 dormidos — si no, el primer apagado depende de la memoria de alguien a las 18:00, que es como murió `[D-041]`. ⛔ Deja caducada `[D-044]` | `[D-029]`, `[D-044]`, `[A-015]`, `[A-018]`, `[T-067]`, `T-065`, `[C-003]` |
| D-044 | 2026-08-08 | ⛔ **CADUCADA el 2026-08-09 — la reemplaza `[D-045]`.** **La EC2 se queda ENCENDIDA esta noche; no se apaga al cerrar la sesión.** Decidido con la pregunta puesta encima de la mesa, no por inercia. **Contra:** apagarla ahorra las horas de instancia, y la regla 5 dice que minimizar factura manda. **A favor, y es lo que pesó:** ⚠️ apagar **no lleva el gasto a cero** —el volumen sigue existiendo y la Elastic IP vuelve a estar **ociosa**, que es exactamente lo que generó los 0,12 US$ de `[A-018]` sin ninguna máquina encendida—; y 🔑 **encender/apagar rompe la aritmética del único experimento abierto**: con la máquina continua, horas facturadas = horas transcurridas y `[A-018]` se divide sola; en cuanto haya tramos hay que llevarlos a mano, que es el error de las 15:08 multiplicado. Mañana hay tres tareas que **exigen** la máquina viva (`T-051` en navegador, redespliegue de `[A-005]` → hoy `[L-032]`, `T-066`). 📌 **Vigencia declarada: UNA noche.** Si mañana no se toca, la decisión caduca y se reevalúa — para varios días sin usarla, apagar gana | `[A-018]`, `[A-005]`, `T-051`, `T-066`, `[C-003]` |
| D-043 | 2026-08-08 | **La AMI es `Ubuntu Server 24.04 LTS`, x86_64 — ni la nueva ni la Pro.** El desplegable ofrecía cuatro: Server y Pro, 24.04 y 26.04. **Contra la 26.04:** `deploy/install.sh` tiene **una sola corrida en su vida**, en contenedor **Ubuntu 24.04** (`[L-024]`), y es toda la evidencia de que funciona — 🔑 cambiar de versión no lo rompe, **lo deja sin medir**, y el fallo aparecería en la máquina de verdad mezclado con el primer despliegue (nombres de paquete, repositorio de Caddy, Python del sistema). Estrenar SO es un experimento aparte y hoy ya hay uno abierto (`[A-018]`). 🚨 **Contra la Pro:** es una **suscripción de pago** con cargo **por hora** encima del de la instancia, y no aporta nada a una máquina que se cierra en seis meses; ❓ la cifra del recargo no se comprobó en pantalla y **la decisión no depende de ella** (cualquier importe > 0 basta si el beneficio es cero). ⚠️ **Lo peligroso es el nombre, no el precio:** "Pro" se lee como *"la versión buena"* y convive en la misma lista que la gratuita, sin un solo aviso — misma familia que `launch-wizard`. 📌 En 5 meses, saltar de versión = volver a correr `install.sh` **en un contenedor** de la nueva, no probarlo en la nube | `deploy/console_steps.md`, `T-059`, `[L-024]` |
| D-042 | 2026-08-07 | **La ausencia de `trusted_proxies` en el Caddyfile pasa a estar VIGILADA por un test, no solo explicada en un comentario.** Es lo que sostiene el hallazgo del día: Caddy descarta el `X-Forwarded-For` forjado **solo** porque no hay ningún proxy declarado de confianza. 🚨 Añadir esa directiva —y hay motivos plausibles para quererla: una CDN delante, una receta copiada— convierte el freno de `/login` en el ataque, **sin un solo error en ningún log**. 🔑 Se vigila con un test y no con un comentario porque el modo de fallo es **mudo**: un comentario solo protege a quien lo lee, y quien copia una receta de internet no lo lee. **Es el segundo test que cruza a `deploy/`**, y por la misma razón que el primero (`[D-035]`): acoplamiento real entre dos archivos que no se conocen, invisible desde Python. **Contra:** dejarlo escrito y ya (era la opción por defecto; se descartó por lo mudo del fallo), o pinchar `header_up X-Forwarded-For` explícito en la plantilla (fija el valor pero **no** impide que alguien añada `trusted_proxies` después, así que no cubre el caso). ✅ **El guardián se vio ROJO sobre la plantilla de verdad**, no solo sobre archivos de mentira (`[L-007]`), y ciego a los comentarios que nombran la directiva para explicar por qué no está. 348 → **351** | `tests/test_deploy_limits.py`, `deploy/Caddyfile.template`, `deploy/README.md`, `T-055`, `[A-014]` |
| D-041 | 2026-08-07 | 🚨 **La segunda mitad de `T-059` NO se lanza hoy: se lanza el 2026-08-08, DESPUÉS de leer `Importe utilizado` y diga lo que diga ese campo.** Sellado hoy, sin el número delante — la lectura no es una condición que pueda absolver o condenar el lanzamiento, es un **orden**. Dos motivos, y cada uno basta solo: **(1)** lanzar hoy mete una segunda fuente de gasto (la EC2) en la misma factura que la Elastic IP, y con eso **muere `t_cargo − t=0`** — el retraso entre el primer cargo real y su aparición en pantalla, medible **una sola vez en la vida de la cuenta** y útil los seis meses; **(2)** encender la EC2 con la alarma **todavía sin habérsele visto morder** es `[LM.13]` exacto: un control que nadie ha visto funcionar no es un control, y el gasto que vigilaría se multiplica el día que arranca la máquina. 📌 **La Elastic IP NO se suelta** — se asocia mañana como parte de esa misma mitad; soltarla y volver a pedir otra rompería el `t=0` que el experimento está midiendo. ⚠️ Precio aceptado a sabiendas: la IP sigue cobrando por ociosa un día más | `T-059`, `[A-018]`, `[D-040]` |
| D-040 | 2026-08-07 | 🚨 **El criterio de lectura de `[A-018]` se sella HOY, antes de la lectura del 08, no mañana con el número delante.** Una tabla de lectura enmendada después del dato deja de ser criterio y pasa a ser racionalización. Tres piezas: **(1)** la **fila 3 queda ANULADA, no borrada** — nombraba "aplican las 750 h gratis de IPv4", causa **desmentida hoy** (esas horas son para direcciones en uso; la nuestra está ociosa y cobra), y la original vive en `cfba50a`, donde se lee con autoridad; **(2)** **guardia sobre la fila 2** — "alarma rota" exige **≥12 h de silencio tras hacerse visible el importe**; 🔴 **su motivo se corrigió DOS veces el mismo día**: ni `24 + 12 = 36`, ni *"eso era doble conteo"* —**esa segunda corrección afirmaba de más**, porque llamarlo doble conteo **es** afirmar que comparten reloj, justo el dato que la misma frase declaraba desconocido. ✅ Redacción final con **un solo desconocido**: *no se sabe si lo que se MUESTRA y lo que se EVALÚA comparten reloj*; si lo comparten faltan **minutos** y la suma sobraba, si van desacoplados faltan **horas** y la suma valía. La regla se queda porque errar hacia esperar de más no produce conclusiones falsas en **ninguna** de las dos ramas. 📌 Patrón anotado: **el texto que documenta una corrección no está exento de la corrección que documenta**; **(3)** queda escrito **qué dejó de cubrir** el experimento al cambiar de instrumento; **(4)** se anotan **dos** horas, `h1` (importe visible) y `h2` (correo): `h2 − h1` es un número que no tiene ni la documentación y decide la duda de (2) gratis — la espera pasa a ser la **segunda medición** (`LM.19`); **(5)** ***"Actualizar plan" SALE de la lista de `T-068`*** y pasa al **protocolo de lectura**: no es la puerta 8, porque las siete hay que ir a buscarlas y esta está en la cabecera que el experimento obliga a abrir **a diario** — el riesgo se mide por **tráfico**, no por peligrosidad (`[L-026]`). 🔴 Y se **retira** la holgura de "32 h" escrita esa misma mañana: eran **cortas**, no solo arbitrarias | `_persistence/assumptions.md` `[A-018]` |
| D-039 | 2026-08-07 | **La precedencia NO se toca —el entorno le sigue ganando al `.env`—: lo que se arregla es que estaba MUDA.** Nueva `config.value_origin`, y el renglón del arranque pasa a decir `origen: .env` o `origen: entorno`. 🔑 El `.env` es el ajuste **por defecto de esta máquina**; el entorno es **esta corrida**: lo específico gana a lo general, y el entorno no es un descuido sino el **canal deliberado de anulación** que usan pytest, un contenedor o un script de una vez. 🧪 **Y se corrigió el argumento que la cerraba:** se sostuvo que invertirla haría escribir a los 342 tests en `data/`, y **medido en contenedor es falso** — 346 pasan y `data/` queda con 0 archivos, porque `load_env_file()` corre una sola vez al importar y el fixture `autouse` desvía por test (`[D-036]` obliga a resolver en cada llamada). La decisión no cambia; el motivo sí. 🚨 **Y el motivo bueno salió de perseguir el falso: el riesgo NO vive en la suite, vive fuera** — un guion suelto (`create_account.py:96`, `measure_body.py`) llama a `load_env_file()` y ahí se acaba, sin fixture que pise después. Medido: con la precedencia invertida y `TEAPP_DATA_DIR` exportada, `create_account.py` escribiría en `/opt/teapp/data` en vez de en la carpeta de la corrida. **Es `T-072` exacta y `[A-020]` con otro disfraz.** Sabotaje del control por los **dos** lados (fijarla en `"entorno"` tumba 2, en `".env"` tumba 4). ⚠️ Punto ciego escrito: si entorno y `.env` traen el mismo valor no los distingue — delata **anulaciones**, no procedencias. 342 → **348** | `app/config.py`, `app/api.py`, `tests/test_config.py` |
| D-038 | 2026-08-07 | 🚨 **En `install.sh`, el `.env` que ya existe MANDA sobre el valor por defecto del guion.** Antes `DATA_DIR` se fijaba siempre a `${INSTALL_DIR}/data` y el `mkdir -p` corría **antes** de mirar el `.env` — así que reinstalar sobre una instalación cuyos datos vivían en otro disco **fabricaba la carpeta vacía de `[D-037]`**: el señuelo exacto que `[D-037]` existe para evitar, hecho con la mano por el guion. Ahora se lee primero y se crea después, y si lo que hay escrito es vacío o relativo el guion **se para en seco** (denegar por defecto, regla 3). **MEDIDO en contenedor, con el guion viejo como control rojo** — ver entrada | `deploy/install.sh` |
| D-037 | 2026-08-06 | 🚨 **La raíz de `data/` sale de `TEAPP_DATA_DIR`, sin valor por defecto, y la app se niega a arrancar si falta o si la carpeta no existe.** Es el movimiento 2 de `T-072`: el aislamiento deja de depender de que quien escriba un script se acuerde de **tres** desvíos (`accounts.ACCOUNTS_FILE`, `tools.USERS_DIR`, `quota.QUOTA_DIR`) y pasa a ser **una variable que, si se olvida, no arranca**. Denegar por defecto, el mismo patrón que ya usa `require_secret` con la llave. **Contra:** dejar el defecto `PROJECT_ROOT/data` (es el fallo), poner la variable **con** defecto (mismo fallo, más tarde), pasar la ruta por parámetro en cada llamada (`PI-2`, y olvidarse seguiría cayendo en el defecto), o un "modo test" (el interruptor **es** lo que se olvida, e invierte el criterio: seguro solo si te acuerdas). 🔑 **Se decide HOY por fecha, no por importancia:** hoy es un refactor; en cuanto exista la EC2 es una migración con ficheros de personas dentro. ⚠️ **La carpeta NO se crea sola** — una ruta mal escrita crearía un `data/` vacío y todo el mundo parecería haber perdido su marcador. ⚠️ **El portero de `no_data_writes.py` NO sigue la variable**: se queda anclado a su propia ruta, o vigilaría la carpeta desviada. 📌 Deja `T-066` con algo concreto que comprobar | `app/config.py`, `app/tools.py`, `app/quota.py`, `app/accounts.py`, `create_account.py`, `tests/conftest.py`, `tests/no_data_writes.py`, `.env.example`, `deploy/` |
| D-036 | 2026-08-06 | **El aislamiento del marcador se arregla en `app/tools.py`, no solo en los tests — y lo vigila un PORTERO sobre `data/` entera, no un test sobre `add_point`.** Las tres funciones del marcador llevaban la carpeta como valor por defecto en la firma (`users_dir: Path = USERS_DIR`), congelada al importar: por eso un `setattr` en `conftest.py` no servía y se tapaba sustituyendo `add_point` por un maniquí en **tres** archivos de tests. Con el maniquí puesto, el camino API → marcador → disco no lo recorría **ningún** test. Ahora se resuelve dentro de la función, igual que `quota.py` (`app/quota.py:129`), y el maniquí se borra. 🚨 El testigo es un portero al estilo `no_network.py`: huella del **contenido** de `data/` antes y después de **cada** test. Se eligió sobre un test que comprobara que `add_point` escribe en `tmp_path`, porque ese vigila a un inquilino y el portero vigila la puerta — pero se escriben **los dos**: el portero se queda verde si alguien vuelve a poner un maniquí (nadie escribe), y eso solo lo caza el test que exige ver el archivo aparecer | `app/tools.py`, `tests/conftest.py`, `tests/no_data_writes.py`, `tests/check_no_data_writes.py`, `tests/test_api.py`, `tests/test_english_tutor.py`, `tests/test_deploy_limits.py`, `T-071`, `[L-020]`, `[L-021]` |
| D-035 | 2026-08-06 | **El tope de cuerpo de Caddy se queda en `16KB`, ahora MEDIDO — y un test de `tests/` lee `deploy/` para que no se despegue de `MAX_SENTENCE_LENGTH`.** El número anterior era criterio y además **falso por 3x** ("500 caracteres no llegan a 2 KB"): pesado con la app real, el peor caso legítimo son **6016 bytes**, porque un emoji escapado `\uXXXX\uXXXX` cuesta **12 bytes** por carácter y `MAX_SENTENCE_LENGTH` acota caracteres, no bytes. Contra 16000 (`KB`=1000 en go-humanize, no 1024) quedan 2,66x. ✅ **Ese 16000 estaba LEÍDO y se MIDIÓ el 2026-08-07** con Caddy 2.11.4 real en contenedor: `caddy adapt` → `16000` (control `16KiB` → `16384`), y por HTTP el borde cae exacto — **16000 B pasa, 16001 B devuelve 413**, con uvicorn directo contestando 401 a todos los tamaños como control. Con eso muere `[A-019]` y se retira la salvedad de `T-054`. 🚨 Se acepta que un test cruce a `deploy/` —el primero que lo hace— porque el acoplamiento es real y hoy no lo vigila nadie: subir el 500 dejaría a Caddy devolviendo 413 a frases legítimas **sin un solo error en Python** | `deploy/Caddyfile.template`, `tests/test_deploy_limits.py`, `app/api.py`, `T-054`, `T-061`, `[C-002]`, `[A-019]`, `[L-019]` |
| D-034 | 2026-08-06 | **El origen real detrás del proxy lo resuelve uvicorn, no `app/api.py` — y las banderas se escriben aunque ya sean el valor por defecto.** `_request_origin` se queda tal cual: medido con uvicorn 0.52.1 de verdad, `--proxy-headers` y `--forwarded-allow-ips 127.0.0.1` ya vienen puestas y hacen exactamente lo que `T-055` pedía (leer `X-Forwarded-For` **solo** si la petición llega por loopback). Se escriben explícitas en `teapp.service` porque un ajuste de seguridad que depende de un valor por defecto cambia el día que alguien actualice la librería, y nadie se entera hasta que la app queda cerrada | `deploy/teapp.service`, `app/api.py`, `T-055`, `T-060`, `T-066`, `[A-014]`, `[L-019]` |
| D-033 | 2026-08-06 | **Todo TEAPP vive en `us-east-1` (Norte de Virginia).** La consola traía `us-east-2` (Ohio) por defecto — nadie la eligió. Se cambia **antes** de reservar la Elastic IP, cuando aún no existe nada: la región no es un ajuste, es un sitio, y las cosas de una región no se ven desde otra. Se elige `us-east-1` porque es la que `[A-015]` ya asume en su tabla de precios; quedarse en Ohio obligaba a comprobar precios y corregir esa tabla sin ganar nada | `T-059`, `[A-015]`, `[L-018]` |
| D-032 | 2026-08-05 | **TEAPP corre en la nube como el usuario `ubuntu`, el mismo que administra — y no como un usuario propio sin permisos.** Se elige contra la práctica estándar, a sabiendas: `create_account.py` lo ejecuta quien administra y escribe el MISMO `data/` que el servidor. Dos dueños distintos sobre esa carpeta es un problema de permisos que no enseña nada de lo que se está aprendiendo | `deploy/teapp.service`, `deploy/install.sh`, `T-064`, `[A-002]` |
| D-031 | 2026-08-05 | **La cuenta se abre con un alias `+aws` del correo personal, y con MFA en el root en el mismo momento de crearla** — no "cuando haya tiempo". 🚨 **El valor literal del correo NO se escribe aquí: el repo es público**, y el correo del root es media llave de recuperación. ⚠️ **Al ejecutarlo el 2026-08-06 se usó el correo personal SIN el alias** — ver la nota al final de la entrada | `T-057`, `[C-005]`, `[C-006]` |
| D-030 | 2026-08-05 | **El paso 7 termina con un CIERRE PLANEADO, no con la cuenta muriéndose sola.** Y la prueba de que `[C-004]` se cumplió es **levantar TEAPP desde cero solo con `deploy/`** — que se ENSAYA PRONTO, no al final: un paracaídas se prueba antes de saltar. 📌 La cuenta es desechable; `deploy/` no | paso 7, `T-069`, `T-070`, `[C-004]`, `[C-006]` |
| D-029 | 2026-08-05 | **La plataforma del paso 7: AWS + EC2 pequeña + Caddy + un nombre gratuito de DuckDNS + IP fija.** No lo decide la nube: lo decide **el disco**. `data/` son archivos, y un disco efímero evaporaría la cuota del paso 6 sin tocarle una línea. Con la plataforma cerrada, las cinco deudas del despliegue por fin tienen dueño | paso 7, `T-050`, `T-051`, `T-054`, `T-055`, `T-056`, `[L-032]` (antes `[A-005]`), `[A-014]`, `[C-002]`, `[C-003]`, `[C-004]` |
| D-028 | 2026-08-04 | **El log se configura (`T-033`): hora, nivel, origen, y `INFO` por defecto.** Lo que arregla no es la forma, es que `info` vuelva a significar algo. Dos renglones bajan de `warning` a `info`; el de los intentos fallidos **se queda** en `warning` | `app/config.py`, `app/api.py`, `tests/test_log_config.py`, `[L-012]` |
| D-027 | 2026-08-04 | **El registro de la v1 es CERRADO**, detrás de `TEAPP_REGISTRATION_OPEN` (por defecto `false`). Las invitaciones son v2 por la regla de `scope.md`. Las cuentas se crean con `create_account.py`, sin teclado — `main.py` no sirve en un servidor | `app/config.py`, `app/api.py`, `create_account.py`, paso 7 |
| D-026 | 2026-08-04 | **El contador de intentos fallidos vive en MEMORIA, y la cuota sigue en disco.** No es incoherencia: en disco, quien ataca decide cuántas veces escribe el servidor — la palanca de `[C-002]`. A cambio, el `dict` necesita barrido propio | `app/login_guard.py`, `app/api.py`, `[A-002]`, paso 7 |
| D-025 | 2026-08-04 | **`/login` se queda sin freno de intentos en el paso 6**, y se anota como deuda con dueño: es el paso 7. El freno de la cuota protege la factura; este protegería las contraseñas, y son cosas distintas | `app/api.py`, paso 7, `[D-026]` · ⏹️ **saldada** el 2026-08-04 |
| D-024 | 2026-08-04 | El "día" de la cuota se mide en **offset fijo −05:00**, escrito en el código, no en UTC ni con `ZoneInfo`. Comprobado: `ZoneInfo('America/Bogota')` **revienta en Windows** | `app/quota.py`, paso 7, `requirements.txt` |
| D-023 | 2026-08-04 | El paso 6 lleva **cuatro** frenos: cuota por persona y día, timeout, tope al tamaño del texto y motivo del frenazo. Los permisos de antemano **no entran**: ya están hechos en los pasos 4 y 5 | paso 6, `app/api.py`, `app/tools.py`, paso 8 |
| D-022 | 2026-08-04 | El portero de red entra al repo, y **con sus controles**: un vigía sin quien lo vigile no demuestra nada. Y `C-001` pasa a medirse en dos mitades, porque el portero no ve subprocesos | `tests/no_network.py`, `tests/check_no_network.py`, `tests/conftest.py`, `[C-001]` |
| D-021 | 2026-08-04 | Contraseña propia con cookie de sesión firmada; el proveedor externo se descarta por ser una pieza que no se controla | `app/api.py`, paso 5, paso 7 |
| D-020 | 2026-08-04 | Los cuatro marcadores de `data/users/` son huérfanos y se borran: sembrarlos obligaría a inventarles contraseña. El criterio no es "¿es de una prueba?" sino "¿tiene dueño?" | `data/users/`, paso 5, registro |
| D-019 | 2026-08-04 | El control del `.js` sube al Paso 2b; el resultado del push no se anota: es imposible, no un olvido | `protocol-close`, `protocol-start`, `session-closer` |
| D-018 | 2026-08-03 | Un control no puede causar un daño mayor que el que previene: el `.js` viejo no cancela el cierre | `protocol-close`, todo control futuro |
| D-017 | 2026-08-03 | Que el `.js` esté al día lo vigila el cierre, no `pytest`: es higiene del repo, no comportamiento | `protocol-close`, `session-closer`, `tests/test_api.py` |
| D-016 | 2026-08-03 | El `session-closer` hace `git push`; solo `--force` sigue prohibido | `protocol-close`, `session-closer`, todo cierre futuro |
| D-015 | 2026-08-03 | El `data/score.json` global se borra, no se adopta | `data/`, paso 4 |
| D-014 | 2026-08-03 | El nombre se normaliza y se valida con lista blanca, y se valida dos veces | `app/tools.py`, `app/api.py`, paso 5, paso 7 |
| D-013 | 2026-08-03 | En el paso 4 la identidad es **declarada, no verificada**: casilla + `localStorage` | `frontend/app.ts`, `app/api.py`, paso 5 |
| D-012 | 2026-08-03 | TypeScript con `tsc`: fuente en `frontend/`, el `.js` compilado sí va a Git | `tsconfig.json`, `package.json`, paso 3, paso 7 |
| D-011 | 2026-08-03 | FastAPI sirve la pantalla: mismo origen, y CORS se descarta (T-029) | `app/api.py`, paso 3, paso 7 |
| D-010 | 2026-08-02 | El detalle completo va al log; al navegador, un mensaje corto y sin rutas | `app/api.py`, todo error futuro |
| D-009 | 2026-08-02 | Candado en memoria + temporal con nombre propio para dos peticiones a la vez | `app/tools.py`, `[A-002]`, paso 4 |
| D-008 | 2026-08-02 | El tutor devuelve tres piezas separadas, no un texto cocinado | `app/english_tutor.py`, `app/api.py`, `main.py`, paso 3 |
| D-007 | 2026-08-02 | El marcador se escribe al lado y se renombra encima (escritura atómica) | `app/tools.py`, paso 4 |
| D-006 | 2026-08-02 | El marcador roto avisa con `ScoreFileError`; ausente sigue siendo 0 | `app/tools.py`, `main.py`, paso 2 |
| D-005 | 2026-08-02 | Nombres en inglés, contenido en español | todo el código del proyecto |
| D-004 | 2026-08-02 | El protocolo de inicio lee `_context/` siempre, no a demanda | `protocol-start`, `session-starter` |
| D-003 | 2026-08-02 | Recuperar 4 principios de ingeniería de un `CLAUDE.md` anterior | cómo se escribe el código |
| D-002 | 2026-08-02 | Los cuatro archivos del porqué los escribe la sesión principal, no el closer | `_persistence/` |
| D-001 | 2026-08-02 | La skill de inicio se llama `protocol-start`, no `protocol-close` | `.claude/skills/` |

---

## Entradas

### [D-055] 2026-08-10 — La cuota se devuelve por lo que dice `usage`, no por la forma de `content`

Corrige la mitad **(2)** de `[D-054]`, tomada el mismo día. La mitad (1) —el
`timeout=8.0`— sigue en pie sin tocar.

- **Se eligió:** decidir si se devuelve la cuota mirando el contador que viene
  dentro de la respuesta — `answer.usage.input_tokens` y `usage.output_tokens`.
  Si los dos son cero, no costó nada y se devuelve; si alguno no lo es, se cobra.
- **Contra:** el proxy de `[D-054]` —`stop_reason == "refusal"` **y** `content`
  vacío— que es lo que había hasta hoy.
- **Por qué:** el proxy tenía un agujero, y no teórico. 🚨 Comprobado en la
  documentación de Anthropic el 2026-08-10 (regla 6): **sin streaming** —que es
  como llama `judge_grammar`— un rechazo a **mitad** de la respuesta *omite el
  parcial*. Esa respuesta llega con `content` vacío y `stop_reason="refusal"`:
  **por fuera es idéntica al rechazo gratis, y por dentro los tokens ya están
  pagados.** El proxy devolvía cuota exactamente en el caso que `[D-051]` decidió
  cobrar.

  🔑 **La lección de fondo: antes de inferir un dato, mirar si el instrumento
  trae su propio contador.** `¿esto se facturó?` era una pregunta que la API ya
  contestaba literalmente; `[D-054]` la dedujo de la forma de `content` teniendo
  la cifra al lado. Un proxy no puede separar dos respuestas que tienen la misma
  forma; un contador sí — y aquí las tenían.

  📌 **`stop_reason` sale de la decisión.** Ya no discrimina nada: se queda en el
  mensaje de error, que es para diagnosticar, no para cobrar.

  ✅ **Verificado en ROJO por sabotaje**, no supuesto: reponiendo el proxy, el
  guardián nuevo `test_a_billed_refusal_with_no_partial_still_charges` falla con
  `request_sent = False` — cuota regalada — y **solo falla ese**.

  ⚠️ Los dos campos son la factura entera **porque este proyecto no usa cache**.
  Si algún día se usara, habría que sumar los tokens de cache.
- **Toca:** `app/tools.py` (la rama del veredicto vacío), `tests/fake_tutor.py`
  (`FakeUsage`, y el `usage` por defecto viene **facturado** — regla 3 metida en
  el valor por defecto), `tests/test_tools.py`, `[D-051]`, `[D-054]`, `T-076`.

### [D-054] 2026-08-10 — El reloj del cliente (`timeout=8.0`) y el rechazo que no se cobra

> 📌 **Su mitad (2) está revisada por `[D-055]`.** El discriminador ya no es
> `content` vacío, es `usage`. La mitad (1) —el `timeout=8.0`— sigue vigente.

Dos arreglos que salen de una **auditoría externa**, no de una revisión propia.
Los dos datos técnicos se comprobaron en la documentación del SDK el mismo día,
no de memoria (regla 6).

#### (1) El reloj que faltaba

- **Se eligió:** construir el cliente con `timeout=8.0`, por debajo de los 10 s
  de `[A-011]`.
- **Contra:** dejar el valor por defecto del SDK, que son **diez minutos**.
  Y contra ponerlo holgado (30 s) hasta medir cuánto tarda Opus 5 de verdad.
- **Por qué:**
  - 🚨 **El aviso lo habíamos escrito nosotros, y se saltó igual.**
    `app/api.py:130`, el 2026-08-04: *"en el paso 8 la llamada al modelo
    necesita SU PROPIO timeout, además de este. Si el cliente del modelo espera
    para siempre, este 504 devuelve el control a quien pregunta y deja el hilo
    secuestrado igual."* `[D-053]` razonó **tres veces** sobre los 10 s de
    `[A-011]` para quitar los reintentos — y el reloj al que se estaba
    ajustando nunca se puso. Intento único con 600 segundos.
  - 🔑 **Son dos frenos distintos y no se sustituyen.** El de `api.py` acota
    **lo que espera quien pregunta**; este acota **lo que espera el servidor**.
    Con solo el primero: a los 10 s el usuario recibe su 504 y se va, pero el
    hilo sigue esperando dentro del SDK hasta diez minutos, ocupando su sitio
    del pool. Si Anthropic se atasca, los hilos se acumulan y el servidor deja
    de atender **sin que haya fallado nada**.
  - 🔑 **Por debajo de los 10 s, no por encima**, y por el mismo motivo que
    `MAX_RETRIES = 0`: que el primero en rendirse sea el cliente, para que
    llegue el error de verdad (`APITimeoutError`) en vez de esconderse detrás
    del 504 del pool.
- ⚠️ **8.0 es una estimación sin corrida detrás** (regla 6). Nadie ha
  cronometrado cuánto tarda Opus 5 en juzgar una frase, y piensa por defecto
  aunque lleve `effort: "low"` (`[D-049]`). **Riesgo aceptado a sabiendas:** si
  tarda más de 8 s, fallan todas las peticiones. Ese riesgo ya existía —
  `[A-011]` puso 10 s al conjunto; lo que cambia es que ahora falla **de forma
  visible** en vez de muda. Se mide en `T-079`; si la medida lo desmiente, el
  número que se mueve es este y `[A-011]` detrás.

#### (2) El rechazo que se cobraba de más

- **Se eligió:** en la rama del veredicto vacío, devolver la cuota **solo**
  cuando `stop_reason == "refusal"` **y** `content` viene vacío.
- **Contra:** dejarlo como estaba (`request_sent=True` siempre, que era lo
  escrito), y contra la regla que propuso el auditor
  (`request_sent = stop_reason != "refusal"`, sin mirar el contenido).
- **Por qué:**
  - 🚨 **Un rechazo del clasificador de seguridad no gasta un token.**
    Documentado: si salta **antes de generar nada**, llega con `content` vacío
    y **no se factura en absoluto** — ni entrada, ni salida, ni cuota de la
    API. Cobrarlo le quita a alguien una práctica de sus 20 por algo que no
    costó nada, que es lo contrario de lo que decidió `[D-051]`.
  - 🔑 **Pero `stop_reason` solo no basta, y por eso la regla del auditor se
    corrige.** Un rechazo **a mitad** de la respuesta **sí** factura lo ya
    generado. Su versión devolvería cuota también ahí. Exigiendo además
    `content` vacío, se devuelve únicamente en el caso documentado como gratis
    y en cualquier otro se cobra: denegar por defecto (regla 3) aplicado al
    dinero, igual que en el `except` de `APIStatusError`.
  - 📌 **Es la misma forma que el hallazgo del que salimos bien parados ayer**
    — `APITimeoutError` heredando de `APIConnectionError`: dos causas cayendo
    por la misma puerta, y una de las dos devolviendo cuota mal. Se cazó en el
    orden de los `except` y se escapó **doce líneas más abajo**, en el `if`.

#### Lo que la auditoría retiró

Su tercer hallazgo del día anterior —poner `cache_control` en la rúbrica— **no
aplica y lo retiró él mismo**: comprobado, el mínimo para cachear en
`claude-opus-5` son **512 tokens** y la rúbrica no llega (678 caracteres,
≈170 tokens). Por debajo del mínimo no avisa: simplemente no cachea.

---

### [D-053] 2026-08-10 — El cliente de Anthropic va con `max_retries=0`: el reloj tiene un solo dueño

- **Se eligió:** construir el cliente con `max_retries=0`. Si hay que reintentar,
  se decide en `api.py`, no dentro del SDK.
- **Contra:** dejar el valor por defecto del SDK, que son **dos** reintentos
  automáticos ante 429 y 500, con esperas crecientes entre ellos.
- **Por qué:**
  - 🚨 **Tres intentos no caben en los 10 s de `[A-011]`.** Lo que se vería
    desde fuera sería el 504 del timeout, con el error de verdad —llave mala,
    Anthropic saturado— **escondido detrás**. Se diagnosticaría un problema de
    lentitud donde hay uno de credenciales.
  - 🔑 **El reloj tiene un solo dueño.** `app/api.py:673` ya decide cuánto se
    espera y qué pasa al agotarse. Un segundo temporizador dentro del SDK no
    coordina con el primero: solo se come su presupuesto sin saber que existe.
- **Precio aceptado:** un 429 aislado que el SDK habría absorbido en silencio
  ahora sube como error. Es lo correcto y además barato: con `[D-051]` ese caso
  devuelve la cuota, así que no le cuesta nada a quien practica.
- **Toca:** `app/tools.py` (`MAX_RETRIES`), y `T-079`, que medirá si esta
  decisión hace falta ajustarla con facturas delante.

### [D-052] 2026-08-10 — `judge_grammar` gana un `client=None`: se amplía la firma que `T-076` dio por cerrada

- **Se eligió:** `judge_grammar(sentence: str, client=None) -> str`. El cliente
  de Anthropic entra como parámetro opcional y se resuelve **dentro** de la
  función cuando no se pasa.
- **Contra:** dejar la firma intacta —`T-076` la había declarado definitiva— y
  desviar el cliente por otro camino: una variable de módulo que los tests
  pisaran, o un parche del entorno.
- **Por qué:**
  - 🔑 **La casa ya tiene esta forma, y la tiene por esta misma razón.**
    `score_file(name, users_dir=None)` y `read_score(name, users_dir=None)`
    llevan exactamente este parámetro, resuelto dentro y no en la firma. Es
    `[D-036]`: sin él, los tests no podían desviar el marcador y el camino de
    verdad se quedaba sin recorrer.
  - 🚨 **`tests/no_network.py` cierra la red en TODA la suite** (`[C-001]`), así
    que un test **no puede** llamar a Claude. Tiene que inyectar un cliente
    falso por alguna puerta; esta es la puerta que el proyecto ya usa.
  - ✅ **No viola PI-2 aunque lo parezca.** No es configurabilidad que nadie
    pidió: es lo único que hace la función comprobable. Sin ella `T-076` no se
    puede dar por terminada según PI-4, porque no habría forma de correrla.
- **🚨 Y el cliente por defecto se construye DENTRO, nunca en la firma.** Un
  `client=Anthropic()` escrito en la firma se evaluaría **una sola vez, al
  importar el módulo**, y se quedaría con la llave de aquel momento para
  siempre. Es palabra por palabra el defecto que `[D-036]` vino a matar.
- **Ningún código existente se rompe:** `respond()` la sigue llamando con un
  solo argumento y no se entera.
- **Toca:** `app/tools.py`, los tests de `T-076`, y el criterio para cualquier
  pieza futura que haya que poder falsear en la suite.

### [D-051] 2026-08-10 — La cuota se devuelve partida: se devuelve si la petición nunca salió, se cobra si salió

- **Se eligió:** cuando falle Claude, la cuota del día se devuelve **solo si la
  petición nunca llegó a salir**. Si salió, se cobra aunque no vuelva veredicto.
  Cierra la pregunta que `[D-050]` dejó abierta a propósito.
- **Contra:** (a) devolver siempre — fue la respuesta inicial del usuario, y es
  la intuitiva: sin veredicto no hubo práctica; (b) no devolver nunca, que es lo
  que hoy dice por escrito `app/quota.py:249`.
- **Por qué:**
  - 🔑 **La cuota no cuenta veredictos, cuenta dinero.** Está escrito en `spend`
    desde el paso 6: *"lo que se cobra es haber intentado, porque intentar es lo
    que cuesta dinero"*. Y `refund` avisa de lo contrario: *"devolver de más
    sería peor que no devolver: regalaría cuota"*.
  - 🚨 **Devolver siempre abre un agujero real, no teórico.** Con Claude
    saturado, cada reintento gasta tokens de entrada y **ninguno gastaría
    cuota**: el freno de facturación dejaría de frenar exactamente el día que
    las cosas van mal, que es el día para el que se construyó.
  - 🪞 **La forma ya estaba inventada en casa.** `api.py:673` no decide a ojo si
    el timeout se cobra: se lo pregunta a `future.cancel()`, que sabe si la
    tarea llegó a arrancar. Esto es la misma pregunta, hecha al SDK en vez de al
    pool de hilos. No es un principio nuevo; es el del paso 6 alcanzando el
    sitio que le faltaba.
- **Dónde cae la línea:**
  - **Nunca salió** → falta la llave, llave inválida, la conexión se rechazó,
    frenó el límite de peticiones. Cero tokens gastados. **Se devuelve.**
  - **Sí salió** → error del servidor de Anthropic, saturación, corte después de
    haber mandado la frase. Los tokens de entrada ya se pagaron. **Se cobra.**
- **⚠️ Lo que NO está comprobado (regla 6):** las **familias** de fallo son las
  de arriba, pero **los nombres exactos de las excepciones del SDK `anthropic`
  no se han verificado**. Se fijan leyendo la documentación al escribir
  `T-076`, no de memoria. Escribir aquí una lista de clases inventada sería
  darle a `T-076` un mapa falso con pinta de comprobado.
- **🚨 Y ante la duda se COBRA, no se devuelve.** Es denegar por defecto (regla
  3) aplicado al dinero: si un fallo no encaja claro en ninguna familia, cuenta
  como intento. Equivocarse cobrando le cuesta a alguien una práctica de 20;
  equivocarse devolviendo deja el freno abierto de par en par.
- **Toca:** `app/tools.py` (la excepción tiene que llevar la distinción
  encima), `app/api.py` (quien llama a `refund`), los tests de `T-076` —que
  ganan un tercero: el fallo que nunca salió devuelve, el que sí salió no—, y
  `[A-010]`, que es la cuota que esto protege.

### [D-050] 2026-08-10 — Si Claude falla, mensaje de error y el marcador no sube

- **Se eligió:** cuando `judge_grammar` no consiga un veredicto —red caída, llave
  mala, modelo que no contesta—, la app muestra un mensaje de error y **no suma
  el punto**. La práctica no cuenta.
- **Contra:** (a) sumar el punto igual, apoyándose en `[A-001]` —el marcador
  cuenta frases **practicadas**, no correctas, y la frase se escribió—; (b)
  devolver un veredicto de repuesto del tipo *"no pudimos revisarla, sigue
  practicando"*, que deja la pantalla entera y no obliga a tocar nada.
- **Por qué:**
  - 🔑 **El veredicto de repuesto es `FAKE_VERDICT` volviendo por la puerta de
    atrás.** El paso 8 existe para echar de casa a la función que contesta
    siempre lo mismo sin mirar la frase; un texto amable de repuesto es
    exactamente eso otra vez, y peor, porque ahora hay un modelo detrás y nadie
    sospecharía. Es un fallo **mudo**, la familia que este proyecto persigue
    desde `[L-032]`.
  - 🔑 **`[A-001]` no cubre este caso, aunque lo parezca.** "Practicada" da por
    hecho que hubo tutor. Una petición sin veredicto no es una práctica floja:
    es una práctica que no ocurrió. La propia `[A-001]` avisa de que el contrato
    de `judge_grammar` cambia en el paso 8, y este es el cambio.
- **Hallazgo, y es lo que más cambia el trabajo de `T-076`:** ✅ el código **ya
  se comporta así**, y no por diseño sino por el orden. En
  `app/english_tutor.py:53` los argumentos de `TutorReply(...)` se evalúan en el
  orden escrito —`count_words`, `judge_grammar`, `add_point`—, así que una
  excepción del juez corta antes de llegar al marcador. Y `app/api.py:708` ya
  convierte cualquier `Exception` en un 500 con mensaje.

  🚨 **Por eso ese orden deja de ser cosmético.** Reordenar tres líneas
  —hoy parece inocuo, y un `add_point` primero se lee igual de bien— cobraría el
  punto de una práctica sin veredicto **sin romper un solo test**. Se vigila con
  un test propio, mismo criterio que `[D-042]` aplicó a `trusted_proxies`: el
  modo de fallo es mudo, así que un comentario no basta.
- **Lo que NO resolvía, y quién lo resolvió:** ❓ la cuota del día se gasta
  **antes** de llamar al tutor (`app/api.py:607`), así que un fallo de Claude le
  costaría a la persona una de sus 20 prácticas de `[A-010]`. Para el timeout la
  pregunta ya estaba contestada —`api.py:673` distingue "nunca empezó", que se
  devuelve, de "ya corría", que se cobra según `[D-023]`—; para el fallo del
  modelo quedó abierta. ✅ **La cierra `[D-051]` el mismo día**, y con la misma
  forma que el timeout: se devuelve solo si la petición nunca llegó a salir.
- **Toca:** `app/tools.py`, `app/english_tutor.py`, `app/api.py`, los tests de
  `T-076`, y el paso 8 entero.

### [D-049] 2026-08-10 — El paso 8 arranca con Opus 5 a `effort: "low"`; el descenso de modelo es trabajo del paso 9

- **Se eligió:** `claude-opus-5` con `output_config: {"effort": "low"}` para el
  cuerpo real de `judge_grammar` (`T-076`). El descenso a `claude-sonnet-5` y
  luego a `claude-haiku-4-5` queda como trabajo **medido** del paso 9, con los
  evals y la rúbrica ya montados.
- **Contra:** arrancar directamente con `claude-haiku-4-5`, que era mi propuesta,
  apoyada en la regla 5 (minimizar factura manda). También se descartó
  `thinking: {"type": "disabled"}` como forma de acotar el gasto — ver abajo.
- **Por qué:** son tres razones, y la primera es la que decide.

  **(1) Deja al sospechoso solo, que es el argumento del propio roadmap.**
  El agente es falso hasta hoy porque *"el modelo es la única pieza que no
  responde igual dos veces"*: sacarlo del camino hace que, cuando algo falle, no
  haya que preguntarse si fue él. Arrancar por Haiku reintroduce exactamente esa
  ambigüedad **el día que se estrena la rúbrica**. Un veredicto malo tendría dos
  culpables posibles —la rúbrica o el modelo— y separarlos obligaría a probar
  Opus de todas formas, más tarde y con menos información. Con Opus, un veredicto
  malo solo puede acusar a la rúbrica.

  **(2) La regla 5 muerde con volumen, y en desarrollo no hay volumen.**
  ⚠️ **Estimación, no corrida** (regla 6): suponiendo ~400 tokens de entrada
  (rúbrica más frase) y ~100 de salida, sale ~$0,0045 por práctica con Opus 5
  contra ~$0,0009 con Haiku 4.5. En doscientas prácticas de prueba son unos
  **$0,90 contra $0,18**. Menos de un dólar de diferencia por quitar una variable
  de la investigación. Los números de verdad se miden en `T-079`.

  **(3) El paso 9 hereda un trabajo concreto en vez de una intención.** Bajar de
  modelo con evals y rúbrica montados no es adivinar, es medir — regla 6 al pie
  de la letra. El plan es del usuario y se adopta tal cual.

- **Por qué `effort: "low"` y no apagar el pensamiento:** 🚨 no es un adorno de
  ahorro, es lo que hace viable la decisión. **Claude Opus 5 piensa por defecto**
  —cambio reciente respecto de Opus 4.8— y esos tokens de razonamiento **se
  cobran como salida, a $25 el millón**, además de consumir reloj. Sin acotarlos,
  la estimación de arriba se multiplica y, peor, **el pensamiento se come el
  timeout de 10 s de `[A-011]`**: veredictos correctos que llegan tarde son
  veredictos perdidos. Apagarlo del todo (`thinking: {"type": "disabled"}`) se
  descarta porque la documentación de Anthropic registra que en Opus 5 se le
  escapan etiquetas `<thinking>` dentro de la respuesta **visible** — y ese texto
  acabaría en el navegador de quien practica.
- **Trampa anotada de antemano para el descenso del paso 9:** una rúbrica escrita
  contra un modelo fuerte tiende a quedarse corta, porque se da por hecho lo que
  ese modelo rellena solo; la documentación de Anthropic avisa de que un prompt
  afinado para un modelo hay que reafinarlo para otro. Por eso *"Haiku falló"*
  solo vale como conclusión **después** de reintentar con la rúbrica ampliada.
  Con la rúbrica tal cual, `modelo` y `rúbrica` vuelven a ser dos variables a la
  vez — el error que esta decisión existe para evitar.
- **Toca:** `app/tools.py` (el cuerpo de `judge_grammar` y la rúbrica),
  `requirements.txt` (entra `anthropic` con versión fija), `T-076`, `T-079`,
  `[A-010]` y `[A-011]` —que dejan de ser predicción cuando haya facturas—, y el
  alcance del paso 9, que gana la comparación entre modelos. 📌 Cambiar de modelo
  más adelante es una línea: el resto del proyecto solo ve la firma
  `judge_grammar(sentence: str) -> str`.

### [D-048] 2026-08-10 — Se cruza al paso 8 con pendientes del 7, nombrados uno a uno

- **Se eligió:** **arrancar el paso 8 ahora**, dejando abiertas `T-046`, `T-067`,
  `T-069` y `T-070` del paso 7 — cada una con su motivo escrito. `T-056` se hace
  de camino, porque son dos minutos y es lo único que bloqueaba de verdad.
- **Contra:**
  1. **Terminar el paso 7 entero antes de cruzar**, que era el plan vigente y lo
     que la regla del roadmap pide al pie de la letra (*"antes de pasar al
     siguiente, córrelo"*).
  2. Dejar los pendientes **sin nombrar**, cruzando y ya.
- **De dónde sale:** de una objeción del usuario, no de una revisión ni de un
  fallo. *"Sentimos que invertimos mucho tiempo en esta aplicación y no hemos
  podido avanzar al siguiente paso."*
- **Por qué:**
  - 📊 **La sensación estaba bien calibrada, y se contó en vez de recordarla**
    (regla 6), sobre el índice de `progress.md`:

    | | sesiones | días |
    |---|---|---|
    | pasos 0 a 6 (siete pasos) | 12 (`S-001`…`S-012`) | 3 |
    | paso 7 (uno solo) | 22 (`S-013`…`S-034`) | 6 |

    **Un paso ha costado casi el doble que los otros siete juntos.**
  - 🔴 **Y hubo que corregir un error de esta misma sesión.** Horas antes, en
    este mismo chat, se afirmó que `T-069` frenaba el paso 8. **Es falso.**
    `[D-030]` pide el ensayo *"pronto"*, pero ese *pronto* está medido **contra
    el cierre de la cuenta** (2027-02-06, `[C-006]`), no contra el paso 8 — que
    para arrancar no toca `deploy/`. Recontado, lo único que bloqueaba era
    `T-056`.
  - 🔑 **El argumento que decide es de recurso escaso, y apunta al revés de lo
    que parecía.** Lo que corre es el calendario de `[C-006]` y los créditos de
    `[C-003]`. Y hoy **se están gastando en infraestructura para una app cuyo
    corazón sigue siendo el maniquí del paso 1**: hay HTTPS, identidad verificada,
    cuota por persona y apagado automático montados encima de una función que
    devuelve siempre lo mismo. Cada día de pulido del paso 7 compra robustez para
    algo que **todavía no hace aquello para lo que existe**.
  - ⚖️ **El contra es real y se acepta a sabiendas:** `deploy/` sin ensayar es
    una promesa (`[C-004]`), y `[D-030]` avisa justamente de que enterarse tarde
    es enterarse sin margen. Por eso `T-069` **no se cancela ni se hunde en la
    lista en silencio**: se le pone dueño de calendario —antes del cierre del
    primer ciclo de facturación, ≈ 2026-09-01— y el precio de aplazarla queda
    escrito aparte, en `[A-023]`.
- 📌 **Lo que NO cambia:** `[D-047]` sigue siendo válida. El ensayo se hará sobre
  instancia nueva y subdominio nuevo, con producción viva. Lo único que se movió
  es la fecha.
- 🧭 **La regla que queda para adelante:** un paso **sí** se puede dejar con
  pendientes, pero **los pendientes se nombran uno a uno, con su motivo y su
  dueño**. Lo que no se puede es cruzar sin saber qué quedó atrás — eso no es
  avanzar, es perder la cuenta.
- **Toca:** paso 7, paso 8, `T-046`, `T-056`, `T-067`, `T-069`, `T-070`,
  `[D-030]`, `[D-047]`, `[A-023]`, `[L-037]`.

### [D-047] 2026-08-10 — El ensayo de `T-069` va sobre instancia nueva y subdominio nuevo, con producción viva

> 🔻 **APLAZADA el mismo día por `[D-048]`.** Todo lo de abajo **sigue vigente**:
> instancia nueva, subdominio nuevo, producción viva, sin Elastic IP. Lo único
> que cambia es **cuándo** — el ensayo se corre después del paso 8, con fecha
> tope ≈ 2026-09-01. El guion ya está escrito en `deploy/console_steps.md`
> (Paso 5c) y no hay que volver a pensarlo.

- **Se eligió:** levantar una **segunda instancia EC2**, solo desde `deploy/`,
  **dejando en pie la de producción**; y darle un **segundo nombre de DuckDNS**
  (`teapp-rehearsal.duckdns.org`) apuntando a su IPv4 pública normal, **sin**
  Elastic IP.
- **Contra:**
  1. **Borrar la instancia de producción y reconstruirla**, que es lo que
     `[D-030]` describe con esas palabras.
  2. **Reutilizar `teapp.duckdns.org`** en la máquina nueva.
  3. Ensayar **sin HTTPS**, saltándose la sección 5 de `install.sh`.
- **Por qué:**
  - 🔑 **La opción 2 no es una preferencia: es imposible, y descubrirlo es medio
    hallazgo.** `teapp.duckdns.org` resuelve a la Elastic IP de la máquina viva.
    Caddy en la máquina nueva pediría certificado, Let's Encrypt iría a
    comprobar el nombre, y **llamaría a la máquina vieja**. El certificado no
    sale y el guion se para en `install.sh:378`, que espera 60 s a un
    `https://${TEAPP_DOMAIN}/` que nunca va a contestar desde ahí.
  - La **opción 3 vacía el ensayo**. Lo que `[C-004]` pone en duda no es si los
    archivos existen: es si la cadena entera (paquetes, servicio, proxy,
    certificado) se levanta sola. Saltarse el certificado es saltarse el único
    tramo que depende de terceros.
  - Contra la **opción 1**, que era la lectura literal de `[D-030]`: lo que
    `[D-030]` compra es **margen de calendario** —enterarse pronto de que
    `deploy/` no levanta—, y ese margen se consigue igual sin apagar lo que hoy
    funciona. Borrar primero convierte **cada fallo del ensayo en una caída de
    producción**, que es justo el apuro del que `[D-030]` quería escapar. El
    espíritu se respeta; la letra se ajusta.
  - ✅ **No hay que tocar una línea de `deploy/`**, y eso es en sí un resultado:
    `TEAPP_DOMAIN` ya era una variable de entrada, no un valor incrustado. Si el
    dominio hubiera estado escrito dentro del guion, este ensayo habría sido
    imposible sin editarlo — y editar el guion para poder probarlo es dejar de
    probar el guion.
  - 📌 **Sin Elastic IP en la de ensayo:** la IP fija existe para que el nombre
    siga resolviendo entre un apagado y un encendido. Esta máquina vive una vez
    y muere; su IPv4 pública normal basta, y es una tarifa menos.
- **Precio aceptado, y no es cero:** con `[C-003]` la EC2 **consume créditos**
  (el plan gratuito ya no trae las 750 h), así que mientras las dos máquinas
  convivan el gasto por horas de instancia corre **al doble**. La cuantía **no
  está medida** y se acota por el único lado que se controla: la duración.
- 🚨 **La instancia de ensayo se borra el mismo día en que se levanta.** Una
  máquina de usar y tirar que sobrevive a su ensayo es gasto puro, y en la lista
  de la consola su nombre no dice que sobra.
- ⚖️ **Lo que este ensayo NO mide, escrito antes de correrlo** para que después
  no se lea como cubierto: la asociación de la **Elastic IP** y el nombre de
  **producción**, porque los dos se quedan donde están. `T-070` sigue siendo la
  única corrida que los toca.
- **Toca:** `T-069`, `T-070`, `[A-022]`, `deploy/console_steps.md`.

### [D-046] 2026-08-09 — La pieza que apaga es un temporizador de systemd, no `cron`

**Qué se decidió.** La pieza de apagado automático que exige `[D-045]` se escribe
como un **temporizador de systemd**, en dos archivos de `deploy/`:

- `teapp-shutdown.service` — **qué hacer**: `/usr/sbin/shutdown -P now`.
- `teapp-shutdown.timer` — **cuándo**: `OnCalendar=*-*-* 23:00:00 UTC`.

Los instala `install.sh` (sección 4b), para que sobrevivan al redespliegue y no
dependan de que alguien los teclee — `C-004`: la cuenta se va a cerrar, y lo que
solo exista porque se hizo a mano está perdido de antemano.

**Contra qué se decidió: `cron`.** Era la opción más corta —un archivo, una
línea— y por PI-2 fue la primera candidata. Se descarta por **la zona horaria**:

> 🔑 `cron` interpreta la hora en la zona horaria de la **máquina**. Ese ajuste
> vive fuera de este repo y nadie vuelve a mirarlo. El día que cambie, el
> apagado se muda de hora **sin un solo error, en ningún log**.

`OnCalendar` permite escribir la zona **dentro de la propia línea**. Con eso la
hora viaja con la pieza, y la ventana de `[D-045]` deja de depender de algo
invisible desde el repositorio. El coste aceptado es un archivo más.

⚖️ **Y se descarta expresamente el argumento fácil.** "systemd porque el proyecto
ya usa systemd" es familiaridad, no una razón — habría sido `[L-008]`: comparar
con la versión floja del rival. `cron` pierde por la zona horaria, no por ser
menos conocido.

**Las tres cautelas que lleva escritas, y por qué cada una.**

1. 🚨 **`-P`, nunca `-h`.** Ya estaba en `[D-045]`; aquí queda en código. `-h`
   deja la máquina *"muerta por dentro y viva para la factura"*.
2. 🚨 **`Persistent=false`, explícito aunque sea el valor por defecto.**
   `Persistent=true` recupera disparos perdidos. Aquí la máquina se pierde el de
   las 23:00 **todas las noches, a propósito**. Con eso puesto, encenderla a las
   07:00 la apagaría inmediatamente — y el síntoma parecería *"la máquina no
   arranca bien"*, que no señala a este archivo. Se escribe explícito por la
   misma razón que las banderas de `teapp.service`: un ajuste de seguridad que
   descansa en un valor por defecto cambia el día que alguien actualice algo.
3. 🚨 **La orden no lleva `[Install]`, y `install.sh` no la arranca.** Son las
   dos formas de confundir la ORDEN con el TEMPORIZADOR. La primera apagaría la
   máquina en cada encendido; la segunda, **a mitad de la instalación**, en la
   máquina de quien la está instalando.

**Por qué esto se vigila con tests.** Los cuatro modos de fallo son **mudos**: la
app funciona igual con la pieza rota, nadie se entera, y el síntoma llega semanas
después en la factura — o al revés, la máquina se apaga cuando no debe y parece
una avería. Es el criterio de `[D-042]` exacto: *un comentario protege a quien lo
lee, y quien viene a arreglar un apagado raro no lo lee.*
`tests/test_deploy_shutdown.py` es el **tercer** test que cruza a `deploy/`, y
cada guardián se vio **rojo con el fallo puesto** (`[L-007]`, `[L-020]`).
351 → **360** tests.

📌 **Una corrección al escribirlo, que vale la pena anotar.** El cuarto guardián
nació buscando el texto literal `systemctl start teapp-shutdown.service` — que
`install.sh` **jamás escribiría**, porque usa `${SERVICE_NAME}`. Era un control
incapaz de ponerse rojo ante el fallo real: `[L-020]` cometido dentro del archivo
que lo cita. Se cambió por una expresión que busca **la forma** del fallo
(arrancar algo llamado `shutdown` que no acabe en `.timer`), y su control rojo usa
la variable tal como la escribe el guion.

✅ **DESPLEGADA en la máquina real el 2026-08-09, entre las 17:37 y las 17:50 UTC.**
Esto sustituye al *"no está medido"* que llevaba escrito una hora antes.
Evidencia, en orden:

1. `git pull` **`0dfdbba..afe2eab`** con los tres `create mode` de los archivos
   nuevos. 📌 Fue un rango **de dos commits**, no de uno: la máquina estaba más
   atrás de lo que se supuso al dictar el paso — se venía de `0dfdbba`, no de
   `104e37a`.
2. `install.sh` de punta a punta en código 0, con el temporizador armado y **la
   hora impresa por el propio guion**:
   `Sun 2026-08-09 23:00:00 UTC · LEFT 5h 17min · LAST – · PASSED –`.
   `LAST`/`PASSED` vacíos = armado y **nunca disparado**.
3. **El despertador viejo, desarmado con medición antes y después** — el control
   que exigía la revisión externa: sin esto, el apagado de las 18:00 no
   distinguiría la pieza nueva del disparo único, y el viejo desaparece al
   reiniciar, así que mañana no quedaría evidencia de ninguno de los dos.
   - antes: `USEC=1786316400000000`, `MODE=poweroff`, `UID=0`
   - `sudo shutdown -c` → *"System shutdown has been cancelled"*
   - después: `No such file or directory`
   🔑 El `USEC` **se tradujo, no se dio por bueno**: `1786316400` →
   **`2026-08-09 23:00:00 UTC`** exacto. Era el disparo único, y su
   `MODE=poweroff` confirma de paso que estaba puesto con `-P`.
4. `list-timers` **después** de cancelar: el temporizador sigue en pie.
   🔑 Se mira a propósito **después**, porque es justo el momento en que
   habérselo llevado por delante pasaría desapercibido — `shutdown -c` y el
   temporizador se parecen lo suficiente como para confundirlos.

📌 **Y la máquina está en UTC** (banner de `ssh`: `Sun Aug 9 17:37:53 UTC`), así
que `list-timers` se lee sin convertir nada. Eso es **suerte, no el diseño**: la
pieza lleva la zona escrita dentro precisamente para no depender de esto.

⚠️ **Lo que TODAVÍA no está medido, y es lo único que queda:** que el
temporizador **dispare de verdad** y que AWS pase la instancia a `stopped`. Todo
lo de arriba mira **configuración**; el disparo es **comportamiento**, y ningún
`list-timers` lo prueba — sería `[L-020]`. Esa medida es **`T-074`, hoy a las
23:00 UTC / 18:00 Colombia**, con alguien mirando la consola.

---

### [D-045] 2026-08-09 — La máquina no vive de noche

- **Se decidió:** **ventana de uso 07:00–18:00 hora de Colombia = 12:00–23:00 UTC.**
  Fuera de ella la EC2 está **detenida**. 11 h encendida, 13 h apagada.
- **Entra en vigor hoy**, 2026-08-09: el primer apagado es esta noche a las
  **23:00 UTC**. No es un régimen "a partir de mañana" — hoy ya cuenta.
- **Contra qué:** dejarla encendida de continuo, que es lo que venía haciéndose
  desde `[D-044]` y lo que `[D-029]` había dado por bueno.

#### 🔁 Lo que esto reabre: `[D-029]` descartó esta pieza con un número no medido

`[D-029]` cerró el asunto así, literalmente: *"la pieza que apaga la máquina
queda descartada"*, y *"encendida y quieta"*. El razonamiento tenía dos patas:

| pata de `[D-029]` | estado hoy |
|---|---|
| *"el gasto del paso 7 es del orden de $50 de $200 — gana el calendario y sobra un factor de cuatro"* | 🚨 es `[A-015]`, **aritmética de lista de precios, nunca corrida**, y el propio `[A-015]` dice que le falta el coste de la IPv4 pública — el que después resultó ser el primero en aparecer en la factura |
| *"apagar por las noches ahorra las horas de instancia **pero la IP sigue cobrando**: complica más de lo que rinde"* | ✅ **la mitad sigue siendo verdad** (ver más abajo), pero *"complica"* se apoyaba en que la pieza había que escribirla y mantenerla a mano |

🔑 **Lo que cambió no es la aritmética: es que ahora hay dinero medido.** Cuando
se escribió `[D-029]` no existía ni un solo importe en pantalla. Hoy hay 0,37 US$
en `Costo Acumulado Mensual` con ~71 h de vida (`[A-018]`, sexta lectura), y la
primera cifra que apareció fue justamente la que `[A-015]` no había contado.

⚠️ **Y sigue siendo verdad que apagar NO lleva el gasto a cero.** La Elastic IP
cobra igual —una IP sin máquina asociada es exactamente el cargo que generó los
primeros 0,12 US$ (`[C-003]`)— y el volumen de disco existe encendida o apagada.
**Lo único que se ahorra son las horas de instancia.** ❓ **Cuántas son en dinero
NO está medido** y aquí no se escribe: el precio/hora de la `t3.micro` no se ha
comprobado en pantalla. Esa cuenta es `[T-067]`.

#### ⚙️ El reparto: apagado automático, encendido a mano — y no es simetría rota por descuido

- **El apagado**: automático, **desde dentro de la máquina**. No un recordatorio,
  no una tarea del calendario de nadie.
- **El encendido**: **manual**. Se enciende el día que se va a trabajar.

🔑 **El motivo es el olvido, no la comodidad.** Los dos lados fallan alguna vez, y
fallan distinto:

| qué se olvida | qué cuesta |
|---|---|
| encender | nada. Se pierden minutos de la sesión |
| **apagar** | 🚨 corre el reloj toda la noche, y **nadie avisa** — el aviso de `[A-018]` llega con ~24 h de retraso |

**El olvido tiene que caer del lado que no cobra.** Por eso el lado caro se
automatiza y el barato se deja a la mano.

#### 🔴 Corregida en el momento — la línea 3 se BORRA, no se matiza

La primera versión de esta decisión, escrita hace minutos, llevaba una tercera
línea: *"arranca cuando la alarma de `[A-018]` haya sonado, no antes: la ventana
rompe la cuenta dinero ÷ horas que es el método del experimento"*.

🚨 **Era falsa, y queda escrita aquí en vez de sobrevivir con una nota al lado.**
Se le atribuyó a `[A-018]` un daño que es de `[T-067]`:

- Lo que le queda a `[A-018]` por medir son **relojes**: `h1` (cuándo el importe
  del presupuesto deja de ser 0,00) y `h2 − h1` (cuánto tarda el correo desde
  ahí). **Ninguno de los dos depende de que la máquina esté viva.**
- El cruce del umbral **ya está bancado**: 0,37 US$ contra un umbral de 0,01.
- La Elastic IP **cobra de noche igual**, así que el gasto no se detiene aunque
  la máquina duerma.
- Y la cuantía dejó de ser atribuible a una sola fuente el **08 a las 15:54 UTC**,
  cuando arrancó la EC2 — no hoy. Apagar no estropea nada que siguiera intacto.

⚖️ **Por qué se borra en vez de enmendarse:** una regla que sobrevive como
*"arranca cuando suene la alarma"* con un asterisco debajo se lee, dentro de dos
semanas, como regla — nadie baja al asterisco. **Lo que cambió tiene que quedar
escrito con el mismo tamaño que lo que queda.** Es la forma de `[L-029]`: lo que
no tiene dueño escrito, desaparece.

#### 🎁 Y la ventana le DA algo a `[A-018]` en vez de quitárselo

Las **23:00 UTC** (antes de apagar) y las **12:00 UTC** (al encender) pasan a ser
**dos lecturas del presupuesto ancladas a una hora fija**, todos los días.

🔑 **Eso acota `h1` por los dos lados**, que es justo el dato que ya se perdió una
vez: el 0,12 US$ apareció en un widget que nadie miraba, y su hora de aparición no
se puede recuperar. **El correo se fecha solo; `h1` no.** Sin lecturas ancladas,
`h1` vuelve a ser "en algún momento entre ayer y hoy".

#### ⏱️ Dos relojes nuevos, y una medición que `T-065` no cubrió

1. **La hora del primer apagado es el `t=0` de horas-encendida.** Desde ahí, el
   tiempo transcurrido y el tiempo facturado **dejan de ser el mismo número** —
   que era la ventaja de `[D-044]`— y hay que llevar la cuenta a mano.
2. 📌 **`[T-067]` se mide BAJO esta ventana, no antes.** Proyectar 180 días desde
   una máquina encendida 24 h sería proyectar **un régimen que no existe**. La
   medida buena empieza mañana, con el primer día completo de ventana.
3. 🧪 **El primer `stop`/`start` se mide.** `T-065` verificó el **reinicio**
   (`reboot`), que no apaga la máquina: es otra cosa. Aquí hay que ver tres:
   - el **marcador sigue vivo** en el disco,
   - la página responde **200 sin tocar nada** al volver,
   - el **certificado no se reemite** (la Elastic IP sigue asociada a la
     instancia detenida, así que el nombre debería resolver igual — eso es lo que
     se comprueba, no lo que se supone).

#### 🚨 "Detener", nunca "Terminar"

Son dos botones vecinos en la misma consola. **Detener** para la máquina y deja
el disco. **Terminar** la borra, y con ella `data/` entero: cuentas, cuotas y
progreso. No hay deshacer. La palabra correcta se escribe aquí porque el error se
comete una sola vez.

##### 🚨 Y el mismo par existe como AJUSTE, donde no hay nadie leyendo el menú

La instancia tiene una propiedad llamada **"comportamiento de apagado iniciado
por la instancia"** (*Detalles de la instancia → Comportamiento de apagado*). Es
lo que AWS hace cuando el sistema operativo **de dentro** se apaga solo. Toma los
mismos dos valores: `stop` o `terminate`.

🔑 **Aquí el aviso de arriba no protege**, y por eso esta sección existe aparte:
el de arriba vale cuando **un humano lee un menú**. La pieza de apagado
automático de `[D-045]` ejecuta lo que diga ese ajuste **todas las noches, sin
que nadie lea nada**. Si estuviera en `terminate`, la primera noche que la pieza
funcione **destruye la instancia y el disco** — `data/`, la cuenta de `jorge`, el
marcador, todo — y lo hace *por funcionar bien*.

📌 **El valor por defecto de AWS es `stop`.** ⚠️ **"Probablemente está bien" no es
"comprobado"** — es `[A-018]` en pequeño, y `[A-018]` lleva seis lecturas
enseñando lo que cuesta esa confusión.

🚨 **Condición dura, escrita antes de la pieza:** el valor **se lee en la consola
y se escribe aquí** *antes* de que se escriba una sola línea del apagado
automático. Sin ese dato en pantalla, la pieza no se construye.

> 📋 **Valor LEÍDO EN PANTALLA el 2026-08-09: `Detener`** (`stop`). ✅ Es el valor
> seguro y coincide con el que AWS trae por defecto — pero ahora está
> **comprobado**, no supuesto. La condición dura queda cumplida: la pieza de
> apagado automático se puede escribir.

⚠️ **Dónde está de verdad, porque costó encontrarlo y volverá a costar:** no está
en la pestaña *Detalles*. Vive en **`Acciones` → `Configuración de la instancia`
→ `Cambiar comportamiento de cierre`**. 🔑 **La consola en español lo llama
"cierre", no "apagado"** — buscar la palabra traducida de oído no lo encuentra. Y
es un cuadro de los que **escriben**: se lee el valor de la casilla cerrada y se
sale con *Cancelar*, sin desplegar la lista.

⚠️ **Y no confundirlo con su vecina**, *"Cambiar protección de terminación"*, que
está en el mismo menú y es otra cosa: esa protege del borrado **desde la consola**
y no dice nada del apagado desde dentro.

##### 🌙 Esta noche la regla no tiene quien la ejecute: disparo único

`[D-045]` empieza a valer hoy a las 23:00 UTC, y **la pieza que la ejecuta no
existe todavía** — ni siquiera es una tarea. O sea que el primer apagado de la
regla dependería de que alguien se acuerde a las 18:00 hora local, en mitad del
bloque de navegador y redespliegue. **Es `LM.24` esperando a repetirse: la sesión
se acaba antes de llegar al clic**, que es exactamente como murió `[D-041]`.

🔑 **Y sería la noche de estreno.** Una regla que falla estrenándose se lee para
siempre como regla opcional.

Se arma un temporizador de una sola vez, por SSH, **después** de haber leído el
ajuste de arriba:

    timedatectl                 # confirmar que la máquina va en UTC
    sudo shutdown -P 23:00      # -P = POWEROFF, no -h. Ver el aviso de abajo
    # sudo shutdown -c          # lo cancela, si algo se tuerce

📌 **No es la pieza definitiva** —esa se escribe como tarea— pero quita esta
noche de la memoria de nadie. Y **sobrevive al redespliegue de `T-050`**: es un
temporizador del sistema, no un servicio de la aplicación.

✅ **ARMADO Y VERIFICADO el 2026-08-09 a las 15:26 UTC**, no solo escrito:

    $ timedatectl
    Time zone: Etc/UTC (UTC, +0000)     ← la máquina va en UTC: 23:00 es 23:00
    System clock synchronized: yes · NTP service: active

    $ sudo shutdown -P 23:00
    Shutdown scheduled for Sun 2026-08-09 23:00:00 UTC, use 'shutdown -c' to cancel

    $ cat /run/systemd/shutdown/scheduled
    USEC=1786316400000000        → 2026-08-09 23:00:00 UTC (convertido aparte)
    MODE=poweroff                ← 🔑 poweroff, NO halt

🔑 **`MODE=poweroff` es la línea que importa**, y es lo que convierte el aviso de
arriba en algo comprobado: el sistema tiene apuntado *apagar*, no *parar la CPU*.
El sello `USEC` se tradujo por separado en vez de leer solo el mensaje de
`shutdown`, para que la hora venga del archivo y no de la frase que la anuncia.

🚨 **Lo que este temporizador NO sobrevive: un `stop`/`start`.** Está en la
memoria del sistema, así que la prueba de apagado/encendido que exige esta misma
decisión **lo borra**. Si esa prueba se hace hoy, hay que **volver a armarlo**
después. Es la trampa obvia de tener las dos cosas el mismo día.

##### 🚨 `-P` y no `-h`: apagar y "detener el procesador" no son lo mismo

Leído en la documentación de AWS el 2026-08-09 (*Change instance initiated
shutdown behavior*), literal:

> *"Note that the **halt** command does not trigger this behavior, as it only
> places the CPU into a HLT state **while the instance continues to run**."*

🔑 **Traducido: `halt` deja la máquina muerta por dentro y VIVA para la
factura.** Nadie entra, nada responde… y el reloj de las horas de instancia sigue
corriendo toda la noche. En `systemd` la bandera `-h` está documentada como
equivalente a *poweroff*, así que **probablemente** haría lo correcto — pero es
la tercera vez hoy que aparece un "probablemente", y aquí no cuesta nada quitarlo:
**`-P` pide apagado a secas, sin depender de esa equivalencia.**

⚠️ **Y el modo de fallo es MUDO, que es lo que lo hace caro:** desde fuera, una
máquina en `halt` y una detenida se parecen — las dos dejan de responder. La
diferencia solo se ve en la consola (`running` vs `stopped`) o, un día tarde, en
la factura. 🧪 **Por eso el primer apagado se hace CON ALGUIEN MIRANDO**, no a las
23:00 con todo el mundo dormido: se ejecuta el `stop`/`start` de prueba que esta
decisión ya exige, y se comprueba en la consola que el estado dice **`stopped`**.
Ahí se validan las dos cosas a la vez — el comando y el ajuste.

### [D-044] 2026-08-08 — La máquina se queda encendida esta noche, y la decisión caduca mañana

> ⛔ **CADUCADA el 2026-08-09. La reemplaza `[D-045]`.** Cumplió su vigencia
> declarada de una noche y se reevaluó, que era exactamente lo que pedía.

- **Qué se decidió:** no apagar la EC2 al cerrar la sesión del 2026-08-08.
  Se decidió **habiendo preguntado explícitamente si apagarla**, no por
  olvidarse de la pregunta — que es la forma habitual de dejar una máquina
  encendida.
- **Contra qué se decidió:** `stop` de la instancia esta noche y `start`
  mañana. Es la opción que empuja la regla 5 del proyecto (*minimizar factura
  manda sobre todo lo demás*) y no es una opción tonta.
- **Por qué se descartó, en dos motivos y cada uno pesa:**
  1. ⚠️ **Apagar no lleva el gasto a cero, y este proyecto ya sabe por qué.**
     El volumen sigue existiendo y se paga; y sobre todo, la **Elastic IP
     vuelve a estar ociosa** — que es *exactamente* la configuración que
     generó los 0,12 US$ de `[A-018]` con **cero máquinas encendidas**. Lo
     aprendido el 2026-08-07 (las 750 h gratis de IPv4 son para direcciones
     **en uso**) aplica igual aquí. El ahorro real es *la diferencia*, no el
     total.
  2. 🔑 **Encender y apagar rompe la aritmética del único experimento
     abierto.** Con la máquina continua, **horas facturadas = horas
     transcurridas**, y `[A-018]` se divide sola contra un `t=0` medido. En
     cuanto haya tramos encendido/apagado las dos dejan de coincidir y hay que
     llevar la cuenta a mano. Es el error de las 15:08 de hoy —un divisor mal
     puesto— pero repetido en cada tramo en vez de una sola vez.
- 📌 **Y hay trabajo mañana que la exige viva:** `T-051` (cookie `Secure` en un
  navegador de verdad), el redespliegue que le queda vivo a `[A-005]` (cerrada el 09 → `[L-032]`), y
  `T-066` (dos dispositivos). Apagar esta noche compra unas horas de instancia
  y las paga ensuciando el experimento.
- 🚨 **VIGENCIA DECLARADA: una noche.** Esto es lo que separa esta decisión de
  dejarla encendida por dejadez. **Si mañana no se toca la máquina, la
  decisión caduca**: para varios días sin usarla los dos motivos se invierten
  —el experimento ya no se beneficia de la continuidad y las horas se
  acumulan—, y **apagar gana**.
- ⚠️ **Lo que NO se rompe al apagar, para cuando toque hacerlo:** la Elastic IP
  sigue asociada a través de un `stop`/`start`, así que la máquina vuelve con
  la misma dirección y `teapp.duckdns.org` no hay que reapuntarlo. Y el
  volumen conserva `data/`. ❓ Medido está el **reinicio** (`T-065`), no el
  `stop`/`start` — son operaciones distintas y la segunda sigue sin corrida
  encima.

### [D-043] 2026-08-08 — La AMI es `Ubuntu Server 24.04 LTS`, ni la nueva ni la Pro

- **Qué se eligió:** `Ubuntu Server 24.04 LTS`, arquitectura **x86_64**.
- **Contra qué:** el desplegable ofrecía cuatro — `Ubuntu Server 24.04 LTS`,
  `Ubuntu Server 26.04 LTS`, `Ubuntu Pro 24.04 LTS` y `Ubuntu Pro 26.04 LTS`.
- **Por qué NO la 26.04**, que es la nueva y la que el asistente empuja:
  `deploy/install.sh` tiene **una sola corrida en su vida**, la del 2026-08-07 en
  un contenedor **Ubuntu 24.04** (`[L-024]`). Esa corrida es toda la evidencia de
  que el guion funciona. 🔑 **Cambiar de versión no lo rompe: lo deja sin medir**,
  que es peor de diagnosticar. Los tres sitios donde suele doler —nombres de
  paquete, el repositorio de Caddy y el Python del sistema— cambian entre
  versiones, y el fallo aparecería en la máquina de verdad, mezclado con el primer
  despliegue. Estrenar sistema operativo es un experimento aparte, y hoy ya hay
  uno abierto (`[A-018]`).
- 🚨 **Por qué NO la Pro, que es la trampa de dinero:** `Ubuntu Pro` es una
  **suscripción de pago** y añade un cargo **por hora** encima del de la instancia.
  Nada de lo que trae (parches extendidos, cumplimiento) hace falta aquí, y la
  máquina se cierra en seis meses. ❓ **La cifra exacta del recargo no se ha
  comprobado en pantalla** — no hace falta para la decisión: cualquier importe > 0
  la resuelve, porque el beneficio es cero. Regla 5 del proyecto.
- ⚠️ **El nombre es lo peligroso, no el precio.** "Pro" se lee como *"la versión
  buena"*, y aparece en la misma lista que la gratuita, con el mismo aspecto. Es la
  familia de `launch-wizard`: **una opción de pago preseleccionable por reflejo,
  sin un solo aviso**. Va escrita en `console_steps.md` por eso.
- **Consecuencia que hay que recordar en 5 meses:** el día que la 24.04 deje de
  recibir actualizaciones o el proyecto quiera saltar de versión, **lo que hay que
  volver a correr es `install.sh` en un contenedor de la versión nueva**, no
  probarlo directamente en la nube.

### [D-042] 2026-08-07 — La ausencia de `trusted_proxies` se vigila, no se explica

- **Qué se decidió:** que un test falle si `deploy/Caddyfile.template` declara
  `trusted_proxies`, en vez de dejarlo escrito como advertencia.
- **Por qué hace falta un guardián y no basta el comentario:** lo que se midió hoy
  —que Caddy descarta un `X-Forwarded-For` forjado— **no es una propiedad de
  Caddy: es una propiedad de esta configuración**. Caddy reescribe la cabecera
  porque no hay ningún proxy declarado de confianza. Con `trusted_proxies` puesto,
  se la cree.
- 🚨 **Y el fallo sería MUDO.** La app sigue contestando 200, no hay excepción, no
  hay renglón en el log. Lo único que cambia es que el freno de `/login` cuenta un
  origen **que elige quien ataca**, distinto en cada intento: no frena nunca.
  🔑 **Un comentario protege a quien lo lee. Quien copia una receta de internet no
  lo lee** — y ese es exactamente el camino por el que entraría la directiva.
- **Contra qué:**
  - **Dejarlo escrito y ya.** Era la opción por defecto y la que estaba sobre la
    mesa. Se descarta por lo de arriba: un fallo silencioso no admite un control
    que depende de la atención.
  - **Pinchar `header_up X-Forwarded-For` explícito en la plantilla.** Fija el
    valor, sí, pero **no impide** que alguien añada `trusted_proxies` después —
    así que no cubre el caso que preocupa. Y sería configuración nueva sin pedir
    (`PI-2`).
- **Es el SEGUNDO test que cruza a `deploy/`**, y por la misma razón que el
  primero (`[D-035]`): un acoplamiento real entre dos archivos que no se conocen,
  invisible desde Python. Se acepta el cruce con el mismo criterio, no con uno
  nuevo.
- ✅ **Cómo se midió, que es lo que lo hace un control y no una nota:**
  - **rojo sobre la plantilla DE VERDAD** — se le añadió `trusted_proxies static
    private_ranges`, falló solo ese test, y se deshizo. `[L-007]`: con el fallo
    puesto y sin él.
  - **rojo sobre las dos formas** en que Caddy acepta la directiva: el bloque
    global `servers { }` y dentro del propio `reverse_proxy`.
  - **ciego a los comentarios**: la plantilla y el propio test **nombran** la
    directiva para contar por qué no está. Un guardián que leyera la prosa se
    pondría rojo sobre su propia explicación, y el arreglo sería borrar la
    explicación — justo al revés.
- 📌 La plantilla revalidada con Caddy 2.11.4 real tras el cambio:
  `Valid configuration`, salida 0, sin marcadores sin sustituir. 348 → **351**.

### [D-041] 2026-08-07 — La EC2 se lanza el 08, después de la lectura, diga lo que diga

- **Qué se decidió:** la segunda mitad de `T-059` —lanzar la `t3.micro` y
  asociarle la Elastic IP ya reservada— **no se hace hoy**. Se hace el
  **2026-08-08**, y **después** de leer `Importe utilizado`. Sellado hoy, con el
  campo todavía sin leer.
- 🔑 **Lo que NO significa:** que la lectura sea un permiso. No hay veredicto de
  `[A-018]` que adelante el lanzamiento a hoy ni que lo cancele mañana. Lo que se
  sella es un **orden**, no una condición. Por eso se puede sellar hoy: no
  depende del número.
- **Contra qué:** contra lanzar hoy, que era lo que la lista de tareas pedía —
  `T-059` es el cuello de botella de `T-060b`, `T-061` y `T-062`, y la Elastic IP
  está cobrando por estar ociosa. Se paga un día más de esa IP a sabiendas.
- **Motivo 1 — lanzar hoy mata una medida irrepetible.** Con la EC2 encendida,
  la factura pasa a tener **dos** fuentes de gasto y el importe deja de poder
  atribuirse. Lo que se perdería es `t_cargo − t=0`: el retraso entre el primer
  cargo real del proyecto y el momento en que se ve en pantalla. 🚨 **Ese número
  solo se puede medir una vez en la vida de la cuenta** —hace falta una cuenta
  sin historial y una sola fuente de gasto— y luego sirve los seis meses enteros,
  cada vez que haya que decidir si un silencio es "todavía no" o "está roto".
- **Motivo 2 — encender la máquina antes de ver morder la alarma es `[LM.13]`.**
  Un control que nadie ha visto funcionar no es un control, es una promesa. Hoy
  la alarma no ha saltado **ni una vez**, y la EC2 es justo lo que multiplica el
  gasto que esa alarma tendría que vigilar. El orden correcto es ver el control
  morder con el gasto pequeño, no con el grande.
- 📌 **La Elastic IP no se suelta.** Se asocia mañana, como parte de esa misma
  mitad. Soltarla y pedir otra después reiniciaría el `t=0` de las 15:29 UTC del
  2026-08-06, que es exactamente el reloj que el experimento está midiendo.
- **Consecuencia para hoy:** el trabajo del día es `T-055`, la mitad de Caddy,
  reclasificada ayer como medible en contenedor sin EC2.

### [D-040] 2026-08-07 — El criterio de lectura de `A-018` se sella HOY, no mañana

- **Qué se decidió:** enmendar la tabla sellada del experimento de la alarma
  **antes** de la lectura del 2026-08-08, en vez de interpretarla con el número
  delante. El detalle vive en `[A-018]`; aquí queda **por qué** se hizo hoy.
- **Contra qué:** contra dejarlo para mañana, que era lo cómodo — la tabla ya
  existía y "solo" había que leerla.
- 🔑 **Por qué manda la fecha:** el valor entero de una tabla de lectura está en
  **existir antes del dato**. Enmendada mañana, con el `0,00` en pantalla, deja de
  ser un criterio y pasa a ser una racionalización. Es la misma regla que hizo
  valioso el sellado original; aplicarla al **papel viejo** y no solo al dato
  nuevo es lo que faltaba.
- **Las tres piezas que se sellaron:**
  1. **Fila 3 anulada, no borrada.** Nombraba una causa —"aplican las 750 h
     gratis de IPv4"— **desmentida hoy**: esas horas son para direcciones en uso,
     la nuestra está ociosa y cobra. Se anula a la vista porque la original está
     en `cfba50a` y se lee con autoridad.
  2. **Guardia sobre la fila 2:** "alarma rota" exige **≥12 h de silencio después
     de que el importe sea visible**. 🔴 **El MOTIVO se corrigió DOS veces el mismo
     día.** Se escribió primero que salía de sumar `~24 h + 8–12 h = 36 h`. Luego
     se dijo que **era** doble conteo. **También eso afirmaba de más.**
     ✅ **Redacción final, con un solo desconocido:** *no se sabe si lo que se
     MUESTRA (`Importe utilizado`) y lo que se EVALÚA (el umbral) comparten
     reloj.* De ahí cuelgan las dos ramas, y **ninguna está descartada**:
     - **si comparten reloj** → ver el importe implica que la evaluación ya pasó;
       falta solo la entrega del correo: **minutos**. La suma sería doble conteo.
     - **si van desacoplados** → la consola calcula en vivo y la evaluación va por
       su ciclo: **horas**. La suma `24 + 12` sería aproximadamente correcta.

     La regla se queda porque **errar hacia esperar de más no produce ninguna
     conclusión falsa, solo tarda** — y eso vale en las dos ramas.
     🔑 **La forma del error vale más que el error:** una regla **correcta**
     sostenida por una razón que podía no serlo. Es `[D-039]` con el signo
     cambiado — allí el motivo estaba **mudo**; aquí **hablaba, y podía mentir**,
     que es peor: un motivo escrito se lee como verificado.
     🚨 **Y el segundo intento cayó en lo mismo, dentro del texto que corregía lo
     primero.** Decir *"era doble conteo"* **es afirmar que comparten reloj** —
     exactamente el dato que la misma frase declaraba desconocido. Un seto y una
     afirmación sin seto conviviendo, sobre el **mismo** desconocido. Que `h2 − h1`
     lo vaya a resolver mañana no lo hace sabido hoy.
     📌 **Se anota como patrón, no como anécdota:** ya salió como *"una lección con
     su propio control no es un buen propósito"*. **El texto que documenta una
     corrección no está exento de la corrección que documenta.**
  4. **Se anotan DOS horas, no una** — `h1` (importe visible > 0,01) y `h2`
     (llega el correo). `h2 − h1` es un número que **no tiene nadie, ni la
     documentación**, y decide la duda de arriba gratis: minutos ⇒ comparten
     reloj; horas ⇒ desacoplados. La espera deja de ser tiempo muerto y pasa a
     ser la **segunda medición** del experimento (`LM.19`).
  5. **_"Actualizar plan" sale de la lista de `T-068`_** y pasa al **protocolo de
     lectura**. No es la puerta 8: las siete hay que ir a buscarlas, y esta está
     en la cabecera de la página que el experimento obliga a abrir **a diario**.
     El riesgo se mide por el **tráfico**, no por la peligrosidad. Ver `[L-026]`.
  3. **El precio del cambio de instrumento queda escrito:** premisa y prueba
     cuelgan ahora del mismo servicio; el experimento **ya no cubre** un fallo en
     la entrada de datos al presupuesto.
- 🔴 **Y se retira un número propio: las "32 h".** Se habían escrito esa misma
  mañana como holgura suficiente. La documentación las dejó **cortas** —son dos
  retrasos en serie, ~24 h + 8–12 h ≈ 36 h—, así que no eran solo arbitrarias:
  eran falsas. 🔑 Es la **regla 6** una vez más: **un número sin corrida detrás**, y en
  un archivo que existe justo para prohibirlos.

### [D-039] 2026-08-07 — La precedencia no se toca: se hace audible

- **Qué se decidió:** que **el entorno siga ganándole al `.env`**
  (`os.environ.setdefault`), y que lo que cambie sea que **el arranque diga de
  dónde salió el valor**. Función nueva `config.value_origin`, y el renglón de
  `log_data_dir` pasa a `Datos de las personas en <ruta> (TEAPP_DATA_DIR,
  origen: .env | entorno)`.

- **Contra qué se decidió:** contra invertir la precedencia para que el `.env`
  fuera la fuente de verdad. 🚨 **La pregunta estaba mal planteada** —se ofreció
  un binario "invertir" o "solo tocar el comentario"— y las dos ramas eran malas:
  una cambia comportamiento del que dependen cosas, la otra deja el problema
  vivo. La tercera vía la trajo una revisión externa.

- 🔑 **Por qué la regla es correcta, dicho como toca:** el `.env` es la
  configuración **por defecto de esta máquina**; el entorno es **esta corrida en
  concreto**. Lo específico gana a lo general, que es la convención de todo el
  mundo. El entorno **no es un descuido: es el canal deliberado de anulación** —
  el que usan `pytest`, un contenedor y cualquier corrida de una sola vez.
  📌 Se había razonado al revés, con una metáfora que lo empeoraba ("contrato
  firmado contra nota adhesiva"): pintaba de accidente lo que es un mecanismo.

- **Entonces, ¿cuál era el defecto?** Que la regla estaba **muda**. Quien anula
  desde el entorno lo hacía sin dejar rastro, incluida `TEAPP_DATA_DIR`, que
  desde `[D-037]` decide dónde viven los datos de las personas. Es `[L-015]`
  otra vez: un instrumento mudo se lee como confirmación.

- 🧪 **Y aquí una corrección, porque el argumento que cerró la decisión estaba
  medio pasado de rosca.** La revisión sostuvo que invertir la precedencia haría
  que *"los 342 tests empezaran a escribir en `data/`"*. **Se midió y no pasa.**
  Sabotaje en el contenedor —`os.environ.setdefault` → `os.environ[name] =
  value`, con el `.env` apuntando a `/opt/teapp/data`—: **346 pasaron, `data/`
  con 0 archivos**, y los dos únicos rojos fueron los tests nuevos de esta misma
  decisión.

  **Por qué no pasa, que es lo que hay que saber:** `load_env_file()` corre **una
  vez**, al importar `app/api.py`. Después, el fixture `autouse` de
  `conftest.py` hace `monkeypatch.setenv` **por cada test**, y `[D-036]` obliga a
  resolver la ruta en cada llamada en vez de guardarla al importar. Esas dos
  piezas sostienen el aislamiento aunque la precedencia se invierta.

  🔑 **La decisión no cambia; el motivo sí.** Un motivo falso sostiene bien hasta
  el día que alguien lo comprueba.

- 🚨 **Y el motivo BUENO apareció al perseguir el falso: el riesgo no vive en la
  suite, vive FUERA de ella.** `pytest` sobrevive a invertir la precedencia
  porque tiene un fixture `autouse` que desvía en cada test. **Un guion suelto no
  tiene fixture.** `create_account.py:96`, `measure_body.py` o cualquier corrida
  de una vez llaman a `load_env_file()` y ahí se acaba: nadie pisa nada después.

  Medido en contenedor, con `TEAPP_DATA_DIR=/tmp/desvio_de_la_corrida` exportada:

  | precedencia | dónde escribiría `create_account.py` |
  |---|---|
  | **buena** (entorno gana) | `/tmp/desvio_de_la_corrida` — obedece |
  | **invertida** (`.env` gana) | 🔴 `/opt/teapp/data` — **los datos de verdad** |

  🔑 **Eso es `T-072` exacta, otra vez:** `measure_body.py`, fuera de `pytest`,
  escribiendo donde no debía. Y es `[A-020]` con otro disfraz — el camino que el
  portero de `no_data_writes.py` no ve, porque ese portero vive dentro de
  `pytest` y una báscula corre fuera (`[L-023]`).

  📌 **La conclusión de la revisión era correcta apuntando al blanco
  equivocado**, y eso es más útil de anotar que "tenía razón": el sitio donde
  vive este riesgo ya mordió a este proyecto esta misma semana.

- ⚠️ **Punto ciego de `value_origin`, escrito antes de que alguien lo descubra a
  las tres de la mañana:** compara valores, así que **cuando el entorno y el
  `.env` traen el mismo valor no los distingue** — dirá `.env` viniendo del
  entorno. Es benigno (el valor efectivo es el mismo, nadie anula nada), pero
  marca qué mide de verdad este renglón: **delata anulaciones, no procedencias**.

- ✅ **Sabotaje del control, por los DOS lados.** Uno solo habría dejado la mitad
  de los tests verdes por la razón equivocada:

  | `value_origin` fijada en | qué cae |
  |---|---|
  | `"entorno"` | los **2** que afirman `.env` |
  | `".env"` | los **4** que afirman `entorno`, `sin valor` y el renglón del log |

  Seis tests nuevos en `tests/test_config.py`, 342 → **348 verdes**.

- 🧹 **Y de aquí salieron dos menciones muertas EN CÓDIGO**, las dos con la misma
  frase, describiendo una plataforma descartada en `[D-029]`: `app/config.py` en
  el docstring de `load_env_file`, y `app/api.py:40-42`. Ver `[L-025]`.

### [D-038] 2026-08-07 — En el guion de instalación, el `.env` que ya existe manda

- **Qué se decidió:** que `install.sh` **lea** `TEAPP_DATA_DIR` del `.env` que ya
  exista **antes** de decidir dónde crear la carpeta de datos. Contra la
  alternativa que había: fijar siempre `${INSTALL_DIR}/data` y crearla de entrada.

- 🚨 **Por qué, y es peor de lo que parece.** El `mkdir -p` corría **antes** del
  `if` que mira el `.env` (`install.sh:126-129`). El bloque de más abajo sí
  respetaba un `TEAPP_DATA_DIR` ya escrito — pero para entonces la carpeta vacía
  ya estaba creada. Reinstalar sobre una máquina cuyos datos se hubieran movido a
  otro disco dejaba **un `data/` vacío al lado de la app**, que no usa nadie.
  🔑 **Es literalmente el señuelo que `[D-037]` existe para evitar** —*"una
  carpeta vacía y quien use la app parecería haber perdido su marcador"*—, solo
  que fabricado por el propio guion. Un freno que crea con la mano el accidente
  del que protege.

- 🧪 **MEDIDO, no leído. Corrida del 2026-08-07 en contenedor Ubuntu 24.04**
  (ver `[L-024]`), con el `.env` apuntando a `/mnt/otro_disco/teapp-data`:

  | corrida | ¿aparece el señuelo `/opt/teapp/data`? | ¿se crea el disco real? |
  |---|---|---|
  | guion **viejo** (`HEAD`, sin el arreglo) | 🔴 **SÍ**, vacío, 0 archivos | ❌ no |
  | guion **arreglado** | ✅ no | ✅ sí, `/mnt/otro_disco/teapp-data` |

  🔑 **El guion viejo es el control rojo.** Sin él, el verde del arreglado no
  demostraría nada: no se sabría si el señuelo desapareció por el arreglo o si
  nunca hubo forma de provocarlo (`[LM.13]`).

- ✅ **Y el freno se vio morder:** con `TEAPP_DATA_DIR=datos_relativos` (relativa)
  el guion imprime `ERROR: el .env existente tiene TEAPP_DATA_DIR vacia o
  relativa.` y sale con `exit=1`. Antes de esto, una línea vacía habría reventado
  el `mkdir` con un error del sistema ilegible, y una relativa habría creado la
  carpeta donde tocara estar parado. Las dos son `[D-037]` otra vez.

- 📌 **De dónde salió:** de una revisión externa que **leyó** el guion y avisó del
  señuelo marcándolo como *"leído, no corrido"*. La lectura era correcta y la
  corrida lo confirmó. La honestidad de la etiqueta es lo que hizo que se
  comprobara en vez de creerse.

### [D-037] 2026-08-06 — La raíz de los datos sale del entorno, y sin ella no se arranca

- **Se eligió:** una variable, `TEAPP_DATA_DIR`, **sin valor por defecto**. De ella
  cuelgan los tres sitios que hoy se resuelven cada uno por su cuenta:
  `accounts.json`, `users/` y `quota/`. Si la variable falta, o si la carpeta a la
  que apunta no existe, **la app no arranca** y lo dice nombrando la variable.

- **Contra**, cuatro alternativas, y ninguna es de paja:

  | alternativa | por qué se descarta |
  |---|---|
  | Dejarlo como está (`PROJECT_ROOT / "data"` por defecto) | es exactamente el fallo de `[L-023]`: el defecto es la carpeta real, así que **olvidarse escribe en los datos de personas**. Falla hacia el lado peligroso |
  | La variable, pero **con** defecto `data/` | la misma criatura con mejor ropa. Quien se olvide sigue escribiendo en los datos reales, solo que ahora creyendo que hay un mecanismo |
  | Pasar la ruta por parámetro desde arriba en cada llamada | `PI-2`: toca todas las rutas para no resolver el problema — el parámetro sigue teniendo un valor por defecto al final del camino, y olvidarse vuelve a caer ahí |
  | Un "modo test" que redirija (`TEAPP_TESTING=true`) | 🚨 invierte el criterio del proyecto: sería seguro **solo si te acuerdas**, y el interruptor es justo lo que se olvida. Es lo que ya falló |

- **Por qué.** El aislamiento de hoy necesita **tres** desvíos y depende de que
  quien escriba un script se acuerde de los tres. La báscula de `T-054` se acordó
  de uno (`[L-023]`). Esto lo convierte en **uno solo, y que si se olvida no
  arranca** — es el criterio de `_context/architecture.md`, denegar por defecto, y
  el patrón que este proyecto **ya usa dos veces**: `require_secret` se niega a
  inventar una llave, y `registration_open` exige la palabra exacta para abrir.
  No es un patrón nuevo; es el de casa.

- 🔑 **Se decide hoy por FECHA, no por importancia.** Hoy es un refactor de unos
  pocos archivos. En cuanto exista la EC2 es una migración con ficheros de
  personas dentro. La máquina está bloqueada por el experimento de `[A-018]` hasta
  el **2026-08-07, 15:29 UTC**, así que la ventana en que esta puerta **no** es de
  una sola vía es exactamente hoy.

- **Qué pasa con la `data/` que ya existe en disco: NADA se mueve.** El valor que
  se pone en el `.env` local apunta a la carpeta que ya está, así que los siete
  archivos siguen donde están, con su contenido. Lo único que cambia es que
  **ahora hay que decir dónde están**. En el servidor la variable apuntará al
  disco que persiste (`[D-029]`), y a partir de ahí mover los datos no exige tocar
  código: se cambia una línea del `.env`.

- ⚠️ **La app NO crea la carpeta raíz.** Solo crea `users/` y `quota/` dentro, que
  es lo que ya hace. Si la raíz no existe, se niega. El motivo: una ruta mal
  escrita crearía un `data/` vacío y **todo el mundo parecería haber perdido su
  marcador** — un fallo mudo, de la familia de `[L-032]` (antes `[A-008]`). Crear la carpeta es un
  acto de instalación, deliberado, y va en `install.sh`.

- 🚨 **Tres cosas del mismo cambio que se harían mal si se dejan para después:**
  1. **El portero de `no_data_writes.py` NO sigue la variable.** `REAL_DATA_DIR`
     se queda colgando de la ruta del propio archivo. Si siguiera a
     `TEAPP_DATA_DIR`, en la suite vigilaría la carpeta temporal: verde siempre,
     mirándose a sí mismo. Ya hay un control que lo exige
     (`test_the_doorman_looks_at_the_real_folder_not_a_diverted_one`) y hay que
     dejarlo mordiendo.
  2. **La regla operativa de `no_data_writes.py` queda mintiendo.** Dice "desvía
     los TRES sitios", y con esto los tres se vuelven uno. Se corrige **en el
     mismo commit**: es el bicho de las sesiones 33 y 41 (`[L-018]`), la misma
     regla en dos sitios diciendo cosas contrarias, y está a un commit de
     distancia.
  3. **`create_account.py` y `main.py` no llaman a `load_env_file()`** — hoy no
     les hace falta porque las rutas tienen defecto. Con este cambio dejarían de
     funcionar, y `create_account.py` es **la herramienta con la que se crea la
     primera cuenta en el servidor** (`[D-027]`). Se arregla aquí o el paso 7 se
     encuentra con ella rota.

- **Toca:** `app/config.py` (la función que resuelve la raíz, resuelta **dentro**,
  nunca como constante de módulo — `[D-036]`), `app/tools.py`, `app/quota.py`,
  `app/accounts.py`, `create_account.py`, `main.py`, `tests/conftest.py` (tres
  `setattr` → una variable), `tests/no_data_writes.py` (la regla),
  `tests/test_config.py` (nuevo), `.env.example`, `README.md`, y `deploy/`
  (`install.sh` crea la carpeta y escribe la variable; `teapp.service` no cambia,
  porque el `.env` se lee al importar `app/api.py`).

- ✅ **Hecho el 2026-08-06.** 342 tests en verde (13 nuevos), `data/` sin tocar, y
  el arranque comprobado **con uvicorn de verdad** y no solo con `TestClient`
  ([L-010]): `GET /` contesta 200, `/practice` sin sesión contesta 401, y el log
  escribe la ruta resuelta. Comprobado también el lado que importa: **sin la
  variable, el import de `app/api.py` se niega** con el mensaje que dice qué
  poner.

- 📌 **Y deja `T-066` con algo concreto que comprobar.** "Que el disco persista"
  era vago; lo que se comprueba ahora es que la carpeta a la que apunta
  `TEAPP_DATA_DIR` sobrevive a un reinicio con los marcadores dentro.

### [D-036] 2026-08-06 — El marcador se aísla en el origen, y lo vigila un portero

- **Se eligió:** cambiar `app/tools.py` para que `score_file`, `read_score` y
  `add_point` resuelvan la carpeta **dentro** de la función (`users_dir=None`),
  desviar `tools.USERS_DIR` una sola vez en `conftest.py`, borrar los tres
  maniquíes, y poner un **portero** (`tests/no_data_writes.py`) que compara la
  huella del contenido de `data/` antes y después de cada test.
- **Contra:** dos alternativas, y las dos se descartaron por lo mismo.
  1. **Subir el maniquí a `conftest.py`** — quitaba la duplicación sin tocar
     `app/`, pero dejaba el doble puesto para siempre. El camino completo (ruta →
     agente → marcador → disco) se quedaba sin un solo test que lo recorriera:
     un verde fabricado, que es el defecto al que `[L-020]` acababa de ponerle
     nombre.
  2. **Un test que comprobara que `add_point` escribe en `tmp_path`** como único
     testigo — vigila a **un inquilino**. El día que aparezca otro camino hacia
     `data/`, sigue verde sin mirar. Se escribió igualmente, pero como segunda
     pieza, no como la que aguanta el peso.
- **Por qué:** el valor por defecto de un parámetro se evalúa **una sola vez, al
  importar el módulo**. `users_dir: Path = USERS_DIR` congelaba `data/users/`
  dentro de las tres funciones, y por eso el desvío no era posible: no era una
  preferencia de los tests, era una consecuencia de la firma. `quota.py` ya lo
  había resuelto así —explicado en su propio docstring, `app/quota.py:129`— y
  `tools.py` era la excepción
  que nadie recordaba.
  🔑 **El portero vigila la puerta, no al inquilino.** No pregunta quién escribe
  ni por qué: pregunta si `data/` cambió. Un test escrito dentro de un año por
  alguien que no leyó nada cae igual. Misma idea que `no_network.py`, que no
  vigila a `english_tutor` sino a `connect`.
- **Tres condiciones que hacen que el portero no sea decorativo:**
  - Compara **contenido** (`md5`), no `iterdir()`. Un `{"score": 5}` que pasa a
    `6` no crea ningún archivo — sería `[L-020]` cometido dentro del arreglo de
    `[L-020]`.
  - Vigila **por test**, no por sesión: con 329 tests, un salto al final sin
    nombre deja buscando a ciegas.
  - `REAL_DATA_DIR` cuelga de la ruta del propio archivo, **no** de
    `tools.USERS_DIR`: un portero que mirase la ruta desviada se estaría mirando
    a sí mismo, verde siempre.
- **Se midió, no se supuso:** quitar la línea del `conftest.py` pone rojo —
  `DataTouched: cambio el contenido de users\juan.json`, más el test del
  inquilino fallando. Y `tests/check_no_data_writes.py` (6 controles, fuera de
  `test_*.py` como `check_no_network.py`) demuestra que el portero muerde cuando
  nadie lo sabotea. 329 tests verdes; `data/` bit a bit intacta antes y después.
- ⚠️ **Lo que este arreglo NO cubre, escrito para que no sorprenda:** el portero
  vive dentro de pytest. Un script suelto, `uvicorn` a mano o cualquier cosa
  fuera de la suite escribe en `data/` de verdad y no lo ve **ni lo verá nunca** —
  misma frontera que los subprocesos de `no_network.py`. No es hipotético: el
  2026-08-06 a las 14:48:33 aparecieron a la vez `data/users/otronombrelargo.json`
  y `data/quota/otronombrelargo.json`, cinco prácticas de una cuenta que no existe
  en `data/accounts.json`. No pudo ser pytest. **Tarea aparte, no se mezcla con
  `T-071`.** La evidencia completa —con las fechas, que ya no están en disco por
  `[L-022]`— y **el culpable, ya identificado en `T-072`: la báscula de `T-054`,
  que desvió las cuentas y se olvidó del marcador y la cuota** — están en
  `[L-023]`.
- ⚠️ **Segundo punto ciego, descubierto el mismo día:** la huella es de bytes, así
  que el portero no ve fechas ni permisos. Ver `[L-022]`.
- **Toca:** `app/tools.py`, `tests/conftest.py`, `tests/no_data_writes.py`,
  `tests/check_no_data_writes.py`, los tres archivos de tests que llevaban el
  maniquí, y `T-071`.

### [D-035] 2026-08-06 — El tope de cuerpo, medido; y un test que cruza a `deploy/`

- **Se eligió:** dejar `max_size 16KB` en `deploy/Caddyfile.template`, cambiar su
  comentario de criterio a medida, y escribir `tests/test_deploy_limits.py`, que
  **lee el número del propio Caddyfile** y lo compara con el peor caso que
  `MAX_SENTENCE_LENGTH` permite.
- **Contra:** (a) dejar el número como estaba, con su "por criterio"; (b) escribir
  el test copiando el 16 KB a mano; (c) no escribir test y confiar en el
  comentario.
- **Lo que se midió** (2026-08-06, app real vía `TestClient`, frase de 500
  caracteres, que es el máximo que acepta):

  | alfabeto | cuerpo | % de 16000 |
  |---|---|---|
  | inglés (ASCII) | 516 B | 3,2 % |
  | español con tildes | 1016 B | 6,4 % |
  | chino | 1516 B | 9,5 % |
  | emoji (UTF-8 crudo) | 2016 B | 12,6 % |
  | **emoji escapado `\uXXXX`** | **6016 B** | **37,6 %** |

  Los cinco contestan **200** — que es la prueba que exigía el enunciado de
  `T-054`: el freno no puede romper el caso normal.
- 🔑 **Lo que un número a ojo no ve: un carácter cuesta entre 1 y 12 bytes.**
  `MAX_SENTENCE_LENGTH` acota **caracteres**. Un emoji ocupa 4 bytes en UTF-8,
  pero JSON permite escribirlo con dos escapes `\uXXXX` seguidos —un *surrogate
  pair*— y eso son **12 bytes ASCII para un solo carácter**. No es un ataque: es
  lo que produce cualquier cliente que serialice con `ensure_ascii=True`, el
  valor por defecto de Python. Por eso el peor caso legítimo es 6016 y no 2016.
- ⚠️ **El criterio anterior no estaba solo sin medir: estaba mal.** Decía "no
  llegan a 2 KB" y el peor caso es 6 KB — un factor de 3. Los 16 KB estaban bien
  **por suerte**, no por cálculo. Un tope puesto "a unos pocos KB", que era el
  enunciado literal de `T-054`, habría roto el uso normal con emoji.
- **Por qué (b) se descarta —y es lo más fino de la decisión:** copiar el número
  al test crearía una **tercera** copia (Caddyfile, test, máquina), y sería
  justamente el archivo que existe para cazar números descoordinados quien
  introdujera uno. El test **parsea** el Caddyfile: una sola fuente.
- 🚨 **`KB` son 1000, no 1024.** Caddy lee estos tamaños con go-humanize, donde
  `KB`=1000 y `KiB`=1024. Un test escrito contra 16384 se pondría **verde en una
  franja de 384 bytes donde Caddy ya devuelve 413**: un control verde midiendo un
  número que no rige, que es la misma familia de fallo que `[L-019]`.

  ✅ **MEDIDO el 2026-08-07 — esto estaba "leído, no medido" y ya no lo está.**
  Caddy 2.11.4 real, en contenedor y sin nube (`[L-024]`). Dos medidas
  independientes, cada una con su control:

  | qué se midió | resultado | control |
  |---|---|---|
  | `caddy adapt` sobre `Caddyfile.template` | `"max_size":16000` | `16KiB` → `16384` |
  | cuerpo real por Caddy → uvicorn | 16000 B → 401 · **16001 B → 413** | 16384 B → 413 |

  🔑 **El 401 es lo que hace válida la fila:** es de la app, por falta de sesión,
  así que prueba que el cuerpo **llegó**. Y uvicorn directo contesta 401 a los
  cinco tamaños, luego el 413 es de Caddy y de nadie más. El borde cae **exacto**
  entre 16000 y 16001. 📌 El número conservador era el correcto: la tabla
  `UNIDADES` de `tests/test_deploy_limits.py` no cambió. Con esto muere `[A-019]`,
  que existía solo para registrar que este párrafo no estaba pesado.
- **Por qué se acepta que un test lea `deploy/`:** es el primero de TEAPP que
  cruza esa frontera, y se hace a sabiendas. El acoplamiento entre
  `MAX_SENTENCE_LENGTH` (caracteres, en `app/`) y `max_size` (bytes, en
  `deploy/`) **es real y hoy no lo vigila nadie**. Si se separan, Caddy rechaza
  frases legítimas con 413 y **en Python no falla nada**, porque la petición
  nunca llega: el síntoma sale en producción, contado por quien usa la app. El
  test convierte ese fallo mudo en rojo antes de desplegar.
- **Sabotajes hechos** (`[L-019]`: resultado **y** montaje):
  - 🔑 **`MAX_SENTENCE_LENGTH` de 500 a 5000** → **4 rojos** (el de acoplamiento,
    más español, chino y emoji). ✅ **Este es EL sabotaje**, y lo aportó la
    auditoría: es el único que ataca el escenario que el test dice existir para
    cazar —alguien sube el límite de Python y se olvida del tope de Caddy—.
    Los otros cuatro atacan el Caddyfile y el conversor, o sea el instrumento.
    ⚠️ **Un guardián al que solo se le sabotea el instrumento no ha demostrado
    que muerda en su propia dirección.**
  - `max_size 4KB` → rojo, en las dos pruebas de acoplamiento ✅
  - directiva comentada → falla con el mensaje que explica qué pasó, no en verde ✅
  - conversor devolviendo el número sin aplicar la unidad → 8 rojos ✅
  - el número escrito en un **comentario** del Caddyfile no se lee como si rigiera ✅
- **Lo que este test NO mide:** que Caddy devuelva el 413 de verdad. Eso necesita
  el binario, y llega con `T-061`.

### [D-034] 2026-08-06 — El origen real lo resuelve uvicorn, y las banderas se escriben igual

- **Se eligió:** dejar `_request_origin` **sin tocar** en `app/api.py`, y añadir
  `--proxy-headers --forwarded-allow-ips 127.0.0.1` explícitas al `ExecStart` de
  `deploy/teapp.service`.
- **Contra:** (a) leer `X-Forwarded-For` a mano dentro de `_request_origin` —el
  arreglo obvio, y el peligroso—; y (b) no escribir nada, apoyándose en que las
  dos banderas ya son el valor por defecto de uvicorn.
- **Por qué (a) se descarta:** esa cabecera **la escribe cualquiera**. Leerla sin
  comprobar de dónde viene la petición no es un freno flojo, es un freno
  **inservible**: quien ataca pone una dirección distinta en cada intento, cae en
  un cubo nuevo cada vez y no se frena nunca. uvicorn ya trae esa comprobación
  hecha y auditada; reescribirla en `app/api.py` sería una pieza más que mantener
  para hacer peor lo mismo (PI-2).
- **Por qué (b) se descarta:** es el mismo argumento de `[D-027]` con
  `TEAPP_REGISTRATION_OPEN`. 🔑 **Un valor por defecto no es una decisión: es una
  coincidencia que hoy nos conviene.** El día que alguien actualice uvicorn y el
  defecto cambie, la app queda cerrada para todos y **no hay ningún error que lo
  explique** — el síntoma es un 429 perfectamente normal.
- **Lo que se midió** (2026-08-06, uvicorn 0.52.1 real, no `TestClient`):

  | escenario | llega desde | `X-Forwarded-For` | origen que cuenta el freno |
  |---|---|---|---|
  | Caddy normal | `127.0.0.1` | `203.0.113.7` | ✅ `203.0.113.7` |
  | cabecera falsa + la real que añade Caddy | `127.0.0.1` | `9.9.9.9, 203.0.113.7` | ✅ `203.0.113.7` |
  | sin cabecera (como hoy en local) | `127.0.0.1` | — | ✅ `127.0.0.1` |
  | **suplantador** | `192.168.40.5` | `203.0.113.7` | ✅ `192.168.40.5` — **ignorada** |

  La segunda fila es la que importa y no era obvia: uvicorn recorre la cadena
  **al revés** buscando el primer host no confiable
  (`uvicorn/middleware/proxy_headers.py`, `get_trusted_client_address`). Como
  Caddy **añade** la dirección real al final, la cabecera que traiga quien ataca
  queda delante y se descarta sola.
- ⚠️ **Esto no cierra `T-055` entero.** La otra mitad no vive en el código: si el
  cortafuegos (`T-060`) deja el 8000 abierto, cualquiera le habla a uvicorn desde
  fuera y `--forwarded-allow-ips` no le sirve de nada — su dirección no sería
  `127.0.0.1`, sí, pero entonces el freno cuenta bien y el problema es otro: **se
  saltó Caddy entero**, sin HTTPS y sin tope de cuerpo. Las dos capas o ninguna.
- **Toca:** `deploy/teapp.service`, `T-055`, `T-060` (cortafuegos), `T-066` (la
  corrida que lo confirma en la máquina de verdad), `[A-014]`, `[L-019]`.

### [D-033] 2026-08-06 — La región: todo TEAPP vive en `us-east-1`

- **Se eligió:** `us-east-1` (Norte de Virginia) como la región **única** de todo
  el paso 7 — Elastic IP, instancia EC2, y lo que venga después.
- **Contra qué:** `us-east-2` (Ohio), que era lo que la consola **traía puesto
  por defecto**. 📌 No se descartó por mala: se descartó porque **nadie la había
  elegido**, y esa es la diferencia entre una decisión y una herencia.
- **Por qué `us-east-1`:**
  - `[A-015]` ya calcula con esa región (`t3.micro`, Linux, `us-east-1`,
    $0.0104/hora). Elegir Ohio obligaba a comprobar precios y **corregir esa
    tabla en el mismo acto**, trabajo de papel a cambio de nada.
  - Virginia está geográficamente más cerca que Ohio de quien construye esto. Es
    un motivo menor y **no medido** — no se ha cronometrado nada.
- ⚠️ **Lo que NO se comparó, y se dice para que nadie lo lea como que sí:** los
  precios entre regiones. No se comprobaron. La regla 6 impide escribir un número
  sin corrida detrás, así que **el precio no fue el criterio** — lo fue la
  coherencia con `[A-015]`.
- 🚨 **Por qué se decidió AHORA y no cuando tocara lanzar la máquina:** una región
  no es una preferencia, **es un sitio**. Lo que vive en una no se ve desde otra.
  Una Elastic IP reservada en Ohio no sirve para una instancia en Virginia: hay
  que soltarla y pedir otra, **la nueva es una dirección distinta**, y
  `teapp.duckdns.org` habría que reapuntarlo dos veces.
  🔑 **Hoy el cambio es un clic porque no existe nada.** Cada cosa que se cree
  encarece ese clic.
- 🔑 **Y así es como se usa `[L-018]` en vez de solo sufrirlo.** La región estaba
  escrita en **un** sitio (la estimación de `[A-015]`) y a punto de decidirse en
  **otro** (un desplegable de la consola). **La segunda copia nace en el clic.**
  Hasta ahora las copias se cazaban *después* de divergir; esta se cazó antes de
  que la segunda existiera. Es la forma barata de usar un catálogo de fallos: no
  como anécdota, como detector.

### [D-032] 2026-08-05 — TEAPP corre como `ubuntu`, y no como un usuario propio

- **Se eligió:** que el servicio de la nube corra con el usuario `ubuntu` —el
  mismo con el que se administra la máquina— **contra** la práctica estándar de
  crear un usuario propio, sin contraseña y sin permisos, solo para la app.
- **Por qué, y es una razón concreta, no pereza:** `create_account.py` (`T-064`)
  lo ejecuta a mano quien administra, y escribe **el mismo `data/`** que el
  servidor. Con dos usuarios distintos, cada archivo que crea uno queda con
  permisos que el otro no puede tocar, y el fallo no aparece al instalar:
  aparece **días después**, la primera vez que se crea una cuenta nueva. Es
  además el terreno de `[A-002]`, donde el candado ya es delicado.
- ⚠️ **Lo que se está aceptando, dicho claro:** si alguien lograra ejecutar
  código dentro de TEAPP, lo haría con un usuario que **puede usar `sudo`**. Con
  un usuario propio, ese mismo fallo se quedaría encerrado en la carpeta de la
  app. **Es una decisión que en un producto de verdad no se tomaría así.**
- **Por qué aquí sí:** la máquina es desechable y vive 6 meses (`[C-003]`), no
  guarda nada irremplazable —`data/` son marcadores de práctica de inglés—, y el
  proyecto ya trae cinco cosas nuevas a la vez. Es PI-2: **¿hace falta para que
  esto funcione hoy?**
- 🔑 **Qué la revertiría, para que no se quede puesta por inercia:** el día que
  `data/` guarde algo que duela perder, o que el paso 8 meta la llave de Claude
  en esa máquina. Con dinero real dentro, el cálculo cambia de lado.

### [D-031] 2026-08-05 — Cómo se abre la cuenta: alias en el correo, y MFA desde el minuto uno

- **Se eligió:** registrar la cuenta con un **alias `+aws`** del correo personal
  (la forma `usuario+etiqueta@gmail.com`, que llega a la misma bandeja), y
  **activar MFA en el usuario root en el mismo acto de crear la cuenta**, no
  después.
- 🚨 **El valor literal del correo NO se escribe en este repo, y es deliberado.**
  `jdrodriguez1000/TEAPP_Aplication` es **público**, y hasta hoy el correo
  personal no aparecía en él: los commits van con la dirección `noreply` de
  GitHub. Escribirlo aquí sería meterlo en el historial de Git **para siempre**,
  porque borrarlo mañana no lo saca de los commits de ayer.
  - **Y no es solo privacidad.** El correo del root es **una de las dos mitades de
    la recuperación** de una cuenta de AWS. Publicar *"esta dirección exacta es
    el root de una cuenta de AWS"* regala media llave. El MFA cubre la otra
    mitad — razón de más para no entregar la primera.
  - 📌 **Lo que se escribe es el patrón, no el valor.** Quien lea el repo entiende
    la decisión; nadie se lleva la dirección.
- **Por qué el alias:** el correo entra igual en la bandeja de siempre, pero deja
  ver de un vistazo qué llega de AWS y permite filtrarlo. Cuesta cero.
- 🚨 **Y lo que el alias NO es, para que nadie lo lea mal dentro de tres meses:**
  no es una forma de sacar un segundo plan gratuito. `[C-006]` ata la
  elegibilidad a **la identidad y la tarjeta, no al correo**. Abrir una segunda
  cuenta con otro alias **no da más créditos: deja inelegible también la que ya
  se tenía**. El alias es organización, no un truco.
- **Por qué el MFA en el mismo momento y no "cuando haya tiempo":** el root es el
  usuario al que **no se le pueden poner límites** — es el dueño de todo, y de él
  cuelga la capacidad de cruzar al plan de pago de `[C-005]`, que no tiene vuelta
  atrás. 🔑 **Un MFA aplazado se aplaza para siempre**, porque nunca hay un día
  en que apetezca.
- ⚠️ **La trampa del MFA, que hay que resolver el mismo día:** si el segundo
  factor vive solo en el móvil y el móvil se pierde o se restablece, **el root
  queda inaccesible** — y recuperarlo con AWS es lento. Al montarlo hay que dejar
  resuelto un camino de vuelta: un segundo dispositivo de MFA, o los códigos de
  recuperación guardados fuera del móvil. **Comprobar en la documentación cuántos
  dispositivos admite el root** el día que se haga; no se escribe de memoria.

#### ⚠️ Cómo se ejecutó de verdad — 2026-08-06 (`T-057`)

- **El alias `+aws` NO se usó.** La cuenta se abrió con el correo personal tal
  cual. **El MFA en root sí se activó en el mismo acto**, como decía la decisión.
- **Impacto: ninguno donde importa.** El alias era **organización, no seguridad
  ni elegibilidad** — está dicho tres puntos más arriba. `[C-006]` ata el plan
  gratuito a la identidad y la tarjeta, así que el correo no cambia nada del
  reloj ni de los créditos.
- **Lo único que se pierde** es filtrar el correo de AWS por la dirección de
  destino. Se sustituye con un filtro por remitente, que hace lo mismo.
- 🚨 **Lo que sigue vigente y NO se relaja:** el valor literal del correo **no se
  escribe en este repo**. Ahora incluso importa un poco más: sin alias, la
  dirección del root es la dirección personal de siempre.
#### ✅ El camino de vuelta del MFA — resuelto y probado el 2026-08-06

- **Cómo quedó:** el segundo factor no vive solo en el móvil. La **semilla** del
  código está en la app **Contraseñas de Apple**, que la sincroniza por el
  Llavero de iCloud. Si el móvil se pierde, los códigos se recuperan desde otro
  dispositivo de la misma cuenta de Apple.
- **Probado de verdad, no supuesto** (`PI-4`): se abrió la app Contraseñas en el
  **iPad** y el código de AWS aparece y rota. Eso demuestra la sincronización
  mejor que leer una casilla de ajustes.
- 🔑 **El riesgo no desapareció, se movió.** Antes el punto único de fallo era el
  móvil; ahora es la **cuenta de Apple**. Lo que lo hace aceptable es que hay un
  **segundo dispositivo de confianza** (el iPad), así que no existe la trampa
  circular de "para recuperar la cuenta de Apple necesito el móvil que perdí".
- ⚠️ **Lo que NO se pudo confirmar:** cuántos dispositivos MFA admite el root. No
  salió en la documentación consultada el 2026-08-06 y **no se escribe de
  memoria**. Si algún día hace falta una segunda llave independiente de Apple, se
  mira en la propia pantalla de credenciales de seguridad de la consola.

### [D-030] 2026-08-05 — El paso 7 termina con un cierre planeado, y el ensayo va pronto

- **Se eligió:** **bajar TEAPP nosotros, con fecha en el calendario**, antes de
  que AWS cierre la cuenta sola. Y **ensayar la reconstrucción pronto**, no al
  final.
- **Contra qué — los tres finales posibles, y solo uno cuesta dinero:**

  | | qué pasa | costo |
  |---|---|---|
  | **A.** no hacer nada | AWS cierra la cuenta sola: 90 días de gracia y borrado | $0 |
  | **B.** apagar antes ✅ | se baja TEAPP con fecha, y luego igual que A | $0 |
  | **C.** pasar a plan de pago | TEAPP sigue vivo y empieza a facturar | ~$11/mes (estimado) |

- 🔑 **La razón NO es el dinero: A y B cuestan lo mismo.** Es que **un cierre
  planeado se aprende y uno automático solo se sufre.** B tiene dentro una
  comprobación que A no tiene, y esa comprobación es todo el valor.
- **La comprobación:** al apagar, **verificar que `deploy/` puede volver a
  levantarlo**. Eso convierte el cierre en la última prueba del paso 7 — y en la
  **única** que demuestra de verdad que `[C-004]` se cumplió.
  - 🔑 Mientras la máquina siga encendida, *"está todo escrito en `deploy/`"* es
    **una afirmación sin corrida detrás**, que es exactamente lo que la regla 6
    prohíbe. **Levantarlo desde cero es la corrida.**
- 🚨 **La corrección de calendario, que es la parte que faltaba.** Si esa prueba
  vive solo al final, **te enteras de que `deploy/` no funciona el día que ya no
  hay margen para arreglarlo**: cuenta muriéndose, créditos gastados y el guion
  que no levanta. Es descubrir que el paracaídas no abre mientras caes.
  - **Por eso el ensayo se hace pronto** (`T-069`): con TEAPP arriba y
    funcionando, se **borra la máquina y se reconstruye solo desde `deploy/`**.
    Una instancia pequeña cuesta céntimos por un día.
  - Así `[C-004]` deja de ser una intención y **queda medida**, con cinco meses
    por delante para arreglar lo que falte. El cierre del final (`T-070`) pasa a
    ser la **segunda** corrida, no la primera.
- 📌 **Y con esto el cierre de la cuenta deja de destruir nada: destruye una
  copia.** 🔑 **La cuenta es desechable; `deploy/` no.** Que es justo lo que
  `[C-006]` obliga a asumir, porque esa ventana de 6 meses no vuelve.

### [D-029] 2026-08-05 — La plataforma del paso 7 la decide el disco, no la nube

- **Se eligió:** **AWS + EC2** (instancia pequeña, tipo `t3.micro`) + **Caddy** de
  servidor de delante + un **nombre gratuito de DuckDNS** + una **IP fija**
  (Elastic IP).
- **Contra qué:** Lambda + API Gateway, y App Runner / Fargate.
- **Que AWS sea la nube no se comparó**, y conviene decir por qué para que nadie
  lo reabra creyendo que se olvidó: es una elección **del curso, no del
  proyecto**. Las metas de quien construye esto —agentes, un SaaS, entender la
  ingeniería por debajo— piden la plataforma donde nada está escondido. Y encaja
  con el método: aquí se escribe `pedir_json` a mano en vez de importar una
  librería. Una plataforma que esconda el proxy contradice el método entero.

#### 🔑 Lo que de verdad decide: `data/` son archivos

TEAPP guarda su estado en el disco — `data/accounts.json`, `data/quota/*.json`,
`data/users/*.json`. **En una máquina local eso no significa nada. En la nube es
el nudo entero del paso 7**, porque casi todas las plataformas modernas dan un
disco **efímero**: existe mientras el programa corre y desaparece al reiniciar.

| lo que pasaría con disco efímero | cómo se vería |
|---|---|
| reinicia el servidor → `accounts.json` desaparece | **se nota en cinco minutos**: nadie puede entrar |
| arrancan dos copias → dos `accounts.json` distintos | me registro en una y entro por la otra: no existo |
| 🚨 reinicio → **cuota nueva** | **no se nota nunca**: el sistema responde contento y habla la factura del paso 8 |

- 🚨 **La tercera es la grave, y por ser la muda.** El freno del paso 6 se
  rompería **sin que nadie le tocara una línea**, solo cambiando lo que hay a su
  alrededor. Es exactamente la forma de `[D-027]`: allí fue el registro abierto,
  aquí sería el disco.
- Por eso la comparación se hizo por una sola columna:

  | camino | disco | veredicto |
  |---|---|---|
  | Lambda + API Gateway | **no hay** | y además necesita un adaptador para FastAPI |
  | App Runner / Fargate | **efímero** | cómodo, y borra las cuentas al reiniciar |
  | **EC2** ✅ | **persiste** | TEAPP sube **sin cambiar una línea de código** |

#### El premio: las dos deudas fantasma se vuelven trabajo concreto

`[C-002]` decía que escribir hoy un tope de tamaño de cuerpo sería *"inventarse
una pieza que la plataforma del paso 7 trae hecha"*. Con el proxy en nuestra
máquina, deja de ser fantasma: `T-054` es una línea de configuración de Caddy.

Y `T-055` es el caso bonito. 🔑 **La garantía de `X-Forwarded-For` NO viene de
que el proxy sea nuestro — viene de que nadie más pueda hablar con FastAPI.** Son
dos cosas juntas, y sin las dos no hay certeza, hay costumbre:

1. uvicorn atado a `127.0.0.1`, no a todas las direcciones.
2. el cortafuegos abierto **solo** en 80 y 443.

#### HTTPS sin dominio: el agujero que casi mata el despliegue

- **Verificado, no supuesto:** Let's Encrypt **se niega por política** a emitir
  certificados para `compute.amazonaws.com`. Devuelve literalmente *"The ACME
  server refuses to issue a certificate for this domain name, because it is
  forbidden by policy"*. Hay hilos en su foro desde 2016. No es configuración: no
  hay forma de convencerlo.
- 🚨 **Sin certificado, `T-051` no se puede cumplir y NADIE ENTRA A TEAPP.**
  `TEAPP_COOKIE_SECURE=true` le dice al navegador *"no mandes esta cookie salvo
  por HTTPS"*. Sin HTTPS válido la cookie de sesión no viaja, y el fallo es mudo.
  **Un despliegue entero muerto por la política de una autoridad certificadora.**
- **Se resuelve con un nombre gratuito de DuckDNS** (`teapp.duckdns.org`): es un
  nombre público de verdad, Let's Encrypt emite sin problema y Caddy hace el
  trámite solo. 📌 **El límite de quien construye esto es el dinero, no el
  nombre**: un nombre regalado y sin tarjeta sí entra.
- **Por eso Caddy y no nginx:** saca y renueva el certificado solo. Con nginx ese
  trámite es una pieza más que montar y mantener, y `T-051` la necesita sí o sí.

#### Por qué IP fija, y no un guion que avise a DuckDNS

La IP pública de una EC2 **cambia al apagar y encender**. Si DuckDNS apunta a la
vieja, el nombre deja de resolver → se cae el HTTPS → se cae la cookie → no entra
nadie.

- 🔑 **El argumento bueno no es "es una pieza menos": es que cuesta lo mismo.**
  AWS cobra por *tener una IPv4 pública*, no por el tipo. La que asigna sola al
  arrancar y la fija se facturan igual. Entonces no se paga un extra por
  comodidad — **se elige cuál de las dos direcciones se tiene, al mismo precio**.
  Cobrando lo mismo, quedarse con la que cambia no tiene defensa.
- El guion que avisa a DuckDNS existe para el caso contrario: alguien en su casa,
  con una IP que le cambia el proveedor y sin forma de fijarla. No es este caso.
- ⚠️ **La trampa clásica:** una IP fija **sin máquina asociada también cobra**.
  Es como AWS evita que se acaparen direcciones. Aquí no aplica —la máquina no se
  va a borrar— pero queda escrito.

#### Lo que se descartó por medición, no por pereza

EC2 **consume créditos**: para cuentas nuevas ya **no existe** la franja de 750
horas. La sospecha era que entonces *"el reloj lo marca la resta, no el
calendario"*, y que habría que escribir una pieza que apagara la máquina sola.

**Al ponerle números, no aguanta:** el gasto estimado del paso 7 es del orden de
$50 de $200 (ver `[A-015]` — es estimación de lista de precios, no corrida).
🔑 **Gana el calendario, y sobra un factor de cuatro.** La pieza que apaga la
máquina queda descartada. Y apagarla por las noches "para ahorrar" ahorra las
horas de la instancia **pero la IP sigue cobrando**: complica más de lo que
rinde. **Encendida y quieta.**

> 🔁 **REVOCADO el 2026-08-09 por `[D-045]`. Ya NO es "encendida y quieta":** hay
> ventana de uso 12:00–23:00 UTC y apagado automático. El *"del orden de $50"* que
> sostenía este párrafo es `[A-015]`, **aritmética de lista nunca corrida**, y le
> faltaba justo el cargo de la IPv4 que después fue el primero en aparecer. Lo que
> sí sobrevive de aquí: apagar **no** lleva el gasto a cero, la IP y el volumen
> cobran igual.

#### Lo que NO arregla, y hay que llevar en la lista

- **"Sube sin cambiar una línea" vale para el código, no para el arranque.**
  Faltan: dirección de escucha, variables de entorno, arranque automático, el
  `.js` compilado, y **correr `create_account.py` allá arriba** — `data/` no va a
  Git, así que la máquina arranca **sin ninguna cuenta** (`[D-027]`).
- **El disco persiste al reiniciar, no si se borra la máquina.** ⚠️ **No hay
  copia de seguridad de nada.** El día que se cierre la cuenta, las cuentas de
  prueba se van con ella. Aceptado: es un ejercicio con fecha de caducidad.
- **`[D-024]` paga por otro lado.** El offset fijo `−05:00` de la cuota se
  escribió a mano por un problema de Windows. Resulta que también salva aquí: la
  máquina de EC2 estará en UTC y a `quota.py` le va a dar igual.

### [D-028] 2026-08-04 — El log se configura, y con él `info` vuelve a significar algo

- **Se eligió:** `configure_logging()` en `app/config.py`, llamada **lo primero**
  al importar `app/api.py`. Formato `hora nivel origen | mensaje`, nivel `INFO`
  por defecto y ajustable con `TEAPP_LOG_LEVEL`.
- 🔑 **Lo que esto arregla no es la forma, aunque sea lo que se ve.** Hasta hoy
  actuaba el handler de último recurso de Python, **que empieza en `WARNING`**:
  cualquier `logger.info(...)` no se perdía por poco, **no existía**. La única
  forma de que un renglón saliera era subirlo de nivel — y eso obliga a mentir
  sobre su importancia. 🚨 **Un log donde todo es aviso no tiene avisos.**
- **Qué renglón queda en qué nivel, y por qué:**

  | renglón | antes | ahora | por qué |
  |---|---|---|---|
  | cuota agotada (`app.api`) | `warning` | **`info`** | es el freno funcionando, no una avería |
  | registro cerrado (`app.config`) | `warning` | **`info`** | es el estado normal de la v1 |
  | **demasiados intentos** (`app.api`) | `warning` | **`warning`** | 🚨 no describe el sistema funcionando: describe a **alguien intentando entrar en una cuenta ajena**. Y el contador vive en memoria ([D-026]), así que este renglón es el único rastro que sobrevive a un reinicio |

  Los dos primeros llevaban escrito en el código *"cuando `T-033` configure el
  log, esto vuelve a `info`"*. Se cumplió: si no, quedaban dos comentarios
  mintiendo.
- **Por qué `basicConfig` y no `dictConfig`:** hace falta una línea, no un árbol
  de configuración. PI-2.
- 🚨 **Y por qué SIN `force=True`**, que era lo tentador: `basicConfig` no hace
  nada si el logger raíz ya tiene handlers, y eso aquí juega a favor.
  - **Con uvicorn** la raíz está limpia —uvicorn configura sus propios loggers,
    no el raíz—, así que la configuración sí aplica. Medido.
  - **Bajo pytest** la raíz está tomada por `caplog`, y que aquí no se pise nada
    es justo lo que se quiere. `force=True` le arrancaría a `caplog` su handler
    en mitad de la suite.
- **Medido, no supuesto** (2026-08-04, uvicorn real, puerto 8094):

  ```
  2026-08-04 19:52:14 INFO     app.config | Registro por red CERRADO (...)
  2026-08-04 19:52:18 INFO     app.api | Cuota agotada: probe-log lleva 20 de 20 el 2026-08-04
  ```

  🔑 **Ese segundo renglón es literalmente el de [L-012]**, el que se midió el
  mismo día como *"20 frenazos, cero líneas"*. Ahora sale.
- ⚠️ **En la misma corrida apareció ruido que no es nuestro:** un
  `ERROR asyncio | ConnectionResetError [WinError 10054]`, una vez. Es el cliente
  de la prueba cerrando la conexión de golpe, cosa de `asyncio` en Windows — las
  22 peticiones contestaron bien. No lo tapa nadie y no se persigue hoy; queda
  escrito para que no se investigue dos veces.
- **Lo que NO se decide aquí:** dónde se guarda el log en la nube ni cuánto se
  conserva. Eso es del paso 7, con la plataforma delante.

### [D-027] 2026-08-04 — El registro se cierra con un interruptor, y las cuentas se crean desde la terminal

- **Se eligió:** que `/register` esté **cerrado por defecto**, detrás de
  `TEAPP_REGISTRATION_OPEN`; que la ruta siga en el código porque la suite la
  usa; y que las cuentas se creen con `create_account.py`, que no espera a nadie.
- **Contra:** dejar `/register` abierto con un tope de registros por origen.
- **El problema, medido** (2026-08-04, `scrypt` con los parámetros de
  `app/accounts.py`):

  | lo que se hizo | resultado |
  |---|---|
  | 200 registros con nombres **nuevos** | 25,6 s — **128 ms cada uno** |
  | el registro nº 201, con 200 cuentas dentro | 121 ms |
  | 200 registros con un nombre **repetido** | 0,12 s — 0,6 ms cada uno |
  | `accounts.json` con 200 cuentas | 30.293 bytes, **reescrito entero cada vez** |

  🔑 **La comparación entre la primera fila y la tercera es toda la historia.**
  Un nombre repetido se rechaza *antes* de `scrypt` y sale 200 veces más barato.
  O sea: lo caro es exactamente lo que quien ataca puede pedir sin límite — un
  nombre nuevo cada vez. Sin sesión, sin cuenta y sin tope. Era una palanca peor
  que la de `/login`, porque allí al menos había un freno.
- **Por qué cerrado y no un tope por origen:**
  - `_context/scope.md` decide los casos dudosos con *"¿hace falta para que la
    tubería funcione en producción?"*. Un sistema de invitaciones no hace falta:
    es **v2**.
  - 🔑 **Cerrar hace desaparecer la palanca; un tope solo la estrecha.** Sin
    invitación no se llega a `scrypt`, y el rechazo cuesta lo que un `if`.
  - Y un tope por origen tenía un daño colateral serio: si quien usa esto es un
    salón de clase, salen todos por la misma dirección, y el tope que frena a
    quien ataca frena también a quien registra a veinte estudiantes seguidos.
- **Lo que la decisión OBLIGA a añadir:**
  - **`create_account.py`**, o el interruptor deja fuera a quien administra. ⚠️ Y
    **`main.py` no bastaba**, aunque también crea cuentas: se comprobó el
    2026-08-04 y usa `getpass`, que en Windows lee **de la consola** y no de la
    entrada estándar. Con la entrada por tubería se queda colgado esperando un
    teclado. Sirve a quien está sentado delante; **en un servidor no sirve**, y en
    el paso 7 no hay nadie sentado delante.
  - **Las dos ramas con test.** `conftest.py` abre el registro con `autouse`
    porque casi toda la suite empieza creando una cuenta, y eso deja el camino
    por defecto sin correr — la trampa de `[L-031]` (antes `[A-009]`) y la
    lección de `T-052`. Los
    tests que anulan ese `setenv` están en `test_api.py`.
  - **Que abrir exija la palabra exacta `true`**, al revés que `cookie_secure`,
    que acepta cualquier cosa que no sea `false`. Allí equivocarse deja la puerta
    cerrada; aquí la abriría.
- **Comprobado de punta a punta** (2026-08-04, uvicorn real, puerto 8095): cuenta
  creada desde la terminal **sin teclado** → `POST /register` por la red contesta
  `403` → `POST /login` con esa cuenta contesta `200`. El interruptor cierra la
  puerta de la calle sin cerrar la de servicio.
- ⏳ **Caducidad:** el día que haya que registrar a **gente desconocida** — gente
  a la que no se le puede crear la cuenta a mano. Ese día esta decisión deja de
  valer y toca el sistema de invitaciones que aquí se aplazó a v2. Hasta entonces
  no hay nada que revisar.
- **Lo que NO se decide aquí:** cómo se registra esa gente desconocida. Cerrar
  hoy no elige la puerta de mañana.

### [D-026] 2026-08-04 — El tope de intentos cuenta en memoria; la cuota sigue contando en disco

- **Se eligió:** guardar los intentos fallidos de `/login` en un `dict` en
  memoria (`app/login_guard.py`), con candado y con barrido de lo vencido.
- **Contra:** guardarlos en disco, por coherencia con `quota.py`, que avisa en su
  propia cabecera de que un contador en memoria se borra en cada arranque.
- **Por qué:**
  - 🔑 **Lo que se cuenta dura cosas distintas.** La cuota dura **un día**: un
    reinicio a media tarde regala medio día de gasto real, y en la nube el
    servidor se reinicia solo. El tope de intentos dura **quince minutos**: un
    reinicio le devuelve los intentos a quien esté probando contraseñas, pero él
    no puede provocar el reinicio — le tocaría de casualidad.
  - 🚨 **Y en disco habría una palanca.** Escribir un archivo en cada intento
    fallido pone en manos de quien ataca **cuántas veces escribe el servidor**.
    Es exactamente el problema de `[C-002]`: quien manda decide lo que cuesta
    atenderle. En memoria, fallar no cuesta un archivo.
- **Lo que la decisión OBLIGA a añadir**, y sin lo cual sería mala:
  - **Barrido de lo vencido**, dentro de `record_failure` — el único sitio donde
    el `dict` crece. Sin él, la palanca del disco reaparece como memoria: mil
    direcciones distintas dejan mil entradas que no se irían nunca. Con testigo:
    `test_the_sweep_runs_by_itself_when_new_failures_arrive`.
  - **Cada frenazo al log con `warning`.** El contador se borra entero en cada
    reinicio, así que ese renglón es **el único rastro que sobrevive** de que
    alguien estuvo probando contraseñas. Con `info` no aparecería mientras
    `[T-033]` no configure el log (`[L-012]`).
  - **Un reinicio del `dict` entre tests**, en `conftest.py`. Vive en memoria: no
    ensucia datos de verdad, pero sobrevive de un test al siguiente y haría que
    los tests de login dependieran del orden en que corren.
- **Hereda `[A-002]`, y de la forma más incómoda:** un `dict` solo lo ve su
  propio proceso. Dos procesos de uvicorn son dos contadores que no se enteran el
  uno del otro, y entonces el tope real es el doble del escrito. Hoy se arranca
  un proceso; el día que se arranquen dos, este freno se afloja **en silencio**.
- **Medido, no supuesto** (2026-08-04, uvicorn de verdad, puerto 8099):

  | intento | respuesta | log |
  |---|---|---|
  | 1 a 5, contraseña mala | `401` | — |
  | 6, contraseña mala | `429`, `retry-after: 900` | `origen 127.0.0.1 lleva 5 de 5` |
  | 7, contraseña **buena** | `429` | mismo renglón |

  🔑 La tercera fila es la que dice que el freno es un freno: **la contraseña
  correcta tampoco abre** mientras el origen esté cerrado. Si abriera, quien
  prueba a la fuerza no estaría frenado — solo tendría que seguir probando.
- **Lo que NO se decide aquí:** de dónde sale el origen en la nube. Hoy es
  `request.client.host`; detrás de un proxy será la dirección del proxy y todo el
  mundo caería en el mismo cubo. Queda con dueño en `T-055`.

### [D-025] 2026-08-04 — `/login` se queda sin freno de intentos, y se anota como deuda

- **Se eligió:** **no** poner tope de intentos fallidos en `/login` dentro del
  paso 6, y dejarlo escrito como deuda del paso 7.
- **Contra:** meterlo ahora, aprovechando que `quota.py` ya sabe contar por
  persona y por día.
- **Por qué:**
  - 🔑 **Parecen el mismo freno y no lo son.** La cuota protege **la factura** y
    cuenta a quien ya demostró quién es. Un tope de intentos protege **las
    contraseñas** y tiene que contar a quien **todavía no** ha demostrado nada —
    o sea, no por persona, porque la persona es justo lo que está en duda. Se
    cuenta por origen de la petición, que es otro dato y otra estructura.
  - Reutilizar `quota.py` para esto sería doblarlo para un trabajo que no es el
    suyo, y acabaría estorbando a los dos.
  - `_context/roadmap.md` pone el paso 6 en *"tope por persona y por día,
    timeouts"*. Esto no es eso.
  - ⚠️ **Y hoy muerde menos de lo que parece:** en local el único que puede
    probar contraseñas es quien ya tiene la máquina. El riesgo nace el día que
    la app esté en internet, que es el paso 7.
- **Lo que NO se decide aquí:** que no haga falta. Hace falta. Se decide
  **cuándo**, y que quede con dueño en vez de olvidado — el mismo trato que
  [L-031] (antes [A-009]) le dio al hueco de la cookie `Secure`.
- **Toca:** `app/api.py` (`/login`), el paso 7, y la suposición [A-012].
- ⏹️ **Saldada el 2026-08-04** por [D-026] (`T-053`). La deuda se pagó **antes**
  del despliegue, que era la fecha que esta entrada se puso a sí misma.
  ⚠️ [A-012] ya **no existe**: se retiró al saldarla y se partió en [A-013] y
  [A-014]. Si has llegado aquí buscándola, está contada en [L-014].

### [D-024] 2026-08-04 — El "día" de la cuota se mide en offset fijo −05:00

- **Se eligió:** una constante en el código, `timezone(timedelta(hours=-5))`, y
  el día se obtiene con `moment.astimezone(...).date()`. El `now` que se inyecta
  es un `datetime` **con zona**, no un número suelto.
- **Contra:** (a) medir el día en **UTC**, que es lo que haría el servidor del
  paso 7 por su cuenta; (b) `ZoneInfo("America/Bogota")`, que es la forma
  "correcta de libro".
- **Por qué:**
  - 🔑 **`sessions.py` mide una duración; la cuota mide un día del calendario.**
    A una duración le da igual dónde estés: siete días son siete días. Un día del
    calendario **no existe sin zona horaria**. Por eso `sessions.py:71` puede
    usar un `float` de `time.time()` y aquí no vale.
  - **UTC se descarta con una corrida, no con una opinión.** El mismo instante
    —`2026-08-05 02:30 UTC`— es día **5** en UTC y día **4** en −05:00. Esa
    ventana de 5 horas es la cuota reiniciándose a las **7pm**. Y el fallo no
    aparecería en local (donde la máquina va en −05:00): **aparecería solo en la
    nube**, que es el peor sitio para descubrirlo.
  - 🚨 **`ZoneInfo` se descarta porque se probó y falló.** En esta máquina,
    `ZoneInfo('America/Bogota')` lanza `ZoneInfoNotFoundError`: Windows no trae
    la base de datos de zonas horarias que Linux sí tiene. Funcionaría en la nube
    y no en casa — el fallo al revés, igual de malo. Arreglarlo pide añadir y
    fijar el paquete `tzdata` ([L-002]), o sea una dependencia más para algo que
    una constante resuelve.
  - **El offset fijo es correcto aquí porque Colombia no cambia la hora en
    verano.** Es lo único que un offset fijo no sabría manejar, y no aplica.
    ⚠️ Si algún día la app sirve a alguien en una zona con horario de verano,
    esta decisión se rompe y hay que volver a `ZoneInfo` **con `tzdata`**.
- **Toca:** `app/quota.py`, el paso 7 (el servidor corre en UTC y esta constante
  es lo que lo hace irrelevante) y `requirements.txt` (la dependencia que **no**
  se añade).

### [D-023] 2026-08-04 — Los cuatro frenos del paso 6, y el que se queda fuera

- **Se eligió:** cerrar el paso 6 con **cuatro** frenos:
  1. **Cuota por persona y por día.** Un contador con clave *(persona, día)*.
  2. **Timeout de la petición.** La que no contesta se corta sola.
  3. **Tope al tamaño del texto de práctica.** Hoy `PracticeRequest.sentence` es
     un `str` sin techo (`app/api.py:105`).
  4. **Motivo del frenazo.** Un 429 sin motivo es un misterio.
- **Contra:** una lista de cinco que incluía *"permisos de antemano"*, y la
  lectura de que *"tope por persona y por día"* del roadmap eran **dos** frenos
  (uno por persona, otro global de la casa).
- **Por qué:**
  - **Los permisos de antemano se quedan fuera porque ya están hechos.** Son la
    regla 3 de `CLAUDE.md`, e implementados: `normalize_user` impide que un
    nombre construya una ruta fuera de sitio ([D-014]), y desde el paso 5 la
    identidad sale de la cookie firmada, así que nadie toca el marcador de otro
    ([D-021]). 🔑 El motivo de fondo: **no tiene terminado**. Los otros cuatro
    tienen un número o una respuesta que mirar; este no, y una tarea sin
    terminado no se cierra nunca.
  - **El freno 3 (tamaño del texto) no está en el roadmap y entra igual.** El
    patrón ya vive en casa dos veces —`MAX_USER_LENGTH` (`app/tools.py:62`) y
    `MAX_PASSWORD_LENGTH` (`app/accounts.py:63`)—. No es una idea nueva: es la
    misma, olvidada justo en el sitio que más va a costar en el paso 8.
  - **Un solo contador, no dos.** *"Por persona y por día"* es una cuota que se
    reinicia cada día, no un tope por persona más un tope global. El tope global
    es el freno de la cartera y pertenece al paso 8, donde hay dólares que
    contar.
- **Cómo se construye, decidido ahora porque después cuesta:**
  - 🚨 **El reloj se inyecta.** `now` como parámetro, igual que
    `sessions.py:71` y `:89`. Un tope por día no se puede ver funcionar en una
    corrida —nadie espera a mañana—, así que si el código llama a `time.time()`
    por dentro, el freno se queda sin testigo.
    ⚠️ Con una diferencia que costó una comprobación: **el `now` de la cuota
    lleva zona horaria** y el de `sessions.py` no. Ver [D-024].
  - 🚨 **El contador sube ANTES de llamar al tutor, no después.** Hoy da igual
    —el tutor falso no falla nunca—, pero en el paso 8 una llamada que **gasta
    tokens y luego revienta** se colaría gratis: el dinero salió y el contador no
    se enteró. 🔑 Lo que se cobra es **haber intentado**, porque eso es lo que
    cuesta.
  - **El tope se inyecta igual que el reloj.** Un `20` incrustado obliga a
    mandar 21 peticiones —a mano y en cada test— para ver el freno morder. Con el
    tope inyectado, un test pone 1 y lo ve morder a la segunda. Y el número es
    una predicción sin medir ([A-010]): cambiarlo no puede costar una reescritura.
  - **El contador cuenta peticiones, pero se diseña para que en el paso 8 se le
    cambie la unidad a dólares sin rediseñarlo.** Hoy es gratis; descubrirlo en
    el 8 no.
  - 🚨 **El contador escribe en disco, y ese terreno ya costó sangre.** Es el
    mismo problema de [T-020], [T-021] y [T-022]: candado, más escribir al lado
    y renombrar encima ([D-007], [D-009]). Hereda [A-002]: solo vale con un
    proceso de uvicorn. Un freno que pierde cuentas con dos peticiones a la vez
    no frena.
  - **El motivo del frenazo viaja en la respuesta, no en el log** — o hay que
    subir [T-033] al paso 6. Escribirlo en el log antes de configurarlo lo manda
    al handler de último recurso de Python ([A-003]): sale por pantalla porque
    Python no sabe qué otra cosa hacer, no porque nadie lo decidiera.
- **Toca:** el paso 6 entero, `app/api.py`, `app/tools.py`, y el paso 8 (la
  unidad del contador y el tope global de la casa).

### [D-022] 2026-08-04 — El portero de red entra al repo, y con sus controles

- **Qué se decidió:** meter el portero de red (`tests/no_network.py`) al repo,
  activo en **todos** los tests vía `conftest.py`, y meter con él sus cinco
  controles (`tests/check_no_network.py`), fuera de la corrida normal.
- **Contra qué:** dejarlo como medición de una sola vez — comprobar hoy que
  `C-001` se cumple, anotarlo, y repetir a mano cuando alguien se acuerde.
- **Por qué:**
  - Medir una vez dice *"el 4 de agosto se cumplía"*. El portero dice *"se
    cumple hoy"*, en cada corrida. El día que alguien meta una llamada de verdad
    a la API, la suite se pone roja **en ese momento**, no meses después.
  - 🔑 **Los controles van o no va nada.** El verde de la suite no demuestra que
    el portero funcione: si el portero se rompe en silencio, los 192 tests pasan
    exactamente igual, porque ninguno intenta salir. Solo los controles — que
    salen a internet a propósito — distinguen *"nadie salió"* de *"y si alguien
    lo intentara, se le vería"*. Un portero en el repo sin sus controles es la
    misma trampa que venía a evitar, un piso más abajo.
  - Los controles **no** se llaman `test_*.py` a propósito: salen a internet de
    verdad si el portero falla, y eso es justo lo que `C-001` prohíbe. Se piden
    por su nombre para reverificar.
- **Lo que esta decisión NO puede dar:** el portero solo parchea el `socket` de
  su propio proceso. `node`, `git` y `npx` son otro proceso: **nunca** los verá.
  Por eso `C-001` queda partida en dos mitades, una automática y otra a mano.
- **Toca:** `tests/no_network.py`, `tests/check_no_network.py`,
  `tests/conftest.py`, `[C-001]`, todo test futuro.

### [D-021] 2026-08-04 — Contraseña propia y cookie de sesión firmada; el proveedor externo se descarta

- **Se eligió:** que el paso 5 pruebe la identidad con **usuario y contraseña
  propios**, guardada como *hash* (cifrado de ida: se comprueba, no se desanda),
  y que la sesión se recuerde con una **cookie firmada por el servidor**,
  `HttpOnly` y `Secure`. Todo con librería estándar: `hashlib.scrypt` para la
  contraseña, `hmac` para la firma, `secrets` para generar. **Cero paquetes
  nuevos**, así que la suite sigue sin tocar la red ([C-001]) sin nada que pensar.
  - **`scrypt`, no `sha256`.** Un hash de contraseña es **lento a propósito**:
    lo que protege es que probar millones de contraseñas cueste caro. `sha256`
    es rápido, que aquí es exactamente el defecto.
  - **`hmac.compare_digest`, no `==`.** Comparar con `==` corta en cuanto
    encuentra la primera diferencia, y ese tiempo se puede medir desde fuera
    para adivinar la firma letra a letra.
- **Contra:** "entrar con Google" (OAuth) y el enlace por correo.
- **Por qué:** el argumento bueno es del propio roadmap — *"el paso 8 cae casi
  al final... el sospechoso queda solo"*. 🔑 **Un proveedor de identidad externo
  es una pieza que no controlo y que no responde igual dos veces: la misma clase
  de ruido que el modelo.** Meterla en el paso 5 es meter en la tubería justo lo
  que el roadmap saca de ella hasta el paso 8. No se descarta por ser "más
  difícil" ni la contraseña se elige por ser "lo básico".
  El enlace por correo, además, necesita un servicio que mande correos: red,
  cuenta y probablemente factura. Choca con la regla 5 y con [C-001].
- ⚠️ **Un argumento que se usó y era falso, anotado para que no vuelva:** se dijo
  que OAuth exige una dirección pública de vuelta que no existe hasta desplegar,
  y por tanto ataba el paso 5 al 7. **No es cierto: Google admite
  `http://localhost` para desarrollo.** El costo real de OAuth es otro —cuenta de
  Google Cloud, pantalla de consentimiento y un secreto de cliente—. La
  conclusión no cambia; el argumento sí. Queda escrito porque una decisión
  correcta sostenida por un motivo falso se cae en cuanto alguien comprueba el
  motivo.
- **Toca:** `app/api.py`, `frontend/app.ts`, `.env.example` (una línea nueva para
  la llave de firma), el paso 5 entero, y el paso 7, que tiene que llevar esa
  llave a la nube.

### [D-020] 2026-08-04 — Los cuatro marcadores de `data/users/` son huérfanos: se borran, no se siembran

- **El problema:** `data/users/` tiene cuatro marcadores sin contraseña —`ana`
  (2), `juan` (4), `maria` (1), `pedro` (3)—. Con un registro abierto, cualquiera
  se registra como `juan` y hereda su marcador. 🔑 **Verificar la identidad no
  sirve de nada si cualquiera puede reclamar una identidad que ya existía:** es
  el agujero de [D-013] con un formulario delante.
- **Se eligió:** declararlos **huérfanos y borrarlos**, dejando `data/users/`
  vacío antes de que exista el registro.
- **Contra:** sembrar las cuatro cuentas a mano con una contraseña cada una.
- **Por qué:** esos cuatro nombres salieron de probar el paso 4, no de cuatro
  personas. Lo dice [S-007] —*"uvicorn con curl (juan/ana separados)"*— y lo
  confirma el disco: los cuatro archivos pesan 12 bytes y están escritos **el
  mismo minuto**, el 2026-08-03 a las 10:44.
  Es el mismo criterio de [D-015] con el `score.json` global, y aquí pesa más:
  🔑 **sembrarlos no obligaría a inventarles un dueño, sino una contraseña.** Una
  contraseña es la prueba de que alguien es quien dice; fabricar cuatro es crear
  cuatro credenciales válidas sin nadie detrás, lo contrario de lo que este paso
  viene a construir.
- **Lo que el vaciado gana, y es la razón de fondo:** restablece una regla que
  hoy está rota — **todo marcador nace junto a su credencial; no existe marcador
  sin dueño**. Con esa regla en pie el agujero se cierra por estructura: el
  registro rechaza un nombre que ya existe, y como ya no queda ningún nombre sin
  credencial, no hay nada que reclamar. Sembrarlos, en cambio, obligaría a una
  regla especial para esas cuatro cuentas, y las reglas especiales son donde se
  cuelan los errores.
- **No se pierde historial:** `data/` está en `.gitignore` y nunca fue a Git, así
  que ahí no había nada que conservar. Y no se hace copia de seguridad: los
  cuatro nombres, los cuatro números y la hora quedan escritos aquí arriba. Se
  pierden 48 bytes; lo que significaban ya está en prosa.

**Dos consecuencias que costó ver, y sin las cuales el borrado no sirve:**

1. 🔑 **Vaciar `data/users/` no es una tarea que se complete hoy: es una
   condición que solo se vuelve estable el día que el registro existe.**
   `add_point` crea el archivo —y la carpeta— la primera vez que alguien
   practica. Hoy cualquier petición a `/practice` fabrica un marcador sin
   credencial: es el agujero de [D-013] visto desde el disco. Así que se borra,
   y el primer `curl` de prueba del paso 5 con `{"user": "juan"}` lo resucita.
   ⚠️ **Por eso no se anota como hecho consumado, sino como condición con punto
   de verificación:** la carpeta se comprueba vacía **después** de que la
   credencial funcione, no ahora. Darlo por hecho hoy significa que esta noche el
   cierre encuentre un `juan.json` y nadie pueda distinguir si es el viejo o uno
   de prueba — y la evidencia del 10:44 ya no estará para desempatar.

2. 🔑 **La lista de quién existe y la lista de quién tiene puntos no son la
   misma lista, aunque hoy se parezcan.** La regla "el registro rechaza un
   nombre que ya existe" está incompleta si no dice **según qué archivo**. Si el
   registro mirara `data/users/`, le estaría preguntando *"¿quién existe?"* a una
   carpeta que cualquiera puede llenar practicando. **La autoridad sobre quién
   existe es el almacén de credenciales, y solo ese.** `data/users/` pasa a ser
   un **derivado**: un marcador solo nace cuando la credencial ya existía.

**El residuo del 2026-08-04 NO es este caso, y la distinción vale más que los
archivos.**

Al terminar el paso 5 quedaron en disco un `juan` (1 punto) y una `ana` (sin
marcador), de las pruebas de esa tarde. Se **conservan**, y eso no contradice
nada de lo de arriba:

| | los cuatro del 2026-08-03 | `juan` y `ana` del 2026-08-04 |
|---|---|---|
| ¿tienen credencial? | **no** | **sí**, nacieron con ella |
| ¿cumplen la regla? | la rompían | la cumplen |
| borrarlos es… | **integridad** | **higiene** |

> 🔑 **Aquellos había que borrarlos; estos se pueden borrar.** No es la misma
> frase. Un marcador sin dueño es una identidad reclamable y hay que quitarla de
> en medio. Un marcador con su credencial detrás es solo desorden, y el desorden
> se limpia cuando apetece.

⚠️ Esto es lo que hay que mirar antes de aplicar `[D-020]` otra vez: **la
pregunta no es "¿esto es de una prueba?", es "¿tiene dueño?".** Confundirlas
llevaría a borrar cuentas reales por parecer de prueba, o a conservar marcadores
huérfanos por parecer datos.

- **Toca:** `data/users/`, el registro del paso 5, `app/accounts.py`, y el
  criterio de cualquier migración futura de datos de personas.

### [D-019] 2026-08-04 — El control del `.js` sube al Paso 2b; el resultado del push no se anota porque no se puede

**El problema (T-049):** `protocol-close` escribía `tasks.md` en el Paso 4, y
**después** corría el control del `.js` (Paso 5b) y el push (Paso 6b). Lo que esas
dos corridas demostraban llegaba tarde: no había dónde anotarlo. Pasó de verdad
con T-048 el 2026-08-03 — la tarea pedía ver el control funcionando en un cierre
real, el control funcionó, y nadie pudo marcarla.

🔑 **Al mirarlo de cerca eran dos problemas distintos con la misma cara.** Uno se
arregla moviendo un paso; el otro no se arregla nunca.

**Mitad 1 — el control del `.js`: se eligió MOVERLO al Paso 2b.**

- **Contra:** dejarlo donde estaba y añadir un repaso de `tasks.md` después del
  push.
- **Por qué:** el control no necesitaba estar abajo. Su única exigencia real es
  ser **antes del `git add`**, y entre "después del traspaso" y "antes del `git
  add`" hay sitio de sobra. Movido arriba, su resultado llega antes de escribir
  `tasks.md` y se anota como cualquier otra evidencia.
- **Por qué se descartó el repaso posterior:** obligaría a un segundo commit cada
  noche, y ese segundo commit tendría el mismo problema con su propio push. Se
  cambiaba un hueco por un bucle.
- **Va después del Paso 2, no dentro del Paso 1:** el Paso 1 tiene una puerta
  —*"si `git status` sale limpio, detente"*— y compilar antes de esa puerta gasta
  trabajo las noches en que no hay nada que cerrar.
- ⚠️ **El movimiento crea una suposición nueva**, anotada como `[A-007]`: entre el
  control y el `git add` no se toca ningún `.ts`.

**Mitad 2 — el push: se eligió TRATARLO COMO IMPOSIBILIDAD, no como pendiente.**

- **Se decidió:** dejar escrito en el protocolo que el resultado del push **no
  puede** vivir en `tasks.md`, con el porqué, y que su sitio son el reporte de hoy
  y el arranque de mañana.
- **Contra:** seguir intentando encajarlo en el commit con más pasos.
- **Por qué:** es una pescadilla que se muerde la cola. Para saber si el push
  funcionó, el commit tiene que existir ya — y `tasks.md` va dentro de ese commit.
  Ninguna reordenación lo resuelve. 🔑 **Un límite lógico escrito como límite
  deja de parecer un olvido**, y nadie vuelve a intentar arreglarlo.

**Lo que casi se queda a medias, y es la parte que más enseña:** la mitad 2 se
apoyaba en que el arranque de mañana lee `git status -sb` y ve la línea `ahead`.
Al comprobarlo, `protocol-start` leía **`git status --short`**, que no imprime la
línea de la rama: un commit sin subir le resultaba **invisible**. La promesa
existía y nadie la cumplía. Por eso la mitad 2 son **dos escrituras**, en dos
archivos, y sin la segunda la primera es papel. Ver `[L-009]`.

- **Toca:** `.claude/skills/protocol-close/SKILL.md` (Pasos 2b, 4 y 6b),
  `.claude/skills/protocol-start/SKILL.md` (Paso 1 y la tabla de desfases, ahora
  de tres filas), `.claude/agents/session-closer.md`, `tests/test_api.py`
  (comentario), `[A-007]`, `[L-009]`.
- ⚠️ **El control se llamaba "Paso 5b" hasta hoy.** Las anotaciones anteriores al
  2026-08-04 —`[D-017]`, `[D-018]`, `[S-008]`, T-037, T-046, T-048— lo nombran
  así. Es el mismo control; no se reescribieron por ser historia.

### [D-018] 2026-08-03 — Un control no puede causar un daño mayor que el que previene: el `.js` viejo no cancela el cierre

- **Se eligió:** que el control del Paso 5b **reporte y siga**. Si el `.js` está
  viejo, o si no se pudo comprobar, el cierre commitea y sube igual, y el aviso
  va a "Sin resolver" con su tarea.
- **Contra:** que el cierre se plante y no commitee hasta que se recompile a mano.
- **Por qué:** un `.js` desactualizado y **señalado** es una molestia: el
  despliegue no es hoy, es el paso 7. Un cierre que se niega a guardar deja el
  día entero solo en este disco, que es exactamente la catástrofe de [L-006] —
  la que el protocolo existe para evitar. 🔑 **Un control no debe poder causar un
  daño mayor que el que previene.** Cambiar una molestia por la pérdida del día
  es un mal negocio aunque el control tenga razón.
- **También se decidió que el closer NO recompile.** Podría dejar el repo
  correcto en el acto, pero borraría la señal de que se olvidó, y mañana se
  olvidaría igual. **El olvido es la información.** Además el `.ts` podría estar
  a medias: recompilar sería commitear código sin terminar.
- **Toca:** `protocol-close` Paso 5b, y cualquier control que se escriba después.

### [D-017] 2026-08-03 — Que el `.js` esté al día lo vigila el cierre, no `pytest`

- **Se eligió:** poner la comprobación en `protocol-close` (Paso 5b), disparada
  por el `session-closer` antes del `git add`.
- **Contra:** un test más en `pytest`, que se dispararía con los otros 121.
- **Por qué:** los 121 tests preguntan *¿el código se porta bien?*. Este pregunta
  *¿lo que commiteaste es lo que hiciste?*. Son cosas distintas, y hay dos
  señales que lo demuestran:
  - 🔑 **Si el arreglo no toca el código, la comprobación no estaba mirando el
    código.** Cuando este control se pone rojo, los dos archivos son correctos
    por separado; lo que falta es correr `npm run build` y commitear. Es una
    acción sobre el repositorio.
  - **En producción no se puede ni formular.** En el servidor solo está el `.js`;
    el `.ts` no viajó. Una comprobación que se evapora al desplegar no hablaba
    del producto, hablaba de la mesa de trabajo.
  - Es la **misma familia** que [L-006]: "¿el commit llegó a `origin`?" y "¿el
    `.js` es el de su `.ts`?" preguntan lo mismo. Esa pregunta ya tenía dueño.
  - **Y mantiene la suite sin red** ([C-001]): meter `tsc` en `pytest` ataría los
    tests de Python a Node, y con `npx` de por medio, a internet.
- **El argumento que se descartó, y por qué era malo:** se recomendó `pytest`
  diciendo "un freno que depende de tu memoria no es un freno". El principio es
  correcto; la aplicación estaba mal. El closer se dispara solo, igual que el
  push — no depende de la memoria de nadie. Ver [L-008].
- **Toca:** `protocol-close`, `session-closer`, `tests/test_api.py` (el test se
  renombró a `test_the_script_is_served` y su comentario dice qué **no** mide).

### [D-016] 2026-08-03 — El `session-closer` hace `git push`; solo `--force` sigue prohibido

- **Se eligió:** darle el `git push` al closer, como Paso 6b del protocolo, y
  obligarlo a comprobar después con `git status -sb` que ya no dice `ahead`.
- **Contra:** dejar la prohibición como estaba y que el closer solo **detectara**
  el `ahead` y lo reportara en "Sin resolver", para que el push lo hiciera una
  persona. Fue lo que se implementó primero, y el usuario decidió lo otro.
- **Por qué:** la prohibición original decía *"tu trabajo es añadir historia,
  nunca reescribir ni borrar la que hay"*, y metía `git push` en la misma lista
  que `--amend`, `reset` y `--force`. Pero 🔑 **un `git push` a secas solo añade:
  encajaba con la razón de la regla y estaba prohibido por su letra.** Lo que
  reescribe historia es `--force`, y ese se queda fuera junto a los demás.
  La alternativa —detectar y avisar— dejaba el cierre dependiendo de que alguien
  leyera el aviso, que es justo el eslabón que fallo en [L-006].
- **Toca:** `.claude/skills/protocol-close/SKILL.md` (Paso 6b nuevo y lista de
  prohibidos), `.claude/agents/session-closer.md` (sus límites, que repetían la
  lista por su cuenta y se habrían contradicho) y todo cierre de sesión futuro.

### [D-015] 2026-08-03 — El `data/score.json` global se borra, no se adopta

- **Se eligió:** borrar el marcador global de 19 puntos que dejó el paso 3.
- **Contra:** adoptarlo como marcador de la primera persona que se registrara, o
  dejarlo huérfano en `data/` junto a la carpeta nueva `data/users/`.
- **Por qué:** esos 19 puntos salieron de probar los pasos 1, 2 y 3, y no son de
  nadie que estuviera practicando inglés. **Adoptarlo obligaría a inventarle un
  dueño**, y eso es escribir una mentira dentro de los datos: mañana ese "juan"
  con 19 puntos parecería historia real. Dejarlo huérfano es peor todavía — un
  archivo con pinta de significar algo que ya no significa nada. Y como `data/`
  no va a Git, no se pierde ningún historial al borrarlo.
- **Toca:** `data/`, y el criterio para cualquier migración futura de datos.

### [D-014] 2026-08-03 — El nombre se normaliza y se valida con lista blanca, y se valida dos veces

- **Se eligió:** `normalize_user` en `app/tools.py` hace las dos cosas —bajar a
  minúsculas y quitar espacios, luego rechazar lo que no sirva— con **cuatro
  frenos**: vacío, largo máximo (32), lista blanca `^[a-z0-9_-]+$` y nombres que
  Windows reserva (`con`, `prn`, `aux`, `nul`, `com1`–`com9`, `lpt1`–`lpt9`).
  Y se llama en **dos sitios**: en `app/api.py` para rechazar pronto con un 422
  explicado, y dentro de `score_file` porque es quien toca el disco.
- **Contra:** una lista negra de caracteres peligrosos; validar solo en la puerta
  de red; validar solo en `tools.py`; y dejar que el navegador validara.
- **Por qué:** con este nombre se construye una **ruta de archivo**, y el nombre
  lo escribe cualquiera desde el navegador. Una lista negra siempre deja algo
  fuera; la lista blanca hace que el olvido falle hacia el lado seguro, que es lo
  que pide `_context/architecture.md`. Tres matices que costaron entenderse:
  - **Normalizar no es validar.** Windows no distingue mayúsculas y Linux sí:
    sin normalizar, `Juan` y `juan` serían **una** persona en local y **dos** en
    la nube del paso 7, sin ningún error y con todos los tests en verde.
  - **Validar los caracteres no es validar el nombre.** `con` es solo letras,
    pasa la lista blanca entera, y Windows lo reserva incluso con extensión.
    El vacío y los nombres larguísimos también se cuelan por ahí.
  - **Validar dos veces no es duplicar.** La puerta rechaza *pronto y con
    explicación*; `score_file` rechaza porque no puede fiarse de quien la llame.
- **Toca:** `app/tools.py`, `app/api.py`, `main.py`, y todo lo que en el paso 5
  y el paso 7 vuelva a convertir texto de fuera en una ruta.

### [D-013] 2026-08-03 — En el paso 4 la identidad es declarada, no verificada

- **Se eligió:** una casilla "Your name" en la pantalla, que el navegador
  recuerda en `localStorage` bajo la clave `teapp.user`, y que el servidor se
  cree sin comprobar nada.
- **Contra:** adelantar el paso 5 y hacer la identidad de verdad antes que la
  memoria.
- **Por qué:** es el mismo truco que `judge_grammar`, y por la misma razón. Se
  construye la tubería con la pieza falsa y **luego se sustituye la pieza, no la
  tubería**: si algo falla en el paso 5, la memoria por persona ya funcionaba
  ayer y el sospechoso queda solo. El roadmap pone memoria en el 4 e identidad en
  el 5 a propósito.
- ⚠️ **Lo que esto significa hoy:** cualquiera puede escribir el nombre de otra
  persona y ver —y sumar a— su marcador. Es **conocido y aceptado hasta el paso
  5**, no un descuido. `localStorage` es una comodidad para no reescribir el
  nombre, nunca una prueba de identidad.
- **Toca:** `frontend/app.ts`, `app/static/index.html`, `app/api.py`, y el paso 5,
  que tiene que **quitar** la casilla, no añadirle nada al lado.

### [D-012] 2026-08-03 — TypeScript con `tsc`: fuente en `frontend/`, el `.js` compilado sí va a Git

- **Se eligió:** escribir la pantalla en TypeScript de verdad y compilarla con
  `tsc`, como dice `_context/architecture.md`. Tres detalles concretos:
  - **El fuente vive en `frontend/`, la salida en `app/static/`.** Se editan solo
    los `.ts` de `frontend/`; los `.js` de `app/static/` los escribe el
    compilador. Dos carpetas y no una para que sea imposible confundirse sobre
    cuál se edita.
  - **`strict: true`.** Todos los avisos encendidos. Apagarlos sería pagar el
    costo de TypeScript sin llevarse lo comprado.
  - **`module: "es2020"`.** Un archivo suelto, sin `import` ni `export`, que el
    HTML carga con un `<script>` normal. Los módulos son un tema entero y no
    hacen falta hoy (PI-2). Se escribió primero `"none"` y **el compilador lo
    rechazó**: TypeScript 7 ya no acepta ese valor. Vale la pena anotarlo porque
    la documentación consultada no lo decía — 🔑 **el compilador es la única
    fuente que no se queda desactualizada.**
  - **Versión fija: `typescript` 7.0.2**, sin `^`. Misma razón que [L-002]: sin
    fijar, dos máquinas instalan compiladores distintos. Se consultó la
    documentación actual antes de escribir el `tsconfig.json` en vez de sacarlo
    de memoria — 7.0.2 es el compilador nativo, muy posterior a lo que el modelo
    recordaba.
- **Contra:** dos alternativas reales, no de paja.
  - **Escribir `app.js` a mano** y saltarse TypeScript en el paso 3.
  - **`app.js` con `// @ts-check` y JSDoc**, que da buena parte de los avisos sin
    compilar ni instalar nada.
  Se descartaron porque la elección de TypeScript **ya estaba tomada** en
  `architecture.md`. Cambiarla aquí habría sido decidir arquitectura de refilón,
  en medio de otra tarea. El costo previsto —instalar Node— resultó ser cero:
  ya estaba instalado (v25.8.1, npm 11.11.0), comprobado antes de proponer nada.
  📌 `// @ts-check` queda anotado como la salida buena si `tsc` diera problemas.
- **Por qué:** el aviso que se compra es concreto. El contrato de [D-008] es
  `verdict`, `words`, `score`; escribir `reply.verdcit` en JavaScript no es un
  error, vale `undefined`, y la pantalla muestra "undefined" sin explotar. Ese
  fallo miente en silencio y se busca en el sitio equivocado. TypeScript lo
  subraya al escribirlo.
  🔑 **Lo que el navegador lee es el `.js`, siempre.** El `.ts` no es una
  alternativa al `.js`: es su original. ⚠️ De ahí el riesgo real y previsible de
  esta decisión: **editar el `.ts` y olvidar compilar** deja el navegador
  comportándose como antes, con el código correcto delante. Queda escrito aquí
  para que el día que pase se busque en el sitio correcto.
  Y el `.js` compilado **se versiona** —contra la costumbre de ignorar lo
  generado— porque en la nube corre **un solo servicio, en Python**: allí no hay
  Node que compile nada. Si el `.js` no está en Git, el paso 7 sube una pantalla
  que no existe. `dist/` sigue en `.gitignore` de cuando se pensó compilar
  aparte; ya no aplica, pero no estorba y no se toca (PI-3).
- **Toca:** `package.json` y `tsconfig.json` (nuevos), `frontend/app.ts`,
  `app/static/app.js` (generado, versionado), y el paso 7, que debe subir
  `app/static/` con el `.js` ya compilado. `node_modules/` ya estaba ignorado.

### [D-011] 2026-08-03 — FastAPI sirve la pantalla: mismo origen, y CORS se descarta (T-029)

- **Se eligió:** que el mismo FastAPI que atiende `/practice` sirva también el
  `index.html` y el `.js` de la pantalla. Un solo servidor, un solo origen, desde
  el primer día de desarrollo y no solo en el despliegue. En consecuencia
  **T-029 (configurar CORS) se descarta**: no se hará, ni ahora ni en el paso 7.
- **Contra:** servir la pantalla aparte —en otro puerto local, o abriendo el HTML
  con doble clic— y configurar CORS con una lista explícita de orígenes, que era
  el plan de T-029 y estuvo a punto de escribirse hoy.
- **Por qué:** CORS solo existe cuando hay **dos orígenes**. Con la pantalla
  servida por el mismo FastAPI, el navegador ve un único edificio y no tiene nada
  que bloquear. 🔑 **La mejor configuración de CORS es no necesitar CORS.**
  T-029 no salía de ningún archivo del proyecto: se revisó `_context/
  architecture.md` y `_context/roadmap.md` a propósito antes de descartarla, y
  ninguno la pide. Al contrario, los dos empujan a un solo origen —arquitectura
  dice que la pantalla son *"archivos quietos"* y que con Next.js serían **dos**
  servidores encendidos en la nube "en vez de uno"; el roadmap describe el paso 2
  como *"una ruta, local"* y el 7 como subir *"la tubería entera"*—. La tarea
  venía de una previsión razonable ("navegador y servidor, seguro hacen falta
  permisos de origen") que no aplica a esta forma de montarlo. Es PI-2 en su
  forma más literal: **la pieza que no se añade no puede fallar, ni hay que
  entenderla, ni mantenerla, ni rehacerla en el paso 5.**
  Y mismo origen en local que en la nube quita una diferencia entre desarrollo y
  producción — de esas que solo se descubren el día del despliegue.
  ⚠️ **Si algún día vuelve a hacer falta CORS** —una pantalla servida aparte, u
  otro cliente— la regla ya está pensada y no se rediscute: **lista de orígenes
  explícita, nunca `allow_origins=["*"]`**. Tres razones. La que no es opinable:
  🚨 con `*` el navegador **se niega a enviar credenciales**, así que la
  identidad del paso 5 no viajaría. Las otras dos: con `*` cualquier página del
  mundo puede montar su pantalla encima de `/practice` y gastar la llave (regla
  5, minimizar factura), y contradice la regla 3, denegar por defecto.
  ⚠️ Y un límite que no hay que confundir después: **CORS nunca protege el
  servidor.** `curl` o un script de Python entran igual, porque no hay navegador
  que obedezca la cabecera. Lo que protege el servidor es la autenticación del
  paso 5.
- **Toca:** `app/api.py` (servir los archivos de la pantalla), el paso 3 entero
  —`index.html` y `app.ts` llamarán a `/practice` con ruta relativa, sin nombrar
  host ni puerto— y el paso 7, que sube un solo servicio. Cierra T-029 como
  descartada, no como pendiente.

### [D-010] 2026-08-02 — El detalle completo va al log; al navegador, un mensaje corto y sin rutas

- **Se eligió:** una sola regla para los dos lados del mismo problema en
  `app/api.py`. El `ScoreFileError` se registra **entero** con `logger.error` y
  se contesta un texto fijo sin ruta. Cualquier otro fallo se atrapa también, se
  registra con `logger.exception` —que guarda el traceback— y se contesta otro
  texto fijo. `Exception` y no `BaseException`, para que un Ctrl-C siga apagando
  el servidor en vez de acabar convertido en una respuesta HTTP.
- **Contra:** lo que había, que fallaba por los dos extremos a la vez. `detail=
  str(error)` **contaba de más**: devolvía la ruta absoluta del servidor, medida
  de verdad en la respuesta. Y un `PermissionError` **contaba de menos**: subía
  sin atrapar y salía como un 500 mudo, sin quedar apuntado en ningún sitio.
- **Por qué:** son dos públicos distintos, igual que el idioma en [D-005]. El
  mensaje de `ScoreFileError` se escribió para la terminal, donde saber qué
  archivo abrir es **ayuda**. Fuera del servidor esa misma frase es información
  regalada sobre cómo está organizado por dentro, y quien pregunta no puede
  hacer nada con ella. 🔑 **Quitar el detalle de la respuesta solo vale si el
  detalle queda escrito en otro sitio**; si no, se cambia un problema por otro.
- **Toca:** `app/api.py` y todo error que se añada de aquí en adelante — la
  regla es del proyecto, no de esta ruta. Cuatro tests nuevos en
  `tests/test_api.py`: dos comprueban que la respuesta no lleva la ruta, y dos
  que el detalle sí llegó al log (con `caplog`).

### [D-009] 2026-08-02 — Candado en memoria + temporal con nombre propio para dos peticiones a la vez

- **Se eligió:** dos arreglos distintos en `add_point`, porque son dos fallos
  distintos que el servidor destapó juntos.
  - **Un temporal por escritura**, con `tempfile.mkstemp(dir=path.parent)`. El
    `dir=` es obligatorio: fuera de la carpeta del definitivo, renombrar deja de
    ser atómico. Si el renombrado falla, el temporal se borra antes de dejar
    subir el error.
  - **Un `threading.Lock` que abarca la lectura Y la escritura juntas.**
- **Contra:** el nombre fijo `score.json.tmp` que puso [D-007], y un candado que
  abarcara solo la escritura. Lo segundo parecía suficiente y no lo es.
- **Por qué:** se midió con el servidor levantado y 50 peticiones simultáneas.
  Con el nombre fijo, entre 31 y 39 de 50 devolvían 500: una petición renombraba
  el temporal mientras otra lo sobrescribía, y Windows lo cortaba con
  `PermissionError: Acceso denegado`. Y de 50 puntos esperados el marcador
  guardaba 8, 10 o 12, con hasta 7 personas recibiendo el mismo número — porque
  entre `read_score` y `os.replace` había un hueco donde otra petición leía el
  mismo total.
  🔑 **La escritura atómica y el candado resuelven cosas distintas.** La primera
  protege de UNA escritura cortada por la mitad; el segundo, de DOS escrituras
  pisándose. [D-007] resolvió la primera y no tocaba la segunda. Un candado que
  abarcara solo la escritura tampoco: el problema no está en escribir, está en
  el hueco entre leer y escribir.
  Nada de esto se veía en la terminal, donde escribía una persona sola, ni en
  los tests, porque `TestClient` manda las peticiones de una en una.
- **Toca:** `app/tools.py` (`_SCORE_LOCK`, `add_point`) y cuatro tests nuevos con
  hilos de verdad en `tests/test_tools.py`. Deja la suposición [A-002]: el
  candado vale dentro de **un solo proceso**. El mismo patrón vuelve en el paso
  4, cuando el marcador pase a ser uno por persona.

### [D-008] 2026-08-02 — El tutor devuelve tres piezas separadas, no un texto cocinado

- **Se eligió:** que `respond` devuelva un `TutorReply` —un `dataclass` congelado
  con `verdict`, `words` y `score`— en vez de la cadena `"veredicto\nWords: 3\n
  Score: 7"` que devolvía antes. La ruta `POST /practice` publica esas mismas
  tres claves en su JSON. Quien junta las piezas en un texto es quien las va a
  mostrar: hoy `main.py`, mañana la pantalla del paso 3.
- **Contra:** dejar la cadena ya armada, que era lo que había y funcionaba
  perfectamente para la terminal.
- **Por qué:** el destinatario cambia en el paso 3. Un texto cocinado solo le
  sirve a quien va a imprimirlo tal cual; a `app.ts` lo deja sin opciones —no
  puede pintar el marcador en su sitio, ni resaltar el veredicto, solo volcarlo
  entero—. 🔑 **El agente manda los ingredientes, no el plato servido:** la
  presentación es de quien tiene delante a la persona, no del que calcula.
  Se hizo ahora y no en el paso 3 porque cambiar el contrato con la pantalla ya
  escrita cuesta el doble. El `frozen=True` es aparte: una vez contestado, nadie
  cambia el veredicto por el camino.
- **Toca:** `app/english_tutor.py` (`TutorReply`, `respond`), `app/api.py`
  (`PracticeResponse`), `main.py` (que ahora arma el texto él), y los tests de
  ambos. Fija el contrato que leerá `app.ts` en el paso 3.

### [D-007] 2026-08-02 — El marcador se escribe al lado y se renombra encima (escritura atómica)

- **Se eligió:** que `add_point` escriba el total en un archivo temporal de la
  misma carpeta (`score.json.tmp`) y luego lo mueva encima del bueno con
  `os.replace`. El temporal va **en la misma carpeta**, no en la de temporales
  del sistema, y se usa `os.replace` y no `Path.rename`.
- **Contra:** dejar el `write_text` de siempre, que era lo que había. También se
  descartó envolver la escritura en un `try/except` que restaurara el archivo
  viejo: eso no cubre el caso que importa —un corte de luz no ejecuta el
  `except`—, y añade código para no resolver nada.
- **Por qué:** `write_text` hace dos cosas seguidas, vaciar el archivo y luego
  llenarlo, y entre las dos hay un instante. Un Ctrl-C o un corte justo ahí deja
  el marcador partido. Esto cierra la causa de raíz que [D-006] dejó abierta:
  aquel arreglo enseña a **leer** un archivo roto sin pisarlo, pero el archivo
  roto lo estábamos creando nosotros. Renombrar es **una sola** operación del
  sistema de archivos: o pasó entera o no pasó, así que ante un corte queda el
  marcador viejo entero o el nuevo entero, nunca un pedazo.
  Los dos detalles finos tienen su razón: renombrar solo es atómico **dentro
  del mismo disco** —cruzar de disco lo convierte en copiar y borrar, que es
  justo lo que se evita—, y `Path.rename` revienta en Windows si el destino ya
  existe, mientras que `os.replace` pisa igual en Windows y en Linux.
- **Toca:** `app/tools.py` (`add_point`) y dos tests nuevos en
  `tests/test_tools.py`: uno comprueba que no queda basura `.tmp`, y el otro
  simula el corte de luz reventando `os.replace` con `monkeypatch` y verifica
  que el marcador viejo sigue legible. El mismo patrón se repetirá en el paso 4,
  cuando el marcador pase a ser uno por persona.
  ⚠️ Un corte real sí puede dejar un `.tmp` huérfano en disco. Es inofensivo: la
  siguiente escritura lo pisa, y `read_score` ni lo mira.

### [D-006] 2026-08-02 — El marcador roto avisa con `ScoreFileError`; ausente sigue siendo 0

- **Se eligió:** separar los dos casos que hasta hoy se confundían.
  - **Ausente** (no hay archivo) → `0`, y a seguir. Es el primer día.
  - **Roto** (existe pero no se entiende) → excepción propia `ScoreFileError`,
    con mensaje en español que nombra el archivo y dice qué le pasa.
  - `read_score` valida tres cosas: que sea JSON, que tenga la clave `score`, y
    que su valor sea un entero de verdad — descartando `bool`, que en Python
    hereda de `int` y colaría un `true` por un `1`.
  - `add_point` **no atrapa** el error: lo deja subir. Como lee antes de
    escribir, la escritura ni se intenta y el archivo roto queda intacto.
  - `main.py` sí lo atrapa, imprime el mensaje y sale. Es la única lógica que
    le corresponde, porque presentar errores a una persona es su trabajo.
- **Contra:** devolver `0` cuando el archivo no se puede leer, que era el camino
  fácil y el que no habría necesitado excepción ninguna. También se descartó
  dejar subir el `JSONDecodeError` de la librería estándar tal cual.
- **Por qué:** devolver `0` en silencio le diría "tienes cero puntos" a alguien
  que tenía seis, y encima le pisaría el archivo con un `1` en el siguiente
  intento. 🔑 **Nunca sobrescribas un dato que no lograste entender:** mientras
  el archivo roto siga entero, su marcador es recuperable a mano; en cuanto se
  pisa, ya no. Se comprobó de verdad — con el archivo partido a la mitad
  todavía se lee `"score": 6` dentro.
  Y la excepción es propia, no la de `json`, porque en el paso 2 FastAPI tiene
  que distinguir "el marcador está roto" —que es un 500 con su mensaje— de
  cualquier otro fallo. `JSONDecodeError` solo dice que algún JSON, en algún
  sitio, no se pudo leer.
- **Toca:** `app/tools.py` (`ScoreFileError`, `read_score`, `add_point`),
  `main.py` (el `try/except`), los 8 tests nuevos de `tests/test_tools.py`, y el
  manejo de errores del paso 2. La causa de raíz —`write_text` no es atómico, así
  que este arreglo curaba la lectura del archivo roto pero no impedía crearlo—
  quedó cerrada el mismo día en [D-007].

### [D-005] 2026-08-02 — Nombres en inglés, contenido en español

- **Se eligió:** partir el idioma por su función, no por el archivo.
  - **En inglés** lo que es *identificador*: funciones, variables, archivos,
    carpetas, ramas y mensajes de commit. Y los textos que ve quien usa la app,
    porque es una app para practicar inglés.
  - **En español** lo que es *explicación*: comentarios, docstrings, la
    conversación del chat, y los mensajes de error o de sistema.
  - Consecuencia inmediata: el agente es `english_tutor`, con guion bajo. Con
    guion no se puede importar — `import english-tutor` es un error de sintaxis,
    porque Python lee el guion como una resta.
- **Contra:** nombrar todo en español, que era el camino por defecto viniendo de
  un `CLAUDE.md` y un `_context/` escritos enteros en español.
- **Por qué:** son dos públicos distintos. El identificador lo lee Python, lo leen
  las librerías y lo lee cualquiera que abra el repo; ahí el inglés es el idioma
  franco y evita el híbrido feo (`contar_words`, `leer_score`). La explicación la
  lee quien está aprendiendo, y en su idioma se entiende mejor. El error de
  sistema es explicación, no interfaz: cuando algo se rompe, tiene que entenderse
  rápido y sin traducir.
- **Toca:** todo el código que se escriba desde el paso 1. Renombra los contratos
  acordados: `count_words`, `judge_grammar`, `read_score`, `add_point`,
  `respond`, y los archivos `app/english_tutor.py`, `app/tools.py`,
  `data/score.json`. Queda escrito en `CLAUDE.md`, sección "Cómo se escribe el
  código", como principio **PI-5**.

### [D-004] 2026-08-02 — El protocolo de inicio lee `_context/` siempre, no a demanda

- **Se eligió:** añadir `_context/scope.md` y `_context/roadmap.md` a la lectura
  obligatoria del Paso 1 de `protocol-start`, junto a `progress.md` y `tasks.md`.
  Encima, una regla que manda sobre todas: lo que el reporte diga sobre **qué es**
  el proyecto tiene que salir de un archivo abierto en esa misma corrida; si no
  está escrito, se dice "no está registrado". En `session-starter` se partió el
  límite de "no inventes" en tres: no inventar el proyecto, no dar un paso por
  completado con tareas abiertas de ese paso, y no recomendar prioridades.
- **Contra:** dejar `_context/` fuera del protocolo, como estaba, y confiar en que
  el agente lo abriera si lo necesitaba.
- **Por qué:** el agente arranca en frío y solo veía el *relato* del avance, nunca
  la *definición* del proyecto. Sin el ancla, el hueco lo rellena con lo que suele
  llevar un proyecto de este tipo — y suena convincente, que es lo peligroso. Los
  dos archivos son cortos: leerlos siempre cuesta poco y el reporte pasa a ser
  verificable. Lo de las prioridades venía de la corrida real de hoy, donde el
  reporte recomendó saltarse cuatro tareas abiertas: esa llamada es del usuario.
- **Toca:** `.claude/skills/protocol-start/SKILL.md` (Paso 1) y
  `.claude/agents/session-starter.md` (Límites). Las descripciones del frontmatter
  de ambos se actualizaron el mismo día para nombrar las tres fuentes reales —`git`,
  `_persistence/` y `_context/`— cerrando la T-009.

### [D-003] 2026-08-02 — Recuperar 4 principios de ingeniería de un `CLAUDE.md` anterior

- **Se eligió:** llevar a `CLAUDE.md`, en una sección propia "Cómo se escribe el
  código", cuatro principios de un `CLAUDE.md` genérico de proyectos IA/DS:
  razonar sin decidir en silencio, simplicidad primero, cambios quirúrgicos y
  "terminado = visto funcionando".
- **Contra:** copiar los seis originales tal cual.
  - Se descartó **"slices verticales / tracer bullet"**: el roadmap ya *es* eso
    —tubería completa con agente falso, modelo en el paso 8, "córrelo antes de
    seguir"—. Repetirlo sería duplicar.
  - Se descartó **"sin decisiones silenciosas"** como principio aparte: decía lo
    mismo que "razona antes de actuar", y su parte de documentar ya la cubre este
    archivo.
  - Se reescribió **"toda tarea tiene un test, sin excepción"**: la pantalla del
    paso 3 no se prueba con un test unitario. Quedó como "donde hay lógica, un
    test; donde hay pantalla, correrla".
- **Por qué:** `CLAUDE.md` prometía "la FORMA es de producto: estructura,
  commits, tests, frenos" sin ninguna regla detrás. Era una promesa sin cobrar.
  Y nada frenaba el refactor no pedido, que es justo lo que ensucia el `git diff`
  del que vive `session-closer`.
- **Toca:** todo el código que se escriba desde el paso 1.

### [D-002] 2026-08-02 — Los cuatro archivos del porqué los escribe la sesión principal, no el closer

- **Se eligió:** partir `_persistence/` por origen de la información.
  `progress.md` y `tasks.md` los escribe `session-closer` al cerrar; `decisions`,
  `assumptions`, `constraints` y `lessons` los escribe la sesión principal, en el
  momento en que las cosas pasan. El closer solo los **revisa** y señala huecos.
- **Contra:** que el closer actualizara los seis al final del día, como estaba
  planteado al principio.
- **Por qué:** lo que se hizo queda en el `git diff` y se puede reconstruir sin
  haber estado presente. Lo que se **decidió** no queda en ningún lado: nace en la
  conversación y ahí se muere. El closer arranca en frío, así que escribir esos
  cuatro sería inventar. Además, el porqué es lo primero que se evapora: anotarlo
  tres horas después es anotarlo a medias.
- **Toca:** `CLAUDE.md` (sección Persistencia), `protocol-close` (Paso 5) y el
  reparto de trabajo entre la sesión principal y `session-closer`.

### [D-001] 2026-08-02 — La skill de inicio se llama `protocol-start`, no `protocol-close`

- **Se eligió:** `protocol-start` para el protocolo de inicio de sesión.
- **Contra:** `protocol-close`, que fue el nombre con el que se creó.
- **Por qué:** el nombre describía un cierre y el contenido era el arranque. El
  nombre quedó libre para lo que de verdad lo necesitaba: el protocolo de cierre,
  creado después. Hoy el par es simétrico —`protocol-start` / `protocol-close`—
  y cada agente tiene el suyo.
- **Toca:** `.claude/skills/`, y el cuerpo de `session-starter`, que invoca la
  skill por su nombre.

<!-- La más reciente arriba. Formato:

### [D-001] 2026-08-02 — <qué se decidió, en una línea>

- **Se eligió:** <la opción>
- **Contra:** <las alternativas descartadas>
- **Por qué:** <la razón, no el resumen>
- **Toca:** <qué parte del proyecto condiciona>

-->
