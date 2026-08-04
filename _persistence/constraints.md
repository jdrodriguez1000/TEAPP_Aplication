# Restricciones — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [C-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

Tipos: 💰 dinero · ⏱️ tiempo · 🔧 plataforma · 📦 alcance

| id | fecha | límite | tipo |
|---|---|---|---|
| C-001 | 2026-08-03 | Nada sale a internet **a buscar algo que le falta**, ni en los tests ni en el cierre. Medida el 2026-08-04 (`T-047`) | 🔧 |

---

## Entradas

### [C-001] 2026-08-03 — Nada sale a internet a buscar algo que le falta

> ✏️ **Redacción corregida el 2026-08-04**, al medirla (`T-047`). Antes decía
> *"la suite no toca la red, y nada de lo que corre en el cierre tampoco"*. Esa
> frase era **falsa desde el día que el `git push` entró en el cierre** (`D-016`):
> un push va a GitHub por internet. Lo que la restricción quiere decir de verdad
> es lo de arriba. 🔑 **`npx` es el peligro; `git push` es el trabajo.** Salir a
> buscar algo que te falta te hace depender de que esté ahí y de que no haya
> cambiado; mandar tu propio código a un sitio que elegiste, no.

- **Tipo:** 🔧 plataforma
- **El límite:** ni los tests ni el protocolo de cierre salen a internet a
  **obtener** nada: ni una dependencia, ni un binario, ni una respuesta de una
  API. Sí está permitido mandar lo propio a donde se decidió mandarlo (`git push`).
- **De dónde sale:** no lo impone nadie de fuera — **es una propiedad que el
  proyecto ya tiene y de la que depende**, y estaba sin escribir. Ese era el
  problema: nadie puede respetar a sabiendas un invariante que no está anotado.
  Un `npx tsc` metido con buena intención lo habría roto sin que nadie lo notara,
  porque `npx` sale a internet a bajar lo que le falte.
- **Qué impide:**
  - Nada de `npx` ni de descargas en tests ni en el protocolo de cierre: se llama
    al binario que ya está en disco, y si no está, se reporta — ver [D-017].
  - Ninguna prueba puede llamar a la API de verdad. La que lo necesite, se marca
    y se corre a mano.
- **Cómo se comprueba — son dos comprobaciones, no una:**
  - **La mitad "tests", automática.** El portero de `tests/no_network.py` corre
    en cada `pytest` y revienta si algo intenta salir. Que el portero siga
    mordiendo se reverifica con `python -m pytest tests/check_no_network.py`
    (ver [D-022]).
  - 🚨 **La mitad "cierre", a mano y para siempre.** El portero **no ve los
    subprocesos**: `node` y `git` son otro proceso y salen por delante de sus
    narices sin que se entere. No es un arreglo pendiente, es cómo está
    construido. Se comprueba mirando que `node_modules/typescript/` esté en
    disco y que en `protocol-close` no aparezca `npx`.
- **Medición del 2026-08-04 (`T-047`):** se cumple. 192 tests verdes con la red
  cortada; los 5 controles del portero, verdes. `node_modules/typescript/bin/tsc`
  en disco (v7.0.2), sin descarga.
<!-- La más reciente arriba. Formato:

### [C-001] 2026-08-02 — <el límite, en una línea>

- **Tipo:** 💰 / ⏱️ / 🔧 / 📦
- **El límite:** <cuál es exactamente>
- **De dónde sale:** <quién o qué lo impone>
- **Qué impide:** <lo que no se puede hacer por su culpa>

-->
