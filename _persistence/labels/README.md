# Etiquetas — la verdad de referencia de las 60 frases

Aquí vive el juicio **humano** sobre `measure_tutor.SENTENCES`: para cada frase,
si está bien escrita o no. Es contra esto que se mide si el juez acierta
(`T-106`).

## Por qué esta carpeta existe aparte de `corpus/`

Son **vidas opuestas**, y por eso son hermanas y no una dentro de otra
(`[D-097]`):

| | `corpus/` | `labels/` |
|---|---|---|
| qué guarda | respuestas que compró el modelo | juicios que escribió una persona |
| cuándo entra | cuando su configuración **muere** (`[D-102]`) | en cuanto se escribe |
| depende de | modelo **y** rúbrica | ni del modelo ni de la rúbrica |
| si se pierde | cuesta `$0,20` y se vuelve a comprar | **no tiene precio** |

⚠️ `test_no_frozen_corpus_carries_the_live_rubric` exige que un corpus congelado
**no** lleve la huella de la rúbrica viva. Las etiquetas nacen contra la rúbrica
viva y valen mientras viva: metidas en `corpus/` pondrían ese test en rojo.

## Qué hay en cada fila

```json
{"number": 1, "sentence": "<la frase>", "verdict": null, "note": "opcional"}
```

- **`number`** — la posición dentro de `SENTENCES`, empezando en 1.
- **`sentence`** — el texto. 🔑 **Va guardado a propósito, no por comodidad:** si
  alguien inserta o reordena una frase en `SENTENCES`, sin este campo las sesenta
  etiquetas apuntarían a la frase de al lado **sin dar un solo error**.
- **`verdict`** — uno de `correct`, `wrong`, `unclear`, o `null` si nadie la ha
  mirado todavía.
- **`note`** — opcional, y **el único sitio donde cabe prosa libre**.

### Los tres veredictos, y por qué son tres y no dos

`unclear` existe porque **una duda resuelta a la fuerza no se recupera después**.
Con solo `correct`/`wrong`, una frase discutible se empuja hacia un lado y la duda
desaparece — y eso **mueve la tasa de acierto medida del juez** en la dirección en
que se haya empujado. El día que alguien note que una frase era discutible, ya
estará clasificada como una de las dos.

`null` **no** es un cuarto veredicto: es *"todavía no la ha mirado nadie"*. Se
separa de `unclear` por el mismo motivo, un piso más arriba — si el esqueleto
naciera con `unclear`, una frase sin tocar sería indistinguible de una que alguien
leyó y no supo clasificar.

## 🚨 `note` no la audita ningún programa

Este repositorio es **público** (`[C-007]`). Los porteros de `tests/test_labels.py`
comprueban que `number` y `sentence` salen de `SENTENCES`, que `verdict` está en el
conjunto cerrado, y que **no existe ningún otro campo con prosa**. De `note` no
comprueban nada: un programa no puede juzgar texto libre.

🔑 Se dice aquí en voz alta para que el verde de la suite no se lea como *"las
etiquetas están auditadas"*. Lo que está auditado es la **forma**. Que una etiqueta
sea acertada, y que `note` no lleve nada que no deba publicarse, lo sostiene quien
escribe — no un test.

## Cómo se trabaja

```bash
python labels.py
```

Sin archivo, lo crea con las 60 frases sin etiquetar. Con archivo, lo valida y dice
por dónde va el etiquetado.
