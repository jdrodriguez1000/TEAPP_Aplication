# Restricciones — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [C-000]`. Búscala con `grep`, no leas el archivo entero.

## Índice

Tipos: 💰 dinero · ⏱️ tiempo · 🔧 plataforma · 📦 alcance

| id | fecha | límite | tipo |
|---|---|---|---|
| C-001 | 2026-08-03 | La suite de tests **no toca la red**, y nada de lo que corre en el cierre tampoco | 🔧 |

---

## Entradas

### [C-001] 2026-08-03 — La suite de tests no toca la red, y el cierre tampoco

- **Tipo:** 🔧 plataforma
- **El límite:** los 121 tests corren sin conexión: el tutor es falso y no hay
  ninguna llamada a la API de nadie. Lo que corre en `protocol-close` hereda la
  misma regla.
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
- **Cómo se comprueba:** desconectar la red y correr `python -m pytest`. Si algo
  se cuelga o falla, esta restricción ya estaba rota.
<!-- La más reciente arriba. Formato:

### [C-001] 2026-08-02 — <el límite, en una línea>

- **Tipo:** 💰 / ⏱️ / 🔧 / 📦
- **El límite:** <cuál es exactamente>
- **De dónde sale:** <quién o qué lo impone>
- **Qué impide:** <lo que no se puede hacer por su culpa>

-->
