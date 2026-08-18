"""El cruce de `T-111`: las etiquetas humanas contra el veredicto real del juez.

🎯 **Qué mide y qué no.** Mide si el corrector **coincide con el juicio de una
persona** sobre las mismas frases. No mide si el juez es bueno enseñando, ni si su
mensaje se entiende: solo si acierta el `OK`/`FIX`.

🚨 **No compra nada.** Lee los dos archivos que ya están en el repositorio y los
compara. `split_verdict` recibe la **respuesta** del modelo, no la frase — es
`split_verdict(answer: str)`, y confundirlo llamaría a Claude otra vez: `$0,21` y,
peor, respuestas distintas de las que están etiquetadas, con lo que el número
dejaría de ser reproducible (`[D-099]`).

📌 **Y el lector del veredicto es `app.tools.split_verdict`, no un lector nuevo.**
Escribir aquí un segundo intérprete de la primera línea deja dos que un día
discrepan — mismo motivo por el que `rubric_check` importa `VERDICT_CORRECT` en vez
de copiarlo (`[D-091]`). ⚠️ Tampoco vale `rubric_check.learner_message`: aquella
contesta **si** había palabra clave y tira **cuál** era, que es justo el dato que
hace falta (`[L-082]`).

🔒 **Las reglas del cruce están selladas en `[D-100]`, escritas ANTES de calcular**,
y esto es solo su ejecución:

- **La regla de exclusión, que es regla y no lista:** *se excluye la fila cuyo
  contenido o veredicto se expuso antes de etiquetar; nombrarla por número, sin
  contenido ni juicio, no excluye.* De ahí salen la **54** y la **55** (`[L-083]`) y
  entra la **37**.
- **Denominador 58**, con el de 60 reportado al lado.
- **Cuentas crudas delante, porcentaje detrás:** sobre 58 cada fila vale `1,72`
  puntos, y un porcentaje con decimal aparenta una precisión que la muestra no
  tiene.
- **Sale la tabla de 2×2, no un solo número.**

🎯 **Por qué la tabla y no la tasa, que es el punto entero.** Los dos errores caen
dentro de la misma tasa de acierto y **no valen lo mismo para un producto que
enseña**:

- **El juez corrige de más** (humano `correct`, juez `FIX`): molesta a quien
  practica y le hace dudar de algo que tenía bien.
- **🔴 El juez perdona** (humano `wrong`, juez `OK`): le dice que lo hizo bien
  cuando no. **Corregir de más molesta; perdonar enseña mal.**

⚠️ **`bad_format` se cuenta APARTE y no como desacuerdo.** `split_verdict` deniega
por defecto (`[D-067]`): si la primera línea no es exactamente `OK`, no hay acierto.
Eso mezcla *"el juez se equivocó"* con *"el juez rompió el formato"* bajo un mismo
fallo, y los arreglos van en direcciones opuestas — uno a la rúbrica, el otro al
modelo. Aquí se separan.
"""

import json
from dataclasses import dataclass
from pathlib import Path

import labels
import replies
from app import tools

# 🔒 Las filas que salen, y salen POR LA REGLA de `[D-100]`, no por una lista que
# alguien recuerde: se usaron como ejemplo al explicar `unclear` antes de que nadie
# etiquetara, así que llevan encima una opinión ajena que ya no se puede separar
# del juicio propio (`[L-083]`). La 37 se nombró por número, sin contenido ni
# veredicto, y por eso **entra**.
EXCLUDED_ROWS = frozenset({54, 55})


@dataclass(frozen=True)
class Crossing:
    """El resultado del cruce, con las cuatro casillas separadas.

    🔑 **Las casillas van sueltas y la tasa se deriva**, no al revés: guardar la
    tasa además sería tener dos datos que pueden discrepar, que es lo que `[D-094]`
    vino a quitar de la traza.
    """

    agree_correct: int  # humano `correct`, juez `OK`
    agree_wrong: int  # humano `wrong`, juez `FIX`
    judge_over: int  # 🟡 humano `correct`, juez `FIX` — corrige de más
    judge_forgives: int  # 🔴 humano `wrong`, juez `OK` — perdona
    bad_format: int  # el juez se saltó el formato: de la frase no se sabe nada
    compared: int  # filas que entraron de verdad en la cuenta

    @property
    def hits(self) -> int:
        """Aciertos: las dos casillas de la diagonal."""
        return self.agree_correct + self.agree_wrong


def cross(label_rows: list[dict], reply_rows: list[dict],
          excluded: frozenset[int] = EXCLUDED_ROWS) -> Crossing:
    """Cruza etiquetas contra veredictos y devuelve las cuatro casillas.

    🚨 **Empareja por número Y por texto, y se para si discrepan.** El número es una
    posición; el día que alguien inserte o reordene una frase en `SENTENCES`, cruzar
    por posición compararía la etiqueta de una frase contra el veredicto de la de al
    lado **sin dar un solo error**. Es el mismo freno que ya tienen los dos porteros.

    :raises ValueError: si una frase no tiene su pareja, o si el texto no coincide.
    """
    by_number = {row["number"]: row for row in reply_rows}

    counts = {"agree_correct": 0, "agree_wrong": 0,
              "judge_over": 0, "judge_forgives": 0, "bad_format": 0}
    compared = 0

    for label_row in label_rows:
        number = label_row["number"]

        if number in excluded:
            continue

        reply_row = by_number.get(number)
        if reply_row is None:
            raise ValueError(f"la frase {number} esta etiquetada y no tiene respuesta")

        if reply_row["sentence"] != label_row["sentence"]:
            raise ValueError(
                f"la frase {number} no dice lo mismo en los dos archivos: "
                f"etiqueta {label_row['sentence']!r}, "
                f"respuesta {reply_row['sentence']!r}"
            )

        human = label_row["verdict"]
        judge = tools.split_verdict(reply_row["reply"]).outcome

        compared += 1

        # ⚠️ Formato roto no es desacuerdo: de la frase no se sabe nada. Se cuenta
        # aparte para que no se disfrace de error de criterio (`[D-067]`).
        if judge == "bad_format":
            counts["bad_format"] += 1
        elif human == labels.LABEL_CORRECT and judge == "correct":
            counts["agree_correct"] += 1
        elif human == labels.LABEL_WRONG and judge == "wrong":
            counts["agree_wrong"] += 1
        elif human == labels.LABEL_CORRECT and judge == "wrong":
            counts["judge_over"] += 1
        else:
            counts["judge_forgives"] += 1

    return Crossing(compared=compared, **counts)


def report(crossing: Crossing) -> str:
    """El resultado en texto: cuentas crudas delante, porcentaje detrás (`[D-100]`).

    ⚠️ **Sin emoji, y no es estilo: la consola de Windows es `cp1252` y revienta.**
    Se vio el 2026-08-18 — `UnicodeEncodeError` al imprimir, con el cruce ya
    calculado. Los docstrings sí los llevan porque los lee quien abre el archivo;
    esto lo escupe una terminal.
    """
    share = 100 * crossing.hits / crossing.compared if crossing.compared else 0

    return "\n".join([
        f"Aciertos: {crossing.hits} de {crossing.compared}  ({share:.0f} %)",
        "",
        "                 juez OK   juez FIX",
        f"  humano correct   {crossing.agree_correct:>5}      {crossing.judge_over:>5}",
        f"  humano wrong     {crossing.judge_forgives:>5}      {crossing.agree_wrong:>5}",
        "",
        f"  [!!] el juez PERDONA un error:  {crossing.judge_forgives}",
        f"  [! ] el juez corrige de mas:    {crossing.judge_over}",
        f"  [ ?] formato roto (aparte):     {crossing.bad_format}",
    ])


def main() -> None:
    """Corre el cruce sellado y, al lado, el de las 60 sin excluir nada."""
    label_rows = labels.load_labels()

    archived = replies.archived_files()
    if not archived:
        raise SystemExit(f"No hay nada archivado en {replies.REPLIES_DIR}")

    reply_rows = replies.load_replies(archived[-1])

    print(f"etiquetas: {labels.LABELS_FILE.name}")
    print(f"respuestas: {archived[-1].name}")
    print()
    print(f"=== SELLADO ({len(labels.SENTENCES) - len(EXCLUDED_ROWS)} filas, "
          f"fuera {sorted(EXCLUDED_ROWS)}) ===")
    print(report(cross(label_rows, reply_rows)))
    print()
    print("=== AL LADO (las 60, sin excluir) ===")
    print(report(cross(label_rows, reply_rows, excluded=frozenset())))


if __name__ == "__main__":
    main()
