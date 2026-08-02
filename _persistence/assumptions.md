# Suposiciones sin comprobar — TEAPP

> 📇 **Lee primero el índice.** Abre una entrada solo si la necesitas: cada una
> vive bajo su ancla `### [A-000]`. Búscala con `grep`, no leas el archivo entero.

⚠️ Aquí vive **solo lo que no se ha comprobado**. Cuando una suposición se
comprueba o se decide, **sale de aquí** y entra en `decisions.md` o `lessons.md`.

## Índice

| id | fecha | qué se está dando por cierto | riesgo si es falsa |
|---|---|---|---|
| A-001 | 2026-08-02 | El marcador cuenta frases **practicadas**, no correctas | hay que cambiar el contrato de `judge_grammar` |

---

## Entradas

### [A-001] 2026-08-02 — El marcador cuenta frases practicadas, no correctas

- **Se supone que:** el marcador mide **esfuerzo**, no acierto. `respond()` llama
  a `add_point()` siempre, sin mirar el veredicto, y eso se queda así.
- **Por qué está aquí y no en `decisions.md`:** la pregunta se planteó hoy y no
  se eligió entre las dos lecturas. Se anota como suposición —que es lo que
  es— en vez de dejarla sin escribir. **Está sin decidir.**
- **Por qué hoy no se nota:** el juez es falso y aprueba todo. Con `judge_grammar`
  devolviendo siempre el mismo veredicto, "practicadas" y "correctas" dan
  exactamente el mismo número. Las dos lecturas son indistinguibles hasta el
  paso 8.
- **Cómo se comprobaría:** en el paso 8, con el modelo enchufado, escribir una
  frase claramente incorrecta —`me likes coffees`— y mirar el marcador.
  - Si sube y eso es lo que se quería → la suposición era cierta. Sale de aquí y
    entra en `decisions.md`.
  - Si sube y chirría → era falsa. Sale de aquí y entra en `lessons.md`.
- **Si es falsa:** no basta con un `if` en `respond()`. Hoy el contrato es
  `judge_grammar(sentence) -> str`: devuelve **texto libre**, y nada dentro de
  esa cadena le dice a `respond` si la frase estaba bien. Contar aciertos obliga
  a cambiar el contrato de la herramienta para que devuelva algo que una máquina
  pueda leer —un aprobado/suspenso junto al mensaje—, y eso arrastra a `respond`
  y a lo que se le pida al modelo en el paso 8.
  🔑 El coste de equivocarse crece con el tiempo: hoy es un contrato que nadie
  usa todavía; en el paso 8 sería rediseñar la herramienta el mismo día que se
  enchufa el modelo, con dos sospechosos en vez de uno.
- **A favor de dejarlo así:** `_context/scope.md` pide que el agente "responda en
  tono positivo", y la v1 es de nivel A1. Un marcador que solo sube al acertar
  castiga justo a quien más se está esforzando.

<!-- La más reciente arriba. Formato:

### [A-001] 2026-08-02 — <qué se supone, en una línea>

- **Se supone que:** <la afirmación sin comprobar>
- **Cómo se comprobaría:** <la prueba concreta>
- **Si es falsa:** <qué se rompe>

-->
