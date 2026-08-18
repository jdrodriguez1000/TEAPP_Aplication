# Respuestas archivadas — la antesala de `corpus/`

Respuestas de corridas del eval (`eval_rubric.py`) **cuya configuración TODAVÍA es
la de producción**, guardadas aquí porque hacen falta para una medición viva.

## Por qué existe esta carpeta

`data/` es un solo disco sin copia y está fuera de Git (`.gitignore:18`). Ese es
exactamente el argumento con el que `[D-097]` mandó las etiquetas a
`_persistence/labels/` — y no se le había aplicado a las respuestas. Las dos
mitades del mismo cruce vivían en regímenes opuestos, y la desprotegida era la que
costó dinero.

🔑 **No es que no se puedan recomprar: es que no se pueden repetir.** `[D-096]`
fija `$0,00342` por llamada — `$0,21` las sesenta. Pero el juez no es
determinista: volver a comprarlas da OTRAS respuestas, y el número que salga del
cruce dejaría de ser reproducible. Lo que se protege no es el archivo, es que la
medición siga siendo auditable.

🔻 **`[D-092]` ya había descrito este agujero**, al descartar la propuesta rival de
promover *"cuando la rúbrica ya no existe en producción"*:

> *"al crear un corpus la rúbrica está viva por definición, así que nada se
> guardaría nunca al nacer — la evidencia esperaría en `data/`, ignorado por Git y
> en un solo disco, exactamente mientras se la considera todavía no valiosa."*

Esta carpeta es esa espera, con respaldo.

## Antesala, no hermana

⚠️ Con `_persistence/labels/` la separación era limpia: etiquetas contra rúbrica
viva, corpus contra rúbrica muerta — **vidas opuestas**, hermanas naturales.

Aquí no. Lo que se guarda es un corpus de respuestas cuya única diferencia con
`_persistence/corpus/` es que su rúbrica todavía vive. **Es la misma vida en dos
momentos**, así que de aquí se sale hacia allá.

## Cuándo se sale, y quién dispara

🔻 **Cuando algún eje del nombre deja de coincidir con producción** — modelo,
huella de rúbrica o marca de selección. Es el criterio de `[D-092]`, sin cambiarlo:
el archivo se mueve a `_persistence/corpus/`, y el disparador va pegado al **commit**
que toque `MODEL` o `GRAMMAR_RUBRIC`.

🚨 **La regla de salida se escribe al nacer la carpeta, no el día que haga falta.**
Una antesala sin puerta de salida escrita es la misma cosa en dos sitios con fecha
diferida.

⚠️ **Y hasta que salga, `test_no_frozen_corpus_carries_the_live_rubric` NO cubre
este archivo**: ese test mira `_persistence/corpus/`, y aquí la huella viva es
legítima — es lo que define esta carpeta. Meter aquí lo de allá, o al revés, pone
rojo por construcción.

## 🔴 Un archivo con el mismo nombre en `data/` no es este archivo

El nombre lleva **fecha sin hora** (`T-109`) y `save_replies` abre en `"w"`. Otra
corrida entera el mismo día crea uno con nombre idéntico y contenido distinto.

**El original vive aquí y lo respalda Git. Quien vaya a cruzar lee esta carpeta,
no `data/`.**

## 🔒 La cerradura, y lo que no cierra

El portero es `replies.py`. Cotea `number` y `sentence` contra `SENTENCES`
—la cerradura de `PI-8`—, cotea `model` y `rubric` contra el nombre del archivo, y
**rechaza cualquier campo que no esté en `ALLOWED_FIELDS`**.

⚠️ **`reply` es prosa libre y ningún programa la audita.** Y aquí no es un campo
lateral como la `note` de las etiquetas: **es la carga entera del archivo** —sesenta
párrafos generados, en un repositorio **público** (`[C-007]`). Hoy la puerta es
inocente, porque el modelo solo puede citar las frases inventadas que se le dieron;
**eso es una propiedad de hoy, no del camino.** Por eso el conjunto de campos está
cerrado: el que se cuele mañana es justo el que nadie mirará. Ver `[D-093]`.

## Qué hay hoy

| archivo | qué es |
|---|---|
| `eval_replies_claude-opus-5_2026-08-18_rubric-bbf4be38_full.jsonl` | Las 60 respuestas del juez, corrida entera del 2026-08-18, `$0,21`. **Insumo de `T-111`**: se cruza contra `_persistence/labels/sentence_labels.jsonl` para medir si el corrector acierta. Rúbrica `bbf4be38` = la viva. |
