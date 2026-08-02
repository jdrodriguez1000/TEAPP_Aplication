"""Las tres herramientas del tutor.

Cada una hace un trabajo distinto, y ninguna sabe que las otras existen. Esa
independencia es lo que permite cambiar una sin tocar las demás — en el paso 8
`judge_grammar` se reescribe entera y estas otras dos ni se enteran.
"""

import json
from pathlib import Path

# La raíz del proyecto, calculada desde este mismo archivo: `app/tools.py` →
# sube a `app/` → sube a `TEAPP/`. Se hace así, y no con una ruta relativa a
# secas, para que el marcador sea siempre el mismo archivo sin importar desde
# qué carpeta se lance el programa.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Dónde vive el marcador. `data/` no va a Git: son datos de quien usa la app.
SCORE_FILE = PROJECT_ROOT / "data" / "score.json"

# El veredicto falso. Siempre el mismo, a propósito.
FAKE_VERDICT = "Nice work! That sentence looks correct to me."


def count_words(sentence: str) -> int:
    """Cuenta las palabras de una frase. Python puro, sin modelo.

    Contar tiene una sola respuesta correcta, así que no se le pregunta al
    modelo: se calcula. `split()` sin argumentos parte por cualquier espacio y
    descarta los huecos vacíos, así que los espacios de más no cuentan.
    """
    return len(sentence.split())


def judge_grammar(sentence: str) -> str:
    """Juzga la gramática de una frase. FALSA: no mira la frase.

    Devuelve siempre el mismo texto. No es pereza: el modelo es la única pieza
    que no responde igual dos veces, y mientras se construye la tubería
    conviene que no esté en el camino. Si algo falla ahora, esta función no
    puede ser la culpable.

    En el paso 8 se borra y en su lugar entra la llamada a Claude.
    """
    # `sentence` no se usa todavía, y es intencional: la firma ya es la
    # definitiva, para que el paso 8 solo cambie el cuerpo.
    return FAKE_VERDICT


def read_score(path: Path = SCORE_FILE) -> int:
    """Lee el marcador guardado. Si el archivo aún no existe, es 0.

    La ruta es un parámetro con valor por defecto para que los tests escriban
    en un archivo temporal en vez de pisar el marcador real.
    """
    if not path.exists():
        return 0
    saved = json.loads(path.read_text(encoding="utf-8"))
    return saved["score"]


def add_point(path: Path = SCORE_FILE) -> int:
    """Suma un punto al marcador y devuelve el total nuevo.

    Crea el archivo —y la carpeta `data/`— la primera vez.
    """
    total = read_score(path) + 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"score": total}), encoding="utf-8")
    return total
