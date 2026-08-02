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


class ScoreFileError(Exception):
    """El archivo del marcador existe, pero no se puede entender.

    Es una excepción propia del proyecto, y no la de `json`, a propósito. En el
    paso 2 FastAPI tiene que poder distinguir "el marcador está roto" de
    cualquier otro fallo, y un `JSONDecodeError` no le dice eso: le dice que
    algún JSON, en algún sitio, no se pudo leer.

    ⚠️ Solo para el archivo ROTO. Que el archivo no exista no es un error: es
    el primer día de esa persona, y el marcador vale 0.
    """

    # Los mensajes van sin tildes a propósito: acaban impresos en la terminal, y
    # la consola de Windows no sabe pintar nada fuera de ASCII (ver [L-001]).


def count_words(sentence: str) -> int:
    """Cuenta las palabras de una frase. Python puro, sin modelo.

    Contar tiene una sola respuesta correcta, así que no se le pregunta al
    modelo: se calcula. `split()` sin argumentos parte por cualquier espacio en
    blanco —espacios, saltos de línea, tabulaciones— y descarta los huecos
    vacíos, así que los espacios de más no cuentan.

    🔑 Si no llega un texto, se avisa; no se convierte. Hoy `main.py` siempre
    manda texto, pero en el paso 2 FastAPI recibe JSON de internet y por ahí
    entra un numero, un `null` o una lista. Hacer `str(sentence)` por nuestra
    cuenta taparia el problema: contaria "4" como una palabra y devolveria 1,
    tan campante. El problema estaria antes, y nadie se enteraria.

    :raises TypeError: si lo que llega no es un `str`.
    """
    if not isinstance(sentence, str):
        raise TypeError(
            f"count_words esperaba un texto (str) y recibio "
            f"{type(sentence).__name__}: {sentence!r}"
        )

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

    🔑 **Ausente y roto no son lo mismo.** Si no hay archivo, es el primer día y
    el marcador vale 0. Si el archivo existe pero no se entiende, se avisa con
    `ScoreFileError`: devolver 0 en silencio sería decirle "tienes cero puntos"
    a alguien que tenia seis.

    :raises ScoreFileError: si el archivo existe pero no se puede interpretar.
    """
    if not path.exists():
        return 0

    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ScoreFileError(
            f"El marcador {path} no es un JSON valido ({error}). "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        ) from error

    if not isinstance(saved, dict) or "score" not in saved:
        raise ScoreFileError(
            f"El marcador {path} no tiene la clave 'score'. "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        )

    total = saved["score"]

    # `isinstance(True, int)` vale True en Python: `bool` hereda de `int`. Sin
    # descartarlo, un {"score": true} pasaria por un 1 perfectamente valido.
    if not isinstance(total, int) or isinstance(total, bool):
        raise ScoreFileError(
            f"El marcador {path} guarda {total!r}, que no es un numero entero. "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        )

    return total


def add_point(path: Path = SCORE_FILE) -> int:
    """Suma un punto al marcador y devuelve el total nuevo.

    Crea el archivo —y la carpeta `data/`— la primera vez.

    🔑 **Nunca sobrescribas un dato que no lograste entender.** Si el archivo
    está roto, quien lo use todavia puede abrirlo y recuperar su marcador a
    mano; si lo pisamos con un 1, ya no. Por eso el `read_score` va PRIMERO y
    su error sube sin atrapar: cuando falla, la escritura de abajo ni se
    intenta. No es casualidad del orden — es el orden lo que protege el dato.

    :raises ScoreFileError: si el archivo existe pero no se puede interpretar.
        En ese caso el archivo queda intacto.
    """
    total = read_score(path) + 1
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"score": total}), encoding="utf-8")
    return total
