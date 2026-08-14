# Lecciones aprendidas — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [L-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

| id | fecha | qué se aprendió | a raíz de |
|---|---|---|---|
| L-067 | 2026-08-15 | 🪞 **El cierre miró la casilla que ya estaba escrita y dedujo que el índice también: "no hay nada que actualizar" sobre un índice al que le faltaba el día entero.** `session-closer` verificó los cinco commits contra `git`, encontró el árbol limpio y concluyó que `progress.md` estaba al día — citando `[S-059]` como *"el detalle de hoy"*. **`[S-059]` es del 14.** La sesión del 15 —cinco commits, el cierre del paso 8, cinco lecciones— **no tenía fila en el índice**, y el índice es exactamente lo que se lee al arrancar. 🔑 **Por qué se equivocó, y no fue por pereza: la casilla `Estado actual` SÍ decía "PASO 8 CERRADO el 2026-08-15", porque la había escrito la sesión principal durante el día.** El cierre leyó una parte correcta del archivo y **generalizó al archivo entero**. Un archivo medio actualizado es peor que uno sin tocar: el trozo bueno avala al malo. ⚠️ **Y el árbol limpio fue lo que remató el engaño** — es la señal de *"no queda trabajo"*, y aquí significaba *"el trabajo se commiteó ANTES de que llegara el cierre"*, que es otra cosa. Ver `[L-029]`: lo que se escribe fuera del cierre no tiene quien lo recorra. 🧭 **Regla: el cierre no pregunta "¿está el archivo al día?" sino "¿tiene ESTA sesión su fila en el índice, con su id nuevo?".** Es una comprobación de una línea —`grep "^| S-0" progress.md | head -1` y mirar la fecha— y no la puede sustituir ninguna lectura de la cabecera. 📌 **Cuarta vuelta del mismo bicho en un día**, y la más incómoda porque cae en el protocolo que existe para evitarlo: `[L-062]` el estado, `[L-063]` la prosa nueva, `[L-066]` la entrada superada, y esta **el cierre que se cree al archivo que él mismo debía escribir** | `[L-062]`, `[L-066]`, `[L-029]`, `protocol-close`, `session-closer`, `progress.md`, cierre del 2026-08-15 |
| L-066 | 2026-08-15 | 🔎 **La corrección vive en la fila NUEVA, y quien busca por tema encuentra la VIEJA — por eso `assumptions.md` tachaba y `decisions.md` no.** Se arregló el guion de arranque para que leyera el campo de estado y se saltara lo tachado, **se corrió para comprobarlo** (`[PI-4]`), y las dos correcciones funcionaron — pero la corrida destapó dos fallos más, que resultaron ser **uno**: `~~D-071~~` citada con sus números (`8,0 s`, `read 4,0`) como si fueran los del código —lo son desde `[D-072]`: `9,0` y `read 6,5`—, y `~~D-080~~` presentada como *"decisión crítica abierta"* con `[D-081]` encima. 🔑 **Causa única: `decisions.md` no tenía convención de tachado.** `assumptions.md` la tenía desde hacía semanas; nadie la extendió al archivo de al lado, y el defecto esperaba ahí. ⚠️ **Por qué es difícil de ver, y esto es lo transferible: el índice se LEE por fecha pero se BUSCA por asunto.** `[D-072]` decía en su propia fila que corregía a `[D-071]` — perfecto para quien baja el índice en orden, **inútil para quien hace `grep "presupuesto del cliente"` y aterriza en la fila vieja**, que no dice nada de estar superada. **Una corrección solo protege si está en el sitio al que se llega, no en el sitio desde el que se corrigió.** 🧭 **Regla: al escribir una decisión que reemplaza a otra, tachar la vieja va EN EL MISMO CAMBIO** — 🔻 SUPERADA (sus números ya no son los del código) o ✅ CUMPLIDA (su mandato se ejecutó). Ni borrar (pierde el porqué) ni corregir en el sitio (la hace parecer que siempre dijo eso). 📌 **Tercera vuelta del mismo bicho en un día:** `[L-062]` el estado se pudre por detrás de las entradas; `[L-063]` la prosa nueva miente si no cita el código; esta, la entrada vieja no sabe que la superaron. **Las tres son la misma forma —una afirmación que fue cierta y nadie fue a apagar—** y las tres se pagan en el arranque siguiente. 🧪 **Y el hallazgo solo existe porque el arreglo se CORRIÓ:** leer el guion arreglado no habría enseñado nada; ejecutarlo devolvió dos fallos nuevos en el mismo reporte | `[L-062]`, `[L-063]`, `[D-071]`, `[D-072]`, `[D-080]`, `[D-081]`, `T-098`, `protocol-start`, corrida de verificación del 2026-08-15 |
| L-065 | 2026-08-15 | 🚪🚪 **Un aviso presente BAJA la guardia sobre el hueco de al lado. Dos de dos, y el mismo defecto exacto.** `T-089` e `install.sh`: aviso en mayúsculas *"NUNCA la llave como argumento"* a **tres** líneas de un ejemplo con la llave delante de `sudo`. `T-088` y `check_api_key.py`: aviso de que *"si cambian el límite en la consola, hay que cambiarlo aquí"* a **doce** líneas de *"da igual cuál sea el modelo"*. 🔑 **Dos archivos distintos, dos semanas de diferencia, un solo defecto: el archivo se molesta en avisar de UNA puerta y con eso mismo tapa que existe una SEGUNDA que el aviso no cubre.** ⚠️ **Y el mecanismo es psicológico, no técnico: un aviso presente se lee como cobertura.** Quien ve un párrafo en mayúsculas sobre el peligro X concluye que el peligro está atendido y deja de buscar; el hueco de al lado queda **más** protegido de la revisión que si no hubiera aviso ninguno. Es `[L-061]` (*"un precedente que no transfiere es peor que no tener ninguno: parece verificado"*) subido un nivel — de la cita al archivo entero. 🧭 **Regla para el paso 9: donde un archivo se molesta en avisar de una puerta, preguntar cuál es la segunda.** No *"¿es correcto este aviso?"* —los dos lo eran— sino *"¿de cuántas formas se rompe esto, y de cuántas avisa?"*. 📌 **Y es lo que convierte `[D-080]` de decisión defendible en regla con dos pruebas:** aquella eligió no cerrar el paso con UN dato y escribió honradamente su propio límite (*"ya hay una prueba"*); el segundo llegó con la misma forma, que es lo que descarta la casualidad. 🚨 En los dos casos el fallo era **mudo**: `ps aux` no da error, y `EXIT_OK` tampoco | `[D-081]`, `[D-080]`, `[L-061]`, `[L-064]`, `[L-050]`, `T-088`, `T-089`, `deploy/install.sh`, `deploy/check_api_key.py`, auditoría externa del 2026-08-15 |
| L-064 | 2026-08-15 | ⏳💣 **Una tarea APLAZADA espera; una tarea ARMADA tiene disparador. Aplazar la primera es gestión; aplazar la segunda es dejar el disparador sin dueño.** `[D-080]` decidió no cerrar el paso 8 hasta mirar las cuatro pendientes una por una, con un argumento correcto —`T-089` cambió de categoría en cuanto se tocó—, **pero sin la regla que dice qué se busca al mirarlas**. Al aplicarla salió: `T-081` está **aplazada** (nada la activa, y su daño ya está escrito en su propia ficha, así que no engaña), y `T-088` estaba **armada** — su ficha decía *"cuando toque el paso 9"* y `[D-049]` mete en el paso 9 el descenso a **Sonnet 5 y Haiku 4.5**, es decir, cambiar `MODEL` —dos veces—, que es exactamente lo que arma la trampa. 🔑 **No estaba aplazada AL paso 9: estaba armada PARA el paso 9.** 🔴 **Corregido el 15:** esta entrada decía *"el paso 9 es literalmente bajar a Haiku"*, escrito sin abrir el roadmap, que lo titula **"Observabilidad y evals con rúbrica"** (`_context/roadmap.md:23`) — `[L-063]` cometida al escribir `[L-064]`. Y la corrección **refuerza** la regla: el disparador es la ACCIÓN, no la fecha; atarlo a *"lo primero del paso 9"* lo habría dejado gastado antes del segundo modelo. Un comentario que afirmaba *"da igual cuál sea el modelo"*, colocado delante de la única persona que iba a cambiar el modelo, el día que lo cambiara. 🧭 **Regla: al revisar una pendiente, la pregunta no es "¿cuánto corre prisa?" sino "¿qué la dispara?".** Si el disparador es una acción planeada, deja de ser pendiente y se convierte en **bloqueante de esa acción** — se hace ya, o se reescribe colgada del disparador con dueño. **Suelta en una lista no vale**, que es justo lo que le pasó a `T-089`. ⚠️ **Y una lista de pendientes las iguala a todas por su aspecto** —tres renglones parecidos, tres 🔲— cuando lo que las separa no se ve en el renglón: si hay algo en el calendario que las active. 📌 `T-088` costó dos comentarios y cero lógica; el precio de aplazarla habría sido un portero mudo aceptando la llave del laboratorio en producción | `[D-080]`, `T-088`, `T-081`, `T-089`, `[L-061]`, `[L-050]`, `deploy/check_api_key.py`, auditoría externa del 2026-08-15 |
| L-063 | 2026-08-15 | 🆕 **La prosa recién escrita también miente, y contra eso no sirve releer más despacio: el código se cita AL LADO de la afirmación.** En un mismo arranque salieron cuatro citas torcidas. Las tres primeras eran **prosa vieja** —fases del cliente citadas como `connect 2,0 / write 1,0 / read 4,0 / pool 1,0` cuando `app/tools.py:245` dice `1,5 / 0,5 / 6,5 / 0,5`— y su diagnóstico fue *"el resumen se fía de la prosa y la prosa envejece"*. **La cuarta no encaja en ese diagnóstico y por eso enseña más:** se escribió ese mismo día, afirmando que las cuatro fases son *"cuatro relojes en paralelo"* y que el 9,0 cabe *"por construcción"*, cuando `app/tools.py:239` lleva puesto desde antes el aviso contrario —*"los 10 s de `api.py` NO sobran: son la única garantía de reloj de pared que existe"*—. 🔑 **Prosa nueva contradiciendo un comentario de código vigente. No hay envejecimiento que culpar: el archivo estaba abierto.** 🧭 **Regla, y sale de comparar los dos párrafos del mismo mensaje:** el párrafo que citó `tools.py:245` junto a la afirmación salió correcto; el que razonó sobre las fases **sin citar nada** salió falso en sus dos mitades. **Citar el fichero y la línea al lado de la frase no es cortesía para el lector: es el acto que obliga a mirar antes de afirmar.** Sin cita, se está recordando; con cita, se está leyendo. ⚠️ **Y la dirección del error fue la peligrosa:** presentar el 9,0 como "el techo real" y el 10,0 como "el hueco" invita a retirar el 10,0 por redundante, que es lo único que corta por reloj de pared (`app/api.py:730`). 📌 **Eco que no se calla:** los dos cierres anteriores de `[A-011]` murieron por colgarse de un techo inexistente (`[D-070]`, `[L-054]`). Tercera vez que este cierre se apoya en un techo. El argumento de hoy no falla — **la frase con que se contó sí era de esa familia**, y esa es la señal a la que hay que hacer caso | `[D-077]`, `[L-054]`, `[D-070]`, `[L-055]`, `app/tools.py:239`, `app/tools.py:245`, `app/api.py:730`, auditoría externa del 2026-08-15 |
| L-062 | 2026-08-15 | 🗺️ **El trabajo se hizo y se commiteó; lo huérfano fue la ACTUALIZACIÓN DEL ESTADO — y un `progress.md` sellado antes que el último commit miente en la dirección más cara.** `[D-080]` se escribió entera y se commiteó (`6c7b5a7`), cumpliendo `[L-029]` al pie de la letra. Pero `progress.md` se había sellado un commit antes (`8b9b37f`) y `6c7b5a7` **solo tocó `decisions.md`**: el archivo de estado quedó congelado con la frase *"esa decisión no está anotada — falta que el usuario la dicte"*, y el resumen de apertura del día siguiente la heredó y la sirvió como verdad. 🔑 **`[L-029]` decía "lo que nace después del cierre no tiene dueño" y lo curó commiteando en el momento. Esta es la vuelta que la regla no cubre: el commit tardío tiene dueño, pero el ARCHIVO QUE RESUME EL ESTADO no se recorre hacia atrás.** El índice apunta a las entradas; nada obliga a las entradas a corregir el índice. 🚨 **Y la dirección del error es lo caro:** el estado no dijo "ya está hecho" cuando faltaba —eso lo detecta cualquiera al ir a hacerlo—, dijo **"falta"** cuando ya estaba hecho. Ese fallo no se detecta: se paga **repitiendo trabajo terminado al arrancar la sesión siguiente**, que es exactamente el gasto que `_persistence/` existe para evitar. 🧭 **Regla: si un commit posterior al sello del día toca `_persistence/`, el mismo commit corrige la casilla de `progress.md` que queda desmentida** — o la sesión siguiente no lo sabrá. Un cierre no termina en el hash: termina cuando el estado y las entradas dicen lo mismo. ⚠️ **Modo de fallo mudo, familia de `[L-029]`:** el árbol está limpio, la suite en verde y ningún archivo a medias. Nada delata que el resumen esté citando una frase caducada | `[D-080]`, `[L-029]`, `progress.md`, commits `8b9b37f`/`6c7b5a7`, auditoría de apertura del 2026-08-15 |
| L-061 | 2026-08-14 | 🚨 **`sudo VAR=valor cmd` NO pasa una variable de entorno: pasa un ARGUMENTO de `sudo`, y los argumentos los lee toda la máquina.** El entorno de un proceso vive en `/proc/PID/environ`, que **solo lee su dueño** — por eso pasar secretos por entorno es correcto (`create_account.py`, `[D-063]`). Pero al poner `VAR=valor` **delante de `sudo`**, quien lo recibe en su línea de comandos es `sudo`, y las líneas de comandos son públicas. 🧪 **MEDIDO en la EC2 el 2026-08-14 18:54 UTC**, no inferido: `sudo FOO=secreto123 sleep 30 &` seguido de `ps aux` **desde la cuenta `ubuntu`** devolvió dos procesos con dueño **`root`** y el valor entero a la vista. 🔑 **Lo peligroso no era el fallo, era el precedente que casi transfiere:** `install.sh` tenía, con tres líneas de separación, un ejemplo de uso con la llave delante de `sudo` **y** un aviso en mayúsculas diciendo *"NUNCA como argumento"*. El aviso era correcto y el ejemplo lo violaba, porque una palabra (`sudo`) convierte lo uno en lo otro. **Un precedente que no transfiere es peor que no tener ninguno: parece verificado.** ✅ Arreglado: el guion ahora recomienda `read -r -s` → `export` → `sudo -E` (que **hereda** el entorno en vez de recibirlo como argumento). ✅ **Y no hubo que rotar nada:** `grep -c "sk-ant"` sobre `~/.bash_history` y `/root/.bash_history` dio **0 y 0** — el despliegue real del 13 ya había usado la forma segura. ⚠️ Severidad honesta: `ps` exige estar dentro de la máquina, así que es un **amplificador** de un acceso ya conseguido, no una fuga remota | `T-089`, `[D-063]`, auditoría externa del 2026-08-14, corrida en la EC2 |
| L-060 | 2026-08-14 | 📐 **Sellar la predicción es la mitad del método; la otra mitad es comprobar que el instrumento tiene RESOLUCIÓN para decidirla.** Antes de leer la barra del día 14 se sellaron **dos** predicciones a propósito para poder distinguirlas — `$0,180–$0,190` (derivación completa) y `$0,177–$0,187` (por resta) —, con la idea de que caer en `$0,177–$0,180` haría fallar la primera y aguantar la segunda. La consola dijo **`$0,18`** y **las dos se cumplen**. 🔑 **Y eso no es una victoria doble:** la consola redondea al céntimo, así que `$0,18` es `[$0,175, $0,185]` y **pisa las dos franjas a la vez**. La zona que iba a discriminar medía **tres milésimas** y el instrumento no resuelve menos de diez. **Se sellaron más cifras significativas de las que la pantalla podía leer.** 🧭 **Regla: antes de sellar dos predicciones que compiten, comprobar que la distancia entre ellas supera la resolución del instrumento que las va a decidir.** Si no, se busca otro instrumento o se sella una sola diciendo claro que esta lectura no separa las hipótesis. ⚠️ **Fallo de la familia silenciosa:** un criterio mal fijado que sale ROJO se investiga; este salió **verde por partida doble** y se lee como *"los dos modelos aciertan"* cuando lo cierto es *"la pantalla no distingue"*. Primo de `[A-018]`, donde un `0,00` con *"sin datos"* al lado se leyó como medición: **en los dos casos el instrumento dijo menos de lo que se le atribuyó**. ✅ Lo que sí quedó bien medido: `$0,18` cae dentro de la banda `$0,156–$0,205` sin ambigüedad — **la banda estaba bien dimensionada; la pareja de predicciones, no** | `[D-079]`, `[L-059]`, `[A-018]`, `[D-074]`, `T-095`, lectura del 2026-08-14 |
| L-059 | 2026-08-14 | 📏 **La cercanía no protege: `[D-077]` se contradijo DENTRO DE SÍ MISMA, a cincuenta líneas, mismo autor y mismo minuto.** La línea 110 registraba *"~361 y ~49 tokens por llamada"* (la corrida nueva) y la 161 mandaba *"comparar contra `60 × $0,00234`"* (precio medido con **247**). 🔑 **Desmonta una defensa que dábamos por buena:** el bicho de la sesión 33 era *"la misma cosa en dos archivos diciendo cosas contrarias"*, y la cura era escribirlas juntas. **Estar cerca pone los datos al alcance; no fuerza la resta. Leer en orden no es comparar.** 📌 **Lo único que habría mordido es ARITMÉTICO:** el `$0,1404` era un **producto ya resuelto** pegado en la prosa, y un número calculado a mano no se recalcula al releerlo — se lee como un hecho. **Una expresión delata sus entradas.** 🧭 Regla: en `decisions.md`, un número derivado de otros se escribe **como la operación con sus entradas visibles**, no como el resultado — que es el método que `measure_tutor.py` ya usaba para `MAX_CALLS_PER_RUN` y `TARGET_SAMPLES`. **El código ya sabía hacerlo y la prosa no lo heredó.** ⚠️ Y `[L-043]` había identificado bien el término dominante —*"la rúbrica pesa casi todo"*— y acto seguido lo trató como constante: **que la rúbrica domine el coste es justo lo que vuelve el coste sensible a editar la rúbrica** | `[D-078]`, `[D-077]`, `[L-043]`, `[D-058]`, `[D-066]`, `measure_tutor.py`, `T-094`, auditoría externa del 2026-08-14 |
| L-058 | 2026-08-13 | 📈 **«El peor de N» no es un techo: es un suelo que crece con N — y el hallazgo salió midiendo algo que no decidía nada.** La báscula local se corrió seis veces y el máximo subió cada vez: **44,9 → 45,9 → 49,2 → 50,6 → 56,3 → 62,4 ms, +39% y subiendo**. Ahí daba igual —sobraba por 30×—, pero el mismo estadístico estaba sosteniendo un número que **sí** decidía: `[D-072]` justificó `read = 6,5` como *"un 38% por encima de los 4,72 s de la peor de diez"*. `max(n=10)` **no estima una cota, estima un cuantil que se mueve con N**. 🔑 **El movimiento transferible es ese, y no lo puede hacer una auditoría externa:** coger un hallazgo de donde no importa y llevarlo a donde sí. Hay que estar corriendo el guion por sexta vez para verlo — nadie que lea el código lo encuentra. 🧭 **Regla: un número que decide algo no se ancla en `max(N)`. O se calcula por resta —lo que cabe en el presupuesto, sin depender de ninguna medida ([D-073])— o se compra un PERCENTIL DECIDIDO ANTES de medir.** Si se decide después, se tomará `max(N)`, que se sentirá más sólido cuanto mayor sea N y será el mismo error. ⚠️ **Y en el caso de red es peor que en el local:** la distribución local la produce esta máquina bajo una carga que elegimos; la del tiempo de generación la produce un sistema que no controlamos y **que no se está quieto** —capacidad, versión del modelo, carga del día—. Medirla hoy dice cómo era hoy. 📌 Tercera generación de `[L-041]`/`[L-044]`: allí el número no medía lo que su nombre decía; aquí **mide bien y envejece**, como `[L-045]` | `measure_local_parts.py`, `app/tools.py`, `[D-073]`, `[D-072]`, `[L-043]`, `[L-045]`, `[L-044]`, `[A-011]`, `T-093` |
| L-057 | 2026-08-13 | 🔬 **Un instrumento no puede medir el tope que hereda — y el arreglo fue lo que lo cegó.** `[D-071]` puso `read=4,0` en producción, y `measure_tutor.py` construye su cliente con `tools.TIMEOUT` **precisamente para medir el camino real** (`[L-043]`). Consecuencia: toda llamada que pasara de 4 s dejaba de ser una **muestra** y pasaba a ser un **error**. ⇒ **La cola de la distribución —lo único que hace falta para colocar bien ese tope— era exactamente lo que el instrumento ya no podía ver.** 🚨 **Y no produce un número falso: produce SILENCIO, disfrazado de "Anthropic tardó".** Correr la báscula al día siguiente para validar el reparto habría salido *"ninguna llamada pasa de 4 s"* — cierto y vacío, porque las que pasaban se estaban convirtiendo en excepciones. Un cero que significa "no hubo" y un cero que significa "no pude ver" se imprimen igual; es `[L-053]` (el `curl` mudo) en un instrumento que costaba dinero. 🧭 **Regla, y es una EXCEPCIÓN ESCRITA a `[L-043]`:** *"un guion que arma su propia llamada mide otra cosa"* sigue siendo cierto, pero **la báscula debe ser idéntica a producción en TODO menos en el tope que está intentando medir**. Si no, mide su propio tope. Aplicado: `MEASURING_READ_SECONDS = 30,0`, con el porqué junto a la constante y no en un índice. 📌 Es `[L-054]` un anillo más afuera: allí la premisa no comprobada estaba en el código, aquí está **en el instrumento que serviría para comprobarla**. Encontrado por auditoría externa el 2026-08-13 | `measure_tutor.py`, `[D-072]`, `[D-071]`, `[L-043]`, `[L-054]`, `[L-053]`, `[A-011]`, auditoría externa del 2026-08-13 |
| L-056 | 2026-08-13 | 🧟 **El invariante del pool se rompe solo, y basta un 504 para romperlo — MEDIDO, no razonado.** `app/api.py` afirmaba *"la cola del tutor nunca es el cuello de botella: si FastAPI no atiende más de 40 a la vez, nunca habrá 41 tutores pidiendo sitio"*. 🔴 **Falso en cuanto vence un timeout.** El invariante supone que cada petición viva ocupa **un** sitio del pool y solo uno; el 504 rompe ese emparejamiento: la ruta devuelve el error y **suelta su ficha de `anyio`**, pero `respond` sigue corriendo dentro —Python no sabe matar un hilo— y **el sitio del pool no se suelta**. Los zombis se acumulan y el pool se llena **con menos de 40 peticiones vivas**. 🔑 **Cómo se demostró, y es lo transferible: con peticiones SECUENCIALES.** `test_a_timed_out_tutor_keeps_its_pool_seat_with_nobody_waiting` lanza dos, una detrás de otra, que nunca coinciden vivas — y la tercera se queda en cola igualmente. **Para atacar un invariante de concurrencia no hizo falta concurrencia**: hizo falta encontrar dónde se rompe la contabilidad. Es `[L-045]` (*"para provocar contención se quita sitio, no se añade carga"*) llevado un paso más allá. ✅ **Y resuelve la contradicción que `[D-070]` dejó abierta:** de sus dos cargas, la falsa es *"no se forma cola"*; el reembolso **no es código muerto**, es lo que atiende a quien esperó detrás de un zombi. ⚠️ Se ve morder: con un sitio libre de más, la tercera arranca y el test cae. 📌 Misma raíz que `[L-054]`: sin techo real en el cliente hay 504, y con 504 hay zombis — los dos hallazgos son el mismo bicho a dos alturas | `app/api.py` (`TUTOR_POOL_SIZE`, `_TUTOR_POOL`), `tests/test_api.py`, `[D-070]`, `[A-011]`, `[L-054]`, `[L-045]`, `[L-042]`, `[L-013]`, auditoría externa del 2026-08-13 |
| L-055 | 2026-08-13 | 📍 **Los punteros de línea se escribieron ANTES de editar los archivos, y el propio commit los desplazó.** `[D-070]` citaba `app/tools.py:83`, `app/api.py:698` y `app/api.py:146`; al acabar el commit vivían en `108`, `714` y `162`. 🔑 **Y la firma delata que no es descuido:** el desfase de cada archivo era **exactamente cuántas líneas insertó el commit en él** (`tools.py` +8, `api.py` +14), y **el único puntero correcto apuntaba al único archivo que el commit no tocó** (`tests/test_tools.py:270`). Un fallo aleatorio no dibuja ese patrón. 🚨 **Y el aterrizaje puede ser peor que "no encuentras la línea":** `measure_local_parts.py` mandaba a `tools.py:83` *"para ver el techo"*, y con el desfase caía **dentro del comentario que afirmaba el techo falso** de `[L-054]`, no en la línea que fija el número. Un puntero desviado no lleva a ninguna parte; uno desviado **unas pocas líneas** lleva a algo plausible. 🧭 **Regla: los punteros se releen AL FINAL, contra el árbol ya escrito — nunca durante la edición.** Y donde valga, se cita el **símbolo** en vez del número: el nombre sobrevive al diff. 🔴 **AMPLIADA la misma tarde por el fallo que la propia regla dejó pasar:** decía *"punteros de LÍNEA"*, y por ese hueco se coló un puntero **por nombre** — `measure_local_parts.py` citaba en presente un test como guardián vivo **en el mismo commit que lo borraba**. 🔑 **Citar el símbolo protege del desplazamiento, no del borrado**, y arreglar media cosa da la sensación de haberla arreglado entera. Vale para cualquier puntero: líneas, nombres de test, archivos, anclas. 📌 Mismo defecto vivo en `[L-045]` y `[L-042]`, que citan `tools.py:82`. Encontrado por auditoría externa el 2026-08-13 | `[D-070]`, `[L-054]`, `[L-045]`, `[L-042]`, `measure_local_parts.py`, auditoría externa del 2026-08-13 |
| L-054 | 2026-08-13 | 🧱 **La premisa en la que se apoyaba todo venía citada de dos sitios, y por eso nadie la volvió a mirar.** `[D-070]` cerró `[A-011]` sobre *"el cliente corta a los 8,0 s pase lo que pase"* — un **techo impuesto**, presentado como más fuerte que una medida porque no depende de cuántas muestras se tomen. 🔴 **El techo no existe:** `httpx` no trata `timeout=8.0` como tope de la llamada, lo reparte a **cuatro fases con cronómetro independiente** (`connect`/`read`/`write`/`pool`) que **suman 32 s**; y `httpcore` aplica el `read` a **cada lectura del socket**, no al cuerpo entero. Se comprobaba con **un comando de una línea que nadie corrió**, gratis y sin red. 🔑 **Lo que lo hizo invisible: la premisa no nació en la entrada que se cayó.** Estaba escrita en `[L-045]` (*"corta el cliente antes"*) y en `[L-043]` (*"el cliente corta a los 8,0 s"*), las dos entradas correctas en todo lo demás. **Se heredó como dato, no como afirmación a verificar** — es `[L-034]` con otro dueño: allí eran citas que se propagaban por parecer verificadas, aquí es una **premisa**, y una premisa repetida en dos entradas tranquiliza igual que un test en verde. 🚨 **Y el disfraz era la propia virtud del argumento:** el razonamiento *"me apoyo en un techo, no en una observación"* es **correcto** y fue lo que dio confianza — solo que el techo era el eslabón sin comprobar. 🧭 **Regla: cuando un cierre se apoya en que "el sistema no deja pasar de X", eso ES la afirmación central y se mide primero, aunque venga citada de tres sitios.** ✅ Lo que sí aguantó: la medida barata que se hizo bien (56,3 ms locales) contestó exactamente lo que prometía. Falló la mitad que se dio por sabida. Encontrado por auditoría externa el 2026-08-13 | `[D-070]`, `[A-011]` (reabierta 2ª vez), `[L-034]`, `[L-045]`, `[L-043]`, `app/tools.py`, auditoría externa del 2026-08-13 |
| L-053 | 2026-08-13 | 🤫 **`curl -s` que no resuelve devuelve cuerpo VACÍO, y un `grep` sobre el vacío no dice "no medí": dice "no está".** La auditoría estuvo a un paso de escribir *"el despliegue contradice tu afirmación"* porque su `curl -s \| grep id="practice"` salió mudo; la corrida siguiente, en el mismo instante, dio `200` con los tres contadores. **La misma trampa había mordido antes ese día** en la sesión principal (`exit 6`, `000`). 🔑 `[A-017]` no cuesta una petición: **fabrica evidencia**, y la que fabrica tiene forma de hallazgo contra un despliegue correcto. 📌 El arreglo es de una línea: **mirar el código de estado ANTES que el cuerpo** (`-w "%{http_code}"` y el `exit`), o usar `--resolve` y saltarse el DNS | `deploy/README.md`, `[A-017]`, `[L-051]`, y el aviso del `000` en `deploy/console_steps.md` |
| L-052 | 2026-08-13 | 🎭 **El maniquí no solo tapa un fallo: tapa una DECISIÓN DE DISEÑO, y la devuelve el día en que es cara.** `[A-001]` —¿el marcador cuenta practicadas o correctas?— se escribió el 2026-08-02 y se resolvió el 2026-08-13: **once días**. No sobrevivió por descuido; sobrevivió porque **con el juez falso las dos lecturas daban el mismo número**, así que ningún test podía distinguirlas y nada empujaba a decidir. 🔑 Y la propia entrada predijo la factura al pie de la letra: *"en el paso 8 sería rediseñar la herramienta el mismo día que se enchufa el modelo, con dos sospechosos en vez de uno."* Pasó exactamente eso. 📌 **Lo transferible:** cuando una pieza se sustituye por un maniquí, hay que preguntar no solo *"¿qué fallo oculta?"* sino ***"¿qué pregunta deja de ser urgente?"*** — esa es la que vuelve, y vuelve tarde | `[A-001]`, `[D-066]`, `[D-049]`, `_context/roadmap.md` |
| L-051 | 2026-08-13 | 🗞️ **Datos nuevos dentro de un molde viejo: el despliegue estaba bien y la pantalla mentía.** Tras subir `[D-066]` al servidor, el navegador seguía mostrando `Words · Score` sin `Practice` — pero el `Score` que enseñaba **sí era el correcto**, porque los números llegan en cada respuesta y solo el HTML estaba cacheado. 🔑 **Esa mezcla es lo que engaña:** con todo viejo se sospecha del caché enseguida; con los datos bien y el molde viejo se sospecha del despliegue. Se resolvió mirando lo que el servidor manda de verdad (`curl` a la línea de contadores) en vez de lo que el navegador pinta. La ventana de incógnito es la prueba concluyente; `Ctrl+Shift+R` no siempre basta | `deploy/README.md`, `[D-066]`, `[L-007]` |
| L-050 | 2026-08-13 | 🎭 **Un comentario que dice justo lo contrario de lo que sostiene el código, y en el sitio donde la mentira sale gratis.** `check_api_key.py:62-63` dice del modelo *"da igual cuál sea… lo que interesa son las cabeceras"*. **No da igual:** los frenos de Anthropic se configuran **por modelo** —`[D-061]` los puso a `claude-opus-5` y la consola los enseña por modelo—, así que el `50` que hace de firma del laboratorio **es el 50 de `claude-opus-5`**. Cambiar `MODEL` deja al portero mirando otro cubo, con otro número: se vuelve **mudo** y deja pasar la llave del laboratorio. Y el comentario invita explícitamente a hacerlo. Es `[L-047]` con una tercera pata: el acoplamiento no eran dos sitios, eran **tres** | leer el guion mientras Anthropic estaba saturado |
| L-049 | 2026-08-13 | 🧟 **Una tarea muerta que reaparece con una FACTURA pegada deja de ser un duplicado y se convierte en la agenda del día.** `T-074` está cerrada desde el 2026-08-10, y aun así viajó viva en dos traspasos seguidos. El primer día volvió como duplicado y la cazó el cerrador — pero la caza vivió en el chat y **no tocó el disco**, así que el puntero viejo siguió en `progress.md` y el arranque del día siguiente lo volvió a servir. El segundo día volvió peor: como prioridad nº 1 y con una consecuencia inventada encima ("cuatro días de retraso, la máquina encendida se come el plan gratuito"), que ni estaba medida ni nombraba al culpable correcto. **La urgencia no se audita, se obedece** | el arranque del 2026-08-13 |
| L-048 | 2026-08-12 | 🟢🔴 **El tercer sabotaje pasó en VERDE, y el roto era el test.** Al construir `T-078` se saboteó cada capa nueva para verla morder. Los dos primeros salieron rojos; el tercero —mover la comprobación de la llave **detrás** de la escritura, el fallo exacto que `[D-063]` impide— **no lo cazó nadie**. 🔍 **La causa:** el test buscaba la primera línea que nombrara `check_api_key.py`, y esa línea **no es la llamada, es un comentario** que la explica doce líneas antes; el comentario queda arriba pase lo que pase. 🚨 **Lo peligroso no es que fallara, es que TRANQUILIZABA:** nombre correcto, aserción correcta, verde. Habría entrado en la suite como un guardián más y habría callado el día real. **Un guardián que se cumple solo es peor que ninguno** — el que no existe al menos no engaña. **Qué se hace distinto:** (1) un test que lee un archivo de texto mira las **líneas activas**, no los comentarios —`test_deploy_limits.py` ya tenía `líneas_activas` y aquí se reinventó peor—, y la cadena buscada tiene que ser la que solo aparece en lo que se ejecuta; (2) 🔑 **un sabotaje verde no prueba que la capa esté bien, prueba que el test no vigila** — `[D-060]` pedía ver morder cada capa; esto añade que el sabotaje **audita también al vigilante**, y aquí fue lo único que lo hizo. 📌 Misma familia que `[L-043]` y `[L-047]`: algo escrito que parece cubrir un riesgo y deja de auditarse **por parecerlo** | `T-078`, `[D-063]`, `[D-060]`, `tests/test_check_api_key.py`, `test_deploy_limits.py`, `[L-043]`, `[L-047]` |
| L-047 | 2026-08-12 | 🧭 **Un acoplamiento se anota donde va a mirar quien lo ROMPA, no donde lo entendió quien lo creó.** `[D-063]` hizo que `install.sh` aborte el despliegue si la llave devuelve `requests-limit: 50` —la firma del laboratorio de `[D-061]`—, y con eso el `50` pasó a vivir en **dos sitios**. La reacción natural fue documentarlo en `[D-063]`, donde se entendió. **Y ahí no lo iba a leer nadie:** el día que ese 50 suba a 80 para medir Haiku (cosa que `[D-061]` ya predice por escrito), quien lo haga **no está desplegando** — está afinando el laboratorio, y abre `[D-061]`, que es donde vive el número. 🔑 **La pregunta correcta no es "¿dónde lo entendí?" sino "¿quién va a romperlo y qué archivo va a tener abierto?".** 🚨 Y el fallo resultante es **mudo**: el laboratorio queda bien afinado, todo en verde, y la comprobación del despliegue deja de reconocerlo sin dar un solo error. **Qué se hace distinto:** el aviso va en los **dos** sitios, y manda el del sitio donde vive el dato; además el número en el código lleva encima de dónde sale y qué se rompe si se mueve — **un número desnudo es un número que alguien va a "limpiar"**. 📌 Misma familia que `[L-043]` un piso más arriba: no basta con que la advertencia exista, tiene que estar **en la ruta de lectura** de quien puede hacer el daño | `[D-063]`, `[D-061]`, `deploy/install.sh`, `[L-043]`, paso 9 |
| L-046 | 2026-08-12 | 🌩️ **El escenario que `[D-051]` decidió sobre el papel ocurrió de verdad: nueve `529 Overloaded` seguidos de `claude-opus-5` en ~50 s.** Salieron al intentar averiguar qué llave hay en el `.env` con una llamada mínima (`T-084`). No es un fallo del proyecto: Anthropic estaba saturado. 🔑 **Lo que enseña es lo que pasa entonces, y está en el código:** `app/tools.py:320` manda el 529 a la red de seguridad con `request_sent=True`, así que **se cobra la cuota y no se devuelve** — decisión consciente de `[D-051]`, denegar por defecto aplicado al dinero. Con `MAX_RETRIES = 0` (`[D-053]`), cada intento de quien practica es un intento perdido: **una racha así le come prácticas de sus 20 sin darle un solo veredicto.** ⚠️ **Y de paso mata una vía de diagnóstico:** las respuestas 529 **no traen cabeceras `anthropic-ratelimit-*`**, así que un fallo no sirve para leer contra qué límites se contó — comprobado, no supuesto. Tampoco las trae `count_tokens`, que además **no deja rastro en la columna "último uso"** de la consola: dos instrumentos gratis descartados el mismo día. 🧭 **Lo transferible: la tolerancia a la saturación es una decisión que hasta hoy nadie había VISTO.** `MAX_RETRIES = 0` se eligió para que el error llegara limpio, y sigue siendo defendible; lo que cambia es que ya no es teórico — conviene decidir a propósito si el paso 9 quiere un reintento con espera, sabiendo que un reintento también cuesta tokens de entrada. 📌 Sin decidir todavía; queda como observación con fecha, no como cambio  📎 **AMPLIADA el 2026-08-13, segundo episodio:** cuatro `529` seguidos comprobando la llave de `[D-065]`. La puerta 4 no distingue *saturado* de *llave mala*; lo separó un **control al lado** —correr una llave que ya se sabía buena, que falló igual—, no un reintento más. | `[D-051]`, `[D-053]`, `app/tools.py:320`, `T-084`, paso 9 |
| L-045 | 2026-08-12 | ⏳ **Un número medido de verdad que envejeció: sobrevivió a la máquina que lo produjo.** El plan de `T-079` era lanzar **23 peticiones a la vez** para provocar cola y ver disparar `TUTOR_TIMEOUT_SECONDS = 10.0`. El 23 no era inventado —está medido y escrito en `[L-013]` y en `app/api.py:689`— pero se midió **contra un pool de 20**, que era lo que `ThreadPoolExecutor()` sacaba de las CPUs de aquella máquina. 🚨 **Hoy `TUTOR_POOL_SIZE = 40` (`app/api.py:184`), puesto a mano justo para arreglar eso: con 40 sitios, 23 peticiones entran todas y nadie hace cola.** La corrida habría medido una espera de cero, el timeout no habría disparado y la conclusión —*"los 10 s aguantan"*— habría salido en verde sobre un escenario que no ocurrió, gastando saldo real para producirla. 🔑 **Y debajo hay algo peor: la cola quizá no pueda formarse nunca.** El invariante de `app/api.py:172` dice que el pool iguala las 40 fichas de `anyio`, así que la petición 41 espera **antes** de que arranque la ruta — antes del `submit` y antes de que el reloj empiece. Junto con que el timeout del cliente son 8,0 s (`app/tools.py:82`) contra 10 s de la ruta, los 10 s no pueden disparar ni por cola ni por modelo lento: lo único que les queda es que `respond()` **fuera del modelo** (`count_words` + `add_point`, que escribe en disco) se coma más de 2 s. 🧭 **Y el experimento ya estaba hecho, gratis:** `tests/test_api.py:1043` deja el pool en **1** *"para que el segundo tenga que hacer cola"*. **Para provocar contención se quita sitio, no se añade carga** — cerrar cajas, no traer clientes. Lo primero es un test con tutor de mentira y cuesta cero; lo segundo son llamadas reales contra un saldo de `$6,55`. ⚠️ Además la ráfaga no cabía: `quota.py:58` es `DAILY_LIMIT = 20` **por persona** y se cobra antes del `submit` (`app/api.py:668`), así que 23 desde una cuenta mete 20 y descarta 3 con un 429 que nunca toca al tutor. 🚨 **Y esto NO cierra `T-079`, que es lo que esta entrada casi tapa:** el test de la cola fija `TUTOR_TIMEOUT_SECONDS = 0.2` para correr rápido, así que prueba **el mecanismo** (quien no arrancó no paga) y **no dice nada del número 10**. Son dos preguntas y solo hay una contestada — *¿la cola devuelve la cuota?* ✅ probado y gratis; *¿10 s es el número correcto?* 🔲 sin contestar. 🧭 **Y la tarea que queda ya no es "cronometrar con concurrencia": es decidir qué hacer con un freno que no gobierna nada** — bajarlo por debajo de los 8,0 s del cliente para que muerda, o retirarlo y escribir por qué. Se lee, no se mide. 📌 Hermana de `[L-044]` con un día de diferencia y la forma invertida: allí el número **nunca** midió nada; aquí midió bien y **caducó**. La pregunta que caza las dos es la misma —*¿qué pregunta contestó el día que se escribió, y es la misma que le hago hoy?*—. Encontrado por auditoría externa el 2026-08-12, verificado contra el código antes de anotarlo | `[L-013]`, `[L-044]`, `[A-011]`, `app/api.py:162,172,184,668,689`, `tests/test_api.py:1043` |
| L-044 | 2026-08-11 | 🔢 **Un número con aspecto de medido que salía de un `len()`, y circuló tres veces sin que nadie preguntara de dónde venía.** `measure_tutor.py` traía `MAX_CALLS = 10` presentado como corte duro de gasto. Al mirarlo: **`SENTENCES` tiene exactamente diez frases**. O sea el diez no medía nada — era la longitud de una lista, y la tanda de `T-079` hizo diez llamadas *porque había diez frases*, no porque diez fuera un tope. 🚨 **Circuló tres veces con tres disfraces distintos:** (1) constante llamada `MAX_CALLS`, (2) "tope" con un comentario encima citando `[D-057]` y `[C-008]`, (3) argumento hablado — *"no hay diseño que pensar: el número ya lo tienes de `T-079`, diez llamadas"*. Cada paso lo hacía parecer más medido. 🔑 **Y lo que lo hacía cumplir tampoco frenaba:** `SENTENCES[:MAX_CALLS]`, un recorte de lista — con tope 10 y lista de 10, `[:10]` sobre diez elementos **no corta nada**. Un freno que nunca podía morder, con nombre de freno, y por eso nadie lo probó. 🧭 **Regla: un número que decide dinero se escribe como la operación que lo produce, no como su resultado.** `int(0.25 / 0.00234)` se puede auditar; `106` hay que creérselo, y `10` hay que creérselo aunque venga de un `len()`. Si la operación no cabe en el código, va en la entrada con sus dos factores. ⚠️ **Cómo se caza, que es lo transferible:** la pregunta no es "¿este número es correcto?" sino **"¿qué pregunta contestó el día que se escribió, y es la misma que le estoy haciendo hoy?"**. 📌 Tercera cara del mismo bicho en tres días con dueños distintos: `[A-011]` medía otro reloj, un resumen ensanchó un bloqueo, y este medía un largo de lista — **ninguno era falso, los tres estaban mal rotulados**. Es `[L-041]` en su forma más pura. Encontrado por auditoría externa el 2026-08-11 | `measure_tutor.py:49` antes de `T-083`; `[D-060]`, `[L-041]`, `[L-043]`, `[A-011]` |
| L-043 | 2026-08-11 | ⏱️ **Primera medición del tutor con el modelo real — y el reloj que vigilábamos no vigila lo que dice su nombre.** 🔴 **CORREGIDA el mismo día por auditoría externa: la primera versión tituló "`[A-011]` muere" y la tachó, midiendo un reloj que no es el suyo.** La báscula cronometra `judge_grammar`; `TUTOR_TIMEOUT_SECONDS` cronometra la **cola del pool más `respond()` entero**. `[A-011]` está REABIERTA como encogida. Diez llamadas a `claude-opus-5` (esfuerzo `low`) con frases A1, por `judge_grammar` y con el cliente de producción — no una imitación. **Tiempo de `judge_grammar`: 1,72 s / 3,33 s mediana / 4,72 s la peor DE DIEZ.** 🔑 **El reencuadre que la hace más fuerte: el timeout del CLIENTE (8,0 s) mide un subconjunto de lo que mide el de la RUTA (10 s) y además es más pequeño — así que en una llamada sin cola el de la ruta no puede disparar NUNCA.** Los 10 s jamás protegieron de un modelo lento; lo único que pueden frenar es la cola (`[L-013]`, `[L-042]`). ⚠️ El margen del cliente —3,28 s sobre 4,72— cuelga de **una sola observación**: n=10 con dispersión de 2,7×. No se toca el `8,0`: es el freno vivo. **Tokens: 247,2 de entrada y 44,3 de salida por práctica.** La entrada apenas se mueve (245–250) porque **la rúbrica pesa casi todo y la frase del alumno casi nada** — o sea el coste por práctica es casi fijo, y el tope de 500 caracteres de `[C-002]` protege un extremo que en uso normal no se toca. ✅ **De regalo, la rúbrica de `[D-049]` se comportó como se le pidió:** un solo error por respuesta, dos frases cortas, sin markdown, y las cuatro frases correctas reconocidas sin inventar correcciones. ⚠️ **Lo que la medida NO cubre, escrito para que nadie lo estire:** diez llamadas, una red doméstica, una hora del día, sin concurrencia y desde Windows — no dice nada del servidor de AWS ni de la cola del pool bajo carga. 🚨 **Y `[L-001]` mordió por tercera vez, DESPUÉS de las diez llamadas:** el resumen final llevaba emoji, `cp1252` lo tumbó con `UnicodeEncodeError` y el cálculo se perdió. Se rehizo con los datos ya impresos; recalcularlo llamando otra vez habría costado dinero. **En un guion que gasta, un fallo de impresión al final es un fallo caro** | `measure_tutor.py` corrido el 2026-08-11; `[A-011]` retirada, `[A-010]` encogida; `[D-049]`, `[C-002]`, `[L-001]`, `[L-039]` |
| L-042 | 2026-08-11 | ⏱️ **El camino del 504 sigue decidiendo dinero con `future.cancel()`, que responde a otra pregunta — y el bloque escrito hoy lo citó como el buen ejemplo a seguir.** `app/api.py:692` decide devolver la cuota con `never_started = attempt.cancel()`: eso contesta *"¿llegó a arrancar la tarea?"*, no *"¿se facturaron tokens?"*. 🔢 **La ventana está MEDIDA en las constantes, no estimada: el cliente de Anthropic corta a los `8.0 s` (`app/tools.py:82`) y la ruta corta a los `10.0 s` (`app/api.py:146`) → bastan 2 s de espera en la cola.** Con eso, una llamada que se agota conectando —cero tokens, `request_sent=False`— llega tarde al reloj de la ruta, `cancel()` devuelve `False`, y **se cobra una práctica que no costó un centavo**. 🚨 **La auditoría acierta el bicho y se pasa en el arreglo:** *no* basta con preguntarle a `request_sent` en vez de a `cancel()`, porque **en el instante del 504 la respuesta todavía no existe** — la tarea sigue corriendo, y esperarla es justo lo que el timeout evita. El dato llega después, así que devolver tarde exige un `add_done_callback`, o sea maquinaria nueva. **Es una decisión con precio, no una línea.** 📌 **Y lo importante es la fecha, no el bug:** `[D-023]` eligió *"ya estaba corriendo → se cobra"* cuando **no había forma de saber si se había facturado**. Desde `[D-051]` sí la hay. Una premisa dejó de ser incomprobable y nadie volvió a mirarla. 🔑 **Es `[L-041]` con otro dueño, el mismo día y en la misma función:** allí el proxy estaba en el nombre, aquí en el instrumento — y esta sesión lo citó en un comentario nuevo como *"la misma forma que el timeout de arriba"*, o sea **lo señaló de ejemplo mientras lo describía**. 🧭 **Regla: cuando se copia un precedente de la misma casa, se comprueba si el precedente sigue siendo válido — no solo si es el mismo patrón.** Detectado por auditoría externa el 2026-08-11 | `app/api.py:692`, `app/tools.py:82`, `[D-023]`, `[D-051]`, `[L-041]`, auditoría externa del 2026-08-11 |
| L-041 | 2026-08-11 | 🏷️ **`request_sent` no significa lo que su nombre dice, y la primera corrida real lo dejó por escrito en el log.** Al probar la app viva con una llave inválida a propósito, el servidor registró: `la peticion salio: no` … `Error code: 401 … 'request_id': 'req_011Cdw3g4CgkcsZFcSWv8qqS'`. 🔑 **Ese `request_id` lo emite Anthropic: la petición SÍ salió de la máquina, viajó, llegó y fue procesada** — y aun así el campo vale `False`, la cuota se devolvió, y **está bien devuelta**. Lo que el campo decide de verdad no es si el paquete salió, es **si se facturaron tokens**; `[D-051]` lo define correctamente en prosa (*"Cero tokens gastados"*) y `[D-055]` ya movió el caso del rechazo vacío a `usage`. **El nombre se quedó atrás.** 🚨 **El modo de fallo es concreto, no estético:** alguien lee `request_sent`, ve un `request_id` en el log, concluye *"esto es un bug, la petición sí salió"* y lo invierte. Con eso, cada 401 y cada 429 pasarían a cobrarse — y `[D-051]` dice justo lo contrario. 🔑 **Es `[L-040]` con el instrumento cambiado: allí un proxy en el CÓDIGO, aquí un proxy en el NOMBRE.** Un nombre que describe el mecanismo (*salió el paquete*) en vez del concepto que decide (*se facturó*) es un dato inferido de la forma, y se lee mal exactamente igual. 🧭 **Regla: cuando un campo decide dinero, su nombre dice el CONCEPTO, no el mecanismo que lo detecta.** `billed` / `tokens_billed` diría la verdad; `request_sent` describe la pista, no la conclusión. ⚠️ **No se renombra hoy, y eso es una decisión, no un olvido:** el nombre viaja por `app/tools.py`, `app/api.py`, siete tests y cuatro entradas de `decisions.md` (`[D-051]` a `[D-055]`), así que tocarlo dentro de `T-077` llenaría el diff del día de cambios que nadie pidió (PI-3). Queda anotado con su riesgo escrito; el renombrado es su propia tarea. 📌 Y salió de **correr la app**, no de leer el código: la suite entera pasaba en verde con el nombre igual de engañoso — PI-4 pagándose solo | primera corrida real de `T-076`/`T-077` con llave inválida, 2026-08-11; log de uvicorn; `[D-051]`, `[D-055]`, `[L-040]` |
| L-040 | 2026-08-10 | 🧾 **Se dedujo un dato de la forma de la respuesta teniendo el dato exacto al lado, dentro de la misma respuesta.** `[D-054]` decidía si devolver la cuota mirando si `content` venía vacío — un **proxy** de *"esto no se facturó"*. La API ya contestaba esa pregunta literalmente en `usage.input_tokens` / `usage.output_tokens`, en el mismo objeto, a un atributo de distancia. 🚨 **Y el proxy tenía un agujero real, no teórico:** sin streaming —que es como llama `judge_grammar`— un rechazo a **mitad** omite el parcial, así que llega con `content` vacío y `stop_reason="refusal"`, **calcado por fuera** al rechazo gratis y con los tokens ya pagados. Se devolvía cuota justo donde `[D-051]` manda cobrar. 🔑 **La forma general: un proxy no puede separar dos casos que tienen la misma forma.** Cuando dos respuestas distintas se ven idénticas, ninguna cantidad de razonamiento sobre su forma las distingue — hace falta un dato que no sea la forma. 🧭 **Regla: antes de inferir un hecho de la respuesta, buscar si el instrumento trae su propio contador de ese hecho.** Aquí el contador se tenía delante. 📌 **Y es `[L-036]` con otro instrumento**, comprobado en sus líneas 334–335: *"antes de citar la narración, mirar si el instrumento ya trae su propio reloj"*. Allí el reloj, aquí el contador; misma forma. 🚨 **De paso, esta entrada estuvo mal dos veces y la segunda fue peor:** la sesión principal declaró falsa esa cita y la retiró, tras abrir `[L-036]` y leer **trece líneas de ciento diecinueve** — el encabezado hablaba de cerrar `[A-014]`, se dio el juicio por hecho y la regla estaba noventa líneas más abajo, dentro de la misma entrada. 🔑 **Una lectura parcial se sintió igual que una comprobación**, que es literalmente `[L-034]` cometido dentro del párrafo escrito para denunciarlo. **Abrir la entrada no es leerla: si la regla puede estar en cualquier línea, la comprobación es `grep` de la frase, no un vistazo al principio.** ⚠️ Y llegó commiteada porque la revisión externa entró con la sesión ya cerrada — `[L-029]`, tercera vez esta semana. **Y el diagnóstico del día anterior estaba a medias.** El cierre concluyó que los dos fallos habían sido *de ejecución, no de conocimiento* (*"un comentario protege a quien lo lee; un test protege también a quien no"*). Esto no: **nadie en el proyecto sabía qué factura un rechazo hasta que se abrió la documentación.** Era un **hueco de conocimiento**, y no había test posible que lo cazara — no se escribe un guardián para una pregunta que nadie ha hecho todavía. 🔬 **Los cuatro hallazgos técnicos del paso 8 —el `max_tokens` compartido, el reloj de diez minutos, el rechazo gratis, el parcial omitido— salieron de abrir la documentación; ninguno salió de razonar.** Se detectó por auditoría externa, igual que `[L-038]` y `[L-037]` | `[D-054]` → `[D-055]`, `app/tools.py`, `[D-051]`, `[L-036]`, `[L-034]`, `[L-029]`, auditoría externa del 2026-08-10 |
| L-039 | 2026-08-10 | 🚨 **El guion que verificaba los guardianes MODIFICÓ lo que estaba verificando — y el daño sobrevivió a la verificación.** Para ver rojos los cinco guardianes nuevos se saboteó cada uno con un guion en Python: leer archivo, sustituir una línea, correr pytest, restaurar. Los cinco mordieron y los cinco se restauraron **con el contenido correcto**. Y aun así `git status` marcó `app/english_tutor.py` como modificado sin que `git diff` mostrara una sola línea. 🔑 **La causa: `Path.write_text()` en Windows traduce `\n` a `\r\n`.** El guion leyó LF, escribió CRLF, y el contenido era idéntico mientras los bytes no lo eran. Tres archivos —`tools.py`, `english_tutor.py`, `test_api.py`— pasaron a CRLF; en `tools.py` eso convertía el diff del día en **el archivo entero**, que es justo lo que PI-3 dice que no puede pasar (*"si viene lleno de cambios que nadie pidió, el registro deja de servir"*). 🔑 **La forma nueva, y es la que hay que recordar: el instrumento de verificación tocó al sujeto y no lo deshizo del todo.** Restaurar el *contenido* se hizo bien y se dio por hecho que eso era restaurar el *archivo*. Todos los controles de la casa vigilan al código (`no_network`, `no_data_writes`, los guardianes de `deploy/`); ninguno vigila al **guion suelto que se escribe para medir**, porque vive fuera de pytest y muere en cinco minutos. ⚠️ **Y el testigo que lo delató fue el más tonto de todos:** `git status` diciendo "modificado" mientras `git diff` no enseñaba nada. Esa contradicción es exactamente la señal de un cambio de bytes sin cambio de contenido, y se lee en dos segundos si uno mira el `git status` **después** de verificar y no solo antes de commitear. 🔧 **Regla: un guion que escribe archivos para medir se escribe con `write_bytes` o con `newline=""`, y al acabar se comprueba `git status`, no solo que la suite esté verde.** Verde y limpio son dos preguntas distintas. 📌 **Y de regalo, `[L-001]` mordió en la misma corrida:** el guion imprimía `✔`/`✘` para marcar cada sabotaje y la consola de Windows lo tumbó con `UnicodeEncodeError` a mitad del bucle — la lección número uno del proyecto, cuatro días después de escribirse, en un guion de usar y tirar donde nadie pensó que aplicaba | sabotaje de los cinco guardianes de `T-076`; `git status` tras la verificación |
| L-038 | 2026-08-10 | 🚨 **El resumen del cierre INVENTÓ un hecho cómodo y lo vistió con dos citas que lo desmienten.** `progress.md`, campo `siguiente acción` —el que se lee primero al día siguiente—: *"no hace falta encenderla a mano, el apagado y encendido ya son automáticos (`[D-045]`/`[D-046]`)"*. `[D-045]` dice literalmente lo contrario (*"el apagado es automático…; **el encendido es manual**"*), `console_steps.md:416` también (*"**no se enciende sola**: hay que venir a la consola"*), y `[D-046]` **ni menciona encender** — es el temporizador que apaga. 🔑 **Esto NO es `[L-034]`**: allí una cita real apuntaba a la entrada equivocada por colisión de identificadores. Aquí **la afirmación no venía de ninguna parte** — se fabricó al comprimir, y los corchetes se le pegaron después como armadura. Dos identificadores al lado bastan para que nadie baje a comprobar. 🧭 **La dirección del error es el diagnóstico, y es lo que hay que recordar: lo inventado fue siempre la versión CÓMODA** (*"no hace falta hacer nada"*), nunca la incómoda. Un resumen comprime, y **la compresión deriva hacia lo tranquilizador**, porque una frase que no pide nada al lector no genera fricción al escribirla. 🏗️ **Causa estructural: quien escribió esa frase no había visto la máquina.** `session-closer` arranca en frío y reconstruye del `git diff` —para eso existe (`[D-002]`)—, y el diff **no dice si una máquina está encendida**. Una afirmación sobre el estado físico del mundo no se puede reconstruir de un diff, y por tanto no le toca a quien no estuvo. 📡 **Y viajó por DOS canales, no uno:** la sesión principal repitió la frase en su resumen hablado al usuario, leyéndola del reporte del cierre sin abrir las fuentes — el mismo fallo que la lección describe, cometido al relatarla. 💰 **El daño no es la molestia de un viaje a la consola:** `T-056` necesita SSH y la máquina amanece apagada, sí, pero lo grave es que el encendido manual **es el mecanismo**, no una carencia — `[D-045]` lo escribió asimétrico a propósito para que el olvido caiga del lado que no cobra. La nota no rompía la máquina: rompía **la decisión diaria de gastar dinero**. 🧭 **Qué se hace distinto: (1)** en `siguiente acción`, toda afirmación sobre el estado físico de la máquina se escribe en **pesimista por defecto** —"amanece apagada mientras no conste lo contrario"—, que es la regla 3 aplicada a los hechos y no a los permisos; **(2)** el closer no afirma estado del mundo: describe lo que el diff respalda y **manda al Paso 5b**; **(3)** al relatar un reporte ajeno, las frases que dicen *"no hace falta"* se abren antes de repetirlas — son las que nadie audita. 📌 Detectada por revisión externa, no por el proyecto: es `[L-037]` otra vez, un control que mira hacia dentro no ve lo que se escribió de más | `progress.md`, `session-closer`, `[D-045]`, `[D-046]`, `[L-034]`, `[L-037]`, `[D-002]` |
| L-037 | 2026-08-10 | 🚦 **El andamio se volvió el trabajo, y ningún control del proyecto podía verlo — porque todos miran hacia dentro de la sesión.** 📊 Contado sobre el índice de `progress.md`, no recordado (regla 6): pasos 0–6 = **12 sesiones / 3 días**; paso 7 solo = **22 sesiones / 6 días**. 🔑 **Lo que falla no es ninguna sesión: todas fueron defendibles.** `[L-034]` es real, el `is-enabled` era un hueco real, las 16 citas estaban mal de verdad. **El fallo es de suma**, y la suma no la mira nadie: cada cierre pregunta *"¿lo que hice hoy estaba bien hecho?"* y ninguno pregunta *"¿lo que llevo hecho me acerca a lo que vine a construir?"*. Un proyecto puede tener **todas** sus sesiones correctas y estar parado. 🚨 **El síntoma que sí era visible y nadie leyó como síntoma:** con HTTPS, identidad verificada, cuota por persona y apagado automático en producción, **el tutor seguía siendo el maniquí del paso 1** — la app para practicar inglés no practicaba inglés. Eso llevaba días escrito en `progress.md`, en la casilla `paso 7 de 9`, y se leía como *ubicación*, no como *aviso*. 👤 **Y lo detectó el usuario, no el sistema de persistencia.** `_persistence/` está diseñado para que no se pierda el porqué de lo hecho; **no tiene ningún instrumento que mida el coste de oportunidad de lo que se está haciendo**. La auditoría externa tampoco: audita lo escrito, y lo escrito era correcto. 🔴 **Agravante, medido en esta misma sesión:** al preguntar el usuario qué faltaba, la respuesta puso `T-069` como bloqueante del paso 8 — y era **falso**: *"pronto"* en `[D-030]` se mide contra el cierre de la cuenta (`[C-006]`, feb-2027), no contra el paso siguiente. Un pendiente **heredó su urgencia del sitio donde estaba escrito**, no de su plazo real. 🧭 **Qué se hace distinto:** al cerrar, **preguntar por el paso, no solo por la sesión** — *"¿qué falta para cruzar, y de eso qué es plazo real y qué es inercia?"*; y tratar *"la pieza central del producto sigue siendo un maniquí"* como una **condición que se nombra en voz alta cada cierre**, no como un dato de posición. 📌 Emparenta con `[LM.13]` (lo escrito no es lo medido) por el otro lado: aquí todo estaba medido, y aun así el conjunto no avanzaba | `[D-048]`, `[A-023]`, objeción del usuario del 2026-08-10 |
| L-036 | 2026-08-10 | ✅ **Cerrada `[A-014]` con `T-066`, y cerrada POR MITADES — la primera versión de esta entrada la dio por muerta con media medición.** (Sustituye a `[A-014]`, retirada hoy de `assumptions.md`; los punteros antiguos apuntan aquí.) 🚨 **La mitad que faltaba es la que aguanta un ataque:** que la cabecera **falsa** se descarte. Estaba medida en maqueta y **solo ahí**; en el servidor real se infería de que `Caddyfile.template:75` no declara `trusted_proxies` — *"está escrito, luego funciona"*, que es `[LM.13]` y que este proyecto ya había prohibido al partir `T-060` (*tener el grupo creado no es tener el cortafuegos*). ✅ **Medida el 15:14 UTC con el cubo de `181.58.39.253` ya agotado, lo que convierte el bloqueo en control:** cuatro peticiones —control sin cabecera, `X-Forwarded-For: 9.9.9.9`, la encadenada `9.9.9.9, 8.8.8.8` y `X-Real-IP: 9.9.9.9`— las cuatro `429` y las cuatro registradas como `181.58.39.253`. **Ni un `9.9.9.9` en el log**, y es un control que se puede **ver morder**. La otra mitad, la de las visitas honestas: computador `181.58.39.253` e `ipify` `181.58.39.253`; celular `191.153.227.163` e `ipify` `191.153.227.163`. Cinco `401` y un `429` desde cada aparato, dos `WARNING` con dos orígenes distintos, ninguno `127.0.0.1`. 🔑 **La trampa se desarmó ANTES de medir, y sin eso la prueba no valía:** el celular tenía que salir por datos móviles, porque en el WiFi de casa habría salido por el mismo router — y entonces *"una sola dirección en el log"* significaría a la vez *"el freno está roto"* y *"medí mal"*, dos cosas que se leen igual. Leer `ipify` en cada aparato **antes** separa esas dos ramas; leerlo después ya no. 🚨 **Y el criterio escrito antes se ganó el sueldo en el minuto exacto en que hizo falta:** el log dijo `191.153.227.163` y lo apuntado a mano decía `191.152.227.163`, un dígito. Con el criterio delante —*"cada una IGUAL a su `ipify`"`*— eso obliga a **parar**; sin él, dos direcciones distintas y ninguna `127.0.0.1` habrían pasado por buenas, porque el resultado ya *parecía* el correcto. Resuelto con una **lectura nueva**, no reinterpretando la vieja: era un dígito mal copiado al escribirlo, y la hipótesis alternativa (la operadora rotando la salida entre conexiones, plausible y que habría explicado el mismo dato) quedó ⚖️ **confirmada como falsa, no descartada a ciegas** — la segunda lectura de `ipify` ocurrió **después** de ver el log, sabiendo qué resultado cuadraría, y eso pesa menos que una lectura hecha sin saberlo; no mueve el veredicto, sí la palabra (corregido tras auditoría externa). 🔑 **`[D-040]` no prohíbe cambiar de idea con el dato delante: prohíbe cambiar el CRITERIO.** La duda se paga con una medición más, que aquí costó treinta segundos. 🏅 **Y hay una SEGUNDA demostración que no comparte instrumento con la primera:** el celular gastó **sus propios cinco intentos** antes del `429` — con el cubo del computador ya agotado a las `15:01:03`, si la app viera solo a Caddy el primer toque del celular a las `15:02:11` habría dado `429` en el acto. Se ve desde el navegador, sin entrar a la máquina; **dos testigos que no comparten instrumento valen más que uno bueno**, porque un instrumento averiado no puede producir los dos. Esta entrada la archivó como *"apoyo"* y la auditoría la subió a hallazgo. ⏱️ **Tercer hallazgo: el log traía su propio reloj y la primera lectura no lo usó.** El `faltan N s` sale de `login_guard.py:191` (`min(recent) + 900 - ahora`), así que despejando se reconstruye el inicio de cada ráfaga sin depender del relato: PC `899 s` → `15:01:01` (cuadra al segundo con la corrida), celular `879 s` → `15:02:11–12` (cinco intentos en ~21 s, coherente con formulario relleno), forjadas `64 s` → expiración `15:16:01`. Regla: **antes de citar la narración de quien midió, mirar si el instrumento ya trae su propio reloj.** 📌 Con esto muere la última suposición del proxy: `[D-034]` (Python), maqueta de dos contenedores (Caddy) y hoy la cadena real | `T-066` medida desde computador y celular; auditoría externa que escribió el criterio |
| L-035 | 2026-08-10 | 🚨 **El testigo que se recomendó para probar el disparo es CIEGO al disparo — y lo es por una decisión nuestra, escrita y bien razonada.** La auditoría propuso `systemctl list-timers` para convertir el descarte en medida, prediciendo *"`LAST` y `PASSED` ya deben venir llenos"*. Vinieron **vacíos**, y no por avería: `Persistent=false` —puesto a propósito en `teapp-shutdown.timer`, con doce líneas de comentario explicando por qué— le dice a systemd que **no lleve la libreta** de disparos pasados (`/var/lib/systemd/timers`). Sin libreta, al reiniciar el temporizador nace de cero: `Started teapp-shutdown.timer` a las 14:06:37, un estreno. 🔑 **`list-timers` no puede contestar "¿disparó ayer?" en esta pieza, y nunca podrá.** El testigo real estaba en otro sitio y sí sobrevive al reinicio: `journalctl -u teapp-shutdown.service` → `Aug 09 23:00:00 Starting teapp-shutdown.service … ([D-045])` seguido en el mismo segundo de `systemd-logind: The system will power off now!` — cadena causal con nuestro nombre dentro, no inferencia por eliminación. ⚠️ **La vuelta nueva sobre `[L-034]`:** allí el punto ciego era un descuido —se tenía a mano `is-active` y se usó—; aquí el punto ciego se **fabricó deliberadamente**, por una razón buena, y aun así se recomendó el instrumento como testigo del pasado. 🔑 **Un ajuste que apaga la memoria de una pieza también apaga los instrumentos que leen esa memoria**, y esa segunda consecuencia no se escribe en el comentario que justifica el ajuste — el comentario de `Persistent=false` habla del riesgo que evita (apagarse en la cara de quien acaba de encender) y no menciona que deja `LAST` mudo para siempre. 🔧 Regla: **antes de citar un instrumento como testigo, preguntar qué lo alimenta y si algo nuestro lo apaga.** Hermana de `[L-030]` (*preguntar qué pone a cero un instrumento antes de usarlo como registro*), con el agravante de que aquí quien lo puso a cero fuimos nosotros. 📌 De regalo, dos hechos que nadie pidió: Caddy salió limpio (`shutdown complete, exit_code: 0` — apagado ordenado, no tirón de cable) y la máquina volvió con **otro núcleo**, `6.17.0-1017-aws` → `7.0.0-1010-aws`: cada noche apagada es también una ventana para que la máquina cambie debajo | auditoría externa del cierre de `T-074`; el journal como testigo real |
| L-034 | 2026-08-09 | 🚨 **Un control que mide el AHORA no mide el MAÑANA — y hoy el mismo animal apareció DOS VECES, en el test y en el guion.** `install.sh` comprobaba el temporizador con `systemctl is-active`, bajo un comentario que declaraba su fallo *"el más mudo de los tres"*. Pero `is-active` no puede ver el estado que importa: **`activo pero NO habilitado`** sale `active` igual. 🔑 **Y ese es exactamente el modo de fallo de esta pieza:** apagaría puntual esta noche, `T-074` saldría **verde**, y al siguiente encendido el temporizador ya no vuelve — con el control habiendo **certificado lo contrario de lo que pasa**. Se arregla con la segunda pregunta, `is-enabled`: *¿volverá tras apagar y encender?* 🔁 **Lo grave no es la línea, es que es la SEGUNDA vez el mismo día.** Horas antes, el cuarto guardián de `tests/test_deploy_shutdown.py` nació buscando un texto literal que `install.sh` nunca escribiría — también incapaz de ponerse rojo ante el fallo real. Dos sitios distintos, misma forma: **un guardián que no puede ponerse rojo justo en el modo de fallo que su propio comentario nombra como el peor**. 🔍 Por qué se repite: el comentario se escribe pensando en el **fallo**, y la comprobación se escribe pensando en la **herramienta que se tiene a mano** — y nadie vuelve a leer las dos juntas. 🔧 Regla: **después de escribir un control, leer su comentario y preguntarle "¿esta comprobación se pondría roja en el caso que acabo de describir?"**. Si la respuesta no es un sí evidente, el control mide otra cosa. 🚨 **Y el antepasado está más cerca de lo que nadie esperaba: `[L-017]` es el MISMO archivo, el MISMO bloque y la MISMA orden `is-active`** —*"el comentario correcto hizo de coartada: nadie audita un bloque que ya se declara auditado"*—. Cuatro días después, al añadir una comprobación nueva a ese mismo bloque, se reintrodujo el atajo que `[L-017]` había arreglado. 🔑 **Lo que `[L-017]` no podía saber sola: arreglar un bloque no lo inmuniza, lo deja MÁS peligroso** — a partir de ahí lleva la cicatriz de haber sido auditado, y esa cicatriz avala también lo que se añada después. Familia de `[L-020]` (*un verde producido por algo distinto de lo que el verde afirma*), que ya iba por su cuarta aparición en `[L-027]`; lo que aporta esta es **la causa**: un control sin estrenar da miedo y se revisa, uno en verde tranquiliza y ya no lo mira nadie. 🔴 **Y la primera versión de esta entrada citó mal a `[L-013]`** heredando la cita de `[D-041]` y `[L-028]` sin abrirla — `[L-013]` dice *"cerrar un hueco no cierra los demás"* y lo dice desde `499879a`, sin una edición. La cita equivocada se propaga **por parecer verificada**, que es esta misma lección en la capa de la documentación. Corregido: `is-enabled` en `install.sh` y quinto guardián con su control rojo. 360 → **362** | revisión externa de `install.sh` tras el cierre del 2026-08-09 |
| L-033 | 2026-08-09 | 🚨 **El rodeo perdió la palabra que lo hacía cierto — dos veces, y la segunda la produjo el resumen de inicio de sesión.** `[A-017]` dejó escrito *"entrar por SSH usando la IP fija"*. Al contarlo, dos veces se quedó en **"entrar por la IP"**: el 08 en el traspaso hablado, y hoy en el arranque de sesión, que lo presentó como rodeo para el navegador. 🔑 **Y sin la palabra `SSH` el consejo no queda vago: queda FALSO.** Medido hoy: `https://32.199.55.191` → `000`, y también con `-k` — Caddy solo sirve el nombre para el que tiene certificado, así que el saludo inicial ni siquiera ocurre; no es un aviso que se pueda aceptar en el navegador. El reparto correcto es **SSH → por la IP; navegador y `curl` → por el nombre**, y si el DNS falla, `curl --resolve teapp.duckdns.org:443:32.199.55.191`. ⚠️ **Lo caro no es el `000`: es lo que se concluye de él.** Quien mida `T-074` mañana entrando por la IP obtiene un `000`, y el `000` **no dice "mediste mal"** — dice *"el redespliegue rompió algo"*. Un instrumento equivocado que además **acusa a otro**. 🔧 Regla: **un rodeo se anota con su protocolo pegado, nunca solo con su dirección** — la dirección sobrevive al resumen, el protocolo no. 📌 Es hermano de `[LM.13]` (lo que solo vive en el chat es una nota, no un freno) con una vuelta más: **aquí sí estaba escrito**, y aun así se perdió al recontarlo — o sea que estar escrito no protege del resumen, y el sitio donde el resumen se fabrica es el arranque de sesión | corrección externa al reporte de inicio del 2026-08-09 |
| L-032 | 2026-08-09 | ✅ **Cerradas `[A-005]` y `[A-008]` con la misma medida — y lo que enseñan es que el resto de una medición barata es justo lo que el instrumento barato no puede ver.** (Sustituye a las dos, retiradas hoy de `assumptions.md`; los punteros antiguos apuntan aquí.) `[L-024]` corrió `install.sh` **entero en un contenedor**, sin gastar un céntimo, y mató el miedo de verdad: el guion **no pisa la llave** (dos corridas, misma huella `7915abd41bf6`; y borrar el `.env` la cambiaba, así que la medida podía ponerse roja). Lo que quedó vivo después no fue un descuido — fue **exactamente lo que un contenedor no tiene**: `systemd` levantando el servicio, un disco que sobrevive, y una sesión abierta en un navegador. 🏁 Las tres se midieron en la máquina real: `T-065` el reinicio (08), y hoy el redespliegue (`T-050`) con `git pull aff4350 → 0dfdbba` + `install.sh` en código 0. **Evidencia, y son tres cosas distintas que no se sustituyen:** huella del `.env` idéntica antes y después (`1f0365563d…`, nunca impresa entera) → el guion no tocó la llave; `data/users/jorge.json` con fecha **2026-08-08 18:25:15** y `{"score": 5}` → el redespliegue no reescribió los datos; **F5 en la pestaña que ya estaba abierta → *"Signed in as jorge"*** → la cadena entera. 🔑 **Solo la tercera prueba lo que importa:** las dos primeras pueden salir verdes con la sesión muerta —bastaría que `teapp.service` leyera otro `.env`—, porque miran **archivos**, y la promesa era sobre **una sesión viva**. 🔧 Regla: cuando una medición barata deja un resto, **el resto no es "lo que faltó por hacer": es la lista de lo que ese instrumento era incapaz de ver**, y se nombra al escribirla. Misma forma que `[L-031]` | `T-050` medida en máquina real; cierre de `[A-005]` y `[A-008]` |
| L-031 | 2026-08-09 | ✅ **Cerrada `[A-009]` — y lo que enseña es dónde acaba lo que Python puede probar.** (Sustituye a `[A-009]`, retirada hoy de `assumptions.md`; los punteros antiguos apuntan aquí.) Nació el 2026-08-04 con un hueco que se encontró **el mismo día que se escribió el código**: `conftest.py` apagaba `TEAPP_COOKIE_SECURE` con `autouse`, así que **la rama por defecto —que es producción— no corría en ningún test**. 🔑 *El camino por defecto es el que menos se prueba, precisamente porque las pruebas lo apagan para poder trabajar.* `T-052` (2026-08-06) le puso testigo: cuatro tests mirando la cabecera `Set-Cookie` **en crudo**, en los dos sitios (`_start_session` y el `delete_cookie` de `/logout`), con sabotaje doble. **Y aun así no la mató**, porque eso era *"Python hablando consigo mismo"*: prueba lo que el servidor **envió**, no lo que un navegador **hace** con ello. 🏁 Muere el 2026-08-09 en la máquina real, con dos medidas y no una: **(1)** la cookie `session` guardada por `https://teapp.duckdns.org` con `Secure ✓`, `HttpOnly ✓`, `SameSite Lax`; **(2)** F5 sin volver a escribir credenciales → *"Signed in as jorge"*. 🔑 **Son dos hechos distintos y el segundo es el que faltaba:** `Secure` decide que se **guarde**, `SameSite` decide cuándo se **devuelve** — y un navegador que decide no mandar una cookie **no dice nada**. 🔧 Regla: **un test de Python cierra "qué mandó el servidor"; no cierra "qué hace el cliente".** Cuando la suposición habla de un cliente real, la última medida la hace un humano con un navegador, y eso **no es un defecto del plan**: `curl` no es un navegador, y llamarlo medida habría sido `[L-020]` | `T-051` medida en navegador real; cierre de `[A-009]` |
| L-030 | 2026-08-09 | 🚨 **Un instrumento que se REINICIA no es un registro — y ayer se le elogió justo por lo contrario.** `[A-018]` selló el `t=0` de la EC2 con `uptime -s` → `2026-08-08 15:54:27 UTC`, y escribió que su ventaja sobre la consola era que **"se relee cuando se quiera"**. Hoy se releyó: dice **`2026-08-08 18:11:15`**. No cambió la instancia — la reinició `T-065` esa tarde, y `uptime -s` no da cuándo **nació la máquina** sino cuándo **arrancó el sistema la última vez**. 🔑 **El valor de ayer sigue siendo correcto, pero dejó de ser comprobable con el instrumento que lo produjo:** pasó de *medido* a *anotado*, y nadie lo notó porque el número ya estaba escrito. ⚠️ **Es el error de las 15:08 con otro traje** —una hora tomada por `t=0` sin serlo— pero peor: aquel se cazó comparando dos horas, y este **se caza solo si alguien vuelve a mirar**, porque el instrumento no avisa de que se ha puesto a cero. 🚨 **Y `[D-045]` lo pone a reiniciarse TODAS LAS NOCHES**: a partir de mañana, `uptime -s` mide *"desde que encendí hoy"*, así que dividir dinero entre esas horas da una tarifa inflada. Las horas acumuladas tienen que venir de otro sitio (`[T-067]`), no de la máquina. 🔧 Regla: **antes de citar un instrumento como registro, preguntar qué lo pone a cero.** Si algo lo reinicia, sirve para medir **ahora** y no para fechar **el origen** | releer `uptime -s` al programar el apagado de `[D-045]` |
| L-029 | 2026-08-08 | 🚨 **Lo que nace DESPUÉS del cierre no tiene dueño.** El `session-closer` corre **una vez** y el commit del día ya está hecho: cualquier archivo escrito después cae en tierra de nadie. Hoy pasó con `[D-044]` —escrita a las 13:37, veinte minutos después del cierre de las 13:17— y se salvó solo porque la conversación siguió; con levantarse de la silla se quedaba en el disco. ⚠️ **Y no es un accidente raro: es donde va a volver a pasar**, porque en este proyecto las decisiones buenas salen conversando *después* de que el trabajo técnico acabó. 🔑 **Una costura no deja hueco:** al abrir mañana se lee un día que terminó limpio y sin nada pendiente, y nadie echa de menos lo que no está. 🔧 Regla: **lo que se escriba después del cierre se commitea en el momento, no se aplaza al día siguiente.** 📌 Se estuvo a punto de aplazar ESTA entrada por no ensuciar el árbol recién limpio — argumento estético que es el propio hallazgo aplicándose a sí mismo: **el árbol limpio no es el objetivo del protocolo, es su efecto secundario** | `[D-044]` escrita tras el cierre `84599f5`; revisión externa |
| L-028 | 2026-08-08 | 🚨 **Partir una tarea en dos deja al guion operativo describiendo la mitad vieja — y ningún `grep` lo encuentra.** `console_steps.md` paso 3 punto 5 decía *"Elastic IP: reservarla y asociarla"*, escrito cuando la IP no existía; al partirse `[T-059]` el 2026-08-06 se ejecutó **solo reservar** y el punto se quedó igual. Ejecutarlo al pie de la letra —que es lo que el archivo **manda** hacer— llevaba a `Allocate` y a una **segunda** dirección, y la IP que cobra es justo **la ociosa**. 📌 No costó dinero: lo cazó una revisión externa minutos antes del clic. 🔑 **La diferencia con `[L-018]` y `[L-025]`:** allí una copia diverge **porque alguien edita otra**, y se caza con `grep`; aquí **nadie editó nada — cambió el mundo que la frase describía**. No hay dos frases en desacuerdo, hay una sola que era verdad y dejó de serlo. 🔧 Regla: **el commit que parte una tarea revisa el guion que la ejecuta** — *¿algún paso escrito describe trabajo que ya está hecho?* ⚠️ Segunda mitad del mismo día: el aviso de no aceptar el `launch-wizard` (que dejaba el **22 abierto al mundo** y el grupo de `T-060a` sin usar) vivía **solo en el chat** — `[LM.13]` con otro traje. Los dos huecos se escribieron **antes** de tocar la consola | revisión externa antes de lanzar la EC2 de `T-059` |
| L-027 | 2026-08-07 | 🚨 **Esta vez el ciego fue el CONTROL, no la medida — y un control ciego devuelve el mismo verde que uno que funciona.** Midiendo `T-055` se hizo lo correcto: antes de creerse el resultado bueno (`origen 172.17.0.4`, la dirección real), arrancar uvicorn **sin** `--proxy-headers` para verlo fallar. **Salió verde igual.** No porque la cadena fuera robusta, sino porque en uvicorn 0.52.1 esa bandera **ya viene puesta por defecto** — dato que `[D-034]` tenía escrito desde el 2026-08-06 y que se olvidó al diseñar el control. 🔑 **El sabotaje no saboteaba nada**, así que su verde no era información: era silencio, exactamente `[L-020]`. El rojo de verdad exigió romper la bandera que sí manda — `--forwarded-allow-ips 203.0.113.5`— y entonces el log escribió `127.0.0.1`, con `[A-014]` a la vista. ⚠️ **La novedad respecto a `[L-020]`:** allí el instrumento ciego era el que medía; aquí era **el que autorizaba a creerse la medida**, que es peor — un control ciego no da un falso negativo, da permiso. 🔧 Regla: **el control se diseña contra el valor por defecto, no contra la bandera escrita.** Quitar una opción no la apaga si la librería ya la trae puesta; hay que ponerle un valor **activamente equivocado**. 📌 Cuarta vez del mismo bicho en tres sesiones (`[L-019]`, `[L-020]`, `[L-021]`, esta) | medir la mitad de Caddy de `T-055` en contenedor |
| L-026 | 2026-08-07 | 🚨 **`T-068` es el único control del proyecto ESTRUCTURALMENTE inverificable, y por eso no es un freno: es disciplina.** `LM.13` pide haber visto morder el control; este **no se puede ver morder nunca**, porque **probarlo ES el desastre** — cruzar una de las siete puertas evapora los créditos sin vuelta atrás. 🔑 La diferencia que importa: **un freno no se degrada con la repetición; la disciplina sí.** Y el desgaste ya tiene fecha de inicio — `[A-018]` obliga a abrir *Facturación y costos* **a diario** durante semanas, y es la misma página donde vive *"Actualizar plan"*. **Lo que se hace:** no llamarlo freno, y **sacar de la lista el riesgo con tráfico** — *"Actualizar plan"* pasa a ser una línea del **protocolo de lectura**, no el renglón 8 de `[C-005]`. Un control inverificable etiquetado como "freno" da la misma calma que uno probado y no la merece: `[LM.13]` con otro traje |
| L-025 | 2026-08-07 | 🚨 **Cambiar un dato no termina cuando se cambia el dato: termina cuando se ha hecho `grep` de sus copias.** El defecto que más veces ha vuelto — siete contando las de hoy. Solo el 2026-08-07: `app/config.py` y `app/api.py:40-42` con **la misma frase** describiendo una plataforma descartada en `[D-029]` hace dos días; y retirar `[A-019]` dejó **cinco punteros a un ancla que ya no existe** (`test_deploy_limits.py:103,108`, `decisions.md:271`, `Caddyfile.template`, `tasks.md:65`, `progress.md:149,151`). 🔑 Lo grave son las dos primeras: **un comentario pegado a la línea que ejecuta se lee como la explicación autorizada de esa línea**, y nadie duda de él porque está al lado — ese justificaba `os.environ.setdefault` con un motivo muerto, y la regla resultó correcta **por otra razón** (`[D-039]`). ⚠️ Y **el arreglo genera el bicho**: limpiar `assumptions.md` es lo correcto y ensucia en otro sitio — `[L-023]` con el signo cambiado, la corrección ensuciando lo que corrige. 🔧 Tras cambiar un hecho: `grep` del ancla y de las palabras de la frase por `_persistence/`, `_context/`, `deploy/`, `app/` y `tests/`; lo que sea de otro dueño se deja escrito **por número de línea** | retirar `[A-019]` y corregir la precedencia del `.env` |
| L-024 | 2026-08-07 | 🚨 **"Necesita la nube" era falso, y se dio por cierto sin recorrer la lista.** `deploy/install.sh` —escrito el 2026-08-05, **nunca corrido**, solo `bash -n`— corre entero en un contenedor Ubuntu 24.04: `apt-get`, Caddy 2.11.4, `venv`, `pip` y el `.env`, y muere en `systemctl: command not found` (línea 223), **después** de la parte que importaba. Con eso se midió `[A-008]` (hoy `[L-032]`) sin EC2 y se probó `[D-038]`. 🔑 El fallo de origen fue de **censo**, no técnico: "no hay nada sin nube" es una afirmación sobre un conjunto que nadie recorrió, con un número inventado encima ("once pendientes" cuando el `grep` propio devolvía **catorce**) — `[L-021]` otra vez. 🔧 Montaje: `git ls-files` y no copiar la carpeta (el `.venv` y `node_modules` de **Windows** habrían hecho al guion saltarse el paso de Python y medir otra cosa), y `MSYS_NO_PATHCONV=1` o Git Bash convierte `/opt/teapp` en ruta de Windows. 📌 Se descartó un test que leía el **texto** del guion: ruidoso al renombrar, ciego al cambiar `-f` por `-e` — mide la forma, no el comportamiento. **Regla: antes de escribir "bloqueada", preguntarse qué mitad no lo está**. 🔻 **Ampliada el 2026-08-07**: aplicada la regla a lo que la propia lección dejaba fuera, **la sección 5 no se había ejecutado nunca** — dentro vivía `caddy validate` (línea 237). Corrida a mano: ✅ `Valid configuration`, salida 0, sin marcadores sin sustituir, con `request_body max_size 16KB` y `reverse_proxy 127.0.0.1:8000`. ⚠️ Mide **sintaxis, no comportamiento**. 📌 Y cayó una suposición sobre el propio contenedor: **NO hay aparejo Caddy↔uvicorn** ahí dentro, su `Caddyfile` es **el de fábrica** con `reverse_proxy` comentado — casi se le pide una medición que no podía dar, **y habría contestado algo**. 🔑 La **receta** (`docker run … ubuntu:24.04 sleep infinity`, todo por `docker exec … sh -c`) vivía solo en un scrollback: ya está en `deploy/README.md`. El contenedor es desechable; la receta no | intentar `T-050` sin máquina, tras una revisión externa |
| L-023 | 2026-08-06 | 🚨 **Lo que ensució los datos reales fue el instrumento de medida.** `T-072` cerrada: el camino de `[A-020]` era `measure_body.py`, la báscula de `T-054`, escrita y ejecutada seis horas antes (19:48:32 UTC = 14:48:32 local, un segundo antes de que nacieran los archivos). Se registró como `otronombrelargo` y practicó 5 veces —los 5 casos de `CASES`—, de ahí `{"score": 5}` y `{"used": 5}`. 🔑 **El mecanismo es de manual: el aislamiento necesitaba TRES desvíos y la báscula se acordó de UNO.** Desvió `accounts.ACCOUNTS_FILE` a un temporal —con su comentario *"medir no debe tocar `data/`"`*— y dejó `USERS_DIR` y `QUOTA_DIR` apuntando a los datos de verdad. Y eso explica la contradicción que abrió `[A-020]`: la cuenta no estaba en `data/accounts.json` **porque `accounts.json` fue justo el único que sí se desvió**; la cuenta se creó en el temporal, el marcador y la cuota en los datos reales. 📌 **No es un accidente, es un patrón:** `probe-log.json`, el otro huérfano de `data/users/`, sale del 2026-08-05, otra sesión y otro día. ⚠️ **Y el portero de `T-071` no lo verá nunca**, porque vive dentro de pytest y una báscula corre fuera. Encadena con `[L-020]` (un instrumento ciego da silencio) y `[L-022]` (un `md5` dice "los bytes, iguales"): **el instrumento que mide puede ensuciar lo que mide** | resolver `T-072` — el rastro estaba en las transcripciones, no en el historial de PowerShell |
| L-022 | 2026-08-06 | 🚨 **Un `md5` no dice "todo igual": dice "los bytes, iguales".** Restaurando `data/` tras el sabotaje de `T-071` (`rm -rf data && cp -r copia data`) se verificó con huella de contenido — siete archivos, siete huellas idénticas, restauración correcta. Y era cierto: **ningún dato de la aplicación se perdió.** Lo que se destruyó fue el **`mtime`**, y con él la prueba física del camino de las 14:48 de `[A-020]` — incluida la más fuerte, que el marcador y la cuota llevaban el mismo nanosegundo. 🔑 **Vuelta nueva sobre `[L-020]`/`[L-021]`:** los casos anteriores eran instrumentos **ciegos a un cambio**; este vio perfectamente el cambio que le importaba y fue ciego a **una dimensión entera del archivo**. Un archivo es contenido **y** metadatos, y `md5` solo mira la mitad. ⚠️ **Y estrenó `[L-021]` el mismo día en que se escribió, dentro de la verificación del portero construido contra ese defecto.** 📌 Regla que queda: **la prueba de un defecto no puede vivir en la carpeta que el defecto ensucia** — se copia a `_persistence/`, que sí va a Git, ANTES de tocar nada. Y antes de restaurar por copia, preguntarse qué del original no viaja en los bytes | restaurar `data/` tras sabotear el portero de `T-071` |
| L-021 | 2026-08-06 | 🚨 **El titular que contradice su propia salvedad — `[L-020]` por el lado acusatorio.** Un análisis tituló *"la trampa ya se disparó"* y tres líneas después escribió *"te lo doy como sospecha fuerte, no como hecho medido"*. Las dos frases no pueden ser ciertas a la vez, y **la que se recuerda es el titular**. La medida (md5 + fecha de los 5 marcadores, suite entera, huella idéntica) dijo lo contrario: la suite de hoy **no** escribe en `data/`. 🔑 `[L-020]` decía que el silencio no confirma que todo esté bien; esto es la otra mitad: **el silencio tampoco confirma que algo esté mal**. Ausencia de historial no es evidencia en ninguna de las dos direcciones. ⚠️ **Y una salvedad correcta no arregla un titular falso** — si la salvedad y el titular discrepan, el que hay que cambiar es el titular | la auditoría de `T-071` |
| L-020 | 2026-08-06 | 🚨 **El modo de fallo característico de este proyecto, ya con nombre: un verde producido por algo distinto de lo que el verde afirma.** El caso: se dijo *"verifiqué con `git status` que `data/` quedó intacto"* — y **`data/` está en `.gitignore` (línea 18)**. `git status` habría callado igual si los tests hubieran escrito ahí. La conclusión era correcta, pero **se supo por suerte, no por la prueba citada**; el testigo que se invocó no estaba mirando. 🔑 **Antes de citar una prueba, preguntar si el instrumento PUEDE ver el fallo que se descarta** — un instrumento ciego no da un falso negativo, da silencio, y el silencio se lee como verde. Se comprobó por el camino que sí ve: las fechas de `data/users/*.json`. Tercera vez en dos sesiones (`[L-019]`, el test contra 16384 de `[D-035]`, y esta): ya no es casualidad | la auditoría de `T-054` |
| L-019 | 2026-08-06 | **El sabotaje que llegaba disfrazado de aquello que quería atacar.** Para probar que uvicorn ignora `X-Forwarded-For` de un desconocido se le habló por `127.0.0.2`, dando por hecho que sería una dirección no confiable. Windows pone **`127.0.0.1` como origen** aunque el destino sea `127.0.0.2`: la petición entraba **como si fuera Caddy**, y el escenario medía justo lo contrario de lo que decía medir. 🔑 **De un test se verifica el montaje, no solo el resultado** — aquí salió rojo y el rojo era mío; si llega a salir verde por la misma razón, se habría cerrado `T-055` sobre nada | medir `[A-014]` con uvicorn real, T-055 |
| L-018 | 2026-08-06 | **En este proyecto los datos se replican solos, y corregir uno no corrige los demás.** Una frase falsa sobre la alarma de facturación vivía en **cinco** sitios (entrada, fila de índice y "Estado actual" de `progress.md`; dos puntos de `A-018`; y un párrafo de `console_steps.md`). 🚨 **Tercera vez con el mismo bicho:** sesión 33 (el repo "privado"), sesión 41 (lo mismo otra vez), y ahora. Ya no es casualidad: el formato de este repo —índice + entrada, más `deploy/` explicando lo mismo en operativo— **obliga a duplicar por diseño**. 🔑 **Corregir es ir a BUSCAR las copias, no editar donde se encontró el error** | la segunda auditoría de `A-018` |
| L-017 | 2026-08-05 | **Un control que comprueba MENOS de lo que su propio comentario promete.** El bloque final de `install.sh` se titulaba *"PI-4: terminado = visto funcionando"* y dos líneas después solo miraba `systemctl is-active` — que demuestra que systemd **lanzó** el proceso, no que la app conteste. Con `Restart=always`, una app que revienta al arrancar se ve `active` y el guion imprimía **"Listo"** sobre algo muerto. 🔑 **El comentario correcto hizo de coartada: nadie audita un bloque que ya se declara auditado.** ⚠️ Y el arreglo trajo la misma criatura con el signo cambiado: reintentos para lo que tarda segundos y ninguno para lo que tarda minutos — **un falso verde y un falso rojo son el mismo error** | revisión de `deploy/`, T-063 |
| L-016 | 2026-08-05 | **Dos veces el mismo error, un piso más abajo cada vez — y las dos veces el hecho salió de la FORMA del texto, no del texto.** Primero: *una lista que tiene sentido parece completa* (3 puertas de AWS se dieron por las 7). Y al corregirla, otra vez: *un documento que no dice "no" parece que dice "sí"* — de cinco de las siete puertas la doc **calla**, y ese silencio se leyó como respuesta favorable. 🔑 **El silencio de una fuente no es un dato** | cerrar `[A-016]`, T-068 |
| L-015 | 2026-08-04 | **El fixture que creía limpiar y no limpiaba.** Para medir el log sin trampas se vaciaron los handlers del raíz en un fixture — y `caplog` los repone **después** de los fixtures. El test volvía a medir el estado de pytest y lo llamaba "lo que hace la función": [L-012] otra vez, y esta vez dentro del arreglo de [L-012] | escribir `test_log_config.py`, T-033 |
| L-014 | 2026-08-04 | **Una suposición que dice qué la mata se muere sola cuando toca.** `[A-012]` llevaba escrita su propia condición de cierre; el día que se cumplió, retirarla no fue un juicio sino una comprobación. Y al retirarla se vio que no era una, sino dos: se partió en `[A-013]` y `[A-014]` | retirar `A-012` al cerrar T-053 |
| L-013 | 2026-08-04 | **Cerrar un hueco no cierra los demás**, y los que quedan no se parecen al que cerraste — por eso no se ven. El candado tapó el hueco entre leer y escribir; quedaron abiertos otros cuatro, y los cuatro cobraban o regalaban de más | los sabotajes a los frenos del paso 6 |
| L-012 | 2026-08-04 | El límite estaba **escrito** —`[A-003]` decía que un `logger.info` se pierde— y aun así se cruzó. El test lo tapó bajando el listón: `caplog.at_level(INFO)` pinta de verde un renglón que en el servidor no existe | escribir el motivo del frenazo de la cuota, T-038 |
| L-011 | 2026-08-04 | El portero de red tenía una puerta de atrás abierta —`connect_ex` devuelve un código en vez de lanzar— y su propio control no la veía: el control usaba un nombre, y lo mataba otro parche | escribir el portero de red, T-047 |
| L-010 | 2026-08-04 | 191 tests en verde y el servidor de verdad reventaba: `TestClient` no es uvicorn, y comprobar el efecto no es comprobar la respuesta | correr el paso 5 a mano, `/logout` |
| L-009 | 2026-08-04 | Una regla que vive en dos archivos se corrige en los dos: `protocol-close` prometía algo que `protocol-start` no leía | arreglar T-049, el desfase del cierre |
| L-008 | 2026-08-03 | Se comparó la opción rival en su versión floja y se le ganó a esa: eso no es comparar, es elegir y buscar razones después | revisar dónde vive el control del `.js`, T-037 |
| L-007 | 2026-08-03 | La comprobación que mide **de más**: `diff -r` gritaba "viejo" con el repo correcto. Un control se mide dos veces —con el fallo puesto y sin él— o no se midió | escribir el control del `.js` compilado, T-037 |
| L-006 | 2026-08-03 | El cierre se cumplió entero y el trabajo se quedó sin subir: si el hash no está en `origin`, no hubo cierre | la revisión cruzada del paso 4 |
| L-005 | 2026-08-03 | Buscar una palabra en un archivo entero no es comprobar el código: los comentarios también cuentan | el primer test de la pantalla, paso 3 |
| L-004 | 2026-08-02 | Una prueba que el código roto también pasa no prueba nada | validar el arreglo de concurrencia del paso 2 |
| L-003 | 2026-08-02 | 45 tests en verde no vieron un fallo que rompía 7 de cada 10 peticiones | la revisión externa del paso 2 |
| L-002 | 2026-08-02 | `pip install` sin versión fijada no da la misma versión dos veces | crear el `.venv` del paso 1 |
| L-001 | 2026-08-02 | La consola de Windows no pinta caracteres fuera de ASCII | correr `main.py` por primera vez |

---

## Entradas

### [L-067] 2026-08-15 — El cierre se creyó al archivo que él mismo tenía que escribir

- **Qué pasó.** `session-closer` hizo bien la parte de evidencia: verificó los
  cinco commits contra `git`, encontró el árbol limpio y sincronizado, y
  comprobó que no había `.ts` en el diff. Y concluyó: *"`_persistence/` ya
  estaba al día antes de que yo entrara — no hubo nada que actualizar"*, citando
  `[S-059]` como *"el índice con el detalle de hoy"*.

  **`[S-059]` es del 2026-08-14.** La sesión del 15 —cinco commits, el cierre
  del paso 8, cinco lecciones nuevas— **no tenía fila en el índice**. Y el
  índice es lo que se lee al arrancar.
- 🔑 **Por qué se equivocó, y no fue por pereza.** La casilla `Estado actual`
  **sí** decía *"PASO 8 CERRADO el 2026-08-15 (`[D-081]`)"* — la había escrito
  la sesión principal durante el día. El cierre leyó **una parte correcta del
  archivo y generalizó al archivo entero**.

  > ⚠️ **Un archivo medio actualizado es peor que uno sin tocar: el trozo bueno
  > avala al malo.** Sin la casilla escrita, el cierre habría visto un
  > `progress.md` que no mencionaba el día y habría actuado.
- ⚠️ **Y el árbol limpio remató el engaño.** `nothing to commit` es la señal de
  *"no queda trabajo"*. Aquí significaba otra cosa: *"el trabajo se commiteó
  **antes** de que llegara el cierre"*. Es `[L-029]` desde el otro lado — allí
  lo huérfano era lo que nacía después del cierre; aquí es lo que nació antes y
  **dejó al cierre sin señales que recorrer**.
- 🧭 **Regla:** el cierre no pregunta *"¿está el archivo al día?"* sino **"¿tiene
  ESTA sesión su propia fila en el índice, con un id nuevo?"**. Es una
  comprobación de una línea y ninguna lectura de la cabecera la sustituye:

  ```
  grep "^| S-0" _persistence/progress.md | head -1
  ```

  Si la fecha de esa fila no es la de hoy, **falta la entrada del día**, diga lo
  que diga la casilla de estado.
- 📌 **Cuarta vuelta del mismo bicho en un solo día, y la más incómoda porque
  cae dentro del protocolo que existe para evitarlo:**

  | | qué se creyó sin comprobar |
  |---|---|
  | `[L-062]` | el archivo de estado, sellado antes del último commit |
  | `[L-063]` | la prosa nueva, escrita sin citar el código |
  | `[L-066]` | la entrada vieja, que no sabía que la superaron |
  | `[L-067]` | **el cierre, que se creyó al archivo que él debía escribir** |

### [L-066] 2026-08-15 — El índice se lee por fecha, pero se busca por asunto

- **Qué pasó.** Se arregló el guion de arranque (`T-098`) para que leyera el
  campo de estado y se saltara lo tachado, y **se corrió para comprobarlo**, no
  se dio por bueno leyéndolo. Las dos correcciones funcionaron. **Y la corrida
  destapó dos fallos más**, que resultaron ser el mismo:

  | lo que reportó | lo que era |
  |---|---|
  | *"timeout del cliente (8,0 s)"*, `read 4,0` — **dos veces** | `9,0` y `read 6,5` desde `[D-072]` (`app/tools.py:245`) |
  | *"`[D-080]`, decisión crítica abierta"* | cumplida entera por `[D-081]` |

- 🔑 **Causa única: `decisions.md` no tenía convención de tachado.**
  `assumptions.md` la tenía desde hacía semanas —`~~A-024~~`, *"RETIRADA;
  vive ahora en `[D-057]`"*— y **nadie la extendió al archivo de al lado**. El
  defecto llevaba ahí desde entonces, esperando a que alguien buscara por tema.
- ⚠️ **Por qué costaba verlo, y esto es lo transferible.**

  > **El índice se LEE por fecha, de arriba abajo. Pero se BUSCA por asunto.**

  `[D-072]` decía **en su propia fila** que corregía a `[D-071]`. Impecable para
  quien recorre el índice en orden. **Inútil para quien hace `grep "presupuesto
  del cliente"`**, aterriza en la fila de `[D-071]` y encuentra unos números que
  no dicen nada de estar superados. **Una corrección solo protege si está en el
  sitio al que se LLEGA, no en el sitio desde el que se corrigió.**
- 🧭 **Regla:** al escribir una decisión que reemplaza a otra, **tachar la vieja
  va en el mismo cambio**, con cuál de las dos marcas corresponde:
  - 🔻 **SUPERADA** — otra la reemplazó, y **sus números ya no son los del
    código**. No se cita ni una cifra de ella.
  - ✅ **CUMPLIDA** — no estaba equivocada; su mandato se ejecutó y se acabó.
    No es una decisión abierta.

  Ni borrarla (pierde el porqué) ni corregirla en el sitio (la deja pareciendo
  que siempre dijo eso).
- 📌 **Tercera vuelta del mismo bicho, y las tres el mismo día:**

  | | qué se pudrió |
  |---|---|
  | `[L-062]` | el archivo de **estado**, por detrás de las entradas |
  | `[L-063]` | la **prosa nueva**, escrita sin citar el código |
  | `[L-066]` | la **entrada vieja**, que no sabe que la superaron |

  **Las tres son la misma forma: una afirmación que fue cierta y a la que nadie
  fue a apagar.** Y las tres se cobran en el mismo sitio — el arranque de la
  sesión siguiente.
- 🧪 **Y el hallazgo existe solo porque el arreglo se CORRIÓ.** Releer el guion
  arreglado no habría enseñado nada: estaba bien. Ejecutarlo devolvió dos fallos
  nuevos dentro del mismo reporte. Es `[PI-4]` cobrando: *lo que no se ha
  corrido no está terminado, aunque el código exista*.

### [L-065] 2026-08-15 — Un aviso presente baja la guardia sobre el hueco de al lado

- **Dos de dos, con dos semanas de diferencia y el mismo defecto exacto:**

  | archivo | el aviso, correcto | lo que lo negaba | distancia |
  |---|---|---|---|
  | `deploy/install.sh` (`T-089`) | *"NUNCA la llave como argumento"*, en mayúsculas | un ejemplo con la llave delante de `sudo` | **3 líneas** |
  | `deploy/check_api_key.py` (`T-088`) | *"si cambian el límite en la consola, cámbialo aquí"* | *"da igual cuál sea el modelo"* | **12 líneas** |

  Los dos avisos eran **correctos**. Ninguno mentía. Cada uno cubría **una**
  puerta, y a pocas líneas había una segunda que el aviso no cubría — y que en
  el segundo caso la línea vecina negaba explícitamente.

- 🔑 **El mecanismo es psicológico, no técnico, y por eso no lo caza un test.**
  Un aviso presente **se lee como cobertura**. Quien ve un párrafo en mayúsculas
  sobre el peligro X concluye que el peligro está atendido y deja de buscar.

  > ⚠️ **El hueco de al lado queda MÁS protegido de la revisión que si no
  > hubiera ningún aviso.** Un archivo sin advertencias se audita entero; uno
  > con una advertencia grande se audita hasta la advertencia.

  Es `[L-061]` un nivel más arriba — allí era *"un precedente que no transfiere
  es peor que no tener ninguno: parece verificado"*, aplicado a una cita. Aquí
  se aplica al archivo entero.
- 🧭 **Regla, y gobierna el paso 9:** donde un archivo se molesta en avisar de
  una puerta, **preguntar cuál es la segunda**. La pregunta útil no es *"¿es
  correcto este aviso?"* —los dos lo eran— sino **"¿de cuántas formas se rompe
  esto, y de cuántas avisa?"**. En `check_api_key.py` la firma se rompe por dos
  sitios (cambiar el límite en la consola, cambiar `MODEL`) y el archivo cubría
  uno; el arreglo fue escribir el par y **apuntar desde los dos extremos**.
- 🚨 **En los dos casos el fallo era MUDO**, que es lo que los hace caros:
  `sudo VAR=...` no da error, sale en `ps aux`; y `requests_limit == 50` con
  otro modelo no da error, devuelve `EXIT_OK`. Un fallo ruidoso con un aviso al
  lado se descubre solo. Uno mudo con un aviso al lado no se descubre nunca.
- 📌 **Qué le hace esto a `[D-080]`.** Aquella decisión eligió no cerrar el paso
  8 con **un** dato, y escribió honradamente su propio límite: *"el argumento no
  es que queden cuatro tareas; es que la clasificación de esas cuatro no era de
  fiar, y ya hay una prueba"*. El segundo dato llegó **con la misma forma**, y
  eso es lo que descarta la casualidad: deja de ser un recuento y pasa a ser una
  regla. Ver `[D-081]`.

### [L-064] 2026-08-15 — Aplazada espera; armada tiene disparador

- **De dónde sale.** `[D-080]` decidió no cerrar el paso 8 hasta mirar las
  cuatro pendientes **una por una**, y el argumento era bueno: `T-089` estaba
  escrita como cosmética y al medirla subió a clase de seguridad. Pero la
  decisión **no dejó escrito qué se busca al mirarlas**. Esto es esa regla.

  > ⏳ **Una tarea APLAZADA espera.** 💣 **Una tarea ARMADA tiene disparador.**
  > Aplazar la primera es gestión. Aplazar la segunda es **dejar el disparador
  > sin dueño**.

- **Las dos que quedaban, con la regla aplicada:**

  | | `T-081` | `T-088` |
  |---|---|---|
  | ¿qué la activa? | nada | **cambiar `MODEL`** |
  | ¿está eso planeado? | no | **sí — `[D-049]` lo mete en el paso 9, y DOS veces** |
  | ¿su ficha engaña? | no — el daño está escrito en ella | **sí — decía "cuando toque el paso 9"** |
  | veredicto | aplazada, aguanta | **armada: se hace ya** |

- 🔑 **Lo que hizo saltar `T-088` no fue su gravedad, fue su calendario.** Su
  ficha decía *"corregir cuando toque el paso 9"*. Y `[D-049]` mete en el paso 9
  **el descenso a Sonnet 5 y a Haiku 4.5**: o sea, cambiar `MODEL` —dos veces—,
  que es exactamente la acción que arma la trampa.
  **No estaba aplazada AL paso 9; estaba armada PARA el paso 9.** Un
  comentario que afirmaba *"da igual cuál sea el modelo"*, puesto delante de la
  única persona que iba a cambiar el modelo, el día en que lo cambiara.
- 🔴 **Corregido el 2026-08-15, y la corrección REFUERZA la regla.** Esta
  entrada decía *"el paso 9 **es** bajar a Haiku"*, escrito sin abrir el
  roadmap, que lo titula **"Observabilidad y evals con rúbrica"**
  (`_context/roadmap.md:23`) — o sea `[L-063]` cometida mientras se escribía
  esta misma lección. 🔑 **Y el error no era solo de nombre, era de forma:**
  atar el disparador a *"lo primero del paso 9"* lo deja **gastado después del
  primer cambio de modelo, justo antes del segundo** — y `[D-049]` mete dos,
  Sonnet 5 y Haiku 4.5.

  > 🔑 **El disparador es la ACCIÓN, no la fecha.** Uno con fecha se dispara una
  > vez. Uno con acción se dispara cada vez que la acción ocurre.
- 🧭 **Regla operativa: al revisar una pendiente, la pregunta no es "¿cuánto
  corre prisa?" sino "¿qué la dispara?".** Si el disparador es una acción que
  ya está en el plan, la tarea deja de ser pendiente y pasa a ser **bloqueante
  de esa acción**. Dos salidas honestas y ninguna más: hacerla ahora, o
  reescribirla colgada del disparador con dueño. **Suelta en una lista no
  vale** — es justo lo que le pasó a `T-089` durante semanas.
- ⚠️ **Por qué una lista de pendientes es el sitio donde esto se esconde.** Las
  iguala a todas por su aspecto: tres renglones parecidos, tres `🔲`. Y lo que
  las separa **no se ve en el renglón** — si hay algo en el calendario que las
  active. El formato mismo borra la distinción que importa.
- 📌 **La aritmética del caso, que es el argumento entero.** Desarmar `T-088`
  costó **dos comentarios y cero lógica**. El precio de aplazarla habría sido un
  portero mudo aceptando la llave del laboratorio en producción, sin dar error
  — porque `requests_limit == 50` sale falso con cualquier otro modelo y la
  función devuelve `EXIT_OK`. **Denegar por defecto (regla 3) convertido en
  aceptar por accidente.**

### [L-063] 2026-08-15 — La cita al lado de la frase es lo que obliga a mirar

- **Qué pasó.** En un mismo arranque salieron **cuatro** citas torcidas sobre
  los mismos números. Las tres primeras eran prosa vieja heredada: el reparto
  del cliente citado como `connect 2,0 / write 1,0 / read 4,0 / pool 1,0`,
  cuando `app/tools.py:245` dice `1,5 / 0,5 / 6,5 / 0,5`.
- 🔑 **La cuarta es la que enseña, porque no encaja en el diagnóstico de las
  otras tres.** Se escribió **ese mismo día**, y decía:

  > *"Son cuatro relojes en paralelo, cada uno con su techo, y la suma ya cabe
  > en los 9,0 por construcción."*

  Las dos mitades son falsas, y el código llevaba el aviso puesto desde antes:

  | dónde | qué dice |
  |---|---|
  | `app/tools.py:107` | el 9,0 es **el presupuesto total, la suma** de las cuatro fases → secuenciales, no paralelas |
  | `app/tools.py:235` | `read` **tampoco** es techo duro: `_receive_response_body` usa el mismo `read` |
  | `app/tools.py:239` | *"los 10 s de `api.py` NO sobran: son la única garantía de reloj de pared que existe"* |
  | `app/api.py:730` | `attempt.result(timeout=TUTOR_TIMEOUT_SECONDS)` — el único corte real |

  Si fueran paralelas el techo sería `max(6,5)`, no la suma `9,0`: **la propia
  aritmética que se estaba escribiendo desmentía la frase.** Y *"por
  construcción"* es justo lo que no es — el `9,0` es una constante nuestra,
  sumada a mano para poder compararla con el `10,0`; el SDK no la impone.
- 🧭 **La regla sale de comparar dos párrafos del mismo mensaje.** Uno citó
  `tools.py:245` pegado a la afirmación y **salió correcto**. El otro razonó
  sobre las mismas fases **sin citar nada** y salió falso en sus dos mitades.
  Misma sesión, mismo archivo abierto, mismo minuto.

  > 🔑 **Citar fichero y línea al lado de la frase no es cortesía para quien
  > lee: es el acto que obliga a mirar antes de afirmar.** Sin la cita se está
  > recordando; con la cita se está leyendo. Y recordar se parece mucho a saber.
- 🚨 **La dirección del error era la peligrosa.** Presentar el `9,0` como "el
  techo real" y el `10,0` como "el hueco" invita a concluir que el `10,0`
  sobra. El día que alguien lo retire se lleva por delante lo único que
  garantiza que una práctica termine. El código ya había previsto ese día y
  dejó el aviso escrito; el resumen lo borró.
- 📌 **Eco que no se calla.** Los dos cierres anteriores de `[A-011]` murieron
  por colgarse de un techo inexistente (`[D-070]`, `[L-054]`). El argumento de
  hoy **no** falla, pero **la frase con que se contó es de esa misma familia**.
  Tercera vez que este cierre se apoya en un techo, y las dos anteriores el
  techo no estaba. Cuando una forma de equivocarse reaparece por tercera vez,
  la señal no es el veredicto: es la forma.
- ⚖️ **Lo que esta lección NO dice.** No dice que la conclusión fuera errónea.
  `[A-030]` sigue sin morder, pero por el camino que **no** invoca paralelismo:
  `connect = 1,5` tiene presupuesto propio y no se come el `read`, y por encima
  está el `10,0` de reloj de pared, que corta sea cual sea el número de fases.
  **Llegar al sitio correcto por un camino falso sigue siendo un fallo**, porque
  el camino es lo que se hereda.

### [L-062] 2026-08-15 — El commit tardío tuvo dueño; el archivo de estado, no

- **Qué pasó.** El resumen de apertura del 2026-08-15 anunció como pendiente
  *"T-090 sin anotar: la decisión nunca llegó a `decisions.md`"*. Era falso.
  `[D-080]` existía entera y commiteada desde el día anterior.
- **Dónde nació la mentira, que es lo único que hay que guardar:**

  | commit | qué tocó | qué dejó dicho |
  |---|---|---|
  | `8b9b37f` | `progress.md` (sello del día) | *"esa decisión no está anotada"* |
  | `6c7b5a7` | **solo** `decisions.md` | `[D-080]`, la decisión anotada |

  El segundo desmintió al primero **y no lo tocó**. El archivo de estado quedó
  congelado con la frase vieja, y el arranque del día siguiente la heredó.
- 🔑 **La distancia con `[L-029]`, que es la vuelta nueva.** Aquella decía *"lo
  que nace después del cierre no tiene dueño"* y lo curó con una regla que aquí
  **se cumplió**: `[D-080]` se escribió y se commiteó en el momento. Lo huérfano
  no fue el trabajo: fue **la actualización del estado**. Las entradas apuntan
  hacia adelante; nada obliga a una entrada nueva a volver atrás y corregir el
  resumen que la contradice.
- 🚨 **La dirección del error es lo que lo hace caro.** Un estado que dice *"ya
  está hecho"* cuando falta se descubre solo: alguien va a hacerlo y no lo
  encuentra. Este dijo **"falta"** sobre algo terminado, y ese fallo **no se
  descubre — se paga repitiéndolo**. El primer cuarto de hora de la sesión se
  fue en dictar una decisión que llevaba un día escrita. Es exactamente el
  gasto que `_persistence/` existe para ahorrar, cobrado por `_persistence/`.
- ⚠️ **Y es mudo, como `[L-029]`.** Árbol limpio, 440 tests en verde, ningún
  archivo a medias, ningún puntero roto. Nada delata que la casilla de estado
  esté citando una frase que el commit siguiente ya había desmentido. La única
  forma de verlo fue comparar `git log -- progress.md` con `git log` a secas.
- 🔧 **Regla:** un commit posterior al sello del día que toque `_persistence/`
  **corrige en el mismo commit la casilla de `progress.md` que deja desmentida.**
  Un cierre no termina en el hash: termina cuando el estado y las entradas
  dicen lo mismo.
- 📌 **Aviso al arranque.** Cuando `progress.md` diga que algo falta, mirar si
  hay commits posteriores a su último sello antes de creerlo. Un archivo de
  estado es un caché, y los cachés se invalidan.

### [L-061] 2026-08-14 — `sudo VAR=valor` no es entorno: es un argumento, y los argumentos los ve toda la máquina

- **Qué pasó.** Una auditoría externa señaló que el mensaje de error de
  `install.sh` (línea 104) recomendaba pasar la llave así:

  ```bash
  sudo TEAPP_DOMAIN=... ANTHROPIC_API_KEY=... bash deploy/install.sh
  ```

  Al leer el archivo entero apareció algo peor que lo señalado: en la cabecera,
  el bloque `Uso:` traía el mismo patrón **con la llave completa**, y tres
  líneas más abajo un aviso en mayúsculas que decía *"La llave va por variable
  de entorno, NUNCA como argumento"*. **El aviso y su violación, en la misma
  pantalla.**

- **Por qué la confusión es fácil y no es tonta.** Pasar un secreto por
  variable de entorno **es** la forma correcta, y está bien usada en otro sitio
  del proyecto: `create_account.py` toma la contraseña por entorno y tiene un
  test que rechaza pasarla como argumento (`[D-063]`). El entorno de un proceso
  vive en `/proc/PID/environ`, que **solo puede leer su dueño**.

  🔑 **Pero `VAR=valor` delante de `sudo` ya no es entorno.** Es un argumento
  **de `sudo`**, que lo recibe en su propia línea de comandos y luego se lo
  monta al hijo. Y las líneas de comandos (`/proc/PID/cmdline`) las lee
  cualquier usuario de la máquina.

- **🧪 Medido, no razonado.** Esto se estuvo a punto de cerrar por inferencia
  ("así trata `sudo` los `VAR=val`"). Costó doce segundos comprobarlo en la EC2
  ya encendida, el 2026-08-14 a las 18:54 UTC:

  ```bash
  sudo FOO=secreto123 sleep 30 &
  sleep 1
  ps aux | grep secreto123 | grep -v grep
  ```

  ```
  root  1599  ... sudo FOO=secreto123 sleep 30
  root  1601  ... sudo FOO=secreto123 sleep 30
  ```

  📌 **La columna del dueño es lo que cierra el argumento:** los procesos son de
  `root` y el `ps aux` se lanzó desde la cuenta `ubuntu`. No es "el dueño ve lo
  suyo": es una cuenta sin privilegios leyendo la línea de comandos de `root`.

- **Lo que NO pasó.** El despliegue real del 2026-08-13 había usado la forma
  segura (`stdin` → `read -r` → `export` → `sudo -E`). Comprobado en la máquina
  con `grep -c "sk-ant"` sobre `~/.bash_history` y `/root/.bash_history`:
  **0 y 0**. La llave nunca tocó una línea de comandos. **No hubo que rotar
  nada.** El fallo era el consejo, no el despliegue.

- **🧭 La regla que queda.** Un precedente correcto en su archivo puede ser
  **engañoso en otro**: mismo patrón, una palabra de diferencia, y se parece
  tanto que invita a copiarlo. **Un precedente que no transfiere es peor que no
  tener ninguno, porque parece verificado.** Cuando un aviso y un ejemplo se
  contradicen en el mismo archivo, el ejemplo es el que la gente copia.

- **⚖️ Severidad, sin inflarla.** `ps` exige estar ya dentro de la máquina. No
  es una fuga remota: es un **amplificador** de un acceso ya conseguido.

- **✅ Arreglo.** `install.sh` recomienda ahora `read -r -s` → `export` →
  `sudo -E`. El `-E` **hereda** el entorno en lugar de recibirlo como argumento;
  el `-s` evita que la llave quede en el historial y en el scrollback.

- **🧪 Y el arreglo también se midió, porque casi no se hace.** El primer
  intento de verificarlo fue `bash -n deploy/install.sh` → OK. **Ese verde no
  decía nada:** los dos cambios eran un bloque de comentarios y una cadena
  dentro de un `echo`, así que el archivo iba a parsear pasara lo que pasara.
  🔑 **Un instrumento que pasa pero es ortogonal al cambio no es evidencia
  sobre el cambio** — misma forma que la barra redondeada de `[L-060]`, el
  mismo día. Lo que de verdad estaba en duda era si `sudo -E` entrega la
  variable: Ubuntu trae `Defaults env_reset` en `/etc/sudoers` y ni
  `ANTHROPIC_API_KEY` ni `TEAPP_DOMAIN` están en el `env_keep`, así que el `-E`
  podía fallar en voz alta o entregar vacío. Medido en la EC2 el 2026-08-14:

  ```bash
  export TEAPP_TEST=hola
  sudo -E bash -c 'echo "llego: ${TEAPP_TEST:-VACIO}"'   # → llego: hola
  ```

  Sobrevive al `env_reset` en esta máquina. **La recomendación nueva está
  vista funcionar, no deducida.**

- **📌 Alcance del arreglo.** Se cambió también la forma en los tres sitios que
  la traían **sin** secreto dentro (`deploy/README.md`,
  `deploy/console_steps.md`, y el otro mensaje de error de `install.sh`). El
  dominio no es secreto y ahí no filtraba nada — **el motivo no era la fuga,
  era la plantilla**. Arreglar la instancia y dejar el molde es dejar viva la
  fábrica, y el de más tráfico es el que menos lo parece: un mensaje de error
  se lee y se copia justo cuando alguien improvisa una línea de comandos con
  algo roto delante.

### [L-060] 2026-08-14 — Sellar la predicción es la mitad del método: falta comprobar que el instrumento puede decidirla

- **Qué pasó.** Antes de leer la barra del día 14 se sellaron **dos**
  predicciones a propósito, para que se pudieran distinguir:

  ```
    derivación completa ... $0,180 – $0,190   (depende del modelo al 100%)
    por resta ............. $0,177 – $0,187   (el modelo solo pesa el 9%)

    la idea: si cae en $0,177–$0,180, falla la primera y aguanta la segunda
  ```

  La consola dijo **`$0,18`**. Las dos se cumplen. **Y eso no es una victoria
  doble.**

- 🔑 **Por qué no lo es.** La consola **redondea al céntimo**, así que `$0,18`
  significa cualquier cosa entre `$0,175` y `$0,185`. Esa horquilla **pisa las
  dos franjas a la vez**. La zona que iba a discriminar —`$0,177` a `$0,180`—
  mide **tres milésimas**, y el instrumento no puede resolver menos de diez.

  > **Las dos predicciones se sellaron con más cifras significativas de las que
  > la pantalla podía leer.** El experimento estaba mal diseñado, y salió
  > "bien" — que es la forma peor de estar mal diseñado.

- 🧭 **La regla que sale, y completa el método de la predicción sellada:**
  **antes de sellar dos predicciones que compiten, comprobar que la distancia
  entre ellas es mayor que la resolución del instrumento que las va a decidir.**
  Si no lo es, o se busca otro instrumento, o se sella **una sola** y se dice
  claro que esta lectura no puede separar las hipótesis.

- ⚠️ **Y el fallo es de la familia silenciosa.** Un criterio mal fijado que sale
  ROJO se investiga. Este salió **verde por partida doble**, y la lectura
  natural es *"los dos modelos aciertan"* cuando lo cierto es *"la pantalla no
  distingue"*. 📌 Es primo de `[A-018]`: allí un `0,00` con *"sin datos"* al lado
  se leyó como medición. **Aquí un acierto sin resolución se lee como
  confirmación.** En los dos casos el instrumento dijo menos de lo que se le
  atribuyó.

- ✅ **Lo que sí quedó bien medido**, y no se toca: `$0,18` cae dentro de la
  banda `$0,156–$0,205`, así que la **rama A** se cumple sin ambigüedad — para
  *eso* la resolución sobraba. La banda estaba bien dimensionada; la pareja de
  predicciones, no.

- **A raíz de:** `T-095`, lectura del 2026-08-14. `[D-079]`, `[L-059]`,
  `[A-018]`, `[D-074]`.

---

### [L-059] 2026-08-14 — La cercanía no protege: dos números contradictorios cabían en la misma entrada, a cincuenta líneas

- **Qué pasó.** `[D-077]` se contradijo **dentro de sí misma**, escrita de una
  sentada por una sola persona:

  ```
    decisions.md:110 → "~361 y ~49 por llamada"        (la corrida NUEVA)
    decisions.md:161 → "comparar contra 60 × $0,00234" (precio medido con 247)
  ```

  Cincuenta líneas de distancia, el mismo autor, el mismo minuto. Y aun así uno
  describía la corrida nueva mientras el otro razonaba con el precio de la
  vieja. Ver `[D-078]`.

- 🔑 **Lo que enseña, y desmonta algo que dábamos por bueno.** Hasta hoy el
  bicho de la sesión 33 era *"la misma cosa escrita en **dos archivos**
  diciendo cosas contrarias"*, y la defensa era **la proximidad**: por eso las
  decisiones se escriben juntas, en una entrada, para que quien lea una lea la
  otra.

  > **Estar cerca no obliga a nadie a cruzar los dos números.** La proximidad
  > pone los datos al alcance; no fuerza la resta. Leer en orden no es comparar.

- 📌 **Lo único que habría mordido aquí es ARITMÉTICO, no de proximidad.** El
  `$0,1404` era un **producto ya resuelto**, pegado en la prosa. Un número
  calculado a mano y pegado no se recalcula al releerlo — se lee como un hecho.
  Una **expresión delata sus entradas**: `60 × $0,00234` con el `247` al lado
  obliga a preguntarse de dónde salió el 247, y ahí el 361 salta solo.

  🧭 **Regla: en `decisions.md`, un número que sale de otros números se escribe
  como la operación, con sus entradas visibles — no como el resultado.** Es
  exactamente el método que `measure_tutor.py` ya usaba para
  `MAX_CALLS_PER_RUN` y `TARGET_SAMPLES`, que son divisiones y no literales
  (`[D-060]`, `[D-075]`). **El código ya sabía hacerlo y la prosa no lo
  heredó.**

- ⚠️ **Y el disparador que faltaba.** Editar `GRAMMAR_RUBRIC` movió el coste sin
  avisar a nadie. `[L-043]` había identificado bien el término dominante —*"la
  rúbrica pesa casi todo"*— y acto seguido lo trató como constante. Es al revés:
  **que la rúbrica domine el coste es exactamente lo que vuelve el coste
  sensible a editar la rúbrica.**

- **A raíz de:** `T-094`, auditoría externa del 2026-08-14. El hallazgo lo trajo
  cruzando dos documentos; al comprobarlo aquí apareció dentro de uno solo, que
  es peor. `[D-078]`, `[D-077]`, `[L-043]`, `[D-058]`, `[D-066]`.

---

### [L-058] 2026-08-13 — «El peor de N» es un suelo que crece, no un techo

- **Qué pasó:** la báscula local se corrió seis veces a lo largo del día. El peor
  caso subió en **todas**:

  ```
  44,9 → 45,9 → 49,2 → 50,6 → 56,3 → 62,4 ms      +39%, y subiendo
  ```

  Ahí no decidía nada: sobraba por 30×. Pero **el mismo estadístico estaba
  sosteniendo un número que sí decidía.** `[D-072]` justificaba `read = 6,5` como
  *"un 38% por encima de los 4,72 s de la peor de diez"*.

  > 🔑 `max(n=10)` **no estima una cota. Estima un cuantil que se mueve con N.**
  > Un número anclado ahí caduca en cuanto se vuelva a medir — y el que lo relea
  > no verá nada raro, porque el número seguirá teniendo el mismo aspecto.

- 🔑 **El movimiento que importa, y es el que no puede hacer una auditoría
  externa:** el hallazgo apareció **midiendo algo que no decidía nada** y hubo
  que llevarlo a donde sí decidía. Nadie que lea el código lo encuentra: hay que
  estar corriendo el guion por sexta vez y notar que el número no se está quieto.

  📌 Lo dijo la propia terminal auditora al devolvérnoslo: *"coger un hallazgo de
  donde no importa y llevarlo a donde sí es lo que esta terminal no puede hacer
  por vosotros"*.

- 🧭 **La regla:**

  > **Un número que decide algo no se ancla en `max(N)`.** O se calcula por
  > **resta** —lo que cabe en el presupuesto, sin depender de ninguna medida
  > (`[D-073]`)— o se compra un **percentil decidido ANTES** de medir.

  ⚠️ Si se decide después, se tomará `max(N)` — que se sentirá **más sólido
  cuanto mayor sea N**, y será exactamente el mismo error con mejor apariencia.

- ⚠️ **Y en el caso de red es peor que en el local, no mejor.** La distribución
  local la produce esta máquina bajo una carga que elegimos nosotros: con más
  muestras converge hacia algo real. La del tiempo de generación la produce un
  sistema que **no controlamos y que no se está quieto** — capacidad, versión del
  modelo, carga del día.

  ⇒ **No hay cola que medir que siga ahí cuando se use el número.** Es el
  argumento definitivo contra afinar `read` a una cola medida, y lo que llevó a
  `[D-073]`.

- 📌 **Tercera generación de la misma familia.** En `[L-044]` el número **no medía
  lo que su nombre decía** (salía de un `len()`). En `[L-045]` **medía bien y
  caducó** al cambiar la configuración. Aquí **mide bien y envejece solo**, sin
  que nadie cambie nada: basta con volver a medir.

- **Cómo se cazó:** corriendo la báscula por sexta vez en la tercera ronda de
  auditoría del día, y preguntándose por qué el número no paraba de subir.

### [L-057] 2026-08-13 — La báscula heredó el tope que tenía que medir, y se quedó ciega

- **Qué pasó:** `[D-071]` puso `read = 4,0` en producción. Y `measure_tutor.py`
  construye su cliente con `tools.TIMEOUT` **a propósito**, porque `[L-043]` dice
  —con razón— que *"un guion que armara su propia llamada mediría otra cosa"*.

  ⇒ Desde ese momento, toda llamada que pasara de 4 s dejaba de ser una
  **muestra** y pasaba a ser un **error**.

- 🔑 **Y lo que quedaba invisible era exactamente lo que hacía falta.** Para
  colocar bien un tope hay que ver **la cola de la distribución**: las llamadas
  lentas. Son justo las que el tope convierte en excepciones.

  > 🔑 **Un instrumento no puede medir el tope que hereda.** Mide su propio tope
  > y llama a eso un resultado.

- 🚨 **No da un número falso: da SILENCIO, y disfrazado.** Correr la báscula al
  día siguiente para validar el reparto habría impreso *"ninguna llamada pasa de
  4 s"*. Cierto y vacío. Y el disfraz es bueno: las que pasaban aparecían como
  `TutorUnavailableError`, o sea **"Anthropic tardó"** — culpa que se le carga a
  un tercero.

  📌 Es `[L-053]` (el `curl` mudo) otra vez: un cero que significa *"no hubo"* y
  un cero que significa *"no pude ver"* se imprimen igual. Solo que aquí el
  instrumento cuesta dinero cada vez que se usa.

- 🧭 **La regla, escrita como EXCEPCIÓN a `[L-043]` y no como enmienda:**

  > **La báscula es idéntica a producción en TODO menos en el tope que está
  > intentando medir.**

  Mismo modelo, mismo esfuerzo, misma rúbrica, mismos `max_retries`, la misma
  función `judge_grammar`. Solo cambia el `read`. La excepción es exacta y no se
  estira a "la báscula puede desviarse cuando convenga".

- **El arreglo:** `MEASURING_READ_SECONDS = 30.0` en `measure_tutor.py`, y el
  porqué escrito **junto a la constante**, no en un índice — es `[L-047]`: el
  aviso va donde va a mirar quien lo rompa.

- 📌 **Parentesco: es `[L-054]` un anillo más afuera.** Allí la premisa sin
  comprobar estaba en el código. Aquí está **en el instrumento que serviría para
  comprobarla**. Cuando el arreglo de un fallo ciega a su propio verificador, el
  siguiente error tarda mucho más en salir.

- **Cómo se cazó:** auditoría externa el 2026-08-13, en la segunda vuelta del
  mismo día — mirando qué le pasaba a la báscula después del arreglo, no solo si
  el arreglo estaba bien.

### [L-056] 2026-08-13 — Un 504 rompe el invariante del pool, y se demostró sin concurrencia

- **Qué se afirmaba**, en `app/api.py`, encima de `TUTOR_POOL_SIZE`:

  > *"La cola del tutor nunca es el cuello de botella. Si FastAPI no puede
  > atender más de 40 peticiones a la vez, nunca habrá 41 tutores pidiendo
  > sitio."*

- 🔴 **Es falso en cuanto vence un timeout.** El invariante supone que cada
  petición viva ocupa un sitio del pool **y solo uno**. El 504 rompe justo esa
  contabilidad:

  1. vence `result(timeout=…)` → la ruta devuelve el 504 y **suelta su ficha de
     `anyio`**;
  2. pero `respond` sigue corriendo en el hilo del pool —Python no sabe matar un
     hilo— y **el sitio no se suelta**.

  ⇒ El pool se llena **con menos de 40 peticiones vivas**. Con Anthropic
  atascado, los zombis se acumulan y vuelve la cola: el cobro por espera de
  `[L-013]`.

- 🔑 **Cómo se demostró, que es lo que vale para el próximo:** con peticiones
  **secuenciales**. `test_a_timed_out_tutor_keeps_its_pool_seat_with_nobody_waiting`
  lanza dos, una detrás de otra, con un pool de 2. **En ningún instante hay dos
  vivas.** Y la tercera se queda en la cola igual, sin arrancar, y se le devuelve
  la cuota.

  > 🔑 **Para atacar un invariante de concurrencia no hizo falta concurrencia.**
  > Hizo falta encontrar **dónde se descuadra la contabilidad**. Es `[L-045]`
  > —*"para provocar contención se quita sitio, no se añade carga"*— un paso más
  > allá: aquí ni siquiera se quitó sitio, se dejó basura ocupándolo.

- ✅ **Resuelve la contradicción que `[D-070]` dejó abierta.** Usaba como carga
  dos cosas incompatibles: *"el reembolso vive en el `except`"* y *"la cola no se
  forma por construcción"*. **La falsa es la segunda.** El reembolso
  (`attempt.cancel()`) **no es código muerto**: es exactamente lo que atiende a
  quien se quedó esperando detrás de un zombi.

- ⚠️ **Se vio morder:** con `max_workers=3` en vez de 2 hay sitio para la
  tercera, esta arranca (`empezo: si` tres veces en el log) y el test cae.

- 📌 **Misma raíz que `[L-054]`, a otra altura.** Sin techo real en el cliente
  hay 504; con 504 hay zombis; con zombis hay cola. Los dos hallazgos de la
  auditoría son el mismo bicho visto desde dos pisos.

- **Cómo se cazó:** la auditoría externa del 2026-08-13 señaló la contradicción
  y apostó por el mecanismo del zombi, citando el comentario de `_TUTOR_POOL`.
  La apuesta era correcta y se confirmó con una corrida.

### [L-055] 2026-08-13 — Los punteros de línea se leyeron antes de editar, y el commit los movió

- **Qué pasó:** `[D-070]` citaba tres sitios del código. Al terminar el commit,
  los tres estaban desplazados:

  | lo que decía la entrada | dónde vivía de verdad | desfase |
  |---|---|---|
  | `app/tools.py:83` | `app/tools.py:108` | +25 |
  | `app/api.py:698` | `app/api.py:714` | +16 |
  | `app/api.py:146` | `app/api.py:162` | +16 |
  | `tests/test_tools.py:270` | correcto ✅ | 0 |

- 🔑 **La firma delata que no es descuido.** El desfase de cada archivo era
  exactamente cuántas líneas insertó el commit en él, y **el único puntero
  correcto apuntaba al único archivo que el commit no tocó.** Un despiste
  aleatorio no dibuja ese patrón: los números se leyeron del árbol **antes** de
  editarlo y se escribieron **después**.

- 🚨 **Y el aterrizaje puede ser peor que "no encuentras la línea".**
  `measure_local_parts.py` mandaba al lector a `tools.py:83` *"para ver el
  techo"*. Con el desfase, eso caía **dentro del comentario que afirmaba el techo
  falso** de `[L-054]` — no en la línea que fija el número.

  > 🔑 Un puntero muy desviado no lleva a ninguna parte y se nota. Uno desviado
  > **unas pocas líneas** lleva a algo plausible, y no se nota. El segundo es el
  > peligroso.

- 🧭 **La regla, y es de procedimiento, no de criterio:**

  > **Los punteros se releen AL FINAL, contra el árbol ya escrito. Nunca durante
  > la edición.**

  Y donde valga, se cita el **símbolo** (`_TUTOR_POOL`, `TIMEOUT_SECONDS`,
  el nombre del test) en vez del número: el nombre sobrevive al diff.

- 🔴 **AMPLIADA el 2026-08-13, misma tarde, por el fallo que la propia regla
  dejó pasar.** Estaba escrita como *"los punteros de LÍNEA se releen al final"*,
  y por ese hueco se coló un puntero **por nombre**: `measure_local_parts.py`
  citaba en presente `test_the_local_scale_uses_the_real_pool_size` como
  guardián vivo… en el mismo commit que **borraba ese archivo**, veinte líneas de
  diff más arriba.

  > 🔑 **Citar el símbolo protege del desplazamiento, no del borrado.** Cambiar
  > números por nombres arregla la mitad del problema y da la sensación de haber
  > arreglado el problema entero — que es peor, porque se deja de mirar.

  ⇒ La regla vale para **cualquier puntero**: líneas, nombres de test, nombres de
  archivo, anclas `[D-0nn]`. Al final, contra el árbol ya escrito.

  📌 Y el sitio vuelve a ser el mismo: `measure_local_parts.py`, tercera vuelta
  seguida de la auditoría sobre este archivo. Un archivo que se toca en tres
  rondas acumula prosa vieja más rápido de lo que nadie la relee.

- 📌 **Mismo defecto sigue vivo en dos entradas viejas:** `[L-045]` y `[L-042]`
  citan `app/tools.py:82`. No se corrigen aquí para no ensanchar el diff, pero
  quedan nombradas.

- **Cómo se cazó:** auditoría externa el 2026-08-13, comprobando cada puntero
  contra el árbol en vez de leerlos.

### [L-054] 2026-08-13 — El techo del que colgaba todo no existía, y venía citado de dos sitios

- **Qué pasó:** `[D-070]` cerró `[A-011]` apoyándose en una frase concreta —*"el
  cliente corta a los 8,0 s pase lo que pase"*— y presentándola, con razón, como
  más fuerte que una medida: un **techo impuesto** no depende de cuántas muestras
  se tomen.

- 🔴 **El techo no existe.** `httpx` no trata `timeout=8.0` como un tope de la
  llamada: lo reparte a **cuatro fases con cronómetro independiente**.

  ```
  connect=8.0   read=8.0   write=8.0   pool=8.0   →   suma 32,0 s
  ```

  Y el `read` es peor de lo que parece: `httpcore` lo aplica a **cada lectura del
  socket**, no al cuerpo entero. Con `keepalive_expiry=5.0` y tráfico esporádico,
  casi toda llamada abre conexión nueva y paga handshake.

  🚨 **Consecuencia viva:** en una red mala la llamada pasa de los 10 s de la
  ruta **sin que el cliente proteste**. El orden `8 < 10` se invierte de hecho, y
  el error real de Anthropic se esconde tras el 504 — justo lo que ese orden
  existía para impedir.

- 🔑 **Lo que lo hizo invisible: la premisa no nació en la entrada que se cayó.**
  Ya estaba escrita en `[L-045]` (*"corta el cliente antes"*) y en `[L-043]`
  (*"el cliente corta a los 8,0 s"*), dos entradas **correctas en todo lo demás**.
  Se heredó como dato, no como afirmación a verificar.

  > 🔑 Es `[L-034]` con otro dueño. Allí eran **citas** que se propagaban por
  > parecer verificadas. Aquí es una **premisa** — y una premisa repetida en dos
  > entradas tranquiliza igual que un test en verde.

- 🚨 **Y el disfraz era la propia virtud del argumento.** *"Me apoyo en un techo,
  no en una observación"* es un razonamiento **correcto**, y fue precisamente lo
  que dio confianza para cerrar. El eslabón sin comprobar era el techo mismo.
  Cuanto mejor es la forma del argumento, menos se audita su base.

- **Y se comprobaba gratis, con una línea que nadie corrió:**

  ```
  python -c "import anthropic; t=anthropic.Anthropic(api_key='x', timeout=8.0)._client.timeout; print(t.connect, t.read, t.write, t.pool)"
  ```

  Sin red, sin llave válida, sin gastar un centavo.

- 🧭 **La regla:**

  > **Cuando un cierre se apoya en que "el sistema no deja pasar de X", eso ES la
  > afirmación central y se mide primero — aunque venga citada de tres sitios.**

- ✅ **Lo que sí aguantó, y conviene separarlo:** la medida barata que se hizo
  bien. Los 56,3 ms de trabajo local son sólidos, no dependen de la red, y la
  báscula está bien construida —incluido su test, que se vio morder—. **Falló la
  mitad que se dio por sabida, no la que se midió.**

- **Cómo se cazó:** auditoría externa el 2026-08-13, atacando exactamente la
  distinción que la sesión principal le pidió atacar.

### [L-053] 2026-08-13 — El `curl` mudo fabricó un hallazgo contra un despliegue correcto

- **Qué pasó:** al auditar el despliegue, la comprobación
  `curl -s https://teapp.duckdns.org/ | grep 'id="practice"'` salió **vacía**. Con
  eso a la vista, la conclusión natural era *"el despliegue contradice lo que
  afirmas: el contador nuevo no está en la página"*. La corrida siguiente, en el
  mismo instante y contra la misma máquina, devolvió `200` y los tres contadores.
- **Por qué salió vacía:** el nombre no resolvió (`[A-017]`, DuckDNS). Con `-s`,
  `curl` **se calla y devuelve un cuerpo vacío**. El `grep` no recibe un error:
  recibe la nada. Y sobre la nada, `grep` no dice *"no pude medir"* — dice **"no
  está"**.
- 🔑 **Ahí está el veneno, y es peor que un falso negativo normal.** Un
  instrumento roto que se queja te para. Este **no se queja y produce una
  afirmación con forma de hallazgo**: acusa a un despliegue correcto, con la
  confianza de una medida.
- 📌 **Mordió DOS veces el mismo día**, a dos terminales distintas: primero a la
  sesión principal —que lo cazó porque miró el `exit 6` y el `000`— y después a
  la de auditoría, que estuvo a un paso de escribirlo como hallazgo. **Dos
  víctimas en un día es un instrumento mal usado, no mala suerte.**
- **El arreglo, de una línea:** mirar **el estado antes que el cuerpo**, y no
  encadenar un `grep` a un `curl` cuyo éxito no se ha comprobado.

  ```bash
  # mal: si no resuelve, esto dice "no está" sobre una pagina que si lo tiene
  curl -s https://teapp.duckdns.org/ | grep 'id="practice"'

  # bien: primero el codigo, y saltandose el DNS
  curl --resolve teapp.duckdns.org:443:<IP> -o /dev/null -s -w "%{http_code}\n" \
       https://teapp.duckdns.org/
  ```

- **Anillo exterior de `[L-051]`.** Aquella fue la pantalla mintiendo sobre un
  despliegue bueno; esta es **el instrumento de medida** mintiendo sobre el mismo
  despliegue bueno. 🔑 La moraleja se repite: **el silencio no es un dato hasta
  que tiene un control al lado.**

### [L-052] 2026-08-13 — El maniquí tapó una decisión de diseño, y la devolvió el día caro

- **Qué pasó:** `[A-001]` —*¿el marcador cuenta frases practicadas o
  correctas?*— se escribió el **2026-08-02** y no se resolvió hasta el
  **2026-08-13**. Once días abierta. Se resolvió justo el día en que había que
  tocar el contrato de `judge_grammar`, con el modelo recién enchufado.
- **Por qué sobrevivió tanto, que no es por descuido.** Con el juez falso —que
  aprobaba todo— **las dos lecturas daban exactamente el mismo número**. Ningún
  test podía distinguirlas, ninguna pantalla se veía distinta, y nada en el
  proyecto empujaba a decidir. La pregunta no se aplazó: **dejó de ser urgente
  sola.**
- 🔮 **Y la propia entrada predijo la factura, al pie de la letra.** `[A-001]`
  decía: *"el coste de equivocarse crece con el tiempo: hoy es un contrato que
  nadie usa todavía; en el paso 8 sería rediseñar la herramienta el mismo día que
  se enchufa el modelo, con dos sospechosos en vez de uno."* **Pasó eso, once
  días después, palabra por palabra.**
- 🔑 **Lo transferible, y es la lección de verdad:** cuando una pieza se sustituye
  por un maniquí, la pregunta habitual es *"¿qué fallo puede esconder?"*. Esa es
  la fácil, y la vigila `no_data_writes.py`. **La difícil es otra: "¿qué DECISIÓN
  deja de doler?"** — porque un maniquí que da siempre la misma respuesta hace
  que varios diseños distintos se vean idénticos. Ese empate es lo que congela la
  decisión, y se descongela el día que el maniquí se va: el día más caro.
- 📌 **No es un argumento contra el maniquí.** El roadmap lo pone en el centro a
  propósito y sigue siendo correcto: sacar la pieza ruidosa deja un solo
  sospechoso cuando algo falla (misma lógica que `[D-049]`). Lo que hay que
  añadir no es quitarlo, es **una pregunta al ponerlo**: *¿qué decisiones voy a
  dejar de sentir mientras esto esté puesto?* Anotarlas ahí mismo — que es
  exactamente lo que `[A-001]` hizo bien, y por eso hoy hubo qué resolver en vez
  de un descubrimiento.
- ⚠️ **Y esta lección nació de una auditoría, no de la sesión.** `[A-001]` había
  escrito su propio destino —*"si sube y chirría → era falsa. Sale de aquí y
  entra en `lessons.md`"*— y al morir se la mandó entera a `decisions.md`
  (`[D-066]`), que es el destino de la **otra** rama. La mitad "decisión" se
  cumplió; la mitad "lección" se perdió, y con ella esto. Lo cazó la auditoría
  del mismo día. 🔑 **Una suposición que asciende puede tener que ir a los DOS
  sitios, y el que se olvida siempre es el segundo.**

### [L-051] 2026-08-13 — Datos nuevos en un molde viejo, y por eso engañó

- **Qué pasó:** después de subir `[D-066]` al servidor, la primera práctica real
  desde el navegador mostró `Words: 4 · Score: 1`. **Sin `Practice`.** El
  despliegue parecía a medias.
- **Qué pasaba de verdad:** el servidor estaba perfecto. Comprobado pidiéndole la
  página con `curl`, que devolvió la línea entera con los tres contadores y el
  `<span id="practice">` dentro. Lo viejo era la copia que el navegador tenía
  guardada.
- 🔑 **Por qué esta forma engaña más que un caché normal.** Si todo estuviera
  viejo, se sospecha del navegador en dos segundos. Aquí no: **el `Score` que se
  veía era el CORRECTO** —una frase mala no lo subió, que es justo lo que se
  acababa de programar—. Los números llegan en cada respuesta y son frescos; el
  molde que los coloca es el archivo cacheado. **Mitad nuevo y mitad viejo, sin
  ninguna señal de cuál es cuál.**
- **Cómo se separó:** dejando de mirar lo que el navegador pinta y mirando lo que
  el servidor manda:

  ```bash
  curl -s https://teapp.duckdns.org/ | grep -o '<p class="counters">.*</p>'
  ```

  Si ahí está el contador, el problema está de este lado de la red.
- **Lo que funciona y lo que no:** `Ctrl+Shift+R` **a veces no basta**. La prueba
  concluyente es una **ventana de incógnito**: arranca sin caché, así que está
  obligada a descargarlo todo. Si ahí aparece, el despliegue estaba bien.
- 📌 **Va a repetirse en cada despliegue que toque la pantalla**, y no tiene
  arreglo en el código de hoy: es cómo funcionan los navegadores. Lo que evita
  perder media hora es el orden — **preguntarle al servidor antes que al ojo**.
- **Hermana de `[L-007]`, y por el fondo, no por el tema.** Allí un `diff -r`
  gritó *"el `.js` está viejo"* con el repositorio correcto: **el instrumento
  medía de más y acusaba a quien no era**. Aquí el instrumento fue el ojo mirando
  la pantalla, dijo *"el despliegue está a medias"*, y el despliegue estaba
  entero. Distinto tema, mismo error de fondo: **se creyó a un instrumento que no
  medía lo que se estaba preguntando.**

### [L-050] 2026-08-13 — El comentario dice que da igual, y de eso depende todo

- **Qué se encontró.** `deploy/check_api_key.py:62-63`, encima de la constante
  del modelo:

  ```python
  # El modelo que usa la app hoy ([D-049] lo revisa en el paso 9). Da igual cuál
  # sea para lo que se pregunta aquí: lo que interesa son las cabeceras.
  MODEL = "claude-opus-5"
  ```

- **Por qué es falso.** Los frenos de Anthropic se configuran **por modelo**. Lo
  dice `[D-061]` desde su propio texto —*"cada modelo nuevo necesita su fila con
  su propia medida"*— y lo confirmó la consola el 2026-08-13, que enseña el
  límite bajo el encabezado *"Claude Opus 5 · Solicitudes"*. Así que la cabecera
  `anthropic-ratelimit-requests-limit` no dice *"el freno del espacio"*: dice
  **el freno de ESE modelo en ese espacio**.
- **Qué rompe.** El `50` de `LAB_REQUESTS_PER_MINUTE` es la firma del
  laboratorio, y es **el 50 de `claude-opus-5`**. El día que alguien cambie
  `MODEL` —al bajar a Haiku en el paso 9, que es exactamente lo que `[D-049]`
  tiene planeado— el portero pasa a leer el cubo de otro modelo, con otro
  número. 🚨 **No da error: se queda mudo y deja pasar la llave del
  laboratorio.** El mismo fallo silencioso que este archivo entero existe para
  impedir, entrando por una puerta que nadie vigila.
- **Y lo que lo hace peor que un despiste:** el comentario no solo se equivoca,
  **autoriza el cambio**. Quien vaya a tocar `MODEL` va a leer justo encima que
  da igual, y va a creerlo — está escrito por quien construyó la pieza.
- **Parentesco.** Es `[L-047]` con una pata más. Allí se anotó que el `50` vive
  en **dos** sitios (`[D-061]` y el código). Son **tres**: el tercero es
  `MODEL`, y no está anotado en ninguno de los dos avisos que ya existen.
- 📌 **No se toca hoy (PI-3).** El hallazgo es de lectura, no de corrida, y
  `T-078` está a medias por otra razón. Queda escrito para que el arreglo se haga
  cuando toque `MODEL`, que es el momento en que muerde.
- **Relacionadas:** `[L-047]`, `[D-061]`, `[D-063]`, `[D-049]`, `T-078`, paso 9.

### [L-049] 2026-08-13 — Una tarea muerta volvió con una factura pegada

- **Qué pasó:** el arranque de esta sesión presentó `T-074` (verificar el apagado
  automático de la EC2) como la tarea **pendiente y más urgente** del día, con
  cuatro días de retraso y una consecuencia económica encima. `T-074` está
  **cerrada desde el 2026-08-10**, con testigo directo en el journal
  (`Aug 09 23:00:00 Starting teapp-shutdown.service …` seguido en el mismo
  segundo de `systemd-logind: The system will power off now!`), registrada en
  `tasks.md:81` y en `[S-034]`.
- **Por qué pasó — y por qué es la SEGUNDA vez:** el 2026-08-12 la misma tarea
  muerta ya viajó en el traspaso, y el cerrador la cazó mandando la evidencia del
  archivo. Pero **esa corrección solo existió en la conversación.** El cerrador
  escribió el puntero viejo de todas formas, y a la mañana siguiente el arranque
  lo leyó y lo sirvió como estado real. Es `[L-029]` en su forma más limpia —
  lo que nace después del cierre no tiene dueño—, salvo que aquí lo huérfano no
  fue una decisión buena: **fue la caza de un error.**
- **Lo que lo hace peor que un duplicado:** el primer día volvió como repetición
  inofensiva. El segundo volvió con **precio**: *"van cuatro días de retraso, y
  esa máquina encendida se come el plan gratuito"*. Esa frase falla por los dos
  lados. La terminal auditora midió la máquina el 2026-08-13 a las 12:46 UTC
  —dentro de la ventana de `[D-045]`, pero el encendido es manual y nadie la
  encendió— y encontró **443 y 22 mudos los dos**, con `nslookup` resolviendo
  bien: no hay nada que sostenga "la máquina encendida". Y aunque lo hubiera,
  con la EC2 apagada lo que sigue cobrando son la **IP elástica y el volumen
  EBS**, no las horas de instancia (`T-067` separa las tres tarifas): la frase
  nombraba al culpable equivocado incluso en el caso de ser cierta.
- **La regla que queda:** 🔑 **una tarea muerta que reaparece con una factura
  pegada deja de ser un duplicado y se convierte en la agenda del día.** El
  dinero y el retraso saltan la cola de la verificación — nadie audita una
  urgencia, se obedece. El antepasado es la sesión 60 del lado supervisor, donde
  lo inventado fue la versión **cómoda** ("no hace falta hacer nada"); aquí fue
  la **incómoda**, y es peor, porque la incómoda suena a diligencia.
- **Qué se hizo hoy:** se borró `T-074` del campo *siguiente acción* de
  `progress.md` (línea 12) y de la cola de `[S-044]`, con la nota de por qué en
  las dos. 🔑 **La caza de ayer solo cuenta cuando toca el disco.** Una
  corrección que vive en el chat es una corrección que mañana no existe.
- **De regalo, episodio nuevo de `[A-017]`:** de tres intentos contra
  `teapp.duckdns.org`, uno falló en resolución de nombre en 0,028 s y los otros
  dos fueron timeout de verdad. El cliente otra vez, no DuckDNS.

### [L-048] 2026-08-12 — El tercer sabotaje pasó en verde, y el roto era el test

- **Qué pasó:** al construir `T-078` se escribieron tres sabotajes para ver
  morder las capas nuevas. Los dos primeros salieron rojos como se esperaba. El
  tercero —mover la comprobación de la llave **detrás** de la escritura, que es
  justo el fallo que `[D-063]` existe para impedir— **pasó en verde**.
- **Por qué pasó:** el test comparaba números de línea así:

  ```python
  comprueba = next(i for i, l in enumerate(lineas) if "check_api_key.py" in l)
  ```

  Y la primera línea que nombra `check_api_key.py` **no es la llamada: es un
  comentario** que la explica, doce líneas antes. Ese comentario está arriba
  pase lo que pase, así que la comparación daba verde con la llamada movida al
  final del archivo.
- 🚨 **Lo que lo hace peligroso no es que fallara: es que tranquilizaba.** El
  test tenía nombre correcto, aserción correcta y salía verde. Habría entrado en
  la suite de 410 como un guardián más, y el día que alguien moviera la
  comprobación de verdad, no habría dicho nada. **Un guardián que se cumple solo
  es peor que ninguno**, porque el que no existe al menos no engaña.
- **Qué se hace distinto, y son dos cosas:**
  1. **Un test que lee un archivo de texto mira las líneas ACTIVAS**, no los
     comentarios. Es lo mismo que ya hacía `test_deploy_limits.py` con
     `líneas_activas`, y aquí se reinventó peor. La cadena buscada tiene que ser
     la que solo aparece en lo que se ejecuta (`bin/python` + el nombre), no una
     que el propio comentario repite.
  2. 🔑 **Y la de fondo: un sabotaje que sale verde no prueba que la capa esté
     bien — prueba que el test no vigila.** Sin los tres sabotajes esto entra al
     repositorio. `[D-060]` ya pedía ver morder cada capa; esto añade que el
     sabotaje también audita al vigilante, y en este caso fue lo único que lo
     hizo.
- 📌 **Parentesco:** misma familia que `[L-043]` y `[L-047]` — algo escrito que
  parece cubrir un riesgo y no lo cubre, y que precisamente por parecerlo deja
  de auditarse. Aquí en forma de test verde.

### [L-047] 2026-08-12 — Un acoplamiento se anota donde va a mirar quien lo rompa

- **Qué pasó:** `[D-063]` hizo que `deploy/install.sh` aborte el despliegue si la
  llave devuelve `requests-limit: 50`, porque ese valor es la firma del
  laboratorio (`[D-061]`). Con eso, el `50` pasó a vivir en **dos sitios**: la
  decisión que lo fijó y el guion que lo interroga. La reacción natural fue
  documentarlo en `[D-063]`, que es donde se entendió. **Y ahí no lo iba a leer
  nadie.**
- **Por qué pasó — la pregunta correcta no es "¿dónde lo entendí?" sino "¿quién
  va a romperlo, y qué archivo va a tener abierto?".** El día que el `50` suba a
  80 para medir Haiku —que `[D-061]` ya predice por escrito en su trampa del paso
  9— quien lo haga **no está desplegando nada**: está afinando el laboratorio.
  Abre `[D-061]`, que es donde vive el número. `[D-063]` ni se le pasa por la
  cabeza, y no tiene por qué. El aviso escrito solo en la entrada que lo entendió
  es un aviso colocado donde no hay nadie.
- 🔑 **Y el fallo que produce es de los mudos:** cambia el número, el laboratorio
  queda bien afinado, todo sigue en verde, y la comprobación del despliegue deja
  de reconocer al laboratorio **sin dar un solo error**. Nadie rompió nada
  visiblemente; solo se apagó una red.
- **Qué se hace distinto:** cuando un dato quede acoplado a dos sitios, **el aviso
  se escribe en los dos, y el que manda es el del sitio donde vive el dato**, no
  el del sitio donde se descubrió el acoplamiento. En este caso `[D-061]` lleva
  *"cambiar este número obliga a tocar `deploy/install.sh` en el mismo cambio"*, y
  el número en el guion lleva encima de dónde sale y qué se rompe si se mueve —
  **un número desnudo en el código es un número que alguien va a "limpiar"**.
- 📌 **Parentesco, porque son la misma familia vista por dos caras:** `[L-043]`
  dice que una salvedad en el párrafo no arregla un titular falso —el párrafo no
  se relee, la tabla sí—. Esto dice lo mismo un piso más arriba: no basta con que
  la advertencia exista, tiene que estar **en la ruta de lectura** de quien puede
  hacer el daño. Las dos son el mismo error: escribir para quien ya entendió.

### [L-046] 2026-08-12 — Nueve 529 seguidos, y lo que cuestan cuando llegan

- **Qué pasó:** para averiguar qué llave había en el `.env` —la de `Default` o
  la nueva de `teapp-measure`— hacía falta una llamada real, porque las
  cabeceras `anthropic-ratelimit-*` dicen contra qué límites se contó. Salieron
  **nueve `529 Overloaded` seguidos** en unos 50 segundos. Anthropic estaba
  saturado; el proyecto no tenía nada roto.

- 🔑 **Lo que enseña no es el 529: es lo que el código hace con él.**
  `app/tools.py:320` lo manda a la red de seguridad con `request_sent=True`:

  > *"Aqui caen los 500 y el 529 de saturacion —que si gastaron tokens de
  > entrada—. Ante la duda se COBRA."*

  Así que **la cuota se cobra y no se devuelve**. Es `[D-051]` funcionando como
  se decidió, no un fallo. Pero júntalo con `MAX_RETRIES = 0` de `[D-053]`:

  > 🚨 **Durante una racha así, quien practica pierde prácticas de sus 20 sin
  > recibir un solo veredicto.** Cada reintento suyo es un intento perdido más.

  Hasta hoy eso era un párrafo en `decisions.md`. Ahora tiene fecha y hora.

- ⚠️ **Y de paso murieron dos vías de diagnóstico, las dos gratis.** Conviene
  saberlo antes de volver a intentarlo:

  | instrumento | qué se esperaba | qué pasó |
  |---|---|---|
  | cabeceras del 529 | leer el límite desde el error | **no trae ninguna** `ratelimit` |
  | `count_tokens` | confirmar la llave sin gastar | válida ✅, pero **no dice cuál** |
  | columna "último uso" | ver qué llave se usó | **no registra** `count_tokens` |

  Comprobado, no supuesto: los tres se probaron hoy.

- 🧭 **Lo transferible.** La tolerancia a la saturación era una decisión que
  **nadie había visto ocurrir**. `MAX_RETRIES = 0` se eligió para que el error
  llegara limpio y sin disfraz, y sigue siendo defendible. Lo que cambia es que
  ya no es teórica: si el paso 9 va a hacer tandas largas, conviene decidir a
  propósito si quiere un reintento con espera — sabiendo que **un reintento
  también cuesta tokens de entrada**, que es justo lo que `[D-051]` cobra.

- 📌 **Se deja como observación con fecha, no como cambio.** Nada se toca hoy.

📎 **SEGUNDO EPISODIO, 2026-08-13 — y esta vez trajo el instrumento que faltaba.**

Al comprobar la llave `teapp-server` recién creada (`[D-065]`), `check_api_key.py`
salió **cuatro veces seguidas por la puerta 4** con `529`. Y ahí está la trampa:
la puerta 4 significa las tres cosas a la vez —red caída, Anthropic saturado, o
llave mal escrita—, así que **una corrida sola no distingue "Anthropic está
saturado" de "esta llave nueva no sirve"**. La conclusión cómoda estaba servida:
culpar a la llave recién creada, borrarla y crear otra.

🔑 **Lo que lo resolvió fue un control al lado, no un reintento más.** Se corrió
la misma llamada con la llave del **laboratorio**, que veinte minutos antes había
contestado `3` limpiamente. Dio `529` también. Con eso el veredicto es
inmediato: si la llave que ya funcionó hoy tampoco pasa, el fallo no está en la
llave nueva. Es la misma forma de `T-060b` y de `[D-063]` — **un instrumento que
puede dar la misma respuesta por dos razones distintas necesita un segundo caso
que las separe**, y aquí el segundo caso ya estaba a mano y era gratis.

📌 **Para la próxima vez, escrito como procedimiento:** ante una puerta 4
repetida, antes de tocar nada, correr una llave que ya se sabe buena. Cuesta ~10
tokens y ahorra borrar y recrear credenciales a ciegas.

⚠️ **Y refuerza lo de arriba:** el `529` no llegó en una tanda larga ni bajo
carga propia. Llegó en llamadas sueltas de 10 tokens, con horas de diferencia
respecto al primer episodio. `claude-opus-5` se satura seguido en esta cuenta, y
eso ya no es una anécdota de un día: son dos días distintos.

### [L-045] 2026-08-12 — El número que sí se midió, en una máquina que ya jubilamos

- **Qué pasó:** el plan de hoy para `T-079` era lanzar **23 peticiones a la vez**
  contra `/practice` con llamadas reales, para provocar cola y ver si
  `TUTOR_TIMEOUT_SECONDS = 10.0` aguanta. El 23 tiene procedencia: está medido y
  escrito en `[L-013]` y repetido en `app/api.py:689` —*"23 peticiones a la vez,
  20 llegaron al tutor, 3 pagaron por nada"*—.

  El problema no es de dónde salió, sino **cuándo**:

  | entonces | ahora |
  |---|---|
  | `ThreadPoolExecutor()` sin número → **20** hilos (16 CPUs de aquella máquina) | `TUTOR_POOL_SIZE = 40`, escrito a mano (`app/api.py:184`) |
  | 23 contra 20 sitios → **3 en cola** | 23 contra 40 sitios → **0 en cola** |

  > 🔑 El 23 era el número correcto para un pool de 20. Ese pool lo jubilamos
  > nosotros, precisamente para arreglar `[L-013]`. **El arreglo dejó obsoleto al
  > número que lo justificaba, y el número siguió circulando.**

- 🚨 **Qué habría pasado si se corre.** Con 40 sitios nadie espera: la espera
  medida sale cero, el timeout no dispara, la corrida sale **verde** y la
  conclusión escrita sería *"los 10 s aguantan"* — sobre un escenario que no
  ocurrió, pagada con saldo real. Un verde que no significa nada es peor que un
  rojo: el rojo se investiga.

- 🚨 **Y debajo, el hallazgo que cambia la tarea entera.** Para que haya cola
  harían falta **más de 40 a la vez**. Pero el invariante de `app/api.py:172`
  dice que el pool iguala las 40 fichas del limitador de `anyio`, así que la
  petición 41 se queda esperando **antes de que arranque la función de la ruta**
  — antes del `submit` de `app/api.py:668`, y por tanto antes de que el reloj de
  los 10 s empiece a contar. Esa espera es **invisible** para el timeout.

  Súmale el otro extremo: el cliente corta a los **8,0 s** (`app/tools.py:82`),
  la ruta a los 10.

  > 🔑 **Los 10 s no pueden disparar por modelo lento (corta el cliente antes) ni
  > por cola (la cola no se forma, por construcción).** La única rendija que
  > queda es que `respond()` **fuera del modelo** —`count_words` y `add_point`,
  > que escribe en disco con candado— se coma más de 2 s.

  📌 Eso no es *"falta medir `[A-011]`"*: es que `[A-011]` puede estar
  preguntando por un freno que no existe. Y esa pregunta **se contesta leyendo,
  no gastando**.

- 🧭 **La regla transferible, y es la que vale para el próximo experimento:**

  > **Para provocar contención se quita sitio, no se añade carga.**

  Cerrar todas las cajas menos una, en vez de traer mil clientes al
  supermercado. Y ya estaba hecho: `tests/test_api.py:1043` monta un pool de
  **1** con el docstring *"deja el pool en un solo sitio, para que el segundo
  tenga que hacer cola"*. Tutor de mentira, coste cero, cola garantizada. La
  ráfaga de 23 con llamadas reales habría gastado dinero para reproducir **peor**
  algo que ya estaba reproducido.

- ⚠️ **Tercer motivo, por si los dos anteriores no bastaran: la ráfaga no cabía.**
  `quota.py:58` es `DAILY_LIMIT = 20` **por persona**, y la cuota se cobra antes
  del `submit`. 23 peticiones desde una sola cuenta meten 20 al pool y las otras
  3 salen con un 429 de cuota **sin tocar al tutor**. Un plan de concurrencia que
  no dice con cuántas cuentas se lanza no es un plan de concurrencia.

- 🚨 **Lo que esta lección NO dice, y hay que leerlo antes de cerrar nada.** El
  test que encontramos fija `TUTOR_TIMEOUT_SECONDS = 0.2` para poder correr en
  milisegundos. Eso prueba **el mecanismo**, no **el número**:

  | pregunta | estado |
  |---|---|
  | ¿La cola devuelve la cuota a quien nunca arrancó? | ✅ probado, y gratis |
  | ¿10 s es el número correcto? | 🔲 sin contestar |

  > ⚠️ **`T-079` sigue viva por su mitad de arriba.** *"El experimento ya estaba
  > hecho"* es cierto de la primera fila y falso de la segunda. Un titular que
  > vale para media tarea la cierra entera si nadie separa las filas.

  🧭 **Y la mitad que queda cambió de forma:** ya no es *"cronometrar bajo
  concurrencia"*. Si el freno no puede disparar —ni por cola ni por modelo
  lento—, lo que queda es **decidir qué se hace con él**: bajarlo por debajo de
  los 8,0 s del cliente para que muerda de verdad, o retirarlo y escribir por
  qué no hacía falta. Las dos salidas son de leer y decidir, no de gastar.

- ➕ **Y el invariante aprieta más de lo que escribimos.** `/practice` no es la
  única ruta síncrona: `/me`, `/login`, `/register`, `/logout` y `/` también son
  `def`, así que también consumen fichas de las 40 de `anyio`. Caben **menos de
  40 prácticas a la vez**, no 40 — la cola del tutor tiene todavía menos
  posibilidades de formarse. ✅ Y el invariante no cuelga de la lectura de nadie:
  `test_the_pool_matches_the_threads_fastapi_actually_uses` se pone rojo si los
  dos números dejan de coincidir.

- 📌 **Hermana de `[L-044]`, con un día de diferencia y la forma invertida.**
  Allí el número nunca midió nada (salía de un `len()`). Aquí midió bien y
  **caducó**. Un número medido no es verdadero para siempre: es verdadero para la
  configuración en la que se midió, y esa configuración es parte del número
  aunque no se escriba al lado.

  La pregunta que caza las dos es la misma: **¿qué pregunta contestó el día que
  se escribió, y es la misma que le estoy haciendo hoy?**

### [L-044] 2026-08-11 — El número que parecía medido y salía de un `len()`

- **Qué pasó:** `measure_tutor.py` traía `MAX_CALLS = 10`, presentado —con un
  comentario de nueve líneas encima citando `[D-057]`, `[C-008]` y `[A-024]`—
  como el corte duro que protege el saldo. Al preguntar de dónde salía el diez,
  la respuesta estaba veinte líneas más abajo: **`SENTENCES` tiene exactamente
  diez frases.**

  ```python
  MAX_CALLS = 10          # ...con aspecto de tope de gasto
  SENTENCES = [ ... ]     # ...diez frases
  for ... in SENTENCES[:MAX_CALLS]:   # [:10] sobre diez: no corta nada
  ```

- **Por qué pasó:** el número **circuló tres veces**, y cada paso lo hizo parecer
  más medido que el anterior:

  | vez | disfraz |
  |---|---|
  | 1 | constante llamada `MAX_CALLS`, que suena a tope |
  | 2 | "corte duro", con comentario citando tres entradas de `_persistence/` |
  | 3 | argumento hablado hoy: *"no hay diseño que pensar: el número ya lo tienes de `T-079`, diez llamadas"* |

  > 🔑 **La tercera es la peor, y la dije yo.** `T-079` hizo diez llamadas
  > **porque había diez frases**. Usé el resultado de un `len()` como si fuera el
  > resultado de una medición, y lo presenté como el paso que no había que
  > pensar.

- 🚨 **Y lo que lo hacía cumplir tampoco frenaba.** La ejecución era
  `SENTENCES[:MAX_CALLS]`. Con tope 10 y lista de 10, ese recorte **no puede
  cortar nunca**. Un freno que jamás podía morder, con nombre de freno — y nadie
  lo probó **precisamente porque el nombre tranquilizaba**.

- **Qué se hace distinto:**

  > 🧭 **Un número que decide dinero se escribe como la operación que lo produce,
  > no como su resultado.**

  `int(0.25 / 0.00234)` se puede auditar leyéndolo. `106` hay que creérselo. Y
  `10` hay que creérselo **aunque venga de un `len()`**. Si la operación no cabe
  en el código, va en la entrada de `decisions.md` con sus dos factores y su
  procedencia. En `[D-060]` la división está en el código y hay un test que
  comprueba que sigue siendo una división y no una constante escrita a mano.

- 🔍 **Cómo se caza, que es lo transferible.** La pregunta útil no es *"¿este
  número es correcto?"* —el diez lo era, para su pregunta— sino:

  > **¿qué pregunta contestó el día que se escribió, y es la misma que le estoy
  > haciendo hoy?**

- 📌 **Tercera cara del mismo bicho en tres días, con dueños distintos:**
  `[A-011]` medía otro reloj, un resumen hablado ensanchó un bloqueo que el
  documento no tenía, y este medía un largo de lista. **Ninguno de los tres era
  falso. Los tres estaban mal rotulados.** Es `[L-041]` en su forma más pura: el
  nombre describe la pista, no el hecho.

- Encontrado por auditoría externa el 2026-08-11 — en dos pasos: primero al
  señalar que el diez venía del historial y no del saldo, y después, leyendo el
  código, al ver que ni siquiera venía del historial.

### [L-043] 2026-08-11 — El tutor medido de verdad, y el reloj que iba justo no era el vigilado

**Cómo se midió.** `measure_tutor.py`, diez llamadas a través de
`judge_grammar` — la misma función que usa la app — con un cliente construido
igual que el suyo (`max_retries=0`, `timeout=8.0`). Un guion que armara su
propia llamada habría medido otra cosa y se habría parecido lo bastante como
para que nadie lo notara. Tope duro de 10 llamadas escrito arriba del archivo,
y `for` sobre lista acotada en vez de `while`.

**Lo medido:**

⚠️ **La cabecera de esta tabla dice `judge_grammar`, no «práctica», y la
diferencia es la que echó a perder el cierre de `[A-011]`.**

| | mínimo | mediana | peor de diez |
|---|---|---|---|
| tiempo de `judge_grammar` | 1,72 s | 3,33 s | 4,72 s |
| tokens de entrada | 245 | — | 250 (media 247,2) |
| tokens de salida | 30 | — | 59 (media 44,3) |

🔴 **CORREGIDO el mismo día por auditoría externa: aquí decía «`[A-011]` queda
cerrada: los 10 s aguantan con 5,28 s de margen». Es falso, y el fallo está en
qué se cronometró.**

| dónde | qué abarca |
|---|---|
| `app/api.py:668-671` | `submit(respond, …)` → `result(timeout=10)`: **cola del pool + `respond()` entero** |
| `app/english_tutor.py:79-83` | `count_words` + `judge_grammar` + `add_point` (disco, con candado) |
| `measure_tutor.py:122-133` | **solo `judge_grammar`**, sin cola |

Los 4,72 s son **uno de los tres trozos**. Restar `10 − 4,72` da un margen sobre
un presupuesto que paga cosas que la báscula no cronometró. `[A-011]` está
**reabierta como encogida**: la mitad medida vale, la de la cola no está hecha.

🔑 **Y el nombre lo delataba: la tabla decía «tiempo por práctica».** Es
`[L-041]` en su tercera generación — el rótulo describe el **mecanismo** por el
que se obtuvo el número, no el hecho que decide. Cazado en un campo el día 10,
en un precedente el 11, y aquí en la **cabecera de la medida que retiraba una
suposición**.

📌 **La salvedad estaba escrita y no sirvió de nada.** Más abajo esta misma
entrada decía «no dice nada de la cola llena» — correcto, y aun así el titular
fue «`[A-011]` muere» y el índice se tachó. **Una salvedad en el párrafo no
arregla un titular falso: el párrafo no se relee, la tabla sí.**

🔑 **El hallazgo bueno, y el reencuadre lo hace más duro de lo que se escribió:**
El cliente de Anthropic corta a los **8,0 s** (`app/tools.py:82`); la ruta, a
los **10 s**. El del cliente mide un **subconjunto** de lo que mide el de la
ruta **y además es más pequeño**.

⇒ **En una llamada que no hace cola, el timeout de la ruta no puede disparar
NUNCA.** El cliente corta antes, siempre, y sale por `app/tools.py:303` como
`APITimeoutError` con `request_sent=True`.

🚨 **O sea: los 10 s nunca protegieron de un modelo lento.** Lo único que pueden
llegar a frenar es la **cola** — el escenario de `[L-013]` y `[L-042]`. Todos
los comentarios del proyecto sobre este freno —`app/api.py`, `[A-011]`— hablan
de él como si acotara la espera al modelo. No la acota: la acota el otro.

⚠️ Y el margen del cliente —3,28 s sobre 4,72— **cuelga de una sola
observación**: n=10 con dispersión de 2,7×, y el máximo de diez muestras no es
la cola de la distribución. Se mira, no se toca: el `8,0` es el freno vivo, y
moverlo sin más datos sería cambiar un número medido por otro inventado.

💰 **El coste por práctica es casi FIJO, y eso cambia cómo se lee `[C-002]`.**
La entrada apenas se mueve entre llamadas —245 a 250 tokens— porque **la
rúbrica del sistema pesa casi todo y la frase del alumno casi nada**. O sea:
una frase de 3 palabras y una de 30 cuestan prácticamente lo mismo. El tope de
500 caracteres sigue haciendo falta —protege del abuso— pero en uso normal
**nunca se acerca**, y por tanto no es la palanca para bajar la factura. La
palanca es el modelo, que es trabajo del paso 9 (`[D-049]`).

✅ **La rúbrica se comportó como se le encargó**, y esto no se había visto
nunca: un solo error señalado por respuesta, dos frases cortas, sin markdown,
y las cuatro frases correctas reconocidas **sin inventarles una corrección** —
que era el riesgo real de un juez con ganas de ayudar.

⚠️ **Lo que esta medida NO dice, escrito para que nadie la estire:** son diez
llamadas, desde una red doméstica, a una hora concreta, **sin concurrencia** y
desde Windows. No dice nada de la latencia desde la EC2 de AWS, ni de qué pasa
con la cola del pool llena —que es justo el escenario de `[L-013]` y de
`[L-042]`.

🔑 **Y esta frase ya estaba escrita cuando la entrada tituló «`[A-011]` muere».**
Ese es el hallazgo de método que deja la corrección: **saber la limitación y
escribirla no impide sacar el titular equivocado.** La salvedad tranquiliza a
quien la escribe —siente que ya lo ha dicho— y no toca el índice, que es donde
vive la conclusión. Si la salvedad contradice al titular, **la que manda es la
salvedad, y el titular hay que reescribirlo**, no acompañarlo.

🚨 **Y `[L-001]` mordió por tercera vez, en el peor sitio posible.** El
resumen final del guion llevaba emoji; `cp1252` lo tumbó con
`UnicodeEncodeError` **después** de haber hecho las diez llamadas. Los números
se salvaron solo porque ya estaban impresos línea a línea; el cálculo se rehizo
aparte. 🔑 **En un guion que gasta dinero, un fallo de impresión al final no es
cosmético: es tirar la corrida.** El archivo lleva ahora el aviso encima de
`main`, y la regla es la de siempre — lo que se **imprime** va en ASCII; los
emoji de los comentarios dan igual, porque nadie los imprime.

### [L-042] 2026-08-11 — El precedente de la casa se copió sin comprobar si seguía siendo válido

**Qué se encontró.** El `except` escrito hoy para `TutorUnavailableError` lleva
un comentario que dice: *"Es la misma forma que el timeout de arriba, que se lo
pregunta a `future.cancel()`"*. Lo cita como el buen precedente. Por el criterio
que esta misma sesión aplicó en `[L-041]`, **es el proxy**.

`app/api.py:692` decide si se devuelve la cuota con `attempt.cancel()`, que
contesta *"¿llegó a arrancar la tarea?"*. La pregunta que decide el dinero es
otra: *"¿se facturaron tokens?"*.

🔢 **La ventana no es teórica y sale de dos constantes que ya existen:**

| reloj | valor | dónde |
|---|---|---|
| cliente de Anthropic | `8.0 s` | `app/tools.py:82` |
| ruta `/practice` | `10.0 s` | `app/api.py:146` |

**Dos segundos de margen.** Si la tarea espera más de 2 s en la cola del pool y
luego la conexión se agota a los 8 s —cero tokens, `request_sent=False`—, el
reloj de la ruta ya venció: `cancel()` devuelve `False` porque la tarea sí había
arrancado, y **se cobra una práctica que no costó nada**. La espera en cola no es
hipotética: está medida en `[L-013]` (23 peticiones a la vez, 20 llegaron al
tutor, 3 pagaron por nada).

⚖️ **Dónde la auditoría se pasa, y cambia el arreglo.** Propone preguntarle a
`request_sent` en vez de a `cancel()`. **No se puede:** en el instante del 504 la
tarea sigue corriendo y ese dato **todavía no existe**. Esperarlo es exactamente
lo que el timeout está evitando. El dato llega después, así que devolver la
cuota exigiría un `add_done_callback` que refunde **más tarde**, cuando el hilo
termine — maquinaria nueva, con su propio riesgo de devolver dos veces.

🔑 **O sea: `[D-023]` no era ingenua, era correcta con lo que se sabía.** Al
decidirse, no había ninguna forma de saber si se había facturado, y ante la duda
se cobra (regla 3 aplicada al dinero). Lo que cambió es que **desde `[D-051]` el
dato existe** — tarde, pero existe. Una premisa dejó de ser incomprobable y nadie
volvió a mirarla.

🔑 **Es `[L-041]` con otro dueño, el mismo día y en la misma función.** Allí el
proxy estaba en el **nombre** (`request_sent`), aquí en el **instrumento**
(`cancel()`). Y lo llamativo: esta sesión pasó por delante y lo citó de **ejemplo
a seguir** en un comentario nuevo. Describirlo y no verlo, en la misma frase.

🧭 **Regla que queda: cuando se copia un precedente de la propia casa, se
comprueba si el precedente SIGUE siendo válido, no solo si es el mismo patrón.**
Un precedente propio se audita menos que uno ajeno, porque ya pasó una vez.

📌 Detectado por auditoría externa el 2026-08-11. **Sin arreglar a propósito:** el
arreglo es una decisión con precio (PI-2), no una línea, y se toma con el usuario.

### [L-041] 2026-08-11 — El campo que decide el dinero tiene nombre de otra cosa

**Qué pasó.** Al terminar `T-077` se levantó la app de verdad —PI-4, *lo que no
se ha corrido no está terminado*— con una llave de API inválida a propósito, para
ver el 503 nuevo sin gastar un centavo. Funcionó todo: `503`, mensaje correcto,
cuota devuelta (`used: 0`) y marcador que no sube. Y en el log apareció esto:

```
WARNING El tutor no esta disponible (usuario prueba, la peticion salio: no):
El tutor rechazo la peticion: Error code: 401 - {'type': 'authentication_error',
'message': 'invalid x-api-key'}, 'request_id': 'req_011Cdw3g4CgkcsZFcSWv8qqS'
```

🔑 **`request_id` lo emite Anthropic.** Para que exista, la petición tuvo que
salir de la máquina, cruzar internet, llegar y ser procesada. O sea: *la petición
salió*. Y el log, en la misma línea, dice **`salio: no`**.

**Por qué el comportamiento es correcto de todos modos.** Lo que ese campo
decide no es si el paquete salió: es **si se facturaron tokens**. Un 401 no
factura nada, así que la cuota se devuelve, y eso es exactamente lo que manda
`[D-051]`, que lo define bien en prosa: *"Cero tokens gastados"*. `[D-055]` ya
había movido el caso del rechazo vacío a `usage` por la misma razón. **El
comportamiento está bien; el nombre se quedó atrás.**

🚨 **El daño posible, escrito concreto para que no haya que imaginarlo:** alguien
abre el log dentro de seis meses, ve un `request_id` junto a `salio: no`,
concluye que es un bug e invierte la condición. A partir de ahí **cada 401 y
cada 429 se cobran**, que es justo lo que `[D-051]` prohíbe. Y no rompería
ningún test que hoy exista si además ajusta el maniquí: el nombre le habría dado
la razón todo el rato.

🔑 **Es `[L-040]` con el instrumento cambiado.** Allí el proxy estaba en el
código —deducir de la forma de `content` lo que `usage` contaba literalmente—.
Aquí el proxy está en el **nombre**: describe el mecanismo por el que se detecta
el hecho (*salió el paquete*) en lugar del hecho que decide (*se facturó*). Un
nombre así se lee mal igual que un proxy se mide mal.

🧭 **Regla: cuando un campo decide dinero, su nombre dice el CONCEPTO, no la
pista.** `billed` o `tokens_billed` habría sido verdad en las dos lecturas.

⚠️ **Por qué no se renombra hoy, que es decisión y no olvido.** El nombre viaja
por `app/tools.py`, `app/api.py`, siete tests y cuatro entradas de
`decisions.md` (`[D-051]` a `[D-055]`). Cambiarlo dentro de `T-077` llenaría el
diff del día de cambios que nadie pidió, y PI-3 dice que entonces el registro
deja de servir. Queda anotado con el riesgo escrito; el renombrado es su propia
tarea, y hasta que se haga **esta entrada es el aviso**.

📌 **Y el hallazgo salió de CORRER la app, no de leer el código.** La suite
entera pasaba en verde —387 tests— con el nombre igual de engañoso, porque
ningún test mira un log con ojos de quien no sabe. PI-4 pagándose solo el mismo
día que se aplicó.

### [L-040] 2026-08-10 — Se dedujo de la forma lo que el instrumento ya contaba, y la corrección se equivocó peor

**Dos fallos encadenados, y el segundo enseña más que el primero.**

## 1. El proxy que no podía separar dos casos iguales por fuera

`[D-054]` decidía si devolver la cuota del día mirando si `content` venía vacío —
un **proxy** de *"esto no se facturó"*. La API contestaba esa misma pregunta
literalmente, en el mismo objeto, a un atributo de distancia:
`usage.input_tokens` y `usage.output_tokens`.

🚨 **Y el proxy tenía un agujero real, no teórico.** Comprobado en la
documentación de Anthropic el 2026-08-10: **sin streaming** —que es como llama
`judge_grammar`— un rechazo a **mitad** omite el parcial. Esa respuesta llega con
`content` vacío y `stop_reason="refusal"`, **calcada por fuera** al rechazo
gratis, y con los tokens ya pagados. Se devolvía cuota justo donde `[D-051]`
manda cobrar.

🔑 **La forma general: un proxy no puede separar dos casos que tienen la misma
forma.** Cuando dos respuestas distintas se ven idénticas, ningún razonamiento
*sobre la forma* las distingue — hace falta un dato que no sea la forma.

📌 **Es `[L-036]` con otro instrumento** (líneas 334–335): *"antes de citar la
narración, mirar si el instrumento ya trae su propio reloj"*. Allí el reloj, aquí
el contador.

🔬 **Y el diagnóstico del día anterior estaba a medias.** El cierre concluyó que
los fallos habían sido *de ejecución, no de conocimiento* — *"un comentario
protege a quien lo lee; un test protege también a quien no"*. Este no: **nadie en
el proyecto sabía qué factura un rechazo hasta abrir la documentación.** Era un
**hueco de conocimiento**, y no había test posible que lo cazara — no se escribe
un guardián para una pregunta que nadie ha hecho todavía. Los cuatro hallazgos
técnicos del paso 8 —el `max_tokens` compartido, el reloj de diez minutos, el
rechazo gratis, el parcial omitido— salieron de **abrir la documentación**;
ninguno de razonar.

## 2. 🚨 La corrección que se equivocó peor que el error

La auditoría citó `[L-036]` para la regla del contador. La sesión principal fue a
comprobar la cita —bien—, **abrió la entrada, leyó trece líneas de ciento
diecinueve**, vio que el encabezado hablaba de cerrar `[A-014]` y
`request.client.host`, y **declaró la cita falsa**. La regla estaba noventa
líneas más abajo, dentro de esa misma entrada.

🔑 **Una lectura parcial se sintió exactamente igual que una comprobación.** El
gesto de abrir el archivo produjo la sensación de haber verificado, y esa
sensación bastó para *retirar* una cita correcta y escribir en su lugar una
afirmación falsa — dentro del párrafo escrito para denunciar `[L-034]`. El fallo
que la lección describe se cometió al describirlo.

🧭 **Regla: abrir la entrada no es leerla.** Si la frase citada puede estar en
cualquier línea de una entrada larga, la comprobación es **buscar la frase**
(`grep` del concepto dentro del rango de la entrada), no un vistazo al principio.
Y una cita solo se **retira** habiendo leído la entrada entera; ante duda, se
deja y se marca.

⚠️ **Y llegó commiteada por `[L-029]`**: la revisión externa entró con la sesión
ya cerrada de hecho —informe escrito, commit en camino—, así que el hallazgo
nació sin dueño y no se recogió. Tercera vez esta semana. Lo que nace después del
cierre solo se arregla si alguien lo lleva **explícitamente** al arranque
siguiente.

---

### [L-039] 2026-08-10 — El guion que verificaba los guardianes modificó lo que verificaba

**Qué pasó.** Los cinco guardianes nuevos de `T-076` hay que verlos rojos antes
de fiarse de ellos. Se hizo con un guion en Python: por cada uno, leer el
archivo, sustituir la línea que sostiene la decisión, correr solo ese test,
restaurar el archivo. Los cinco se pusieron rojos. Todo correcto.

Después, `git status` marcó `app/english_tutor.py` como modificado — un archivo
que el trabajo del día **no toca**. Y `git diff` no enseñaba ni una línea.

**Por qué.** `Path.write_text()` en Windows traduce `\n` a `\r\n`. El guion leyó
LF y escribió CRLF. El contenido volvió a ser el correcto; los bytes, no.

```
identicos byte a byte: False
CRLF en disco: 57 | CRLF en el repo: 0
```

Tres archivos quedaron convertidos: `app/tools.py`, `app/english_tutor.py` y
`tests/test_api.py`. En `tools.py` eso convertía el diff del día en **el archivo
entero**, que es exactamente lo que PI-3 prohíbe: *"si viene lleno de cambios que
nadie pidió, el registro deja de servir"*.

**Lo que enseña, y es una forma que no estaba en la lista.**

🔑 **El instrumento de verificación tocó al sujeto y no lo deshizo del todo.**
Se restauró el **contenido** con cuidado, y se dio por hecho que restaurar el
contenido era restaurar el **archivo**. No es lo mismo, y la diferencia no
aparece en ninguna comprobación que mire texto.

🔑 **Este proyecto tiene porteros para el código y ninguno para el andamio.**
`no_network.py`, `no_data_writes.py` y los guardianes de `deploy/` vigilan lo que
corre dentro de pytest. Un guion escrito para medir vive fuera, dura cinco
minutos y nadie lo audita — pero escribe en los mismos archivos.

⚠️ **El testigo que lo delató fue el más tonto:** `git status` diciendo
"modificado" y `git diff` sin enseñar nada. Esa contradicción **solo** puede
significar bytes cambiados sin contenido cambiado. Se lee en dos segundos, si
uno mira el `git status` al terminar de verificar y no solo al ir a commitear.

🔧 **Regla.** Un guion que escribe archivos para medir usa `write_bytes` (o
`newline=""`), y al acabar se comprueba **`git status`**, no solo que la suite
esté verde. *Verde* y *limpio* son dos preguntas distintas, y la segunda no la
contesta pytest.

📌 **De regalo, `[L-001]` mordió en la misma corrida.** El guion imprimía `✔` y
`✘` para marcar cada sabotaje, y la consola de Windows lo tumbó con
`UnicodeEncodeError` a mitad del bucle — la primera lección del proyecto,
cometida en un guion de usar y tirar donde nadie pensó que aplicaba. Una lección
escrita no protege el código que se escribe *fuera* del proyecto para medirlo.

---

### [L-038] 2026-08-10 — El resumen del cierre inventó un hecho cómodo y lo vistió con citas que lo desmienten

- **Qué pasó:** el cierre escribió en `progress.md`, campo `siguiente acción` —el
  primero que se lee al día siguiente—:

  > *"La máquina de producción sigue viva y facturando dentro de su ventana de
  > uso — no hace falta encenderla a mano, el apagado y encendido ya son
  > automáticos (`[D-045]`/`[D-046]`)."*

  Las tres fuentes disponibles dicen lo contrario:

  | fuente | qué dice de verdad |
  |---|---|
  | `[D-045]` | *"el apagado es automático desde dentro de la máquina; **el encendido es manual**"* |
  | `console_steps.md:416` | *"**no se enciende sola**: hay que venir a la consola"* |
  | `[D-046]` | **ni menciona encender** — es el temporizador que APAGA |

  Y hay un argumento que no necesita abrir ningún archivo: **una máquina apagada
  no tiene nada corriendo dentro que pueda encenderla.**

- **Por qué pasó:**
  - 🔑 **No es `[L-034]`, y la diferencia importa.** Allí una cita real apuntaba
    a la entrada equivocada por colisión de identificadores. Aquí **la
    afirmación no venía de ninguna parte**: se fabricó al comprimir, y los
    corchetes se le pegaron **después**, como armadura. Dos identificadores al
    lado bastan para que nadie baje a comprobar la frase.
  - 🧭 **La dirección del error es el diagnóstico.** Lo inventado fue siempre la
    versión **cómoda** (*"no hace falta hacer nada"*), nunca la incómoda. Un
    resumen comprime, y **la compresión deriva hacia lo tranquilizador**: una
    frase que no le pide nada al lector no ofrece resistencia al escribirse.
  - 🏗️ **Causa estructural: quien escribió esa frase no había visto la
    máquina.** `session-closer` arranca en frío y reconstruye del `git diff` —
    para eso existe (`[D-002]`). Pero **un diff no dice si una máquina está
    encendida.** Una afirmación sobre el estado físico del mundo no se puede
    reconstruir de ahí, así que no le toca a quien no estuvo.
  - 📡 **Y viajó por dos canales, no uno.** La sesión principal repitió la frase
    en su resumen hablado, leyéndola del reporte del cierre **sin abrir las
    fuentes** — cometiendo al relatarla el mismo fallo que la lección describe.
- 💰 **El daño real no es el viaje a la consola.** `T-056` necesita SSH y la
  máquina amanece apagada, sí. Pero lo grave es que **el encendido manual es el
  mecanismo, no una carencia**: `[D-045]` lo escribió asimétrico a propósito para
  que el olvido caiga del lado que **no** cobra.

  > 🔑 La nota no rompía la máquina. Rompía **la decisión diaria de gastar
  > dinero**, que era el producto real de `[D-045]`.

- **Qué se hace distinto:**
  1. En `siguiente acción`, toda afirmación sobre el estado físico de la máquina
     se escribe en **pesimista por defecto** — *"amanece apagada mientras no
     conste lo contrario"*. Es la regla 3 (denegar por defecto) aplicada a los
     hechos y no a los permisos.
  2. El closer **no afirma estado del mundo**: describe lo que el diff respalda y
     manda al Paso 5b de `deploy/console_steps.md`, que es quien sí lo sabe.
  3. Al relatar un reporte ajeno, las frases que dicen ***"no hace falta"*** se
     abren antes de repetirlas. Son exactamente las que nadie audita, porque
     ahorran trabajo a quien las lee.
- 📌 **La detectó una revisión externa, no el proyecto.** Es `[L-037]` otra vez
  por otra puerta: un control que solo mira hacia dentro de la sesión no ve lo
  que la sesión escribió de más.

### [L-037] 2026-08-10 — El andamio se volvió el trabajo, y ningún control del proyecto miraba hacia ahí

- **Qué pasó:** el paso 7 se comió más tiempo que todos los anteriores juntos, y
  **nadie dentro del proyecto lo detectó**. Lo dijo el usuario:

  > *"Siento que estamos invirtiendo mucho tiempo en esta aplicación, que es de
  > carácter educativo, solo para aprender, y no hemos podido avanzar al
  > siguiente paso."*

  Contado sobre el índice de `progress.md` (regla 6 — contado, no recordado):

  | | sesiones | días |
  |---|---|---|
  | pasos 0 a 6 (siete pasos) | 12 (`S-001`…`S-012`) | 3 |
  | paso 7 (uno solo) | 22 (`S-013`…`S-034`) | 6 |

- **Por qué pasó — y esta es la parte incómoda:**
  - 🔑 **Ninguna sesión estuvo mal.** `[L-034]` es una lección real; el hueco del
    `is-enabled` era un hueco real; las 16 citas cruzadas estaban mal de verdad y
    corregirlas valía la pena. **El fallo es de suma, no de sumandos.**
  - **Y la suma no la mira ningún control.** Cada cierre pregunta *"¿lo que hice
    hoy está bien hecho?"*. Ninguno pregunta *"¿lo que llevo hecho me acerca a lo
    que vine a construir?"*.

    > 🔑 **Un proyecto puede tener todas sus sesiones correctas y estar parado.**

  - 🚨 **El síntoma era visible y se leyó como otra cosa.** Con HTTPS, identidad
    verificada, cuota por persona y apagado automático corriendo en producción,
    **el tutor seguía siendo el maniquí del paso 1**: la aplicación para
    practicar inglés no practicaba inglés. Eso llevaba días escrito en
    `progress.md`, en la casilla `paso 7 de 9` — y se leía como **ubicación**,
    nunca como **aviso**.
  - 👤 **Lo detectó el usuario, no el sistema.** `_persistence/` está diseñado
    para que no se pierda el porqué de lo que se hizo; **no tiene ni un
    instrumento que mida el coste de oportunidad de lo que se está haciendo**.
    Las auditorías externas tampoco lo habrían visto: auditan lo escrito, y lo
    escrito era correcto.
  - 🔴 **Agravante, y ocurrió en esta misma sesión.** Cuando el usuario preguntó
    qué faltaba para cruzar al paso 8, la respuesta puso `T-069` como
    bloqueante — **y era falso**. El *"pronto"* de `[D-030]` se mide contra el
    cierre de la cuenta (`[C-006]`, febrero de 2027), no contra el paso
    siguiente. Un pendiente **heredó su urgencia del sitio donde estaba
    escrito**, no de su plazo real.
- **Qué se hace distinto:**
  1. Al cerrar, **preguntar por el paso, no solo por la sesión**: *"¿qué falta
     para cruzar, y de eso, qué tiene plazo real y qué es inercia?"*.
  2. Tratar *"la pieza central del producto sigue siendo un maniquí"* como una
     **condición que se dice en voz alta en cada cierre**, no como un dato de
     posición en una tabla.
  3. A un pendiente se le pregunta **su plazo**, no su ubicación. Estar escrito
     en la sección del paso 7 no lo convierte en requisito del paso 7.
- 📌 **Emparenta con `[LM.13]` por el lado contrario.** Allí el problema era que
  lo escrito se daba por medido. Aquí **todo estaba medido**, cada pieza
  verificada con su testigo — y aun así el conjunto no avanzaba. Medir bien no
  protege de medir lo que no toca.

### [L-036] 2026-08-10 — El criterio escrito antes es lo que convierte un susto en una lectura más

**Cerrada `[A-014]`.** (Sustituye a esa entrada, retirada hoy de
`assumptions.md`; los punteros antiguos apuntan aquí.) Nació el 2026-08-04 al
partirse `[A-012]`, y decía que `request.client.host` es el origen **real** de
quien pregunta, no la dirección del proxy. Se encogió dos veces —el 06 con la
mitad de Python (`[D-034]`), el 07 con Caddy en maqueta de dos contenedores— y
hoy muere con la cadena entera en el servidor de verdad.

**🚨 Y muere por MITADES, que es como había que matarla.** La primera versión de
esta entrada la dio por cerrada con una sola medición, y una auditoría externa
señaló que faltaba la otra mitad — la que de verdad aguanta un ataque:

| mitad | qué dice | medida |
|---|---|---|
| que llegue la **real** | dos visitas honestas escriben dos direcciones correctas | ✅ máquina real, 15:01–15:02 |
| que se descarte la **falsa** | quien manda `X-Forwarded-For: 9.9.9.9` no consigue que le crean | ✅ máquina real, 15:14 |

🔑 **La segunda es la que importa cuando alguien ataca:** si la cabecera falsa
colara, quien ataca pone una dirección distinta en cada intento y el freno **no
muerde nunca** — el aviso está escrito en `app/api.py:411`. Estaba medida en la
maqueta de contenedores y **solo ahí**; en el servidor real se estaba infiriendo
de que `Caddyfile.template:75` no declara `trusted_proxies`. Eso es *"está
escrito, luego funciona"*, que es justo lo que `[LM.13]` prohíbe — y lo prohíbe
este mismo proyecto, que partió `T-060` en dos por esa razón: **tener el grupo
creado no es tener el cortafuegos**.

**La medida de la mitad falsa, 2026-08-10 15:14 UTC.** Cuatro peticiones con el
cubo de `181.58.39.253` **ya agotado**, lo que convierte el bloqueo en control:
si la cabecera colara, crearía un cubo nuevo y la respuesta sería `401`.

| cabecera enviada | respuesta | origen en el log |
|---|---|---|
| *(ninguna — control)* | `429` | `181.58.39.253` |
| `X-Forwarded-For: 9.9.9.9` | `429` | `181.58.39.253` |
| `X-Forwarded-For: 9.9.9.9, 8.8.8.8` | `429` | `181.58.39.253` |
| `X-Real-IP: 9.9.9.9` | `429` | `181.58.39.253` |

Ni un solo `9.9.9.9` en el log. **Y es un control que se puede ver morder**, no
un verde de los que solo dicen silencio.

**La medida de la mitad real, 2026-08-10 15:01–15:02:**

| dispositivo | `api.ipify.org` | log del servidor | |
|---|---|---|---|
| computador | `181.58.39.253` | `181.58.39.253` | ✅ |
| celular (datos móviles) | `191.153.227.163` | `191.153.227.163` | ✅ |

Cinco `401` y un `429` desde cada aparato; dos `WARNING` con dos orígenes
distintos; ninguno `127.0.0.1`.

**🔑 La trampa se desarmó ANTES de medir, y sin eso la prueba no valía.** El
celular tenía que salir por datos móviles con el WiFi apagado. En el WiFi de casa
habría salido por el mismo router que el computador, y entonces *"una sola
dirección en el log"* significaría dos cosas a la vez —*"el freno está roto"* y
*"medí mal"*— que se leen exactamente igual. Leer `ipify` en cada aparato
**antes** separa esas dos ramas. Leerlo después, ya no: con el resultado delante,
la explicación cómoda gana.

**🚨 Y el criterio escrito antes se ganó el sueldo en el minuto justo.** El log
escribió `191.153.227.163`; lo apuntado a mano decía `191.152.227.163`. Un
dígito. El resultado ya *parecía* el correcto —dos direcciones distintas, ninguna
de loopback— y sin criterio delante habría pasado por bueno sin que nadie mirara
el tercer grupo. El criterio decía *"cada una **igual** a su `ipify`"*, y eso
obliga a parar.

**Cómo se resolvió, que es la otra mitad.** Con una **lectura nueva**, no
reinterpretando la vieja. Había dos explicaciones vivas y las dos encajaban con
el dato: un dígito mal copiado, o la operadora móvil repartiendo la salida entre
direcciones de un mismo bloque entre una conexión y otra. La segunda es real y
habría explicado lo mismo — por eso no se podía elegir la cómoda. Volver a leer
`ipify` en el celular decidió: era el dígito.

⚖️ **Y la palabra exacta es *confirmada*, no *descartada*.** La segunda lectura
de `ipify` ocurrió **después** de ver el log, no a ciegas, así que sabía qué
resultado la haría cuadrar. No mueve el veredicto —las dos direcciones del log
son distintas entre sí y coherentes con cada aparato aunque la operadora
rotase— pero una lectura hecha sabiendo qué se espera pesa menos que una hecha
sin saberlo, y la entrada no puede decir lo contrario. Corregido tras auditoría
externa.

🔑 **`[D-040]` no prohíbe cambiar de idea con el dato delante; prohíbe cambiar el
CRITERIO.** La diferencia práctica es que la duda se paga con una medición más.
Aquí costó treinta segundos.

**🏅 La SEGUNDA demostración, y no comparte instrumento con la primera.** El
celular gastó **sus propios cinco intentos** antes del `429`. El computador había
dejado el cubo agotado a las `15:01:03`; si la app viera solo a Caddy, el primer
toque del celular a las `15:02:11` habría dado `429` en el acto. Dio *"contraseña
incorrecta"* cinco veces.

🔑 **Es la misma conclusión por un camino que no pasa por el log** — se ve desde
el navegador, sin entrar a la máquina. **Una prueba con dos testigos que no
comparten instrumento vale más que una con un solo testigo bueno**, porque un
instrumento averiado no puede producir las dos. Esta entrada la archivó primero
como *"apoyo"*, y una auditoría externa la subió a donde va: es un hallazgo, no
una nota al pie.

**⏱️ Y el log traía un segundo reloj que la primera lectura no usó.** El
`faltan N s` del renglón no es decoración: sale de `login_guard.py:191`
(`retry_after = int(min(recent) + 900 - ahora) + 1`), así que despejando se
reconstruye **cuándo empezó cada ráfaga**, sin depender de lo que nadie cuente.

| aparato | `429` | `faltan` | primer fallo reconstruido |
|---|---|---|---|
| computador | `15:01:03` | `899 s` | `15:01:01` — cuadra al segundo con la corrida |
| celular | `15:02:33` | `879 s` | `15:02:11–12` → cinco intentos en ~21 s, coherente con un formulario ya relleno |
| forjadas | `15:14:57` | `64 s` | `15:16:01` de expiración — el mismo instante, hora y media después |

🔑 **El log llevaba dentro el testigo del relato**, y el relato se había apoyado
en la narración de quien midió. Regla: **antes de citar la narración, mirar si el
instrumento ya trae su propio reloj.**

📌 Con esto muere la última suposición del proxy. Las tres capas quedan medidas
en tres sitios distintos y ninguna sustituye a las otras: `[D-034]` la de Python,
la maqueta de contenedores la de Caddy, y hoy la cadena real de punta a punta.

---

### [L-035] 2026-08-10 — El testigo recomendado era ciego, y lo cegamos nosotros

**Qué se encontró.** Para cerrar `T-074` —ver el temporizador de `[D-045]`
disparar de verdad— una auditoría externa propuso el instrumento evidente:

```bash
systemctl list-timers teapp-shutdown.timer   # LAST y PASSED ya deben venir llenos
```

Vinieron **vacíos**:

```
NEXT                        LEFT LAST PASSED UNIT
Mon 2026-08-10 23:00:00 UTC   8h  -      -   teapp-shutdown.timer
```

**Y no es una avería: es nuestra propia decisión funcionando.** `Persistent=false`
está puesto a propósito en `deploy/teapp-shutdown.timer`, con doce líneas de
comentario explicando por qué (`Persistent=true` apagaría la máquina en la cara
de quien acaba de encenderla por la mañana). Lo que ese ajuste hace por dentro es
decirle a systemd que **no lleve la libreta** de disparos pasados en
`/var/lib/systemd/timers`. Sin libreta, al reiniciar el temporizador nace de
cero — el journal lo confirma: `Started teapp-shutdown.timer` a las `14:06:37` de
hoy, un estreno, no una continuación.

🔑 **`list-timers` no puede contestar *"¿disparó ayer?"* en esta pieza. No hoy:
nunca.**

**Dónde sí estaba el testigo.** En el journal, que en Ubuntu 24.04 vive en disco
y sobrevive al reinicio:

```
Aug 09 23:00:00  Starting teapp-shutdown.service - Apagar la maquina
                 al cerrar la ventana de uso ([D-045])...
Aug 09 23:00:00  systemd-logind[543]: The system will power off now!
```

Nuestra unidad arranca, y el apagado la sigue en el mismo segundo. Eso es una
cadena causal con nuestro nombre dentro — no *"nadie más pudo haberla apagado"*,
que era inferencia por eliminación.

**⚠️ La vuelta nueva sobre `[L-034]`.** Allí el punto ciego era un **descuido**:
se tenía `is-active` a mano y se usó sin preguntar qué no veía. Aquí el punto
ciego se **fabricó deliberadamente**, por una razón buena y bien argumentada — y
aun así se recomendó ese instrumento como testigo del pasado.

🔑 **Un ajuste que apaga la memoria de una pieza apaga también los instrumentos
que leen esa memoria.** Y esa segunda consecuencia no aparece en el comentario
que justifica el ajuste: el de `Persistent=false` habla del riesgo que evita, y
no dice en ninguna línea que deja `LAST` mudo para siempre. Quien lea el
comentario entero —está bien escrito— sigue sin enterarse.

**🔧 Regla.** Antes de citar un instrumento como testigo, preguntar **qué lo
alimenta, y si algo nuestro lo apaga**. Es hermana de `[L-030]` (*preguntar qué
pone a cero un instrumento antes de usarlo como registro*), con el agravante de
que aquí quien lo puso a cero fuimos nosotros, a propósito y por escrito.

**📌 Dos hechos de regalo, que nadie pidió y no cambian nada hoy.**

1. Caddy salió limpio: `{"msg":"shutdown complete","signal":"SIGTERM","exit_code":0}`.
   El apagado fue ordenado, no un tirón de cable.
2. La máquina volvió con **otro núcleo**: `6.17.0-1017-aws` → `7.0.0-1010-aws`,
   actualizado solo y estrenado al reiniciar. Cada noche apagada es también una
   ventana para que la máquina cambie debajo. Los cinco controles pasaron igual;
   se anota, no se toca.

---

### [L-034] 2026-08-09 — El control medía el ahora; la promesa era sobre el mañana

**Qué se encontró.** `install.sh` comprobaba el temporizador de apagado así:

```bash
systemctl is-active --quiet "${SERVICE_NAME}-shutdown.timer"
```

Y justo encima, un comentario declarando que **el fallo del temporizador es el
más mudo de los tres** que hace el guion. El comentario tenía razón. La
comprobación no la miraba.

**Por qué `is-active` no sirve aquí.** Son dos preguntas distintas:

| estado real | `is-active` | `is-enabled` |
|---|---|---|
| habilitado y activo | `active` | `enabled` | ← el bueno |
| ni habilitado ni activo | `inactive` | `disabled` | ← lo ven las dos |
| **activo pero NO habilitado** | **`active`** | `disabled` | ← **solo la segunda** |

> 🔑 **La tercera fila es exactamente el fallo de esta pieza.** Apagaría puntual
> esta noche, `T-074` saldría **verde**, y al siguiente encendido el temporizador
> no vuelve. El control no habría fallado en callarse: habría **certificado lo
> contrario de lo que pasa**.

`is-active` pregunta *"¿está corriendo ahora?"*. Lo que la pieza promete es
*"¿volverá mañana, tras apagar y encender?"*, y eso solo lo contesta
`is-enabled`. **La promesa de la pieza y la pregunta del control hablaban de
tiempos distintos.**

**🔁 Y lo grave no es la línea: es que es la segunda vez el mismo día.** Horas
antes, el cuarto guardián de `tests/test_deploy_shutdown.py` nació buscando el
texto literal `systemctl start teapp-shutdown.service`, que `install.sh` nunca
escribiría porque usa `${SERVICE_NAME}`. Dos sitios distintos —una prueba y un
guion— con la misma forma:

> 🚨 **Un guardián incapaz de ponerse rojo justo en el modo de fallo que su
> propio comentario nombra como el más peligroso.**

**🔍 Por qué se repite.** El comentario se escribe pensando en **el fallo**; la
comprobación se escribe pensando en **la herramienta que se tiene a mano**. Se
escriben con la cabeza en dos sitios y quedan pegadas, así que a partir de ahí
el comentario **avala** la comprobación en vez de examinarla — y quien lo lea
después va a confiar en el conjunto.

**🔧 Regla.** Después de escribir un control, **leer su comentario y preguntarle
a la comprobación: *"¿te pondrías roja en el caso que este comentario acaba de
describir?"*.** Si la respuesta no es un sí evidente, el control mide otra cosa.

## 🚨 El antepasado, y está más cerca de lo que nadie esperaba: `[L-017]`

Buscando con qué enlazar esta lección apareció algo peor que un parecido de
familia. `[L-017]`, del 2026-08-05, dice:

> *El bloque final de `install.sh` se titulaba "PI-4: terminado = visto
> funcionando" y dos líneas después solo miraba `systemctl is-active`.*
> 🔑 *El comentario correcto hizo de coartada: nadie audita un bloque que ya se
> declara auditado.*

**Mismo archivo. Mismo bloque. La misma orden `is-active`. Y el mismo mecanismo
del comentario haciendo de coartada.** Cuatro días después, al añadir una
comprobación **nueva a ese mismo bloque**, se reintrodujo el atajo exacto que
`[L-017]` había arreglado — con un comentario todavía más enfático encima
(*"el más mudo de los tres"*), que volvió a funcionar como coartada.

> 🔑 **Y eso enseña algo que `[L-017]` no podía saber sola:** arreglar un bloque
> no lo inmuniza. **Lo deja más peligroso**, porque a partir de ahí lleva encima
> la cicatriz de haber sido auditado, y esa cicatriz avala también las líneas
> que se añadan después. La coartada la hereda el código nuevo.

📌 **Es el mismo animal que `[L-020]`** —*un verde producido por algo distinto de
lo que el verde afirma*—, que ya iba por su cuarta aparición en `[L-027]`. Lo que
aporta esta es **la causa de por qué se repite**: un control sin estrenar da
miedo y se revisa; **uno en verde tranquiliza y ya no lo mira nadie**. Hasta hoy
eso era una observación; ahora tiene mecanismo.

🔴 **Corrección de esta misma entrada.** La primera versión citaba aquí a
`[L-013]` como *"un control que nadie ha visto funcionar no es un control"`*.
**`[L-013]` no dice eso** — dice *"cerrar un hueco no cierra los demás"*, y lo
dice desde que nació (`499879a`, sin una sola edición). La cita se heredó de
otras entradas del repo sin comprobarla, que es exactamente el error que esta
lección describe, cometido al escribirla. Ver la nota de abajo.

✅ **Corregido el mismo día:** `is-enabled` añadido en `install.sh` junto al
`is-active` —las dos preguntas, no una sustituyendo a la otra— y **quinto
guardián** en `tests/test_deploy_shutdown.py`, cuyo control rojo usa el guion
**tal como estaba antes de la revisión**. 360 → **362** tests.

⚠️ Hoy no mordía, porque unas líneas más arriba está el `enable --now`. El
control existe para el día en que alguien cambie esa línea por un `start`: todo
seguiría verde y la pieza se rompería a partir del siguiente encendido.

### 🚨 Nota aparte, y resultó ser lo más grande del día: `L-013` contra `LM.13`

Al buscar el antepasado apareció que **`[L-013]` estaba mal citada en DIECISÉIS
sitios** — quince en `_persistence/` y uno en `tests/`. Trece de ellas querían
decir `[LM.13]`; las otras tres no eran ninguna lección. Y la causa **no** es lo que
se escribió primero aquí —*"un error de sentido heredado"*—, que era una
explicación plausible y falsa. La causa es una **colisión de identificadores
entre dos repositorios**:

```
LM.13   ← la de verdad. Vive en Edu_TripleS/PROGRESO.md (repo supervisor).
           "un freno que no has visto morder es una nota, no un freno"
 L-013  ← la que se escribió. Vive en TEAPP/_persistence/lessons.md (este repo).
           "cerrar un hueco no cierra los demás"
```

**Una letra de diferencia, dos espacios de nombres, numeración que se solapa.**
No es un descuido de escritura: es una colisión que **volvió a pasar diez veces**
y va a seguir pasando.

📌 **Y es el reparto de la sesión 43 mordiendo:** aquí el porqué del código, allá
el método. Las lecciones de método se quedaron del otro lado, el código de este,
y **las citas cruzan la frontera sin pasaporte**.

**No es que la entrada cambiara:** `git log -S` sigue a `[L-013]` hasta `499879a`
y su título es el mismo desde el primer día.

🔑 **Y la cara que faltaba nombrar:** la misma cita significaba **tres cosas
distintas** en tres sitios (*"nadie lo ha visto morder"*, *"solo vive en el
chat"*, *"un número sin corrida detrás"*). Eso ya no es un puntero roto — es
**la misma cosa escrita en varios sitios diciendo cosas contrarias**, el bicho de
la sesión 33, ahora en las citas en vez de en las reglas.

⚠️ El daño no es cosmético: quien siga el puntero desde `[D-041]` lee sobre
huecos de concurrencia buscando un argumento sobre controles sin estrenar, y
concluye **que no entendió** — no que la cita estaba mal.

#### ✅ Lo que se corrigió, y lo que de verdad lo cierra

**Trece** punteros pasados a `[LM.13]`, **cambiando el destino y no la prosa** —
las frases eran ciertas, apuntaban mal:

| archivo | dónde |
|---|---|
| `decisions.md` | `[D-041]` (índice y entrada), `[D-038]` (entrada) |
| `lessons.md` | `[L-026]`, `[L-028]`, `[L-033]` — índice y entrada las tres |
| `assumptions.md` | `[A-018]` (dos sitios) |
| `progress.md` | dos sitios |

⚠️ **`progress.md` es del `session-closer`, no mía**, y aun así se tocó. Se cruzó
la frontera a sabiendas y solo para punteros: dejar dos citas falsas justo en el
archivo que el `session-starter` lee **primero** las habría vuelto a propagar
mañana, que es el fallo entero de esta entrada.

> 🚨 **Y cruzarla abre un riesgo nuevo: este arreglo puede deshacerse SOLO.**
> Esas dos líneas viven ahora en un archivo que **escribe otro proceso**. Si un
> cierre futuro regenera esa sección arrastrando texto viejo, los dos punteros
> vuelven a `[L-013]` **sin ningún error y sin que nadie lo note** — y vuelven
> justo al archivo que más los propaga.
>
> 📌 **Las dos líneas de `progress.md` con `[LM.13]` son correcciones
> deliberadas. No se revierten.** Si un cierre las toca, se rehacen.
>
> 🔍 Se comprueba en diez segundos, y toca hacerlo **después de cada cierre** que
> reescriba esa parte. Se buscan **las dos frases**, no un número:
>
> ```bash
> grep -c "visto morder es \`\[LM\.13\]\` exacto" _persistence/progress.md   # → 1
> grep -c "Es \`\[LM\.13\]\` en versión alarma" _persistence/progress.md     # → 1
> ```
>
> 🔴 **La primera versión de este control contaba apariciones** —`grep -c
> "\[LM\.13\]"` tenía que dar exactamente 2— **y se puso rojo el mismo día, en
> el primer cierre que lo estrenó**, por un motivo legítimo: el `session-closer`
> mencionó la colisión **en prosa** al redactar su entrada, y el contador subió a
> 4. Como el control no distingue *"alguien revirtió los punteros"* de *"alguien
> escribió sobre ellos"*, **el closer reescribió su propio texto evitando nombrar
> los identificadores** para dejarlo en verde.
>
> 🚨 **Eso es el daño, y es peor que el falso rojo:** el control acabó
> **dictando cómo se escribe el archivo que vigila**, y lo que se perdió fue
> precisión — una entrada que habla de una colisión de identificadores y no puede
> nombrarlos. 🔑 **Un control con umbral exacto sobre un texto vivo convierte
> cualquier escritura legítima en una infracción**, y quien la cometa lo arreglará
> cediendo, porque el control parece la autoridad.
>
> 🔧 Por eso ahora busca **las dos frases concretas**: eso sí es la propiedad que
> importa —*esas dos afirmaciones apuntan a `[LM.13]`*— y deja escribir libremente
> alrededor. 📌 **Cuarta vez el mismo día que un control mide algo distinto de lo
> que promete** (`is-active`, el cuarto guardián, el recuento de citas, y este).
>
> 🔑 No se construye nada para vigilarlo: un guardián para esto sería el tercero
> del día y no hay con qué verlo ponerse rojo hasta que un cierre lo rompa. Queda
> escrito y con su comando, que es lo que `C-004` pide de todo lo demás.

Tres que **no** eran `LM.13` y se trataron aparte:

- `[D-040]`, *"un número sin corrida detrás"* → no es ninguna lección: es la
  **regla 6** de `CLAUDE.md`, con la que coincide palabra por palabra.
- `tests/test_config.py`, *"un control que no distingue no es un control"* → **no
  lo dice ninguna lección de ningún repo.** Corchete quitado, frase suelta.
- `[A-018]`, *"una explicación cómoda que era de memoria"* → tampoco. No es
  `LM.13` (*no se ha visto morder*) ni la regla 6 (*un número*): lo que falló fue
  una **explicación**. Corchete quitado, y anotado en su sitio.

🔑 **Una frase sin puntero es honesta; un puntero falso no.**

🔴 **Esta lista se escribió mal DOS veces, y las dos se cazaron releyéndola.**

1. La primera decía **nueve** y nombraba `[L-019]` y `[L-021]`, que no se
   tocaron. Se rehízo contra `git diff`, localizando cada línea con `awk`.
   ⚠️ El nueve **era correcto para lo mirado hasta ese momento** —faltaban por
   auditar `assumptions.md` y `progress.md`—, y eso es justo lo que lo hacía
   engañoso: un recuento parcial no se anuncia como parcial.
2. La segunda dejó **"nueve" arriba y "trece" abajo** en la misma nota, y luego
   sumó **quince** donde eran dieciséis.

📌 Anotado, y no por escrúpulo: es **esta misma lección a la tercera capa** —una
lista sobre citas sin verificar, escrita sin verificar, dentro de la entrada que
trata de eso— y el segundo fallo es literalmente **la misma cosa escrita en dos
sitios diciendo cosas distintas**, que es el bicho de la sesión 33 reproducido
dentro del párrafo que lo denuncia.

🔧 Lo que enseña, y es la parte útil: **contar es una medida, y una medida se
vuelve a correr después de cambiar el alcance.** Los tres números salieron de la
cabeza; el bueno salió de `git diff`.

📌 **Y esto tampoco es nuevo — tiene antepasado del lado del supervisor.** En la
**sesión 7 de `Edu_TripleS`, el costo estimado en vez de medido**: un docstring
anunciaba ~0,02 US$ y la corrida real dio 0,038. De ahí sale la regla 6 de
`CLAUDE.md`. Aquí reaparece contando **archivos** en lugar de midiendo **dinero**,
y por eso no se reconoció: se creyó que la regla hablaba de costes.
⚠️ **Esa lección NO tiene identificador** —vive sin numerar en la lista de
errores de `PROGRESO.md`—, así que se cita por su nombre y **no se le inventa
uno**. Inventarle un `[LM.nn]` sería fabricar exactamente el puntero falso que
esta entrada existe para arreglar.

🆕 **Lo que esta sí añade, y aquella no tenía:** el nueve **no era falso, era
parcial** — y un recuento parcial que no se anuncia como parcial engaña más que
uno equivocado, porque no hay nada en él que invite a comprobarlo.

Dos que **no** eran `LM.13` y se trataron aparte:

- `decisions.md` *"un número sin corrida detrás"* → no es ninguna lección: es la
  **regla 6** de `CLAUDE.md`, con la que coincide palabra por palabra.
- `tests/test_config.py` *"un control que no distingue no es un control"* → **no
  lo dice ninguna lección de ningún repo.** Se le quitó el corchete y la frase se
  quedó suelta. 🔑 **Una frase sin puntero es honesta; un puntero falso no.**

🔧 **Y lo que cierra esto no son las correcciones, es el prefijo.** Queda como
convención escrita en `CLAUDE.md`: **`[LM.nn]` con doble letra para el repo
supervisor, `[L-nnn]` con guion solo para este.** Con eso la colisión deja de ser
posible, en vez de irse arreglando cada vez que alguien la pilla.
📌 La convención **ya existía de hecho** —`LM.13`, `LM.15` y `LM.19` se usan bien
en 19 sitios del repo— pero **no estaba escrita, así que no protegía de nada.**
Funcionaba hasta el primer despistado, y **un acuerdo que depende de que nadie se
despiste no es un acuerdo: es una racha.**

🔑 **Y es el mismo animal que `Persistent=false`**, escrito a la fuerza en
`deploy/teapp-shutdown.timer` esa misma mañana *aunque ya sea el valor por
defecto*. Las dos veces la razón es idéntica: **lo que se cumple solo mientras
nadie lo toque no es una garantía, es una coincidencia que dura.** Se escribió en
un archivo de systemd a las 17:00 y no se reconoció en las citas a las 18:00 —
📌 la misma regla cuesta reconocerla cuando cambia de material.

---

### [L-033] 2026-08-09 — El rodeo perdió la palabra que lo hacía cierto

**Qué pasó.** `[A-017]` dejó escrito el rodeo para el DNS intermitente:
*"entrar **por SSH** usando la IP fija `32.199.55.191`"*. Al contarlo, la palabra
`SSH` se cayó dos veces:

- el 2026-08-08, en el traspaso hablado entre sesiones;
- **hoy, en el reporte de inicio de sesión**, que lo presentó como rodeo para el
  navegador: *"si no responde, entra por la IP"*.

**Por qué importa que se caiga esa palabra.** Sin ella el consejo no queda vago,
queda **falso**. Medido hoy, no citado:

| cómo entras | resultado |
|---|---|
| `https://32.199.55.191` | `000` |
| `https://32.199.55.191` con `-k` | `000` |
| `https://teapp.duckdns.org` | `200` (1 de cada 5 falla) |
| `curl --resolve` (nombre + IP a mano) | `200` |

> 🔑 **No es un aviso de certificado que se pueda aceptar en el navegador.** El
> saludo inicial ni siquiera llega a ocurrir: Caddy solo sirve el nombre para el
> que tiene certificado. Por la IP no se entra con navegador **nunca**.

El reparto correcto, y va junto:

- **SSH** → por la IP. `32.199.55.191`.
- **Navegador y `curl`** → por el nombre. Y si el DNS falla,
  `curl --resolve teapp.duckdns.org:443:32.199.55.191`.

**⚠️ Lo caro no es el `000`. Es lo que se concluye de él.** Quien mida `T-074`
mañana entrando por la IP obtiene un `000` — y ese `000` no dice *"mediste
mal"*, dice *"el redespliegue rompió algo"*. Es un instrumento equivocado que
además **acusa a otro**: se saldría a depurar Caddy, el certificado o el arranque
automático, todos sanos.

**🔧 Regla.** **Un rodeo se anota con su protocolo pegado, nunca solo con su
dirección.** Una dirección sobrevive a cualquier resumen porque parece la
información; el protocolo suena a detalle y se cae el primero.

📌 **Hermana de `[LM.13]` con una vuelta más.** Allí lo que se perdía era lo que
*solo vivía en el chat*. Aquí **sí estaba escrito**, en `[A-017]`, y se perdió
igual **al recontarlo**. O sea: estar escrito no protege del resumen. Y el sitio
donde el resumen se fabrica a diario es el **reporte de inicio de sesión**, que
es exactamente donde volvió a nacer hoy.

---

### [L-032] 2026-08-09 — El resto de una medición barata es lo que el instrumento no ve (cierre de `[A-005]` y `[A-008]`)

> 📌 **Esta entrada sustituye a `[A-005]` y `[A-008]`**, retiradas de
> `assumptions.md` el 2026-08-09 al comprobarse las dos con la misma corrida.
> Cualquier puntero antiguo a esas anclas se lee aquí.

#### Lo que ya estaba medido, y lo que quedó vivo

`[L-024]` hizo lo difícil y lo hizo gratis: correr `install.sh` **entero en un
contenedor Ubuntu**, sin EC2 y sin gastar. De ahí salió muerta la sospecha que de
verdad daba miedo — *"el guion de instalación pisa la llave de firma"*:

    dos corridas seguidas  → misma huella  7915abd41bf6
    borrando el .env       → huella distinta e3f588ea2399   ← la medida podía ponerse ROJA

Y aun así `[A-008]` siguió viva, con tres cosas pendientes. 🔑 **No eran un
descuido: eran exactamente lo que un contenedor no tiene.**

| lo que quedaba | por qué el contenedor no podía verlo |
|---|---|
| que `teapp.service` lea ese `.env` **bajo systemd** | en el contenedor no había unidad de systemd corriendo |
| que el disco sobreviva | el disco de un contenedor se evapora, es su naturaleza |
| que **una sesión viva** aguante el redespliegue | no hay navegador, ni cookie, ni nadie sentado |

Lo mismo le pasaba a `[A-005]`: el reinicio quedó medido el 08 con `T-065`, y
quedó vivo **solo el redespliegue** — que era lo que su propio criterio pedía.

#### 🏁 La corrida de hoy (`T-050`), y sus tres evidencias

`git pull` de `aff4350` a `0dfdbba`, `install.sh` en **código 0**, con la pestaña
del navegador abierta y con sesión desde antes.

| evidencia | qué prueba |
|---|---|
| huella del `.env` idéntica antes y después (`1f0365563d…`, nunca impresa entera) | el guion **no tocó la llave** |
| `data/users/jorge.json` con fecha **2026-08-08 18:25:15** y `{"score": 5}` | el redespliegue **no reescribió los datos** |
| **F5 en la pestaña ya abierta → *"Signed in as jorge"*** | **la cadena entera** |

#### 🔑 Las tres no se sustituyen, y solo la tercera prueba lo prometido

Las dos primeras miran **archivos**. Podrían salir verdes las dos con la sesión
muerta: bastaría con que `teapp.service` estuviera leyendo **otro** `.env`, o con
que el proceso hubiera arrancado con la llave vieja en memoria. Los archivos
estarían intactos y nadie podría entrar.

⚠️ **Y la promesa nunca fue sobre archivos.** `[A-008]` decía que si fallaba,
*"todas las sesiones mueren de golpe y todo el mundo queda fuera, sin ningún
error que lo delate"*. Eso solo lo desmiente **alguien que sigue dentro**.

#### 🔧 La regla

Cuando una medición barata deja un resto, **ese resto no es "lo que faltó por
hacer": es la lista de lo que ese instrumento era incapaz de ver.** Y se escribe
así, nombrando la incapacidad, en el momento de anotar el resto.

📌 Escrito de esa forma, el resto deja de parecer pereza y pasa a ser un plan: no
hay que repetir la medida barata mejor, hay que **cambiar de instrumento**. Misma
forma que `[L-031]`, donde lo que Python no podía ver era el navegador.

### [L-031] 2026-08-09 — Dónde acaba lo que Python puede probar (cierre de `[A-009]`)

> 📌 **Esta entrada sustituye a `[A-009]`**, retirada de `assumptions.md` el
> 2026-08-09 al comprobarse. Una suposición comprobada no puede vivir en los dos
> archivos: una de las dos copias acabaría mintiendo. Cualquier puntero antiguo
> a `[A-009]` se lee aquí.

**El arco entero, porque la lección está en la forma y no en el resultado:**

| fecha | qué se supo | estado |
|---|---|---|
| 2026-08-04 | La rama `secure=True` **nunca se había ejecutado**: `conftest.py` la apaga con `autouse` en los 192 tests | 🆕 hueco escrito el mismo día que el código |
| 2026-08-06 | `T-052`: cuatro tests miran la cabecera `Set-Cookie` en crudo, en los dos sitios, con sabotaje doble | 🔻 encogida, **no** muerta |
| 2026-08-09 | Navegador real por `https://`: cookie guardada **y** devuelta | ✅ **cerrada** |

#### 🔑 Por qué el testigo de Python no bastaba, y no era pesimismo

`T-052` hizo todo lo que se le podía pedir: midió el **defecto de verdad**
(borrando la variable, no poniéndola a mano), miró la cabecera **en crudo** en
vez del tarro del cliente, cubrió `_start_session` *y* el `delete_cookie` de
`/logout`, y se saboteó dos veces — resultado y montaje.

Y aun así la suposición siguió viva, con esta frase escrita en su entrada:

> *"Eso es Python hablando consigo mismo hasta que haya máquina."*

**Un test de Python prueba lo que el servidor ENVIÓ. No prueba lo que un cliente
real HACE con ello.** Son dos afirmaciones distintas, y la segunda es la que le
importa a quien entra a TEAPP.

#### 🏁 Las dos medidas del cierre — y la segunda es la que faltaba

1. **Guardada.** En `DevTools → Application → Cookies`, la cookie `session` de
   `https://teapp.duckdns.org` con `Secure ✓`, `HttpOnly ✓`, `SameSite Lax`.
2. **Devuelta.** F5 sin volver a escribir usuario ni contraseña →
   *"Signed in as jorge"*.

🔑 **No es la misma medida repetida.** `Secure` decide que la cookie se
**guarde**; `SameSite` decide cuándo se **devuelve**. Se puede tener lo primero
sin lo segundo, y el resultado sería una sesión que se pierde en cada recarga.
⚠️ **Y el fallo habría sido mudo por partida doble:** un navegador que decide no
mandar una cookie no escribe nada, ni en pantalla ni en el log del servidor. Se
vería como *"el inicio de sesión no hace nada"*.

Si solo se hubiera mirado la primera, `[A-009]` se habría dado por muerta con la
mitad del enunciado sin comprobar — y su enunciado decía, literal, *"guarde esa
cookie **y la devuelva**"*.

#### 🔧 La regla

**Un test de Python cierra "qué mandó el servidor"; no cierra "qué hace el
cliente".** Cuando la suposición habla de un cliente real —un navegador, un
teléfono, otro servicio—, la última medida la hace un humano.

📌 **Y eso no es un defecto del plan.** `T-051` estuvo bloqueada desde el
2026-08-04 esperando esta medida, y hubo la tentación de darla por buena con
`curl` sobre HTTPS real. `curl` no es un navegador: no tiene política de
`SameSite`, no descarta nada por sí mismo. Llamar medida a eso habría sido
`[L-020]` — un verde que es silencio.

### [L-030] 2026-08-09 — Un instrumento que se reinicia no es un registro

**Qué pasó.** Al entrar por SSH para programar el apagado de `[D-045]` se releyó
`uptime -s` de pasada, por costumbre. Devolvió:

    2026-08-08 18:11:15        ← hoy
    2026-08-08 15:54:27        ← lo que dice [A-018], medido ayer

Dos horas distintas para la misma máquina, sin que nadie la haya relanzado.

**Por qué.** `uptime -s` no dice cuándo **nació la instancia**: dice cuándo
**arrancó el sistema operativo la última vez**. Y ayer se reinició — es
literalmente `T-065`, la prueba de que el disco sobrevive a un `reboot`. El
instrumento hizo lo suyo; lo que estaba mal era lo que se esperaba de él.

#### 🔑 Lo que de verdad se aprendió: el número no se estropeó, se estropeó su respaldo

`2026-08-08 15:54:27` **sigue siendo correcto**. Era el primer arranque, minutos
después del lanzamiento. Lo que cambió es que **ya no se puede volver a
comprobar** con el instrumento que lo produjo.

📌 Y `[A-018]` había escrito, con todas las letras, que la ventaja de `uptime -s`
sobre la consola era que *"se relee cuando se quiera, sin abrir el navegador"*.
🚨 **Esa frase es hoy falsa**, y era el argumento por el que se prefirió ese
instrumento. El dato pasó de **medido** a **anotado** sin que nadie lo notara,
porque el número ya estaba escrito y los números escritos no piden revisión.

⚠️ **Es el error de las 15:08 con otro traje** —tomar por `t=0` una hora que no lo
era— pero es peor de cazar. Aquel se descubrió comparando dos horas que no
cuadraban. Este **solo aparece si alguien vuelve a mirar**: el instrumento no
avisa de que se ha puesto a cero, y devuelve una respuesta con la misma cara de
seguridad que la primera vez. Es `[L-020]` otra vez — el silencio disfrazado de
verde.

#### 🚨 Y `[D-045]` convierte el accidente en régimen

A partir de esta noche la máquina se apaga y se enciende **todos los días**. O
sea que `uptime -s` va a marcar *"desde que encendí hoy"* de forma permanente.

Quien mañana quiera calcular *dinero ÷ horas* y lea la máquina, dividirá el gasto
acumulado —que incluye la Elastic IP desde el 06 y el volumen desde el 08— entre
**las horas de hoy**. El resultado no es un poco alto: es una tarifa inventada.

📌 **Las horas acumuladas tienen que salir de otro sitio** — de la ventana escrita
en `[D-045]` o de la propia consola de facturación. Es trabajo de `[T-067]`, y
esta lección es parte de su enunciado.

#### 🔧 La regla

**Antes de citar un instrumento como registro, preguntar qué lo pone a cero.**

Si algo lo reinicia —un `reboot`, un despliegue, un contenedor nuevo, un fichero
de log que rota— entonces sirve para medir **ahora**, y no para fechar **el
origen**. Son dos usos distintos y el instrumento no distingue: contesta igual a
las dos preguntas.

### [L-029] 2026-08-08 — Lo que nace después del cierre no tiene dueño

- **Qué pasó.** El cierre commiteó a las `13:17:05`, con el árbol limpio y el
  control verificado. A las `13:37:41` —veinte minutos después— la conversación
  produjo `[D-044]`, una decisión con **fecha de caducidad de una noche**. El
  `session-closer` ya no existía y el commit del día ya estaba hecho: nadie era
  responsable de guardarla. Se salvó porque se siguió hablando.
- 🔑 **El mecanismo, y por qué va a repetirse.** No es un descuido de nadie: es
  estructural. El cierre corre **una vez**. Y en este proyecto las decisiones
  buenas nacen justo ahí — después de que el trabajo técnico acabó, cuando ya
  se puede pensar. **La costura está exactamente donde más se escribe.**
- ⚠️ **Por qué no se detecta al día siguiente.** Una costura **no deja hueco**.
  Al abrir sesión se lee `_persistence/` y se ve un día que terminó limpio y
  sin nada pendiente. No hay archivo a medias ni test rojo que delate la
  ausencia. Es el mismo modo de fallo mudo de `[L-031]` (antes `[A-009]`) y
  `[A-017]`, aplicado
  al protocolo en vez de al código.
- 🔧 **Regla:** lo que se escriba después del cierre **se commitea en el
  momento**, no se aplaza al cierre siguiente.
- 📌 **Y el intento de aplazarla, que es la mitad interesante.** Se estuvo a
  punto de dejar esta entrada para mañana con el argumento *"acabamos de dejar
  el árbol limpio y no me apetece ensuciarlo para contar que se ensució"*. Una
  revisión externa lo señaló: eso es **el propio hallazgo aplicándose a sí
  mismo** —aplazar al día siguiente una lección sobre el trabajo huérfano del
  día siguiente— y el argumento es estético. 🔑 **El árbol limpio no es el
  objetivo del protocolo: es su efecto secundario.** Ensuciarlo veinte segundos
  para guardar lo aprendido es el mismo intercambio que se hizo media hora
  antes con `[D-044]`, y fue el correcto las dos veces.
- ⚖️ **Lo que esta entrada NO dice, escrito a propósito.** La misma revisión
  propuso antes otra lección —*"el cierre no se comprueba con «¿hay hash?» sino
  con `git status` limpio después"*— sobre el supuesto de que el cierre había
  **omitido** `decisions.md`. Los `mtime` lo desmintieron: el archivo se
  escribió veinte minutos después, el control corrió y dio verde, y habría dado
  verde igual porque no había nada que cazar. **Esa lección se descartó por
  venir de un no-evento**, y anotarla habría envenenado el archivo. 📌 El
  síntoma era bueno (`D-044` estaba en un solo disco); la causa, no. **Acertar
  el síntoma no vuelve buena la causa.**
- ❓ **Queda una decisión de diseño abierta, sin prisa:** si el cierre debería
  poder correrse **dos veces** en un mismo día. No se decide hoy.

### [L-028] 2026-08-08 — Partir una tarea en dos deja al documento diciendo la mitad vieja

- **Qué pasó, y hasta dónde llegó.** `deploy/console_steps.md`, paso 3, punto 5,
  decía *"Elastic IP: reservarla y asociarla a la instancia"*. Se escribió cuando
  la IP no existía. El 2026-08-06 `[T-059]` se partió en dos por `[A-018]`, se
  ejecutó **solo la mitad de reservar**, y el punto 5 se quedó igual — describiendo
  un trabajo del que la mitad ya estaba hecha. 📌 **No llegó a costar dinero: lo
  cazó una revisión externa minutos antes del clic.**
- 🚨 **Lo que habría costado.** El guion se ejecuta a propósito sin decidir dentro
  de la consola (así está escrito arriba del propio archivo), así que "hacer lo que
  dice el punto 5" era el comportamiento **correcto** — y llevaba a pulsar
  `Allocate Elastic IP address`. Resultado: **una segunda dirección**, y en AWS la
  IP elástica que cobra es justo **la que no está asociada a nada**. Un goteo
  silencioso, del tipo que `[A-018]` todavía no ha visto detectar.
- 🔑 **La novedad respecto a `[L-018]` y `[L-025]`.** Aquellas hablan de copias que
  divergen **porque alguien edita una y no las otras**: el arreglo es hacer `grep`
  de las copias al cambiar un hecho. Aquí **nadie editó nada**. El documento no
  cambió; **cambió el mundo que describía**. Ninguna búsqueda de texto lo encuentra,
  porque no hay dos frases en desacuerdo — hay una frase sola, que era verdad y dejó
  de serlo.
- 🔧 **Regla que queda:** cuando una tarea se parte en dos, el mismo commit que la
  parte revisa **el guion operativo que la ejecuta**. Partir es un cambio de estado
  del mundo, no solo de `tasks.md`. La pregunta concreta: *¿algún paso escrito
  describe ahora trabajo que ya está hecho?*
- ⚠️ **Y hay una segunda mitad, del mismo día y del mismo tipo.** El aviso de no
  aceptar el `launch-wizard` del asistente —que habría dejado el **22 abierto al
  mundo** y el grupo de `T-060a` sin usar— existía **solo en la conversación**. El
  paso 3 no nombraba el cortafuegos ni una vez. Es `[LM.13]` con otro traje: **un
  freno que vive en un chat se muere al cerrar la sesión.** Los dos huecos se
  taparon escribiéndolos en el archivo **antes** de tocar la consola, no después:
  arreglar el guion mirando lo que ya pasó es escribir la crónica, no el guion.

### [L-027] 2026-08-07 — El ciego era el control, y un control ciego da permiso

- **Qué pasó:** midiendo la mitad de Caddy de `T-055`, la cadena real contestó lo
  que se quería oír — seis logins fallidos con seis orígenes falsos distintos y el
  freno saltando igual, contra el origen **real** (`172.17.0.4`).
- ✅ **Y se hizo lo correcto:** no creérselo. Antes de escribirlo se montó un
  control para **verlo fallar** — arrancar uvicorn **sin** `--proxy-headers`, que
  debería dejar a todo el mundo compartiendo el cubo de `127.0.0.1`.
- 🚨 **El control salió VERDE.** Mismo origen real, mismo resultado. Durante un
  minuto eso parecía tranquilizador: *"aguanta incluso sin las banderas"*.
- 🔑 **Y era lo contrario.** En **uvicorn 0.52.1 `--proxy-headers` ya viene puesta
  por defecto** — un dato que `[D-034]` tenía escrito desde el 2026-08-06 y que se
  olvidó justo al diseñar el control. **Quitar la bandera no apagaba nada.** El
  sabotaje no saboteaba: su verde no era una medida, era **silencio**.
- **El rojo de verdad** salió poniéndole a la bandera que sí manda un valor
  activamente equivocado — `--forwarded-allow-ips 203.0.113.5`, que excluye
  loopback. Entonces el log escribió `origen 127.0.0.1`, que es `[A-014]` en falso
  y a la vista. **Solo después la medida verde significó algo.**
- 🚨 **En qué se diferencia de `[L-020]`, y por qué es peor:**

  | | `[L-020]` | esta |
  |---|---|---|
  | quién estaba ciego | **el instrumento que medía** | **el control que autorizaba a creerse la medida** |
  | qué produce el fallo | una conclusión sin respaldo | **permiso para publicar la conclusión** |

  Un instrumento ciego da un dato flojo. Un **control** ciego da algo peor: da la
  sensación de haber hecho la comprobación. Es el sello de calidad falsificado.
- 🔧 **La regla que queda, y es concreta:** **un control se diseña contra el valor
  POR DEFECTO, no contra la bandera escrita.** Quitar una opción no la apaga si la
  librería ya la trae puesta. Para romper algo de verdad hay que darle un valor
  **activamente equivocado**, no ausente. Y antes de escribir el control:
  *¿sé cuál es el valor por defecto de lo que estoy quitando?*
- 📌 **Cuarta vez del mismo bicho en tres sesiones** — `[L-019]` (el montaje que
  medía lo contrario), `[L-020]` (el testigo que no miraba), `[L-021]` (el silencio
  leído como acusación) y esta. El patrón del proyecto ya no es "los tests
  mienten": es **verde producido por algo distinto de lo que el verde afirma**.

### [L-026] 2026-08-07 — `T-068` no es un freno: es disciplina, y la disciplina se gasta

- **Qué pasó:** al preparar el primer clic en la consola se releyó la lista de
  `T-068` —las siete puertas que cruzan al plan de pago sin vuelta atrás— y se
  cayó en algo que no estaba escrito en ninguna parte.
- 🚨 **`T-068` es el único control del proyecto ESTRUCTURALMENTE inverificable.**
  `LM.13` dice que un freno que no has visto morder es una nota, no un freno. Y
  este **no se puede ver morder nunca** — no por descuido ni por falta de tiempo:
  **probarlo ES el desastre.** Cruzar la puerta para comprobar que la puerta hace
  daño evapora los créditos y no tiene vuelta atrás.
- 🔑 **Eso no lo invalida. Lo convierte en OTRA COSA, y la diferencia importa:**

  | | freno | disciplina |
  |---|---|---|
  | ejemplo | el portero de `no_data_writes.py`, el tope de Caddy | `T-068` |
  | se ha visto morder | ✅ sí | ❌ imposible por construcción |
  | con la repetición | **no se degrada** — la máquina no se cansa | 🚨 **se degrada** |

- ⚠️ **Y el desgaste ya tiene fecha de inicio:** el experimento de `[A-018]`
  obliga a abrir *Facturación y costos* **a diario** durante semanas. Dentro de
  dos semanas esa página será rutina. **La rutina es exactamente lo que gasta la
  disciplina** — y es la misma página donde vive *"Actualizar plan"*.
- 🔑 **Lo que se hace con esto, y es lo único que se puede hacer:** no fingir que
  la lista es un freno, y **mover el riesgo de más tráfico fuera de la lista**.
  *"Actualizar plan"* deja de ser el renglón 8 de `[C-005]` y pasa a ser una línea
  del **protocolo de lectura** del experimento, donde sí se lee cada día. El
  detalle, en `[A-018]`.
- 📌 **La regla general que deja:** cuando un control no se puede verificar,
  **decirlo en voz alta y llamarlo por su nombre**. Un control inverificable
  etiquetado como "freno" da la misma calma que uno probado, y no la merece —
  es `[LM.13]` con otro traje: **verde porque no existe nada capaz de ponerlo
  rojo.**

### [L-025] 2026-08-07 — Un dato que se toca obliga a salir a buscar sus copias

- **La regla, y ya no es una nota al pie:** en este proyecto, **cambiar un dato
  no termina cuando se cambia el dato**. Termina cuando se ha hecho `grep` de su
  nombre por todo el repo y se ha mirado qué dicen las otras apariciones. Un
  hecho vive repetido en documentos, comentarios, docstrings y anclas, y **la
  copia vieja no avisa: se queda ahí, afirmando lo contrario, con la misma cara
  de verdad que la buena**.

- 🚨 **Por qué merece nombre propio: es el defecto que más veces ha vuelto.**
  Recuento sin redondear, solo del 2026-08-07:

  | dónde | qué decía la copia muerta |
  |---|---|
  | `app/config.py`, docstring de `load_env_file` | *"en la nube no hay `.env`, los pone la plataforma"* — plataforma descartada en `[D-029]`, hace dos días |
  | `app/api.py:40-42` | **la misma frase**, en otro archivo |
  | `tests/test_deploy_limits.py:103,108` | apuntaban a `[A-019]` después de que `[A-019]` muriera |
  | `_persistence/decisions.md:271` | *"esto está leído, no medido"* — ya estaba medido |
  | `deploy/Caddyfile.template` | *"falta correr `caddy adapt`"* — ya se había corrido |

  Y antes del día de hoy: las cuatro menciones de `T-068` dándola por pendiente
  con la tarea cerrada, y los casos de las sesiones 33, 41 y 50.

- 🔑 **Lo que hace tan resistente al bicho, y es lo que hay que entender.** Las
  dos primeras filas son **comentarios dentro del código que corre**, y ahí el
  daño es distinto: un documento desactualizado se lee con desconfianza, pero un
  comentario pegado a la línea que ejecuta **se lee como la explicación
  autorizada de esa línea**. Nadie duda de él porque está al lado. Ese comentario
  llevaba dos días justificando `os.environ.setdefault` con un motivo que ya no
  existía — y la regla resultó ser correcta **por otra razón** (`[D-039]`). Un
  motivo falso sostiene bien hasta el día que alguien lo comprueba.

- ⚠️ **Y el arreglo genera el bicho.** Retirar `[A-019]` de `assumptions.md`
  —el gesto correcto, *"las suposiciones se mueren ascendiendo"*— dejó **cinco
  punteros apuntando a un ancla que ya no existe**. Limpiar es una operación que
  ensucia en otro sitio. 📌 Encadena con `[L-023]`: allí el instrumento ensuciaba
  lo que medía; aquí **la corrección ensucia lo que corrige**.

- 🔧 **Qué hacer, en concreto:** después de cambiar un hecho o de retirar una
  entrada, `grep` de su ancla y de las palabras clave de la frase por
  `_persistence/`, `_context/`, `deploy/`, `app/` y `tests/`. Y las que
  pertenezcan a otro dueño —`tasks.md` y `progress.md` son del `session-closer`—
  **se dejan escritas por número de línea**, no se arreglan a medias ni se
  olvidan.

### [L-024] 2026-08-07 — "Necesita la nube" era falso: un contenedor corre el guion de verdad

- **Qué se aprendió:** que `deploy/install.sh` —escrito el 2026-08-05 y **nunca
  corrido**, con `bash -n` como única verificación— **sí se puede correr hoy**, en
  un contenedor Ubuntu, sin EC2 y sin gastar un céntimo. Once tareas estaban
  clasificadas como "piden máquina". Al menos una no la pedía.

- 🚨 **El error no fue técnico, fue de censo.** Se dio "no hay nada que hacer sin
  nube" como conclusión, y era una **suposición sobre un conjunto** que nadie
  había recorrido. Encadena con `[L-021]`: el titular era más fuerte que la
  evidencia. Y llegó acompañado de un número inventado —"las once pendientes"
  cuando el `grep` propio ya había devuelto **catorce** filas—, que es el mismo
  defecto en pequeño: **poner una cifra redonda encima de la evidencia que ya
  estaba en pantalla**.

- 🔧 **El montaje, para repetirlo.** `git ls-files` en vez de copiar la carpeta:
  el repo local lleva un `.venv` y un `node_modules` **de Windows**, y con ellos
  dentro el guion habría visto un `.venv` ya existente, se habría saltado el paso
  de Python y habría medido otra cosa. ⚠️ `MSYS_NO_PATHCONV=1` o Git Bash
  convierte `/opt/teapp` en una ruta de Windows y el `docker exec` falla mudo.

- **Hasta dónde llega y dónde se para, medido:** el guion corrió entero —`apt-get`,
  Caddy 2.11.4, `venv`, `pip`, el `.env`— y murió en `systemctl: command not
  found` (línea 223). **La parte que importaba queda ANTES de ese punto.** Lo que
  el contenedor no puede medir: systemd, el cortafuegos, el certificado real y el
  disco que persiste a un reinicio. Esos siguen siendo de EC2.

#### 🔻 Ampliada el 2026-08-07 (noveno tramo) — se le cobró un trozo más al contenedor

- 🔑 **Aplicando la propia regla de esta lección a lo que la lección dejaba fuera:**
  si el guion muere en la 223, **la sección 5 entera no se ha ejecutado nunca** —ni
  aquí ni en EC2, que no existe—. Dentro está `caddy validate` (línea 237), y un
  error de sintaxis en `Caddyfile.template` se habría descubierto **mañana, en la
  máquina, con `install.sh` abortando a mitad de despliegue**.
- ✅ **Se ejecutó a mano, con el mismo `sed` de la 232. Primera vez en la vida del
  proyecto:** `Valid configuration`, salida **0**, sin `DOMAIN_PLACEHOLDER` sin
  sustituir. Directivas efectivas: `request_body { max_size 16KB }` y
  `reverse_proxy 127.0.0.1:8000`. El validador confirmó de paso *"enabling
  automatic HTTP->HTTPS redirects"* y el 443 con política TLS.
- ⚠️ **Mide la SINTAXIS, no el comportamiento.** Que la configuración sea válida no
  dice que Caddy escriba `X-Forwarded-For` ni que el 413 llegue: eso es `T-055` y
  `T-060b`, y siguen necesitando la máquina.
- 📌 **Y se cayó de paso una suposición sobre el propio contenedor:** *"ahí dentro
  hay un aparejo de Caddy hablando con uvicorn"*. **No lo hay.** Su
  `/etc/caddy/Caddyfile` es **el de fábrica**, con `reverse_proxy` comentado —
  porque la sección 5 nunca corrió. Son **dos procesos sueltos** levantados a mano
  para medir el tope de 16 KB, no un aparejo. 🔑 Casi se le pide a ese contenedor
  una medición que no podía dar, y **habría contestado algo**.
- 🔑 **La receta del contenedor vivía solo en el scrollback de una terminal, y eso
  es lo único irrecuperable de todo esto.** Ya está escrita en `deploy/README.md`:
  `docker run -d --name teapp-test ubuntu:24.04 sleep infinity`, sin puertos y sin
  volúmenes, todo por `docker exec ... sh -c '...'`. **El contenedor es desechable;
  la receta no.**

- 🔑 **Lo que deja como regla:** *"necesita la nube"* casi nunca es cierto de la
  **tarea entera**. Es cierto de una parte, y la otra suele ser medible hoy. Es el
  mismo corte de `T-054` y `T-055` —la mitad medible y la que espera— aplicado
  esta vez al guion de despliegue completo. **Antes de escribir "bloqueada",
  preguntarse qué mitad no lo está.**

- 📌 **Y el atajo que se descartó:** se propuso un test que leyera el **texto** de
  `install.sh` y comprobara que unas líneas siguen dentro de un `if`. Habría sido
  ruidoso (rojo al renombrar una variable) y ciego donde duele (verde al cambiar
  `-f` por `-e`). 🔑 Es el material de `[L-023]`: un control que mide **la forma
  del código** en vez del comportamiento. Se descartó **porque existía la vía que
  mide de verdad**, no por gusto.

### [L-023] 2026-08-06 — El instrumento que mide puede ensuciar lo que mide

- **Qué pasó:** `[A-020]` denunciaba un camino desconocido que escribía en `data/`
  real: el 2026-08-06 a las 14:48:33 aparecieron `data/users/otronombrelargo.json`
  (`{"score": 5}`) y `data/quota/otronombrelargo.json` (`{"used": 5}`) de una
  cuenta que no existía en `data/accounts.json`. `T-072` lo resolvió. El culpable
  fue **`measure_body.py`, la báscula de `T-054`** — la propia medición del peor
  caso de bytes, escrita y ejecutada esa misma tarde.

- **La cadena, con relojes** (19:48 UTC = 14:48 local):

  | reloj | qué |
  |---|---|
  | 19:48:17.409 UTC | se escribe `measure_body.py` |
  | 19:48:32.094 UTC | se ejecuta desde la raíz de TEAPP |
  | 19:48:33.051 local | nacen los dos archivos en `data/` |
  | 19:48:33.182 UTC | la báscula imprime su tabla |

  El script termina registrando a `otronombrelargo` y recorriendo `CASES`, que
  tiene **cinco** elementos: cinco `/practice`, `{"score": 5}` y `{"used": 5}`.
  Cuadra exacto.

- **Por qué pasó — y es de manual.** La báscula **sí se acordó de desviar**. Tenía
  su línea, con comentario y todo: `accounts.ACCOUNTS_FILE = Path(_tmp) /
  "accounts.json"`, *"medir no debe tocar `data/`"*. Lo que no desvió fue
  `USERS_DIR` ni `QUOTA_DIR`. 🔑 **El aislamiento necesitaba tres desvíos y se
  acordó de uno.**

- 🔑 **Y ahí estaba la contradicción de `[A-020]`, explicada.** `otronombrelargo`
  no aparecía en `data/accounts.json` **porque `accounts.json` fue el único que sí
  se desvió**: la cuenta se creó en el temporal, el marcador y la cuota se fueron
  a los datos de verdad. La ausencia no probaba lo que parecía probar.

- ⚠️ **Y por eso mismo, una corrección al análisis que la investigó.** Ese
  análisis dedujo de la cuenta ausente que *"`/practice` nunca comprueba que la
  cuenta exista, y un script que se firme su propia cookie entra sin
  registrarse"*, y lo llamó *"la pista principal"*. **La pista apuntaba al desvío
  incompleto, no a la puerta**: el script se registró. 📌 Es `[L-021]` otra vez —
  un titular fuerte apoyado en una prueba que significaba otra cosa. La lectura
  del código (`app/api.py:554` → `_current_user`) valía por su cuenta y **se
  verificó aparte**: ver `[A-021]`.

- **No es un accidente, es un patrón.** `probe-log.json`, el otro huérfano de
  `data/users/`, sale del 2026-08-05 — otra sesión, otro día, la misma clase de
  script.

- **Qué se hace distinto:**
  1. 🚨 **Un script de medición que importe `app` desvía los TRES sitios**:
     `accounts.ACCOUNTS_FILE`, `tools.USERS_DIR` y `quota.QUOTA_DIR`. Acordarse de
     uno no es acordarse.
  2. **Y toma la huella de `data/` real antes y después**, con
     `tests/no_data_writes.py`, que ya sirve fuera de pytest. Un desvío que hay que
     recordar falla el día que se olvida; el portero delante lo caza igual.
  3. 🔑 **La regla de fondo, que es más grande que la tarea:** el acto de medir es
     código que corre, y corre **fuera** de la suite. El portero de `T-071` vive
     dentro de pytest y **no lo verá nunca**. Encadena con `[L-020]` —un
     instrumento ciego da silencio— y `[L-022]` —un `md5` dice "los bytes,
     iguales"—: esta añade que el instrumento no solo puede no ver, **puede
     ensuciar lo que mide**.
  4. ⚠️ **Y por eso importa antes de la nube:** en el servidor esa carpeta tiene
     fichas de personas de verdad, y una báscula que se acuerde de dos desvíos de
     tres las escribe sin que nadie proteste.

- 📌 **El rastro estaba en las transcripciones de la otra terminal, no en el
  historial de PowerShell** — ese archivo no se tocó desde las 07:51, así que lo
  de las 14:48 no lo tecleó nadie a mano. Vale como método para la próxima.

### [L-022] 2026-08-06 — Un `md5` no dice "todo igual", dice "los bytes, iguales"

- **Qué pasó:** para demostrar que el portero de `T-071` muerde, se quitó a
  propósito la línea del `conftest.py`. Como el sabotaje escribe en `data/` de
  verdad, se hizo copia antes y se restauró después con
  `rm -rf data && cp -r copia data`. La verificación fue huella `md5` de los
  siete archivos: idénticas antes y después. **Restauración correcta, y ningún
  dato de la aplicación se perdió.**
- **Lo que sí se destruyó:** las **fechas de modificación**. Los siete archivos
  quedaron con el mismo segundo, el de la copia de vuelta. Con ellas se fue la
  prueba física del camino de `[A-020]`, y en particular la más fuerte de todas:
  que `data/users/otronombrelargo.json` y `data/quota/otronombrelargo.json`
  llevaban **el mismo nanosegundo**, que era el argumento de que fue una petición
  a `/practice` y no alguien tocando archivos a mano.
- **Por qué pasó:** `md5` es del contenido. Es ciego al `mtime` **por
  construcción**, no por accidente. Era el instrumento correcto para *"¿se
  corrompió un dato?"* y no podía contestar *"¿se perdió la prueba?"*. Nadie hizo
  la segunda pregunta.
- 🔑 **La vuelta nueva sobre `[L-020]` y `[L-021]`:** los tres casos anteriores
  eran instrumentos **ciegos a un cambio** — `git status` sobre una carpeta
  ignorada, un test escrito contra el número equivocado. Este **vio** el cambio
  que le importaba, y fue ciego a **una dimensión entera del archivo**. Un
  archivo es contenido *y* metadatos. La frase "las huellas coinciden" suena a
  "todo igual" y significa "los bytes, iguales".
- ⚠️ **Y estrenó `[L-021]` el mismo día en que se escribió**, dentro de la
  verificación del portero que se construyó justo contra ese defecto. El titular
  *"restaurada y verificada con las mismas siete huellas"* era cierto y decía más
  de lo que la medida sostenía.
- **Qué se hace distinto, dos reglas:**
  1. 🚨 **La prueba de un defecto no puede vivir en la carpeta que el defecto
     ensucia.** Se copia a `_persistence/` —que sí va a Git— **antes** de tocar
     nada. Es lo mismo que hizo falso el `git status` de `[L-020]`, un día
     después y en la otra dirección.
  2. **Antes de restaurar por copia, preguntarse qué del original no viaja en los
     bytes:** fechas, permisos, orden, enlaces. `cp -r` no es una máquina del
     tiempo, es un duplicador de contenido.
- 📌 Consecuencia para el portero, ya escrita en su docstring: **compara
  contenido, así que un camino que reescriba un archivo con los mismos bytes le
  pasa invisible.** Hoy no importa —sumar un punto siempre cambia el número—
  pero es de la misma clase que "vive dentro de pytest" y va escrito al lado.

### [L-021] 2026-08-06 — El titular que contradice su propia salvedad

- **Qué pasó:** al analizar `T-071` se encontraron cinco marcadores en
  `data/users/` con nombres que olían a test (`otronombrelargo`, `probe-log`,
  `juan` con 13 puntos). El punto se tituló **"la trampa ya se disparó"**, y tres
  líneas más abajo el mismo texto decía *"te lo doy como sospecha fuerte, no como
  hecho medido"*. Las dos frases no pueden ser ciertas a la vez.
- **Por qué pasó:** `data/` no va a Git, así que no hay historial que consultar.
  De esa ausencia se sacó una conclusión — y encima la más llamativa. Es
  `[L-020]` con el signo cambiado: allí el silencio de `git status` se leyó como
  *"todo bien"*; aquí el silencio del historial se leyó como *"ya pasó"*.
  🔑 **La ausencia de dato no es evidencia en ninguna de las dos direcciones.**
- **Lo que dijo la medida**, hecha después: huella `md5` + fecha de los cinco
  marcadores → suite entera (328 verdes) → huella **idéntica**. La suite de hoy
  no escribe en `data/`. Y por otro camino: `conftest.py` desvía la cuota, así
  que una corrida normal de pytest **no puede** escribir en `data/quota/` —
  luego lo del 14:48 no fue pytest. La trampa estaba **armada**, no disparada.
- ⚠️ **Una salvedad correcta no arregla un titular falso.** La salvedad estaba
  bien escrita y no sirvió de nada: nadie recuerda la letra pequeña de un
  epígrafe en negrita. Si la salvedad y el titular discrepan, **el que se
  cambia es el titular**, no al revés.
- **Qué se hace distinto:** un titular afirma lo que se midió. Si hace falta una
  salvedad para que el titular sea honesto, el titular está mal escrito. Y lo
  que se sospecha se titula como sospecha — "hay marcadores sin explicar",
  no "la trampa ya se disparó".

### [L-020] 2026-08-06 — El testigo ciego, y el animal que ya tiene nombre

- **Qué pasó:** al cerrar `T-054` se escribió *"verifiqué con `git status` que
  `data/` quedó intacto"*. **`data/` está en `.gitignore`, línea 18.** `git
  status` no la mira y no la puede mirar: habría dicho exactamente lo mismo si
  los tests hubieran escrito dentro.
- ⚠️ **El testigo no se equivocó — no estaba mirando.** Y esa diferencia importa:
  un instrumento equivocado da un dato falso, que se puede contradecir. Un
  instrumento ciego da **silencio**, y el silencio se lee como confirmación. Es
  `[L-016]` otra vez ("el silencio de una fuente no es un dato"), pero aplicado a
  una herramienta en vez de a una documentación.
- **La conclusión era correcta**, y se comprobó después por el camino que sí ve:
  las fechas de `data/users/*.json`. El más nuevo era de las 14:48, la corrida de
  la suite fue a las ~20:00. El `fixture` funciona. 🔑 **Pero se supo por suerte,
  no por la prueba que se citó.**
- **La regla que queda:** antes de citar una prueba, preguntar **si el
  instrumento puede ver el fallo que se está descartando**. Aquí bastaba con
  saber que la carpeta está ignorada — y está escrito en `.gitignore`, que es un
  archivo de este repo.
- 📌 **Los instrumentos que sí ven `data/`**, para la próxima vez:
  - `git check-ignore -v data/…` → contesta **por qué** está ignorada, con
    archivo y línea. Es el que convierte "creo que git no la mira" en un dato.
  - `git status --porcelain --ignored` → lista también lo ignorado.
  - las **fechas de modificación** de los archivos, que es lo que se usó aquí.
  ⚠️ Ninguno de los tres es más difícil que el que se citó. **No falló el
  esfuerzo: falló no preguntarse qué mira cada herramienta.**

#### 🚨 Y esto ya no es un caso suelto: es EL modo de fallo de este proyecto

**Un verde producido por algo distinto de lo que el verde afirma.** Tres veces en
dos sesiones, y cada vez con una cara nueva:

| dónde | el verde decía | lo que de verdad lo producía |
|---|---|---|
| `[L-019]` | "uvicorn ignora al suplantador" | la petición entraba **como Caddy**, por `127.0.0.1` |
| `[D-035]` | "cabe bajo el tope de Caddy" | se habría medido contra **16384**, y Caddy corta en 16000 |
| aquí | "los tests no tocaron `data/`" | `git status` **no mira** `data/` |

Y más atrás está el mismo animal: `[L-017]` (un `is-active` que declaraba
"funcionando"), `[L-015]` (un fixture que creía limpiar), `[L-012]` (un
`at_level` que pintaba de verde un renglón inexistente), `[L-011]` (un control
que parcheaba un nombre distinto del que se usaba).

🔑 **Ninguno de estos se descubre mirando el verde: solo se descubren
preguntando qué lo produce.** De ahí sale el hábito que ya es de la casa —
sabotear el montaje además del resultado (`[L-019]`)— y su ampliación de hoy:
**sabotear también en la dirección para la que el control se escribió.** Los
cuatro sabotajes de `[D-035]` atacaban el instrumento; el que faltaba —subir
`MAX_SENTENCE_LENGTH` a 5000— era el único que atacaba el escenario que el test
decía existir para cazar. Lo aportó la auditoría, no quien escribió el test.

### [L-019] 2026-08-06 — El sabotaje llegaba disfrazado de aquello que quería atacar

- **Qué pasó:** para medir `[A-014]` se montaron cuatro escenarios contra un
  uvicorn de verdad. El cuarto era el importante: fingir ser **alguien que no es
  Caddy** mandando un `X-Forwarded-For` inventado, para ver que uvicorn lo
  ignoraba. Se hizo hablándole por `127.0.0.2`, dando por supuesto que esa
  dirección no estaría en la lista de confianza. Salió **rojo**: uvicorn se creyó
  la cabecera.
- **Por qué pasó:** el rojo no era de uvicorn, era del montaje. Windows usa
  **`127.0.0.1` como dirección de origen** aunque el destino sea `127.0.0.2`
  (medido aparte, con dos sockets). Así que la petición llegaba desde la
  dirección de confianza: el escenario que decía *"esto lo manda un extraño"*
  entraba **por la puerta de Caddy**. Medía lo contrario de lo que anunciaba.
- 🔑 **Lo que lo hace grave es la simetría.** Aquí el error se delató porque el
  resultado salió rojo y el rojo pedía explicación. Pero el mismo montaje
  equivocado, aplicado a cualquiera de los otros tres escenarios, habría salido
  **verde por la razón falsa** — y `T-055` se habría dado por cerrada sobre una
  medición que no midió nada. Es `[L-007]` otra vez, con el signo cambiado: allí
  el control medía de más, aquí el escenario mentía sobre desde dónde llamaba.
- **Qué se hace distinto:** de un sabotaje se verifica **el montaje, no solo el
  resultado**. Antes de creerse el veredicto, comprobar por separado que la
  condición que el escenario dice reproducir se está reproduciendo de verdad —
  aquí, preguntarle al sistema qué dirección de origen ve, en vez de deducirla
  del destino al que se marcó.

### [L-018] 2026-08-06 — Los datos se replican solos, y corregir uno no corrige los demás

- **Qué pasó:** una frase falsa —*"si no llega correo, la alarma está bien
  montada"*— se corrigió al encontrarla. Al ir a buscarla en serio, estaba en
  **cinco** sitios: la entrada `[S-019]`, su fila de índice y el "Estado actual"
  de `progress.md`; dos puntos distintos de `[A-018]`; y un párrafo de
  `deploy/console_steps.md`. Corregir el primero habría dejado cuatro mintiendo.
- 🚨 **Y es la tercera vez con el mismo bicho:** sesión 33 (el repo dado por
  "privado"), sesión 41 (lo mismo otra vez), y esta. **Tres veces deja de ser
  casualidad y pasa a ser una propiedad del proyecto.**
- 🔑 **Por qué pasa aquí y no es descuido:** el formato de `_persistence/`
  **obliga a duplicar por diseño** — cada hecho vive en la entrada *y* en su fila
  de índice, porque el índice existe para no leer el archivo entero. Y `deploy/`
  vuelve a contar lo mismo en clave operativa, porque quien está en la consola no
  va a abrir `assumptions.md`. La redundancia es útil; **el precio es que un error
  nace multiplicado.**
- ✅ **La regla que queda:** al corregir un hecho, **no se edita donde se
  encontró: se va a buscar dónde más vive.** Un `grep` de la frase antes de dar
  la corrección por hecha.
- ⚠️ **Y la asimetría que lo hace peligroso:** escribir en dos sitios cuesta el
  doble, pero **corregir en uno solo cuesta cero y parece terminado.** Por eso el
  fallo no se siente como fallo mientras se comete.
- 📌 **Corolario aplicado el mismo día:** la tabla de lectura del experimento de
  `[A-018]` se escribió **en un solo sitio**, y `console_steps.md` la referencia
  en vez de copiarla. Documentar el problema de las copias haciendo una copia
  habría sido la sexta.

### [L-017] 2026-08-05 — El comentario correcto que sirvió de coartada

- **Qué pasó:** el bloque de comprobación final de `deploy/install.sh` llevaba
  escrito, textualmente, *"PI-4: terminado = visto funcionando. Un guion que
  acaba sin error no demuestra que la app conteste — solo que el guion acabó."*
  Y lo único que hacía dos líneas más abajo era `systemctl is-active` de los dos
  servicios.
- **Por qué eso no comprueba lo que dice:** `is-active` demuestra que **systemd
  lanzó el proceso**, no que la app conteste. Y el hueco es alcanzable, no
  teórico:

      uvicorn arranca → medio segundo después `require_secret` revienta porque
      `ubuntu` no puede leer el `.env` → `Restart=always` lo relanza → y
      `systemctl restart` ya había vuelto, así que `is-active` lo ve `active`

  El guion habría impreso **"Listo. TEAPP corriendo en https://..."** sobre una
  app muerta. Una afirmación que nunca se comprobó.
- 🔑 **Lo que hay que llevarse, y es lo incómodo:** el comentario **no evitó** el
  fallo — **lo escondió.** Un bloque que se declara a sí mismo auditado es un
  bloque que nadie vuelve a auditar. Saber enunciar el principio y cumplirlo son
  dos habilidades distintas, y la primera **disfraza** la ausencia de la segunda.
- 📌 **Y es la misma familia de la sesión de `[L-006]`**, donde el cierre se
  cumplió entero y el trabajo se quedó sin subir: el procedimiento se recitó
  completo y el resultado no se miró. Aquí, otra vez: **el principio citado, el
  efecto sin medir.**
- **Cómo se arregló:** tres comprobaciones en vez de una, porque prueban cosas
  distintas — `is-active` (systemd lo lanzó), `curl` a `127.0.0.1:8000` (la app
  contesta) y `curl` al dominio (se llega desde fuera, con certificado). Y el
  mensaje final cambió de *"Listo, TEAPP corriendo en…"* a **"Comprobado: TEAPP
  contesta en…"**. 🔑 **Ese cambio de verbo es el arreglo de verdad; los `curl`
  son solo cómo se consigue.**
- ⚠️ **La regla práctica que deja:** cuando un comentario prometa que algo está
  comprobado, **leer lo de debajo con MÁS desconfianza, no con menos.** Es donde
  menos ojos van a mirar.
- 🔑 **Y el arreglo trajo la misma criatura con el signo cambiado**, que es lo
  que convierte esto en una lección general y no en una anécdota. Al añadir los
  dos `curl` se le dieron **10 reintentos al que tarda segundos** (arrancar
  uvicorn) y **ninguno al que tarda minutos** (que Let's Encrypt emita el
  certificado). El primero decía verde sin haber mirado; el segundo habría dicho
  **rojo por haber mirado demasiado pronto**.

  > 🚨 **Las dos veces el control no medía lo que su nombre promete.** Un falso
  > verde y un falso rojo no son errores opuestos: son el mismo error —no haber
  > pensado *cuándo* es válido preguntar— y por eso el segundo se coló mientras
  > se arreglaba el primero.

- 📌 **Y un tercer filo del mismo cuchillo, en el mismo bloque:** la ruta del
  `curl` es `/` **porque entrega `index.html` sin pedir sesión**. Apuntarlo a
  `/me` —que suena más representativo— daría 401, `curl -f` lo tomaría por
  fallo, y **cada instalación se pararía en rojo estando todo bien**. Quedó
  escrito en el guion para que nadie lo "mejore": un control que se pone rojo
  por el motivo equivocado es un control verde disfrazado.

### [L-016] 2026-08-05 — El mismo error dos veces, un piso más abajo cada vez

> 🔑 **Las dos mitades van juntas a propósito.** No son dos lecciones parecidas:
> es la misma, y la segunda se cometió **corrigiendo la primera**. Separarlas
> escondería justo lo que hay que ver.

**Primera mitad — la lista supuesta tenía tres de siete**

- **Qué pasó:** `[C-005]` nació con tres puertas al plan de pago —Organization,
  Control Tower, Partner Network— y una nota al margen que decía *"la FAQ
  menciona algún caso más"*. Al leer las fuentes enteras aparecieron **siete**.
  Las cuatro que faltaban: contrato de **Professional Services**, **Enterprise
  Agreement**, suscripción **Skill Builder Team**, y marcar la cuenta **HIPAA o
  SEC compliant**.
- 🔑 **Por qué se coló:** las tres conocidas formaban una familia coherente
  —"cosas de empresa grande organizando cuentas"— y esa coherencia se leyó como
  completitud. **Una lista que tiene sentido parece terminada.** Las que faltaban
  venían de familias distintas (formación, cumplimiento normativo) y por eso no
  se echaban de menos: **para notar que falta algo hay que haberlo imaginado.**
- 🚨 **El aviso estaba escrito.** La propia entrada decía *"menciona algún caso
  más"* y aun así se siguió adelante — familia de `[L-012]`, donde el límite
  también estaba anotado antes de cruzarlo. **Una nota que dice "puede que falte
  algo" es una tarea, no un descargo de responsabilidad.**
- **Qué lo salvó:** que la mitad floja se escribiera **aparte**, como `[A-016]`,
  en vez de enterrada dentro de `[C-005]`. Una suposición con nombre propio se
  puede poner como bloqueante de una tarea; una frase en medio de un párrafo, no.
  Es `[L-014]` desde el otro lado.

**Segunda mitad — y al corregirla se cayó en lo mismo**

- **Qué pasó:** con las siete puertas ya verificadas, se escribió que las dos
  primeras evaporan los créditos **y las otras cinco los conservan**. La
  documentación **no dice eso**. Solo se moja con las dos primeras; de las cinco
  restantes no dice ni que se salvan ni que se pierden. La frase de "los créditos
  se aplican a facturas futuras" existe, pero es del **upgrade manual**, y se le
  pegó al caso equivocado.
- 🔑 **Por qué se coló, que es la primera mitad un piso más abajo:** **un
  documento que no dice "no" parece que dice "sí".** El silencio de una fuente se
  leyó como respuesta favorable — y encima la favorable, que es la que menos se
  audita. 🚨 **El silencio de una fuente no es un dato. Es un silencio.**
- 📌 **Y una trampa de método que venía dentro:** se escribió *"las tres fuentes
  repiten la misma frase"*. Cierto **para la lista de siete**; falso para los
  créditos — los Términos, que son la fuente que manda porque es la que se firma,
  solo hablan de Organizations, ni mencionan Control Tower, y con palabras
  peores. **Tres fuentes que coinciden en el párrafo A no coinciden
  automáticamente en el párrafo B: la coincidencia se verifica por afirmación,
  no por documento.**
- **Cómo se arregló:** las cinco desconocidas se marcan ❓ y **se tratan como si
  evaporaran**. Es `PERMISOS.get(nombre, "prohibir")` aplicado a una fuente en
  vez de a un usuario: sin dato, se asume lo caro, para que el olvido falle hacia
  el lado seguro.

**Lo común, que es lo que hay que llevarse**

- 🔑 **Las dos veces el hecho no salió del texto: salió de la FORMA del texto.**
  De que la lista *pareciera* cerrada, y de que el silencio *pareciera*
  permiso. Ninguna de las dos cosas estaba escrita en ningún sitio.
- **El coste de las dos:** unas lecturas y una corrección. Comparado con lo que
  protegían —la única ventana de 6 meses de `[C-006]`, que no se repite— barato
  hasta el ridículo.

### [L-015] 2026-08-04 — El fixture que creía limpiar y no limpiaba

- **Qué pasó:** `T-033` configura el log, y hacía falta un test que midiera eso
  **sin usar `caplog`** — porque `caplog` es justo la herramienta que miente
  sobre esta pregunta ([L-012]). Se escribió un fixture que vaciaba los handlers
  del logger raíz para dejarlo como en un servidor recién arrancado. Tres de los
  cinco tests salieron rojos con un mensaje revelador: los handlers **estaban
  ahí otra vez**, y eran `LogCaptureHandler`.
- **Por qué pasó:** pytest instala el handler de `caplog` **alrededor de la fase
  de ejecución del test**, o sea **después** de que corran los fixtures. El
  fixture vaciaba, pytest volvía a llenar, y para cuando corría el cuerpo del
  test el raíz tenía handlers otra vez. Y `logging.basicConfig` **no hace nada si
  el raíz ya tiene handlers**: la función que se quería medir se salía por la
  primera línea sin hacer nada.
- 🚨 **Lo que lo hace grave no es el fallo, es dónde estaba.** Ese test era el
  arreglo de [L-012] — el test cuyo trabajo era impedir que un renglón se
  aprobara a sí mismo. Y reproducía el mismo defecto: **medía el estado que había
  puesto el framework y lo llamaba "lo que hace `configure_logging`"**.
  > Si el fixture hubiera "funcionado" en silencio, habría quedado un test verde
  > vigilando exactamente nada, en el sitio donde más falta hacía uno de verdad.
- 🔑 **Por qué se vio a tiempo, y esto es lo que hay que repetir:** porque el test
  se puso rojo **por su cuenta**, no porque alguien sospechara. Al lado del test
  del estado bueno se escribió el del estado malo —*sin configurar, `info` no
  pasa*—, y ese par es lo que delata a un fixture que no hace su trabajo. Un test
  que solo mira el estado bueno no distingue *"lo arreglé"* de *"esto ya estaba
  así"*.
- **Cómo se arregló:** midiendo en **otro proceso**. Un intérprete recién
  arrancado es la única condición honesta, porque es exactamente la de uvicorn:
  raíz limpia, nada configurado, nadie escuchando. `subprocess.run` con
  `sys.executable`, sin red, sin instalar nada — [C-001] sigue en pie.
- **Qué se hace distinto:** cuando un test necesite **quitar** algo que el
  framework pone, no basta con quitarlo en un fixture: hay que comprobar que
  sigue quitado **dentro del cuerpo del test**. Y si el framework lo repone,
  medir fuera del framework.
  🔑 La regla corta: **cuando lo que quieres medir es "cómo arranca esto de
  cero", arráncalo de cero.**

### [L-014] 2026-08-04 — Una suposición que dice qué la mata se muere sola cuando toca

- **Qué pasó:** al terminar `T-053`, `[A-012]` —*"nadie prueba contraseñas a la
  fuerza contra `/login`"*— dejó de ser cierta y de ser necesaria a la vez.
  Retirarla no costó ninguna discusión: la propia entrada decía **de qué dependía
  y qué la mataría**, así que solo hubo que mirar si eso ya había pasado.
- **Por qué pasó:** porque estaba escrita con fecha de caducidad **atada a un
  hecho concreto** —*"el día que la app tenga una URL pública"*, *"hoy no hay
  tope de intentos"*— y no a un vago "más adelante". 🔑 **Una suposición con
  condición de cierre se comprueba; una sin ella se opina**, y lo que se opina no
  se retira nunca: se queda ahí envejeciendo y mintiendo.
- **La otra mitad, que no se esperaba:** al ir a retirarla se vio que `A-012` no
  era **una** suposición sino **dos pegadas**, y que solo una se había resuelto.
  - Lo que `T-053` resolvió: que no hubiera freno. Eso ya no se supone.
  - Lo que quedó vivo: que **los números del freno sean los correctos**
    (`[A-013]`), y que **el origen que lee el servidor sea el origen real**
    (`[A-014]`). Lo segundo caduca el mismo día que caducaba `A-012`.
  - 🚨 Y `[D-026]` **no** las sustituye. Una decisión guarda lo que se eligió y
    por qué; una suposición guarda **lo que se está dando por cierto sin
    comprobar**. Meter lo segundo dentro de lo primero lo esconde: `decisions.md`
    no es la lista que uno repasa buscando qué puede estar mal.
- **Qué se hace distinto:** al escribir una suposición, decir **qué hecho
  concreto la mata**. Y al retirarla, no darla por muerta entera: preguntar qué
  parte se resolvió y qué parte solo cambió de nombre. Lo que sigue sin
  comprobarse se queda en `assumptions.md`, aunque la entrada vieja se vaya.

### [L-013] 2026-08-04 — Cerrar un hueco no cierra los demás

- **Qué pasó:** los frenos del paso 6 se escribieron con mucho cuidado puesto en
  **un** hueco: el que hay entre leer el contador y escribirlo. Ese se cerró con
  candado, se probó con 50 hilos y se demostró que sin candado se rompía.
  Con 247 tests en verde, dos sabotajes encontraron **otros cuatro huecos** —y
  ninguno se parecía al primero.
- 🔑 **La lección, y es la que vale para lo que venga:** un hueco cerrado
  entrena la vista para ese hueco, no para los demás. Los otros cuatro no se
  vieron **porque no tenían la forma del que ya conocía**.

  | hueco | entre qué y qué | qué costaba |
  |---|---|---|
  | el conocido | leer el contador y escribirlo | prácticas gratis, ya cerrado |
  | 1 | preguntar el día y volver a preguntarlo | cuota regalada en la medianoche |
  | 2 | encolar el trabajo y empezarlo | cobrar por trabajo que nadie empezó |
  | 3 | contestar el 504 y terminar el trabajo | el marcador sube sin nadie mirando |
  | 4 | acabar un test y acabar sus hilos | un test contó puntos de otro |

- **Hueco 1 — la medianoche.** `spend` preguntaba **dos veces** qué día era: una
  para sí y otra dentro de `read_usage`. Entre las dos cabe la medianoche.
  Cuando cabía, comprobaba contra el día **nuevo** —limpio, así que pasaba— y
  escribía bajo el día **viejo**, borrando lo gastado. Cuota gratis, una vez al
  día, y precisamente a quien esté practicando a esa hora.
  🔑 **El comentario del código defendía justo lo contrario de lo que el código
  hacía.** Arreglado preguntando el día UNA vez y pasándolo hacia dentro.
- **Hueco 2 — la cola.** `result(timeout=)` cuenta desde que se **llama**, no
  desde que la tarea **arranca**. Con el pool lleno, el tiempo de cola se le
  cobraba a quien esperaba en ella. Medido: 23 peticiones a la vez contra un
  pool de 20 → 20 llegaron al tutor y **3 pagaron un 504 por nada**.
  ⚠️ Y el pool no tenía tamaño escrito: `ThreadPoolExecutor()` lo saca de las
  CPUs de la máquina —20 aquí, otro en la nube—. **Un freno cuyo tamaño depende
  de dónde corra no se puede razonar.** Ahora el tamaño está escrito (40) y
  `future.cancel()` distingue lo que empezó de lo que no: lo que no empezó se
  devuelve.
  🔑 Eso no contradice *"se cobra el intento"*: **lo completa**. Se cobra por
  intentar porque intentar cuesta; una petición que nunca salió de la cola no
  intentó nada.
- **Hueco 3 — después del 504.** El tutor sigue corriendo y acaba llamando a
  `add_point`: el marcador sube cuando quien preguntó ya se fue con un error.
  **Se decidió dejarlo** —el marcador cuenta frases practicadas ([A-001]), y esa
  se practicó— pero lo que cambia es que ahora está **escrito y con test**, no
  descubriéndose el día que alguien pregunte por qué le subió el número.
- **Hueco 4 — el que apareció al arreglar los otros.** El test del hueco 3 falló
  con `['juan', 'juan']`: dos puntos donde solo hubo una práctica. Eran hilos
  colgados de tests anteriores despertando **dentro** de este y llamando a su
  `add_point`. 🔑 Es la limitación del propio freno —un hilo no se puede matar—
  mordiendo dentro de la suite. Arreglado dándole a cada test lento su propio
  pool y esperándolo con `shutdown(wait=True)`.
- **Y lo que enseña sobre el verde:** los 247 tests no vieron ninguno de los
  cuatro, y no por descuido — cada uno probaba bien lo que decía probar. Es
  [L-003] otra vez, con más tests: **el verde mide lo que se te ocurrió
  preguntar.** Lo que no se te ocurrió no sale rojo, sale ausente.
- 🔑 **El remate, y es media lección más: se arregló el número y quedó heredada
  la RAZÓN del número.** Escribir `TUTOR_POOL_SIZE = 40` quitó la dependencia de
  las CPUs de la máquina. Pero el 40 solo es correcto porque el limitador de
  hilos de `anyio` —el que usa FastAPI para las rutas `def`— trae 40 fichas por
  defecto. Y `anyio` **ni siquiera está fijado**: entra de rebote con `fastapi`.
  Una subida de FastAPI podía romper el invariante *"la cola nunca es el cuello
  de botella"* **sin que nadie tocara una línea de este proyecto**, y con él
  volvía el cobro por espera del hueco 2.
  Cerrado con un test que compara los dos números, medido en los dos sentidos:
  verde con `anyio` en 40, rojo simulándolo en 15.
  > **Un invariante que depende del valor por defecto de otro necesita quien lo
  > vigile, no un comentario que lo explique.**
  Es [D-022] otra vez —un vigía sin quien lo vigile no demuestra nada— aplicado
  a una suposición prestada en vez de a un portero.

### [L-012] 2026-08-04 — El límite estaba escrito, y aun así se cruzó

- **Qué pasó:** el cuarto freno del paso 6 es *"registrar por qué se frenó"*. Se
  escribió `logger.info("Cuota agotada: ...")` en `app/api.py`, y su test pasó.
  Con uvicorn de verdad: **20 frenazos seguidos y cero líneas en el log.**
- **Por qué:** nadie ha configurado el log todavía ([T-033]), así que actúa el
  handler de último recurso de Python, **que empieza en WARNING**. Se midió:
  `logger.getEffectiveLevel()` devuelve `WARNING`, y `isEnabledFor(INFO)`
  devuelve `False`. Un `info` no se pierde por poco: no existe.
- 🔑 **Lo primero, y es lo incómodo: esto ya estaba escrito.** `[A-003]` lo decía
  con estas palabras desde el 2 de agosto — *"Solo sale WARNING o peor. Un
  `logger.info(...)` se pierde en silencio."* No fue un límite desconocido. Fue
  un límite **conocido, anotado, y cruzado igual**.
  ⚠️ [L-011] cerraba con *"un límite sabido y no escrito es un límite que alguien
  va a cruzar"*. Esta lección es la corrección de aquella: **escribirlo no
  basta.** Un límite que solo vive en un `.md` no frena a nadie en el momento de
  teclear. Lo único que lo frena es algo que se ponga rojo.
- 🔑 **Lo segundo, que es lo que enseña de verdad: el test tapó el agujero
  activamente.** `caplog.at_level(logging.INFO)` **baja el listón del logger para
  ese test**. O sea que el test creaba las condiciones que hacían visible el
  renglón, y luego comprobaba que era visible. Se aprobaba a sí mismo.
  > No medía *"¿se ve esto?"*. Medía *"¿se vería esto si el log estuviera
  > configurado?"* — y respondía que sí a una pregunta que nadie hizo.
- **Familia:** es [L-004] con otra ropa —una prueba que el código roto también
  pasa— y prima de [L-031] (antes [A-009]), donde la suite apaga `Secure` para poder trabajar y
  al apagarlo deja de mirar el otro lado. 🔑 **En los tres casos el fallo no está
  en lo que el test afirma, sino en la condición que el propio test cambia para
  poder afirmarlo.**
- **Cómo se arregló:** el renglón pasa a `logger.warning`, que es el nivel más
  bajo que hoy se ve de verdad, y el test pide `caplog.at_level(WARNING)` — el
  nivel que el servidor tiene, no uno prestado. Comprobado con uvicorn: el
  renglón sale. Cuando [T-033] configure el log, vuelve a `info`.
- **Y lo que cierra `[A-003]`:** dejó de ser una suposición porque se midió. Sale
  de `assumptions.md` y llega aquí. ⚠️ La tarea que la resuelve, [T-033], **sigue
  pendiente** — lo que se acabó es la duda, no el trabajo.

> ⏩ **Continúa el 2026-08-04.** [T-033] se hizo ([D-028]): el log ya está
> configurado, `info` se ve de verdad, y este renglón —el de la cuota— volvió a
> `info`. El "sigue pendiente" de arriba ya no lo está.
>
> 🚨 **Y esta lección se repitió dentro de su propio arreglo, que es lo que hay
> que leer antes de tocar nada de esto: [L-015].** El test escrito para que un
> renglón no se aprobara a sí mismo medía el estado que ponía pytest y lo llamaba
> "lo que hace la función". La forma de esta trampa no es "usar `caplog` mal":
> es **cambiar la condición que hace verdad lo que vas a afirmar**, y tiene más
> disfraces de los que parece.

### [L-011] 2026-08-04 — El portero tenía una puerta de atrás, y su control no la veía

- **Qué pasó:** el portero de red bloqueaba `socket.connect` y `getaddrinfo`, y
  sus dos controles se ponían rojos como debían. Parecía terminado. La revisión
  externa probó `socket().connect_ex(('example.com', 80))` con el portero puesto
  y devolvió **`0`**: conectó. El portero estaba abierto de par en par.
- **Por qué se coló:** `connect_ex` hace lo mismo que `connect`, pero **devuelve
  un código de error en vez de lanzarlo**. Es la misma puerta con otra manija, y
  yo solo había cerrado la que conocía.
- 🔑 **Lo segundo, que es lo que enseña.** Al parchear `connect_ex` escribí el
  control con un **nombre** (`example.com`). Se puso rojo. Pero un nombre pasa
  primero por `getaddrinfo`, **que ya estaba parcheado desde antes**: ese rojo lo
  producía el parche viejo, y habría salido igual de rojo con el parche nuevo
  vacío. **El control no medía lo que decía medir.** Se separó con una IP literal
  (`1.1.1.1`), que no pasa por resolución de nombres: `0` sin portero,
  `NetworkTouched` con él. Recién ahí quedó demostrado.
- **Lo que se aprendió:** un control tiene que poder **fallar por una sola
  razón**. Si dos protecciones distintas producen el mismo rojo, el rojo no dice
  cuál de las dos funcionó — y una de ellas puede estar muerta sin que nadie se
  entere. Es [L-007] visto desde el otro lado: allí un control medía de más y
  gritaba con el código sano; aquí medía de más y **callaba el hueco**.
- **Y una tercera, del tamaño de la anterior:** el portero no ve los subprocesos
  (`node`, `git`), y no los verá nunca — son otro proceso. Eso no se arregla, se
  **escribe**: quedó en el docstring del portero y en la mitad "a mano" de
  [C-001]. 🔑 Un límite sabido y no escrito es un límite que alguien va a cruzar
  creyendo que estaba cubierto.

### [L-010] 2026-08-04 — 191 tests en verde y el servidor de verdad reventaba en `/logout`

- **Qué pasó:** `/logout` estaba escrito así —`def logout(response: Response) ->
  Response:` … `return response`—, devolviendo el objeto que FastAPI inyecta. La
  suite entera pasaba, incluido `test_logout_ends_the_session`. Al correrlo con
  uvicorn de verdad: `curl` devolvió **HTTP 000** y el log del servidor,
  `KeyError: None` en `STATUS_PHRASES[status]`. El `Response` inyectado nace con
  `status_code = None`, y uvicorn no tiene nombre para el código `None`.
- **Por qué la suite no lo vio.** Dos motivos que se sumaron, y el segundo es el
  que enseña:
  - `TestClient` no habla por HTTP: no pasa por `h11`, que es donde estaba la
    línea que reventaba. **El servidor de mentira era más tolerante que el de
    verdad.**
  - 🔑 **El test miraba el EFECTO, no la RESPUESTA.** Comprobaba que después de
    `/logout` la sesión estaba cerrada —y lo estaba, la cookie se borraba
    igual—, así que pasaba mientras la respuesta era inservible. Un test que
    solo mira consecuencias da por bueno cualquier camino que llegue ahí.
- **Lo que se aprendió:** *"terminado = visto funcionando"* (PI-4) no es una
  formalidad que se cumple después de tener los tests verdes. 🔑 **Los tests y la
  corrida real no miden lo mismo, así que uno no sustituye al otro.** Y es la
  tercera vez que este proyecto lo aprende: [L-003] (45 tests no vieron un fallo
  en 7 de cada 10 peticiones), [L-004] (una prueba que el código roto también
  pasa) y ahora esta.
- **El arreglo, y el test que faltaba:** se toca la cookie en el `response`
  inyectado y se devuelve `None`; FastAPI arma la respuesta con el 204 declarado.
  Y se añadió `test_logout_answers_the_status_code_it_declares`, que mira el
  código de estado y no solo lo que pasó después.
- **Toca:** `app/api.py` (`logout`), `tests/test_api.py`, y cualquier ruta futura
  que devuelva el `Response` inyectado en vez de dejar que FastAPI lo arme.

### [L-009] 2026-08-04 — Una regla que vive en dos archivos se corrige en los dos, o no se corrigió

- **Qué pasó:** al arreglar T-049 había que dejar escrito que el resultado del
  push no cabe en `tasks.md`, y que **el arranque de mañana lo recoge leyendo
  `git status -sb`**. La frase sonaba completa. Al ir a comprobarla,
  `protocol-start` no leía `-sb`: leía **`git status --short`**.
- **Medido aquí el 2026-08-04**, en un repo de prueba con un commit sin subir a
  propósito:

  ```
  === git status --short ===
  [vacío — no vio nada]

  === git status -sb ===
  ## main...origin/main [ahead 1]
  ```

  `--short` **no imprime la línea de la rama**. Los dos comandos listan los
  archivos sueltos, y por eso se parecen; solo uno dice si el trabajo llegó a
  `origin`.
- **Qué habría pasado sin comprobarlo:** el cierre se ejecuta entero, todo en
  verde, la nota dice "esto lo recoge mañana el arranque" — y mañana el arranque
  no ve nada, porque el repo le parece limpio. 🔑 **Una promesa escrita en un
  archivo que otro archivo tiene que cumplir no vale nada hasta que se abre el
  otro archivo.**
- **Por qué es [L-006] otra vez, y por eso duele:** L-006 fue "el cierre se
  cumplió entero y el trabajo se quedó sin subir". Este arreglo iba a reconstruir
  exactamente ese fallo, esta vez con la red de seguridad escrita y rota. La forma
  de la trampa es la misma: **algo que parece cubierto porque está escrito.**
- **La regla que queda:** cuando corrijas una regla, **pregunta quién más la
  dice**. Si la corrección se apoya en el comportamiento de otro archivo, ese
  archivo se abre y se comprueba — no se supone. Aquí la regla vivía en dos
  skills y solo se iba a tocar una.
- **Cómo se aplica:** antes de dar por cerrada una corrección de protocolo,
  `grep` del comando, del nombre del paso o de la promesa por todo el repo. En
  este arreglo eso sacó cinco sitios más: `session-closer.md`, `test_api.py`,
  `[A-006]`, y las referencias al nombre viejo del control.

### [L-008] 2026-08-03 — Se comparó la opción rival en su versión floja y se le ganó a esa

- **Qué pasó:** había que decidir dónde vivía el control del `.js`: en `pytest` o
  en el cierre. Se describió la opción del cierre como "un comando que tú corres
  antes de commitear" y se rechazó con "un freno que depende de tu memoria no es
  un freno". Nadie había propuesto esa versión: `.claude/agents/session-closer.md`
  existe y ya dispara controles solo, sin memoria de nadie.
- **Por qué pasó:** el principio invocado era correcto, y eso fue lo que lo
  escondió. Un argumento válido aplicado a una versión que nadie defendía suena
  igual de bien que uno bueno. 🔑 **Ganarle a la peor versión de la otra opción
  no es compararlas: es elegir primero y buscar razones después.**
- **Qué se hace distinto:** antes de recomendar entre dos caminos, escribir la
  opción rival **como la defendería quien la prefiere**, con lo mejor que tenga
  a favor. Si al lado de esa versión la recomendación se cae, es que no había
  recomendación. Aquí se cayó: el control acabó en el cierre, ver [D-017].
  Y ojo con el otro lado del mismo error — cuando el argumento propio se aplica
  también a la propia propuesta, hay que decirlo: `pytest` tampoco avisa si no
  corres los tests.

### [L-007] 2026-08-03 — La comprobación que mide de más: gritaba "viejo" con el repo correcto

- **Qué pasó:** el primer control del `.js` compilado usaba `diff -r` entre la
  carpeta que produce `tsc` y `app/static/`. Con el `.js` **perfectamente al
  día**, salía `Only in app/static: index.html` y el control lo declaraba viejo.
  La causa: `diff -r` compara en **las dos direcciones**, y `app/static/` es una
  carpeta mixta —también vive ahí `index.html`, escrito a mano, que ningún
  compilador va a generar nunca.
- **Por qué pasó:** se comprobó que el control **detectaba el fallo** y no se
  comprobó que **dejara pasar lo correcto**. Es el mismo animal de [L-003],
  [L-004], [L-005] y [L-006], pero por la cara que faltaba: las anteriores medían
  **de menos** —pasaban con el defecto puesto—; esta medía **de más**.
  🔑 **Y medir de más es peor de una forma concreta:** una alarma que nunca suena
  te deja ciego; una que suena **todas las noches con el repo correcto te entrena
  a apagarla**, y el día que suene de verdad ya le enseñaste a la gente a no
  mirar. La primera falla sola; la segunda se lleva por delante tu atención.
- **Lo doloroso:** la lección ya estaba escrita en este repo, por quien la volvió
  a incumplir un paso antes. `tests/test_tools.py`, en
  `test_normalize_user_accepts_ordinary_names`: *"El freno tiene que dejar pasar
  lo normal. Un validador que rechaza todo también pasaría los tests de arriba."*
  `diff -r` era exactamente ese validador que rechaza todo. **Saber un principio
  y aplicárselo a lo que estás escribiendo ahora son dos habilidades distintas**,
  y por eso el arreglo no puede ser "acordarse mejor" — [L-006] otra vez.
- **Qué se hace distinto:**
  1. **Un control se mide dos veces o no se midió:** una corrida con el fallo
     puesto y otra con el caso bueno. Las dos, en pantalla.
  2. **Y se mide en el caso que el diseño presume manejar.** La primera versión
     se midió con **un** archivo generado, y con uno solo el bug del bucle no
     puede aparecer: `for` devuelve el código del **último** comando, no de
     "alguno falló". Se destapó al probar con dos, con el que difiere delante.
  3. **La lista de lo que se vigila la declara el compilador**, no una lista
     negra de excepciones: se recorre lo que hay en su carpeta de salida. Una
     lista negra hay que mantenerla; esta se mantiene sola.
  4. **Detectar, informar y devolver éxito es no tener control.** Cada rama que
     encuentra algo mal levanta la bandera; un `echo` no frena nada.
  5. **El texto que se revisa tiene que ser el texto que se corrió.** La versión
     medida llevaba bandera y la que se pasó a revisar no: se "limpió" al
     transcribirla. El control vive en un archivo y se corre ese archivo.

### [L-006] 2026-08-03 — El cierre se cumplió entero y el trabajo se quedó sin subir: si el hash no está en `origin`, no hubo cierre

- **Qué pasó:** el cierre del paso 4 terminó con su commit y su hash, `f015a01`.
  La regla de cierre pedía exactamente eso, y se cumplió. Pero `origin/main`
  seguía en `460b04f`: el commit existía **solo en este disco**. Lo descubrió una
  revisión cruzada desde otra terminal haciendo `git fetch`. Un disco roto esa
  noche se habría llevado el paso 4 entero, con el cierre marcado como correcto.
- **Por qué pasó:** la regla vieja —nacida en la sesión 31— era *"si no hay hash,
  no hubo cierre"*. Esa regla comprueba que **existe un commit**, y de ahí se
  dedujo que el trabajo estaba a salvo. Son dos cosas distintas: un commit es
  local. 🔑 **Un control puede cumplirse entero y no comprobar lo que su nombre
  promete.** Cumplirlo daba tranquilidad y la tranquilidad era falsa, que es
  peor que no tener control: un hueco conocido se vigila, uno tapado no.
- **Y de qué familia es este fallo:** es el mismo defecto de [L-003], [L-004] y
  [L-005] —*la comprobación mide algo distinto de lo que dice medir*—, pero esta
  vez **no estaba en el código: estaba en el protocolo**. Sexta aparición del
  patrón, y la primera fuera de los tests. Donde haya un control hay que
  preguntarle qué mide de verdad, y los protocolos son controles.
- **Qué se hace distinto:** la regla queda corregida a **"si el hash no está en
  `origin`, no hubo cierre"**, y se comprueba con:

  ```bash
  git status -sb
  ```

  Si la primera línea dice **`ahead`**, no terminaste. El cierre acaba cuando esa
  palabra no aparece — no cuando aparece un hash.

### [L-005] 2026-08-03 — Buscar una palabra en un archivo entero no es comprobar el código: los comentarios también cuentan

- **Qué pasó:** la pantalla del paso 3 tiene que llamar a `/practice` con ruta
  relativa, sin nombrar host ni puerto — un `http://localhost:8000` escrito a
  mano funcionaría hoy y se rompería el día del despliegue. Para fijarlo se
  escribió un test que pedía el `app.js` compilado y comprobaba
  `assert "localhost" not in script`. Falló al primer intento, con el código
  **correcto**.
- **Por qué pasó:** la palabra `localhost` sí estaba en el archivo — dentro de un
  comentario que explica justamente por qué NO se usa. El compilador conserva los
  comentarios en la salida. El test decía medir "cómo llama la pantalla al
  servidor" y en realidad medía "qué letras aparecen en el archivo", incluidas
  las de la prosa que nadie ejecuta.
- **Qué se hizo:** apuntar a la llamada en sí, no al archivo:
  `assert 'fetch("/practice"' in script` y `assert 'fetch("http' not in script`.
  Eso sí distingue entre lo que el navegador ejecuta y lo que solo lee un humano.
- **Qué se hace distinto:** 🔑 **cuando un test busca texto dentro de un archivo,
  el patrón tiene que incluir la parte que lo hace código.** `"localhost"` cabe en
  un comentario; `fetch("http` no. Es la misma familia de [L-003] y [L-004] vista
  desde otro ángulo: allí el test no creaba el estado que decía probar, aquí no
  mira el sitio que dice mirar. En los tres casos el síntoma es el mismo —**la
  prueba mide algo distinto de lo que su nombre promete**— y solo se descubre
  preguntándose qué tendría que pasar para que fallara.
- **Y lo que salió bien:** falló al primer intento y por eso se encontró. Un test
  que hubiera pasado por casualidad —si el comentario no llega a existir— habría
  quedado ahí, dando una confianza falsa hasta el paso 7.

### [L-004] 2026-08-02 — Una prueba que el código roto también pasa no prueba nada

- **Qué pasó:** para comprobar el arreglo de concurrencia se montó una prueba de
  50 peticiones simultáneas por HTTP, con PowerShell. Dio **0 errores y marcador
  50**: perfecto. Pero por un puerto ocupado resultó que quien había contestado
  era el servidor **viejo**, sin el arreglo. Y también había dado 50 de 50.
- **Por qué pasó:** las 50 peticiones no salían lo bastante juntas. PowerShell
  tarda en arrancar cada hilo, así que llegaban en fila y nunca llegaron a
  pisarse. La prueba medía otra cosa distinta de la que decía medir.
- **Qué se hizo:** correr el `add_point` viejo y el nuevo, uno al lado del otro,
  con 50 hilos de Python sobre el mismo archivo. El viejo: **45 errores de 50**,
  marcador 1, números repetidos. El nuevo: 0 errores, marcador 50, 50 números
  distintos. Eso sí es una prueba.
- **Qué se hace distinto:** 🔑 **antes de fiarse de una prueba, comprobar que
  falla con el código roto.** Una prueba que pasa en los dos casos no está
  midiendo el arreglo, y da una confianza que no existe. Es el mismo criterio
  que ya está en `CLAUDE.md` como PI-4 —terminado = visto funcionando— llevado
  un paso más: **visto fallando cuando debía fallar.**
- **Y una segunda:** al levantar un servidor, comprobar en su log que dice
  "Uvicorn running on…". Si dice `[Errno 10048] error while attempting to bind`,
  el que contesta es otro, y todo lo que se mida después es sobre el código
  equivocado.

### [L-003] 2026-08-02 — 45 tests en verde no vieron un fallo que rompía 7 de cada 10 peticiones

- **Qué pasó:** el paso 2 se cerró con 45 tests en verde y el servidor probado a
  mano. Una revisión externa lo levantó con **50 peticiones a la vez** y entre 31
  y 39 devolvieron error 500. De 50 puntos esperados, el marcador guardaba 8.
- **Por qué pasó:** `TestClient` manda las peticiones **de una en una**. Todos
  los tests, y todas las pruebas a mano, ejercitaban un solo escritor. Con un
  solo escritor el código era correcto — el fallo no estaba en las piezas, estaba
  en dos piezas ocurriendo a la vez, que es un estado que ninguna prueba creaba.
- **Qué se hace distinto:** 🔑 **un test en verde no dice "el código está bien",
  dice "el código está bien para lo que este test hace".** Al cambiar de terminal
  a servidor cambió una suposición de fondo —de un escritor a muchos— y ninguna
  prueba se enteró. Cuando cambie esa clase de suposición, hay que escribir el
  test que la ejercite: aquí, hilos de verdad sobre el mismo archivo.
- **Cuándo vuelve a pasar:** en el paso 4 (memoria por persona) y en el paso 7
  (la nube decide cuántos procesos hay). Anotado como suposición [A-002].

### [L-002] 2026-08-02 — `pip install` sin versión fijada no da la misma versión dos veces

- **Qué pasó:** al crear el entorno virtual, `pip install pytest` instaló
  **pytest 9.1.1**. El Python global de la misma máquina tenía **8.1.1**. Dos
  versiones distintas, el mismo día, sin haber hecho nada raro.
- **Por qué pasó:** `pip install pytest` no pide "pytest": pide "el pytest más
  nuevo que haya hoy". La respuesta cambia con el calendario. El global se
  instaló hace meses; el del entorno, hoy.
- **Qué se hace distinto:** toda dependencia va en `requirements.txt` con `==` y
  versión exacta. Se instala con `pip install -r requirements.txt`, nunca por
  nombre suelto. Sin eso, un fallo que solo aparece en una máquina —o solo en el
  servidor del paso 7— se vuelve casi imposible de encontrar: el código es el
  mismo y las librerías no.

### [L-001] 2026-08-02 — La consola de Windows no pinta caracteres fuera de ASCII

- **Qué pasó:** `main.py` imprimía `TEAPP — write a sentence...` con guion largo,
  y en pantalla salió `TEAPP ? write a sentence...`. Los tests no lo detectaron:
  pasaban los 14. Se vio solo al correr la app de verdad.
- **Por qué pasó:** la consola de Windows no usa UTF-8 por defecto, y el guion
  largo no existe en su tabla de caracteres. Lo sustituye por `?`. El código era
  correcto; lo que fallaba era el sitio donde se imprimía.
- **Qué se hace distinto:** en lo que se imprime por terminal, solo ASCII. Y la
  lección de fondo, que es la que importa: **PI-4 no es burocracia.** Los tests
  daban verde sobre un texto que en pantalla salía roto. Un test comprueba lo que
  la función devuelve, no lo que la persona ve. Por eso "terminado = visto
  funcionando" pide las dos cosas, no una.

<!-- La más reciente arriba. Formato:

### [L-001] 2026-08-02 — <la lección, en una línea>

- **Qué pasó:** <el fallo o la sorpresa>
- **Por qué pasó:** <la causa, ya entendida>
- **Qué se hace distinto:** <la regla que queda para adelante>

-->
