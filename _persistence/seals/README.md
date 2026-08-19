# Sellos — lo que se escribió ANTES de conocer el resultado

Aquí vive un solo tipo de cosa: **un dato que se fija antes de mirar**, para que
después no se pueda reinterpretar con el resultado delante.

## Por qué es una carpeta aparte y no un archivo dentro de `labels/`

Dos razones, y la segunda es la que decidió:

1. **El portero de `labels/` recorre `*.jsonl`.** Un `.json` se le cuela sin que
   nadie lo mire — es la rendija de `T-108`, y este archivo la cruzó de verdad al
   nacer, no en teoría. Sacándolo de ahí, la regla de `T-108` puede quedarse
   **estricta**: en `labels/`, todo lo que no sea `README.md` acaba en `.jsonl`.

2. 🔑 **El archivo que no hay que leer no debe vivir en la carpeta donde se
   trabaja.** Quien etiqueta abre `labels/` sesenta veces. Poner ahí dentro lo que
   contamina su juicio es confiar en que no mire — y eso no es una protección, es
   una esperanza.

## Qué hay hoy

| archivo | qué sella | cuándo se abre |
|---|---|---|
| `hard_arms_sealed.json` | a qué brazo del desacuerdo apunta cada frase 61-90 de `T-112` | cuando las 90 filas de `sentence_labels.jsonl` tengan veredicto |

## 🚨 Honestidad sobre la fuerza de esto

Este repositorio es **público** (`[C-007]`) y el archivo está **en claro**. Así que
**no leerlo es procedimiento, no cerradura** — misma clase que `PI-8`, y se dice en
voz alta por el mismo motivo: una casilla pregunta, no detecta.

Lo que **sí** es comprobable es que nadie lo editó después de sellarlo: su `sha256`
quedó escrito dentro de `[D-104]`, en `decisions.md`, el mismo día. Comprobarlo:

```bash
sha256sum _persistence/seals/hard_arms_sealed.json
```
