# Decisiones — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [D-000]`. Búscala con `grep`, no leas el archivo entero.

## 🚨 El id tachado: una decisión que ya no se cita como vigente

Igual que en `assumptions.md`, **el id va tachado cuando la decisión dejó de ser
la respuesta actual**. El texto viejo **se conserva** —el porqué sigue
enseñando— pero **no se cita**, y la fila empieza diciendo adónde ir:

| marca | qué significa | ejemplo |
|---|---|---|
| `~~D-nnn~~` 🔻 **SUPERADA** | otra decisión la reemplazó; **sus números ya no son los del código** | `~~D-071~~` → `[D-072]` |
| `~~D-nnn~~` ✅ **CUMPLIDA** | no estaba equivocada: su mandato se ejecutó y se acabó | `~~D-080~~` → `[D-081]` |

> 🔑 **Una decisión superada no se borra y no se corrige: se marca.** Borrarla
> pierde el porqué; corregirla en el sitio la hace parecer que siempre dijo eso.

⚠️ **Por qué hizo falta escribir esto.** El 2026-08-14 el arranque reportó los
números de `~~D-071~~` (`8,0 s`, `read 4,0`) como si fueran los del código —lo
son desde `[D-072]`: `9,0` y `read 6,5`— **dos veces**, y presentó `~~D-080~~`
como *"decisión crítica abierta"* con `[D-081]` encima. Las dos filas se leían
como vigentes porque **nada en ellas decía lo contrario**: la corrección vivía
en la fila de la decisión nueva, y quien busca por tema encuentra la vieja. Ver
`[L-066]`.

📌 **Solo están marcadas las dos que se vieron fallar.** Puede haber más:
`[D-070]` ya llevaba su propia enmienda con otro formato. Se marcan **cuando se
detecten**, no en una pasada — pero al escribir una decisión que reemplaza a
otra, **tachar la vieja va en el mismo cambio**.

## Índice

| id | fecha | qué se decidió | toca |
|---|---|---|---|
| D-099 | 2026-08-18 | 🗄️ **El corpus de respuestas del juez se ARCHIVA en `_persistence/replies/`, y de `data/` se BORRA: una sola copia, la respaldada.** Firmado por el usuario. 🔑 **El argumento es el de `[D-097]` aplicado a la otra mitad del cruce:** `data/` es un disco sin copia y fuera de Git (`.gitignore:18`, comprobado hoy), así que las dos mitades de `T-111` vivían en regímenes opuestos — y la desprotegida era la que costó dinero. ⚠️ **No es que no se pueda recomprar: es que no se puede repetir.** `[D-096]` fija `$0,21` las sesenta, pero el juez no es determinista: recomprarlas da otras respuestas y el número del cruce deja de ser reproducible. 🔻 **Mover y no copiar, por un motivo estructural y no de higiene:** con copia, `T-111` **puede** leer el archivo equivocado; con movimiento, el archivo equivocado **no existe en el disco**. Es el mismo tipo de freno que `[D-097]`, no una convención que haya que recordar. 🚨 **Y el ORDEN se invirtió respecto al propuesto —copiar, portero, verificar en Git, y solo entonces borrar—** porque `mv` como primera operación es el único instante del plan en que existe una sola copia en el mundo: un destino mal escrito o un `git clean` de más y se acabó. El movimiento es el RESULTADO del plan, no su primera acción. 📌 **`replies/` no es hermana de `corpus/`: es su ANTESALA**, y su puerta de salida es la de `[D-092]` sin cambiarla —cuando algún eje del nombre deja de coincidir con producción, el archivo se muda a `corpus/`, disparado por el commit que mueve `MODEL` o `GRAMMAR_RUBRIC`. Se escribe al nacer la carpeta porque una antesala sin salida escrita es la misma cosa en dos sitios con fecha diferida. 🔒 **El portero cierra el conjunto de campos** (`number`, `sentence`, `reply`, `broken`, `model`, `rubric`) y **declara en voz alta que `reply` no lo audita nadie** — aquí la prosa libre no es un campo lateral como la `note` de `labels/`: es la carga entera del archivo, sesenta párrafos generados a un repo PÚBLICO (`[C-007]`). **Contra:** copiar a `_persistence/corpus/` (descartado: pone `test_no_frozen_corpus_carries_the_live_rubric` en rojo por partida doble —el nombre lleva la huella viva `bbf4be38` y las filas también—, y `_frozen_corpora()` usa `glob("*.jsonl")`, así que sí lo alcanzaría); dejar copia en `data/` (descartado: dos archivos con el mismo nombre que un día discrepan); `mv` directo como primera acción (descartado por el riesgo de arriba). ⚠️ **Lo que esto NO cierra:** otra corrida entera hoy vuelve a crear ese nombre en `data/` — `T-109` sigue abierta y ahora apunta a un insumo concreto. | `_persistence/replies/`, `replies.py`, `tests/test_replies.py`, `data/`, `[D-092]`, `[D-093]`, `[D-096]`, `[D-097]`, `[C-007]`, `[C-009]`, `T-109`, `T-111`, paso 9 |
| D-098 | 2026-08-18 | 📏 **La vara del etiquetado es el INGLÉS ESCRITO DE LIBRO, no el inglés que un nativo aceptaría de oído.** Firmado por el usuario. 🔑 **No se contestó preguntando: se leyó de las etiquetas.** Las frases 22 (*There is many people*), 30 (*How much time you need?*) y 54 (*There are less people today*) son las tres que caen a un lado o a otro según la vara —las tres se oyen a diario y las tres fallan en un examen— y las tres salieron `wrong`. Tres de tres es criterio, no casualidad. 🔻 **Y la 55 se revisó bajo esa vara SIN cambiarla:** *"She told me that she is tired"* quedó `correct`, y aguanta — el retroceso de tiempo tras `told` es **opcional** en la gramática de referencia cuando el estado sigue vigente, así que `is` no es un error de libro. La inconsistencia que esta terminal señaló contra 22/30/54 **era más débil de lo que dijo al señalarla**. ⚠️ **Y esa fila estaba contaminada de antemano:** la 55 y la 54 se usaron como EJEMPLOS al explicar `unclear`, antes de que nadie etiquetara — ver `[L-083]`. 📌 **Cero `unclear` en las 60, y se deja constancia de que eso no se auditó:** puede ser que las frases se inventaran claras a propósito, o que una duda se empujara hacia un lado para no complicarse. Ningún programa distingue las dos cosas, y `note` está vacía en las sesenta. **Contra:** la vara del hablante nativo — descartada porque la app enseña a ESCRIBIR y `GRAMMAR_RUBRIC` ya está redactada en esos términos; con dos varas distintas lo que se mide no es el acierto del juez sino el desacuerdo entre reglas. | `_persistence/labels/sentence_labels.jsonl`, `T-106`, `[D-097]`, `[L-083]`, `GRAMMAR_RUBRIC`, paso 9 |
| D-097 | 2026-08-18 | 🗂️ **El etiquetado manual vive en `_persistence/labels/`, HERMANA de `corpus/` y no dentro, con portero propio desde el primer commit.** Firmado por el usuario. 🔑 **Por qué no cabe en `corpus/`: son vidas opuestas.** `corpus/` guarda lo que ya **no** es producción —`[D-092]`— y `test_no_frozen_corpus_carries_the_live_rubric` lo hace cumplir contra el nombre **y fila por fila**. Las etiquetas nacen contra la rúbrica **viva** (`bbf4be38`, leída del intérprete hoy) y valen mientras viva: meterlas en `corpus/` pone el test en ROJO mañana. 🚨 **Y no es lo mismo que perder el corpus:** sin etiquetas el archivo cuesta `$0,20` y se vuelve a comprar; con sesenta juicios humanos dentro **deja de tener precio** (`[C-009]`), y hoy `data/` es un disco sin copia y fuera de Git. ⚠️ **`PI-8` aquí está CIEGA, y por eso hace falta portero nuevo:** `sentences_are_invented()` mira el campo `sentence` y su propio docstring declara que **no** audita `reply` —*"un freno estrecho y bien puesto, no una garantía"*—. El archivo de etiquetas no aporta frases: aporta **prosa del humano**, sesenta veces, a un repo PÚBLICO (`[C-007]`). La cerradura vieja pasaría en VERDE sobre él. 🔁 **Es `LM.15` (`LESSONS.md:3424`): un instrumento ciego no da un dato falso, da silencio — y el silencio se lee como confirmación.** 🔻 **Qué puede y qué NO puede el portero, dicho antes de escribirlo:** un programa **no** puede vetar prosa semánticamente; un detector de *"¿esto lleva datos de una persona?"* nacería con el defecto de `LM.15` de fábrica. Lo que sí puede es **estrechar la superficie no auditable hasta un solo campo con nombre**: (1) `sentence` ∈ `SENTENCES`, reutilizando la cerradura que ya existe; (2) el juicio en campos **cerrados** —`verdict` de conjunto fijo, reglas incumplidas ⊆ nombres de la rúbrica—, exhaustivamente comprobables por `assert`; (3) la prosa libre confinada a **UN** campo `note` opcional, y el portero afirma que ningún otro campo lleva texto libre; (4) el docstring **dice en voz alta que `note` no lo audita ningún programa** —esa frase es lo que impide que el verde mienta, y es lo que `sentences_are_invented()` hizo bien; (5) guardia de carpeta vacía, hermano de `test_the_corpus_folder_is_not_empty`, porque un `glob` sin resultados pasa en silencio (`[L-048]`). 📌 **Formato `.jsonl`, una fila por juicio — por su propio mérito, NO por herencia del portero de `corpus/`.** Esta terminal propuso `.jsonl` *"para que el portero de `T-108` las alcance sin inventar un segundo mecanismo"*, y **eso era falso**: `T-108` endurece `CORPUS_DIR.glob("*.jsonl")`, que **no mira otra carpeta** esté arreglado o roto. 🔴 **De ahí que `T-108` NO sea bloqueante de esta decisión**, contra lo que se dijo al proponerla: bajo el plan firmado el bloqueante es el portero de `labels/`, que nace con la carpeta. `T-108` sigue siendo trabajo real, como tarea suya. **Contra:** `labels/` dentro de `corpus/` (descartado: test en rojo y criterio de entrada opuesto); dejarlo en `data/` como el corpus (descartado: sin copia y fuera de Git, y el trabajo humano no se vuelve a pagar); crear la carpeta hoy y el portero después (descartado: **el archivo que se cuela es el que entra el día que aún no había portero**). | `_persistence/labels/`, `eval_rubric.py`, `tests/`, `PI-8`, `[C-007]`, `[C-009]`, `[D-092]`, `[D-093]`, `[L-048]`, `LM.15`, `T-106`, `T-108`, paso 9 |
| D-092 | 2026-08-18 | 🏷️ **El nombre del corpus lleva CUATRO ejes —modelo, fecha, huella de `GRAMMAR_RUBRIC` y marca de selección— y la promoción a `_persistence/corpus/` cuelga del COMMIT que mueve la configuración, no de que alguien caiga después.** Firmado por el usuario. 🚨 **El bicho de partida (`T-107`, `[L-076]`): `replies_file()` devolvía nombre fijo y `save_replies` abre en `"w"`, así que cada corrida borraba la anterior.** NO se arregla con `"a"`: sobrescribir está bien razonado en su propio docstring —dos modelos o dos rúbricas revueltos son `[L-071]`—; lo que faltaba era **identidad en el nombre**. 🔑 **Por qué CUATRO y no dos.** (1) El **modelo** ya viaja dentro de la fila, así que en el nombre no añade identidad nueva —pero hace falta para no pisarse. (2) La **rúbrica** no estaba en ningún sitio: ni en la fila, ni en el nombre. Y es el eje que **ya se movió dos veces sin dejar rastro** —`678 → 1.016` caracteres (`[D-066]`/`[D-067]`) y `1.016 → 1.098` ayer (`[D-090]`/`[D-091]`)—, el mismo bicho que `measure_tutor.py:85-88` lleva escrito desde antes (`[L-059]`). ⚠️ **Y la fecha NO lo tapa:** la línea base corrió a las 21:43 UTC y el diagnóstico a las 21:54, **mismo día**, con la rúbrica cambiada entre medias. (3) La **marca de selección**, que es el hallazgo que ninguno de los dos ejes anteriores cubre: el archivo en disco tiene **10 filas y 10 rotas**, y eso **no es un resultado, es la selección** —se escogieron a propósito las que habían fallado—. Quien lo divida mañana obtiene `100% de fallo` y se lo cree: `[L-071]` otra vez, un agregado sobre un conjunto sesgado. 🔻 **El criterio de promoción, y las tres versiones que se descartaron.** Contra (a) *"corpus que respalda una decisión firmada"* — se estira, todo acaba respaldando algo; contra (b) *"corpus cuya rúbrica ya no existe en producción"* (propuesta de esta terminal) — **pierde el eje del modelo**, que es justo el que `[D-049]` va a mover **tres veces**: un corpus de Opus 5 con la rúbrica intacta deja de ser repetible el día que `MODEL` baje a Sonnet, y **es la línea base contra la que se mide el descenso**, o sea el que más duele perder es el que ese criterio deja fuera. 🚨 **Y el defecto de fondo de (b) era ser RETROSPECTIVO:** al crear un corpus la rúbrica está viva por definición —acabas de correr con ella—, así que **nada se guardaría nunca al nacer**, y la sala de espera es `data/`: ignorado por Git (`git check-ignore`, comprobado), **un solo disco, sin copia**. El criterio dejaba la evidencia en el sitio menos duradero del proyecto exactamente mientras se la consideraba *"todavía no valiosa"*. ✅ **Lo elegido: el criterio ES el propio nombre** —se promueve cuando algún eje deja de coincidir con producción—, que no se estira porque los ejes son los que son, lo comprueba un programa y **cubre el modelo**. 🔑 **Y el disparador va pegado al cambio, mismo patrón que `[D-081]`** (leer el límite por minuto y ponerlo en `LAB_REQUESTS_PER_MINUTE` **en el mismo commit**): quien toque `MODEL` o `GRAMMAR_RUBRIC` promueve, en ese commit, el último corpus de la configuración que se va. **Cuelga de un evento que ocurre seguro y se nota seguro, no de una realización posterior.** 📌 **La huella se calcula, no se teclea** —`sha256` de `GRAMMAR_RUBRIC` ya montado, 8 caracteres—, por el mismo motivo por el que `replies_file()` es una función y no una constante: se pregunta en cada llamada en vez de fiarse de que alguien mantenga el dato. 🔍 **La huella de la rúbrica JUBILADA salió del blob de Git por programa, no a mano:** `9844eac^:app/tools.py` la tenía como cadena llana (sin `f`), **1.016 caracteres**, que cuadra exacto con el `[D-066]`; vieja `67a8a252`, actual `bbf4be38`. 🔻 **Lo que se movió hoy:** las 10 filas del diagnóstico del 2026-08-17, evidencia primaria de `[D-090]` y `[D-091]`, salen de `data/` y entran en `_persistence/corpus/` con los cuatro ejes en el nombre y `rubric` en cada fila. **No se borran** porque su rúbrica ya no está en producción: no se pueden volver a levantar **ni pagando**. ⚠️ **Las corridas VIVAS siguen escribiendo en `data/`** — solo se promueve lo congelado | `eval_rubric.py`, `tests/test_eval_rubric.py`, `_persistence/corpus/`, `[D-049]`, `[D-066]`, `[D-081]`, `[D-085]`, `[D-089]`, `[D-090]`, `[D-091]`, `[D-093]`, `[L-059]`, `[L-071]`, `[L-076]`, `T-107`, `T-106`, `PI-8`, paso 9, auditoría externa del 2026-08-18 |
| D-096 | 2026-08-18 | 💵 **`COST_PER_CALL_USD` vuelve a estar MEDIDO: `$0,00304` → `$0,00342`.** La corrida de línea base de hoy —60 llamadas, entera— facturó **`$0,20`** en la consola de Anthropic, y quien lleva el proyecto confirmó que **no hubo ninguna otra llamada** ese día contra la cuenta — así que la atribución es limpia pese a que `[C-009]` declara el saldo **compartido**. ⚠️ **La consola redondea al céntimo, o sea que lo medido es un INTERVALO:** `$0,20` ∈ `[0,195 , 0,205]` → **`$0,00325 – $0,00342`** por llamada, ±2,5%. 🔑 **Se escoge el lado ALTO, y no el punto medio, siguiendo el precedente de `[D-079]` sin inventar criterio nuevo:** esto **calibra un freno**, no describe el mundo — sobreestimar aprieta el tope, subestimar lo afloja, y aflojarlo ya costó `$0,32` contra un presupuesto de `$0,25` en `[D-078]`. 🔴 **Lo que se cobró, dicho en voz alta:** `MAX_CALLS_PER_RUN` sale de dividir `$0,25` entre esta constante — con el valor caducado daba **82** llamadas, con el medido da **73**. El freno de `measure_tutor.py` llevó desde el 17 dejando pasar **nueve llamadas de más** de las que caben en su presupuesto. 📌 **Y no se descubrió: estaba escrito.** El bloque anterior se marcó a sí mismo `CADUCADO ... HACIA EL LADO MALO`, explicó que un divisor pequeño da un tope grande, y predijo que *"la corrección sale sola de la próxima corrida de 60"*. Salió sola. **Un número caducado con su caducidad escrita al lado se comporta como una tarea con disparador** (`[L-064]`) — es la forma buena de aplazar. ⚠️ **El margen al acantilado se ENCOGIÓ al medir:** `int(0,25/x) >= 60` rompe en `$0,00416`, así que de veintidós llamadas de sobra se pasa a **trece**. No subió el coste: se corrigió lo que creíamos que valía. 🔒 El `assert` de `test_the_cap_still_lets_the_whole_run_through` **no se tocó** — solo el ejemplo de su docstring, que es exactamente la distinción de `[L-078]`. **Contra:** el punto medio `$0,00333` (descartado: no es como se calibra un freno) y dejarlo caducado hasta tener una consola sin redondeo (descartado: el intervalo ya decide, y esperar deja el freno flojo). Suite `534` verde | `measure_tutor.py`, `tests/test_measure_tutor.py`, `eval_rubric.py`, `[C-009]`, `[D-060]`, `[D-078]`, `[D-079]`, `[D-090]`, `[L-059]`, `[L-064]`, `[L-078]`, regla 6, `T-106`, paso 9 |
| D-095 | 2026-08-18 | 🧭 **El nombre del archivo de respuestas se calcula con lo que LLEGÓ (`len(records)`), no con lo que se planeó (`calls = len(plan)`).** 🚨 **El bicho:** el bucle de `main()` tiene dos `break` —presupuesto agotado y `TutorUnavailableError`— y la cabecera del propio archivo dice que cortarse es el modo de fallo **esperado**; así que una tanda de 60 podía acabar con 30 filas guardadas en un archivo llamado `full`. 🔑 **Y el aviso existía, en el sitio equivocado:** `report_lines` imprime *"faltan N respuestas... no valen como línea base"*, pero eso vive en el scrollback de la consola — **la parte que sobrevive era justo la que mentía**. ⚠️ **La segunda mitad es peor que la primera:** `save_replies` abre en `"w"`, y modelo, fecha y huella son los mismos dentro del mismo día — así que una segunda corrida cortada **borraba la línea base pagada** de la primera. Es `[L-076]` viva dentro de su propio arreglo: `[D-092]` cerró la colisión entre modelos y entre rúbricas, **no la de una corrida consigo misma**. Con `len(records)` el nombre cambia a `pick`, que en este vocabulario ya significa *"esto no es una línea base"*, y de paso deja de pisar el archivo bueno. 📌 **Los dos `print` dicen cosas distintas a propósito:** el de arriba enseña el destino **planeado** —ahí aún no se sabe cuántas llegarán, y se marca `(si llega entera)`—; el de abajo, el **real**, que es el que hay que mirar. 🔻 **VISTO MORDER:** sabotaje a `replies_file(calls)` → rojo con 30 filas en `..._full.jsonl` y el AVISO impreso justo encima. 🔴 **Y el test que parecía cubrirlo no cubría nada:** `test_a_partial_run_is_named_pick_not_full` prueba `replies_file(10)`, una tanda que se **pidió** parcial; el camino roto —plan de 60, llegaron 30— solo existía dentro de `main()`, y **ningún test entraba en `main()`**. El nuevo es el primero. Suite `533 → 534` | `eval_rubric.py`, `tests/test_eval_rubric.py`, `[D-092]`, `[L-071]`, `[L-076]`, `[L-080]`, paso 9, auditoría externa del 2026-08-18 |
| D-094 | 2026-08-18 | 🧭 **La traza deja de escribir `correct: bool` y escribe `outcome` con TRES estados —`correct`, `wrong`, `bad_format`— más `broken`, la lista de promesas rotas.** Firmado por el usuario. 🚨 **El bicho, que es `[D-089]` cobrando:** `split_verdict` devuelve `correct=False` tanto cuando la frase estaba mal **como cuando el juez se saltó el formato**, así que el cuaderno escribía *"el alumno se equivocó"* y *"nuestro modelo se rompió"* **como el mismo dato**. Dos causas opuestas, arreglos en direcciones contrarias —uno a la clase de inglés, otro a la rúbrica— y **la ambigüedad no se ve en la gráfica**: `LM.15` dentro del paso que se llama Observabilidad. 🔑 **Un campo de tres estados y NO dos booleanos**, que era la salida obvia: dos casillas dan cuatro combinaciones, **una imposible**, y alguien acabaría leyendo la imposible como un dato; además obligan a cruzarlas para contestar *"¿quién falló?"*, cuenta que se hace mal una vez y no se nota nunca. 📌 **Y `outcome` NACE en `split_verdict`, en las tres ramas que esa función ya tenía** — no se deduce después cruzando campos: es lo que la función siempre supo y tiraba al devolver un `bool`. `correct` pasa a ser **propiedad derivada**, no campo, así que no puede discrepar. 🔒 **`check_reply` corre DENTRO de `split_verdict`, donde el texto crudo todavía existe, y del módulo salen NOMBRES DE PROMESA, nunca texto — es `PI-8`:** la respuesta cruda puede citar dentro la frase de quien practica, y la evidencia es literal, del corpus promovido hoy (*"Say: They are my friends"*, fila 4). ⚠️ **El import de `rubric_check` va dentro de la función a propósito:** arriba sería ciclo, porque `rubric_check` importa de `tools` y `[D-091]` fijó que la dependencia solo va en ese sentido. 🔑 **`broken` no es redundante con `outcome`:** `outcome="correct"` con `broken=["too_many_sentences"]` significa *"el veredicto aguanta y la forma se está yendo"* — el aviso temprano que `[D-049]` necesita al bajar de modelo, y que un solo campo no puede enseñar. 🔻 **Se SUSTITUYE, no conviven, y la razón se comprobó:** no hay **ningún** lector de `trace.jsonl` en el repo —solo `config.trace_file()`, `app/trace.py` y los tests—, así que la compatibilidad a proteger era con un lector que no ha nacido; y `T-102` sigue abierta diciendo que la traza **no se ha visto escribir con el servidor levantado**, o sea que el archivo puede estar vacío. **Contra:** meter `outcome` y retirar `correct` en un cambio aparte — descartado porque sería una tarea aplazada **sin disparador** (`[L-064]`) y el tercer acto de acordarse del día, después del `mv` y de la cerradura. 🚨 **Dónde NO corta el bisturí, que es la mitad del asunto:** `GrammarVerdict.correct` y `TutorReply.correct` **se quedan** — son los que dan el punto en el marcador, y un barrido que los arrastrara **le cambiaría la nota a la gente en silencio**, porque un marcador equivocado sigue pareciendo un marcador. Lo que se retira es el campo del **cuaderno**, no el de la clase. 🔻 **VISTO MORDER — cuatro sabotajes, rojo cada uno:** `outcome` clavado en `respond` (el bicho de `[L-073]` repetido), `bad_format` degradado a `wrong`, el texto crudo saliendo por `broken`, y el punto regalado en el marcador. 🔴 **Y los dos guardianes de conjunto de `[L-073]` salieron rojos al añadir los campos** — el control haciendo su trabajo: se escribieron primero los vigilantes y **después** se amplió el conjunto, que es lo que su propio docstring manda. Suite `526 → 533` | `app/tools.py`, `app/english_tutor.py`, `app/api.py`, `app/trace.py`, `tests/test_tools.py`, `tests/test_english_tutor.py`, `tests/test_trace.py`, `tests/fake_tutor.py`, `[D-049]`, `[D-085]`, `[D-089]`, `[D-091]`, `[L-064]`, `[L-073]`, `[L-078]`, `LM.15`, `PI-8`, `T-105`, `T-102`, paso 9, auditoría externa del 2026-08-18 |
| D-093 | 2026-08-18 | 🔒 **La regla `PI-8` deja de ser una advertencia en la puerta y pasa a ser una CERRADURA: un corpus solo se promueve a `_persistence/` si TODAS sus `sentence` están en `SENTENCES`.** Firmado por el usuario. 🚨 **El problema que resuelve:** `[D-092]` abre la puerta de `_persistence/` a archivos de corrida, y el repo es **público** (`[C-007]`). Hoy esa puerta es inocente —el corpus se construye contra `SENTENCES`, frases **inventadas** que ya están en el repo; comprobado fila por fila en las 10 del diagnóstico: ninguna la escribió una persona—, **pero mañana no se nota**. 🔑 **Por qué cerradura y no nota, que es el punto entero:** una advertencia escrita es una promesa de tenerlo en cuenta, y `PI-8` ya se documenta a sí misma como la más débil de las tres reglas de código —*"la respalda una casilla en `protocol-close`, y una casilla pregunta, no detecta"*—. La condición aquí **sí es comprobable por un programa**, así que se comprueba: un corpus hecho con frases de gente usando la app **falla solo**, sin que nadie se acuerde de la regla. **Contra:** dejarlo como comentario junto a la promoción, que era la propuesta de esta terminal. ⚠️ **Honestidad sobre su alcance, para no repetir el defecto que denuncia:** la cerradura cubre el campo `sentence`, que es por donde entraría una frase de una persona. **No** audita `reply` —eso lo escribe el modelo— ni impide que alguien copie una frase a mano en un archivo del repo. Es un freno estrecho y bien puesto, no una garantía. 🔻 **VISTO MORDER:** sabotaje con una fila cuya `sentence` no está en `SENTENCES` → rojo | `eval_rubric.py`, `tests/test_eval_rubric.py`, `[D-092]`, `[C-007]`, `[L-048]`, `PI-8`, `T-107`, `T-071`, paso 9 | 🔴 **AMPLIADA el mismo día:** la cerradura solo la llamaban tres tests con registros a mano —nadie sobre la carpeta— y la promoción es un `mv` manual, así que **invocarla seguía siendo acordarse**. Cerrado con el portero de `T-071` aplicado a `_persistence/corpus/`: `glob` en cada `pytest`, más el invariante de que ningún corpus congelado lleve la huella viva, más el freno contra el portero en vacío (`[L-048]`). Suite `523 → 526` |
| D-091 | 2026-08-17 | 🔒 **Se endurece la RÚBRICA para prohibir TODAS las comillas, en vez de afinar el corrector para mirar solo las de la corrección; y los dos números que se vigilaban con comentarios pasan a ser UNO.** Firmado por el usuario. 🚨 **El motivo de descartar la opción fina no es que costara más código —eso es un precio—: es que NO SE PUEDE CONSTRUIR con lo que el módulo dice ser.** Para mirar solo las comillas *alrededor de la corrección*, el programa tiene que saber qué trozo **es** la corrección, y la respuesta no trae delimitador: en las nueve `FIX` que hay en disco la corrección entra de **cinco formas distintas** (`Say:`, `We say:`, `It should be:`, `The correct sentence is:`, y la fila 5 **sin ninguna entradilla**). 🔑 **Cualquier detector fino sería una heurística sobre el FRASEO del modelo — y el fraseo es exactamente lo que `[D-049]` va a mover** al bajar a Sonnet 5 y Haiku 4.5: cuando fallara en esa corrida, *"el modelo se rompió"* y *"la heurística resbaló"* serían indistinguibles. **Es la enfermedad que `[D-090]` acaba de curar en el tope saturado, reintroducida en la promesa de al lado.** Y haría que una de las cuatro promesas mecánicas dejara de serlo, con la cabecera del módulo explicando por qué esas cuatro. **Precio real de la opción elegida, dicho entero:** el modelo pierde una forma legítima de nombrar una expresión —*"you used going to for the future"* sin comillas—; se paga barato porque para un A1 se entiende igual, y **es gratis si entra en este cambio**: la línea base de 60 ya hay que rehacerla por el tope de frases. 📌 **Y la prohibición va en su PROPIA LÍNEA, no colgando de la frase de markdown** —iba de cuarto ítem de una lista de markdown, **y una comilla no es markdown**: por ahí se separaron rúbrica y corrector sin que nadie lo notara. 🚨 **Segunda mitad — el aviso cruzado de `[D-090]` era una NOTA, no un freno:** `MAX_SENTENCES` ahora vive en `app/tools.py` (la dependencia solo puede ir en ese sentido: `rubric_check` ya importaba de `tools`, al revés sería ciclo), la prompt lo mete con `f-string`, y `rubric_check` lo **importa**. Un número, un sitio. 🔻 **VISTO MORDER — tres sabotajes, un rojo cada uno:** prompt a `two` a mano, comilla otra vez condicionada, y copia del monedero restaurada. Suite `513 → 516` | `app/tools.py`, `app/rubric_check.py`, `eval_rubric.py`, `tests/test_rubric_check.py`, `tests/test_eval_rubric.py`, `[D-049]`, `[D-089]`, `[D-090]`, `[L-077]`, `T-104`, paso 9 |
| D-090 | 2026-08-17 | 📏 **El tope de la rúbrica sube de DOS frases a TRES, firmado por el usuario, y el motivo escrito NO es el que traía `[D-089]`.** La hipótesis de `[D-089]` —*"el aliento cálido añade una tercera frase, así que la rúbrica se contradice"*— **no aguanta leída entera**: para `FIX` la rúbrica pide dos cosas (*"give the corrected sentence and name the one mistake that matters most"*), y lo cálido sale de la línea de personaje, que es **tono, no un renglón**. Si ese fuera el argumento, la conclusión correcta sería la contraria: apretar el tono dentro de dos frases. 🔑 **Los dos motivos que SÍ deciden.** (1) **El `dos` duplicaba trabajo:** su razón escrita es *"A1 learners give up when a reply is a list of everything they did wrong"* —el miedo es a una **lista de errores**, no al largo— y de eso ya se encarga *"never correct more than one thing at a time"*. (2) 🚨 **Un detector saturado deja de ser un instrumento y pasa a ser una constante:** `too_many_sentences` salía roja **18 de 60 con Opus 5**, el modelo más capaz, y `[D-049]` existe para bajar a Sonnet 5 y Haiku 4.5 **midiendo cuándo se les va la forma**. Con la promesa ya rota arriba, *"Haiku se rompió"* y *"esto ya estaba rojo"* llegan como el mismo dato — es `LM.15` por el lado contrario. **Contra:** dejar el dos y apretar el tono, que conserva respuestas más cortas para A1. 🔻 **VISTO MORDER en los dos sentidos:** primero el test movido al borde nuevo **en rojo** contra el código viejo (tres frases marcadas como rotas), y después, con el tope ya en tres, **sabotaje a cuatro → 3 tests en rojo**. Suite `512 → 513`. ⚠️ **Y la mitad que faltaba de `T-104` sigue abierta:** lo de las comillas (`_has_markdown` rechaza cualquier `"`, la rúbrica solo prohíbe las que envuelven la corrección) **no se decide aquí**. 💰 **Consecuencia inmediata y escrita en el código, no solo aquí: `COST_PER_CALL_USD` queda CADUCADO hacia el lado malo** — tres frases son más tokens de salida, el número viejo es más bajo que el real, y `MAX_CALLS_PER_RUN` sale de dividir por él, así que el freno de la tanda **deja pasar más llamadas de las que caben en `$0,25`**. Es `[D-078]` repetido. Se deja el número viejo sin inventar otro (regla 6) y se corrige con la próxima corrida de 60 | `app/tools.py`, `app/rubric_check.py`, `tests/test_rubric_check.py`, `tests/test_eval_rubric.py`, `measure_tutor.py`, `[D-049]`, `[D-078]`, `[D-089]`, `[L-059]`, `[L-076]`, `LM.15`, `PI-6`, `T-104`, paso 9 |
| D-089 | 2026-08-17 | 🔴 **ENMENDADA EL MISMO DÍA — su hipótesis final quedó DESMENTIDA por `[D-091]`** (la rúbrica no pide tres cosas para `FIX`: pide dos, y el tono no es un renglón), y su *"línea base de 60 frases"* es **falsa por omisión**: nunca se guardaron, ver `[L-076]`. Sigue en pie todo lo demás. 🧪 **Los evals arrancan por la FORMA de la rúbrica, no por el veredicto: `GRAMMAR_RUBRIC` pide SIETE cosas y se empieza por las CUATRO que comprueba un programa sin opinar** —primera línea `OK`/`FIX` a secas, nada de markdown ni viñetas ni comillas, dos frases como mucho, y que `OK`/`FIX` no se le escapen al alumno—. Las otras tres (si el veredicto acierta, si corrigió uno o tres, si se fue del tema) piden etiquetar las 60 frases a mano o leerlas. **Contra:** empezar por el veredicto, que es lo que suena a eval de verdad. 🔑 **Y las mecánicas no son las fáciles, son las que se van a romper:** `[D-049]` baja a Sonnet 5 y luego a Haiku 4.5, y un modelo pequeño **no deja de ver** que una frase A1 está mal —gramática de primer año—; lo que se le va es **la forma**, y la forma **sale a la pantalla** porque `app/static` pinta el mensaje tal cual. 🚨 **Y por el camino apareció un agujero de observabilidad que vale más que el eval, verificado en disco:** `split_verdict` (`tools.py:601`) hace lo correcto cuando el modelo rompe el formato —no da el punto, enseña el mensaje entero— **pero no se lo cuenta a nadie**, y la traza escribe `correct: bool`, así que *"el juez rompió el formato"* y *"el alumno se equivocó"* llegan al cuaderno **como el mismo `correct=False`**. Dos causas opuestas, un número, y arreglos en direcciones contrarias: uno a la rúbrica, el otro a la clase de inglés. Es `LM.15` dentro del paso que se llama Observabilidad — **no da un dato falso, da uno AMBIGUO**, y la ambigüedad no se ve en la gráfica. 📌 **Escrito y NO cableado:** que la ruta llame al corrector y la traza apunte el fallo es un cambio en `app/api.py` y se decide aparte. 🚨 **La excepción de `[L-057]` NO se hereda, y es lo más fácil de copiar mal:** `measure_tutor.py` sube el `read` a 30 s porque **está midiendo ese tope**; este eval mide la forma, no el reloj, así que usa el `read` de producción (6,5 s) — lo que interesa es la rúbrica **tal como la vive la app**. ⚠️ Precio dicho antes de correr: una llamada que cruce los 6,5 s deja de dar muestra, **no en silencio** —el guion para y el informe avisa de tanda parcial—. 🔍 **El obstáculo real, resuelto sin tocar producción:** `judge_grammar` devuelve `GrammarVerdict`, o sea **tira la primera línea**, que es justo lo que mide la promesa 1 — resuelto heredando del `RecordingClient` que ya existía y apuntando el texto crudo al pasar, **por el parámetro `client` que ya usan los tests**; cero cambios en `app/tools.py`, y el precio de repetir `tools.py:542` **atado con un test** que exige el mismo veredicto por las dos vías, con y sin bloque `thinking` delante. 💰 **Freno del gasto ajustado al plan: 60 llamadas, ni una más** (`measure_tutor` deja 82 porque su tanda se recorta sola) — 🔑 **un tope ajustado caza el bucle roto en la llamada 61; uno holgado veintidós después, y esas veintidós ya se pagaron.** ⚠️ **Lo que el eval NO puede decir va IMPRESO en su salida, no solo en el docstring:** limpio significa *"contestó con la forma pedida"*, **nunca** *"juzgó bien"* — `LM.20`, quien lea la salida pegada en un chat no abre el archivo. ⏳ Y el número **solo vale comparado consigo mismo**, así que la línea base se toma **antes** de bajar de modelo, como `[D-079]` selló antes de mirar. 🔻 **VISTO MORDER — trece sabotajes con su rojo, `445 → 501` tests**, incluidos el alambre contra la deriva (rojo al quitarle el `.upper()` que `split_verdict` sí hace) y `PROMISES` con una quinta promesa muda. 🔑 **Y uno de mis sabotajes salió VERDE porque el roto era el sabotaje:** escribí *"medicion"* sin tilde para probar el freno de `[L-001]` — repetido con tilde de verdad, `UnicodeEncodeError`. **Un sabotaje que no rompe nada no es un sabotaje**, familia del que rompe la carga en `[D-086]`. 📖 **LÍNEA BASE MEDIDA — Opus 5, 2026-08-17 21:43:47 → 21:46:56 UTC, 60 de 60 llamadas y ninguna cortada:** `bad_first_line` **0**, `leaks_keyword` **0**, `has_markdown` **5**, `too_many_sentences` **18** — **limpias 40 de 60**. Estimado `60 × $0,00304 = $0,1824`; el real se lee en la consola (regla 6). 🚨 **Y el resultado acusa a la RÚBRICA, no al modelo, con el argumento ya escrito en `tools.py:38-39`** (*"con Opus, un veredicto malo solo puede acusar a la rúbrica"*): es el modelo más capaz saltándose *"at most two short sentences"* 18 veces, y el `bad_first_line` a **0** descarta que sea incapacidad de seguir instrucciones — **falla la promesa del largo, y solo esa.** 🔍 **Hipótesis SIN COMPROBAR (regla 6):** una corrección natural son dos frases —la arreglada y la explicación— y el tono cálido que la rúbrica **también** pide añade la tercera; si es eso, **la rúbrica pide dos cosas que compiten** y el modelo elige el tono. 🔴 **HUECO DEL INSTRUMENTO, visto al leer su propio resultado: la corrida cuenta y TIRA la evidencia** — no guarda las respuestas, así que el `18` no se investiga sin **volver a pagar `$0,18`**. Es `[L-071]` (*cuadrar contra un agregado no es cuadrar*) cometido en un instrumento nuevo **el mismo día que se citó la lección**, y lo caro es cuándo se nota: el número sorprendente llega **después** del gasto. ✅ **HIPÓTESIS CONFIRMADA con el texto delante — corrida de diagnóstico de 10 frases, 2026-08-17 21:54 UTC, `$0,03`**, guardando las respuestas en `data/eval_replies.jsonl` y eligiendo **las 10 que habían fallado**, no diez al azar: **volvieron a fallar las 10** (reproducible, no ruido). El patrón de las nueve de `too_many_sentences` es siempre el mismo — **[aliento] + [frase corregida] + [explicación] = TRES frases**; real, frase 4: *"Almost there! Say: They are my friends. With they, we use are, not is."* 🚨 **La rúbrica se pide tres cosas y le da sitio para dos:** pide *"warm, encouraging"*, pide la frase corregida, pide nombrar el error, y luego *"at most two short sentences"*. **No es que el modelo desobedezca: las dos instrucciones no caben juntas**, y elige el tono, que es lo que la rúbrica pone primero. 📌 Comprobado a mano que no es artefacto del contador: **3 cierres exactos** y son 3 frases de verdad. 🔴 **Y el mismo diagnóstico cazó un FALSO POSITIVO en mi instrumento:** la frase 14 —correcta— salió `has_markdown` por *"you used "going to" for the future perfectly"*, donde las comillas **nombran una expresión, no envuelven una corrección**, y la rúbrica prohíbe *"no quotation marks **around the correction**"*. 🔑 Mi comprobación es **más estricta que la regla que dice comprobar**, avisado en su docstring como *"la parte basta"* — se investigó y era de más. ⚠️ **Así que el `5` de `has_markdown` es un TECHO, no una medida.** 🔴 **Tercer fallo, solo visible corriendo: la cuenta imprimía `[12/10]`** — se mezclaba el número de frase con la posición en la tanda; coinciden en la tanda entera y no en una parcial. Corregido a `[ 6/10] frase 12`. 🔻 **ABIERTA — lo que NO se decide aquí y espera FIRMA del usuario** (preguntado al final de la sesión, sin contestar, **nada tocado**): (1) **¿sube el tope a TRES frases** en `GRAMMAR_RUBRIC` y en `rubric_check.MAX_SENTENCES`? — el argumento a favor sale de la propia rúbrica: su razón escrita para el dos es *"A1 learners give up when a reply is a list of everything they did wrong"*, o sea el miedo es a una **lista de errores**, no a la longitud, y de eso ya se encarga *"never correct more than one thing at a time"*: **el tope de dos hace un trabajo que otra promesa ya hace y a cambio rompe el tono que la rúbrica pide en su primera línea**; (2) **¿se afina la comprobación de comillas** a solo las que envuelven una corrección, o se endurece la rúbrica para prohibirlas todas? 🚨 **Y antes de tocar la rúbrica, no después: cambiarla CADUCA el `$0,00304`** (`measure_tutor.py:85-88`, *"`GRAMMAR_RUBRIC` ya lo movió una vez sin que nadie se enterara"*) — el coste por llamada dejaría de estar **medido**, y con él el tope de las tandas. Ver `[L-059]`. 🔴 **Segundo fallo, `PI-4` cobrando limpio: el guion no arrancaba** — le faltaba `config.load_env_file()` (que `measure_tutor.py:407` sí tiene) y moría sin llave antes de llamar a nadie, **con los 19 tests en verde**, porque ninguno llama a `main()` (hace red). 📌 Nadie lo vigila: `tests/test_measure_tutor.py` tampoco tiene freno | `app/rubric_check.py`, `eval_rubric.py`, `tests/test_rubric_check.py`, `tests/test_eval_rubric.py`, `measure_tutor.py` (importado, no tocado), `app/tools.py` (leído), `[D-049]`, `[D-079]`, `[D-085]`, `[D-086]`, `[D-087]`, `[C-009]`, `[L-001]`, `[L-023]`, `[L-043]`, `[L-048]`, `[L-057]`, `[L-059]`, `[L-073]`, `[L-075]`, `LM.15`, `LM.20`, `PI-8`, paso 9 |
| D-088 | 2026-08-17 | 🛑 **`T-103` se PARA con disparador de acción —igual que `T-102`—: NO se pone hoy el `if` protector, porque no se puede ver morder.** 🔍 **Verificado en disco, no razonado:** el camino del timeout termina en `raise HTTPException(504)` en **`api.py:804`** y el bloque que lee `tutor_started[0]` está en **`api.py:906`** — la 906 va **después** de la 804. `attempt.cancel() == True` deja la lista vacía, sí, pero **por ese camino nadie la lee**: no hay entrada que provoque el `IndexError`, así que no hay test que lo cace ni rojo que enseñar. Un `if` ahí es `[L-048]` exacto —*un guardián que se cumple solo es peor que ninguno, porque además tranquiliza*— y encima marcaría la tarea como cerrada. **Contra:** ponerlo hoy, que era mi propuesta y la presenté como *"lo único de código listo para arrancar"*. 🔍 **La salida que SÍ mordería, escrita para cuando llegue el disparador:** no proteger la línea, sino **llamar al bloque de la traza con `tutor_started` vacía, ver el `IndexError` de verdad, y entonces poner el freno** — descartada hoy porque fabricar ese escenario exige inventar un camino que el código no tiene, y eso prueba el andamio. ✅ **Lo que ya está hecho, que es lo que le toca a una nota: el aviso en los DOS sitios con la salvedad dentro** — `api.py:892-897` (*"Ese camino no escribe traza hoy"*, nombrando la línea a mirar primero) y el docstring de `tests/test_api.py:690-693`, que dice lo que ningún test puede decir de sí mismo: ***"el día que la escriba, este test seguirá en verde y no avisará"***. 🔴 **El error que precedió es mío, de resumen y no de código: el reporte de arranque se comió la salvedad** y presentó el `IndexError` como bicho vivo del presente cuando es condicional a futuro. 🔑 **El documento era mejor que su resumen** —misma forma ya anotada para la sesión 54— **y peor aquí, porque el resumen es lo que se lee al arrancar el día y el documento no.** 🚨 **Quién firma, que es la mitad del asunto:** había **dos votos técnicos** verificados contra el disco —esta terminal y la auditora— y eso **no es la decisión**; `PI-6` pone la firma en quien lleva el proyecto, no en la sesión que construye ni en la que audita. Se pidió explícitamente y el usuario la dio | `T-103`, `T-102`, `[D-087]`, `[L-048]`, `[L-064]`, `[L-065]`, `[L-069]`, `PI-6`, `PI-7`, `app/api.py` (804, 892-897, 906), `tests/test_api.py:682-693`, paso 9, auditoría externa del 2026-08-17 |
| D-087 | 2026-08-17 | ⏱️ **El tiempo de la práctica se parte en TRES —`queue_seconds` + `model_seconds` + `rest_seconds` = `seconds`—, y NO en las cuatro fases de `tools.py`, que no se pueden medir.** 🔴 **`connect`/`write`/`pool`/`read` son TOPES, no medidas:** `anthropic.Timeout(...)` es un presupuesto que se le **entrega** a la librería —cuánto se les *permite* durar—, y `[D-073]` calculó `read` **restando de ese presupuesto**, no cronometrando. Verificado en el disco en las **dos** librerías del `.venv`: `httpx 0.28.1` y `httpx2 2.9.1`, ambas `_client.py:157`, **un solo `elapsed`** y es el total de la respuesta. **No hay salida por fase en ninguna parte de la cadena.** ⚠️ **`[D-085]` queda ENMENDADA en el sitio, no matizada debajo:** su frase *"la arquitectura ya piensa en fases; el registro no las escribe"* es cierta palabra por palabra y engaña en conjunto —se lee como que los números existen—, y **la propuesta de las cuatro fases nació de leerla**. Una regla con asterisco se sigue leyendo como regla. ⏱️ **Por qué TRES y no dos:** el reloj de la ruta arranca **antes** del `submit` a propósito (`[L-013]`, se mide lo que espera la persona), así que `total − modelo` es *"cola + nuestro código"* revuelto — **con los hilos ocupados la cola se dispara y el descenso de `[D-049]` parecería inútil cuando el culpable sería la cola**, que es exculpar al modelo por el motivo equivocado. 🏗️ **Dónde se mide cada uno:** la cola en `api.py` con un **cierre POR PETICIÓN** (no una global: dos prácticas a la vez se pisarían el número **en silencio**); el modelo con un reloj alrededor de la línea `judge_grammar(sentence)` en `respond`; el resto **se CALCULA en `record`, nunca se recibe** —recibirlo dejaría mandar tres números que no cuadran con el cuarto—. 🔑 **`GrammarVerdict` NO se toca**, y ese fue el hallazgo que ahorró el trabajo: `respond` ya tiene la llamada aislada en una línea, así que **la nota sube UN piso, no tres**. 🔴 **Mis dos errores, los dos corregidos por la auditoría:** (1) defendí la pureza de `TutorReply` cuando **tres de sus cinco campos ya no venían del juez** desde `[D-066]` — y lo que me llevó al error estaba en el código: **el docstring decía *"en tres piezas"* y ya eran cinco**; corregido, junto a la cabecera de `tests/test_trace.py`, que enumeraba tres tests de cinco. **Una caja que se describe más pequeña de lo que es invita a defenderle una pureza que ya perdió.** (2) propuse medir dentro de `judge_grammar`, tres pisos de viaje. 🔻 **VISTO MORDER — el alambre de `[L-073]` se puso rojo solo** (`Extra items in the left set: 'model_seconds'`), **segunda vez**, y se siguió su instrucción: escribir primero quién vigila el campo, **después** tocar el conjunto. Tres sabotajes con su rojo: `model_seconds=0.0` → `assert 0.0 >= 0.05`; reloj abrazando `respond` entera → `assert 0.151 < 0.15`; `queue_seconds=0.0` → `assert 0.0 >= 0.2`. 🔑 **El segundo justifica la cota de ARRIBA**, que no es obvia: un reloj demasiado ancho también sube y baja con el juez, así que pasaría cualquier test que solo mirase la cota de abajo. **El tercero explica por qué el test fabrica una cola de verdad: con el pool libre el cero es un valor plausible**, que es lo que hizo invisible el sabotaje de `correct`. **452 → 456 tests.** ⚠️ **Lo que NO cierra:** en el camino del timeout con `cancel() == True` la lista de la marca está **vacía**; ese camino no escribe traza hoy, y si algún día la escribe un `IndexError` perdería la fila entera por un campo — el aviso está en `api.py`, encima de la línea, porque un test en verde no avisa de un camino que no existe | `[D-085]`, `[D-086]`, `[D-049]`, `[D-073]`, `[D-066]`, `[L-013]`, `[L-073]`, `LM.20`, `app/english_tutor.py`, `app/api.py`, `app/trace.py`, `tests/test_english_tutor.py`, `tests/test_trace.py`, `tests/test_api.py`, paso 9, auditoría externa del 2026-08-17 |
| D-086 | 2026-08-17 | 🧪 **Dos frenos escritos ANTES de la primera línea de la traza: el test prueba el COMPORTAMIENTO, y el fallo de la traza no puede tumbar la práctica pero tampoco puede callarse.** 🎯 **(1) El test NO comprueba que la ruta sea una función.** Yo había prescrito `callable(config.trace_file)`, y eso vigila **la implementación que hoy creo que evita el fallo**. El fallo real es *"la ruta no siguió a `TEAPP_DATA_DIR`"*, y la constante de módulo es **solo una de sus formas**. Se prueba **moviendo `TEAPP_DATA_DIR` y comprobando que la ruta de la traza se movió con él**. 🔑 Es la doctrina del propio portero, escrita por él: *"no pregunta quién escribe ni por qué. Pregunta si `data/` cambió."* Y hay precedente en la suite: `check_no_data_writes.py:116`, que corre **con el desvío puesto** y por eso caza al vigilante que se cuelga de `config`. ✅ **VISTO MORDER, y el primer sabotaje desmintió a esta misma entrada:** predije que la constante de módulo pondría el test en rojo — **no**: `require_data_dir()` corre al importar, no hay `TEAPP_DATA_DIR`, y la suite **no arranca** (`ImportError` en `conftest.py`). Es `[D-037]` cobrando de más —la forma "constante" no es un fallo cazable, es un programa que no existe— pero **no demuestra el test, porque el test no corrió.** 🎯 El sabotaje **alcanzable** sí: una **caché** (`if _TRACE_CACHE is None`) arranca bien y da **`1 failed, 17 passed`**; restaurado, **440 passed**. Y el mensaje reveló el daño real: la ruta cacheada apuntaba a la carpeta temporal de **otro test** — una ruta congelada **se filtra de un test al siguiente**. 📌 **Un sabotaje que rompe la carga no es un sabotaje:** parece más contundente y demuestra menos. 🚨 **(2) Qué pasa si escribir la traza falla** —disco lleno, permisos, un `json.dumps` con un valor raro—, con las dos salidas malas nombradas: **si tumba la petición**, el instrumento rompe lo que mide y alguien pierde su práctica porque el registro no pudo escribir — es `T-054` otra vez, la báscula estropeando los datos que medía (`[L-023]`); **si falla en silencio**, es `LM.15` exacto (abierta en `Edu_TripleS/LESSONS.md:3424` antes de citarla, y **nació en TEAPP cerrando `T-054`**): *un instrumento ciego no da un dato falso, da silencio, y el silencio se lee como confirmación* — un día la traza lleva semanas sin escribir y el tablero dice *"pocas prácticas"* en vez de *"no estoy viendo nada"*. ✅ **La salida ya está montada y no cuesta nada: el fallo de la traza NO propaga —la práctica se sirve igual— y se anota con el `logger.error` que ya existe.** Así los dos registros se cubren mutuamente: **el estructurado cuenta el caso feliz; el de prosa cuenta cuando el estructurado se rompe.** Es la red de seguridad puesta en quien llama y no dentro de la herramienta. 📌 Formato y sitio, por `PI-2`: **un solo `trace.jsonl`** que se abre en modo añadir, dentro de `data/`, con su ruta resuelta por `trace_file()` como las otras tres. Nada de rotación ni de por-día hasta que haga falta. 🔻 **VIVO — hueco de `PI-4` aplazado con disparador, decisión del usuario:** la traza se ha visto escribir con `TestClient` y el juez de mentira, **nunca con el servidor levantado y una llamada real**. **Disparador: la primera llamada real del descenso de modelo** (`[D-049]`) — se mira que `trace.jsonl` tenga su línea con el `model` nuevo dentro, que de paso comprueba que `MODEL_NAME` llega al cuaderno sin copiarse a mano. Se monta encima de un gasto ya decidido en vez de pagar ~`$0,003` aparte de un saldo que `[C-009]` declaró compartido | `[D-085]`, `[D-037]`, `[L-023]`, `[L-020]`, `LM.15`, `LM.13`, `app/config.py`, `app/api.py`, `tests/test_config.py`, `tests/conftest.py`, `tests/check_no_data_writes.py`, `PI-2`, `PI-4`, paso 9, auditoría externa del 2026-08-17 |
| D-085 | 2026-08-17 | 👁️ **El paso 9 arranca por OBSERVABILIDAD, y la traza guarda la FORMA de la práctica, nunca la frase — con la fila que `.gitignore` no puede defender ascendida a `PI-8`.** 🔀 **Orden del paso 9, decidido por el usuario:** observabilidad → evals con rúbrica → descenso de modelo (`[D-049]`) → seguridad. **Contra** mi propuesta de empezar por evals, que **descarté la observabilidad sin decirlo** (`PI-1` incumplida). El descenso va en medio porque es lo que los evals existen para medir. 🔍 **El hueco, verificado en el disco, no supuesto: `app/api.py:838` termina la práctica exitosa en `return PracticeResponse(...)` sin escribir una línea.** El log tiene `error`/`warning` para averías y frenos, y `info` para la cuota agotada — **el suceso más frecuente, que la app funcione, es invisible.** 🤝 **Y el hallazgo aguantó dos instrumentos sin fuente común:** esta terminal leyendo `api.py`, la auditora interrogando su propio registro. Mismo cruce que `[D-058]` (consola `$0,02` contra tokens × lista `$0,0234`). 📊 **LA TRAZA — forma, nunca la frase:** usuario, hora, nº de palabras, puntuación, prácticas, **`correct` (booleano)**, segundos, modelo. Vive en `data/`, que `.gitignore` sí cubre. ⏱️ **El reparto del tiempo lo aporta la auditora y es el campo que salva el paso 9:** *"cuánto tardó"* a secas no distingue *"el modelo es lento"* de *"la red es lenta"*, y llevan a arreglos opuestos — si `[D-049]` baja a Sonnet y Haiku, eso **solo acelera la parte del modelo**. `app/tools.py` ya parte el presupuesto en `connect`/`write`/`pool`/`read`. 🔴 **ENMENDADO el 2026-08-17: aquí seguía *"la arquitectura ya piensa en fases y el registro no las escribe"*, y eso se lee como que los números existen. NO EXISTEN — son TOPES, no medidas**, y `httpx 0.28.1` y `httpx2 2.9.1` dan **un solo `elapsed`** cada una, el total de la respuesta. El reparto que sí se puede medir es `[D-087]`: **cola / modelo / resto**. ⚠️ Su `20,7 s / 59 s` es de otro sistema: **el principio viaja, el número no.** 📌 **La frase se APLAZA con la razón escrita, y no es una patada:** no sabemos si hay alguien de quien recolectar —esa es la pregunta 1 de la traza—, y `measure_tutor.py:292` ya trae **60 frases A1 escritas a mano**, *"unas correctas y otras con un error claro"*, que es un conjunto de casos elegidos a propósito y no un plan B. 🔴 **Aquí me equivoqué dos veces y las dos las corrige la auditora:** (1) cité `[D-060]` contra inventar frases — mal aplicada: `[D-060]` era un número que **aparentaba estar medido** saliendo de un `len()`, no un conjunto de prueba diseñado; (2) prescribí *"desviar la ruta de la traza en `conftest.py`, acordándose en el mismo cambio"* — **eso es el mundo anterior a `[D-037]`**: `conftest.py:81` desvía **una** variable (`TEAPP_DATA_DIR`) y `users_dir()`/`quota_dir()`/`accounts_file()` cuelgan de `require_data_dir()`. No hay tres sitios que desviar ni habrá cuatro, y **poner un "acuérdate" encima de una estructura que ya lo resuelve reintroduce el mecanismo que `[L-023]` costó quitar.** ✅ **La condición que SÍ hay que escribir es otra, y es comprobable: la traza resuelve su ruta LLAMANDO a una función, nunca en una constante de módulo** — una constante se congela al importar, antes de que `monkeypatch` corra, y ahí sí se escapa (lo dice `conftest.py:78-80`). 🚨 **Y sigue en pie que el portero de `T-071` NO cubre este flanco:** `no_data_writes.py` vigila que **la suite** no ensucie `data/`, y él mismo documenta su punto ciego —*"lo que corre fuera de pytest… uvicorn levantado a mano… y el portero ni se entera"*—, que es **el modo normal de la traza**. Quien da la privacidad es `.gitignore`, no el portero. 🔒 **TERCERA FILA, la que ninguna herramienta defiende → asciende a `PI-8` en `CLAUDE.md` + casilla en `protocol-close`:** ninguna frase de ninguna persona entra en `_persistence/`, ni como ejemplo. `_persistence/` **no** está en `.gitignore` y el repo es **público** (`[C-007]`). 🔑 **Por qué no basta `decisions.md`: `LM.20`** (verificada en `Edu_TripleS/LESSONS.md:3673` antes de citarla) — *"una copia correcta que nadie alcanza"*. `decisions.md` se lee cuando alguien va a buscarlo; `CLAUDE.md` se lee sin buscarlo. 📌 **Y queda escrito que `PI-8` es más débil que `PI-6`/`PI-7`: una casilla PREGUNTA, no detecta.** Fingir que muerde sería marcarla con una intención | `[C-007]`, `[C-009]`, `[D-049]`, `[D-037]`, `[D-073]`, `[D-060]`, `[D-058]`, `[L-023]`, `[L-020]`, `[L-069]`, `LM.20`, `CLAUDE.md` (`PI-8`), `protocol-close` (Paso 5 y Paso 7), `app/api.py:838`, `app/tools.py`, `app/config.py`, `tests/conftest.py`, `tests/no_data_writes.py`, `measure_tutor.py`, paso 9, `PI-1`, auditoría externa del 2026-08-17 |
| D-084 | 2026-08-17 | 💰 **SALDO LEÍDO: `$6,24 US$`, 2026-08-17 16:05 UTC — el disparador de `[D-081]` queda descargado ANTES de la primera llamada del paso 9. Y la resta NO cuadra: hay un hueco de `$0,09–0,13` fuera de `teapp-measure`.** 🕒 **La hora se fijó antes del número**, como manda `[D-079]`, y se fijó una sola vez para las dos lecturas del día. ✅ **El techo predicho aguantó:** antes de leer se escribió *"$6,35 es un TECHO, no un saldo"* y la lectura cayó por debajo — la predicción se hizo pública antes del clic, no después. 🧮 **La resta, con los redondeos al céntimo dentro y no a punto fijo:** gasto desde el 11 = `$0,30–0,32`; `teapp-measure` del 1 al 17 = `$0,19–0,21` (**solo dos días con gasto: ago 13 `$0,02` y ago 14 `$0,18`**); **hueco = `$0,09–0,13`**, unas **29–45 llamadas** al perfil medido. 🚨 **Y el hueco vive en el ESPACIO `Default`, que es el único que NO admite tope de gasto** (`[D-059]`, cita de Anthropic: *"You cannot set limits on the Default Workspace"*). Esto es `[C-008]` —medir y servir del mismo bolsillo— dejando de ser teórico por segunda vez. 🔍 **Candidato principal, y es barato de comprobar: `T-079`.** Sus 10 llamadas costaron `$0,02` (`[D-058]`, leído) y corrieron el **2026-08-11** — el día antes de que `teapp-measure` existiera (`[D-061]` lo crea el 12), así que **cayeron en `Default`**. Si corrieron después de la lectura de `T-080` ese mismo día, están dentro del hueco. **Explican `$0,02` de `$0,11`: no lo cierran.** 📌 **Lo que esta entrada NO afirma:** no dice qué gastó el resto. `$0,11` no es alarmante en dinero; lo es en forma — es `T-096` otra vez y **cinco veces más grande**, en el espacio sin freno. 🔴 **Corrige una premisa de `[D-079]`, que mandó descontar *"las sondas de `check_api_key.py` (13 de agosto)"* dándolas por debajo del céntimo: la consola dice `$0,02` el día 13**, y `1.834` entrada + `338` salida ÷ `361+5×49` = **~5 llamadas COMPLETAS del tutor, no sondas**. 🎯 **Con eso `T-096` deja de ser "5 llamadas en algún día de la semana" y pasa a estar fechada: el 13.** Hipótesis **sin comprobar**: el 13 es el día de `T-087` (saturación), y `[D-075]` documenta que los dos `except` del bucle hacen `break` — una tanda cortada a mitad hace unas pocas llamadas completas y se va. **Contra:** abrir el paso 9 y perseguir el hueco después —descartado hoy: el hueco se lee gratis y `[D-041]` ya falló una vez por aplazar un clic de dos minutos. ✅ **RESUELTO el mismo día, y no era un bicho: el usuario confirmó que la cuenta paga TAMBIÉN su estudio de programación con agentes de IA** — tercer inquilino del saldo, invisible en la vista de COSTO (*"solo uso de API"*), exactamente la trampa pre-registrada por `[D-079]`. El límite real queda en `[C-009]`; `T-096` se cierra sin bicho. 🔴 **Y el proceso salió mal aunque el hallazgo saliera bien: se pidieron TRES tablas de consola antes de preguntar lo único que lo resolvía —*¿qué más corre con esta cuenta?*—.** El instrumento se usó tres veces para responder algo que el dueño de la cuenta sabía de memoria. Ver `[L-072]` | `[C-009]`, `[L-071]`, `[L-072]`, `[D-081]`, `[D-079]`, `[D-078]`, `[D-061]`, `[D-059]`, `[D-058]`, `[D-057]`, `[D-041]`, `[C-008]`, `T-096`, `T-079`, `T-080`, `T-087`, `T-095`, espacio `Default`, regla 5, regla 6, auditoría externa del 2026-08-17 |
| D-083 | 2026-08-17 | 📜 **`PI-6` y `PI-7` entran en `CLAUDE.md`, copiadas del verbatim de `GUIDE.md` §11.i (`Edu_TripleS`, líneas 1787-1794) y NO de una paráfrasis.** `PI-6`: ante un test rojo se arregla el código; tocar un test exige autorización explícita **del humano**, con la razón escrita. `PI-7`: **pide** el refactor de forma explícita, cada ciclo. 🚨 **La paráfrasis que llegó primero perdía las tres cosas que hacen el trabajo**, y por eso se pidió el original antes de escribir: (1) *"del humano"* — sin el actor, la regla la puede autorizar la propia sesión que construye, que es como no tener regla; (2) la regla 2 venía **en pasiva** (*"el refactor se pide"*), y en pasiva el actor se invierte — el original es imperativo dirigido al agente; (3) los porqués `LM.43`/`LM.44` y la frase *"la salida barata siempre gana"*. 🔍 **Y §11.i no terminaba en las dos reglas: traía las dos comprobaciones que las hacen exigibles**, que también faltaban — el **diff de los tests mirado aparte** del diff del código (un test ablandado solo se ve ahí) y **que el rojo existiera** (un test que nunca falló no se distingue de uno vacío mirando el verde). Sin la primera, `PI-6` es una nota. **Contra:** escribirlas desde la paráfrasis —descartado, es `[L-069]` en vivo: un dato copiado de segunda mano al que se le cae el trozo que trabaja. 📌 Citadas como `LM.nn` con el repo nombrado, por el solape de prefijos que ya cobró `[L-034]` | `CLAUDE.md` (`PI-6`, `PI-7`), `[D-082]`, `[L-068]`, `[L-069]`, `[L-034]`, `[L-048]`, `[D-060]`, `PI-3`, `PI-4`, `T-100`, `GUIDE.md` §11.i, auditoría externa del 2026-08-17 |
| D-082 | 2026-08-17 | 🧪 **El disparador del paso 9 deja de ser un comentario y pasa a ser un test: se clava el PAR `(MODEL, LAB_REQUESTS_PER_MINUTE)`, no la mitad.** El test que existía para vigilar el acoplamiento de `[L-047]` clavaba solo el `50`, así que **el escenario exacto que `[D-081]` manda vigilar —cambiar `MODEL` sin tocar el número— dejaba los 440 en verde y al portero mudo**. Y `[D-049]` lo tiene programado **dos veces** dentro del paso 9 (Sonnet 5 y Haiku 4.5). 🔻 **Visto morder:** `MODEL = "claude-sonnet-5"` con el 50 intacto → `1 failed, 439 passed`; restaurado → **440 passed**. **Contra:** dejarlo como comentario (descartado: es `[L-065]` otra vez —un aviso presente se lee como cobertura— y `[D-081]` ya lo había escrito confiando en que alguien lo leyera); y hacer que el test consulte la consola de Anthropic (descartado: gasta una llamada por corrida y ata la suite a la red). 📌 **Lo que esta decisión NO dice:** el test **no** verifica que el 50 sea el límite real del modelo de hoy — no lee la consola. Verifica que nadie mueva media firma sola. El clic sigue siendo humano; lo que cambia es que ahora hay un rojo que lo exige. ⚠️ **Y el rojo necesita instrucción al lado**, o la salida cómoda es editar el test: el comentario de `MODEL` ahora nombra el test y dice explícitamente que el arreglo es la consola, no el assert | `[D-081]`, `[D-049]`, `[D-061]`, `[L-047]`, `[L-050]`, `[L-065]`, `T-088`, `T-099`, `deploy/check_api_key.py`, `tests/test_check_api_key.py`, auditoría externa del 2026-08-17 |
| D-081 | 2026-08-14 | 🏁 **EL PASO 8 CIERRA, con las cuatro miradas de `[D-080]` hechas: `T-089` ✅ cerrada midiendo, `T-079` 🟡 condición viva con disparador, `T-081` 🔲 aplazada con motivo, `T-088` ✅ DESARMADA.** 🚨 **Queda UNA pendiente, no dos:** `T-088` no quedó pendiente, quedó desarmada — una tarea sin disparador espera, una con disparador en el calendario es un bloqueante disfrazado (`[L-064]`). 🔑 **Lo que `[D-080]` decidió con UN dato ahora tiene DOS DE DOS, y de la misma forma exacta:** `install.sh` y `check_api_key.py`, dos archivos distintos con un solo defecto — un aviso correcto sobre una puerta, a pocas líneas de una línea que niega la otra. La regla que sale gobierna el paso 9 y vive entera en `[L-065]`. 🔻 **DISPARADOR: antes de cambiar `MODEL` — CADA VEZ — leer en la consola el límite por minuto de ese modelo en `teapp-measure` y ponerlo en `LAB_REQUESTS_PER_MINUTE` en el mismo cambio.** 🔴 Corregido el 14: esta fila decía *"la primera acción del paso 9"*, dando por hecho que el paso 9 es bajar a Haiku — `_context/roadmap.md:23` lo titula **"Observabilidad y evals con rúbrica"** y `[D-049]` mete ahí el descenso a **Sonnet 5 y Haiku 4.5**, dos modelos. El disparador es la ACCIÓN, no la fecha. 📌 Vivo sin bloquear: saldo de `[D-057]` antes del próximo bucle de llamadas, `T-086`, y `T-098` (armada, disparador = próximo arranque) | `[D-080]`, `[L-064]`, `[L-065]`, `[D-077]`, `[D-057]`, `T-088`, `T-081`, `deploy/check_api_key.py`, auditoría externa del 2026-08-14 |
| ~~D-080~~ | 2026-08-14 | ✅ **CUMPLIDA el 2026-08-14 por `[D-081]`: su mandato —mirar las cuatro pendientes una por una— se ejecutó entero y el paso 8 quedó cerrado. 🚨 NO es una decisión abierta**, y como tal se reportó el 2026-08-14 (ver `[L-066]`). No estaba equivocada: se acabó de cumplir. Decía: 🚦 **El paso 8 NO se declara cerrado hoy (`T-090`), y `T-079` pasa a primera tarea del próximo día.** Se eligió contra la alternativa de cruzar ya al paso 9 dejando las cuatro pendientes como remates. 🔑 **El motivo no es la lista de pendientes, es lo que pasó al mirar una:** `T-089` estaba clasificada como cosmética (*"el mensaje de error recomienda una forma insegura"*) y al medirla en doce segundos resultó ser **clase de seguridad, con corrida detrás** (`[L-061]`). Una de cuatro cambió de categoría al tocarla → **declarar el paso cerrado sin mirar las otras tres era declararlo a ciegas.** ✅ Cerradas hoy con eso: `T-089` y `T-097`. Quedan `T-088` (cosmética de verdad, depende de bajar a Haiku en el paso 9) y `T-079`. ⏳ **Por qué `T-079` NO se abrió hoy pese a ser la que manda:** una auditoría externa pide quitarle el ✅ por estar cerrada por inferencia, y eso obliga a abrir `[D-077]` y sostener una discusión con evidencia propia. Era la **cuarta sesión del día**. 🔑 `[D-041]` falló en la sesión 54 exactamente así: no por un mal argumento, sino porque la sesión se acabó antes de llegar al clic. **Empezar una decisión que pide evidencia con el día gastado es cómo se toman las decisiones cansado.** 📌 Lo que sí se hizo antes de cerrar fue lo que ya estaba **escrito y sin verificar** (`sudo -E` contra el `env_reset`), que es distinto: dejar dormir una instrucción sin comprobar es dejarla para que alguien la siga mañana | `T-090`, `T-079`, `T-089`, `T-097`, `T-088`, `[D-077]`, `[D-041]`, `[L-061]`, auditoría externa del 2026-08-14 |
| D-079 | 2026-08-14 | 🔒 **El criterio de `T-095` queda SELLADO antes de abrir la consola: banda, sitio, cuatro ramas y la hora.** 🔑 Después de ver el número, **arreglar el criterio y moverlo son indistinguibles** para quien lo lea luego — es `[D-074]` aplicado a una lectura en vez de a un gasto. 🎯 **BANDA: `$0,156 – $0,205`**, y no es un ±10% a ojo: el eslabón débil de `[D-078]` era el reparto entrada/salida, así que **se barre entero** — `$0,00234 × [f×1,4615 + (1−f)×1,1136]` da **$0,156** con `f=0` (todo salida), **$0,182** con `f=0,53` (`[D-058]` tal cual) y **$0,205** con `f=1`. ✅ **De regalo, robustez de `[D-078]`: el `$0,1404` viejo cae FUERA de la banda** — aunque el 53/47 estuviera del todo mal, no podía cuadrar. 📍 **Se lee el espacio `teapp-measure`, NO el total de la organización:** la báscula corre con la llave del laboratorio (`[D-061]`), y el total metería dentro el tráfico de producción. Línea base en pantalla del 2026-08-12: *"USD 0,00 de USD 2,00"* (`[D-062]`); a descontar las sondas de `check_api_key.py` y la llamada mínima de `[D-061]`. 🚦 **Cuatro ramas, y se pre-compromete la LISTA, no la conclusión** —ese fue el error de `[D-077]`—: 🟢 **A** dentro → `COST_PER_CALL_USD` pasa de derivado a **medido**; 🔵 **B** por debajo → caché de prompt o `[D-058]` alto de origen; 🟠 **C** por encima → **gasto ajeno**, se busca qué corrió con esa llave **antes de tocar ningún precio**; ⚪ **D** "sin datos" → 🚨 **eso NO es un cero**, se anota hora UTC y `T-095` sigue abierta. 🔴 **Corregido el encargo: en la rama B el dato NO está guardado** — `measure_tutor.py` no escribe nada en disco, así que `client.usages` murió con el proceso. ✅ **Sustituto mejor y gratis: la caché se descarta desde el CÓDIGO** — el *prompt caching* es opt-in vía `cache_control`, que **no aparece en ningún `.py` del repo**; si la consola muestra caché, **esa es la sorpresa, no la explicación**. 📏 Y se sella un matiz: `[D-058]` cruzó *"$0,02"* contra *"$0,0234"*, pero a resolución de céntimo `$0,02` es **±25%**; sobre ~$0,18 es **±2,7%** — esta lectura **sí mide ~9× mejor**, aunque no sea "6× más muestras de lo mismo". ⏰ **La hora UTC se anota ANTES de leer el número** — pero 🔴 **`T-086` NO se salda aquí, y esa parte del encargo se corrige**: dice *"la próxima lectura de **AWS**"*, y Anthropic es **otro bolsillo** (`[A-024]`: *"cuatro bolsillos distintos y no se mezclan — `[A-018]` ya se rompió una vez por juntar fuentes"*). Se toma el hábito, no el cierre: **ninguna lectura de costo se anota sin hora UTC**, sea de AWS o de Anthropic. 📖 **LECTURA PARCIAL del 2026-08-14, 15:08 UTC, dentro de la entrada — y `T-095` SIGUE ABIERTA.** ✅ **El día 14 está limpio AL TOKEN:** la consola dice `21.668 | 2.959` y `T-093` midió `21.668 | 2.959` — idénticos, ninguna llamada ajena, **no hay nada que descontar**. ✅ **Tarifas unitarias validadas contra un número LEÍDO:** la semana derivada da `$0,2004` y la consola dice **`$0,20`**, sobre un mix de **7,1:1** cuando `[D-058]` era **5,6:1** — no es circular. 🚨 **Y aun así NO cierra: el `$0,20` es de "últimos 7 días", no del día 14**; ese sigue derivado y la regla 6 lo prohíbe. Falta **un clic**: la barra del 14 en *"Costo diario de tokens"*. 🔮 **Dos predicciones selladas antes de ese clic, y NO son la misma:** derivación completa **$0,18–$0,19** (depende del modelo al 100%) y **por RESTA $0,177–$0,187** (el día 14 es el **91,2%** de una semana **leída**, así que el modelo solo pesa en el 9%) — **la segunda es más fuerte**, y si la barra cae entre `$0,177` y `$0,180` falla la primera y aguanta la segunda, lo que diría que las tarifas van algo altas. 🚨 **DOS VISTAS, DOS DEFINICIONES:** USO *"incluye API y Consola"*, COSTO *"solo uso de API"* — hoy no muerde porque el 14 no tuvo uso de consola, **pero el día que USO y COSTO no cuadren, la primera hipótesis es esta, no un error de cálculo**. ⏱️ Observación de UN día, no regla: el cargo apareció **el mismo día** (AWS tardaba ~24 h) — retardo real **sin medir, entre 0 y ~15 h**. 📌 Cabo suelto a `T-096`: **1.834 entrada + 338 salida ≈ $0,018** de la semana que el día 14 no explica, ~5 llamadas, y **no cuadran con las sondas anotadas**. ✅ **DESENLACE el mismo día: barra del 14 leída = `$0,18` → RAMA A, `T-095` CERRADA.** `COST_PER_CALL_USD` pasa de **derivado a MEDIDO** y `[D-058]` queda confirmada en su mecánica — el modelo de tarifas acertó **dos veces sobre números leídos** (semana `$0,2004`/`$0,20`, día `$0,1828`/`$0,18`). 📊 Coste por llamada medido = `$0,18/60 = $0,00300`, **y es un intervalo**: la consola redondea al céntimo, así que es `[$0,00292, $0,00308]`; 🔑 **la constante se queda en `0,00304` y no baja a `0,0030`** — los dos caen dentro, y **sigue siendo un freno**, así que dentro de lo que la medición permite se escoge el lado alto (el punto (c) de `[D-078]` sobrevive a la medición). 🚨 **Y lo que la lectura NO hizo: no discriminó entre las dos predicciones selladas.** Las dos se cumplen, y eso no es victoria doble sino falta de resolución — `$0,18` abarca `[$0,175, $0,185]` y pisa las dos franjas. Lección en `[L-060]` | `T-095`, `T-086`, `[D-078]`, `[D-077]`, `[D-074]`, `[D-062]`, `[D-061]`, `[D-058]`, `[D-046]`, `[A-018]`, `measure_tutor.py`, auditoría externa del 2026-08-14 |
| D-078 | 2026-08-14 | 💵 **El precio por llamada estaba CADUCADO: `[D-077]` mandaba comparar la consola contra `$0,1404`, un precio medido con una rúbrica que nosotros mismos borramos. La comparación correcta de `T-095` es contra ~$0,182 (+29,8%).** `[D-058]` midió `$0,00234` con **247 tokens de entrada**; `[D-066]`/`[D-067]` engordaron `GRAMMAR_RUBRIC` de **678 → 1.016 chars (+49,9%)** el 13 de agosto, y los tokens medidos subieron **247 → 361 (+46,2%)** — las dos cifras se persiguen. Nadie tocó `COST_PER_CALL_USD`. 🚨 **Y lo peor no era el desvío, era el otro lado:** `[D-077]` dejaba pre-escrito *"si cuadra, confirma `[D-058]` con 6× más muestras"* — **no puede: no son más muestras de lo mismo, es otra prompt**; si la consola dijera $0,14 sería la señal de que algo está mal. La otra rama mandaba a auditar `[A-010]`, el tope de 20 prácticas, que no pinta nada: **la tercera explicación estaba impresa en la salida de la propia corrida**. ➕ **`COST_PER_CALL_USD` sube a `0,00304` marcado como DERIVADO.** 🔑 La disyuntiva *"medido contra derivado"* **no existía**: `0,00234` tampoco es hoy un número medido. Y esa constante **no afirma, divide** — es la calibración de un freno, y **un freno se calibra para fallar hacia el lado seguro; una afirmación se escribe solo cuando se midió**. Con `0,00234` el tope dejaba **106 llamadas = $0,322 reales** contra $0,25 escritos: estaba **largo**, justo la dirección que el comentario del archivo prometía evitar. 📉 Y un lado sale gratis: el acantilado está en `$0,00416`, con `0,00304` caben **82** y la tanda de 60 entra entera. ➕ **El acantilado deja de ser comentario:** nuevo test `MAX_CALLS_PER_RUN >= TARGET_SAMPLES` — sin él el monedero corta antes de las 60 y `verdict_for` dice `SIN VEREDICTO` **después de gastar**. Suite 439 → **440**. Hallazgos H-1 y H-2 de la auditoría externa del 2026-08-14, comprobados aquí sobre `46cce85` | `measure_tutor.py` (`COST_PER_CALL_USD`), `tests/test_measure_tutor.py`, `[D-077]`, `[D-058]`, `[D-066]`, `[D-067]`, `[D-060]`, `[C-008]`, `[A-010]`, `T-095`, `[L-059]`, auditoría externa del 2026-08-14 |
| D-077 | 2026-08-14 | 🟡 **VIVA, NO ARCHIVADA — `T-079` baja de ✅ a 🟡 el 2026-08-14: la condición de esta entrada no depende de nosotros y no se cierra midiendo. Disparador: si vuelven los cortes, se repite la tanda de 60 ANTES de tocar `TUTOR_TIMEOUT_SECONDS`. Y corrige una frase del 14 — las cuatro fases son SECUENCIALES, el 9,0 es una suma nuestra que el SDK no impone, y la única garantía de reloj de pared es el 10,0 de `app/api.py:730` (`app/tools.py:239`).** `[A-011]` MUERE al tercer intento: `TUTOR_TIMEOUT_SECONDS = 10,0` se queda, con la corrida delante.** `T-093` corrida contra `claude-opus-5`, 60 frases distintas, 60 de 60 completadas: **0 por encima del corte de 6,5 s**, 0 por encima de 9,0 s, **mediana 2,88 s, peor de 60 = 3,91 s**. Por la regla de tres con cero cortes en 60 muestras, la tasa **no pasa del 5,0%**, que es el criterio exacto. 🚨 **Y el cierre es CONDICIONADO, escrito dentro de la entrada:** *el 5% vale mientras Anthropic responda como el 2026-08-14; si vuelve la saturación de `T-087`, la tanda se repite — no porque el criterio falle, sino porque cambió el mundo que se midió*. Las 60 llamadas fueron **secuenciales, en ~3 minutos**, contra un sistema que no controlamos: no son 60 observaciones independientes. Sin esa condición, `[A-011]` no muere — se levanta en seis meses disfrazada de asunto zanjado. ⚠️ **El 3,91 < 4,72 NO es una mejora:** `max(N)` es un cuantil que se mueve, y el veredicto no se apoya en esa cifra sino en el conteo contra un umbral fijado antes (`[L-058]`). ✅ Sin censura de la cola: 30 s de báscula contra 3,91 s de peor caso (`[L-057]`). 🧭 **Y salió verde con el criterio MÁS ESTRICTO**, el de `[D-075]`, no con el laxo. 📌 Pendiente cobrar el dato gratis: comparar el cargo real de la consola con lo esperado. 🔴 **El `$0,1404` que decía aquí estaba CADUCADO y lo corrige `[D-078]` el mismo día: la comparación es contra ~$0,182, y si no cuadra la primera sospecha es la prompt, no `[A-010]`** | `[A-011]` (muerta aquí), `app/api.py` (`TUTOR_TIMEOUT_SECONDS`), `measure_tutor.py`, `T-093`, `[D-075]`, `[D-074]`, `[D-058]`, `[A-010]`, `[L-058]`, `[L-057]`, `[L-043]`, `T-087`, auditoría externa del 2026-08-14 |
| D-076 | 2026-08-14 | 🔒 **El hueco entre el reloj del cliente y el de la ruta deja de ser una tabla en un comentario y pasa a ser un assert.** Los dos sumandos que `[D-073]` llevaba solo como texto se vuelven constantes: `LOCAL_WORK_SECONDS = 0,07` y `SURRENDER_MARGIN_SECONDS = 0,50`, y el test exige `TUTOR_TIMEOUT_SECONDS − TIMEOUT_SECONDS >= 0,57`. 🚨 **Lo que no cubrían los dos asserts que ya había:** con `TIMEOUT_SECONDS = 9,9` **los dos siguen verdes** y el hueco cae a **0,1 s** — el cliente deja de rendirse antes que la ruta y nadie se entera. 🔑 **«Más corto» no basta: tiene que ser más corto POR ALGO**, y ese algo estaba escrito en prosa, que ningún test puede leer. ⏫ **Y sube de prioridad por culpa de nuestro propio arreglo:** era deuda independiente desde la sesión 71, pero `[D-075]` derivó el umbral de ROJO de `TIMEOUT_SECONDS`, así que **el hueco pasó a sostener también el criterio de `T-093`**. ⚠️ `LOCAL_WORK_SECONDS` es `max(N)` redondeado y va anotado como suposición en `[A-029]`; se usa porque **el margen lo domina** —500 ms contra 70 ms, unas 7 veces—, así que un error de ±10 ms no puede voltear el assert. **No** porque "el error caiga del lado seguro": eso describe falsos negativos, que en un guardián son la dirección peligrosa, no la benigna. 🧭 Es `LM.34` un piso más arriba: la tabla que justificaba `read` era un párrafo con paréntesis. Propuesto por auditoría externa el 2026-08-14 | `app/tools.py` (`LOCAL_WORK_SECONDS`, `SURRENDER_MARGIN_SECONDS`), `tests/test_tools.py`, `[D-075]`, `[D-073]`, `[A-029]`, `T-093`, auditoría externa del 2026-08-14 |
| D-075 | 2026-08-14 | 🔴 **El umbral de ROJO deja de ser un `9,5` literal y pasa a LEERSE de producción (`tools.TIMEOUT_SECONDS` = 9,0). El criterio de `[D-074]`, escrito ayer para no decidir después de ver los datos, tenía tres defectos y uno cambiaba un veredicto.** 🚨 **El defecto que mordía:** 9,5 estaba **por encima** del techo del cliente entero (9,0), así que una llamada de 9,2 s caía en ÁMBAR — cuya receta es *"quitar de connect/write/pool y dárselo a read"*—, y esa receta es **imposible**: `read` no llega a 9,2 ni vaciando las otras tres fases. Era ROJO. 🧮 **El número correcto sale de que el reparto de fases está ACOTADO por el presupuesto del cliente:** ninguna fase puede recibir más de lo que hay que repartir, así que el máximo de `read` —vaciando las otras tres— es `TIMEOUT_SECONDS` entero. 🔴 **Aquí se escribió primero una justificación de "dos restas independientes" y era circular** (el camino A es una tautología; el camino B da 9,43, no 9,0, con los componentes reales de la tabla): el número era correcto y el porqué no, que es lo único que engañaría al siguiente. Corregido el mismo día — el argumento del acotamiento se sostiene solo. ➕ **Dos textos que afirmaban cosas falsas:** ÁMBAR decía *"1.7%, por encima del 5% acordado"* (1,7 no está por encima de 5 — lo cierto es que con algún corte ya no se puede **afirmar** que esté por debajo, que no es lo mismo que superarlo), y VERDE con tanda corta decía *"por debajo de 6.7%, que es el 5% acordado"*. ⚠️ **Y la tanda corta era alcanzable de verdad:** los dos `except` del bucle hacen `break`, así que un fallo en la frase 45 imprimía un aviso **y el veredicto igual**. Ahora `verdict_for` **se niega a emitir veredicto** con `total < TARGET_SAMPLES`: 🔑 **un aviso se salta; un veredicto que no sale, no.** ➕ `TARGET_SAMPLES` pasa a ser `ceil(3 / ACCEPTED_CUT_RATE)` para que la tasa aceptada mande de verdad y no sea decorativa. ➕ **Y `verdict_for` estrena tests** (12): la función se escribió para poder auditarla sin gastar, y aun así se le colaron tres defectos porque **nadie la miraba**. Propuesto por auditoría externa el 2026-08-14 | `measure_tutor.py` (`ROUTE_THRESHOLD_SECONDS`, `TARGET_SAMPLES`, `verdict_for`), `tests/test_measure_tutor.py`, `[D-074]`, `[D-073]`, `T-093`, `[A-011]`, auditoría externa del 2026-08-14 |
| D-074 | 2026-08-13 | 🎯 **El criterio de `T-093` queda fijado ANTES de gastar un centavo: 60 frases, tasa de corte aceptada del 5%, y tres veredictos escritos en el código.** 🔢 **El 60 no es redondo: sale de la regla de tres.** Con cero cortes observados, lo máximo que se puede afirmar es `3/n` — `n=40 → 7,5%` (afirma menos de lo que exigimos, no concluye nada) y `n=60 → 5,0%` (coincide con el criterio). Cinco centavos más para que la afirmación y el objetivo sean el mismo número: **~$0,14**. 🚦 **Los tres veredictos, decididos a ciegas:** 🟢 **VERDE** = 0 de 60 por encima de `tools.TIMEOUT.read` → los 10 s de la ruta valen y `[A-011]` se cierra; 🟡 **ÁMBAR** = alguna corta pero ninguna pasa de 9,5 s → la ruta está bien, hay que reequilibrar fases quitando de `connect`/`write`/`pool`; 🔴 **ROJO** = alguna pasa de 9,5 s → ningún reparto salva nada, lo que está mal es el presupuesto de la ruta. 🔑 **El criterio vive en el guion (`verdict_for`), no en esta entrada:** un criterio que hay que ir a buscar a `decisions.md` se reinterpreta al leer los datos; uno que imprime el programa, no. Es la defensa contra `[L-058]`, que ya mordió dos veces hoy. ⚠️ Y si la tanda no completa las 60, el guion avisa de que **el veredicto no se puede escribir en `[A-011]`**: se repite. ➕ 60 frases **distintas**, no 10 repetidas: repetir mediría la caché de Anthropic y saldría más rápido de lo real. 🔴 **Corregida al día siguiente por `[D-075]`: el `9,5` estaba por encima del techo del cliente (9,0) y marcaba como ÁMBAR lo que era ROJO; además dos veredictos afirmaban cosas falsas y la tanda corta emitía veredicto igual. El criterio se queda; los tres defectos se van** | `measure_tutor.py` (`TARGET_SAMPLES`, `ACCEPTED_CUT_RATE`, `verdict_for`), `T-093`, `[A-011]`, `[D-073]`, `[L-058]`, `[L-057]`, `[D-058]` |
| D-073 | 2026-08-13 | 🧮 **`read` deja de ESTIMARSE y pasa a CALCULARSE por resta: es el máximo que cabe, no "un poco por encima del peor caso observado". El número no cambia (6,5); cambia el porqué, que era lo que iba a engañar al siguiente.** `[D-072]` justificó el 6,5 como *"un 38% por encima de los 4,72 s"* — y `4,72` es `max(n=10)`, que **no estima una cota: estima un cuantil que crece con N**. Lo demostraron nuestras propias seis tandas locales: 44,9 → 62,4 ms, **+39% y subiendo**. Un número anclado en `max(N)` caduca en cuanto se vuelva a medir. 🧮 **La resta que lo sustituye:** `10,00 (ruta) − 2,50 (connect+write+pool) − 0,07 (trabajo local) − 0,50 (margen para que el cliente se rinda siempre antes) = 6,93`. Se deja en 6,5, holgura de regalo. 🔑 **No depende de ninguna medición, así que no caduca** — y protege del error que viene: dentro de dos semanas, con datos nuevos, `max(40)` parecerá más sólido que `max(10)` y será el mismo fallo con más muestras. ⚖️ **El motivo de fondo es que el coste NO es simétrico:** pasarse cuesta cero (muerde la ruta, el único tope de pared); quedarse corto **cobra una práctica** y culpa a Anthropic en el log. ➕ **Y rescata a `T-093`:** si `read` es máximo por construcción, la tanda de 30-40 frases no sirve para ajustarlo — sirve para contestar la pregunta que `[A-011]` no sabía formular, **¿son 10 s el presupuesto correcto de la RUTA?**. Propuesto por auditoría externa el 2026-08-13 | `app/tools.py` (`TIMEOUT`), `[D-072]`, `[D-071]`, `[A-011]`, `T-093`, `[L-043]`, `[L-058]`, auditoría externa del 2026-08-13 |
| D-072 | 2026-08-13 | 🔴 **`read` sube de 4,0 a 6,5 — el reparto de `[D-071]`, escrito dos horas antes, metía una REGRESIÓN que nuestros propios datos ya predecían.** Reparto nuevo: `connect 1,5 + write 0,5 + read 6,5 + pool 0,5 = 9,0` (`TIMEOUT_SECONDS` sube de 8,0 a 9,0; sigue < 10,0 de la ruta). 🚨 **La causa: se creyó que `read` cronometraba "entre el primer byte y el último". Es falso, y se comprobó en la fuente instalada:** `httpcore/_sync/http11.py::_receive_response_headers` usa `timeouts.get("read")` — y sin streaming Anthropic no manda un byte hasta terminar de generar, así que **`read` cronometra la generación entera**. Con `read=4,0` contra los **4,72 s** ya medidos (`[L-043]`, n=10), **al menos 1 de cada 10 llamadas medidas se habría cortado**. ⚠️ **Y el modo de fallo COBRA:** el corte entra por `APITimeoutError` → `request_sent=True` → `[D-051]` cobra la práctica, la persona pierde una de sus 20 del día por un veredicto que estaba a punto de llegar, y el log dice *"el tutor no contestó"* — diagnóstico apuntando al sitio equivocado. 🔑 **El reparto no es simétrico a propósito:** `pool` (httpx admite 1000 conexiones y aquí ve 40 como mucho), `write` (~1 KB) y `connect` estaban sobrefinanciados; todo lo liberado va a la única fase donde se tarda. `read=6,5` queda por encima del peor observado, en vez de por debajo. 🔴 **Y ese "38% por encima" era un razonamiento roto: `[D-073]` lo retira el mismo día.** `4,72` es `max(n=10)`, un cuantil que crece con N — no una cota. El 6,5 se queda, pero por **resta del presupuesto**, no por margen sobre una medida. ➕ **Y la báscula sale de su propio tope** (`MEASURING_READ_SECONDS = 30,0`): un instrumento no puede medir el tope que hereda — ver `[L-057]`. Propuesto por auditoría externa el 2026-08-13 | `app/tools.py` (`TIMEOUT`, `TIMEOUT_SECONDS`), `measure_tutor.py`, `measure_local_parts.py`, `[D-071]`, `[D-051]`, `[L-043]`, `[L-057]`, `[A-011]`, auditoría externa del 2026-08-13 |
| ~~D-071~~ | 2026-08-13 | 🔻 **SUPERADA el 2026-08-13 por `[D-072]`, dos horas después: el reparto vigente es `connect 1,5 + write 0,5 + read 6,5 + pool 0,5 = 9,0`. 🚨 Los números de abajo YA NO SON LOS DEL CÓDIGO** (`app/tools.py:245`) — se conservan porque el porqué sigue enseñando, pero **no se citan como actuales**. Se reportaron como vigentes dos veces el 2026-08-14, ver `[L-066]`. Decía: ⏱️ **El presupuesto del cliente se reparte FASE POR FASE: `connect 2,0 + write 1,0 + read 4,0 + pool 1,0 = 8,0`.** Arregla el agujero de `[L-054]`: `httpx` no divide un `timeout` escalar, **lo multiplica** — daba 8 s a cada fase, 32 s en total. 🚨 **Y el arreglo de una línea que propuso la auditoría (`Timeout(8.0, connect=2.0)`) NO arregla nada: suma 26 s.** Se comprobó antes de aplicarlo; es el sabotaje con el que se vio morder el test nuevo. **Contra:** (1) ese one-liner, descartado por lo anterior; (2) bajar el escalar a 2,5 para que 4×2,5 = 10, descartado porque ata cuatro fases distintas al mismo número y deja `read` —donde se tarda— igual de apretado que `connect`. 🔑 `TIMEOUT_SECONDS` deja de ser lo que se pasa al SDK y pasa a ser **el presupuesto total**; lo ata `test_the_timeout_is_split_by_phase_and_the_parts_add_up_to_the_budget`, que vigila **la SUMA**, no que haya cuatro números. Se usa `anthropic.Timeout` (mismo tipo que `httpx.Timeout`) porque `anthropic` está fijado y `httpx` entra de rebote — trampa de `[L-047]`. ⚠️ **Sigue sin ser techo duro:** `httpcore` aplica `read` a cada lectura de socket. Por eso los 10 s de la ruta son la única garantía de reloj de pared. ⚠️ `read=4,0` es más ajustado que el 8,0 de antes: si reaparece el 4,72 s de `[L-043]` entre el primer byte y el último, corta un veredicto que antes llegaba | `app/tools.py` (`TIMEOUT`, `TIMEOUT_SECONDS`), `tests/test_tools.py`, `measure_tutor.py`, `[D-070]`, `[A-011]`, `[L-054]`, `[L-043]`, `[L-047]` |
| D-070 | 2026-08-13 | 🔴 **ENMENDADA el mismo día por auditoría externa: el número se queda, el ARGUMENTO se cayó, y `[A-011]` está REABIERTA.** ✅ **Sobrevive:** `TUTOR_TIMEOUT_SECONDS` sigue en **10,0** (bajarlo invierte el orden de los relojes; retirarlo se lleva el reembolso), y los **56,3 ms** de trabajo local medidos con `measure_local_parts.py` son sólidos. 🔴 **Se cayó:** *"el cliente corta a los 8,0 s pase lo que pase"* — **`httpx` reparte `timeout=8.0` a cuatro fases con cronómetro propio (`connect`/`read`/`write`/`pool`), que suman 32 s.** Con eso mueren *"techo de 8,06 s"* y *"sobran 1 944 ms"*, y en una red mala una llamada pasa de los 10 s **sin que el cliente proteste**, invirtiendo de hecho el orden `8 < 10`. 📌 La premisa venía de `[L-045]` y `[L-043]` y se heredó sin recomprobar: `[L-034]` aplicado a una premisa. ⚠️ Queda además una contradicción sin resolver: *"el reembolso vive en el `except`"* y *"no se forma cola"* no pueden ser ciertas a la vez. **Texto original conservado bajo la enmienda.** | ~~`[A-011]` († )~~ → `[A-011]` **viva**, `app/api.py`, `app/tools.py`, `measure_local_parts.py`, `[L-045]`, `[L-043]`, `[L-042]`, `[L-034]`, `T-079`, auditoría externa del 2026-08-13 |
| D-069 | 2026-08-13 | ✅ **`[D-067]` COMPROBADO contra el modelo real, y `[A-028]` muere siendo CIERTA: Opus 5 pone la primera línea.** **Cinco llamadas locales en dos corridas:** 3 por guion (cuenta `probe-format`, borrada al acabar — su `{"score": 1, "practice": 3}` **ya no está en el disco**) y 2 desde el navegador (cuenta `jorge`, `data/users/jorge.json` → `{"score": 1, "practice": 2}`, **el único respaldo que sobrevive**). 🔑 Los veredictos llegaron **sin `OK` ni `FIX` a la vista** — la palabra clave se recortó. ⚠️ Cinco llamadas no son una garantía de formato: si algún día deja de cumplirse, el síntoma es `Score` clavado en 0 con `Practice` subiendo | `[D-067]`, `[D-066]`, `[A-028]`, `T-019` |
| D-068 | 2026-08-13 | 🔑 **Los marcadores viejos se BORRAN, no se migran — y `read_counters` exige la clave `practice` igual que exige `score`.** El `9` de un archivo viejo contaba prácticas; con `[D-066]` `score` cuenta aciertos: el mismo número diciendo dos cosas. Migrar obligaba a mentir en una de las dos (o `score=0` borra lo visible, o `score=9` afirma aciertos que no hubo). Se pudo elegir borrar porque los archivos son **un día de pruebas del propio autor**, no de alumnos. ⚠️ Exigir la clave es a propósito: un archivo viejo que sobreviva da `ScoreFileError` ruidoso en vez de un número que miente | `app/tools.py` (`read_counters`), `data/users/`, `[D-066]` |
| D-067 | 2026-08-13 | 🔑 **El veredicto legible por máquina viaja en una PRIMERA LÍNEA FIJA (`OK` / `FIX`), que el código lee y recorta antes de mostrar.** No en salida estructurada del SDK. Se eligió por depurabilidad: el texto crudo se lee entero y un desvío del formato se ve a simple vista. ⚠️ El precio es que el formato **no está garantizado** — si el modelo se salta la primera línea hay que decidir qué hacer, y eso se resuelve denegando por defecto (regla 3): sin `OK` explícito, no hay punto | `app/tools.py` (`GRAMMAR_RUBRIC`, `judge_grammar`), `[D-066]` |
| D-066 | 2026-08-13 | 🔑 **El marcador cuenta frases CORRECTAS, no practicadas — y se añade un contador `practice` aparte para los intentos.** Mata `[A-001]`, abierta desde el 2026-08-02: resultó **falsa**. La prueba que pedía —frase mal y mirar el marcador— corrió sin buscarla el 2026-08-13: `I cooking in these morning` estaba mal y el marcador subió igual. ⚠️ Obliga a cambiar el contrato de `judge_grammar`, que hoy devuelve texto libre y no sabe decir "correcta" a una máquina. El `practice` evita el castigo que `[A-001]` temía: quien falla ve su esfuerzo en un contador propio, no un cero | `app/tools.py`, `app/english_tutor.py`, `app/api.py`, la pantalla, `[A-001]`, `[D-050]`, `T-019` |
| D-065 | 2026-08-13 | 🔑 **Producción no comparte llave con el curso: se crea `teapp-server`, con nombre propio, ANTES de correr `install.sh`.** Mata `[A-027]`, que resultó FALSA: el "algo más" que usa la llave de `Default` es el repositorio del curso — **21 archivos `.py` cargan ese `.env`, en los ocho niveles del 00 al 06b** (medido el 2026-08-13). Y el orden ya no es preferencia: `install.sh:89-95` **nunca pisa una llave ya escrita**, así que mandar hoy la provisional convierte el arreglo de mañana en edición a mano por SSH sobre la máquina viva, por un camino sin guion y sin tests. ⚠️ El freno del espacio nuevo **no puede ser 50** — es la firma del laboratorio en `check_api_key.py:LAB_REQUESTS_PER_MINUTE` | `T-078`, `deploy/install.sh`, `deploy/check_api_key.py`, `[A-027]`, `[D-063]`, `[D-061]`, `[D-059]`, `[L-047]` |
| D-064 | 2026-08-12 | 🧪 **La terminal que AUDITA sí puede correr `pytest -q`, y el disparador se mira en presente: siempre que vaya a ESCRIBIR o CITAR un número de la suite.** Cierra una pregunta de reparto abierta desde la sesión 59 (`PROGRESO.md` 862–867). **Por qué se abre:** quien audita y no puede medir solo sabe **releer** — releer caza razonamientos torcidos (hoy tres, uno mío en `[D-062]`), pero **no caza un número**; en la sesión 51 correr la suite aquí destapó un **342 que eran 348**. 🔑 **Es la regla 6 aplicada al auditor: gana el instrumento, no la lista.** Riesgo ninguno: lectura sobre este repo, sin nube, sin gasto, y `conftest.py` + los porteros de `tests/` impiden que toque `data/` de verdad (`[D-037]`). 🔑 **Por qué gana este disparador y no *"cuando el número sostenga una decisión"* —y esto es lo transferible—:** el otro obliga a **predecir el futuro**, y una regla que exige adivinar **se resuelve siempre del lado cómodo**; este se contesta mirando el presente, sí o no, sin juicio. 📌 **Un disparador que se comprueba observando lo que haces vale más que uno que se comprueba estimando lo que importará** — misma familia que el `CallBudget` de `[D-060]` (cobra antes de llamar) y el `install -m 600` de `install.sh:168` (cierra el archivo antes de que tenga nada): el momento en que la regla muerde lo fija la **mecánica**, no el criterio de alguien. 🚨 **Remate 1 — se cierra la escapatoria que la propia regla abre:** "correr si vas a escribir el número" se esquiva **no escribiendo el número** (*"la suite pasa"* en vez de *"410 pasan"*). Por eso: **si no se corrió, no se puede afirmar el estado de la suite ni en vago**; solo dos formas legales — **medido aquí, con su número**, o **reportado, no verificado**, dicho con esas palabras. Nunca sin etiqueta (la honradez del `session-closer` de la 55). 🚨 **Remate 2 — un número solo se compara contra el MISMO commit:** si a la auditoría le sale distinto, la primera hipótesis no es que el otro mienta, es que **corrió otro árbol**; al correr, se registra el commit. Hoy pasó la versión conceptual: se reconstruyó un peligro que `install.sh` ya tenía resuelto, por leer el comentario y no el código. 📌 **Estado de hoy bajo esta regla:** los **410** son **medidos** por la terminal que construye sobre `d4c40eb`; para la que audita son **reportados, no verificados** | reparto de las dos terminales, `PROGRESO.md` 862–867, regla 6, `[D-037]`, `[D-060]`, `tests/conftest.py` |
| D-063 | 2026-08-12 | 🔑 **Cómo llega la llave al servidor en `T-078`: por variable de entorno, interrogada ANTES de escribirse, sin pisar nunca una que ya exista, y con fallo ruidoso si al terminar sigue vacía.** Las cuatro piezas hacen falta. **1) Entra por `environ`, no por argumento** — patrón ya construido y probado en `create_account.py:44` (`main(argv, environ)`, contraseña por `environ` en la 55) con `tests/test_create_account.py:93` **rechazando** el segundo argumento: un argumento queda en el historial del shell y en la lista de procesos. **2) Tres reglas del `.env`:** vacía + variable ⇒ escribe; ya tiene valor ⇒ **no la toca** y avisa de cómo cambiarla a mano; al terminar sigue vacía ⇒ **falla, salida ≠ 0**. 🔑 **La tercera hace valer a las otras dos:** sin ella *vacía* sigue siendo estado legal, y `T-078` existe para que deje de serlo — despliegue en verde, servicio arrancado y el fallo saliendo en la primera práctica de una persona real es `[C-008]` por otra puerta. Misma forma que `[D-037]`. El olvido queda del lado correcto (`[D-045]`): olvidarse cuesta trabajo a mano, lo contrario cuesta producción degradada en silencio. **3) Identidad de la llave, del revés de lo obvio: abortar si `requests-limit` vale `50`** —la firma del laboratorio—, no exigir el `1.000` de `Default`. 🔑 **Lo decide de quién es cada número:** el 1.000 es heredado, **no lo controlamos**, y `[D-061]` lo vio desmentirse en un día; colgar el freno de ahí fabrica un **rojo falso con fecha desconocida**, y un freno que muerde en falso se acaba quitando con red y todo. ⚠️ **Lo que se paga:** exigir el 1.000 falla en **rojo falso** (ruidoso, alguien mira); abortar con el 50 falla en **verde falso** (mudo: el 429 de dentro de tres semanas). Se acepta porque el riesgo real es **exactamente uno** —mandar la del laboratorio porque en el `.env` local se llama igual— y contra ese muerde igual. 🚨 **Y el disparador del verde falso ya lo predice `[D-061]` por escrito** (*"cada modelo nuevo necesita su fila"*, con Haiku nombrado): ese 50 **se va a mover en el paso 9**. Por eso la **condición no opcional**: el 50 vive en dos sitios, así que el guion lleva encima de dónde sale y qué se rompe si se mueve, y `[D-061]` dice que cambiarlo obliga a tocar `install.sh` — el acoplamiento se ve desde los dos lados. **4) Dos mecánicas:** 🚨 la comprobación va **ANTES de escribir** (misma forma que el `CallBudget` de `[D-060]`, que cobra antes de llamar) — al revés, *"nunca pisar"* deja la llave mala clavada para siempre y la regla que protege pasa a impedir el arreglo; y **"llave del laboratorio" y "no hubo red" salen por puertas distintas**, códigos y mensajes, o un corte de red se disfraza del rojo falso que se acaba de evitar. 📌 **Fuera de alcance:** que la **app** se niegue a arrancar con la llave vacía es otra pregunta, con su propia entrada. 📌 **Falsa alarma verificada de paso:** la ventana entre escribir el `.env` y cerrarlo **no existe** — `deploy/install.sh:168` hace `install -m 600 … /dev/null` y el archivo nace vacío y ya cerrado; el `chmod` de la 211 cierra el otro camino. ⚠️ Pero su comentario pone cuatro líneas de peligro antes de una de solución y se leyó como ventana viva: cuando se toque (`[PI-3]`, no hoy), que la primera línea diga el **estado**. 🚨 **CONDICIÓN PARA CERRAR `T-078`, escrita para no confiarla a la memoria** (mismo mecanismo que `[D-059]` sobre la capa 1): hay que **ver morder DOS puertas con DOS llaves reales** — la **3** con la del laboratorio (que la reconozca y se niegue) y la **0** con la de `Default` (que pase, antes de que `install.sh` la use). ⚠️ **La puerta 3 sola no vale:** con la llave del laboratorio *solo se puede* salir por la 3, así que ese 3 es compatible con "la identificó" y con "acierta por casualidad" — misma forma que `T-060b`, donde sin nada escuchando en el 8000 *"cerrado"* salía igual con el cortafuegos abierto que cerrado, y hizo falta el **control al lado**. El control aquí es la llave de `Default`, que hay que sacar de la consola ese día de todos modos. 📌 **Hasta entonces `T-078` NO se cierra**, por muchos verdes que haya: los 15 tests nuevos prueban la lógica contra una Anthropic **de mentira**, y `ask_anthropic` —lo único que toca la red— no se ha ejecutado nunca | `deploy/install.sh`, `deploy/check_api_key.py`, `tests/test_check_api_key.py`, `T-078`, `[D-061]`, `[D-060]`, `[D-059]`, `[D-045]`, `[D-037]`, `[C-008]`, `create_account.py`, `T-060b`, paso 9 |
| D-062 | 2026-08-12 | 💵 **El espacio `teapp-measure` lleva tope de gasto de `$2,00` al mes — y NO es una capa de protección.** Cierra `T-085` y el `📌 Sin decidir` de `[D-061]`. Verificado en pantalla: *"Límite Mensual: USD 0,00 de USD 2,00"*. 🚨 **Por qué no protege, con la aritmética de números ya medidos:** techo físico de la báscula `35` llamadas/min (`[D-061]`) × `$0,00234` (`[D-058]`) = `$0,082/min`; `$6,48 ÷ 0,082 =` **79 minutos** para vaciar el saldo entero, contra una ventana de reacción del tope de **120 minutos** (`[A-025]`). Llega 41 minutos tarde; si la báscula fuera concurrente, 55 minutos — peor. **Quien protege el saldo sigue siendo el `CallBudget` de `[D-060]`.** 🔍 **`[A-025]` se comprobó y salió MUDA, que no es salir falsa:** la pantalla `Settings → Workspaces → Spend limits` dice *"El límite de gastos mensual de tu organización es de $500,00. Puedes establecer un límite de gastos inferior…"* y **nada más** — ni `soft`, ni umbrales, ni retraso. Se queda en suposición y se decide por su rama pesimista: lo que no se puede comprobar no cuenta como freno. 🔑 **Por qué se pone igual — no es un corte, es una RESERVA:** `Default` no admite tope (`[D-059]`), así que a producción no se le puede poner suelo directo; el único suelo es indirecto, capando al laboratorio. La pregunta útil no era *"cuánto puede gastar la báscula"* sino **"cuánto saldo se le reserva al que sirve"**: quedan **$4,48 = 1.914 prácticas ≈ 95 días** de una persona a tope (`[D-058]`) — **y esto vale SOLO frente a gasto LENTO: frente a una corrida desbocada no hay reserva ninguna, hay `CallBudget`**. ⚠️ **Lo que este tope muerde, con su alcance pegado al titular: el gasto REPARTIDO en más de dos horas.** 🔻 **Rectificado el mismo día:** esta entrada dijo primero que cortaba el flanco de las 26 corridas de `[D-060]` y escribió al lado, entre paréntesis, el número que la desmiente — `26 × 106 × 1,72 s ≈ 79 min`, **dentro** de la ventana ciega de 120. Por la propia regla de esta entrada, ese flanco **no queda cortado**: 26 corridas seguidas vacían el saldo antes de que el tope se entere, igual que el bucle roto. **Reparto verdadero: lo RÁPIDO lo tapa `CallBudget`** —y las corridas repetidas seguidas, **nadie**: `[A-026]`— **y lo LENTO lo tapa este tope**, que ahí sí reserva de verdad. Las **8 tandas al mes** (`2,00 ÷ 0,25`) son un techo mensual, no una defensa contra una tarde intensa. ✅ **El paso 9 cabe:** tres modelos (Opus 5 actual contra Sonnet y Haiku) × una tanda = `$0,75`, con cinco tandas de margen; y el `CallBudget` cobra siempre a precio de Opus, así que Sonnet y Haiku gastarán menos. 🚨 **Disparador, porque los dos relojes no coinciden:** el tope es **mensual y se reinicia**, el saldo es prepago y **no** — tres meses a tope son $6 de $6,48 sin que el instrumento se pase nunca. El número está elegido **contra los $6,48, no contra un mes**: se revisa en **cada cambio de mes y en cada recarga** (misma familia que el disparador del $500 en `[D-057]`) | `T-085`, `T-078`, `[C-008]`, `[A-025]`, `[D-059]`, `[D-060]`, `[D-061]`, `[D-058]`, `[D-057]`, paso 9, regla 5, regla 6 |
| D-061 | 2026-08-12 | 🚦 **El espacio `teapp-measure` existe, y su freno de velocidad para `claude-opus-5` queda en `50 / 20.000 / 5.000` (peticiones, tokens de entrada, tokens de salida por minuto).** Es la capa 2 de `[D-059]`, la mitad de `T-084` que no era la llave. **De dónde salen los números, que es lo que los hace auditables:** `measure_tutor.py:208` llama en un `for` **secuencial** —nunca dos a la vez—, y la llamada más rápida de las diez de `[A-011]` tardó **1,72 s**, así que el techo físico de la báscula es `60 ÷ 1,72 = 35` llamadas/min; con los 247 tokens de entrada y 44 de salida por llamada de `[D-058]`, eso son ~8.650 y ~1.540 por minuto. Los tres valores llevan ~1,4× de holgura sobre lo medido. 🚨 **Y aquí la regla 6 mordió en directo: la documentación decía que Start da a Opus 5 `2.000.000` de entrada y `400.000` de salida; la consola de ESTA cuenta dijo `1.000 / 500.000 / 80.000`.** No coinciden — gana la consola, que es el instrumento de la cuenta, no una lista general. Escribir los de la documentación habría guardado un dato falso con aspecto de verificado. Los límites puestos son el **5% / 4% / 6%** de lo heredado: si la báscula se vuelve concurrente por accidente, no puede robarle velocidad a `Default`, que es quien atiende personas. ✅ **Semántica confirmada en pantalla:** *"si se establece, se aplicarán tanto los límites del espacio de trabajo como los de la organización"* — se suman, no se sustituyen; y `Default` **no admite límites** por diseño de Anthropic, lo cual encaja: al que sirve no se le frena. ⚠️ **Esto NO frena el dinero, y confundirlo sería el error entero:** un bucle roto secuencial tampoco pasa de 35/min, así que 50 no lo para — quien protege el saldo es el `CallBudget` de `[D-060]`. Este freno protege la **velocidad** del servicio, que es otra cosa. 🧭 **Trampa apuntada de antemano para el paso 9:** las demás filas se dejan heredadas a propósito (`[PI-2]`: un límite para un modelo que no se llama sería un número inventado), pero Haiku 4.5 es mucho más rápido y podría pasar de 50/min **sin estar roto** — con `MAX_RETRIES = 0` ese 429 llega como fallo del tutor y **medirías el límite que tú pusiste creyendo que mides el modelo**. Cada modelo nuevo necesita su fila con su propia medida antes de la primera tanda. ✅ **Verificado en vivo:** la llave nueva está en el `.env` local bajo el mismo nombre `ANTHROPIC_API_KEY` (sin variable nueva — el corte es *máquina contra producción*, no *app contra báscula*), y una llamada mínima devolvió `requests-limit: 50`, `input-tokens-limit: 20000`, `output-tokens-limit: 5000` y `requests-remaining: 49` — los tres valores escritos, y el freno contando en directo. `Default` habría dicho `1.000/500.000/80.000`. Costó 10 tokens de entrada y 4 de salida. Antes hubo que descartar tres instrumentos gratis que no distinguían una llave de otra (`[L-046]`). ⚠️ La llave de `Default` sigue haciendo falta: va al servidor en `T-078`. 📌 Queda abierto: la consola ofrece además tope de **gasto** por espacio de trabajo, que `[D-059]` descartó por ser reparto del mismo techo — cierto contra los $500 mensuales, pero el freno real es el saldo de $6,55 y un tope mensual bajo sí mordería antes. ✅ **CERRADO el 2026-08-12 por `[D-062]`**: $2,00 al mes, como reserva, no como protección. 🚨 **AÑADIDO el 2026-08-12 — el `50` ya no es solo un freno, también es una FIRMA, y vive en dos sitios:** `[D-063]` hace que `deploy/install.sh` **aborte el despliegue si la llave devuelve `requests-limit: 50`**, porque ese valor identifica al laboratorio y las dos llaves se llaman igual en el `.env` local. ⚠️ **Cambiar este número obliga a tocar `deploy/install.sh` en el mismo cambio** — si sube a 80 para medir Haiku (lo que la trampa del paso 9 de esta misma entrada predice), la comprobación del despliegue **se queda muda sin dar error** | `[D-059]`, `[D-060]`, `[D-058]`, `[D-062]`, `[D-063]`, `[A-011]`, `[C-008]`, `T-084`, `T-078`, `deploy/install.sh`, paso 9, `[D-049]`, regla 3, regla 6 |
| D-060 | 2026-08-11 | 💵 **El tope de la báscula sale del SALDO, no del historial: `$0,25` por tanda ÷ `$0,00234` por llamada = 106 llamadas.** Es la capa 1 de `[D-059]`, construida y **vista morder** (`T-083`). 🚨 **El error que corrige, y es de los que no dan error:** el archivo ya traía `MAX_CALLS = 10`, y ese diez **salía de un `len()`** — `SENTENCES` tiene exactamente diez frases, así que la tanda de `T-079` hizo diez llamadas *porque había diez frases*. Circuló tres veces (constante, tope y argumento en conversación) con aspecto de medido, sin serlo. Ver `[L-044]`. Fallaba por los dos lados: el paso 9 compara modelos con decenas de llamadas y habría mordido en falso, y de dinero no decía nada. 🔑 **Y lo que lo hacía cumplir tampoco era un freno:** un recorte de lista (`SENTENCES[:MAX_CALLS]`), que con el tope en 106 y diez frases no frena nada. Ahora es un `CallBudget` compartido que **cobra ANTES de llamar** y vive dentro de `RecordingClient`, el paso obligado de toda llamada. ⚠️ **Alcance escrito a propósito, con su número: para un bucle roto DENTRO de una corrida; NO para de correr el guion muchas veces a mano** — el monedero se reinicia en cada arranque, y **`$6,55 ÷ $0,25 = 26 corridas` vacían el saldo**. Veintiséis no es un número grande cuando el paso 9 es correr el guion una vez por modelo. Deliberado: el fallo **mudo** de `[C-008]` es el primero. 📌 `$0,25` = 3,8% del saldo si un accidente quema la tanda entera; el precio por llamada se toma del modelo **más caro** (`claude-opus-5`), así el tope se queda corto, nunca largo | regla 5, regla 6, `[D-059]`, `[D-058]`, `[C-008]`, `T-083`, `T-078`, `measure_tutor.py`, `tests/test_measure_tutor.py` |
| D-059 | 2026-08-11 | 🚧 **MEDIR y SERVIR se parten en DOS capas, no en una: corte duro dentro de `measure_tutor.py` + espacio de trabajo propio para medir, con su llave y su límite de VELOCIDAD.** ✅ Cierra `T-082`, **que pedía DECIDIR**. 🚨 **NO desbloquea `T-078` — esto es una decisión, y una decisión no frena un bucle.** La única capa que protege el saldo es la 1, y **todavía no está escrita**. `T-078` cuelga de que **la capa 1 exista y se le haya visto morder** (test que sabotee el contador y lo vea en ROJO, como el `refund` de `T-076`), no de que la partición esté decidida. ✅ **CONDICIÓN CUMPLIDA el mismo día por `[D-060]`** — capa 1 construida, tres sabotajes vistos en rojo, suite en 395. `T-078` queda desbloqueada **desde ahí, no desde aquí**. 🔑 **La asignación de llaves, escrita porque desde hoy hay dos:** la llave **nueva** es la de MEDIR y **se queda local**; la llave **de hoy** es la de SERVIR y es la que viaja al servidor en `T-078`. 📌 Con ese reparto **servir queda en el espacio por defecto, el único sin tope posible — y es a propósito**: se quiere frenado el laboratorio, no la app, y el abuso ya lo tapa la cuota (`[D-058]`). 🔑 **Lo que decide, leído en la documentación de Anthropic:** los espacios de trabajo (*workspaces*) SÍ existen y SÍ admiten tope de gasto propio, **pero el tope es un reparto del mismo techo, no un bolsillo aparte** — *"You can set workspace limits lower than (but not higher than) your organization's limits"* y *"Organization-wide limits always apply, even if workspace limits add up to more"*. El saldo de $6,55 es de la ORGANIZACIÓN y sigue siendo uno solo: si medir se lo come, servir se queda sin llave igual, esté en el espacio que esté. ⚠️ **Y el espacio por defecto —donde vive la llave de hoy— no admite ningún tope:** *"You cannot set limits on the Default Workspace"*. 🔻 **Esto REVIERTE la mitad de `[D-057]`**, que descartó el corte duro en el guion por PI-2 con el argumento "el saldo ya hace ese trabajo": era cierto **mientras el servidor tuviera la llave vacía**. Después de `T-078` el saldo agotado deja de ser un freno inofensivo sobre la medición y pasa a ser una **caída de producción** — el mismo hecho cambia de significado, no de valor. 📌 Descartado también **Claude Platform on AWS**: factura a mes vencido en CCUs y *"There is no CCU balance"*, o sea cambiar un techo duro por una cuenta abierta — contra la regla 5 | regla 5, `T-082`, `T-078`, `[C-008]`, `[D-057]`†, `[D-058]`, `[A-025]`, `measure_tutor.py` |
| D-058 | 2026-08-11 | 💵 **El tope de 20 prácticas al día SE QUEDA, ahora con la corrida detrás: cierra `[A-010]`.** Medido con `T-079` y **cruzado con dos instrumentos que no comparten fuente** — la consola dijo **$0,02** por las diez llamadas y los tokens medidos × precio de lista oficial dan **$0,0234**: coinciden dentro del redondeo a céntimos, así que ninguno de los dos está mintiendo. **$0,00234 por práctica** (53% entrada, 47% salida: la salida es 1/5 de los tokens pero cuesta 5×). ⇒ **$0,047 al día, $1,41 al mes, $8,44 en 180 días** por una persona a tope. 🚨 **El hallazgo incómodo: el saldo de $6,55 NO cubre a UNA sola persona a tope durante los 180 días — se acaba a los 140.** ✅ **Aun así el 20 no se toca, y el motivo es que el tope no es el que gasta:** nadie practica 20 veces al día 180 días seguidos, y el 20 está para frenar el abuso, no para describir el uso. Bajarlo castigaría a quien estudia de verdad sin ahorrar nada real. ⚠️ **Lo que SÍ cambia: `[C-008]` deja de ser teórica.** Con el saldo dando para 140 días-persona a tope, medir y servir del mismo bolsillo ya no es un riesgo lejano. 📌 Y la palanca para bajar la factura **no es el tope ni el límite de 500 caracteres** (`[C-002]`, que en uso normal no se toca): es el modelo, trabajo del paso 9 (`[D-049]`) | regla 5, `[A-010]`†, `[C-008]`, `[C-002]`, `[D-049]`, `[D-057]`, `app/quota.py` |
| D-057 | 2026-08-11 | 💰 **El freno de gasto del paso 8 es el SALDO PREPAGADO con la recarga automática apagada, y NADA MÁS: el límite mensual se deja en los 500 US$ que puso Anthropic.** 🔻 **Rectificada el mismo día, decisión del usuario, y tiene razón:** bajarlo a 10 no protege de nada que el saldo no cubra ya —6,55 muerde muchísimo antes que 500—, así que era prevención para después disfrazada de tarea de hoy. Cierra `[A-024]`, que era **falsa**: mirado en la consola de Anthropic (`T-080`) hay saldo de **6,55 US$**, **recarga automática DESACTIVADA** y un **límite mensual de 500 US$** puesto por Anthropic, con botón de ajustar. 🔑 **El techo que manda hoy es el saldo, no el límite:** 500 no puede morder nunca porque 6,55 se agota mucho antes, y un saldo que nadie rellena solo es un tope **duro** —las llamadas fallan—, no una alerta que avisa mientras el agua corre. ⬇️ **Aun así el límite se baja a 10 US$, y no por hoy: por el futuro.** El día que se recargue saldo, el saldo deja de ser el freno pequeño y lo único que queda de pie es ese número; dejarlo en 500 es heredárselo a uno mismo dentro de dos meses. Dos capas de mecanismo distinto, como en `T-060a`/`T-060b`. ⚠️ **El 10 es un JUICIO, no una medición** (regla 6): nadie ha corrido `T-079`, que es justo lo que va a medir cuánto cuesta. Se elige bajo a propósito — si el freno muerde antes de tiempo se sube en diez segundos y se aprende un número real; si no muerde nunca no se aprende nada. 🚫 **La recarga automática NUNCA se enciende:** convierte el techo en manguera, misma familia que las siete puertas de `[C-005]`. 📌 Descartado el plan B de `[A-024]` —contador de llamadas y corte duro dentro del guion de `T-079`— por PI-2: el saldo ya lo hace, y en un sitio donde un `while` roto no puede desactivarlo. 🚨 **El precio queda escrito y con disparador: el día que se RECARGUE saldo, el saldo deja de ser el freno pequeño y el 500 pasa a ser el único freno vivo — ese día se baja, antes de llamar.** | regla 5, `T-079`, `T-080`, `[A-010]`, `[A-011]`, `[C-006]` |
| D-056 | 2026-08-10 | 📚 **Para consultar documentación, `ctx7` SIEMPRE es la primera opción; la skill `claude-api` es el último recurso.** Decisión del usuario, a raíz de medir el coste: invocar `claude-api` para una sola pregunta llevó la sesión de **55 K a ~340 K tokens** — vuelca de golpe unos treinta documentos (agentes gestionados, lotes, migración, caché…) cuando TEAPP hace **una** llamada, `messages.create` con una rúbrica. 🔑 **La skill no se abre por trozos: es todo o nada**, así que su coste no escala con el tamaño de la pregunta. `ctx7` sí — trae la página que se pidió. ⚠️ **Y lo caro no es el dinero, es la ventana de contexto:** lo que se llena de manuales que no se usan empuja fuera el código, las decisiones y los tests, y en sesión larga se resume y se pierde con detalle. ✅ **El disparador de `claude-api` está escrito ancho a propósito** —se activa casi con nombrar a Anthropic— porque sirve a cualquier proyecto; en uno que hace una sola llamada se dispara mucho más de lo que aporta. 📌 **La escalera queda así: (1) `ctx7`; (2) la página suelta de la documentación; (3) la skill entera, y solo si las dos primeras vuelven vacías o contradictorias — diciéndolo en voz alta al hacerlo.** 🚨 **Esto NO afloja la regla 6:** el dato se sigue comprobando siempre; lo que cambia es por dónde se trae. 📉 De todos modos este proyecto ya casi no la necesita: el paso 8 era el único tramo que tocaba la API, y sus cuatro preguntas gordas están contestadas y fechadas en `app/tools.py` | método de trabajo, `_context/`, regla 5, regla 6, `[D-055]`, `T-079` |
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

### [D-099] 2026-08-18 — Las respuestas del juez se archivan en `replies/` y se borran de `data/`

- **Se eligió:** el corpus de respuestas se **mueve** de `data/` a
  `_persistence/replies/`, carpeta nueva con portero propio (`replies.py`) desde el
  primer commit. Queda **una sola copia**, y es la que Git respalda. `T-111` lee
  esa, no `data/`.
- **Contra:**
  - **Copiarlo a `_persistence/corpus/`.** Descartado, y comprobado antes de
    descartarlo: `_frozen_corpora()` usa `glob("*.jsonl")`, así que **sí** lo
    alcanza, y `test_no_frozen_corpus_carries_the_live_rubric` lo pondría rojo por
    partida doble — el nombre lleva la huella viva `bbf4be38` y las filas también.
    Es la misma trampa que `[D-097]` esquivó con las etiquetas, un día después y
    con el otro archivo.
  - **Dejar copia en `data/`.** Descartado: dos archivos con el mismo nombre que un
    día discrepan, sin forma de saber cuál manda.
  - **`mv` directo como primera acción.** Descartado por el orden, no por el
    destino. Ver abajo.
- **Por qué:** es el argumento de `[D-097]` aplicado a la otra mitad del mismo
  cruce. `data/` está fuera de Git —`.gitignore:18`, comprobado hoy— y es un solo
  disco. Las etiquetas estaban protegidas y las respuestas no, aunque son las dos
  mitades de la misma medición.
- **🔑 Y lo que se protege no es el archivo, es la auditabilidad del número.**
  `[D-096]` fija `$0,21` las sesenta, así que es recomprable. Pero el juez no es
  determinista: recomprarlas da **otras** respuestas, y entonces el resultado de
  `T-111` ya no se puede reproducir. Irrepetible pesa más que caro.
- **🔻 Mover y no copiar, y el motivo es estructural:** con copia, `T-111` **puede**
  leer el archivo equivocado; con movimiento, el archivo equivocado **no existe en
  el disco**. No es una convención que haya que recordar — es que la opción mala
  deja de estar disponible. Mismo tipo de freno que `[D-097]`.
- **🚨 El ORDEN se invirtió respecto al que propuso esta terminal, y ese fue el
  aporte de la auditoría.** Se había propuesto `mv` como primera acción. Pero en el
  instante del `mv` sigue habiendo **una sola copia en el mundo**: un destino mal
  escrito, un portero nuevo que rechaza, un `git clean` de más, y se acabó. La
  secuencia que se ejecutó fue: **(1)** copiar —momento seguro, dos copias—,
  **(2)** portero, tests y commit, **(3)** verificar contra Git las dos mitades
  (`check-ignore` y `ls-files --error-unmatch`), **(4)** solo entonces borrar el de
  `data/`. **El movimiento es el resultado del plan, no su primera operación.**
- **📌 `replies/` es una ANTESALA, no una hermana de `corpus/`.** Con `labels/` la
  separación era limpia —etiquetas contra rúbrica viva, corpus contra rúbrica
  muerta, vidas opuestas—. Aquí no: lo archivado es un corpus de respuestas cuya
  única diferencia con `corpus/` es que su rúbrica **todavía vive**. Es la misma
  vida en dos momentos.
- **La puerta de salida es la de `[D-092]`, sin cambiarla:** cuando algún eje del
  nombre deja de coincidir con producción, el archivo se muda a
  `_persistence/corpus/`, disparado por el commit que mueve `MODEL` o
  `GRAMMAR_RUBRIC`. 🔑 **Se escribe al nacer la carpeta** porque una antesala sin
  salida escrita es la misma cosa en dos sitios con fecha diferida.
- **🔻 Y `[D-092]` ya había descrito este agujero**, al descartar la propuesta rival
  de promover *"cuando la rúbrica ya no existe en producción"*: *"al crear un
  corpus la rúbrica está viva por definición, así que nada se guardaría nunca al
  nacer — la evidencia esperaría en `data/`, ignorado por Git y en un solo disco,
  exactamente mientras se la considera todavía no valiosa"*. Esta carpeta es esa
  espera, con respaldo.
- **🔒 El portero cierra el conjunto de campos** —`number`, `sentence`, `reply`,
  `broken`, `model`, `rubric`, todos obligatorios— y **declara en voz alta que
  `reply` no lo audita ningún programa**. ⚠️ Aquí la prosa libre no es un campo
  lateral como la `note` de `labels/` —que acabó vacía en las sesenta—: **es la
  carga entera del archivo**, sesenta párrafos generados a un repositorio
  **público** (`[C-007]`). Ver `[L-084]`.
- **🔻 El rojo existió y se vio:** `test_the_archived_replies_are_backed_up_by_git`
  falló con el archivo ya en disco y todavía fuera de Git, antes del `git add`.
  Ese es el fallo que el test existe para cazar, y se enseñó (`[D-060]`, `[L-048]`).
- **⚠️ Lo que esto NO cierra:** mover no impide que una corrida futura vuelva a
  crear ese mismo nombre en `data/` —fecha sin hora, `save_replies` en `"w"`—.
  `T-109` sigue abierta y deja de ser tarea de fondo: apunta al insumo de `T-111`.

### [D-098] 2026-08-18 — La vara del etiquetado es el inglés escrito de libro

- **Se eligió:** inglés escrito correcto —el de un examen— como criterio de las 60
  etiquetas. Firmado por el usuario.
- **Contra:** el inglés que un hablante nativo aceptaría de oído aunque un examen
  lo marcara.
- **Por qué:** la app enseña a **escribir**, y `GRAMMAR_RUBRIC` ya está redactada
  en esos términos. Con el etiquetado en una vara y el juez en la otra, la tasa de
  acierto no mediría al juez: mediría el desacuerdo entre dos reglas.
- **Cómo se supo:** 🔑 **no se contestó preguntando, se leyó del propio archivo.**
  Las frases 22, 30 y 54 son las tres que separan una vara de la otra, y las tres
  salieron `wrong`.
- **La 55, revisada y NO cambiada:** *"She told me that she is tired"* se queda
  `correct`. El retroceso de tiempo tras `told` es **opcional** cuando el estado
  sigue vigente, así que bajo esta misma vara `is` no es un error. 🔴 La
  inconsistencia que esta terminal señaló era más débil de lo que dijo al
  señalarla, y la fila venía además anclada por un ejemplo propio (`[L-083]`).
- **Toca:** cierra el criterio de `T-106`. Las 60 etiquetas quedan como las escribió
  el humano; ningún veredicto lo puso esta terminal.

### [D-097] 2026-08-18 — El etiquetado manual vive en `labels/`, hermana de `corpus/`, con portero propio desde el primer commit

- **Se eligió:** `_persistence/labels/` en `.jsonl`, una fila por juicio, **con su
  portero escrito en el mismo commit que crea la carpeta**. Firmado por el usuario.
- **Contra:** meterlo en `_persistence/corpus/` (pone en rojo
  `test_no_frozen_corpus_carries_the_live_rubric`: las etiquetas nacen con la
  huella **viva** `bbf4be38` y esa carpeta guarda lo que ya murió); dejarlo en
  `data/` junto al corpus (disco sin copia, fuera de Git); crear hoy la carpeta y
  el portero más adelante.
- **Por qué:** el corpus sin etiquetas cuesta `$0,20` y se vuelve a comprar; con
  sesenta juicios humanos dentro **deja de tener precio**. Y `PI-8` no lo cubre:
  `sentences_are_invented()` audita `sentence`, no la **prosa del humano**, en un
  repo público (`[C-007]`). Un portero que dijera validar esa prosa sería el
  instrumento ciego de `LM.15` — pasa verde sobre lo que no ve, y el verde se lee
  como auditado.
- **Alcance honesto del portero:** **no valida los juicios; valida que tengan
  forma**, y aísla lo no validable en **un** campo con nombre (`note`), cuyo
  docstring declara que ningún programa lo audita. Campos cerrados (`verdict`,
  reglas ⊆ rúbrica) por `assert`, `sentence` ∈ `SENTENCES`, y guardia de carpeta
  vacía (`[L-048]`).
- **Toca:** desbloquea `T-106`. 🔴 **`T-108` deja de ser su bloqueante** — se
  propuso como tal por creer que su `glob` alcanzaría a `labels/`, y `T-108`
  endurece `CORPUS_DIR`, que es otra carpeta. Pasa a tarea independiente.

### [D-096] 2026-08-18 — El coste por llamada vuelve a estar medido: $0,00342

- **Se eligió:** `COST_PER_CALL_USD = 0.00342`, el **extremo alto** del intervalo
  que permite la consola (`$0,20 / 60`, redondeado al céntimo → `0,00325–0,00342`).
- **Contra:** el punto medio `$0,00333`; y dejarlo caducado a la espera de una
  cifra sin redondeo.
- **Por qué:** esta constante **calibra un freno**, no describe el mundo. Dentro
  de lo que la medición permite se escoge el lado que falla seguro — mismo
  criterio que `[D-079]`, no uno nuevo. Un divisor pequeño da un tope grande: así
  fue como `[D-078]` dejó pasar `$0,32` contra `$0,25`.
- **Toca:** `MAX_CALLS_PER_RUN` pasa de **82** a **73** — el freno llevaba un día
  dejando pasar nueve llamadas de más. Y el margen al acantilado
  (`int(0,25/x) >= 60`, roto en `$0,00416`) baja de veintidós llamadas a trece.

### [D-095] 2026-08-18 — El archivo de respuestas se nombra por lo que llegó, no por lo que se planeó

- **Se eligió:** calcular el nombre con `replies_file(len(records))`, en una
  variable `written` que usan tanto `save_replies` como el `print` final.
- **Contra:** dejar `replies_file(calls)` y confiar en el AVISO que ya imprime
  `report_lines` cuando la tanda se cortó.
- **Por qué:** el aviso vive en la consola y el nombre vive en el disco. **Lo que
  sobrevive al scrollback era lo que mentía:** 30 filas dentro de un archivo
  llamado `full`. Y como `save_replies` abre en `"w"` y los otros tres ejes
  —modelo, fecha, huella— no cambian dentro del mismo día, una segunda corrida
  cortada borraba la línea base que la primera ya había pagado.
- **Toca:** `eval_rubric.main()`, el nombre de todo corpus futuro, y por tanto lo
  que se promueve a `_persistence/corpus/` bajo `[D-092]`.

### [D-094] 2026-08-18 — La traza cambia `correct: bool` por `outcome` de tres estados, y gana `broken`

- **Se eligió:** `trace.record` escribe **`outcome`** (`"correct"` / `"wrong"` /
  `"bad_format"`) y **`broken`** (los nombres de las promesas rotas). `correct`
  sale del cuaderno.
- **Contra:**
  - Dos booleanos (`correct` + `format_ok`). Cuatro combinaciones, **una
    imposible**, y hay que cruzarlas para saber quién falló.
  - Grabar `broken` y deducir el culpable cruzándolo con `correct`. Es lo mismo
    con otra ropa: dos casillas y una cuenta que se hace mal una vez.
  - Meter `outcome` ahora y retirar `correct` en un cambio aparte. Descartado: una
    tarea aplazada **sin disparador** es `[L-064]`, y habría sido el tercer acto de
    acordarse del día.
- **Por qué:** `split_verdict` devuelve `correct=False` en dos situaciones
  opuestas: la frase estaba mal, o **el juez se saltó el formato**. El cuaderno las
  escribía iguales, y los arreglos van en direcciones contrarias — uno a la clase
  de inglés, el otro a la rúbrica. No da un dato falso: da uno **ambiguo**, y la
  ambigüedad no se ve en la gráfica (`[D-089]`, `LM.15`).
- **Dónde nace, que es lo que impide que se desincronice:** `outcome` se compone en
  **las tres ramas que `split_verdict` ya tenía**. No es un resumen calculado
  después: es lo que esa función siempre supo y tiraba al devolver un `bool`. Y
  `correct` pasa a ser **propiedad derivada**, no campo — no tiene vida propia que
  mantener, así que no puede contradecir a `outcome`.
- **`PI-8`, y la evidencia es de hoy:** `check_reply` corre **dentro** de
  `split_verdict`, donde el texto crudo todavía existe. Del módulo salen nombres de
  promesa y nunca la respuesta entera, porque puede citar dentro la frase de quien
  practica — *"Say: They are my friends"*, fila 4 del corpus promovido esta misma
  sesión. El import de `rubric_check` va dentro de la función porque arriba sería
  ciclo (`[D-091]`).
- **Por qué `broken` además:** contesta otra pregunta. `outcome` dice *quién falló*;
  `broken` dice *qué se rompió*. El caso que lo justifica es `outcome="correct"` con
  `broken=["too_many_sentences"]`: el veredicto aguanta y la forma se está yendo —
  el aviso temprano que `[D-049]` necesita al bajar de modelo.
- **Por qué se sustituye y no conviven:** no hay **ningún** lector de `trace.jsonl`
  en el repo (solo `config.trace_file()`, `app/trace.py` y los tests), así que la
  compatibilidad a proteger era con un lector que no ha nacido. Y `T-102` sigue
  abierta diciendo que la traza no se ha visto escribir con el servidor levantado:
  el archivo puede estar vacío.
- **🚨 Dónde NO corta el bisturí:** `GrammarVerdict.correct` y `TutorReply.correct`
  **se quedan**. Son los que dan el punto en el marcador. Un barrido de `correct`
  que los arrastrara le cambiaría la nota a la gente **en silencio**, porque un
  marcador equivocado sigue pareciendo un marcador. Se retira el campo del
  cuaderno, no el de la clase.
- **Visto morder:** cuatro sabotajes, un rojo cada uno — `outcome` clavado en
  `respond`, `bad_format` degradado a `wrong`, el texto crudo saliendo por `broken`,
  y el punto regalado en el marcador. Los dos guardianes de `[L-073]` salieron
  rojos al añadir los campos: se escribieron los vigilantes **primero** y se amplió
  el conjunto **después**, que es lo que su docstring manda. Suite `526 → 533`.
- **Toca:** `app/tools.py`, `app/english_tutor.py`, `app/api.py`, `app/trace.py`, y
  los tests de los cuatro.

### [D-093] 2026-08-18 — `PI-8` deja de ser una advertencia y pasa a ser una cerradura comprobable

- **Se eligió:** un corpus solo se promueve a `_persistence/` si **todas** sus
  `sentence` están en `SENTENCES`. Lo comprueba `sentences_are_invented()`, y la
  promoción sin esa comprobación no existe como camino.
- **Contra:** dejarlo escrito como comentario junto a la promoción —que era la
  propuesta de esta terminal— y confiar en que quien promueva se acuerde.
- **Por qué:** `[D-092]` abre la puerta de `_persistence/` a archivos de corrida,
  y el repo es público (`[C-007]`). Hoy la puerta es inocente: las 10 filas del
  diagnóstico se comprobaron una por una y ninguna frase la escribió una persona.
  Pero `PI-8` se documenta a sí misma como la más débil de las tres reglas de
  código —*"la respalda una casilla en `protocol-close`, y una casilla pregunta,
  no detecta"*—, y aquí la condición **sí** la puede comprobar un programa. Un
  corpus hecho con frases de gente usando la app falla solo, sin que nadie
  recuerde la regla. Es la diferencia entre escribir en la puerta y ponerle
  cerradura.
- **Alcance real, dicho para no repetir el defecto que denuncia:** cubre el campo
  `sentence`, que es por donde entraría la frase de una persona. **No** audita
  `reply` —eso lo escribe el modelo— ni impide que alguien copie una frase a mano
  en otro archivo del repo. Es un freno estrecho y bien puesto, no una garantía.
- 🔴 **AMPLIADA EL MISMO DÍA, y hacía falta: la cerradura estaba puesta y sin
  echar.** Tal como se cerró primero, `sentences_are_invented()` solo la llamaban
  **tres tests con registros hechos a mano**; nadie la llamaba sobre la carpeta, y
  la promoción es un `mv` manual — así que **invocarla seguía siendo un acto de
  acordarse**, que es literalmente lo que esta decisión existe para eliminar. Y
  `eval_rubric.py:89` ya afirmaba en presente *"la excepción no se apoya en
  acordarse"*: no era mentira sobre el código —la función existe y funciona— pero
  sí una **intención escrita en pasado**, de la clase que nadie vuelve a auditar
  porque tranquiliza (`LM.15`). 🔑 **La forma general, que es la lección del día
  repetida un piso más abajo:** ayer la regla era un comentario y se convirtió en
  función; hoy era una función que había que acordarse de invocar. **El mismo
  defecto con una capa más de pintura.** ✅ **Arreglado con el portero de `T-071`
  sobre `data/`, aplicado a `_persistence/corpus/`:** tres tests que recorren la
  carpeta con `glob` —no con una lista escrita— y corren en cada `pytest` da igual
  quién movió el archivo y por qué vía. (1) toda fila de todo corpus pasa la
  cerradura; (2) ningún corpus congelado lleva la huella **viva** —caza una
  promoción que **sobra**, no una que falta, y cuesta una línea—; (3) la carpeta no
  está vacía, porque **un portero sobre un `glob` sin resultados es verde y no
  vigila nada** (`[L-048]`). 🔻 **VISTO MORDER — tres sabotajes, un rojo cada uno:**
  frase de fuera de `SENTENCES` en la carpeta, corpus congelado con la rúbrica
  viva, y carpeta vaciada. Suite `523 → 526`. 📌 Cazado por la terminal auditora.
- **Toca:** `eval_rubric.py`, `tests/test_eval_rubric.py`, `_persistence/corpus/`,
  la promoción de `[D-092]`, y `PI-8` en `CLAUDE.md`, que pasa a tener un artefacto
  detrás **que se ejecuta solo**.

### [D-092] 2026-08-18 — El nombre del corpus lleva cuatro ejes, y la promoción cuelga del commit que mueve la configuración

- **Se eligió:** `replies_file()` compone el nombre con **modelo, fecha, huella de
  `GRAMMAR_RUBRIC` y marca de selección** (`full` / `pick`). Un corpus se promueve
  a `_persistence/corpus/` **cuando algún eje de su nombre deja de coincidir con
  producción**, y el disparador va pegado al **commit** que mueve `MODEL` o
  `GRAMMAR_RUBRIC`.
- **Contra:**
  - Abrir en `"a"` en vez de `"w"`. Descartado: sobrescribir está bien razonado en
    su propio docstring —dos modelos o dos rúbricas revueltos son `[L-071]`—. El
    fallo no era el modo de apertura, era el **nombre**.
  - Solo modelo y fecha. Pierde la rúbrica, que es el eje que ya se movió dos
    veces sin dejar rastro, y pierde la marca de selección.
  - *"Corpus que respalda una decisión firmada"*. Se estira: todo acaba
    respaldando algo.
  - *"Corpus cuya rúbrica ya no existe en producción"* —propuesta de esta
    terminal—. Dos fallos, y el segundo es el grave. **Pierde el eje del modelo**,
    que es justo el que `[D-049]` va a mover tres veces: un corpus de Opus 5 con
    la rúbrica intacta deja de ser repetible el día que `MODEL` baje a Sonnet, y
    ése es **la línea base contra la que se mide el descenso**. Y es
    **retrospectivo**: al crear un corpus la rúbrica está viva por definición, así
    que nada se guardaría nunca al nacer — la evidencia esperaría en `data/`,
    ignorado por Git y en un solo disco, exactamente mientras se la considera
    "todavía no valiosa".
- **Por qué:** el criterio elegido **es el propio nombre**. No se estira porque los
  ejes son los que son, lo comprueba un programa en vez de un juicio, y cubre el
  modelo. Y el disparador pegado al commit es el patrón que `[D-081]` ya usa —leer
  el límite por minuto y ponerlo en `LAB_REQUESTS_PER_MINUTE` en el mismo cambio—:
  la acción cuelga de un evento que ocurre seguro y se nota seguro, no de que
  alguien caiga en la cuenta más tarde.
- **Los tres ejes nuevos, uno a uno:**
  - **Modelo:** ya viajaba dentro de la fila, así que en el nombre no añade
    identidad nueva, pero hace falta para que dos corridas no se pisen.
  - **Rúbrica:** no estaba en ningún sitio —ni en la fila ni en el nombre—, y es el
    eje que más se mueve: `678 → 1.016` caracteres (`[D-066]`/`[D-067]`) y
    `1.016 → 1.098` el 2026-08-17 (`[D-090]`/`[D-091]`). La fecha no lo tapa: la
    línea base corrió a las 21:43 UTC y el diagnóstico a las 21:54, **mismo día**,
    con la rúbrica cambiada entre medias.
  - **Selección:** el archivo en disco tiene 10 filas y **10 rotas**, y eso no es un
    resultado: es la selección. Se escogieron a propósito las que habían fallado.
    Quien lo divida mañana obtiene `100% de fallo` y se lo cree.
- **La huella se calcula, no se teclea:** `sha256` de `GRAMMAR_RUBRIC` ya montado,
  ocho caracteres. Mismo motivo por el que `replies_file()` es una función y no una
  constante (`[D-085]`): se pregunta en cada llamada en vez de fiarse de que
  alguien mantenga el dato. La huella de la rúbrica jubilada salió del blob de Git
  **por programa**: `9844eac^:app/tools.py` la tenía como cadena llana, 1.016
  caracteres. Vieja `67a8a252`, actual `bbf4be38`.
- **🔻 TRAMPA ARMADA PARA LA PRÓXIMA RECONSTRUCCIÓN, y hoy no se disparó por
  suerte sino por construcción.** La huella se calcula sobre la rúbrica **ya
  montada**, y la de hoy es un `f-string` con `{MAX_SENTENCES}` dentro. La vieja
  **no lo era**: el `two` estaba en letra, porque `MAX_SENTENCES` todavía no
  existía. Por eso reconstruirla desde el blob dio el número bueno sin margen de
  error.

  🚨 **A partir de la rúbrica de HOY deja de ser así.** Quien recalcule mañana la
  huella de la rúbrica de este commit tiene que montarla con el `MAX_SENTENCES`
  **de ese mismo commit**, no con el de entonces. Montarla con la constante
  vigente da un hash distinto **y con el mismo aspecto que el bueno**: no hay
  error, no hay aviso, y el corpus queda etiquetado con una identidad que no es la
  suya. 📌 La comprobación barata: reconstruir el módulo entero desde el blob de
  ese commit, nunca pegar la plantilla en el intérprete de hoy. Verificado por la
  terminal auditora recalculando las dos huellas desde el AST, sin usar este
  código.
- **Qué se movió hoy:** las 10 filas del diagnóstico del 2026-08-17 —evidencia
  primaria de `[D-090]` y `[D-091]`— salen de `data/` y entran en
  `_persistence/corpus/`. No se borran: su rúbrica ya no está en producción, así
  que no se pueden volver a levantar **ni pagando**. Las corridas **vivas** siguen
  escribiendo en `data/`; solo se promueve lo congelado.
- **Toca:** `eval_rubric.py`, `tests/test_eval_rubric.py`, `_persistence/corpus/`,
  el disparador de `[D-049]`, y `T-106`, que dejaba de poder etiquetar nada.

### [D-091] 2026-08-17 — Se endurece la rúbrica en vez de afinar el corrector, porque la opción fina no se puede construir

**Qué se decidió.** Dos cosas que van juntas, firmadas por el usuario el
2026-08-17:

1. `GRAMMAR_RUBRIC` prohíbe **todas** las comillas dobles, no solo las que
   envuelven la corrección — y lo dice **en su propia línea**.
2. `MAX_SENTENCES` deja de estar escrito dos veces. Vive en `app/tools.py`, la
   prompt lo mete con una `f-string`, y `app/rubric_check.py` lo **importa**.

**Contra qué.** Afinar `_has_markdown` para que mirara solo las comillas
alrededor de la corrección, que era lo que el falso positivo de la frase 14
parecía pedir.

---

#### 🚨 Por qué la opción fina se descarta: no es cara, es imposible

El módulo se abre declarando su propia frontera: *"tres necesitan que una persona
lea la respuesta y opine; las otras cuatro las comprueba un programa sin
opinar"*.

Para mirar solo las comillas *alrededor de la corrección*, el programa tiene que
saber **qué trozo es la corrección**. Nadie se lo dice: la respuesta no lleva
delimitador. En las nueve `FIX` que hay en disco, la corrección entra de **cinco
formas distintas**:

```
Say: She goes to school every day.
We say: I am 20 years old.
It should be: My sister has a dog.
The correct sentence is: Where are you going?
He doesn't like pizza.          ← fila 5, sin ninguna entradilla
```

La fila 5 no tiene ancla. Cualquier detector sería una **heurística sobre la
manera de hablar del modelo**.

> 🔑 **Y el fraseo es exactamente lo que `[D-049]` va a mover.** Bajar a Sonnet 5
> y a Haiku 4.5 lo cambia. Cuando la heurística fallara en esa corrida, *"el
> modelo se rompió"* y *"la heurística resbaló"* llegarían como el mismo dato.

**Es la enfermedad que `[D-090]` acaba de curar en el tope saturado, metida otra
vez en la promesa de al lado.** Y de propina, una de las cuatro promesas
mecánicas dejaría de serlo, con la cabecera del módulo explicando justo por qué
son esas cuatro.

📌 Hallazgo de la terminal auditora. Las cinco formas se verificaron aquí contra
`data/eval_replies.jsonl` antes de aceptarlo.

---

#### El precio de lo elegido, dicho entero

El modelo pierde una forma legítima de nombrar una expresión: *"you used going to
for the future perfectly"* va sin comillas. **Es real.** Se paga barato porque
para un A1 se entiende igual, y porque **entra gratis en este cambio**: la línea
base de 60 ya hay que rehacerla por el tope de frases, así que no cuesta una
corrida extra. Dejarlo para después sí costaría una.

⚠️ **Y va en su propia línea a propósito.** Antes era el cuarto ítem de una frase
sobre markdown — **y una comilla no es markdown**. Por ahí se separaron la
rúbrica y el corrector sin que nadie lo notara.

---

#### 🔒 La segunda mitad: el aviso cruzado de `[D-090]` era una nota, no un freno

`[D-090]` dejó `MAX_SENTENCES` en `rubric_check` y el `three` a mano en la
prompt, con **dos comentarios vigilándose**. Un comentario no pone nada en rojo.

Ahora el número vive en `app/tools.py`, junto a la rúbrica que lo escribe.
📌 **La dirección no es de gusto:** `rubric_check` ya importaba
`VERDICT_CORRECT`/`VERDICT_WRONG` de `tools`, así que ponerlo al revés sería un
import circular.

---

#### 🔻 Visto morder — tres sabotajes, un rojo cada uno

| sabotaje | qué se puso en rojo |
|---|---|
| la prompt vuelve a `at most two` escrito a mano | `test_the_rubric_asks_for_the_number_the_checker_measures` |
| la comilla vuelve a estar condicionada a la corrección | `test_the_rubric_forbids_every_quotation_mark…` |
| se restaura la copia de `COST_PER_CALL_USD` | `test_the_wallet_is_imported_not_copied` |

Suite **513 → 516**.

---

### [D-090] 2026-08-17 — El tope de la rúbrica sube de dos frases a tres, y el motivo escrito en `[D-089]` no era el bueno

**Qué se decidió.** `GRAMMAR_RUBRIC` pasa de *"at most two short sentences"* a
*"at most three"*, y `rubric_check.MAX_SENTENCES` de `2` a `3`. **Firmado por el
usuario el 2026-08-17**, que es lo que `PI-6` exige para mover un listón.

**Contra qué.** Dejar el tope en dos y apretar la rúbrica por el otro lado
—añadir *"be warm inside those two sentences, not in a third"*—, que conserva
respuestas más cortas, y para un A1 más corto casi siempre es mejor.

---

#### 🔴 El motivo que traía `[D-089]` no aguanta, y se dice aquí en vez de heredarlo

`[D-089]` cerró con esta hipótesis: *"una corrección natural son dos frases y el
tono cálido que la rúbrica también pide añade la tercera; si es eso, la rúbrica
pide dos cosas que compiten"*.

**Leída entera, la rúbrica no pide tres cosas para `FIX`.** Pide dos:

> *"give the corrected sentence and name the one mistake that matters most"*

Lo cálido sale de la línea de personaje —*"a warm, encouraging tutor"*—, que es
**tono, no un renglón**. El modelo eligió gastar una frase entera en el tono,
pero eso es una elección suya, no una contradicción de la rúbrica.

🔑 **Y si ese fuera el argumento, la conclusión correcta sería la contraria:**
apretar el tono dentro de las dos frases y quedarse con respuestas cortas — que
es lo que la propia rúbrica defiende. Hallazgo de la terminal auditora,
verificado aquí contra `app/tools.py:260-283`.

---

#### Los dos motivos que sí deciden

**(1) El `dos` hacía un trabajo que otra promesa ya hace.** La razón escrita del
tope es *"A1 learners give up when a reply is a list of everything they did
wrong"* — o sea, el miedo es a una **lista de errores**, no al largo. Y de eso ya
se encarga, por escrito y aparte, *"never correct more than one thing at a
time"*. El tope de dos cobraba dos veces por lo mismo.

**(2) 🚨 Una promesa que el mejor modelo rompe casi siempre no es un instrumento,
es una constante.** `too_many_sentences` salía roja **18 de 60 con Opus 5**, y
`bad_first_line` a **0** descarta que sea incapacidad de seguir instrucciones.

`[D-049]` existe para bajar a Sonnet 5 y luego a Haiku 4.5 **midiendo cuándo se
les va la forma**. Con la promesa ya rota arriba, *"a Haiku se le fue la forma"* y
*"esto ya estaba rojo"* llegan al cuaderno como el mismo dato. Es `LM.15` por el
lado contrario: allí un número ambiguo, aquí **un rojo permanente que dejó de
significar algo**.

---

#### 🔻 Visto morder, en los dos sentidos

`PI-6` obliga a que el rojo existiera, y un listón que sube es justo donde eso se
finge más fácil. Se hizo en este orden:

1. **Primero el test al borde nuevo, con el código viejo** → rojo: la respuesta
   de tres frases (*aliento + corrección + explicación*) marcada como rota.
2. Después el código.
3. **Con el tope ya en tres, sabotaje aflojándolo a cuatro** → **3 tests en
   rojo**, incluido `test_more_than_three_sentences_is_caught`.

Suite **512 → 513** (el borde nuevo añadió un caso). 🔑 **El segundo sabotaje es
el que importa:** demuestra que subir el listón no fue quitarlo.

---

#### 💰 Lo que esto rompe, escrito en el código y no solo aquí

🔴 **`COST_PER_CALL_USD` queda CADUCADO, y hacia el lado malo.** El número
describe un perfil de 49 tokens de salida; tres frases son más. El coste real
sube, el número guardado se queda **por debajo**, y `MAX_CALLS_PER_RUN` sale de
**dividir** por él: divisor pequeño, tope grande. El freno de la tanda deja pasar
**más** llamadas de las que caben en `$0,25`.

Es `[D-078]` repetido — entonces valía `$0,00234` y dejó pasar `$0,32` contra un
presupuesto de `$0,25`.

📌 **Se deja el número viejo sin inventar otro** (regla 6: un número sin corrida
detrás no se escribe). La corrección sale sola de la próxima corrida de 60. El
aviso está en `measure_tutor.py`, donde lo lee quien vaya a gastar.

---

#### ⚠️ Lo que NO se decide aquí

**La otra mitad de `T-104` sigue abierta:** `_has_markdown` rechaza **cualquier**
comilla doble y la rúbrica solo prohíbe las que envuelven la corrección
(`[D-089]` lo cazó en la frase 14). Se afina la comprobación o se endurece la
rúbrica — sin firma todavía.

---

### [D-089] 2026-08-17 — Los evals arrancan por la FORMA de la rúbrica, no por el veredicto: cuatro promesas que comprueba un programa sin opinar

> 🔴 **ENMENDADA EL MISMO DÍA, y solo en una parte — léela antes de citar esta
> entrada.**
>
> **Lo que sigue en pie:** las cuatro promesas mecánicas, la línea base medida
> (`40 limpias de 60`, `too_many_sentences` **18**, `has_markdown` **5** como
> techo), el agujero de observabilidad de `split_verdict`, y el falso positivo
> de la frase 14.
>
> **Lo que quedó DESMENTIDO:** la hipótesis del cierre —*"la rúbrica pide tres
> cosas y le da sitio para dos, porque el tono cálido añade la tercera"*—. Leída
> entera, para `FIX` la rúbrica pide **dos** cosas (*"give the corrected
> sentence and name the one mistake that matters most"*); lo cálido es **tono,
> no un renglón**. 🔑 Si ese fuera el argumento, la conclusión correcta sería la
> contraria: apretar el tono dentro de dos frases. **El tope subió igual, pero
> por los motivos de `[D-091]` y `[D-090]`, no por éste.**
>
> **Lo que resultó FALSO por omisión:** *"las 60 frases de la línea base"*. Nunca
> se guardaron — el archivo tiene 10 filas. Ver `[L-076]`.
>
> 📌 Se enmienda **aquí arriba y no en un bloque debajo**: quien busca por tema
> cae en esta entrada, y lee lo primero que encuentra.

- **Se decidió:** partir `GRAMMAR_RUBRIC` en las **siete** cosas que pide, y
  empezar por las **cuatro que no necesitan que nadie opine**:

  | promesa | cómo se comprueba |
  |---|---|
  | la primera línea es `OK` o `FIX` a secas | comparación de cadena |
  | nada de markdown, viñetas ni comillas | búsqueda de caracteres |
  | como mucho dos frases | conteo de cierres |
  | `OK`/`FIX` no se le escapan al alumno | palabras sueltas, con mayúsculas |

  Las otras tres —si el veredicto acierta, si corrigió un error o tres, si se fue
  del tema— **quedan para después**: exigen etiquetar las 60 frases a mano o leer
  las respuestas.

- **Contra:** empezar por el veredicto, que es lo que suena a "eval de verdad".

- 🔑 **Por qué las mecánicas primero, y no es que sean las fáciles: son las que se
  van a romper.** `[D-049]` baja el modelo a Sonnet 5 y luego a Haiku 4.5. Un
  modelo pequeño **no deja de ver** que una frase A1 está mal —eso es gramática de
  primer año—; lo que se le va es **la forma**. Y la forma **sale a la pantalla**:
  `app/static` pinta el mensaje tal cual, así que un asterisco llega como un
  asterisco delante de alguien que no sabe si es parte de la corrección.

- 🚨 **Y por el camino apareció un agujero de observabilidad que vale más que el
  eval, verificado en disco.** `split_verdict` (`tools.py:601`) hace lo correcto
  cuando el modelo rompe el formato —no da el punto, enseña el mensaje entero—
  **pero no se lo cuenta a nadie**, y la traza escribe `correct: bool`:

      el juez rompe el formato  ->  correct=False
      el alumno se equivoca     ->  correct=False

  **Dos causas opuestas, un solo número.** El día que el modelo nuevo empiece a
  romperse, `trace.jsonl` dirá *"la gente falla más"* cuando lo cierto sea *"el
  juez dejó de contestar como se le pidió"*, y los arreglos van en direcciones
  contrarias: uno a la rúbrica, el otro a la clase de inglés. Es `LM.15` dentro del
  paso que se llama **Observabilidad**: no da un dato falso, da uno **ambiguo**, y
  la ambigüedad no se ve en la gráfica.

  📌 **Queda escrito y NO cableado.** Que la ruta llame al corrector y la traza
  apunte el fallo de formato es un cambio en `app/api.py` y **se decide aparte**.

- 🏗️ **Dónde vive cada cosa, y por qué:** el corrector en `app/rubric_check.py`
  —al lado de la rúbrica que comprueba, o las dos se separan sin que nadie lo
  note— y el runner en `eval_rubric.py`, junto a `measure_tutor.py`, que es el
  precedente de un instrumento que cuesta dinero.

- 🚨 **La excepción de `[L-057]` NO se hereda, y esto es lo más fácil de copiar
  mal.** `measure_tutor.py` sube el `read` a 30 s porque **está midiendo ese
  tope** y un instrumento no puede medir el suyo. Este eval mide **la forma**, no
  el reloj, así que usa el `read` de producción (6,5 s): lo que interesa es la
  rúbrica *tal como la vive la app*. ⚠️ Precio dicho antes de correr: una llamada
  que cruce los 6,5 s deja de dar muestra — **no en silencio**, el guion para y el
  informe avisa de que la tanda es parcial.

- 🔍 **El obstáculo real y cómo se resolvió sin tocar producción.**
  `judge_grammar` devuelve `GrammarVerdict`, o sea que **tira la primera línea**,
  que es justo lo que la promesa 1 mide. Se resolvió heredando de
  `RecordingClient` —que ya existía en `measure_tutor.py`— y apuntando el texto
  crudo al pasar, **por el parámetro `client` que ya usan los tests**. Cero
  cambios en `app/tools.py`. 📌 Y el precio de repetir la línea que saca el texto
  (`tools.py:542`) está **atado con un test** que exige que las dos formas den el
  mismo veredicto, con y sin bloque `thinking` delante.

- 💰 **El freno del gasto es EXACTAMENTE el plan: 60 llamadas, ni una más.**
  `measure_tutor` deja 82 (`$0,25 / $0,00304`) porque su tanda se recorta sola;
  aquí el plan es fijo. 🔑 **Un tope ajustado caza el bucle roto en la llamada 61;
  uno holgado lo caza veintidós después, y esas veintidós ya se pagaron.**

- ⚠️ **Lo que este eval NO puede decir, impreso en su propia salida y no solo en
  el docstring:** un informe limpio significa *"contestó con la forma pedida"*,
  **nunca** *"juzgó bien"*. La advertencia viaja **con el número** por `LM.20`:
  quien lea la salida pegada en un chat no va a abrir el archivo.

- ⏳ **Y el número solo vale comparado consigo mismo**, así que la línea base del
  modelo de hoy hay que tomarla **antes** de bajar de modelo, o no habrá contra qué
  comparar. Mismo método que `[D-079]` con el coste: sellar antes de mirar.

- 🔻 **VISTO MORDER — trece sabotajes con su rojo, y dos enseñaron algo.**
  `445 → 501` tests (26 del corrector + 19 del runner). Los cuatro frenos del
  corrector en rojo uno a uno; el alambre contra la deriva en rojo al quitarle el
  `.upper()` que `split_verdict` sí hace; el conjunto `PROMISES` en rojo con una
  quinta promesa muda. 🔑 **Y uno de mis sabotajes salió VERDE y el fallo era del
  sabotaje:** escribí *"medicion"* sin tilde para probar el freno de `[L-001]`, así
  que no saboteé nada. Repetido con tilde de verdad: `UnicodeEncodeError`. **Un
  sabotaje que no rompe nada no es un sabotaje** — misma familia que el sabotaje
  que rompe la carga de `[D-086]`.

- 📖 **LÍNEA BASE MEDIDA — Opus 5, 2026-08-17, 21:43:47 → 21:46:56 UTC.** Las 60
  frases, las 60 llamadas, **ninguna cortada**: la tanda no es parcial.

  | promesa | rotas de 60 |
  |---|---|
  | `bad_first_line` | **0** |
  | `leaks_keyword` | **0** |
  | `has_markdown` | **5** |
  | `too_many_sentences` | **18** |

  **Limpias del todo: 40 de 60.** Coste estimado `60 × $0,00304 = $0,1824`; el real
  se lee en la consola, no aquí (regla 6).

- 🚨 **Y el resultado acusa a la RÚBRICA, no al modelo — con el argumento que ya
  estaba escrito en `tools.py:38-39`:** *"con Opus, un veredicto malo solo puede
  acusar a la rúbrica"*. Esto es el modelo **más** capaz del catálogo saltándose
  *"at most two short sentences"* en **18 de 60**, y el `bad_first_line` a **0**
  descarta que sea un problema de seguir instrucciones en general: **la promesa que
  falla es la del largo, y solo esa.**

- 🔍 **Hipótesis SIN COMPROBAR de por qué las 18, y se marca como hipótesis
  (regla 6):** una corrección natural son dos frases —la frase arreglada y la
  explicación— y el tono cálido que la rúbrica **también** pide añade una tercera
  (*"keep going!"*). Si es eso, la rúbrica se está pidiendo dos cosas que compiten
  y el modelo elige el tono. **No se puede confirmar con esta corrida**, por lo de
  abajo.

- 🔴 **HUECO DEL INSTRUMENTO, encontrado al leer su propio resultado: la corrida
  cuenta y TIRA la evidencia.** `eval_rubric.py` no guarda las respuestas, así que
  el `18` no se puede investigar sin **volver a pagar `$0,18`**. Es `[L-071]` otra
  vez —*cuadrar contra un agregado no es cuadrar*— cometido en un instrumento
  nuevo el mismo día que se citó la lección: hay un total y no hay desglose, y la
  pregunta *"¿son tres frases de verdad o mi contador cuenta puntos de abreviatura?"*
  necesita el texto. ⚠️ **Y lo caro no es el hueco, es cuándo se nota:** el número
  sorprendente aparece **después** de que el dinero ya se gastó.

- ✅ **HIPÓTESIS CONFIRMADA con el texto delante — corrida de diagnóstico de 10
  frases, 2026-08-17 21:54 UTC, `$0,03`.** Se guardaron las respuestas y se
  eligieron **las 10 que habían fallado**, no diez al azar. **Volvieron a fallar las
  10**, así que es reproducible y no ruido. Y el patrón es el mismo en las nueve de
  `too_many_sentences`:

      [aliento] + [frase corregida] + [explicacion] = TRES frases

  Ejemplo real, frase 4 (`"They is my friends"`):
  *"Almost there! Say: They are my friends. With they, we use are, not is."*

  🚨 **La rúbrica se pide a sí misma tres cosas y le da sitio para dos.** Pide
  *"warm, encouraging"*, pide **la frase corregida**, pide **nombrar el error** — y
  luego dice *"at most two short sentences"*. **No es que el modelo desobedezca: es
  que las dos instrucciones no caben juntas**, y el modelo elige el tono, que es lo
  que la rúbrica pone primero. 📌 Comprobado a mano que no es un artefacto del
  contador: las nueve tienen **exactamente 3 cierres** y leyéndolas son 3 frases de
  verdad, sin puntos de abreviatura.

- 🔴 **Y el mismo diagnóstico cazó un FALSO POSITIVO en mi propio instrumento.** La
  frase 14 (`"We are going to the beach tomorrow"`, que es **correcta**) salió como
  `has_markdown` por esto: *"you used "going to" for the future perfectly"*. Las
  comillas están **nombrando una expresión gramatical, no envolviendo una
  corrección** — y la rúbrica prohíbe exactamente *"no quotation marks **around the
  correction**"*. 🔑 **Mi comprobación es más estricta que la regla que dice
  comprobar**, y estaba avisado en su docstring como *"la parte basta"*: se aceptó
  a propósito porque un aviso de más se investiga y uno de menos no se sabe que
  faltó. **Se investigó y era de más.** ⚠️ Así que de los `5` de `has_markdown` de
  la línea base, **un número desconocido son falsos positivos**: ese `5` es un
  techo, no una medida.

- 🔴 **Tercer fallo cosmético que solo se ve corriendo: la cuenta de progreso
  imprimía `[12/10]`.** Se mezclaba el número de la frase en la lista de 60 con la
  posición dentro de la tanda; con la tanda entera coinciden y con una parcial no.
  Corregido a `[ 6/10] frase 12`.

- 🔴 **Segundo fallo, y es `PI-4` cobrando limpio: el guion no arrancaba.** Le
  faltaba `config.load_env_file()` —que `measure_tutor.py:407` sí tiene—, así que
  moría sin llave antes de llamar a nadie. **Los 19 tests estaban en verde y no
  podían cazarlo:** ninguno llama a `main()`, porque `main()` hace red. *"Lo que no
  se ha corrido no está terminado, aunque el código exista."* 📌 Y queda dicho que
  **nadie lo vigila**: `tests/test_measure_tutor.py` tampoco tiene freno para eso,
  así que los dos guiones dependen de que quien los escriba se acuerde.

- 🔻 **ABIERTA — lo que esta entrada NO decide, y espera firma del usuario.** Se
  preguntó al final de la sesión y se quedó sin contestar; **no se tocó nada**:

  1. **¿Sube el tope a TRES frases**, en `GRAMMAR_RUBRIC` y en
     `rubric_check.MAX_SENTENCES`? 🔑 **El argumento a favor sale de la propia
     rúbrica:** su razón escrita para el tope de dos es *"A1 learners give up when a
     reply is a list of everything they did wrong"* —o sea el miedo es a una **lista
     de errores**, no a la longitud— y de eso ya se encarga otra promesa distinta,
     *"never correct more than one thing at a time"*. **El tope de dos hace un
     trabajo que otra promesa ya hace, y a cambio rompe el tono que la rúbrica pide
     en su primera línea.** La alternativa es dejarlo en dos y pedirle que meta el
     aliento dentro de la frase de la corrección: más apretado y más difícil de
     obedecer.
  2. **¿Se afina la comprobación de comillas** para que solo mire las que envuelven
     una corrección, o se endurece la rúbrica para prohibirlas todas? Hoy el
     corrector es **más estricto que la regla**.

  🚨 **Y una consecuencia que hay que decir antes de tocar la rúbrica, no después:
  cambiarla CADUCA el `$0,00304`.** Lo dice `measure_tutor.py:85-88` — ese precio
  describe un perfil de 361 tokens de entrada, *"y `GRAMMAR_RUBRIC` ya lo movió una
  vez sin que nadie se enterara"*. Si se cambia, el coste por llamada deja de estar
  **medido** y con él el tope de las tandas: habría que volver a leer la consola.
  Ver `[L-059]`.

- **Toca:** `app/rubric_check.py` (nuevo), `eval_rubric.py` (nuevo),
  `tests/test_rubric_check.py` (nuevo), `tests/test_eval_rubric.py` (nuevo),
  `measure_tutor.py` (se importa, no se toca), `app/tools.py` (se lee, no se
  toca), `[D-049]`, `[D-079]`, `[D-085]`, `[D-086]`, `[D-087]`, `[C-009]`,
  `[L-001]`, `[L-023]`, `[L-043]`, `[L-048]`, `[L-057]`, `[L-059]`, `[L-073]`,
  `[L-075]`, `LM.15`, `LM.20`, `PI-8`, paso 9.

---

### [D-088] 2026-08-17 — `T-103` se PARA con disparador de acción: un freno que no se puede ver morder es una nota, y se escribe como nota

- **Se decidió:** **no** poner hoy el `if` protector de `T-103`. La tarea queda
  parada, con **disparador de acción** —igual que `T-102`—: se arregla **el día que
  el camino del timeout escriba traza**, y en ese mismo cambio, no antes.

- **Contra:** ponerlo hoy, que era mi propuesta y llegué a presentarla como *"lo
  único de código listo para arrancar"*.

- **Por qué, y es `PI-6`/`PI-7` leídas al pie de la letra:** las dos se comprueban
  **viendo el rojo**, y este freno no puede ponerse rojo. Verificado en disco, no
  razonado:

  | qué | dónde |
  |---|---|
  | el camino del timeout termina | `app/api.py:804`, `raise HTTPException(504)` |
  | el bloque que lee `tutor_started[0]` | `app/api.py:906` |

  **La 906 está después de la 804.** `attempt.cancel() == True` deja la lista vacía,
  sí, pero por ese camino **nadie la lee**: no hay entrada que provoque el
  `IndexError`, así que no hay test que lo cace y no hay rojo que enseñar. Un `if`
  ahí sería exactamente lo que `[L-048]` describe —*un guardián que se cumple solo
  es peor que ninguno, porque además tranquiliza*— y encima marcaría la tarea como
  cerrada.

- 🔍 **La salida que SÍ mordería, escrita para cuando llegue el disparador:** no
  proteger la línea, sino **llamar al bloque que escribe la traza con
  `tutor_started` vacía, ver el `IndexError` de verdad, y entonces poner el freno.**
  Eso convierte `T-103` en algo que se puede ver morir. Se descarta hoy porque
  fabricar ese escenario exige inventar un camino que el código no tiene, y eso es
  probar el andamio en vez del edificio.

- ✅ **Lo que YA está hecho y es lo que corresponde a una nota: el aviso, en los dos
  sitios y con la salvedad dentro.** `app/api.py:892-897` dice *"Ese camino no
  escribe traza hoy"* y nombra la línea a mirar primero; el docstring de
  `tests/test_api.py:690-693` va más lejos y dice lo que ningún test puede decir de
  sí mismo: ***"el día que la escriba, este test seguirá en verde y no avisará"***.

- 🔴 **Y el error que precedió a esta decisión es mío, de resumen y no de código.**
  El código llevaba la salvedad escrita; **el reporte de arranque se la comió** y
  presentó *"un `IndexError` se comería la fila entera"* como un bicho vivo del
  presente, cuando es condicional a futuro. 🔑 **El documento era mejor que su
  resumen** — la misma forma ya anotada para la sesión 54, y peor aquí porque el
  resumen es lo que se lee al arrancar el día y el documento no.

- 🚨 **Quién firma, porque esto es la mitad del asunto.** Había **dos votos
  técnicos** —esta terminal y la auditora, los dos verificados contra el disco— y
  eso **no es la decisión**: `PI-6` dice que la firma la pone quien lleva el
  proyecto, no la sesión que construye ni la terminal que audita. **Se pidió
  explícitamente y el usuario la dio.** Un voto verificado sigue siendo un voto.

- **Toca:** `T-103`, `T-102`, `app/api.py` (líneas 804, 892-897, 906),
  `tests/test_api.py:682-693`, `PI-6`, `PI-7`, `[D-087]`, `[L-048]`, `[L-064]`
  (aplazada contra armada: ésta es **parada**, y su disparador es una acción del
  código, no una fecha), `[L-065]`, `[L-069]`, paso 9, auditoría externa del
  2026-08-17.

---

### [D-087] 2026-08-17 — El tiempo se parte en TRES —cola, modelo, resto—, y no en las cuatro fases, que no se pueden medir

- **Se decidió:** la traza guarda `queue_seconds`, `model_seconds` y
  `rest_seconds`, además del `seconds` total que ya tenía.

  ```
  seconds = queue_seconds + model_seconds + rest_seconds
  ```

- **Contra dos alternativas, y las dos venían de fuera:**

  | descartada | por qué |
  |---|---|
  | las cuatro fases `connect`/`write`/`pool`/`read` | **no se pueden medir** — ver abajo |
  | dos números (total y modelo), dejando el resto por resta | **exculpa al modelo por el motivo equivocado** — ver abajo |

---

#### 🔴 Por qué las cuatro fases no se pueden medir, verificado en el disco

Son **topes, no medidas**. `app/tools.py:245` entrega un presupuesto a la
librería: dice cuánto se les *permite* durar, no cuánto duraron. Nadie las
cronometra, y el dato no existe aguas abajo. Comprobado en las **dos** librerías
de este `.venv` —no de memoria, no de documentación:

```
httpx  0.28.1   _client.py:157   elapsed = time.perf_counter() - self._start
httpx2 2.9.1    _client.py:157   elapsed = time.perf_counter() - self._start
```

Un solo número cada una, y es el total de la respuesta entera.

🔑 **Y `[D-085]` queda ENMENDADA, no matizada.** Decía que *"la arquitectura ya
piensa en fases; el registro no las escribe"* — cierto palabra por palabra y
engañoso en conjunto: se lee como que los números existen y solo falta apuntarlos.
La propuesta de las cuatro fases **nació de leer esa frase**, así que un asterisco
debajo no habría servido: una regla con asterisco se sigue leyendo como regla.

📌 **Y la razón se escribe en `app/trace.py`, no solo aquí** — `LM.20`, *"una
copia correcta que nadie alcanza"*. Quien vuelva a proponer las cuatro fases
llegará mirando la tabla de `tools.py:182-185`, no `decisions.md`.

---

#### ⏱️ Por qué TRES y no dos

Dos números —total y modelo— parecen bastar, y no bastan. El reloj de la ruta
arranca **antes** del `submit` a propósito (`[L-013]`: se mide lo que espera la
persona, cola incluida). Entonces `seconds − model_seconds` no es *"nuestro
código"*: es **"cola + nuestro código"** revuelto.

🚨 **Con los hilos ocupados la cola se dispara, y el descenso de modelo de
`[D-049]` parecería inútil cuando el culpable sería la cola.** Es exculpar al
modelo por el motivo equivocado — justo el fallo que el reparto existe para
evitar.

⚠️ **Y la cola NO sale por resta:** se saca con una marca al arrancar `respond`,
comparada con `started`. Vive entera en `api.py`, que es quien tiene los dos
relojes; **no pasa por ninguna caja de datos.**

---

#### 🏗️ Dónde se mide cada uno, y por qué la nota sube UN piso y no tres

| número | quién lo mide | cómo |
|---|---|---|
| `queue_seconds` | `api.py` | cierre **por petición** que apunta `perf_counter()` al arrancar el tutor |
| `model_seconds` | `english_tutor.respond` | reloj alrededor de la línea `judge_grammar(sentence)` |
| `rest_seconds` | `trace.record` | **calculado**, nunca recibido |

🔑 **`GrammarVerdict` NO se toca, y ese fue el hallazgo que ahorró el trabajo.**
La primera propuesta —mía— fue meter el reloj dentro de `judge_grammar` y hacerlo
subir tres pisos. No hace falta: `respond` ya tiene la llamada al modelo aislada
en una línea propia, así que **un `perf_counter` alrededor de esa línea mide lo
mismo sin entrar en la función**. `GrammarVerdict` tiene dos campos y los dos son
del juez; ahí sí habría sido contaminación.

⚠️ **Lo que se pierde midiendo desde fuera no es una pérdida:** entran también
construir el cliente y leer la respuesta. El handshake vive ahí, y es parte de lo
que cuesta preguntar. Y no hay reintentos que ensucien el número —
`tools.py:64`: `MAX_RETRIES = 0`, deliberado. **Si algún día deja de ser cero,
`model_seconds` pasa a significar "todos los intentos juntos"** — sigue siendo el
número correcto para observabilidad, pero deja de compararse con el precio de una
llamada.

🚨 **El cierre de la cola es por petición, no una variable de módulo.** La lista
se crea dentro del handler, así que dos prácticas simultáneas no se pisan el
número. Con una global se pisarían **en silencio**, dando un dato plausible y
falso — que es peor que no tenerlo.

---

#### 🔴 Y aquí me equivoqué dos veces, las dos corregidas por la auditoría

**(1) Defendí la pureza de una caja que ya no la tenía.** Argumenté que meterle un
reloj a `TutorReply` le cambiaba el significado, *"de qué dijo el tutor a qué dijo
y cuánto tardó"*. Falso: de sus cinco campos, **tres no vienen del juez** desde
`[D-066]` — `words` lo cuenta `respond` en local, `score` y `practice` salen del
archivo de contadores. `TutorReply` es *"lo que la ruta necesita saber de esta
práctica"*, y el reloj encaja en el significado que **ya tenía**.

🔑 **Lo que me llevó al error estaba escrito en el propio código: el docstring
decía *"en tres piezas separadas"* y ya eran cinco.** Corregido. **Una caja que se
describe más pequeña de lo que es invita a defenderle una pureza que ya perdió**
— y el mismo día se encontró la misma costumbre en la cabecera de
`tests/test_trace.py`, que enumeraba tres tests de cinco. También corregida.

**(2) Propuse medir dentro de `judge_grammar`**, tres pisos de viaje, cuando
`respond` ya tenía la línea aislada. Menos trabajo y menos invasivo.

---

#### 🔻 Visto morder, porque un test que nunca falló no probó nada

**El alambre de `[L-073]` —el conjunto de campos de `TutorReply` clavado— se puso
rojo solo al añadir `model_seconds`.** Segunda vez que se le ve morder:

```
E   AssertionError: Extra items in the left set: 'model_seconds'
```

Y se siguió su propia instrucción: **no editar el conjunto primero**, sino
escribir quién vigila el campo nuevo y **entonces** añadirlo.

Los tres sabotajes, con su rojo:

| sabotaje | rojo |
|---|---|
| `model_seconds=0.0` clavado | `assert 0.0 >= 0.05` |
| reloj abrazando `respond` entera | `assert 0.151 < (0.05 + 0.1)` |
| `queue_seconds=0.0` clavado | `assert 0.0 >= 0.2` |

🔑 **El segundo es el que justifica la cota de arriba del test**, y no es obvio:
un reloj demasiado ancho **también sube y baja con el juez**, así que pasaría
cualquier test que solo mirase la cota de abajo. Se caza haciendo
`record_practice` lento a propósito.

🔑 **Y el tercero explica por qué el test de la cola fabrica una cola de verdad:**
con el pool libre la espera es de milisegundos, así que un `0.0` clavado a mano
pasaría desapercibido. **El cero es un valor plausible aquí**, que es exactamente
lo que hizo invisible el sabotaje de `correct` (`[L-073]`).

**Suite: 452 → 456.**

---

#### ⚠️ Lo que esta decisión NO cierra

`tutor_started[0]` no puede reventar por el camino del éxito —si `result()`
devolvió, el cierre corrió—, y hay un test que lo fija. **Pero en el camino del
timeout con `attempt.cancel() == True` la lista está vacía**, porque la tarea
nunca arrancó. Ese camino **no escribe traza hoy**. Si algún día la escribe, un
`IndexError` ahí se lo comería el `except` de abajo y **perdería la fila entera
por un campo**. El aviso está escrito en `api.py`, encima de la línea, porque un
test en verde no puede avisar de un camino que todavía no existe.

- **Toca:** `app/english_tutor.py` (`TutorReply.model_seconds`, `respond`),
  `app/api.py` (el cierre de la cola, `trace.record`), `app/trace.py` (los tres
  campos y el porqué de las cuatro fases), `tests/test_english_tutor.py`,
  `tests/test_trace.py`, `tests/test_api.py`, `[D-085]` (enmendada), `[D-049]`,
  paso 9.
- **Relacionadas:** `[D-085]`, `[D-086]`, `[D-049]`, `[D-073]`, `[D-066]`,
  `[L-013]`, `[L-073]`, `LM.20`, auditoría externa del 2026-08-17.

### [D-086] 2026-08-17 — Los dos frenos de la traza, escritos antes de la primera línea

- **Se decidió**, antes de escribir una sola línea de la traza y no después del
  primer susto, cómo se prueba su ruta y qué pasa cuando escribir falla.

---

#### 🎯 (1) El test prueba el COMPORTAMIENTO, no la forma del código

- **Se eligió:** mover `TEAPP_DATA_DIR` y comprobar que la ruta de la traza **se
  movió con él**.

- **Contra:** lo que yo había prescrito, `callable(config.trace_file)`. 🔴 **Eso
  vigila la implementación que hoy creo que evita el fallo.** El fallo real es
  *"la ruta no siguió a `TEAPP_DATA_DIR`"*, y una constante de módulo es **solo
  una de las formas de causarlo**. Un test atado a la forma se pone verde el día
  que el fallo llegue por otra puerta.

- 🔑 **Es la doctrina del propio portero de `data/`, escrita por él mismo:**

  > *"El portero no pregunta quién escribe ni por qué. Pregunta si `data/`
  > cambió."*

  Y hay precedente en la suite: `check_no_data_writes.py:116`,
  `test_the_doorman_looks_at_the_real_folder_not_a_diverted_one`, que corre **con
  el desvío puesto** y por eso caza al vigilante que se cuelga de `config`.

- ✅ **VISTO MORDER el mismo día — y el primer sabotaje enseñó algo que esta
  entrada había predicho mal.**

  🔴 **Lo que escribí aquí primero:** *"congelar la ruta en una constante de
  módulo tiene que poner ese test en rojo"*. **Falso, y por una razón buena.**
  Con la constante puesta, `require_data_dir()` corre **al importar**, no
  encuentra `TEAPP_DATA_DIR` y revienta — así que no hay test rojo: hay
  `ImportError` cargando `conftest.py` y **la suite entera se niega a arrancar**.

  🔑 **Eso es `[D-037]` cobrando de más de lo que prometía: al no darle valor por
  defecto a la raíz, la forma "constante de módulo" no es un fallo que un test
  tenga que cazar — es un programa que no existe.** Protección estructural, más
  fuerte que un assert. Pero **no demuestra que el test funcione**, porque el test
  no llegó a correr.

  ✅ **El sabotaje que sí lo demuestra es la forma ALCANZABLE del mismo bicho: una
  caché.**

  ```python
    global _TRACE_CACHE
    if _TRACE_CACHE is None:                       # se calcula una vez
        _TRACE_CACHE = require_data_dir() / "trace.jsonl"
    return _TRACE_CACHE
  ```

  Arranca sin problema y **pone el test en rojo: `1 failed, 17 passed`**.
  Restaurado: **440 passed**.

  🎯 **Y el mensaje del fallo dijo más que el veredicto:** la ruta cacheada
  apuntaba a la carpeta temporal de **otro test** (`test_the_four_places_hang_from0`
  mientras corría `test_the_root_is_asked_again_on_every_call`). O sea que una ruta
  congelada no solo deja de seguir al desvío — **se filtra de un test al
  siguiente**. Ese es el daño con nombre, y salió gratis.

  📌 **La lección de procedimiento: un sabotaje que rompe la carga no es un
  sabotaje.** Parece más contundente —todo en rojo— y demuestra menos: hay que
  elegir el sabotaje que **deja correr al guardián**, o lo que se comprueba es el
  intérprete de Python. Misma familia que `[L-048]`.

---

#### 🚨 (2) Si escribir la traza falla: no tumba la práctica, y no se calla

La pregunta que faltaba en mi plan: **¿qué pasa si el `write` falla?** Disco
lleno, permisos, un `json.dumps` que revienta con un valor raro.

**Las dos respuestas obvias son malas, y las dos tienen precedente en este
proyecto:**

| salida | qué rompe | precedente |
|---|---|---|
| la traza **tumba** la petición | el instrumento rompe lo que mide: alguien pierde su práctica porque el registro no pudo escribir | `T-054`, la báscula estropeando los datos que medía (`[L-023]`) |
| la traza **falla en silencio** | el silencio se lee como confirmación | `LM.15` |

🔑 **`LM.15`, abierta antes de citarla** (`Edu_TripleS/LESSONS.md:3424`) — y **nació
en TEAPP, cerrando `T-054`**, el mismo incidente de la fila de arriba:

> *"Un dato falso deja huella y choca con algo. **El silencio no choca con
> nada.** Se parece demasiado a un 'todo bien' como para que alguien lo mire dos
> veces."*

El escenario concreto: la traza lleva tres semanas sin escribir y el tablero dice
**"pocas prácticas"** en vez de **"no estoy viendo nada"**. Y esas dos frases
llevan a decisiones opuestas.

✅ **La salida ya está montada en TEAPP y no cuesta nada:**

- **El fallo de la traza NO propaga.** La práctica se sirve igual — el estudiante
  no pierde nada por un problema del cuaderno.
- **Y se anota con el `logger.error` que ya existe**, que es el registro en prosa
  que lleva funcionando desde el paso 2.

🔑 **Así los dos registros se cubren mutuamente, y esa es la idea entera:**

```
    el estructurado (trace.jsonl)  cuenta el CASO FELIZ
    el de prosa     (logger)       cuenta cuando el estructurado se ROMPE
```

Cada uno ve el punto ciego del otro. La red de seguridad va **en quien llama**, no
dentro de la herramienta.

---

- 📌 **Formato y sitio, por `PI-2`:** un solo `trace.jsonl` abierto en modo
  añadir, dentro de `data/`, con la ruta resuelta por `trace_file()` igual que
  `users_dir()`, `quota_dir()` y `accounts_file()`. **Nada de rotación, ni un
  archivo por día, ni configurabilidad** — no hace falta para que esto funcione
  hoy.

---

#### 🔻 VIVO — un hueco de `PI-4`, aplazado con disparador y decisión del usuario

**Lo que NO se ha visto:** la traza escribiendo con **el servidor levantado y una
llamada real al modelo**. Se ha visto escribir con `TestClient` y el juez de
mentira —los seis sabotajes están en verde y rojo donde toca—, pero eso es la
suite, no la app corriendo.

⚠️ **Y `PI-4` dice exactamente esto:** *"lo que no se ha corrido no está
terminado, aunque el código exista"*. Así que **no se declara terminado**: se
declara aplazado, que es distinto.

🔻 **DISPARADOR: la primera llamada real del descenso de modelo.** Ese momento ya
va a gastar dinero por otra razón (`[D-049]`, Sonnet 5 y Haiku 4.5), así que la
comprobación viaja gratis encima de un gasto que ya estaba decidido. **Se mira que
`trace.jsonl` tenga su línea, con el `model` nuevo dentro** — que de paso es la
comprobación de que `MODEL_NAME` viaja hasta el cuaderno sin que nadie lo copie a
mano.

📌 **Por qué no se hizo hoy, decidido por el usuario:** cuesta ~`$0,003` de un
saldo que `[C-009]` acaba de declarar compartido con el estudio de agentes, y no
desbloquea nada del paso 9. **Un gasto que se puede montar encima de otro no se
paga dos veces.**

- **Toca:** `app/config.py` (`trace_file()`), `tests/test_config.py` (el test del
  desvío), `app/api.py` (la llamada y su `try`), `app/english_tutor.py`
  (`TutorReply.correct`), y el reparto entre los dos registros.

### [D-085] 2026-08-17 — El paso 9 arranca por observabilidad, y la traza guarda la forma y no la frase

- **Se decidió, y el orden lo puso el usuario:**

  ```
    observabilidad  →  evals con rúbrica  →  descenso de modelo  →  seguridad
  ```

  El descenso (`[D-049]`: Sonnet 5 y Haiku 4.5) va **en medio**, porque es
  justamente lo que los evals existen para medir.

- **Contra:** empezar por los evals, que fue lo que propuse. 🔴 **Y el defecto no
  era el argumento, era el procedimiento: descarté la observabilidad sin
  decírtelo.** Mi razón —*bajar de modelo sin evals es cambiar el motor sin
  velocímetro*— es cierta, pero solo obliga a tener evals **antes del descenso**,
  no antes de la observabilidad. Las dos órdenes la cumplen. Presenté como
  forzada una decisión que era libre, que es `PI-1` incumplida.

- ✅ **Por qué el orden del usuario es mejor, con evidencia del mismo día:** se
  movieron once centavos y hubo que pedir **cuatro tablas de consola** porque por
  dentro no había nada que mirar (`[L-072]`). Eso es la falta de observabilidad
  cobrada en tiempo, en vivo.

---

#### 🔍 El hueco, verificado en el disco y no supuesto

`app/api.py:838` termina la práctica exitosa así:

```python
    return PracticeResponse(...)      # y no escribe una sola línea
```

El log **sí** tiene `logger.error` y `logger.warning` para averías, y `logger.info`
para la cuota agotada y el timeout. O sea: **el cuaderno solo apunta lo que va
mal.** El suceso más frecuente de la aplicación —que funcione— es invisible.

🤝 **Y el hallazgo aguantó dos instrumentos sin fuente común:** esta terminal
leyendo `api.py` hasta el `return`; la auditora interrogando su propio registro
con ocho preguntas y viendo que ninguna se contesta en el caso feliz. Mismo tipo
de cruce que `[D-058]`, que validó el precio contra la consola (`$0,02`) y contra
tokens × lista (`$0,0234`) — dos fuentes que no se hablan.

---

#### 📊 El reparto: tres filas, y la tercera no la defiende ninguna herramienta

| | qué guarda | dónde | quién puede leerlo |
|---|---|---|---|
| **Traza operativa** | usuario, hora, nº de palabras, puntuación, prácticas, **`correct` (booleano)**, segundos, modelo | `data/` — cubierto por `.gitignore` | solo el servidor |
| **Material de evals** | la frase | aplazado, con la razón escrita | decisión posterior |
| 🚨 **`_persistence/`** | **ninguna frase de ninguna persona, nunca** | público | el mundo |

⏱️ **El reparto del tiempo lo aporta la auditoría, y es el campo que salva el
paso 9.** *"Cuánto tardó"* a secas no distingue *"el modelo es lento"* de *"la red
es lenta"*, y esas dos llevan a arreglos opuestos. Si `[D-049]` baja a Sonnet y a
Haiku, eso **solo acelera la parte del modelo**: si el modelo es un tercio del
reloj de pared, el descenso compra un tercio.

🔴 **ENMENDADO el 2026-08-17 — aquí había una frase FALSA, y se sustituye en el
sitio en vez de matizarse debajo.** Decía:

> ~~*"`app/tools.py` ya parte el presupuesto en `connect`/`write`/`pool`/`read`, y
> `[D-073]` calculó `read` por resta. La arquitectura ya piensa en fases; el
> registro no las escribe. El campo no inventa una idea nueva: le pone
> instrumento a una que ya está en el código."*~~

**Cada palabra de eso es cierta y el conjunto engaña.** Se lee como *"los números
existen y solo falta apuntarlos"*. **No existen.** Aquellas cuatro son **topes,
no medidas**: `anthropic.Timeout(connect=1.5, …)` es un presupuesto que se le
*entrega* a la librería —cuánto se les *permite* durar—, y `[D-073]` calculó
`read` **restando de ese presupuesto**, no cronometrando nada. Verificado en el
disco el 2026-08-17, en las **dos** librerías de este `.venv`:

```
httpx  0.28.1   _client.py:157   elapsed = time.perf_counter() - self._start
httpx2 2.9.1    _client.py:157   elapsed = time.perf_counter() - self._start
```

Un solo número cada una, y es el total de la respuesta entera. No hay salida por
fase en ninguna parte de la cadena.

🔑 **Lo que sí se puede medir es `[D-087]`, y contesta la misma pregunta con menos
trabajo:** cola / modelo / resto. **Y el porqué de la enmienda importa tanto como
el dato:** una frase con asterisco debajo se sigue leyendo como regla, y la
propuesta de las cuatro fases ya nació de leer esta frase. Se corrige donde está.

⚠️ Su `20,7 s / 59 s` viene de otro sistema, no de TEAPP. **El principio viaja, el
número no.**

🔴 **CORREGIDO al construirlo, el mismo día: esta entrada listaba "veredicto"
entre los campos, y ese campo NO puede guardarse.** `TutorReply.verdict` es *"lo
que dice el juez"* — **texto libre**, que puede citar la frase del estudiante
dentro (*"you wrote 'I has a cat'…"*). Guardarlo habría metido la frase por la
puerta de atrás, violando la fila 3 de esta misma tabla.

✅ **Lo que se guarda en su lugar es `correct`, un booleano** — y no es un invento:
es `[D-066]` llegando un piso más arriba. `GrammarVerdict` ya venía partido en
`correct` + `message` por esta razón exacta; `TutorReply` solo se llevaba el
`message`, así que **arriba la mitad legible por una máquina no existía**. Ahora sí.

⚠️ **Y se descartó la alternativa gratis, que era deducirlo de `score`:** con dos
líneas consecutivas se ve si el marcador subió. Pero la traza **puede perder
líneas a propósito** —su fallo no propaga, `[D-086]`—, y con una línea perdida el
marcador salta de dos y no hay a quién atribuirlo. **Una deducción que se rompe
justo por el comportamiento diseñado del sistema no es una deducción.**

📌 **Por qué la frase se aplaza, y no es una patada hacia adelante:**

1. **No hay frases que recolectar.** La pregunta 1 de la traza es *"¿está usando
   esto alguien?"*, y no lo sabemos. Recolectar de usuarios cuya existencia no
   está comprobada rinde cero.
2. **`measure_tutor.py:292` ya trae 60 frases A1 escritas a mano** — *"unas
   correctas y otras con un error claro, para que de paso se vea si la rúbrica de
   `[D-049]` juzga como se le pidió"*. Eso no es un plan B: es un conjunto de
   casos **elegidos a propósito**, que es lo que un eval necesita y lo que una
   cosecha aleatoria no da.
3. **Un conjunto de prueba es una cosecha, no una llave abierta.** Unas decenas
   de frases, una vez — no todas las frases de todos para siempre.

---

#### 🔴 Mis dos errores, los dos corregidos por la auditoría

**(1) Cité `[D-060]` contra inventar frases, y está mal aplicada.** `[D-060]` es
el `MAX_CALLS = 10` que salía de un `len()`: un número que **aparentaba estar
medido** sin serlo. Un conjunto de prueba diseñado a mano no aparenta nada — dice
lo que es. No es el mismo bicho.

**(2) Prescribí un "acuérdate" sobre una estructura que ya lo resuelve.** Escribí
que la traza es *"un cuarto camino hacia `data/` que todo desvío tiene que
acordarse de mover"*. **Eso describe el mundo anterior a `[D-037]`**, y el propio
`no_data_writes.py:67` lo dice ocho líneas debajo del punto ciego que yo cité
bien. Comprobado:

```
  tests/conftest.py:81      monkeypatch.setenv(config.DATA_DIR_NAME, str(tmp_path))
  app/config.py:157,162,167 users_dir()  quota_dir()  accounts_file()
                            → las tres cuelgan de require_data_dir()
```

**Una línea, una variable.** No hay tres sitios que desviar y no habrá cuatro.

🔑 **Y el fondo importa más que el ahorro de una línea:** `[L-023]` no pasó por
falta de una nota — pasó porque el remedio **era acordarse** (desviar tres
constantes a mano) y alguien se acordó de una y olvidó dos. `[D-037]` cambió eso
de *acordarse* a *estructura*. Poner un recordatorio encima es reintroducir el
mecanismo que se pagó por quitar.

✅ **La condición que sí hay que escribir, y esta es comprobable con un test:**

> **La traza resuelve su ruta LLAMANDO a una función (`require_data_dir()`),
> nunca guardándola en una constante de módulo.**

Una constante se fija al importar, **antes** de que `monkeypatch` corra, y ahí sí
se escapa. Lo dice `conftest.py:78-80`: *"esto solo funciona porque los tres
módulos resuelven la ruta DENTRO de cada función"*. Por eso `users_dir()` es
función y no constante.

🚨 **Lo que sigue en pie: el portero de `T-071` NO cubre este flanco.**
`no_data_writes.py` vigila que **la suite** no ensucie `data/` (`[L-020]`) — nada
que ver con privacidad. Y documenta su propio punto ciego: *"lo que corre fuera de
pytest… uvicorn levantado a mano… escriben en `data/` de verdad y el portero ni se
entera"*. **Ese es el modo normal de operación de la traza.** Quien da la
privacidad es `.gitignore`.

---

#### 🔒 La tercera fila asciende a `PI-8`, porque `decisions.md` no alcanza

**El límite:** ninguna frase escrita por una persona que use la app entra en
`_persistence/`, nunca, ni como ejemplo de *"mira qué error tan típico"*. Si hace
falta ilustrar, se inventa una frase y se dice que es inventada.

**Por qué es la única de las tres sin herramienta:** `data/` está en `.gitignore`.
**`_persistence/` no** — va a Git a propósito, y `[C-007]` verificó que el
repositorio es **público**. Así que un dato personal no se escapa por el archivo
grande que alguien vigila: se escapa por **el ejemplo pequeño que nadie revisó**.
Clase muda, la misma por la que la fecha del 15 viajó a seis archivos
(`[L-069]`).

**Por qué no basta escribirla aquí: `LM.20`** — abierta y leída en
`Edu_TripleS/LESSONS.md:3673` antes de citarla, como manda `CLAUDE.md`. Su núcleo:

> *"Una copia falsa te engaña. **Una copia correcta que nadie alcanza** te deja
> cometer el mismo error dos veces, y encima con la respuesta ya escrita dentro."*

`decisions.md` se lee **cuando alguien va a buscarlo**. `CLAUDE.md` se lee
**siempre, sin buscarlo**. Escribir la fila 3 solo aquí sería escribirla cierta y
fuera de alcance.

**Dónde quedó, en los tres sitios:**

| sitio | qué lleva |
|---|---|
| `CLAUDE.md` | **`PI-8`**, corto, junto a `PI-6`/`PI-7` |
| `protocol-close` | casilla obligatoria en el Paso 5 + línea en el reporte del Paso 7 |
| esta entrada | el porqué completo |

📌 **Y queda escrito que `PI-8` es más DÉBIL que `PI-6` y `PI-7`.** A esas dos las
respalda un diff que se mira aparte. A esta la respalda una casilla, **y una
casilla pregunta, no detecta.** Fingir que muerde sería marcarla con una
intención — exactamente lo que `PI-6` prohíbe en su terreno.

- **Toca:** el paso 9 entero, `CLAUDE.md` (`PI-8`), `protocol-close` (Pasos 5 y
  7), y —cuando se construya— la ruta de la traza en `app/config.py` y su test de
  que es función y no constante.

### [D-084] 2026-08-17 — El saldo se lee ANTES de la primera llamada del paso 9: `$6,24`, y la resta deja un hueco de `$0,11` fuera de `teapp-measure`

- **Se decidió:** descargar el disparador de `[D-081]` —*"se lee antes del
  próximo bucle de llamadas, sea cual sea"*— **antes de abrir el paso 9**, y no
  después de cruzarlo.

- **Contra:** abrir el paso 9 escribiendo rúbrica y observabilidad (que no gastan
  nada) y leer el saldo justo antes de la primera llamada. Es **defendible al
  pie de la letra** —el disparador es la primera llamada, no el cruce de paso— y
  se descartó por dos razones: la lectura cuesta `$0,00` y dos minutos, y
  `[D-041]` ya falló exactamente así en la sesión 54, no por un mal argumento
  sino porque la sesión se acabó antes de llegar al clic.

- 🕒 **LA HORA, FIJADA ANTES DEL NÚMERO: 2026-08-17, 16:05 UTC.** Una sola vez
  para las dos lecturas del día, que ocurrieron en el mismo cuarto de hora.
  Disciplina de `[D-079]`: después de ver el número, arreglar el criterio y
  moverlo son indistinguibles para quien lo lea luego.

- ✅ **EL TECHO PREDICHO AGUANTÓ, y se escribió antes del clic.** Con la primera
  lectura en la mano se publicó `$6,35` **marcado como techo, no como saldo**,
  porque el espacio `Default` no aparecía en esa vista. La lectura dio `$6,24`:
  por debajo. La predicción no discrimina gran cosa —era una desigualdad, no una
  banda— pero **estaba fuera antes del dato**.

- 🧮 **LA RESTA, con los redondeos dentro.** La consola redondea al céntimo, así
  que ningún número de aquí es un punto:

  ```
    saldo 2026-08-11 ..... $6,55  →  [6,545 , 6,555]
    saldo 2026-08-17 ..... $6,24  →  [6,235 , 6,245]
    gasto desde el 11 ................. $0,30 – $0,32

    teapp-measure, del 1 al 17 (leído hoy, día por día):
      ago 13 ............. $0,02  →  [0,015 , 0,025]
      ago 14 ............. $0,18  →  [0,175 , 0,185]   (T-093 entera)
      todos los demás .... $0,00
    subtotal .......................... $0,19 – $0,21

    🚨 HUECO SIN EXPLICAR .............. $0,09 – $0,13
       ≈ 29 – 45 llamadas al perfil medido de [D-079]
  ```

- 🚨 **El hueco vive donde no hay freno.** `teapp-measure` tiene tope de `$2,00`
  al mes (`[D-062]`); el espacio `Default` **no admite tope ninguno** —
  `[D-059]` lo trae citado de Anthropic: *"You cannot set limits on the Default
  Workspace"*. Así que el gasto que no sabemos identificar está precisamente en
  el único sitio sin capa. **Es `[C-008]` dejando de ser teórica por segunda
  vez**, después de `[D-058]`.

- 🔍 **Candidato principal, y explica una quinta parte: `T-079`.** Sus 10
  llamadas costaron `$0,02` según la consola (`[D-058]`) y corrieron el
  **2026-08-11**, el día **antes** de que `teapp-measure` existiera — `[D-061]`
  crea el espacio el 12. Luego cayeron en `Default`. Si corrieron **después** de
  la lectura de saldo de `T-080` ese mismo día, están dentro del hueco; si
  antes, ya estaban descontadas del `$6,55`. **Comprobable y gratis.**
  ⚠️ **Explican `$0,02` de `$0,11`. No lo cierran.**

- 📌 **Lo que esta entrada NO afirma:** no dice qué gastó el resto, y no lo
  supone. `$0,11` no es alarmante **en dinero** — es el 1,7% del saldo. Lo es
  **en forma**: es la misma figura que `T-096` y unas **cinco veces más
  grande**, en el espacio sin tope.

---

#### 🔴 Y corrige una premisa de `[D-079]`: el día 13 no fue de sondas

`[D-079]` fijó el procedimiento de lectura y mandó descontar *"las sondas de
`check_api_key.py` con la llave del laboratorio (13 de agosto) y la llamada
mínima de `[D-061]` del 12"*, calificándolas de **"los dos por debajo del
céntimo pero se nombran"**.

La consola dice **`$0,02` el 13 de agosto**. Y la aritmética de `T-096` dice de
qué tamaño eran:

```
  1.834 tokens de entrada ÷ 361 por llamada  ≈  5,1 llamadas
    338 tokens de salida  ÷ 5 llamadas       ≈  68 de salida cada una
    (perfil de llamada de decisions.md:707 — 361 + 5×49)
```

**No son sondas. Son ~5 llamadas completas del tutor**, del tamaño de las de
`T-093`.

🎯 **Con eso `T-096` cambia de estado:** deja de ser *"5 llamadas sin dueño en
algún día de la semana 10–16"* y pasa a estar **fechada en el 13**. La tarea no
se cierra —sigue sin saberse **qué** llamó— pero el espacio de búsqueda pasa de
siete días a uno.

🔮 **Hipótesis, marcada como tal porque no se ha comprobado:** el 13 es el día de
`T-087`, la saturación de Anthropic. `[D-075]` documenta que los dos `except`
del bucle de `measure_tutor.py` hacen `break` — una tanda que se corta a mitad
hace unas pocas llamadas completas y se va sin dejar veredicto. Cinco llamadas y
un corte encaja. **Se comprueba** cruzando la vista de USO del 13 contra si se
corrió la báscula ese día; no se da por cierto.

---

#### ✅ RESUELTO el mismo día — y no había ningún bicho

El usuario confirmó, al preguntarle por qué se estaba validando todo esto, que
**la cuenta paga también su estudio de programación con agentes de IA.** Ese es
el tercer inquilino del saldo, y es invisible en la vista de COSTO porque esa
vista enseña *"solo uso de API"*. **Es la trampa que `[D-079]` pre-registró tres
días antes, palabra por palabra.**

- El hueco de `$0,02–0,095` **no es tráfico de producción sin dueño.**
- **`T-096` se cierra sin bicho:** el excedente del 13 y los `$0,10` del **ago
  01** —anteriores a `[D-001]`, el primer día del proyecto— son del mismo
  inquilino. No hubo corrida fantasma.
- El límite que sí queda, y que sí cambia cómo se lee un freno ya escrito, vive
  en **`[C-009]`**: el saldo no mide TEAPP.
- El paso 9 **no queda bloqueado.**

🔴 **Y el proceso salió mal aunque el hallazgo saliera bien.** Se pidieron **tres
tablas de consola** antes de preguntar lo único que lo resolvía: *¿qué más corre
con esta cuenta?*. El dueño de la cuenta lo sabía de memoria. Lección en
`[L-072]`.

- **Toca:** `[C-009]` (nueva, y es lo que sobrevive de aquí), `T-096` (cerrada
  sin bicho), `[D-057]` y `[D-058]` (su lectura del saldo como medidor de TEAPP
  queda matizada por `[C-009]`), y el procedimiento de lectura de `[D-079]`.

### [D-083] 2026-08-17 — `PI-6` y `PI-7` entran en `CLAUDE.md`, desde el verbatim y no desde la paráfrasis

- **La pregunta.** Una auditoría externa señaló que dos reglas duras de tests
  redactadas en el repo supervisor (`GUIDE.md` §11.i) **nunca llegaron a TEAPP**.
  Comprobado: `grep` de `GUIDE.md` y de `11.i` en todo el repo, cero
  coincidencias. La pregunta era si escribirlas desde la paráfrasis que traía la
  auditoría o pedir el original.

- **Se pidió el original, y menos mal.** La paráfrasis había perdido tres cosas,
  y **una era de carga**:

  | lo que faltaba | por qué importa |
  |---|---|
  | 🔴 **"del humano"** | *"autorización explícita"* a secas la cumple la sesión que construye, o la terminal auditora. **El punto entero es que la firma la pone quien lleva el proyecto.** Sin el actor, la regla se autoriza sola |
  | 🟠 **La voz de la regla 2** | venía en pasiva (*"el refactor se pide explícitamente"*), y en pasiva se lee como que lo pide el humano. El original es **imperativo dirigido al agente**: *"Pide el refactor"* |
  | 🟡 **Los porqués** | `LM.43`, `LM.44`, y la frase *"la salida barata siempre gana"* — que es exactamente el riesgo del rojo que `[D-082]` acaba de armar |

  🔑 **Es `[L-069]` otra vez, en vivo:** un dato copiado de segunda mano al que se
  le cae por el camino el trozo que hacía el trabajo. La diferencia es que esta
  vez se cazó **antes** de escribirlo, porque se fue a la fuente.

- 🔍 **Y §11.i no terminaba en las dos reglas.** Traía además las dos
  comprobaciones que las hacen exigibles, que tampoco estaban en la paráfrasis y
  **sin las cuales `PI-6` es una nota**:

  - **El diff de los tests se mira aparte del diff del código.** Un test
    ablandado no se anuncia; solo se ve ahí. Sin esto nadie llega a saber si se
    tocó.
  - **Que el rojo existiera.** Un test que nunca falló no probó nada, y mirando
    el verde no se distingue de uno vacío. Ya es la práctica de la casa
    (`[D-060]`, `[L-048]`, y hoy `[D-082]`), pero no estaba escrito como
    requisito.

  Las dos entran como bloque de comprobación debajo de `PI-6`/`PI-7`.

- **Dónde se colocaron y por qué ahí.** Al final de *"Cómo se escribe el
  código"*, después de `PI-5`, para no romper el orden numérico. `PI-4`
  —*terminado = visto funcionando*— es la vecina temática y queda citada:
  `PI-4` dice que lo que no se ha corrido no está terminado; `PI-6` añade que
  **un test al que se le baja el listón deja de correr aunque siga
  ejecutándose**.

- ⚠️ **Se dejó escrito que `PI-7` no choca con `PI-3`**, porque leídas seguidas
  parecen contrarias. `PI-3` prohíbe refactorizar **por mi cuenta**; `PI-7` me
  obliga a **preguntar** si toca. La respuesta puede ser que no, y entonces
  `PI-3` manda.

- 📌 **Las citas se escribieron con el repo nombrado.** `LM.43` y `LM.44` viven
  en `Edu_TripleS`, no aquí, y los números **se solapan** con los `L-nnn` de este
  repo. Meterlas sin decir de dónde son es `[L-034]` otra vez — nueve citas
  equivocadas, una misma significando tres cosas.

- 🚩 **Discrepancia detectada y no resuelta al escribir esto** (`T-101`). La tabla
  de citas de `CLAUDE.md` decía que las lecciones de método viven en
  `Edu_TripleS/PROGRESO.md`; la auditoría decía `LESSONS.md`. No se podía
  verificar desde aquí —bajo `Test_Edu_TripleS` solo está `TEAPP`— así que
  **`PI-6`/`PI-7` se escribieron citando el repo y no el archivo**, ciertas bajo
  las dos versiones, y la tabla se dejó intacta.

  ✅ **RESUELTA el mismo día por `T-101`: es `LESSONS.md`, y la tabla estaba
  mal.** Conteo del repo supervisor: **48** encabezados `### LM.n` en
  `LESSONS.md` (LM.1–LM.48, sin huecos), **0** en `PROGRESO.md`. Fila corregida,
  y ampliada para decir **dónde no están** — `PROGRESO.md` los menciona ~200
  veces sin definir ninguno, así que la dirección mala se auto-confirma al
  visitarla. 🔑 **La cautela de citar el repo y no el archivo fue lo único que
  impidió que las dos reglas duras nacieran con una cita rota.** Ver `[L-070]`:
  el puntero no había caducado, **nació falso dentro del arreglo de otra
  auditoría**.

- **Fecha:** 2026-08-17. **Origen:** auditoría externa del 2026-08-17, hallazgo
  H-3, con el verbatim de `GUIDE.md` §11.i líneas 1787-1794 pedido y recibido.
- **Relacionadas:** `[D-082]`, `[L-068]`, `[L-069]`, `[L-034]`, `[L-048]`,
  `[D-060]`, `PI-3`, `PI-4`, `T-100`, `T-101`.

---

### [D-082] 2026-08-17 — El disparador del paso 9 pasa de comentario a test, clavando el par

- **La pregunta.** `[D-081]` cerró el paso 8 dejando armado un disparador: antes
  de cambiar `MODEL`, leer en la consola el límite por minuto de ese modelo y
  ponerlo en `LAB_REQUESTS_PER_MINUTE` **en el mismo cambio**. La pregunta que
  nadie hizo el 14 es **quién lo hace cumplir**. Respuesta que había: un
  comentario en `deploy/check_api_key.py:90-97`. Es decir, nadie.

- **El agujero, medido y no razonado.** `tests/test_check_api_key.py` tenía un
  guardián del acoplamiento de `[L-047]`, pero clavaba **una sola mitad**:
  `assert check_api_key.LAB_REQUESTS_PER_MINUTE == 50`. Ningún test del repo
  nombraba `check_api_key.MODEL` — las tres apariciones de `MODEL` en `tests/`
  son `MODEL_NAME`, de `app/tools.py`, otra constante y otro archivo. Así que
  el escenario **exacto** que `[D-081]` describe —cambiar `MODEL`, no tocar el
  50— dejaba la suite entera en verde.

- 🚨 **Y el propio archivo ya decía por qué eso es grave**, a treinta líneas del
  test que no lo cubría: *"la firma es el par (espacio, modelo)"*
  (`check_api_key.py:58-60`). El código sabía que era un par; el test clavaba la
  mitad.

- **Qué se decidió.** El test clava el par:

  ```python
  assert (check_api_key.MODEL, check_api_key.LAB_REQUESTS_PER_MINUTE) == (
      "claude-opus-5",
      50,
  )
  ```

  Cambiar `MODEL` pone la suite roja, y devolverla a verde obliga a tocar el
  número del laboratorio **en el mismo cambio**. El disparador deja de depender
  de que alguien lea un comentario.

- 🔻 **Visto morder (`[PI-4]`), que es la mitad que importa.** Con
  `MODEL = "claude-sonnet-5"` y el 50 intacto: `1 failed, 439 passed`, y el
  único rojo es el test nuevo. Restaurado: **440 passed**. `check_api_key.py`
  volvió idéntico — el `git diff` de esa corrida fue solo el archivo de tests.

- **Contra qué se eligió.**
  - *Dejarlo como comentario.* Descartado: es `[L-065]` por tercera vez. Un
    aviso presente se lee como cobertura, y este ya estaba escrito el 14
    confiando exactamente en eso. Sesión 57 lo dice más corto: **un control
    escrito para un humano no protege a un programa.**
  - *Que el test pregunte a la consola de Anthropic.* Descartado por dos
    motivos independientes: gasta una llamada de verdad en cada corrida de la
    suite (regla 5, minimizar factura), y ata los 440 a que la red y Anthropic
    respondan — el `529` de `[L-046]` volvería como rojo falso.

- 📌 **Lo que esta decisión NO dice, y conviene que quede escrito.** El test
  **no** verifica que 50 sea el límite real de `claude-opus-5` hoy. No lee la
  consola y no puede. Verifica que nadie mueva **media firma sola**. La otra
  mitad —que el número sea el de verdad— sigue siendo un clic humano, y el
  disparador de `[D-081]` sigue vivo tal cual. Lo que cambia es que ahora hay un
  rojo que lo exige en vez de un párrafo que lo pide.

- ⚠️ **Un rojo sin instrucción se arregla por el lado cómodo.** El día que la
  suite se ponga roja por un `MODEL` nuevo, la salida barata es editar el
  assert — y eso devuelve el portero mudo con la sensación de haber arreglado
  algo. Por eso el comentario de `MODEL` ahora **nombra el test** y dice que el
  arreglo es ir a la consola, no tocar el assert. 🔑 Esto es lo mismo que pide
  la regla de tests que la sesión supervisora dejó redactada y que **todavía no
  está en este repo** — ver `T-100`. 🟢 **Dejó de ser cierto el mismo día:**
  entró como **`PI-6`** con `[D-083]`, desde el verbatim de `GUIDE.md` §11.i.

- **Fecha:** 2026-08-17. **Origen:** auditoría externa del 2026-08-17, hallazgo
  H-1, verificado contra el disco antes de aplicarlo.
- **Relacionadas:** `[D-081]`, `[D-049]`, `[D-061]`, `[D-063]`, `[L-047]`,
  `[L-050]`, `[L-065]`, `T-088`, `T-099`, `T-100`.

---

### [D-081] 2026-08-14 — El paso 8 CIERRA, con las cuatro miradas hechas y una sola pendiente

- **La pregunta la dejó abierta `[D-080]`:** el paso 8 no cerraba hasta mirar las
  cuatro pendientes **una por una**, porque la clasificación de esas cuatro no
  era de fiar. Las cuatro están miradas. **El paso 8 queda cerrado.**

- **Qué salió de cada una:**

  | tarea | venía clasificada como | qué resultó ser | estado |
  |---|---|---|---|
  | `T-089` | *"cosmética: el mensaje de error recomienda la forma insegura"* | **clase de seguridad**, medida en 12 s en la EC2 | ✅ cerrada midiendo |
  | `T-079` | *"decidir qué hacer con el timeout"* | medición real y buena, **con el símbolo equivocado** | 🟡 condición viva, con disparador |
  | `T-081` | *"renombrar un campo"* | decisión de facturación, **con su daño ya escrito en la ficha** | 🔲 aplazada con motivo (PI-3) |
  | `T-088` | *"corregir un comentario"* | **denegar por defecto convertido en aceptar por accidente** | ✅ desarmada |

- 🚨 **Queda UNA pendiente, no dos.** `T-081` está **aplazada**: nada la
  dispara, y su ficha ya escribe el daño, así que no engaña a quien la lea.
  `T-088` **no quedó pendiente — quedó DESARMADA**. La diferencia es la regla de
  `[L-064]` y no es contabilidad: una tarea sin disparador espera; una con
  disparador en el calendario no es una pendiente, es un bloqueante disfrazado.

- 🔑 **Lo que `[D-080]` decidió con UN dato, ahora tiene DOS DE DOS — y de la
  misma forma exacta.** Aquella entrada fue honrada al escribir su propio
  límite: *"el argumento no es que queden cuatro tareas; es que la clasificación
  de esas cuatro no era de fiar, y ya hay una prueba"*. Con `T-088` hay dos, y
  lo que las une no es la gravedad, es **el defecto**:

  | archivo | avisaba de | negaba, a pocas líneas |
  |---|---|---|
  | `deploy/install.sh` | *"NUNCA la llave como argumento"* | un ejemplo con la llave delante de `sudo` |
  | `deploy/check_api_key.py` | *"si cambian el límite en la consola, cámbialo aquí"* | *"da igual cuál sea el modelo"* |

  🔑 **Dos archivos distintos, un solo defecto: un aviso correcto sobre una
  puerta, a pocas líneas de una línea que niega la otra.** Eso convierte a
  `[D-080]` de decisión defendible en **regla con dos pruebas**, y la regla que
  sale gobierna el paso 9 — está escrita entera en **`[L-065]`**, no aquí, para
  que no viva en dos sitios.

- 🔻 **DISPARADOR DEL PASO 9, y es lo primero que hay que leer al abrirlo.**

  > 🚨 **Antes de cambiar `MODEL` — cada vez — leer en la consola el límite por
  > minuto de ese modelo en `teapp-measure` y ponerlo en
  > `LAB_REQUESTS_PER_MINUTE` EN EL MISMO CAMBIO.**

  🔴 **Corregido el 2026-08-14, sobre una frase de esta misma entrada.** Decía
  *"la primera acción del paso 9 NO es cambiar `MODEL`"*, dando por hecho que el
  paso 9 **es** bajar a Haiku. **No lo es, y no se había abierto el roadmap.**
  Lo que dicen los archivos:

  | archivo | qué dice |
  |---|---|
  | `_context/roadmap.md:23` | paso 9 = **"Observabilidad y evals con rúbrica"** |
  | `[D-049]` | *"el descenso a **Sonnet 5 y a Haiku 4.5** se convierte en trabajo medido del paso 9"* |

  🔑 **Y la corrección hace el disparador MÁS fuerte, no más flojo.** Son **dos
  modelos, no uno**: el disparador no salta una vez al abrir el paso — salta
  **cada vez que se toca `MODEL`**, al menos dos. Atarlo a *"lo primero del paso
  9"* lo habría dejado gastado después del primer cambio, justo antes del
  segundo. **El disparador es la acción, no la fecha.**

  El aviso ya vive en el código, junto a `MODEL` en `deploy/check_api_key.py`.
  Se repite aquí porque **el paso 9 se abre leyendo el roadmap, no el guion del
  portero**: si el disparador solo vive donde ya has llegado, llega tarde. Sin
  eso, el portero acepta la llave del laboratorio y **no da ningún error**.

- 📌 **Vivo, sin bloquear el cierre:**
  - **Saldo prepagado de `[D-057]`** — 6,55 US$ es del 2026-08-11 y desde
    entonces corrieron `T-093` y `T-095`. **Se lee antes del próximo bucle de
    llamadas, sea cual sea**, con la hora UTC anotada ANTES del número
    (`[D-079]`).
  - **`T-086`** — lectura de AWS con su hora UTC, también antes del número.
  - **`T-098`** (nueva) — el guion de arranque lee la prosa en vez del campo de
    estado y no se salta lo tachado. **Armada: su disparador es el próximo
    arranque.**

- **Fecha:** 2026-08-14. **Origen:** auditoría externa del 2026-08-14, cuarta
  ronda, sobre el mandato que dejó abierto `[D-080]`.

### [D-080] 2026-08-14 — El paso 8 no se cierra hoy, y `T-079` espera al próximo día

- **La pregunta era `T-090`:** ¿el paso 8 queda cerrado, o falta algo antes de
  cruzar al paso 9?

- **Alternativas.** (a) Declararlo cerrado y tratar las cuatro pendientes
  (`T-079`, `T-081`, `T-088`, `T-089`) como remates que se arrastran al paso 9.
  (b) No cerrarlo hasta mirarlas de una en una.

- **Se eligió (b), y no por criterio sino por lo que pasó al mirar la primera.**
  `T-089` estaba escrita como cosmética: *"el mensaje de error de `install.sh`
  sigue recomendando la forma insegura"*. Medirla costó doce segundos en una
  máquina ya encendida y la subió a **clase de seguridad, con corrida detrás**
  — `sudo VAR=valor` expone el valor en `ps aux` a cualquier usuario de la
  máquina, medido, ver `[L-061]`.

  🔑 **Una de las cuatro cambió de categoría en cuanto se tocó.** Con eso, la
  opción (a) no era "cerrar el paso": era "cerrarlo sin haber mirado", que es
  otra cosa y no se puede afirmar. El argumento no es que queden cuatro tareas;
  es que la clasificación de esas cuatro **no era de fiar**, y ya hay una prueba.

- **Lo que se cerró hoy con eso:** `T-089` (la llave deja de estar expuesta) y
  `T-097` (la forma peligrosa sale de circulación en los tres sitios que la
  traían sin secreto dentro). Quedan `T-088`, que sí es cosmética de verdad y
  además depende de bajar a Haiku en el paso 9, y `T-079`.

- **⏳ Por qué `T-079` no se abrió hoy, siendo la que manda.** Una auditoría
  externa pide **quitarle el ✅**, por estar cerrada por inferencia. Atender eso
  obliga a abrir `[D-077]`, releer su cierre condicionado y sostener una
  discusión con evidencia propia — no es un cambio de estado, es una revisión.

  Era la **cuarta sesión del día**. 🔑 `[D-041]` falló en la sesión 54
  exactamente por esta forma: no por un mal argumento, sino porque la sesión se
  acabó antes de llegar al clic. **Una decisión que pide evidencia, empezada con
  el día gastado, es cómo se toman las decisiones cansado.**

- **📌 El límite de ese razonamiento, para que no se use de excusa.** "Estoy
  cansado" no vale para todo lo pendiente. Antes de cerrar sí se midió
  `sudo -E` contra el `Defaults env_reset` de Ubuntu, porque esa instrucción
  **ya estaba escrita en el repo sin verificar**, y dejarla dormir es dejarla
  para que alguien la siga mañana. La distinción es: **lo que aún no existe
  puede esperar; lo que ya está escrito y sin comprobar, no.**

### [D-079] 2026-08-14 — El criterio de `T-095` queda sellado ANTES de abrir la consola: banda, sitio, cuatro ramas y la hora

- **Se decidió:** fijar por escrito, **antes de que nadie mire la consola de
  Anthropic**, contra qué se compara la lectura y qué significa cada resultado
  posible. 🔑 **Después de ver el número, arreglar el criterio y moverlo son
  indistinguibles para quien lo lea luego.** Es `[D-074]` aplicado a una lectura
  en vez de a un gasto.

- 🎯 **LA BANDA: `$0,156 – $0,205`.** No es un ±10% a ojo: es el rango que sale
  bajo **cualquier** reparto entrada/salida posible, porque el eslabón débil de
  `[D-078]` era justamente ese reparto. Así que no se usa — se barre entero:

  ```
    coste(nuevo) = $0,00234 × [ f×(361/247) + (1−f)×(49/44) ]
      f = fracción del coste de [D-058] que era de ENTRADA

      factor entrada  361/247 = 1,4615
      factor salida    49/44  = 1,1136

      f = 0,00  (todo salida, extremo)  → 60 llamadas = $0,156
      f = 0,53  ([D-058] tal cual)      → 60 llamadas = $0,182
      f = 1,00  (todo entrada, extremo) → 60 llamadas = $0,205
  ```

  Dice: **si los precios unitarios no cambiaron y el `$0,00234` era correcto, el
  resultado cae ahí dentro pase lo que pase con el reparto.**

  ✅ **Y de regalo, una comprobación de robustez de `[D-078]`:** el `$0,1404`
  viejo queda **fuera** de la banda. Aunque el 53/47 estuviera del todo
  equivocado, el número viejo no podía cuadrar. **H-1 no dependía del reparto.**

- 📍 **DÓNDE SE LEE: el espacio de trabajo `teapp-measure`, NO el total de la
  organización.** `measure_tutor.py` corre con el `.env` local, que lleva la
  llave del laboratorio (`[D-061]`), así que el gasto de `T-093` cayó ahí y no
  en `Default`. 🚨 **Leer el total de la organización mete dentro el tráfico de
  producción (`teapp-server`) y la comparación deja de significar nada.**

  ✅ **Hay línea base, y es buena:** `[D-062]` verificó **en pantalla** el
  2026-08-12 *"Límite Mensual: USD 0,00 de USD 2,00"* para ese espacio. Estaba
  en **cero** hace dos días, así que esto es un experimento limpio y no una
  resta contra ruido de fondo. **A descontar, los dos por debajo del céntimo
  pero se nombran:** las sondas de `check_api_key.py` con la llave del
  laboratorio (13 de agosto) y la llamada mínima de `[D-061]` del 12 (10 tokens
  de entrada, 4 de salida).

- 🚦 **LAS CUATRO RAMAS. Se pre-compromete la LISTA, no la conclusión** — ese
  fue exactamente el error de `[D-077]`, y la reparación no es dejar de escribir
  nada de antemano, es escribir **todas** las salidas:

  - 🟢 **A — dentro de `$0,156–$0,205`.** La derivación se confirma.
    `COST_PER_CALL_USD` pasa de **derivado a medido** y se le retira la etiqueta
    de tres partes de `[D-078]`. `[D-058]` queda confirmada **en su mecánica**:
    los precios unitarios no cambiaron.
  - 🔵 **B — por debajo de `$0,156`.** Primer sospechoso: **caché de prompt** (la
    rúbrica es idéntica en las 60 y pesa casi toda la entrada). Segundo: que el
    `$0,00234` de `[D-058]` viniera alto de origen — ver el punto de la
    resolución, abajo.
  - 🟠 **C — por encima de `$0,205`.** Hay **gasto ajeno** en ese espacio. Se
    mira qué más corrió con la llave del laboratorio **antes de tocar ningún
    precio**. 🔑 No se ajusta una constante para explicar un número: primero se
    descarta la contaminación.
  - ⚪ **D — la consola dice "sin datos".** 🚨 **ESO NO ES UN CERO.** Se anota
    *"consultado el `<fecha>` a las `<hora>` UTC, todavía sin datos"* — ni
    *"cuadró"* ni *"no cuadró"*. `T-095` **queda abierta**. Es el hueco por el
    que ya se cayó este proyecto con el `0,00 USD` de AWS (`[A-018]`).

- 🔴 **CORRECCIÓN AL ENCARGO, comprobada aquí: en la rama B el dato NO está
  guardado.** La auditoría supuso que `RecordingClient` conservaba la evidencia
  —`self.usages.append(answer.usage)` guarda el objeto entero y `main()` solo
  imprime `input_tokens` y `output_tokens`—, pero **`measure_tutor.py` no
  escribe nada en disco** (ni un `json.dump`, ni un `open`, ni un `Path`,
  comprobado). `client.usages` vivió en memoria y **murió con el proceso el 14
  de agosto**. Lo impreso tampoco sirve: imprime los mismos dos campos.

  ✅ **Pero el sustituto es mejor y también gratis: la caché se descarta desde el
  código, sin leer nada.** El *prompt caching* de Anthropic **es opt-in** — hay
  que marcar `cache_control` en el bloque que se quiere cachear — y **no aparece
  en ninguna parte del repo** (`grep` sobre todos los `.py`: cero
  coincidencias). La llamada de `app/tools.py` pasa `system=GRAMMAR_RUBRIC` como
  texto plano. **Sin marca no hay caché**, así que la rama B **no debería poder
  explicarse por ahí**. 🔑 Y eso invierte la utilidad de la rama: si la consola
  **sí** muestra una línea de caché, esa es la sorpresa que hay que perseguir,
  no la explicación cómoda.

- 📏 **Y se sella un matiz sobre `[D-058]` que su redacción escondía.** Se validó
  cruzando *"la consola dijo $0,02"* contra *"el cálculo dio $0,0234"*, aceptando
  que coincidían dentro del redondeo. **A resolución de céntimo, `$0,02` es
  cualquier cosa entre `$0,015` y `$0,025`: ±25%.** El cruce fue legítimo, pero
  mucho más flojo de lo que suena.

  ✅ **Aquí `[D-077]` tenía razón en algo, y conviene dejarlo escrito bien:**
  sobre ~$0,18 la misma resolución de céntimo es **±2,7%**. Esta lectura **sí
  mide unas nueve veces mejor**. Lo que no podía decirse era *"6× más muestras
  de lo mismo"* — es otra prompt. Como **ganancia de precisión** la afirmación se
  sostiene; como confirmación de la misma medida, no.

- ⏰ **La hora UTC se anota ANTES de leer el número — pero `T-086` NO se salda
  aquí, y esa parte del encargo se corrige.** La auditoría propuso matar `T-086`
  de camino *"porque esta es la próxima lectura de costos"*. **No lo es:**
  `T-086` dice literalmente *"la próxima lectura de **AWS**"*, y la consola de
  Anthropic **es otro bolsillo**.

  🚨 **Y esa confusión ya rompió algo aquí una vez.** `[A-024]` lo dejó escrito:
  *"son cuatro bolsillos distintos y no se mezclan — `[A-018]` ya se rompió una
  vez por juntar fuentes"*. Dar `T-086` por cerrada con una lectura de Anthropic
  la mataría **sin que nadie hubiera mirado AWS**, que es justo lo que pide.

  ✅ **Lo que sí se toma del encargo es el hábito, que es lo transferible:**
  **ninguna lectura de costo se anota sin su hora UTC, con la zona escrita
  dentro del dato** (`[D-046]`), sea de AWS o de Anthropic. 🔑 Hay que acordarse
  **ahora**: después de ver el número, la hora ya se perdió. `T-086` sigue
  abierta y sigue esperando a AWS.

- 👤 **La lectura la hace el estudiante.** Es su cuenta, cuesta $0 y `[D-058]` ya
  sentó que es acción suya (regla 1). No se da por hecha ni se simula.

---

#### 📖 LECTURA PARCIAL del 2026-08-14 — `T-095` sigue ABIERTA

- 🕒 **Lo leído, con la zona dentro del dato (`[D-046]`):**

  ```
    Lectura de la consola de Anthropic (T-095)
    Fecha/hora: 2026-08-14, 15:08 UTC (10:08 hora Colombia, UTC−5)
    Espacio:    teapp-measure (wrkspc_016KhRzaTBUeGZ9ZukWsoRUe)
    Clave:      teapp-measure-local
    Vista USO,   día 14/08:       21.668 entrada | 2.959 salida
    Vista USO,   semana 10–16/08: 23.502 entrada | 3.297 salida
    Vista COSTO, últimos 7 días:  0,20 US$  (solo uso de API)
    Costo del día 14 AISLADO:     PENDIENTE de leer
  ```

- ✅ **El día 14 está limpio AL TOKEN.** La consola dice `21.668 | 2.959` y
  `T-093` midió `21.668 | 2.959`: **idénticos**. No hubo ni una llamada ajena en
  `teapp-measure` ese día. 🔑 **Eso simplifica lo que `[D-079]` había previsto:
  no hay que descontar nada** — ni las sondas de `check_api_key.py` ni la llamada
  mínima de `[D-061]`, porque no cayeron el 14. **El día 14 es `T-093` entera, y
  `T-093` entera es el día 14.**

- ✅ **Las tarifas unitarias quedan validadas contra un número LEÍDO, y sobre un
  mix distinto del que las originó:**

  ```
    a = 0,53 × $0,00234 / 247 = $0,000005021 por token de entrada
    b = 0,47 × $0,00234 /  44 = $0,000024995 por token de salida
    b/a = 4,98  ← coherente con el "la salida cuesta 5×" de [D-058]

    SEMANA (23.502 / 3.297) derivado = $0,2004
    SEMANA leído en la consola       = $0,20        ✅ COINCIDE
  ```

  🔑 **No es circular:** la semana va **7,1:1** entrada/salida y `[D-058]` iba
  **5,6:1**. El modelo de tarifas acierta sobre una mezcla que no es la suya.

- 🚨 **Y AUN ASÍ `T-095` NO SE CIERRA HOY. Falta un clic.** El `$0,20` que se
  leyó es de *"últimos 7 días"*, **no del día 14**. El número del día 14 está
  **derivado, no leído** — cerrar con él es exactamente lo que prohíbe la regla
  6, y sería especialmente feo hoy, en la sesión que lleva tres defectos de esa
  familia cazados. **Estado exacto de `T-095`: banda sellada, lectura parcial
  tomada el 2026-08-14 a las 15:08 UTC, falta el costo del día 14 aislado.** Ni
  *"cuadró"* ni *"no cuadró"*.

  👉 **Lo que falta:** en la vista de COSTO, la gráfica *"Costo diario de
  tokens"* → leer la barra del 14 de agosto. Alternativa: cambiar el rango a uno
  personalizado 14→14.

- 🔮 **DOS PREDICCIONES SELLADAS ANTES DE ESE CLIC, y no son la misma.** Se
  escriben las dos porque **una es más fuerte que la otra y conviene saber cuál
  falla:**

  | predicción | intervalo | de qué depende |
  |---|---|---|
  | derivación completa (auditoría) | **$0,18 – $0,19** | del modelo de tarifas al 100% |
  | **por RESTA** (más fuerte) | **$0,177 – $0,187** | del modelo solo para el 9% |

  🔑 **Por qué la resta es mejor:** el día 14 es el **91,2%** del gasto de la
  semana, y la semana está **leída**. `día 14 = $0,20 leído − $0,0177 del
  excedente`, y el `$0,20` a resolución de céntimo es `$0,195–$0,205`. Solo el
  excedente —una novena parte— necesita el modelo de tarifas. **Cuanto menos
  pesa lo derivado, más vale la predicción.**

  ⚠️ **Y no coinciden del todo:** si la barra sale entre `$0,177` y `$0,180`, la
  predicción de la auditoría falla y la de la resta aguanta. Eso **no sería un
  empate**: sería la señal de que el modelo de tarifas está algo alto, y se
  sabría hoy y no dentro de tres semanas.

- 🚨 **DOS VISTAS, DOS DEFINICIONES — y lo declaran ellas solas.** Va escrito
  aquí, junto al procedimiento de lectura, y no en una nota suelta:

  > **Vista USO** → *"Incluye el uso de la API y la Consola"*
  > **Vista COSTO** → *"Mostrando solo el uso de API"*

  Son **dos instrumentos con criterios de inclusión distintos sobre el mismo
  bolsillo**. Hoy no muerde —los tokens del 14 coinciden exactos con `T-093`, así
  que no hubo uso de consola ese día y las dos vistas describen el mismo
  conjunto—. 🔑 **Pero el día que un número de USO y uno de COSTO no cuadren, la
  primera hipótesis no es un error de cálculo: es esto.** Misma familia que el
  cuarto reloj de `[A-018]`.

- ⏱️ **Observación suelta, y se marca como tal: el cargo apareció EL MISMO DÍA.**
  En AWS el dato de facturación tardaba ~24 h y esa espera costó sesiones
  enteras (`[A-018]`). ⚠️ **Es UNA observación de UN día, no una regla** — no se
  escribe *"la consola de Anthropic actualiza en tiempo real"*. **Y lo que no se
  sabe:** no se midió cuánto tardó en aparecer, solo que a las 15:08 UTC ya
  estaba. **El retardo real está entre 0 y ~15 horas.** Lo que sí cambia es la
  expectativa: no hay que planificar una espera de 24 h para leer gasto de
  Anthropic.

- 📌 **Cabo suelto, anotado con el número dentro** (`T-096`): la semana trae
  **1.834 tokens de entrada y 338 de salida ≈ $0,018** que el día 14 no explica —
  unas **5 llamadas** al perfil actual. **No cuadra con las sondas que teníamos
  anotadas:** `check_api_key.py` y la llamada mínima de `[D-061]` suman decenas
  de tokens, no 1.834. Algo más llamó con la llave del laboratorio esa semana,
  **en un día que no es el 14**. No bloquea nada —son centavos y no tocan el día
  de la corrida— pero es el tipo de cabo que aquí se cobra tres sesiones después.

---

#### ✅ DESENLACE del 2026-08-14 — barra del día 14 leída: **$0,18**. RAMA A. `T-095` CERRADA

- 🕒 **Lo leído:** vista de COSTO → *"Costo diario de tokens"* → **barra del
  14/08 = `0,18 US$`**, espacio `teapp-measure`. Lectura del estudiante en su
  cuenta, 2026-08-14.

- 🟢 **RAMA A, la que estaba escrita antes de mirar.** `$0,18` cae dentro de la
  banda sellada `$0,156–$0,205`. En consecuencia, y **porque estaba
  pre-comprometido, no porque encaje**:

  - **`COST_PER_CALL_USD` pasa de DERIVADO a MEDIDO** y se le retira la etiqueta
    de tres partes de `[D-078]`.
  - **`[D-058]` queda confirmada en su mecánica:** los precios unitarios no
    cambiaron. El modelo de tarifas acertó **dos veces sobre números leídos** —
    la semana (`$0,2004` derivado contra `$0,20` leído) y el día
    (`$0,1828` derivado contra `$0,18` leído).

- 📊 **El coste por llamada, ahora medido — y es un INTERVALO, no un punto:**

  ```
    60 llamadas de T-093 ......... $0,18   (leído; el día 14 es T-093 entera)
    por llamada .................. $0,18 / 60 = $0,00300

    ⚠️ la consola redondea al céntimo:
       $0,18 es en realidad [$0,175 , $0,185]
       por llamada ............... [$0,00292 , $0,00308]
  ```

  🔑 **`COST_PER_CALL_USD` se queda en `0,00304` y no baja a `0,0030`.** Los dos
  caen dentro del intervalo medido, y la constante **sigue siendo la calibración
  de un freno**: dentro de lo que la medición permite, se escoge el lado alto.
  Es el punto (c) de `[D-078]`, que sobrevive a la medición en vez de
  desaparecer con ella. `MAX_CALLS_PER_RUN` sigue en **82**, con la tanda de 60
  entrando entera.

- 🚨 **LO QUE ESTA LECTURA NO HIZO, y hay que decirlo: no discriminó entre las
  dos predicciones.** Se sellaron `$0,18–$0,19` (derivación completa) y
  `$0,177–$0,187` (por resta), con la idea de que si caía entre `$0,177` y
  `$0,180` fallaría la primera y aguantaría la segunda. **Las dos se cumplen, y
  eso no es una victoria doble: es que el instrumento no da para separarlas.**
  A resolución de céntimo, `$0,18` abarca `[$0,175, $0,185]` y pisa las dos
  franjas a la vez.

  🔑 **Lo que enseña:** *la predicción se selló con más cifras significativas de
  las que el instrumento podía leer.* Dos predicciones que se distinguen en
  `$0,003` no son distinguibles por una pantalla que redondea a `$0,01`.
  **Sellar la predicción es la mitad del método; la otra mitad es comprobar que
  el instrumento tiene resolución para decidirla.** Ver `[L-060]`.

- 📌 **Sigue viva `T-096`** (las ~5 llamadas del excedente semanal, `$0,018`): la
  lectura del día no la toca, porque el excedente cayó en otro día.

- **Toca:** `T-095` (cerrada aquí), `T-096`, `T-086`, `[D-078]`, `[D-077]`,
  `[D-074]`, `[D-062]`, `[D-061]`, `[D-058]`, `[D-046]`, `[A-018]`, `[L-059]`,
  `[L-060]`, `measure_tutor.py`, `app/tools.py`, `check_api_key.py`.

- **Origen:** encargo 3 de la auditoría externa del 2026-08-14, sellado **antes**
  de abrir la consola. La banda, la resolución de ±25%/±2,7% y las dos
  comprobaciones de la rama B (ni persistencia en disco, ni `cache_control` en el
  repo) se verificaron aquí.

---

### [D-078] 2026-08-14 — El precio por llamada estaba caducado: `[D-077]` esperaba $0,1404 con el precio de una rúbrica que ya habíamos borrado

- **Se decidió (tres cosas, y la tercera es la que toca código):**

  1. **El número esperado de `T-095` deja de ser `$0,1404`.** La comparación
     correcta es contra **~$0,182**, derivado del perfil real de `T-093`.
  2. **Se retira la conclusión pre-escrita de `[D-077]`.** Si la consola no
     cuadra, la primera sospecha es **la prompt**, no `[A-010]`.
  3. **`COST_PER_CALL_USD` sube de `0,00234` a `0,00304`**, marcado como
     **derivado**, no medido.

- 🚨 **El defecto, y dónde estaba.** `[D-058]` midió `$0,00234` por práctica el
  2026-08-11 con **247 tokens de entrada y 44 de salida**. El 13 de agosto,
  `[D-066]`/`[D-067]` le añadieron a `GRAMMAR_RUBRIC` el bloque OK/FIX:

  ```
    GRAMMAR_RUBRIC en 1365ed1 (corrida de [D-058]):    678 chars
    GRAMMAR_RUBRIC hoy        (corrida de T-093)  :  1.016 chars
    crecimiento de la rúbrica ...................... +49,9%
    tokens de entrada que medimos: 247 → 361 ....... +46,2%
  ```

  Las dos cifras se persiguen. Creció la rúbrica y **nadie tocó
  `COST_PER_CALL_USD`**.

- 🧮 **El número corregido, y de qué está hecho.** Solo con datos nuestros — la
  relación de `[D-058]`, donde el token de salida cuesta **5×** el de entrada:

  ```
    unidad = $0,00234 / (247 + 5×44)           = $5,011e-6
    llamada [D-058]: 247 + 5×44 = 467 unidades = $0,00234
    llamada T-093  : 361 + 5×49 = 606 unidades = $0,00304
    60 llamadas .............................. = $0,182   (no $0,1404)
    desvío ................................... = +29,8%
  ```

  ⚠️ **Ese `$0,182` es DERIVADO, no leído**, y no se puede citar como coste
  medido (regla 6). Supone que el precio por token no cambió. El instrumento
  sigue siendo la consola, y sigue siendo `T-095`.

- 🚨 **Lo peor no era el 30% de desvío: era el otro lado.** `[D-077]` dejaba
  escrito *"si cuadra, `[D-058]` queda confirmada con 6× más muestras"*. **No
  puede.** No son 6× más muestras de lo mismo — **es otra prompt**. Si la
  consola dijera `$0,14`, eso no confirmaría nada: sería la señal de que algo
  está mal. Y la otra rama mandaba a auditar `[A-010]`, el tope de 20 prácticas
  al día, que no tiene nada que ver: **la tercera explicación estaba impresa en
  la salida de la propia corrida.**

- 💵 **Por qué el `0,00304` entra en el código aunque sea derivado.** La
  disyuntiva parecía *"número medido contra número derivado"* y **esa opción no
  existía**: `0,00234` tampoco es hoy un número medido, es la medición de una
  configuración que borramos nosotros. Las dos opciones metían en el código un
  número que nadie ha medido; una de las dos, además, era conservadora.

  - 🔑 **Esa constante no AFIRMA nada: divide.** Su único uso es
    `MAX_CALLS_PER_RUN = int(BUDGET_PER_RUN_USD / COST_PER_CALL_USD)`. La regla
    6 protege contra **afirmar** lo no medido. **Un freno se calibra para fallar
    hacia el lado seguro; una afirmación se escribe solo cuando se midió.**
  - ⚖️ **La dirección del error ya la habíamos decidido, y estaba invertida.**
    El comentario de `measure_tutor.py` prometía *"el tope se queda corto, nunca
    largo"* — y estaba **largo**: 106 llamadas al perfil real son **$0,322**
    contra un presupuesto escrito de $0,25. Ese argumento cubría *cambiar de
    modelo*; no cubría **el mismo modelo con una prompt más grande**.
  - 📉 **Y un lado sale gratis.** El acantilado está en `$0,00416`
    (`int(0,25/x) >= 60`): con `0,00304` caben **82** llamadas y la tanda de 60
    que exige `TARGET_SAMPLES` sigue entrando entera, con 22 de sobra. Pasarse
    cuesta **cero**; quedarse corto cuesta **dinero** del saldo de `[C-008]`.
    ⚠️ **Sin relleno "por si acaso":** un padding sería otro número sin origen.

- ➕ **Y el acantilado deja de ser un comentario.** `MAX_CALLS_PER_RUN` sale del
  **dinero** y `TARGET_SAMPLES` sale de la **regla de tres**, y nadie los
  cruzaba. Nuevo test: `assert MAX_CALLS_PER_RUN >= TARGET_SAMPLES`. 🔑 Sin él,
  subir el coste lo suficiente hace que el monedero corte antes de las 60 y
  `verdict_for` devuelva `SIN VEREDICTO` **después de haber gastado** — se paga
  y no se concluye. Es `[L-013]` otra vez: un freno que no has visto morder es
  una nota, no un freno. Suite: 439 → **440 passed**.

- 📌 **`T-095` no se cae; se vuelve más fuerte.** Comparar la consola contra
  ~$0,182 es una prueba **que de verdad puede fallar**. Contra $0,1404 estaba
  condenada a dar un desacuerdo falso y a mandarnos a auditar `[A-010]`. Cuando
  la consola hable, el derivado se reemplaza por el medido — y **ese** sí se
  puede escribir aquí.

- **Toca:** `measure_tutor.py` (`COST_PER_CALL_USD`, `MAX_CALLS_PER_RUN`),
  `tests/test_measure_tutor.py`, `[D-077]`, `[D-058]`, `[D-066]`, `[D-067]`,
  `[D-060]`, `[D-062]`, `[C-008]`, `[A-010]`, `T-095`, `[L-059]`.

- **Origen:** `T-094`, auditoría externa del 2026-08-14 (hallazgos H-1 y H-2).
  Los tres crecimientos —rúbrica, tokens y el acantilado de $0,00416— se
  comprobaron aquí sobre `46cce85` antes de escribir nada.

---

### [D-077] 2026-08-14 — `[A-011]` se cierra al tercer intento, con la corrida delante y con condición

> 🟡 **ESTA DECISIÓN ESTÁ VIVA, NO ARCHIVADA. `T-079` baja de ✅ a 🟡 el
> 2026-08-14.**
>
> **Disparador — si vuelven los cortes al practicar, se repite la tanda de 60
> ANTES de tocar `TUTOR_TIMEOUT_SECONDS`.** El número no se sube porque duela:
> primero se comprueba si el mundo medido sigue siendo el mismo.
>
> 🔑 **Por qué baja la marca, y el motivo NO es que la medición fuera pobre.**
> La medición existe y es real: 60 llamadas, cero cortes, criterio fijado antes
> de mirar. Lo que falla es el símbolo. **Un ✅ afirma que no queda nada que
> vigilar**, y esta entrada deja algo vivo que vigilar: su propia condición
> —*"vale mientras Anthropic responda como el 2026-08-14"*— **no depende de
> nosotros y no se puede cerrar midiendo**. Repetir la tanda mañana daría otro
> verde igual de condicionado y costaría otros $0,18: pagar por no cambiar de
> estado. La condición no se cierra, se vigila.
>
> 🔴 **Corrección del 2026-08-14, sobre una frase que se dijo HOY y no sobre
> prosa vieja.** El resumen de esta entrada llegó a describir las cuatro fases
> como *"cuatro relojes en paralelo, y la suma ya cabe en los 9,0 por
> construcción"*. **Las dos mitades son falsas, y `app/tools.py:239` ya avisaba
> de lo contrario antes de que se escribiera:**
>
> - **No son paralelas, son SECUENCIALES.** Si lo fueran, el techo sería
>   `max(6,5)` y no la suma `9,0` — la propia aritmética lo desmiente.
> - **`9,0` no sale "por construcción": es una constante nuestra**, una suma
>   hecha a mano para poder compararla con el `10,0`. El SDK no la impone en
>   ningún sitio. Y `read` **tampoco** es techo duro por su cuenta:
>   `_receive_response_body` usa el mismo `read`, así que un cuerpo en muchos
>   trozos puede pasar de 6,5 (`app/tools.py:235`).
>
> 🚨 **Lo único que corta por reloj de pared es `attempt.result(timeout=
> TUTOR_TIMEOUT_SECONDS)`, `app/api.py:730`.** Los 10 s **no son "el hueco" y no
> sobran: son la única garantía que existe.** Quien lea que el 9,0 es el techo
> real concluirá un día que el 10,0 es redundante y lo retirará — llevándose por
> delante lo único que garantiza que una práctica termine.
>
> ⚠️ **Y el eco pesa: los DOS cierres anteriores de `[A-011]` murieron por
> colgarse de un techo inexistente** (`[D-070]`, `[L-054]`). El argumento de hoy
> no falla, pero la frase con que se contó es de esa misma familia. Tercera vez
> que este cierre se apoya en un techo; las dos anteriores el techo no estaba.
>
> ✅ **Lo que sí se sostiene, y por el camino que no depende de nada que el SDK
> no garantice:** `[A-030]` (la báscula reusó la conexión, así que `connect` se
> ejerció en 1 de 60) **no muerde igual**. `connect = 1,5` tiene presupuesto
> propio y no se come el `read`, así que el peor caso medido —**3,91 s**— sigue
> siendo peor caso de la fase que el corte de 6,5 vigila. Y por encima de todo
> está el `10,0` de reloj de pared, que corta **sea cual sea** el número de fases
> que se ejerciten. Se llega al mismo sitio sin invocar el paralelismo que no
> existe.

- **Se decidió:** **`TUTOR_TIMEOUT_SECONDS = 10.0` se queda**, y `[A-011]` deja
  de ser suposición. Es el **tercer** intento de cerrarla y el primero con una
  medición que contesta la pregunta correcta.

- 📊 **La corrida, del 2026-08-14** — `measure_tutor.py` contra `claude-opus-5`,
  60 frases distintas, 60 de 60 completadas:

  ```
    mínimo:      1,73 s
    mediana:     2,88 s
    peor de 60:  3,91 s

    por encima de 6,5 s (corta y COBRA):        0 de 60
    por encima de 9,0 s (ni el reparto salva):  0 de 60
  ```

  Tokens: **21.668 entrada + 2.959 salida** (~361 y ~49 por llamada).
  Presupuesto: 60 llamadas de las 106 que permitía el monedero.

- ✅ **VERDE.** Por la regla de tres, con cero cortes en 60 muestras la tasa de
  corte **no pasa del 5,0%** — que es exactamente la tasa aceptada, porque el 60
  se eligió para que esos dos números fueran el mismo (`[D-074]`).

- 🚨 **EL CIERRE ES CONDICIONADO, y la condición va aquí dentro y no en el
  resumen de nadie:**

  > **El 5% vale mientras Anthropic responda como respondió el 2026-08-14. Si
  > vuelve la saturación de `T-087`, este número no aplica y la tanda se repite
  > — no porque el criterio fallara, sino porque cambió el mundo que se midió.**

  🔑 **Por qué esto no es una cautela de adorno.** Las 60 llamadas fueron
  **secuenciales, en unos 3 minutos** (60 × 2,88 s ≈ 173 s), un solo día, contra
  un sistema que no controlamos. No son 60 observaciones independientes de "cómo
  le va a alguien practicando": son **60 llamadas pegadas bajo unas condiciones
  que duraron tres minutos**. Y hay evidencia directa de que la condición varía:
  `T-087` fue literalmente *"Anthropic dejó de saturar"* — hace nada, estas
  mismas 60 habrían dado otra cosa.

  ⚠️ **Y el fallo que la condición previene tiene forma conocida:** sin ella,
  `[A-011]` no muere, se vuelve a levantar dentro de seis meses cuando alguien
  vea cortes, no encuentre el porqué, y lea una entrada cerrada diciéndole que
  eso ya se resolvió. Sería el cuarto intento, y el peor, porque llegaría
  disfrazado de asunto zanjado.

- ⚠️ **Lo que NO dice esta medición.** El peor de 60 (**3,91 s**) salió **por
  debajo** del peor de 10 que ya teníamos (4,72 s). 🔑 **Eso no es una mejora:**
  `max(N)` es un cuantil que se mueve, y que una tanda de 60 dé menos que una de
  10 es ruido, no tendencia (`[L-058]`). El veredicto **no se apoya en esa
  cifra**: se apoya en el conteo contra un umbral fijado antes de mirar. Y sigue
  sin ser el tiempo de una práctica entera — falta `respond()` (`[L-043]`).

- ✅ **El instrumento no censuró la cola.** `MEASURING_READ_SECONDS = 30` contra
  un peor caso de 3,91 s: ninguna muestra se perdió contra el tope de la báscula,
  así que la distribución que se vio es la que hubo. El cuidado de `[L-057]`
  resultó no hacer falta — **pero eso solo se sabe después**, que es justo el
  motivo por el que se tomó antes.

- 🧭 **El orden importa tanto como el resultado.** Los tres arreglos de hoy
  (`[D-075]`) **endurecieron** el criterio: ROJO bajó de 9,5 a 9,0, ÁMBAR dejó de
  afirmar cosas falsas, y la tanda corta pasó a no emitir veredicto. **Salió
  verde con el criterio más estricto, no con el más laxo.** Si se hubiera corrido
  primero y arreglado después, este VERDE no valdría nada: nadie podría
  distinguirlo de un umbral movido para que encajara.

- 🔴 **ESTE PÁRRAFO ESTABA MAL Y LO CORRIGE `[D-078]` EL MISMO DÍA. Léelo allí,
  no aquí.** El `$0,1404` usa el precio de `[D-058]`, medido con **247** tokens
  de entrada — y esta misma entrada, cincuenta líneas más arriba, registra que
  la corrida gastó **361**. La comparación correcta es contra **~$0,182**, y si
  no cuadra la primera sospecha es **la prompt**, no `[A-010]`. Se deja tachado
  y no borrado porque el fallo enseña más que el número:

  > ~~Los tokens de estas 60 llamadas son seis veces más muestras que las 10 con
  > las que se fijó `[D-058]` (`$0,00234` por práctica). **Cuando se lea la
  > consola de Anthropic, hay que comparar el cargo real contra
  > `60 × $0,00234 = $0,1404`:** si cuadra, `[D-058]` queda confirmada con 6× más
  > muestras y $0 extra; si no cuadra, lo que necesita revisión es `[A-010]` —el
  > tope de 20 prácticas al día—, y es mejor saberlo hoy que en el paso 9
  > comparando modelos.~~ 🚨 El número **no se escribe aquí de memoria**
  > (regla 6): se escribe cuando se haya leído.

  > 🚨 **Y si la consola todavía no muestra el cargo, ESO NO ES UN CERO.** Es el
  > hueco por el que ya se cayó este proyecto: el `0,00 USD` de AWS venía con
  > *"Sin datos"* al lado y se leyó como medición durante días. La anotación
  > correcta si sale vacío es **"consultado el 14, todavía sin datos"** — ni
  > *"cuadró"* ni *"no cuadró"*. Señalado por la auditoría del 2026-08-14, que lo
  > sitúa en LM.31 del repo supervisor (sin corchetes: desde aquí no se puede
  > abrir esa entrada para comprobarla).

- **Origen:** `T-093`, propuesta por auditoría externa el 2026-08-13 y corregida
  por la misma el 2026-08-14 antes de gastar. La condición de este cierre la
  señaló la auditoría del 2026-08-14, tercera ronda.

---

### [D-076] 2026-08-14 — El hueco entre el cliente y la ruta pasa de comentario a assert

- **Se eligió:** convertir en constantes con nombre los dos sumandos que la
  tabla de `app/tools.py` llevaba solo como texto —**`LOCAL_WORK_SECONDS = 0.07`**
  y **`SURRENDER_MARGIN_SECONDS = 0.50`**— y atarlos con un assert:

  ```python
  hueco = api.TUTOR_TIMEOUT_SECONDS - TIMEOUT_SECONDS
  assert hueco >= LOCAL_WORK_SECONDS + SURRENDER_MARGIN_SECONDS
  ```

- 🚨 **Qué no cubría lo que ya había.** Existían dos asserts: `sum(fases) ==
  TIMEOUT_SECONDS` y `TIMEOUT_SECONDS < api.TUTOR_TIMEOUT_SECONDS`. Con
  `TIMEOUT_SECONDS = 9.9` **los dos siguen en verde** y el hueco cae a **0,1 s**,
  por debajo de los 0,57 que la propia tabla exige: el cliente deja de rendirse
  antes que la ruta en cuanto haya algo de disco.

  🔑 **«Más corto» no es suficiente: tiene que ser más corto POR ALGO.** Eso
  "algo" estaba escrito, pero en prosa.

  Visto morder, no supuesto — con `TIMEOUT_SECONDS = 9.9`:

  | assert | antes | ahora |
  |---|---|---|
  | `sum(fases) == TIMEOUT_SECONDS` | ✅ verde | ✅ verde |
  | `TIMEOUT_SECONDS < TUTOR_TIMEOUT_SECONDS` | ✅ verde | ✅ verde |
  | `hueco >= local + margen` | *no existía* | 🔴 **rojo** (0,10 < 0,57) |

- ⏫ **Por qué sube de prioridad justo ahora, y es culpa de nuestro propio
  arreglo.** Esto llevaba de deuda desde la sesión 71 como algo independiente de
  `T-093`. Dejó de serlo con `[D-075]`: al derivar el umbral de ROJO de
  `TIMEOUT_SECONDS`, **el hueco cliente→ruta pasó a ser carga estructural del
  criterio de `T-093`**. Un arreglo correcto puede ascender una deuda ajena.

- ⚠️ **`LOCAL_WORK_SECONDS = 0,07` es una ESTIMACIÓN, y va anotada como tal en
  `[A-029]`.** Sale de redondear los 56,3 ms de `measure_local_parts.py`, que son
  `max(N)` — la sexta corrida ya dio 62,4 ms.

  🔑 **Se usa igual porque el margen lo domina: 500 ms contra 70 ms, unas 7
  veces.** `SURRENDER_MARGIN_SECONDS` no es una medida ni pretende serlo — es
  holgura decidida en `[D-073]`—, y un error de ±10 ms en la estimación no puede
  voltear el assert en ninguna configuración realista.

  > 🔴 **Aquí se escribió primero *"el error cae del lado seguro"*.** Es flojo:
  > subestimar produce **falsos negativos**, y en un **guardián** esa es la
  > dirección peligrosa —un verde que no significa nada—, no la benigna. Vale
  > para un `read`, no para esto. Corregido el 2026-08-14, misma ronda.

  Lo que no se puede en ningún caso es dejar que el assert convierta la
  estimación en dato, y por eso el comentario lo dice con todas las letras.

- 🧭 **La lección de fondo, que es `LM.34` un piso más arriba:** *"una función
  que nadie prueba es un párrafo con paréntesis"* — y **la tabla que justifica
  `read` era exactamente eso**. Un comentario no lo lee ningún test. Esta entrada
  es esa lección ejecutándose sobre sí misma.

- **Coste:** $0.

- **Origen:** auditoría externa del 2026-08-14, segunda ronda.

---

### [D-075] 2026-08-14 — El umbral de ROJO se lee de producción; el `9,5` literal cambiaba un veredicto

- **Se eligió:** **`ROUTE_THRESHOLD_SECONDS = tools.TIMEOUT_SECONDS`** (9,0), en
  vez del `9,5` escrito a mano. Y de paso, reescribir los textos de los tres
  veredictos y negar el veredicto cuando la tanda no llega a las 60 muestras.

- **Contra qué:** contra dejar el criterio de `[D-074]` tal cual y correr la
  tanda. Cuesta $0 arreglarlo antes; arreglarlo **después de ver los números** es
  exactamente lo que la disciplina de "fijado antes de gastar" prohíbe.

- 🚨 **El defecto que cambiaba un veredicto.** El umbral de ROJO (9,5) estaba
  **por encima del presupuesto entero del cliente** (`TIMEOUT_SECONDS = 9,0`):

  ```
    ruta    (api.TUTOR_TIMEOUT_SECONDS)   10,0
    cliente (tools.TIMEOUT_SECONDS)        9,0   ← el techo real
    fases   1,5 + 0,5 + 6,5 + 0,5          9,0
    ROUTE_THRESHOLD_SECONDS                9,5   ← por encima del techo
  ```

  El caso que lo rompe es una llamada de **9,2 s**: pasa del corte (6,5) pero no
  del 9,5, así que salía **ÁMBAR**. Y la receta de ÁMBAR es *"quitar de
  `connect`/`write`/`pool` y dárselo a `read`"* — **imposible aquí**: el techo de
  `read` es `TIMEOUT_SECONDS` menos las otras tres fases, así que aunque se
  dejaran en cero, `read` no pasa de 9,0. No hay reparto que salve 9,2 s. **Era
  ROJO y el criterio decía ÁMBAR.**

- 🧮 **De dónde sale el 9,0:** **el reparto de fases está acotado por el
  presupuesto del cliente.** Ninguna fase puede recibir más de lo que hay que
  repartir, así que el máximo que `read` podría llegar a tener —vaciando las
  otras tres— es `TIMEOUT_SECONDS` entero. Por encima de ahí no hay reparto que
  salve nada, que es justo lo que ROJO significa.

  > 🔴 **Aquí se escribió primero una justificación de DOS restas
  > "independientes", y era circular.** Corregido el mismo día por la auditoría:
  >
  > - **Camino A** (`9,0 − 0 − 0 − 0 = 9,0`) es una **tautología**: "el máximo
  >   que cabe si le doy todo a `read`" **es** el presupuesto del cliente, por
  >   definición. No demuestra nada, lo repite.
  > - **Camino B** (`10,0 − 1,0 = 9,0`) solo aterriza en 9,0 **si el 1,0 se toma
  >   como ruta menos cliente** — que es lo que se quería demostrar. Con los
  >   componentes de verdad de la tabla de `tools.py`: `0,07 + 0,50 = 0,57`, y
  >   `10,0 − 0,57 = 9,43`, **no 9,0**. El 0,43 que falta no es reserva de nada:
  >   es lo que sobró de poner `read` en 6,5 en vez de 6,93.
  >
  > 🔑 **El número era correcto y el porqué no**, que es lo único que habría
  > engañado al siguiente. Se borra el segundo camino: el argumento del
  > acotamiento **se sostiene solo y no necesita corroboración**.

- 🔑 **Y se LEE, no se copia.** El comentario viejo prometía *"ninguno se estima:
  los dos salen del código"*, y era verdad para uno solo: `CUT_THRESHOLD_SECONDS`
  se leía de `tools.TIMEOUT.read`, pero `9,5` era un literal. Saboteando el
  reparto (`TIMEOUT_SECONDS = 7,0`, `read = 4,5`) se ve morder: antes se movía un
  umbral, ahora se mueven los dos —`CUT 6,5 → 4,5`, `ROUTE 9,0 → 7,0`—.

- ➕ **Dos textos que afirmaban cosas literalmente falsas.** Se comprobaron
  llamando a la función, sin gastar un centavo:

  | llamada | decía | por qué es falso |
  |---|---|---|
  | `verdict_for(1, 0, 60)` | *"1.7%, por encima del 5% acordado"* | 1,7 **no** está por encima de 5 |
  | `verdict_for(0, 0, 45)` | *"por debajo de 6.7%, que es el 5% acordado"* | 6,7 **no** es 5 |

  🔑 **El umbral no estaba mal; lo que decía de sí mismo, sí.** Exigir **cero**
  cortes para VERDE es correcto: la regla de tres solo permite afirmar `≤ 5%` con
  cero observados. Lo que no se puede decir con 1 corte de 60 es *"está por
  encima del 5%"* — lo cierto es más flojo: **ya no se puede AFIRMAR que esté por
  debajo**, que es otra cosa.

- ⚠️ **La tanda corta era alcanzable de verdad, no un caso de laboratorio.** Los
  dos `except` del bucle hacen `break`, no `continue`. Un `TutorUnavailableError`
  en la frase 45 termina la tanda con `rows` lleno, salta el `if not rows`,
  imprime el aviso de N corta —**y a continuación el veredicto igual**, con la
  ecuación falsa dentro. El aviso decía *"no se puede escribir en `[A-011]`"* y
  justo después escribía la frase que alguien copiaría.

  > 🔑 **Un aviso se salta; un veredicto que no sale, no.** `verdict_for` ahora
  > devuelve `SIN VEREDICTO` cuando `total < TARGET_SAMPLES`, y el aviso
  > duplicado de `main()` desaparece: una sola voz.

- ➕ **`TARGET_SAMPLES` pasa a ser `ceil(3 / ACCEPTED_CUT_RATE)`.** La tasa
  aceptada no aparecía en **ninguna** comparación: solo se interpolaba en textos,
  y las ramas se elegían por `over_cut == 0`. Derivando el 60 de ella, la
  constante manda por construcción, sin ramas muertas. Mismo método que
  `MAX_CALLS_PER_RUN`.

- 🚨 **Por qué se coló todo esto: `verdict_for` no tenía un solo test.**
  `[D-074]` acertó al escribir el criterio como **función y no como párrafo** —es
  lo que hizo posible auditarlo con tres comandos de una línea y $0—, pero una
  función que nadie prueba es un párrafo con paréntesis. Ahora hay 12 tests, y
  tres de ellos son exactamente los tres defectos.

- **Lo que la auditoría confirmó que está bien y no se toca:**
  `MEASURING_READ_SECONDS = 30` (un instrumento no mide su propio tope),
  `CUT_THRESHOLD_SECONDS` leído de producción, las 60 frases **distintas** por lo
  de la caché, el `if not rows: return`, y el criterio como función.

- **Coste:** $0. Todo es texto, un umbral y tests.

- **Origen:** auditoría externa del 2026-08-14 (terminal supervisora), sobre el
  commit `464cdf9`. Verificado aquí comando por comando antes de tocar nada.

---

### [D-074] 2026-08-13 — El criterio de `T-093`, fijado antes de gastar

> 🔴 **Corregida el 2026-08-14 por `[D-075]`, antes de gastar nada.** La forma
> —criterio escrito antes, y como función— se queda entera. Lo que se retira son
> tres defectos: el umbral de ROJO (9,5) estaba **por encima del techo del
> cliente** y mandaba a ÁMBAR llamadas que eran ROJO, dos veredictos afirmaban
> cosas falsas sobre la tasa, y la tanda corta imprimía veredicto igual. **Lee
> `[D-075]` antes de fiarte de los números de aquí abajo.**

- **Se eligió:** dejar escrito, **antes de correr la tanda**, cuántas muestras se
  compran, qué tasa de corte se acepta y qué significa cada resultado.

- **Por qué antes y no después:** decidir el umbral viendo ya los datos lleva a
  tomar `max(N)` como si fuera una cota. Es `[L-058]`, y hoy mordió **dos veces**
  — con `max(10)` en `[D-072]` y con las seis tandas locales. 🚨 Y con más
  muestras el error **se siente más sólido**, no menos.

- 🔢 **De dónde sale el 60, que no es un número redondo.**

  La tasa de corte que se acepta es **5%**: 1 de cada 20 prácticas cortada **y
  cobrada** (`[D-051]`). Con cero cortes observados, lo máximo que se puede
  afirmar es la regla de tres, `3/n`:

  | n | se puede afirmar | ¿sirve? |
  |---|---|---|
  | 40 | tasa < **7,5%** | ❌ afirma menos de lo que exigimos: no concluye |
  | **60** | tasa < **5,0%** | ✅ coincide con el criterio |

  Con 40 habría que escribir *"menos del 7,5%"* y compararlo con un objetivo del
  5%: no se puede cerrar nada. **Cinco centavos más** —**~$0,14** en total— para
  que la afirmación y el objetivo sean el mismo número.

- 🚦 **Los tres veredictos, escritos a ciegas:**

  | | condición | qué significa |
  |---|---|---|
  | 🟢 **VERDE** | 0 de 60 por encima de `tools.TIMEOUT.read` | los 10 s de la ruta valen; **`[A-011]` se cierra**, esta vez sin techos inventados |
  | 🟡 **ÁMBAR** | alguna corta, ninguna pasa de 9,5 s | la ruta está bien; **reequilibrar fases** dentro de los 10 s: quitar de `connect`/`write`/`pool`, dárselo a `read` |
  | 🔴 **ROJO** | alguna pasa de 9,5 s | **ningún reparto de fases salva nada**: lo que está mal es el presupuesto de la ruta |

  El `9,5` es la ruta (10 s) menos el trabajo local y un margen.

- 🔑 **El criterio vive en el CÓDIGO, no en esta entrada.** Es la función
  `verdict_for` de `measure_tutor.py`, y el guion la imprime.

  > Un criterio que hay que ir a buscar a `decisions.md` **se reinterpreta** con
  > los datos ya delante. Uno que imprime el programa, no.

- **⚠️ Salvaguardas escritas dentro:**
  - Si la tanda **no completa las 60**, el guion avisa de que el veredicto **no
    se puede escribir en `[A-011]`** y hay que repetirla. La regla de tres
    necesita la N entera.
  - **60 frases distintas, no 10 repetidas seis veces.** Repetir mediría la
    caché de Anthropic, y saldría **más rápido de lo real** — el lado peligroso
    del error.
  - La báscula sigue corriendo con `MEASURING_READ_SECONDS = 30` (`[L-057]`): si
    heredara el tope de producción, las llamadas lentas dejarían de ser muestras
    y pasarían a ser errores, que es justo lo que hay que contar.

- **Contra:** correr 40 frases por ~$0,09, que era el plan escrito en `T-093`.
  Descartado por la tabla de arriba: es más barato y **no contesta la pregunta**.

- **Toca:** `measure_tutor.py`, `T-093`, `[A-011]`.

### [D-073] 2026-08-13 — `read` no se estima: se calcula por resta, y el número no cambia

- **Se eligió:** **dejar `read` en 6,5 y reescribir su justificación.** El valor
  no se toca; lo que se retira es el razonamiento que lo sostenía.

- **Qué estaba mal:** `[D-072]` lo justificó como *"un 38% por encima de los
  4,72 s de la peor de diez"*. Eso presenta `max(n=10)` como si fuera una cota.
  **No lo es: es un cuantil que crece con N.**

  🔑 Y la prueba salió de casa, midiendo otra cosa. El peor caso **local** en seis
  tandas: `44,9 → 45,9 → 49,2 → 50,6 → 56,3 → 62,4 ms`. **+39% y subiendo.**
  Mismo estadístico, mismo defecto: un número anclado ahí caduca en cuanto se
  vuelva a medir.

- 🧮 **De dónde sale ahora, y es una RESTA, no una medida:**

  ```
    presupuesto de la ruta (TUTOR_TIMEOUT_SECONDS)        10,00
  − connect + write + pool        (1,5 + 0,5 + 0,5)        2,50
  − trabajo local de respond(), peor caso            ~     0,07
  − margen para que el cliente se rinda SIEMPRE antes      0,50
    ──────────────────────────────────────────────────────────
    read máximo                                     ~     6,93
  ```

  Se deja en **6,5**, por debajo del máximo. Esa diferencia es holgura de regalo,
  no un ajuste fino.

- 🔑 **Por qué esta forma no caduca:** no depende de ninguna medición. Y protege
  del error que viene: dentro de dos semanas, con datos nuevos, la tentación será
  recalcular contra un `max(40)` — que **parecerá más sólido que `max(10)` y será
  el mismo error con más muestras**.

- ⚖️ **El motivo de fondo: el coste de equivocarse no es simétrico.**

  | | qué pasa |
  |---|---|
  | `read` **de sobra** | si la generación tarda más que la ruta, muerde la ruta — el único tope de pared que existe. **Coste: cero.** |
  | `read` **corto** | `APITimeoutError` → `request_sent=True` → `[D-051]` **cobra la práctica**, y el log culpa a Anthropic |

  ⇒ Ante ese desequilibrio, `read` se pone **tan alto como quepa**. No tan alto
  como sugiera la última medida.

- ⚠️ **Y hay una segunda razón, que va en contra nuestra y conviene tenerla
  escrita.** La distribución local la produce esta máquina bajo una carga que
  elegimos nosotros: con más muestras converge hacia algo real. **La del tiempo
  de generación la produce un sistema que no controlamos y que cambia sin
  avisar** — capacidad, versión del modelo, carga del día. No es solo que
  `max(N)` crezca con N: es que **la distribución no se está quieta**. Medirla
  hoy dice cómo era hoy.

- ➕ **Rescata a `T-093` de ser inútil.** Si `read` es máximo por construcción, la
  tanda de 30-40 frases **no sirve para ajustar `read`** — y nunca fue esa la
  pregunta. Contesta la que `[A-011]` llevaba haciendo desde el 4 de agosto sin
  saber formularla:

  > **¿Son 10 s el presupuesto correcto de la RUTA?**

  | si el p95 de generación sale… | entonces |
  |---|---|
  | ~7 s | los 10 s valen, `read` los aprovecha enteros, y `[A-011]` se cierra sin techos inventados |
  | ~12 s | **ningún reparto de fases salva nada**: lo que está mal es el presupuesto de la ruta, y 1 de cada 20 personas se come un 504 haga lo que haga el cliente |

  🚨 **Y al correrla hay que aplicarse esta misma lección:** 40 muestras tampoco
  dan un techo. **Se decide ANTES de medir qué percentil se compra y qué tasa de
  corte se acepta** (p95 = 1 de cada 20 cortada y cobrada). Sin decidirlo antes,
  se tomará `max(40)`, que se sentirá más sólido que `max(10)` y será el mismo
  fallo con una N más grande.

- **Toca:** `app/tools.py` (la justificación de `TIMEOUT`, no su valor),
  `[D-072]`, `T-093` (reformulada), `[A-011]`.

### [D-072] 2026-08-13 — `read` sube a 6,5: el reparto de hace dos horas cortaba veredictos buenos

- **Se eligió:** `connect 1,5 + write 0,5 + read 6,5 + pool 0,5 = 9,0`, y
  `TIMEOUT_SECONDS` sube de 8,0 a 9,0. Sigue por debajo de los 10 s de la ruta.

- **Qué estaba mal en `[D-071]`, escrito dos horas antes:** situaba el riesgo del
  `read` en el sitio equivocado. Decía *"si 4,72 s vuelve a aparecer **entre el
  primer byte y el último**"*, tratando ese escenario como el caso a vigilar.

  🚨 **`read` no es eso. `read` es la generación entera.** Comprobado en la
  fuente instalada, no recordado:

  ```
  httpcore/_sync/http11.py :: _receive_response_headers
      timeout = timeouts.get("read", None)
  ```

  Quien espera **las cabeceras** es el `read`. Y sin streaming, Anthropic no
  manda un solo byte hasta que ha terminado de generar. El escenario "cuerpo en
  muchos trozos" existe —`_receive_response_body` también usa `read`— pero con
  `MAX_TOKENS = 1000` es el de riesgo bajo. El caso normal es el otro.

- 🔴 **Y con eso, `read = 4,0` no era un riesgo: era una regresión que nuestros
  propios datos ya predecían.**

  | `[L-043]`, n=10 | s |
  |---|---|
  | mínimo | 1,72 |
  | mediana | 3,33 |
  | **peor de diez** | **4,72** ← `read=4,0` iba por debajo |

  Al menos **1 de cada 10 llamadas medidas** habría cruzado el tope. Y la mediana
  en 3,33 dejaba 0,67 s: eso no es margen, es un pelo.

- 🚨 **El modo de fallo COBRA, y ahí está lo caro.** Un corte del `read` entra
  por `APITimeoutError` → `request_sent=True` → `[D-051]` **cobra la práctica**.
  La persona pierde una de sus 20 del día por un veredicto que Anthropic estaba a
  punto de entregar, y el log dice *"el tutor no contestó"*: **el diagnóstico
  apunta al sitio equivocado**, en producción, con alguien practicando.

- **De dónde sale el reparto nuevo, que no es simétrico a propósito:**

  | fase | antes | ahora | por qué |
  |---|---|---|---|
  | `connect` | 2,0 | **1,5** | sigue siendo ~10× un handshake TLS normal |
  | `write` | 1,0 | **0,5** | la petición es ~1 KB |
  | `read` | 4,0 | **6,5** | la generación entera. ⚠️ El *"38% por encima del peor observado"* que se escribió aquí lo **retira `[D-073]`** el mismo día: `max(n=10)` no es una cota. El 6,5 se queda, pero por resta del presupuesto |
  | `pool` | 1,0 | **0,5** | el pool de `httpx` admite 1000 y aquí ve 40 como mucho: no espera nunca |

  🔑 **Las otras tres estaban sobrefinanciadas, y todo lo liberado va a la única
  fase donde de verdad se tarda.** Repartir a partes iguales habría sido tratar
  como equivalentes cuatro cosas que no lo son.

- **Contra:** dejar `read` en 4,0 y aceptar el corte, argumentando que un
  presupuesto apretado vale más que uno holgado. **Descartado**: eso vale cuando
  el tope no se ha medido; aquí sí se había medido y el tope iba por debajo. No
  es prudencia, es contradecir el propio dato.

- ➕ **Y de paso, la báscula sale de su propio tope.** `measure_tutor.py` heredaba
  `tools.TIMEOUT`, así que toda llamada por encima del `read` de producción
  dejaba de ser muestra y pasaba a ser error — **la cola de la distribución, que
  es justo lo que hace falta para colocar el `read`, era lo invisible.** Ahora usa
  `MEASURING_READ_SECONDS = 30,0`, con la excepción a `[L-043]` escrita al lado.
  Ver `[L-057]`.

- **⚠️ Lo que sigue sin estar resuelto:**
  - **Sigue sin ser techo duro** (`_receive_response_body` también usa `read`).
    Los 10 s de la ruta siguen siendo la única garantía de reloj de pared.
  - **El 6,5 se coloca contra el máximo de diez muestras**, que no es la cola de
    la distribución. Lo que falta es una tanda de 30-40 frases con `read` alto y
    colocarlo contra un **percentil**. Con `[D-058]` cuesta ~$0,09. Es lo que
    `[A-011]` lleva pidiendo desde el día 4, y ahora por fin se sabe qué
    preguntarle.

- **Toca:** `app/tools.py`, `measure_tutor.py`, `measure_local_parts.py` (su
  salida ya no habla de "techo" ni resta márgenes, y lee los presupuestos del
  código), `[D-071]`, `[A-011]`.

### [D-071] 2026-08-13 — El presupuesto del cliente se reparte fase por fase

- **Se eligió:** repartir a mano el presupuesto entre las cuatro fases de una
  petición HTTP, de forma que **la suma sea el presupuesto**:

  | fase | s | por qué ese número |
  |---|---|---|
  | `connect` | 2,0 | abrir TCP + TLS. Con `keepalive_expiry=5.0` y tráfico esporádico, casi cada llamada paga handshake nuevo |
  | `write` | 1,0 | mandar la petición: la rúbrica más una frase A1, ~250 tokens de entrada medidos (`[L-043]`) |
  | `read` | 4,0 | esperar y leer la respuesta. Se lleva la mitad porque es donde de verdad se tarda |
  | `pool` | 1,0 | esperar conexión libre del pool de `httpx`, que admite 1000 |
  | **suma** | **8,0** | = `TIMEOUT_SECONDS`, y sigue por debajo de los 10 s de la ruta |

- **De dónde sale:** de `[L-054]`, el hallazgo 1 de la auditoría del 2026-08-13.
  `httpx` **no divide un `timeout` escalar: lo multiplica** — le da el número
  entero a cada fase por separado. `timeout=8.0` eran 32 s.

- **Contra:**
  1. **El arreglo de una línea que propuso la propia auditoría**,
     `httpx.Timeout(TIMEOUT_SECONDS, connect=2.0)`. 🚨 **Descartado porque no
     arregla el problema: suma 26 s.** Se comprobó antes de aplicarlo, en vez de
     copiarlo. La auditoría lo sabía —decía *"o mejor: fase por fase"*—, pero la
     línea que alguien copia es la primera que se lee.
  2. **Bajar el escalar a 2,5**, para que 4 × 2,5 = 10. Descartado: ata cuatro
     fases con naturalezas distintas al mismo número, y deja `read` —donde se
     tarda de verdad— tan apretado como `connect`.

- 🔑 **`TIMEOUT_SECONDS` cambia de papel, y conviene tenerlo claro.** Deja de ser
  *"lo que se le pasa al SDK"* y pasa a ser **el presupuesto total**. Sigue
  sirviendo para lo único para lo que se usaba: compararlo con los 10 s de la
  ruta.

  🚨 **Y esa comparación sola ya no basta.** `TIMEOUT_SECONDS` podría quedarse en
  8 mientras las fases suman 32, y
  `test_the_client_timeout_is_shorter_than_the_one_in_the_api` seguiría en verde
  afirmando algo falso — que es exactamente lo que pasó media jornada. Lo que ata
  las dos cosas es el test nuevo,
  `test_the_timeout_is_split_by_phase_and_the_parts_add_up_to_the_budget`, y
  **vigila la SUMA**, no que haya cuatro números.

  ✅ Se vio morder con el one-liner descartado: `assert 26.0 == 8.0`.

- **Por qué `anthropic.Timeout` y no `httpx.Timeout`**, siendo **el mismo tipo**
  (`anthropic.Timeout is httpx.Timeout` → `True`, comprobado): `anthropic` está
  fijado en `requirements.txt` y `httpx` entra de rebote con él. Importar
  directamente lo que no se fija es la trampa de `[L-047]` con el 40 de `anyio`.

- **⚠️ Lo que esta decisión NO consigue, y hay que leerlo antes de citarla:**
  - **Sigue sin ser un techo duro.** `httpcore` aplica el `read` a **cada lectura
    del socket**, no al cuerpo entero: una respuesta en muchos trozos, cada uno
    por debajo de 4 s, puede sumar más de 4. Con `MAX_TOKENS = 1000` el riesgo es
    bajo, no nulo.
  - 🔑 **Por eso los 10 s de la ruta no sobran: son la única garantía de reloj de
    pared que existe.** Es el argumento correcto para conservarlos, y no el que
    `[D-070]` escribió.
  - **`read = 4,0` es más ajustado que el 8,0 de antes.** Si el 4,72 s de
    `[L-043]` reaparece entre el primer byte y el último, esto corta un veredicto
    que antes llegaba. El síntoma sería `APITimeoutError` donde había respuesta.
    Es deliberado —un presupuesto que no se puede rebasar vale más que uno holgado
    que miente—, pero si pasa, se sube `read` y se baja otra.

- **Toca:** `app/tools.py` (`TIMEOUT` nuevo, `TIMEOUT_SECONDS` cambia de papel),
  `tests/test_tools.py` (un test nuevo, dos actualizados), `measure_tutor.py`
  (construye su cliente con `tools.TIMEOUT` para seguir midiendo el camino real,
  e imprime las cuatro fases en vez del total), `[A-011]`.

### [D-070] 2026-08-13 — El timeout de la ruta se queda en 10 s (y el cierre de `[A-011]` se cae)

🔴 **ENMENDADA el 2026-08-13, horas después de escribirse, por auditoría
externa.** Lo que sobrevive y lo que no:

| pieza de esta decisión | estado |
|---|---|
| `TUTOR_TIMEOUT_SECONDS` se queda en **10,0** | ✅ **sigue en pie**, y ahora con más razón |
| No bajarlo por debajo de los 8,0 | ✅ sigue en pie |
| No retirarlo (se lleva el reembolso) | ⚠️ en pie, pero ver la contradicción de abajo |
| Los 56,3 ms de trabajo local | ✅ medidos, sólidos, no dependen de la red |
| *"El cliente corta a los 8,0 s pase lo que pase"* | 🔴 **FALSO** |
| *"Una práctica tiene techo de 8,06 s"* | 🔴 **FALSO**, se apoyaba en lo anterior |
| *"Sobran ~1 944 ms"* | 🔴 **FALSO**, misma raíz |
| **`[A-011]` muere** | 🔴 **REVERTIDO — está reabierta** |

🚨 **La raíz: `timeout=8.0` no es un tope.** `httpx` lo reparte a cuatro fases
con cronómetro independiente (`connect`, `read`, `write`, `pool`), **32 s de
suma**. El comando que lo mide, la consecuencia en producción y el arreglo
propuesto están en `[A-011]`, que es donde vive el problema ahora.

📌 **Y la premisa se heredó, no se inventó aquí:** venía de `[L-045]` y
`[L-043]`. Nadie la recomprobó porque ya estaba escrita en dos sitios.

✅ **Contradicción RESUELTA el mismo día, y con una corrida.** Esta entrada usaba
como carga dos cosas incompatibles: *"el reembolso vive dentro del `except`"* y
*"la cola no se forma, por construcción"*. Si la segunda fuera cierta, la tarea
siempre arrancaría, `attempt.cancel()` devolvería siempre `False` y el reembolso
sería código muerto.

🔴 **La falsa es la segunda.** Un 504 devuelve el control a quien preguntó y
**suelta su ficha de `anyio`**, pero deja a `respond` corriendo en el hilo del
pool: el sitio **no** se libera. El emparejamiento «una petición viva = un sitio
del pool» se rompe, y los zombis llenan el pool con menos de 40 vivas.

Demostrado con peticiones **secuenciales** —nunca dos vivas a la vez— en
`test_a_timed_out_tutor_keeps_its_pool_seat_with_nobody_waiting`. Se vio morder.
Detalle completo en `[L-056]`.

⇒ **El reembolso NO es código muerto**, así que el argumento «retirarlo se lleva
el reembolso» **se sostiene**. Y el invariante de `TUTOR_POOL_SIZE` deja de valer
como carga: su comentario en `app/api.py` está corregido.

⚠️ **Lo que sigue debajo es el texto ORIGINAL, sin tocar**, para que se vea de
qué se partía. Léelo con la tabla de arriba delante.

🚨 **Y sus punteros de línea están MUERTOS — los mató este mismo commit.** El
texto original citaba `app/tools.py:83`, `app/api.py:698` y `app/api.py:146`;
esas líneas se escribieron **antes** de editar los archivos, y las ediciones las
desplazaron. Releídos contra el árbol ya escrito:

| lo que dice el texto original | dónde está de verdad |
|---|---|
| `app/tools.py:83` (el `8.0`) | `app/tools.py:108` |
| `app/api.py:146` (el `10.0`) | `app/api.py:162` |
| `app/api.py:698` (`attempt.cancel()`) | `app/api.py:714` |

🧭 **Regla que sale de aquí, y vale para toda entrada futura: los punteros de
línea se releen AL FINAL, contra el árbol ya escrito — nunca durante la
edición.** El desfase de cada archivo era exactamente cuántas líneas insertó el
commit en él, y el único puntero correcto apuntaba al único archivo que el
commit no tocó. No es descuido: es un modo de fallo del procedimiento. Por eso
la enmienda de arriba cita **nombres de símbolo** (`_TUTOR_POOL`), no números.

---

- **Se eligió:** **dejar `TUTOR_TIMEOUT_SECONDS = 10.0` tal cual**, y cerrar
  `[A-011]` — que llevaba abierta desde el 2026-08-04 y ya se había cerrado mal
  una vez (`[L-043]`).
- **Contra:**
  1. **Bajarlo por debajo de los 8,0 s del cliente** para que muerda de verdad.
  2. **Retirarlo**, escribiendo por qué no hacía falta.

  Las dos las nombró `[L-045]` como las únicas salidas vivas. Las dos se
  descartan abajo, con motivo.

- **De dónde sale:** de la mitad de arriba de `T-079`, que `[L-045]` dejó
  reformulada: *"si el freno no puede disparar, lo que queda es decidir qué se
  hace con él"*. Y de una pregunta del usuario —*"¿qué implica bajarlo y qué
  implica retirarlo?"*— que obligó a mirar el código en vez de recordarlo.

- **La medida que lo cierra, y lo primero es que fue GRATIS.** `[L-045]` ya había
  acotado por lectura el único hueco que quedaba:

  > *"Los 10 s no pueden disparar por modelo lento (corta el cliente antes) ni
  > por cola (la cola no se forma, por construcción). La única rendija que queda
  > es que `respond()` fuera del modelo —`count_words` y `add_point`, que escribe
  > en disco con candado— se coma más de 2 s."*

  Esa rendija se cronometró con `measure_local_parts.py`, cinco corridas:

  | pieza | peor caso | cómo |
  |---|---|---|
  | `count_words` | **0,007 ms** | n=1000 |
  | `record_practice`, sin competencia | **2,4 ms** | n=50 |
  | `record_practice`, **40 hilos, mismo archivo** | **56,3 ms** | 5 corridas, peor de todas |

  **56,3 ms contra 2 000 ms de presupuesto: 35× de margen.**

  🔑 **Y la contención se provocó quitando sitio, no añadiendo carga** — la regla
  de `[L-045]`. Cuarenta hilos sobre **el mismo archivo** es lo que hace que el
  candado los ponga en fila; con un archivo por persona habría salido el caso
  feliz disfrazado de peor caso.

- **Por qué se queda, y no es "por si acaso":**

  - 🔑 **El cierre se apoya en un TECHO IMPUESTO, que es más fuerte que una
    medida.** `judge_grammar` no puede pasar de 8,0 s porque el cliente de
    Anthropic no la deja (`app/tools.py:83`), no porque se haya observado que
    tarda menos. Sumado a los 56 ms locales, **una práctica entera tiene tope de
    8,06 s**. El reloj de la ruta no puede morder por nada de lo que hay dentro
    de él. Eso no depende de cuántas muestras se tomen.

    📌 **Y es la diferencia exacta con el cierre fallido de `[L-043]`.** Aquel
    restaba `10 − 4,72` de una medida —*"la peor de diez"*, n=1, dispersión
    2,7×—; este resta de un techo que el código impone. Una observación se puede
    superar mañana; un techo no.

  - 🚨 **Es lo único que libera a quien pregunta.** Python no sabe matar un hilo:
    lo que este freno corta es la espera de quien llamó, no el trabajo. Si
    `respond()` se colgara en algo que **no es la llamada al modelo**, el timeout
    del cliente no lo cubre — ese solo vigila el modelo.

  - 🚨 **Y el reembolso vive DENTRO de ese `except`.** `never_started =
    attempt.cancel()` (`app/api.py:698`) es lo que decide si se devuelve la
    práctica. Sin timeout no hay `except`, y no hay devolución. Retirarlo no
    quita un reloj: quita una regla de dinero.

  - ⚠️ **El invariante que sostiene "no hay cola" es prestado.** El 40 del pool
    iguala las 40 fichas de `anyio`, que es **un defecto de una librería que no
    fijamos** (`app/api.py:176`). Si cambiara, la cola vuelve — y esos 1 944 ms
    son lo único que la frena. El freno se queda **porque** su justificación
    cuelga de algo ajeno. Lo vigila
    `test_the_pool_matches_the_threads_fastapi_actually_uses`.

- **Por qué NO se baja:** invertiría el orden de los dos relojes. Hoy el cliente
  se rinde primero **a propósito**, para que suba el error de verdad de Anthropic
  —un 429, una llave mala— en vez de un 504 genérico que lo esconde. Hay un test
  que lo vigila: `test_the_client_timeout_is_shorter_than_the_one_in_the_api`
  (`tests/test_tools.py:270`). Bajarlo lo pone rojo, y con razón.

- **⚠️ Lo que esta decisión NO dice, escrito para que nadie la estire:**
  - Los 56 ms salen de **la máquina de desarrollo, en Windows**, no del servidor
    de AWS. Otro disco da otro número. Lo que aguanta el traslado no es el 56: es
    que para comerse el margen el disco tendría que ser **35× más lento**.
  - **La cola sigue sin cronometrarse.** No hace falta para esta decisión —el
    invariante la descarta y un test lo vigila—, pero si alguien sube el pool sin
    subir `anyio`, esto hay que volver a abrirlo.

- **Toca:** `app/api.py:146` (el número se queda, el comentario pierde el *"sigue
  siendo una predicción"*), `measure_local_parts.py` y
  `tests/test_measure_local_parts.py` (nuevos), `_persistence/assumptions.md`
  (`[A-011]` sale), `T-079` (se cierra su mitad de arriba).

### [D-069] 2026-08-13 — El formato de la primera línea funciona con el modelo real

- **Qué se comprobó:** que Opus 5 obedece la rúbrica de `[D-067]` y abre su
  respuesta con `OK` o `FIX`. Era `[A-028]`, escrita esta misma sesión, y ha
  resultado **cierta**.
- **Corrida 1 — por guion.** Servidor local, cuenta `probe-format`, tres
  prácticas seguidas contra la API de verdad:

  | frase | correcta | `score` | `practice` |
  |---|---|---|---|
  | `I like coffee` | sí | 1 | 1 |
  | `I cooking in these morning` | no | 1 | 2 |
  | `me likes coffees` | no | 1 | 3 |

  Al terminar quedó `{"score": 1, "practice": 3}` en `probe-format.json`.

  🚨 **Ese archivo YA NO EXISTE, y hay que decirlo aquí o esta entrada miente.**
  `probe-format` era una cuenta desechable creada para esta comprobación, y se
  borró —cuenta y marcador— al acabar. Quien lea esto mañana, vaya al disco y
  busque el `practice: 3` **no lo va a encontrar**, y sin este párrafo concluiría
  que la entrada se inventó los números. Lo detectó la auditoría del 2026-08-13.
  🔑 **Un dato borrado no es un dato ausente: es un dato que hay que declarar
  muerto donde se citó.**
- **Por qué la primera frase era la que decidía:** una frase mala da `score 0`
  tanto si el formato funciona como si no. **Solo una frase buena distingue las
  dos cosas**, y por eso se empezó por `I like coffee`.
- 📌 **Y la segunda cierra el círculo.** `I cooking in these morning` es
  literalmente la frase que el 2026-08-13 sumó punto estando mal, y que mató a
  `[A-001]`. Hoy, con el mismo texto, `score` no se movió.
- 🔑 **Los tres veredictos llegaron limpios**, sin `OK` ni `FIX` a la vista: el
  recorte de `split_verdict` funciona contra texto real, no solo contra las
  cadenas escritas a mano de los tests.
- ✅ **Corrida 2 — desde el NAVEGADOR**, por quien construye, el mismo día y sin
  guion de por medio. Cuenta `jorge`, local: `I like coffee in the morning`
  (correcta) → `Words 6, Score 1, Practice 1`; `I cook chicken yesterday with my
  girlfriend` (mala) → `Words 7, Score 1, Practice 2`. Es PI-4 cumplido donde hay
  pantalla: corrida, no deducida.

  📌 **Esta es la que SÍ se puede ir a mirar:** `data/users/jorge.json` →
  `{"score": 1, "practice": 2}`. Es el único archivo de las dos corridas que
  sobrevivió, y es el que vale como respaldo comprobable.
- ⚠️ **Lo que esto NO demuestra.** **Cinco llamadas** —3 de la corrida 1 y 2 de
  la corrida 2, todas locales— no garantizan el formato para siempre: es texto
  generado. Lo que sí hay es un síntoma reconocible si algún día se rompe —
  **`Score` clavado en 0 mientras `Practice` sube**. Queda escrito aquí porque es
  lo que nadie sabría interpretar dentro de tres meses.
- 📌 **Una desviación menor, anotada para el paso 9 y no arreglada hoy:** la
  rúbrica pide *"no quotation marks"* y el modelo entrecomilló la frase del
  aprendiz igualmente. No toca al formato de la primera línea —que es lo que
  sostiene `[D-066]`— así que no se cambia nada ahora; es material de las evals
  con rúbrica del paso 9, que es donde se mide la obediencia fina.
- **Toca:** `[D-067]`, `[D-066]`, `[A-028]` (que muere aquí), `T-019`.

### [D-068] 2026-08-13 — Los marcadores viejos se borran; no se migran

- **Se eligió:** **borrar** los archivos de `data/users/` —la máquina local y el
  servidor— y empezar de cero. Y que `read_counters` **exija** la clave
  `practice`, igual que ya exigía `score`.
- **Contra:**
  1. **Pasar el número viejo a `practice` y dejar `score` en 0.** Lo único
     literalmente cierto —sabemos cuántas veces practicó, no cuántas acertó—
     pero el marcador visible cae a cero.
  2. **Dejar `score` como estaba y copiar el número a `practice`.** No pierde
     nada, pero afirma que todas fueron aciertos, y se sabe que al menos una no
     lo fue (`I cooking in these morning`, 2026-08-13).
- **Por qué:**
  - 🔑 **El número viejo cambió de unidad.** Con la regla anterior `score`
    contaba **prácticas**; con `[D-066]` cuenta **aciertos**. Es la misma cifra
    queriendo decir dos cosas, y cualquier migración tiene que inventarse la
    mitad que nunca se midió. Un dato inventado que parece medido es peor que no
    tener dato.
  - **Se pudo elegir la salida limpia porque no hay nadie a quien perjudicar:**
    los archivos son de **un día de pruebas del propio autor**, no de alumnos
    reales. Con usuarios de verdad esta decisión habría sido otra.
- ⚠️ **Exigir la clave `practice` es la parte que protege, y es deliberada.** Si
  algún archivo viejo sobrevive al borrado —uno olvidado en el servidor—, saldrá
  un `ScoreFileError` que se lee, en vez de un contador a 0 que nadie cuestiona.
  Es la misma regla que ya defendía `read_score`: *"devolver 0 en silencio sería
  decirle 'tienes cero puntos' a alguien que tenía seis."* **Ausente y roto no
  son lo mismo**, y aquí un archivo viejo está roto.
- **Toca:** `app/tools.py` (`read_counters`), `data/users/` en local y en el
  servidor, `[D-066]`.

### [D-067] 2026-08-13 — El veredicto viaja en una primera línea fija, no en salida estructurada

- **Se eligió:** que `GRAMMAR_RUBRIC` pida al modelo abrir su respuesta con una
  **primera línea de una sola palabra** —`OK` si la frase está bien, `FIX` si
  no—, seguida del mensaje cálido de siempre. `judge_grammar` lee esa línea, la
  **recorta**, y devuelve el veredicto y el texto por separado. Quien muestre
  la respuesta nunca ve la palabra clave.
- **Contra:** pedirle al SDK una **respuesta estructurada** (que el modelo
  rellene un esquema con un campo booleano y otro de texto). Es más robusto:
  el formato lo garantiza la API, no la buena voluntad del modelo.
- **Por qué:**
  - **Se puede leer entero.** El texto crudo que devuelve Anthropic se imprime
    y se entiende de un vistazo. Si el modelo se salta el formato, **se ve**.
    Con salida estructurada, cuando algo falla hay que depurar una pieza de la
    API que aún no se ha usado nunca en este proyecto.
  - **PI-2:** no mete una pieza nueva de la API para un problema que una línea
    de texto resuelve. El paso 8 va de enchufar el modelo, no de estrenar
    funciones del SDK.
  - **Es reversible.** Si el formato falla demasiado en la práctica, cambiar a
    salida estructurada toca `GRAMMAR_RUBRIC` y el trozo que parte la respuesta
    — no toca `respond`, ni la pantalla, ni el marcador.
- ⚠️ **El riesgo asumido, escrito:** el modelo **puede** no poner la línea. No
  es hipotético — es texto generado, no un contrato. Se resuelve **denegando
  por defecto** (regla 3): si la primera línea no es exactamente `OK`, no hay
  punto. Equivocarse así cuesta un punto no sumado; al revés, regalaría
  aciertos y el marcador dejaría de significar nada.
- **Toca:** `app/tools.py` (`GRAMMAR_RUBRIC` y `judge_grammar`), `[D-066]`.

### [D-066] 2026-08-13 — El marcador cuenta aciertos, y los intentos van en un contador aparte

- **Se eligió:** `score` sube **solo si la frase está bien**. Y se añade
  **`practice`**, un contador nuevo que sube en **cada** práctica con veredicto.
  Quedan tres piezas, cada una midiendo una cosa: `words` (palabras de la frase,
  no acumula), `score` (aciertos), `practice` (intentos).
- **Contra:**
  1. Dejarlo como estaba —`score` sube siempre—, que es lo que suponía
     `[A-001]` y lo que el código hace hoy en `english_tutor.py:82`.
  2. Cambiar `score` a aciertos **sin** añadir `practice`.
- **Por qué:**
  - 📊 **`[A-001]` era falsa, y se comprobó sin buscarlo.** Llevaba abierta
    desde el 2026-08-02 con una prueba escrita: *"en el paso 8, con el modelo
    enchufado, escribir una frase claramente incorrecta y mirar el marcador."*
    El 2026-08-13, en la primera práctica real desde el navegador, se escribió
    `I cooking in these morning` —incorrecta— y **el marcador subió igual**. La
    prueba corrió sola. Solo faltaba mirar el resultado y decidir.
  - **`practice` desactiva la única objeción que `[A-001]` dejó por escrito:**
    que un marcador que solo sube al acertar *"castiga justo a quien más se
    está esforzando"*. Con los dos contadores, quien falla ve `3 de 10` en vez
    de un cero: el esfuerzo tiene su propio sitio y el acierto no se diluye.
  - **El almacenamiento ya lo aguanta.** El archivo de cada persona es un
    diccionario (`read_score` exige la clave `"score"`), no un número suelto:
    `practice` es una clave más, no un formato nuevo.
  - 🚨 **Y ahora es más barato que después.** El paso 9 son evals con rúbrica, y
    una rúbrica califica **contra** lo que el marcador significa. Decidirlo
    después obligaría a reescribir las evals recién hechas. Lo avisaba la propia
    `[A-001]`: *"el coste de equivocarse crece con el tiempo."*
- ⚠️ **Lo que arrastra, dicho antes de empezar:**
  - `judge_grammar` devuelve hoy `str` —texto libre— y **nada dentro de esa
    cadena le dice a `respond` si la frase estaba bien**. El contrato cambia.
    El cómo es `[D-067]`.
  - **Hay archivos reales en el servidor desde el 2026-08-13**, escritos sin la
    clave `practice`. Si `read_score` la exige, el marcador de gente real pasa a
    estar "roto". Se trata **ausente como 0**, igual que ya se hace cuando no
    existe el archivo entero.
  - `[D-050]` **no cambia**: si no hubo veredicto, no sube nada — ni `score` ni
    `practice`. Una práctica sin veredicto no ocurrió.
- 📌 **`[A-001]` murió con DOS destinos, y aquí solo se cumplió uno.** Su propia
  regla decía *"si sube y chirría → era falsa. Sale de aquí y entra en
  `lessons.md`"*. La decisión vino aquí, que era necesario; la **lección** no se
  escribió hasta que la auditoría del mismo día la reclamó. Vive en `[L-052]`, y
  es lo más valioso que dejó: **un maniquí no solo tapa fallos, congela
  decisiones, y las devuelve el día caro.**
- **Toca:** `app/tools.py`, `app/english_tutor.py`, `app/api.py`, la pantalla,
  `[A-001]` (que muere aquí), `[D-050]`, `[L-052]`, `T-019`.

### [D-065] 2026-08-13 — Producción tiene llave propia, y se crea antes de desplegar

**Qué se decidió.** Antes de correr `install.sh` con la llave, se crea en el
espacio `Default` una llave nueva **con nombre propio, `teapp-server`**, que solo
use el servidor. Esa es la que viaja. La que pasó la corrida B de `[D-063]` **no**
se manda.

**Contra qué se decidió.** Contra mandar hoy la que ya pasó el examen —que era el
camino corto y estaba a un paso— y arreglarlo después.

**Por qué. `[A-027]` se comprobó y salió FALSA, con nombre y apellido.** La
suposición decía *"algo usa esa llave y no sabemos qué"*. Ya se sabe: **el
repositorio del curso**. Medido el 2026-08-13 sobre `Edu_TripleS`, excluyendo
`.venv`:

| medida | número |
|---|---|
| archivos `.py` que cargan ese `.env` (`load_dotenv`) | **21** |
| archivos `.py` que nombran `ANTHROPIC_API_KEY` directamente | 2 |
| niveles implicados | **8** — `00-setup` … `06b-memoria-skills` |

🚨 **El enunciado empeora al concretarse.** No es "alguien podría revocarla". Es
que producción compartiría la llave con un repositorio de enseñanza donde se
corren ejemplos a diario. El día que se rote por un motivo del curso —un
ejercicio que la imprima, una sesión que la regenere— **se cae la app**, y el
síntoma le llega a una persona practicando inglés mientras la causa está en otro
repositorio. Nadie relaciona las dos cosas.

**🔑 Y el orden dejó de ser una preferencia: lo decide `install.sh`.** Líneas
89-95, la regla de `[D-063]`:

```
==> El .env ya tiene ANTHROPIC_API_KEY: no se toca ([D-063])
    Aviso: se IGNORA la ANTHROPIC_API_KEY del entorno.
```

Una llave ya escrita **no se pisa nunca**. Es la regla correcta —protege de dejar
una llave mala clavada— pero tiene un precio hoy: escribir la provisional
**no es un paso reversible barato**. Cambiarla mañana no sería volver a correr el
guion; sería editar el archivo a mano por SSH en la máquina viva, un camino que
no está escrito, no tiene tests y no ha corrido nadie.

📌 **Lo barato va primero, entonces.** Crear la llave cuesta minutos en la
consola y **$0**. Correr `install.sh` exige encender la EC2 y es el paso grande.
En este orden no se pierde nada; al revés, sí.

**⚠️ Condición al crearla, y es `[L-047]` con un tercer consumidor.** El límite
de peticiones por minuto de `teapp-server` **no puede ser 50**. Ese 50 es la
firma del laboratorio en `check_api_key.py:LAB_REQUESTS_PER_MINUTE`
(`[D-061]`). Si el espacio nuevo lo hereda por copiar la configuración del de
medir, el portero **abortaría el despliegue acusando a la llave buena de ser la
del laboratorio** — un rojo falso, y de los que dan la razón a quien quiera
quitar el freno. Se comprueba el número antes de correr nada.

**Lo que NO cambia.** La llave nueva sale del **mismo saldo de $6,55**. Un nombre
propio separa *quién gasta*, no abre un bolsillo (`[D-059]`). Y de regalo deja
las tres llaves viejas de `Default` revocables sin miedo, porque por fin se sabrá
cuál hace qué.

✅ **`teapp-server` creada y COMPROBADA el 2026-08-13 a las 13:57 UTC —
`T-087` cerrada.** `check_api_key.py` con esa llave: **salida `0`**,
`requests-limit=1000`. Identidad fuerte: la creó el usuario en `Default` mirando
la consola, no se dedujo del orden de uso.

📌 **Y de paso quedó medido el episodio de saturación**, que es el dato que
`[L-046]` no tenía: la misma llave dio **diez `529` entre las 13:36 y las 13:46
UTC** y pasó limpia a las 13:57. **El episodio duró entre 9 y 19 minutos**, no
los ~50 segundos del primero. La sonda que lo declaró terminado fue la llave del
laboratorio —que a las 13:55 volvió a dar `3`— y no un reintento a ciegas con la
llave que se quería probar: el mismo control al lado que separó las dos causas
por la mañana.

⚠️ **Lo que esto NO cierra:** `check_api_key.py` sabe que esta llave no es la del
laboratorio. **No sabe que sea `teapp-server`** — el freno es por espacio de
trabajo, así que la llave del curso responde `1000` igual. Lo que separa a
`teapp-server` de la del curso es el **nombre en la consola**, no el portero.

- **Toca:** `T-078`, `T-087`, `deploy/install.sh`, `deploy/check_api_key.py`,
  `[A-027]` (muerta aquí), `[D-063]`, `[D-061]`, `[D-059]`, `[L-046]`, `[L-047]`.

### [D-064] 2026-08-12 — La terminal de auditoría sí corre la suite, y el disparador se mira en presente

- **Qué se decidió:** la terminal que audita **puede correr `pytest -q`**, con un
  disparador y dos obligaciones:

  | | regla |
  |---|---|
  | **cuándo** | siempre que vaya a **escribir o citar** un número de la suite |
  | **si no la corre** | **no puede afirmar el estado de la suite, ni en vago** |
  | **al correrla** | **registra el commit** sobre el que corrió |

- **Contra qué:** que no ejecute nada (la línea de la sesión 59), y contra el
  disparador alternativo *"correr solo cuando el número sostenga una decisión"*.
- **Fecha:** 2026-08-12. Cierra una pregunta de reparto abierta desde la sesión
  59 (`PROGRESO.md`, líneas 862–867).

**Por qué se abre la puerta.** Una terminal que audita y no puede medir solo sabe
**releer**. Releer caza un razonamiento torcido —hoy cazó tres, uno de ellos el
flanco de las 26 corridas de `[D-062]`, que estaba mal razonado por mi lado— pero
**no caza un número**. Un número solo lo caza una corrida: en la sesión 51,
correr la suite aquí destapó un **342 que eran 348**, escrito con toda la
confianza del mundo. 🔑 **Es la regla 6 aplicada al auditor: gana el
instrumento, no la lista.** Y el riesgo es ninguno — es lectura sobre este repo,
no toca la nube, no gasta un céntimo, y `conftest.py` más los porteros de
`tests/` garantizan que una corrida no escriba en `data/` de verdad (`[D-037]`).

**🔑 Por qué gana este disparador y no el otro, que es la parte transferible.**
*"Cuando el número sostenga una decisión"* obliga a **predecir el futuro**: si
este número acabará importando no se sabe al escribirlo, se sabe después. Y una
regla que exige adivinar **se resuelve siempre del lado cómodo**, porque el lado
cómodo es el que no obliga a hacer nada ahora. *"Cuando vaya a teclear un número
de la suite"* se contesta mirando el presente: sí o no, ahora, sin juicio.

> 📌 **Un disparador que se comprueba observando lo que haces vale más que uno
> que se comprueba estimando lo que importará.** Misma familia que el
> `CallBudget` de `[D-060]`, que cobra **antes** de llamar, y que el
> `install -m 600` de `deploy/install.sh:168`, que cierra el archivo **antes** de
> que tenga nada dentro: en los tres, el momento en que la regla muerde lo fija
> la **mecánica**, no el criterio de alguien.

**🚨 Remate 1: la regla trae su propia escapatoria, y se cierra aquí.** *"Correr
si vas a escribir el número"* tiene una salida cómoda — **no escribir el
número**. Decir *"la suite pasa"* en vez de *"410 pasan"* cumple la letra y
esquiva la corrida. Por eso la otra mitad: **si no se corrió, no se puede
afirmar el estado de la suite ni en vago**. Solo hay dos formas legales de
nombrarla:

- **medido aquí**, con su número; o
- **reportado por la otra terminal, no verificado**, dicho con esas palabras.

Nunca una afirmación sin etiqueta. Es la honradez del `session-closer` de la
sesión 55 —*"reportado, no visto"*— aplicada al otro lado.

**🚨 Remate 2: un número solo se compara contra el mismo commit.** Si la auditoría
corre y le sale distinto, **la primera hipótesis no es que el otro mienta: es que
corrió otro árbol** — cambios sin commitear del otro lado, otro entorno virtual,
o estar parada en un commit anterior. Hoy pasó la versión conceptual de esto: se
reconstruyó un peligro que `install.sh` **ya tenía resuelto**, por leer el
comentario y no el código. En la sesión 51 el desacuerdo sí señaló al culpable
**porque el árbol estaba sincronizado**. Sin commit anotado, un desacuerdo de
números no dice quién se equivocó.

📌 **Estado de hoy bajo esta regla, para estrenarla con el ejemplo:** los **410**
son **medidos por la terminal que construye**, sobre `d4c40eb`. Para la terminal
que audita son **reportados, no verificados**.

- **Toca:** el reparto de trabajo entre las dos terminales, `PROGRESO.md`
  (líneas 862–867), regla 6, `[D-037]`, `[D-060]`, `tests/conftest.py`.

### [D-063] 2026-08-12 — La llave viaja por variable de entorno, y el guion la interroga antes de escribirla

- **Qué se decidió:** cómo `ANTHROPIC_API_KEY` llega al servidor en `T-078`.
  Cuatro piezas, y las cuatro hacen falta: **entra por variable de entorno**, el
  guion **comprueba de quién es la llave ANTES de escribirla**, **nunca pisa** una
  que ya tenga valor, y **falla ruidosamente** si al terminar sigue vacía.
- **Contra qué:** pasarla como argumento; rellenar sin comprobar; y terminar en
  verde con la línea vacía, que era el comportamiento de hoy.
- **Fecha:** 2026-08-12, decidido con la terminal de auditoría.

**1. Cómo entra: variable de entorno, no argumento — y no se reinventa.**
Es el patrón que ya está construido y probado en `create_account.py:44`, cuyo
`main(argv, environ)` toma el nombre por argumento y **la contraseña por
`environ`** (línea 55); `tests/test_create_account.py:93` **rechaza** el segundo
argumento porque *"casi siempre es la contraseña puesta como argumento por
error"*. Un argumento queda en el historial del shell y en la lista de procesos.

**2. Las tres reglas del `.env`:**

| situación | qué hace `install.sh` |
|---|---|
| línea vacía **y** llega la variable | la escribe |
| la línea **ya tiene valor** | **no la toca**, ni aunque venga la variable. Avisa de cómo cambiarla a mano |
| al terminar **sigue vacía** | **falla ruidosamente**, salida ≠ 0. No termina en verde |

🔑 **La tercera fila es la que hace valer a las otras dos.** Sin ella, "rellena si
está vacía" deja *vacía* como estado legal para siempre — y `T-078` existe justo
para que deje de serlo. Un operador que se olvide de aportar la llave tendría un
despliegue en verde, un servicio arrancado, y el fallo apareciendo en la primera
práctica de una persona real: `[C-008]` entrando por otra puerta. Es la misma
forma de `[D-037]` (sin `TEAPP_DATA_DIR`, la app no arranca). 📌 El reparto del
olvido queda del lado correcto (`[D-045]`): olvidarse cuesta **un trabajo a
mano**; lo contrario cuesta **producción degradada en silencio**.

**3. La comprobación de identidad, y por qué va del revés de lo obvio.**
`[D-061]` dejó el único instrumento probado que distingue una llave de otra: una
llamada mínima devuelve las cabeceras del espacio (costó 14 tokens; antes se
descartaron tres instrumentos gratis que no distinguían nada, `[L-046]`).

> **La regla: abortar si `requests-limit` vale `50`** — esa es la firma del
> laboratorio. Cualquier otro valor pasa.

🔑 **Se deniega lo conocido-malo en vez de exigir lo conocido-bueno, y lo que lo
decide es de quién es cada número.** El `1.000` de `Default` es un dato heredado
que **no controlamos**, y `[D-061]` lo vio desmentirse en un solo día (la
documentación decía 2.000.000; la consola, otra cosa). Colgar el freno del
despliegue de un número que Anthropic puede mover mañana es fabricar un **rojo
falso con fecha desconocida** — y un freno que muerde en falso se acaba quitando,
llevándose la red entera. El `50` lo pusimos nosotros y está escrito.

**⚠️ Lo que se paga por dar la vuelta, escrito porque no es gratis:**

| comprobación | cómo falla | qué se ve |
|---|---|---|
| exigir el `1.000` | **rojo falso** — el despliegue se para con la llave buena | ruidoso, alguien mira |
| abortar con el `50` | **verde falso** — pasa la del laboratorio | **mudo**: el 429 dentro de tres semanas |

Se acepta el verde falso porque el riesgo real que se tapa es **exactamente uno**
—mandar la del laboratorio porque en el `.env` local se llama igual (`[D-061]`)—
y contra ese muerde igual de fuerte.

**🚨 Y el disparador del verde falso ya está predicho, por `[D-061]` y por
escrito:** *"cada modelo nuevo necesita su fila con su propia medida antes de la
primera tanda"*, con Haiku nombrado. O sea que `[D-061]` **dice hoy que ese 50 se
va a mover en el paso 9**. El día que suba a 80, la comprobación deja de
reconocer al laboratorio y no avisa de nada.

**Condición no opcional, por eso: el 50 pasa a vivir en DOS sitios.** Misma
familia de bicho que la sesión 33 — la misma cosa escrita en dos lugares
diciendo cosas contrarias, sin dar error. Se cierra por los dos lados:

- en `install.sh`, el número lleva encima **de dónde sale** (`[D-061]`) y **qué se
  rompe si se mueve** (el freno se queda mudo);
- en `[D-061]`, queda escrito que **cambiar el límite obliga a tocar
  `install.sh`**. El acoplamiento tiene que verse desde los dos lados, no desde
  uno.

**4. Dos mecánicas, y la primera puede arruinar todo lo demás.**

- 🚨 **La comprobación va ANTES de escribir.** Misma forma que el `CallBudget` de
  `[D-060]`, que cobra antes de llamar porque cobrar después significa que la
  llamada ya se pagó. Aquí: si se escribe primero y se comprueba después, la
  regla *"nunca pisar una que ya tenga valor"* **deja la llave mala clavada para
  siempre** — la regla que protege se convierte en la que impide el arreglo.
- **"Llave del laboratorio" y "no hubo red" salen por puertas distintas**, con
  códigos de salida y mensajes distintos. Si un corte de red devuelve el mismo
  error que la llave equivocada, el primero que despliegue con la red mala verá
  *"llave equivocada"* teniendo la buena — el rojo falso que se acaba de evitar,
  entrando por la ventana.

📌 **Fuera de alcance a propósito:** si la **app** debe negarse a arrancar con la
llave vacía es otra pregunta y merece su propia entrada. `install.sh` fallando
ruidosamente cubre el camino del despliegue; un `.env` editado a mano es un
camino distinto.

📌 **Verificado de paso, y era una falsa alarma:** la ventana entre escribir el
`.env` y cerrarlo **no existe**. `deploy/install.sh:168` hace
`install -m 600 -o … /dev/null "${ENV_FILE}"` — el archivo nace vacío y ya en
600, y el `cat >` de la 173 no toca permisos. El `chmod 600` de la 211 cierra el
**otro** camino, el del `.env` preexistente al que se le añade una línea. Dos
caminos, dos cierres. ⚠️ Pero el comentario que lo explica dedica cuatro líneas
al peligro y una a la solución, y **la del peligro va primero**: se leyó como
"aquí sigue habiendo una ventana". Un comentario que explica un peligro puede
leerse como que el peligro sigue vivo. Cuando se toque (`[PI-3]`, no hoy): que la
primera línea diga el **estado** y el riesgo baje a explicación.

**🚨 CONDICIÓN PARA CERRAR `T-078`, escrita aquí porque a la memoria no se le
confía.** Mismo mecanismo que `[D-059]` puso sobre la capa 1: no basta con que
exista, hay que **verla morder**. Aquí son **dos** puertas y **dos** llaves:

| puerta | con qué llave | qué tiene que verse |
|---|---|---|
| **3** — laboratorio | la de `teapp-measure` (la que hay hoy en el `.env` local) | que la reconozca y **se niegue** |
| **0** — correcta | la de `Default`, sacada de la consola el día de `T-078` | que **pase**, antes de que `install.sh` la use |

⚠️ **Por qué la puerta 3 sola no vale, y es el error que casi se cuela:** con la
llave del laboratorio **solo se puede salir por la 3**, así que un 3 es
compatible con dos mundos — que la comprobación leyera el `50` y lo
identificara, o que salga por 3 por otra razón y hoy acierte por casualidad. Sin
una llave que **no** sea la del laboratorio, el 3 no los distingue. 🔑 Es la
misma forma que `T-060b`: con nada escuchando en el 8000, *"cerrado"* sale igual
con el cortafuegos abierto que cerrado — hizo falta el **control al lado**. Aquí
el control es la llave de `Default`, y llega sola: el día de `T-078` hay que
sacarla de la consola de todos modos. Que pase por `check_api_key.py` **antes**
de que `install.sh` la escriba. Otros ~10 tokens.

📌 **Hasta que las dos puertas estén recorridas con llaves reales, `T-078` NO se
cierra**, por muchos tests en verde que haya. Los 15 tests nuevos prueban la
lógica **contra una Anthropic de mentira**: `ask_anthropic` —la única función que
toca la red— no se ha ejecutado nunca. ⚠️ Y la corrida no puede imprimir la
llave, ni un prefijo suyo (regla 7). ✏️ **ENMENDADA el 2026-08-13, después de
saltármela:** la regla pasa a ser **"los cuatro caracteres finales, solo en la
terminal, jamás en el repositorio"**. 4 de 108 no reconstruyen nada, y ese
puñado es el único instrumento que permite decir *cuál* llave es cuál cuando en
el `.env` se llaman igual — que es el problema entero de esta decisión. Se
enmienda en vez de dejar la desviación anotada debajo porque **una regla con
asterisco es una regla que ya no manda**: quien lea la norma leerá "ni un
prefijo" y quien lea el registro verá que se hizo igual. La versión de abajo
manda.

✅ **CONDICIÓN CUMPLIDA el 2026-08-13. Las dos puertas mordieron, con dos llaves
reales, contra la red de Anthropic.** `ask_anthropic` se ejecutó por primera vez.

| corrida | identidad — **de la consola, ANTES de correr** | salida | número impreso |
|---|---|---|---|
| A | la llave de `teapp-measure` (laboratorio) | `3` | `requests-limit=50` |
| B | la llave de `Default` de uso más reciente | `0` | `requests-limit=1000` |

🔑 **Lo que hace que estas dos corridas afirmen algo, y no es el resultado:** la
identidad de cada llave se leyó en la consola **antes** de correr el guion. Si se
hubiera averiguado preguntándole al guion, el examinado habría escrito su propio
examen y el verde habría salido igual sin saber nada — que es el fallo de
`T-060b` en su forma exacta. El control viene de fuera, como allí.

**Dos hipótesis murieron por el camino, y conviene que quede escrito:**

1. Se dio por cierto que la llave de `Default` se había quedado en el `.env` del
   repo del curso. **Falso:** las llaves de los dos `.env` locales no coinciden
   con la de uso reciente de `Default`. Nunca fue un dato, era una suposición
   heredada de un traspaso.
2. `Default` no tiene una llave: **tiene tres**, y de ninguna se conserva el
   valor — Anthropic la enseña una sola vez, al crearla. La corrida B fue posible
   solo porque el usuario tenía guardado el texto completo de una de ellas fuera
   del proyecto. Sin eso, la única salida era **crear** una llave nueva en
   `Default`; queda anotado como el camino de repuesto si esa llave se revoca.

**Camino de la llave en las dos corridas:** de un archivo fuera del repositorio
al **entorno del proceso**, nunca a un argumento, nunca a un archivo del
proyecto, nunca a la pantalla; el temporal se borró al terminar. Es el mismo
camino que hará `install.sh`.

⚠️ **Desviación propia, y cómo se resolvió.** Esta entrada exigía arriba *"la
corrida no puede imprimir la llave, ni un prefijo suyo"*, y al identificarlas se
imprimieron en la terminal el prefijo común `sk-ant-` y **los cuatro últimos
caracteres** de cada una. La regla se **enmendó** arriba en vez de dejar la
excepción escrita aquí: la práctica y la norma no pueden decir cosas distintas.
**En el repositorio no se escribe ningún final de llave** — por eso la tabla
nombra las llaves por su espacio de trabajo.

⚠️ **Y el identificador de la corrida B era más blando de lo que parecía.** Se
llamó *"la de uso más reciente"* de `Default`. Ese orden lo mueve cualquiera que
use el espacio — y `[D-065]` acaba de demostrar que el curso lo usa a diario, así
que "uso más reciente" podía estar apuntando a la llave del curso **por
construcción**. No invalida la corrida: lo que la B demuestra no es *"esta llave
concreta"* sino que **el cubo respondió 1000**, o sea espacio `Default`, que es
justo lo que el portero tiene que ver. Pero para el registro, la identidad fuerte
es el nombre en la consola o los cuatro caracteres finales, nunca el orden de
uso.

🚨 ~~Esto cierra la condición de `[D-063]`, NO cierra `T-078`.~~ ✅ **`T-078`
CERRADA el 2026-08-13, 14:04–14:08 UTC, en la máquina real.** El párrafo de
arriba se queda tachado y no borrado: describe correctamente el estado de la
mañana, y el salto de ahí a aquí es lo que hizo la tarde.

**Lo que se corrió, en orden:**

| tramo | evidencia |
|---|---|
| `git pull` en `/opt/teapp` | `afe2eab` → `699f2b2`, 36 commits — entró **todo el paso 8**, no solo la llave |
| `install.sh` | **código 0**. Portero ANTES de escribir: `==> Llave comprobada: requests-limit=1000, no es la del laboratorio` → `==> Escribiendo ANTHROPIC_API_KEY en el .env` |
| el `.env` resultante | `-rw------- ubuntu ubuntu` — permisos cerrados; llave de 108 caracteres, la de `teapp-server` |
| servicios | `teapp` y `caddy` `active`; app escuchando en `127.0.0.1:8000` |

**🔑 Y la prueba que de verdad cierra (PI-4), porque el archivo no demuestra
nada:** una práctica real desde el navegador. `I cooking in these morning` →
*"Almost! Say: I cooked this morning. The verb needs a past form: cooking becomes
cooked."* · Words: 5 · Score: 9. **Primera corrección real del proyecto.**

El rastro del otro lado, que es lo que la ata:

```
POST https://api.anthropic.com/v1/messages "HTTP/1.1 200 OK"
POST /practice HTTP/1.1  200 OK
data/quota → {"day": "2026-08-13", "used": 1}
data/users/jorge.json → {"score": 9}
```

Llamada facturada, cuota gastada (no devuelta: la petición sí salió), marcador
escrito. Las cuatro piezas de `[D-051]` y `[D-050]` funcionando juntas por
primera vez fuera de los tests.

**Cómo viajó la llave, que era media decisión de esta entrada.** `install.sh`
sugiere en su propio mensaje de error `sudo TEAPP_DOMAIN=... ANTHROPIC_API_KEY=...
bash …`, y eso **deja la llave en la línea de comandos**, visible en `ps` y en el
historial del shell. Se usó en su lugar: `stdin` → `read -r` → `export` →
`sudo -E`. Se comprobó antes, en la máquina, que `sudo -E` preserva el entorno
(no está garantizado: muchos `sudoers` lo deniegan). 📌 **Queda tarea:** el
mensaje de `install.sh` sigue recomendando la forma insegura.

⚠️ **`[L-033]` mordió durante el despliegue y estaba escrita.** El primer `ssh`
por nombre entró; los dos siguientes fallaron con `Could not resolve hostname`,
mientras `nslookup` y `socket.gethostbyname` resolvían al instante. Es el
resolvedor de esta terminal, no DuckDNS — cuarto episodio del día, y el primero
que le pega a `ssh` en vez de a `curl`. Se entró por la **IP fija**, que es lo
que `[L-033]` manda desde el 2026-08-09: *la IP es para SSH y solo para SSH*.

📌 **Falsa alarma anotada para que no se repita el susto:** en la salida de
`install.sh` aparece `curl: (7) Failed to connect to 127.0.0.1 port 8000` y el
guion sigue y termina en 0. No es un guardián mudo: `install.sh:452-463` es un
bucle de diez intentos con `exit 1` al final. Lo que se vio fue el intento 1
quejándose mientras la app terminaba de levantar.

- **Toca:** `deploy/install.sh`, `deploy/check_api_key.py`,
  `tests/test_check_api_key.py`, `T-078`, `[D-061]` (acoplamiento del 50),
  `[D-060]`, `[D-059]`, `[D-045]`, `[D-037]`, `[C-008]`, `create_account.py`,
  `T-060b`, paso 9.

### [D-062] 2026-08-12 — Al laboratorio se le pone techo mensual de $2, y no es una capa de protección

- **Qué se decidió:** el espacio `teapp-measure` lleva **tope de gasto propio de
  `$2,00` al mes**. Puesto y verificado en pantalla: *"Límite Mensual: USD 0,00
  de USD 2,00"*. Cierra `T-085` y el `📌 Sin decidir` que dejó abierto `[D-061]`.
- **Contra qué:** dejarlo sin tope (estado por defecto, que era lo que `[D-059]`
  había descartado por "reparto del mismo techo"), y contra ponerlo más alto.
- **Fecha:** 2026-08-12. Saldo de la organización leído ese día: **$6,48**.

**🚨 Lo primero, porque es lo que se lee al revés: esto NO protege el saldo.**
El tope de gasto es blando y con retraso (`[A-025]`), y la aritmética de los
números ya medidos dice cuánto retraso sobra:

| paso | de dónde | valor |
|---|---|---|
| techo físico de la báscula | `[D-061]`, `60 ÷ 1,72` | 35 llamadas/min |
| precio por llamada | `[D-058]`, medido | $0,00234 |
| gasto máximo por minuto | `35 × 0,00234` | **$0,082/min** |
| tiempo en vaciar el saldo entero | `6,48 ÷ 0,082` | **79 minutos** |
| ventana de reacción del tope | `[A-025]`, sin comprobar | **120 minutos** |

El saldo se vacía **41 minutos antes** de que el tope pueda mirar. Y si la
báscula se volviera concurrente, el freno de velocidad de 50/min lo deja en 55
minutos — peor. La conclusión aguanta las dos ramas. **Quien protege el saldo
sigue siendo el `CallBudget` de `[D-060]`, capa 1.** Este tope es contabilidad y
aviso.

**🔍 `[A-025]` se comprobó y salió muda, que no es lo mismo que salir falsa.**
Se abrió `Settings → Workspaces → Spend limits` como la propia suposición
prescribía. La pantalla dice *"El límite de gastos mensual de tu organización es
de $500,00. Puedes establecer un límite de gastos inferior a esta cantidad para
este espacio de trabajo"* — y **nada más**: ni `soft`, ni umbrales, ni retraso.
La consola de primera parte no se pronuncia. Así que `[A-025]` **se queda en
suposición** y la decisión se toma por su rama pesimista: lo que no se puede
comprobar no cuenta como freno.

**🔑 Por qué se pone igual: el corte no es contra un bucle, es una RESERVA.**
`Default` —donde vive el que sirve— no admite tope (`[D-059]`). A producción no
se le puede poner suelo directamente; el único suelo posible es indirecto,
capando al laboratorio. La pregunta útil no era *"¿cuánto puede gastar la
báscula?"* sino **"¿cuánto saldo se le reserva al que sirve?"**.

| | |
|---|---|
| saldo real | $6,48 |
| techo del laboratorio | $2,00 |
| **reservado para servir, SOLO frente a gasto LENTO** | **$4,48** = 1.914 prácticas ≈ **95 días** de una persona a tope (`[D-058]`) |
| **reservado frente a una corrida desbocada** | **nada.** Ahí no hay reserva, hay `CallBudget` (`[D-060]`) |

**⚠️ Lo que este tope muerde, con su alcance en la misma frase: el gasto
REPARTIDO en más de dos horas.** No las 26 corridas seguidas.

🔻 **Rectificado el mismo día, y el error estaba entre dos líneas de esta misma
entrada.** Se escribió que el tope cortaba el flanco de las 26 corridas de
`[D-060]` —el monedero se reinicia en cada arranque, `$6,48 ÷ $0,25 = 26`
corridas vacían el saldo— y se apuntó al lado el número: `26 × 106 × 1,72 s ≈ 79
min`. **Esos 79 minutos caen DENTRO de la ventana ciega de 120.** Por la misma
regla que se fija cuatro líneas más arriba —lo que no se puede comprobar no
cuenta como freno— el flanco **no queda cortado**: 26 corridas seguidas vacían el
saldo antes de que el tope se entere, exactamente igual que el bucle roto. Se vio
la coincidencia de los dos 79 y se sacó la conclusión contraria a la que el
número sostiene.

**Entonces el reparto verdadero queda así, y es lo único que hay que recordar:**

| forma de gastar | quién lo tapa |
|---|---|
| rápido (bucle roto, o corridas seguidas dentro de ~2 h) | **`CallBudget`** por corrida (`[D-060]`) — y contra corridas repetidas, **nadie**: ver `[A-026]` |
| lento (tandas repartidas en más de 2 h, uso a lo largo del mes) | **este tope de $2**, que ahí sí reserva de verdad |

Los **8 tandas al mes** (`2,00 ÷ 0,25`) son un techo **mensual**, no una defensa
contra una tarde intensa.

**El paso 9 cabe con holgura:** tres modelos (`claude-opus-5` actual, contra
Sonnet y contra Haiku), una tanda cada uno = **$0,75**. Quedan cinco tandas de
margen para repetir o reafinar. 📌 El `CallBudget` cobra siempre al precio de
Opus (`[D-060]`), así que las tandas de Sonnet y Haiku gastarán bastante menos de
$0,25: el freno se queda corto, nunca largo.

**🚨 Disparador escrito, porque los dos relojes no coinciden.** El tope es
**mensual y se reinicia**; el saldo es prepago y **no**. Tres meses seguidos a
tope son $6 de un saldo de $6,48 sin que el instrumento se haya pasado nunca:
diría que todo va bien mientras el bolsillo se vacía. Por eso el número está
elegido **contra los $6,48, no contra un mes**, y se vuelve a mirar en **cada
cambio de mes y en cada recarga de saldo** — misma familia de disparador que el
del límite de $500 en `[D-057]`.

- **Toca:** consola de Anthropic (espacio `teapp-measure`), `T-085` (cierra),
  `T-078` (le levanta el bloqueo), `[C-008]`, `[A-025]`, `[D-059]`, `[D-060]`,
  `[D-061]`, paso 9 (`[D-049]`), regla 5, regla 6.

### [D-061] 2026-08-12 — El laboratorio tiene espacio propio, y su freno es de velocidad

- **Qué se decidió:** existe el espacio de trabajo `teapp-measure` en la consola
  de Anthropic, y su límite de velocidad para `claude-opus-5` queda en:

  | columna | heredado de la organización | puesto en el espacio | fracción |
  |---|---|---|---|
  | solicitudes / min | 1.000 | **50** | 5% |
  | tokens de entrada / min | 500.000 | **20.000** | 4% |
  | tokens de salida / min | 80.000 | **5.000** | 6% |

- **Contra qué:** dejarlo heredado (que es el estado por defecto: *"si no se
  establece, los límites se heredarán de la organización"*), y contra buscar un
  tope de gasto por espacio, que `[D-059]` ya había descartado.
- **Fecha:** 2026-08-12, con `T-084` en la mano.

**De dónde salen los tres números.** Ninguno es redondo por gusto:

| paso | de dónde | valor |
|---|---|---|
| la báscula llama **de una en una** | `measure_tutor.py:208`, un `for` secuencial | — |
| la llamada más rápida de diez | `[A-011]`, medido | 1,72 s |
| techo físico de la báscula | `60 ÷ 1,72` | **35 llamadas/min** |
| tokens por llamada | `[D-058]`, medido | 247 entrada + 44 salida |
| a 35/min | multiplicación | ~8.650 y ~1.540 |

Los 50 / 20.000 / 5.000 son eso con ~1,4× de holgura. La holgura no es un adorno:
un límite que muerde en uso normal produce 429 del servidor de Anthropic, y con
`MAX_RETRIES = 0` (`app/tools.py:62`) eso llega como un fallo del tutor.

- 🚨 **La regla 6 mordió en directo, y por eso se preguntó antes de escribir.**
  La documentación pública dice que el nivel Start da a Opus 5 **2.000.000** de
  entrada y **400.000** de salida. La consola de **esta** cuenta dijo
  **1.000 / 500.000 / 80.000**. No coinciden.

  > 🔑 **Gana la consola.** Es el instrumento de la cuenta; la documentación es
  > una lista general. Haber escrito los números de la documentación habría
  > guardado un dato falso **con aspecto de verificado**, que es la forma más
  > cara de equivocarse en este repo.

- ✅ **Semántica confirmada en pantalla, no supuesta:** *"si se establece, se
  aplicarán tanto los límites del espacio de trabajo como los de la
  organización"*. **Se suman, no se sustituyen.** Y el espacio `Default` **no
  admite límites** por diseño de Anthropic — lo cual encaja con lo que queremos:
  al que sirve a personas no se le frena.

- ⚠️ **Lo que este freno NO hace, y confundirlo sería el error entero.** No
  protege el dinero. Un bucle roto **secuencial** tampoco pasaría de 35 llamadas
  por minuto, así que un tope de 50 no lo para. Quien protege el saldo es el
  `CallBudget` de `[D-060]`, con sus 106 llamadas por tanda.

  Lo que este freno protege es la **velocidad del servicio**: pase lo que pase en
  el laboratorio, a `Default` le quedan siempre el 95% de las peticiones libres.

- 🧭 **Trampa apuntada de antemano para el paso 9.** Las demás filas se dejan
  heredadas a propósito —`[PI-2]`: un límite para un modelo que todavía no se
  llama sería un número inventado, y no hay ni una medida de Sonnet ni de
  Haiku—. Pero Haiku 4.5 es mucho más rápido: si contesta en menos de un
  segundo, la báscula pasaría de 50/min **sin estar rota**.

  > 🚨 Recibirías 429, llegaría como fallo del tutor, y **medirías el límite que
  > tú pusiste creyendo que mides el modelo.** Cada modelo nuevo necesita su fila
  > con su propia medida **antes** de la primera tanda.

- ✅ **Verificado en vivo el 2026-08-12, y no por la vía fácil.** La llave nueva
  vive en el `.env` local bajo el mismo nombre de siempre, `ANTHROPIC_API_KEY`
  —sin variable nueva: `[PI-2]`, y el corte real no es *app contra báscula* sino
  **máquina contra producción**—. Que la del `.env` fuera **la nueva** y no la
  vieja de `Default` costó tres instrumentos descartados (`[L-046]`) y al final
  una llamada mínima leyendo las cabeceras:

  ```
  anthropic-ratelimit-requests-limit:      50
  anthropic-ratelimit-input-tokens-limit:  20000
  anthropic-ratelimit-output-tokens-limit: 5000
  anthropic-ratelimit-requests-remaining:  49
  ```

  > 🔑 Los tres coinciden con lo escrito en la consola, y `Default` habría dicho
  > `1.000 / 500.000 / 80.000`. **El `remaining: 49` es el freno contando en
  > directo**, no una etiqueta. Costó 10 tokens de entrada y 4 de salida.

  ⚠️ Y la llave de `Default` **sigue haciendo falta**: es la que va al servidor
  en `T-078`, guardada aparte antes de sobrescribir el `.env`.

- 📌 **Queda abierto, y a propósito.** La consola ofrece además tope de **gasto**
  por espacio de trabajo. `[D-059]` lo descartó por ser reparto del mismo techo
  — cierto contra el tope mensual de $500, pero el freno real de este proyecto es
  el **saldo de $6,55**, y un tope mensual bajo sí mordería antes que él. No se
  toca `[D-059]` por mi cuenta: se señala para decidirlo con la pantalla delante.
  ✅ **CERRADO el 2026-08-12 por `[D-062]`:** tope de `$2,00` al mes, puesto como
  **reserva y contabilidad, nunca como protección**.

- 🚨 **AÑADIDO el 2026-08-12 — el `50` de la primera fila dejó de ser solo un
  freno: ahora es también una FIRMA, y vive en dos sitios.** `[D-063]` decidió que
  `deploy/install.sh` **aborte el despliegue si la llave que le dan devuelve
  `requests-limit: 50`**, porque ese valor identifica al laboratorio y evita
  mandar a producción la llave equivocada (las dos se llaman igual en el `.env`
  local, ver más arriba).

  > ⚠️ **Por eso, cambiar este número obliga a tocar `deploy/install.sh` en el
  > mismo cambio.** Si se sube a 80 para medir Haiku —que es justo lo que la
  > trampa del paso 9, cuatro puntos más arriba, dice que va a pasar— la
  > comprobación del despliegue **deja de reconocer al laboratorio y no avisa de
  > nada**. No da error: se queda muda.

  🔑 Se escribe aquí, y no solo en `[D-063]`, a propósito: **el acoplamiento tiene
  que verse desde los dos lados.** Quien venga a afinar el freno abre esta
  entrada, no la otra.

### [D-060] 2026-08-11 — El tope de la báscula sale del saldo, no del historial

- **Qué se decidió:** el corte duro de `measure_tutor.py` —la capa 1 de
  `[D-059]`— se deriva del **dinero**, con la división escrita en el código:

  ```
  BUDGET_PER_RUN_USD   = 0.25       # decisión de dinero, del usuario
  COST_PER_CALL_USD    = 0.00234    # medido, [D-058]
  MAX_CALLS_PER_RUN    = 106        # la división, no una constante a mano
  ```

- **Contra qué:** contra dejar el `MAX_CALLS = 10` que el archivo ya traía, y
  contra elegir un número redondo "que suene bien".
- **Por qué:** ver abajo.
- **Fecha:** 2026-08-11, construido y corrido en `T-083`.
- **Toca:** `measure_tutor.py`, `tests/test_measure_tutor.py`, `[C-008]`,
  `T-078` (le levanta la condición que `[D-059]` le puso).

🚨 **El error que corrige, que no daba ningún error.**

El archivo ya tenía un tope: `MAX_CALLS = 10`.

🔻 **Y su procedencia era peor de lo que esta entrada dijo en su primera
versión.** Aquí se escribió que el diez era "el tamaño de la tanda de `T-079`",
que ya habría estado mal. Al mirar el archivo se ve que **`SENTENCES` tiene
exactamente diez frases**. Así que:

| pregunta | lo que contestaba el diez |
|---|---|
| ¿cuántas puede quemar una tanda sin poner en riesgo el servicio? | nada |
| ¿cuántas llamadas hizo `T-079`? | diez — **pero porque había diez frases** |
| ¿de dónde salía el diez, entonces? | 🔑 **de un `len()`** |

> 🔑 **El número tenía aspecto de medido y no lo estaba.** Circuló **tres veces**
> —como constante, como tope, y como argumento en la conversación de hoy ("el
> número ya lo tienes de `T-079`")— sin que nadie pudiera decir de dónde salía,
> porque en el fondo salía de la longitud de una lista. Ver `[L-044]`.

Falla por los dos lados: por arriba, el paso 9 compara modelos con decenas de
llamadas y el freno habría mordido en la 11 dando un rojo falso en la primera
medición de verdad; por abajo, de dinero no decía absolutamente nada, que es de
lo que protege.

Señalado por auditoría externa el 2026-08-11, antes de teclear, y precisado por
la misma auditoría después de leer el código.

🔑 **Y lo que lo hacía cumplir tampoco era un freno.**

La ejecución era `SENTENCES[:MAX_CALLS]`, un recorte de lista. Con el tope en 106
y diez frases en la lista, ese recorte **no corta nada**: un freno decorativo que
se lee como un freno de verdad. Se quitó.

Ahora quien frena es un `CallBudget`, y las dos cosas que lo hacen freno:

- **Cobra ANTES de llamar.** Cobrando después, la llamada que rebasa el tope ya
  se hizo y ya se pagó: el freno denunciaría el gasto en vez de impedirlo.
- **Vive dentro de `RecordingClient`**, que es el **paso obligado** de toda
  llamada del guion. Puesto más arriba —en el bucle de `main()`— dejaría escapar
  cualquier camino que no pase por el bucle.

✅ **Se le vio morder, con tres sabotajes en ROJO** (`tests/test_measure_tutor.py`,
8 tests, suite en **395**):

| sabotaje | qué salió |
|---|---|
| cobrar **después** de llamar | `assert 3 == 2` — tres llamadas hechas con dos pagadas |
| contador **por cliente** en vez de compartido | `DID NOT RAISE` — el guion seguiría igual, sin frenar nunca |
| `>` en vez de `>=` | `DID NOT RAISE` en cuatro tests |

El del medio es el que justifica el archivo entero: `main()` construye un
`RecordingClient` nuevo en cada vuelta, así que un contador dentro del cliente se
pondría a cero en cada frase **y nadie lo notaría**.

⚠️ **Lo que este freno NO cubre, escrito aquí y en el código.**

| amenaza | ¿frena? |
|---|---|
| un bucle roto que llama mil veces **en una corrida** | ✅ sí — es el fallo mudo de `[C-008]` |
| correr `python measure_tutor.py` a mano una y otra vez | ❌ no — el monedero se reinicia en cada arranque |

🚨 **El hueco tiene un número, y va escrito porque la prosa no asusta:**

```
$6,55 de saldo ÷ $0,25 por tanda = 26 corridas
```

**Veintiséis vaciarían el saldo.** Y 26 no es un número grande: el paso 9 es
comparar modelos, o sea correr el guion **una vez por modelo, varias veces**. Una
tarde de depuración se come una fracción visible.

Es deliberado, no un olvido: el corte por corrida mata el fallo **mudo**, que era
el objetivo, y ese es el peligroso. 🔑 **Pero "no protege de correrlo muchas
veces" se lee como "habría que ser tonto", y 26 se lee como lo que es.** Un freno
sin su alcance escrito —y sin el número al lado— se lee como un freno completo.

💵 **De dónde sale el `$0,25`** (decisión del usuario, regla 5):

| $ por tanda | llamadas | % del saldo de $6,55 si un accidente la quema entera |
|---|---|---|
| $0,10 | ~43 | 1,5% — riesgo de rojo falso en el paso 9 |
| **$0,25** | **106** | **3,8%** ✅ |
| $0,50 | ~214 | 7,6% — el accidente ya duele |

📌 Y el precio por llamada se toma del modelo **más caro** que se vaya a probar
(`claude-opus-5`). Con modelos baratos el tope se queda corto —sobra presupuesto,
no muerde nadie— **nunca largo**. Errar del lado seguro.

### [D-059] 2026-08-11 — Medir y servir se parten en dos capas, porque el saldo no se puede partir

- **Qué se decidió:** la separación entre **medir** y **servir** se hace con
  **dos frenos distintos**, no con uno:

  1. 🚧 **Corte duro dentro de `measure_tutor.py`** — un tope de llamadas que el
     propio guion hace cumplir. Es el que protege el saldo compartido.
  2. 🗂️ **Un espacio de trabajo propio para medir**, con **su llave** y **su
     límite de velocidad**. Es el que separa la llave, la velocidad y la
     contabilidad.

- **Contra qué:** contra las dos alternativas que `T-082` dejaba escritas.
  - **Fiarlo todo al tope de gasto por espacio de trabajo** — descartado porque
    no es un bolsillo (ver abajo).
  - **Partir por orden** (medir siempre antes de tocar producción) — descartado
    porque es un acuerdo, no un freno, y un acuerdo que depende de que nadie se
    despiste es una racha.
- **Fecha:** 2026-08-11, con la documentación de Anthropic delante.
- **Toca:** `T-082` (cierra), `T-078` (le pone condición), `[C-008]`,
  `measure_tutor.py`.

🚨 **Lo que esta decisión NO hace: desbloquear `T-078`.**

La primera versión de esta entrada decía "desbloquea `T-078`" en el índice, con
la salvedad —"está decidida, no arreglada"— enterrada en el cuerpo. Señalado por
auditoría externa el mismo día, y es un fallo de sitio, no de contenido:

> 🔑 **El índice es lo que se lee en frío mañana; el párrafo no se relee.** Una
> salvedad en el párrafo no arregla un titular falso.

De las dos capas, **la única que protege el saldo es la 1, y todavía no está
escrita**. `T-078` es justo la acción que convierte `[C-008]` en real: pone la
llave en el servidor. Hacerla con la capa 1 sin construir deja la llave en
producción con **cero partición** — el estado exacto que `T-082` se abrió para
evitar.

📌 **La condición de `T-078` queda escrita así:** no cuelga de "la partición está
decidida", sino de **"la capa 1 existe y se le ha visto morder"** — un test que
sabotee el contador y lo vea ponerse ROJO, como se hizo con el `refund` en
`T-076`. Una decisión no frena un bucle.

🔑 **La asignación de llaves, que desde hoy hay dos.**

`T-078` se escribió cuando solo había una llave, así que su frase —"que
`ANTHROPIC_API_KEY` llegue al servidor"— quedó ambigua. Se fija:

| llave | para qué | dónde vive |
|---|---|---|
| la **nueva**, del espacio de medir | MEDIR | **local**, no sale de aquí |
| la **de hoy** (`T-075`) | SERVIR | **viaja al servidor** en `T-078` |

📌 **Consecuencia que se nombra a propósito, para que no parezca un accidente:**
con ese reparto **servir se queda en el espacio por defecto**, el único donde no
se puede poner ningún tope. Es deliberado. Lo que se quiere frenado es el
**laboratorio**, que es donde un `while` roto llama sin techo; la app no se quiere
frenada, y su abuso ya lo tapa la cuota diaria (`[D-058]`).

**Lo que dice la documentación, que es lo que decide.**

Los espacios de trabajo existen en la consola de primera parte y **sí** admiten
tope de gasto propio. Pero:

> *"You can set workspace limits **lower than (but not higher than)** your
> organization's limits"*
>
> *"**Organization-wide limits always apply**, even if workspace limits add up
> to more"*

🔑 **Eso es un reparto del mismo techo, no un bolsillo aparte.** El saldo de
$6,55 es de la **organización**. Si medir se lo come, servir se queda sin llave
igual, esté en el espacio de trabajo que esté. **`[C-008]` no se cierra con la
consola** — por eso hace falta la capa 1.

⚠️ Y un estorbo práctico: *"You cannot set limits on the Default Workspace"*. La
llave de hoy vive ahí, así que en el espacio por defecto no se puede poner nada.

**Qué frena cada cosa, que es donde está la trampa.**

| mecanismo | ámbito | cuándo muerde | ¿protege el saldo? |
|---|---|---|---|
| **límite de velocidad** por espacio (RPM/ITPM/OTPM) | espacio de trabajo | **en el momento** — la petición rebota | ❌ frena el ritmo, no el total |
| **tope de gasto** por espacio | reparto del techo de la organización | mensual, y ver `[A-025]` | ❌ no es bolsillo |
| **saldo prepagado**, recarga apagada (`[D-057]`) | organización entera | al agotarse | ✅ pero **es justo el recurso compartido** |
| 🚧 **corte duro en el guion** | la medición | en la llamada N | ✅ **el único que ataja el fallo real** |

**Lo que compran los espacios de trabajo aunque no cierren `[C-008]`:** una llave
distinta para medir, revocable sola; un límite de velocidad duro sobre esa llave
—no impide gastar el saldo, pero impide gastarlo **rápido**—; y contabilidad
separada, porque la API de uso y coste agrupa por `workspace_id`. Barato y útil.
No suficiente.

🔻 **Esto revierte media `[D-057]`, y el motivo importa más que el cambio.**

`[D-057]` descartó exactamente este corte duro, por PI-2, con este argumento:
*"el saldo ya hace ese trabajo, y lo hace fuera del programa, donde un `while`
roto no puede desactivarlo"*. **Era cierto, y sigue siéndolo hoy** — mientras el
servidor tenga la llave vacía, un saldo agotado solo apaga la medición, y eso no
rompe nada.

> 🔑 **Después de `T-078` el mismo hecho significa otra cosa.** El saldo agotado
> deja de ser un freno inofensivo y pasa a ser una **caída de producción**, muda
> además (`[C-008]`: el camino que devuelve cuota no toca el marcador). No es
> que `[D-057]` estuviera mal medida; es que dejó de aplicar el día que la llave
> cambia de sitio.

📌 **Descartado además: Claude Platform on AWS.** La misma API facturada por AWS
Marketplace. Se miró y se descarta por la regla 5: *"Usage is denominated in
Claude Consumption Units (CCUs) … invoiced monthly in arrears. CCUs are not
prepaid credits. **There is no CCU balance**"*. Sería cambiar un techo duro —el
saldo prepagado con la recarga apagada— por una cuenta abierta a mes vencido.

**Lo que queda sin comprobar:** cómo se hace cumplir el tope de gasto por espacio
en esta cuenta. Vive en `[A-025]`, no aquí.

### [D-058] 2026-08-11 — El tope de 20 se queda, y ahora tiene una corrida detrás

- **Qué se decidió:** `DAILY_LIMIT = 20` no se toca. Cierra `[A-010]`, que
  llevaba desde el 4 de agosto siendo una predicción.
- **Contra qué:** bajarlo, que es lo que sugeriría mirar solo el saldo.
- **Fecha:** 2026-08-11, con `T-079` corrido.

**Los dos instrumentos, y por qué son dos.**

| instrumento | qué dijo (10 llamadas) |
|---|---|
| consola de Anthropic | **$0,02** |
| tokens medidos × precio de lista oficial | **$0,0234** |

🔑 **Coinciden dentro del redondeo a céntimos, y eso vale más que cualquiera
de los dos por separado.** La consola redondea, así que dividir $0,02 entre 10
arrastra hasta un 25% de error — sirve para confirmar, no para proyectar. El
cálculo por tokens sí proyecta, pero es **aritmética de lista sobre una medida**,
no una medida. Juntos se sostienen: un instrumento averiado no puede producir
los dos. Es la forma de `[L-036]`.

**Lo que sale:**

| | |
|---|---|
| por práctica | **$0,00234** (53% entrada, 47% salida) |
| 20 al día, una persona | **$0,047** |
| al mes | **$1,41** |
| 180 días | **$8,44** |

🚨 **El hallazgo incómodo: el saldo de $6,55 no cubre a UNA persona a tope
durante la ventana.** Se acaba a los **140 días**, no a los 180.

✅ **Y aun así el 20 se queda. El motivo importa más que el número:** el tope no
describe el uso, **frena el abuso**. Nadie practica 20 veces al día 180 días
seguidos; el escenario de los $8,44 es el techo teórico, no la previsión.
Bajarlo a 10 castigaría a quien estudia de verdad un día intenso y no ahorraría
un centavo de los que se gastan en realidad.

🔎 **Lo que enseña la composición del coste:** la salida son 44 tokens contra
247 de entrada — una quinta parte— pero cuesta **casi la mitad**, porque el
precio de salida es 5× el de entrada. Acortar la respuesta del tutor rendiría
tanto como acortar la rúbrica, y la rúbrica es lo que hace que juzgue bien.

⚠️ **Consecuencia sobre `[C-008]`, que deja de ser teórica.** Con el saldo dando
para 140 días-persona a tope, que medir y servir salgan del mismo bolsillo ya no
es un riesgo lejano: una tanda de medición descuidada se come días de servicio.

📌 **Y la palanca para bajar la factura no es esta.** No es el tope de
prácticas, y no es el de 500 caracteres de `[C-002]` —que en uso normal no se
toca, porque la rúbrica pesa y la frase no (`[L-043]`)—. Es **el modelo**, y eso
es trabajo medido del paso 9 (`[D-049]`).

### [D-057] 2026-08-11 — El freno del paso 8 es el saldo, no el límite mensual

- **Qué se decidió:** el tope de gasto de la llave de la API para todo el paso 8
  es el **saldo prepagado con la recarga automática apagada**, y nada más. El
  **límite mensual se queda en los 500 US$** que puso Anthropic.
- 🔻 **Rectificado el mismo día (decisión del usuario), y la rectificación es
  buena:** la primera versión de esta entrada mandaba bajarlo a 10. No hacía
  falta. El saldo ya muerde muchísimo antes, así que bajar el límite hoy no
  protege de nada — era prevención para después vendida como tarea de hoy, que
  es justo lo que PI-2 pide no hacer.
- **Contra qué:** contra el plan B que `[A-024]` dejaba escrito — correr `T-079`
  con un contador de llamadas y un corte duro dentro del propio guion. Se
  descarta por PI-2: el saldo ya hace ese trabajo, y lo hace **fuera** del
  programa, donde un `while` roto no puede desactivarlo.
- **Por qué:** ver abajo.
- **Fecha:** 2026-08-11.

**Lo que se MIDIÓ mirando la consola** (`T-080`, acción del usuario):

| qué | valor el 2026-08-11 | qué clase de freno es |
|---|---|---|
| saldo prepagado | **6,55 US$** | 🚧 tope **duro**: se agota y las llamadas fallan |
| recarga automática | **DESACTIVADA** | 🔑 es lo que convierte el saldo en techo |
| límite de gasto mensual | **500 US$**, puesto por Anthropic, ajustable | 🚪 hoy inerte |

🔑 **La aritmética es todo el argumento: 500 no puede morder porque 6,55 se
agota antes.** El número grande y llamativo de la pantalla no es el freno del
proyecto; el freno es el número pequeño que casi no se ve. Leer la pantalla al
revés habría dejado el paso 8 creyéndose protegido por un techo que está 76
veces por encima del dinero que existe.

⚠️ **Y un saldo solo es techo si nadie lo rellena solo.** Con recarga automática
encendida, 6,55 no es un techo sino un escalón que se vuelve a subir cada vez
que se pisa — y entonces el único freno vivo sería el de 500, que ya vimos que
no sirve. Por eso la recarga **nunca se enciende**: es la misma familia de botón
que las siete puertas de `[C-005]`, que cruzan a gastar sin preguntar.

🚨 **Lo que sí queda escrito es el DISPARADOR, porque el riesgo no desaparece:
se aplaza.** Mientras el saldo sea pequeño, el 500 es inerte y da igual. **El día
que se recargue saldo, se invierte:** el saldo deja de ser el freno pequeño y el
500 pasa a ser el único freno vivo del proyecto. Ese día se baja **antes** de
volver a llamar, no después.

> ⚠️ **El peligro no es el 500 de hoy. Es el 500 de dentro de dos meses**, cuando
> ya nadie recuerde esta conversación y la recarga parezca un trámite.

📌 Si se baja alguna vez, el número será un **juicio, no una medición** (regla 6):
lo que costaría `T-079` es precisamente lo que `T-079` va a medir.

> 🔑 **Un freno que nunca se activa y un freno que no existe se ven exactamente
> igual desde dentro.** Es `[A-024]` otra vez, que llevaba un día entero
> pareciendo verdad sin que nadie hubiera mirado.

📌 **Consecuencia práctica para `T-079`:** 6,55 US$ es poco, y es posible que la
medición se quede a medias por falta de saldo. Eso **no es un fallo** — es el
freno funcionando, y deja el primer dato real de cuánto cuesta una práctica.

✅ **Nada pendiente en la consola.** Lo medido está firme y el freno de hoy ya
está puesto — lo puso Anthropic y lo confirmó la mirada del usuario.

### [D-056] 2026-08-10 — `ctx7` primero siempre; la skill `claude-api`, último recurso

- **Se eligió:** para cualquier consulta de documentación, una escalera fija —
  **(1)** `ctx7`; **(2)** la página suelta de la documentación oficial; **(3)** la
  skill `claude-api` entera, y solo si las dos primeras vuelven vacías o se
  contradicen, **diciéndolo en voz alta al subir el escalón**.
- **Contra:** lo que se venía haciendo — invocar la skill en cuanto la pregunta
  rozaba la API de Anthropic.
- **Por qué:** medido, no estimado. Una sola consulta llevó la sesión de **55 K a
  ~340 K tokens**. 🔑 **La skill no se abre por trozos: es todo o nada.** Vuelca
  unos treinta documentos —agentes gestionados, lotes, archivos, migración,
  caché— y TEAPP hace **una** llamada, `messages.create` con una rúbrica. Su
  coste no escala con el tamaño de la pregunta; el de `ctx7` sí.

  ⚠️ **Y lo caro no es el dinero, es la ventana de contexto.** Lo que se llena de
  manuales que no se usan empuja fuera el código, las decisiones y los tests; en
  sesión larga eso se resume, y lo resumido pierde el detalle.

  ✅ **El disparador de la skill está ancho a propósito** —se activa casi con
  nombrar a Anthropic— porque sirve a cualquier proyecto: uno que monte agentes,
  otro que migre de modelo. En uno que hace una sola llamada se dispara mucho más
  de lo que aporta. No es un defecto de la skill; es un desajuste con este
  proyecto.

  🚨 **Esto NO afloja la regla 6.** El dato se sigue comprobando siempre, y sigue
  prohibido contestar de memoria. Lo único que cambia es **por dónde se trae**.

  📉 De todos modos la necesidad va a bajar sola: el paso 8 era el único tramo
  que tocaba la API, y sus cuatro preguntas gordas ya están contestadas y
  fechadas dentro de `app/tools.py`. Lo que queda —`api.py`, y medir el timeout
  en `T-079`— es código y cronómetro, no manual.
- **Toca:** el método de trabajo de cualquier sesión, regla 5 (minimizar factura
  manda), regla 6 (comprobar siempre), `T-079`.

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
