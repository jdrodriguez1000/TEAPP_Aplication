# Corpus congelados

Respuestas de corridas del eval (`eval_rubric.py`) **cuya configuración ya no es
la de producción**. Aquí no entra una corrida viva: ésas escriben en `data/`, que
`.gitignore` cubre.

## Por qué existe esta carpeta

Un corpus cuyo modelo o cuya rúbrica ya cambiaron **no se puede volver a levantar
ni pagando**, y `data/` es un solo disco sin copia. Si además respalda una
decisión firmada, borrarlo la vuelve inauditable para siempre: la razón escrita
sigue ahí, pero ya no se puede comprobar. Ver `~~D-092~~`.

## Cuándo se promueve, y quién dispara

🔻 **Cuando algún eje del nombre deja de coincidir con producción** — modelo o
rúbrica. El criterio es el propio nombre, así que lo decide un programa y no un
juicio.

🚨 **El disparador va pegado al commit**, no a que alguien caiga después: quien
toque `MODEL` o `GRAMMAR_RUBRIC` promueve, **en ese mismo commit**, el último
corpus de la configuración que se va. Mismo patrón que `[D-081]`.

## Cómo se lee el nombre

    eval_replies_<modelo>_<fecha>_run-<sello>_<full|pick>.jsonl

El **sello** es `sha256(huella_rúbrica + huella_frases + huella_detector)[:8]`, y
contesta la única pregunta que el nombre tiene que contestar: **¿es este el mismo
experimento?** Ver `[D-102]`.

🔻 **Y hay una GENERACIÓN LEGADO, anterior al 2026-08-19, que no se renombra:**

    eval_replies_<modelo>_<fecha>_rubric-<huella>_<full|pick>.jsonl

Aquellos cuatro ejes sellaban la rúbrica pero **no** el conjunto de frases ni el
detector. `[D-102]` decidió **no tocarlos**: son evidencia congelada de corridas
**pagadas**, y su valor entero es ser el artefacto intacto. 🔑 **La generación
legado está muerta por construcción** —`save_replies` solo sabe escribir nombres
sellados— así que es una cola que decrece, no un diseño. Lo sostiene
`test_the_legacy_generation_never_grows`.

⚠️ **`pick` significa que la tanda fue una SELECCIÓN, no una muestra.** El archivo
del 2026-08-17 tiene 10 filas y 10 rotas: se escogieron a propósito las que habían
fallado. **Un porcentaje sacado de un `pick` no significa nada.**

## 🔒 La cerradura

Nada se promueve sin pasar `eval_rubric.sentences_are_invented()`: todas las
`sentence` tienen que salir de `SENTENCES`, que son frases inventadas y ya
públicas. `PI-8` prohíbe que una frase escrita por una persona usando la app entre
aquí, y este repositorio es **público** (`[C-007]`). Ver `[D-093]`.

## Qué hay hoy

| archivo | qué es |
|---|---|
| `eval_replies_claude-opus-5_2026-08-17_rubric-67a8a252_pick.jsonl` | Diagnóstico de 10 frases, `$0,03`. **Evidencia primaria de `[D-090]` y `[D-091]`**: la fila 4 es el ejemplo de las tres frases; la 14 es el falso positivo de `has_markdown` que mandó a `[D-091]`. Rúbrica `67a8a252` = la de `9844eac^`, jubilada el 2026-08-17. |
