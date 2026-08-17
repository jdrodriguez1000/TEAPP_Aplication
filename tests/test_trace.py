"""Los tests del cuaderno: que apunte, que añada, que reparta el tiempo, que NO
guarde la frase, que avise cuando se rompe y que escriba en la raíz desviada.

🔑 **El de la frase es el que importa de verdad.** Los demás comprueban que la
herramienta funciona; ese comprueba que cumple `PI-8`, que es lo único de aquí
que ninguna otra cosa vigila.

📌 **Esta cabecera se enumera entera a propósito.** Decía *"que apunte, que añada
y que NO guarde la frase"* cuando ya había cinco tests dentro, y el mismo día
—2026-08-18— se vio lo que cuesta esa costumbre: el docstring de `TutorReply`
decía *"tres piezas"* con cinco campos, y eso llevó a defenderle a la clase una
pureza que ya no tenía. Ver `[D-087]`.
"""

import json
from datetime import datetime, timezone

import pytest

from app import trace
from app.tools import MODEL_NAME

# La frase va aquí, en una constante con nombre gritado, para que los tests puedan
# exigir que NO aparezca en el archivo. Es de mentira: nadie la escribió.
LA_FRASE_QUE_NO_DEBE_SALIR = "I has a cat and she are happy"


def leer(path):
    """Las líneas del cuaderno, ya convertidas en diccionarios."""
    return [json.loads(linea) for linea in path.read_text(encoding="utf-8").splitlines()]


def test_record_writes_one_line_with_the_shape_of_the_practice(tmp_path):
    destino = tmp_path / "trace.jsonl"

    trace.record(
        user="ana",
        words=3,
        score=1,
        practice=1,
        correct=True,
        seconds=2.8765,
        queue_seconds=0.4,
        model_seconds=2.0,
        at=datetime(2026, 8, 17, 16, 5, tzinfo=timezone.utc),
        path=destino,
    )

    (fila,) = leer(destino)

    assert fila["user"] == "ana"
    assert fila["words"] == 3
    assert fila["score"] == 1
    assert fila["practice"] == 1
    assert fila["model"] == MODEL_NAME
    # 🔑 La mitad de máquina del veredicto: un booleano, no el texto del juez.
    assert fila["correct"] is True
    # Redondeado a milisegundos: el detalle más fino no lo lee nadie y ensucia el
    # archivo. Ver `record`.
    assert fila["seconds"] == 2.877
    assert fila["at"] == "2026-08-17T16:05:00+00:00"


def test_the_time_is_split_in_three_and_the_three_add_up(tmp_path):
    """🚨 El reparto de `[D-087]`: cola + modelo + resto = total, sin sobras.

    🔑 **El resto se calcula, no se recibe**, y esto es lo que lo comprueba. Si
    algún día `rest_seconds` entrara por la firma, quien llama podría mandar tres
    números que no cuadran con el cuarto — y una fila que se contradice a sí misma
    engaña más que una fila sin el dato, porque tiene todos los campos llenos.

    ⚠️ **Y `queue_seconds` no puede salir por resta**, que era la versión barata:
    sin él, `total − modelo` sería *"cola + nuestro código"* revuelto. Con los
    hilos ocupados la cola se dispara y el descenso de modelo de `[D-049]`
    parecería inútil **cuando el culpable sería la cola** — exculpar al modelo por
    el motivo equivocado, que es justo lo que este reparto existe para evitar.
    """
    destino = tmp_path / "trace.jsonl"

    trace.record(
        user="ana",
        words=3,
        score=1,
        practice=1,
        correct=True,
        seconds=3.0,
        queue_seconds=0.5,
        model_seconds=2.25,
        path=destino,
    )

    (fila,) = leer(destino)

    assert fila["queue_seconds"] == 0.5
    assert fila["model_seconds"] == 2.25
    # Lo que sobra del total: nuestro código, la cuota, el marcador.
    assert fila["rest_seconds"] == 0.25
    # Y la cuenta cierra. Es la propiedad entera del reparto en una línea.
    assert (
        fila["queue_seconds"] + fila["model_seconds"] + fila["rest_seconds"]
        == fila["seconds"]
    )


def test_record_appends_instead_of_replacing(tmp_path):
    """🚨 Dos prácticas son dos líneas, no una que pisó a la otra.

    Un `open(..., "w")` en lugar de `"a"` dejaría el archivo con la última
    práctica y borraría el resto — y **no daría ningún error**: el cuaderno
    seguiría existiendo, con una línea válida dentro. Se leería como "hubo una
    sola práctica".
    """
    destino = tmp_path / "trace.jsonl"

    trace.record(
        user="ana", words=3, score=1, practice=1, correct=True, seconds=1.0,
        queue_seconds=0.1, model_seconds=0.8, path=destino,
    )
    trace.record(
        user="luis", words=5, score=0, practice=1, correct=False, seconds=2.0,
        queue_seconds=0.2, model_seconds=1.5, path=destino,
    )

    filas = leer(destino)

    assert len(filas) == 2
    assert [fila["user"] for fila in filas] == ["ana", "luis"]
    # Y cada línea se lleva SU acierto, que es lo que la deducción por `score` no
    # podía garantizar si se perdiera una línea ([D-086]).
    assert [fila["correct"] for fila in filas] == [True, False]


def test_the_sentence_never_reaches_the_notebook(tmp_path):
    """🚨 `PI-8` con un test detrás, que es más de lo que `PI-8` tiene en general.

    🔑 **Y comprueba lo que NO está, que es un tipo de test raro y aquí
    necesario.** La forma de que la frase se filtre no es que alguien la escriba a
    propósito: es que alguien añada un campo `sentence` "para poder depurar", o
    que meta el texto del veredicto —que puede citar la frase dentro— creyendo
    que es un dato de forma. Este test se pone rojo en los dos casos.

    ⚠️ `record` **no recibe la frase**, así que hoy no podría guardarla ni
    queriendo. Eso es lo que lo hace fuerte: la firma es el freno, y este test
    es lo que impide que la firma crezca.
    """
    destino = tmp_path / "trace.jsonl"

    trace.record(
        user="ana",
        words=len(LA_FRASE_QUE_NO_DEBE_SALIR.split()),
        score=0,
        practice=1,
        correct=False,
        seconds=1.5,
        queue_seconds=0.1,
        model_seconds=1.2,
        path=destino,
    )

    crudo = destino.read_text(encoding="utf-8")

    assert LA_FRASE_QUE_NO_DEBE_SALIR not in crudo
    # Ni la frase entera ni un trozo suyo: una palabra sola ya sería una filtración
    # si el campo existiera.
    assert "cat" not in crudo
    assert "sentence" not in crudo
    assert "verdict" not in crudo


def test_record_does_not_swallow_its_own_failure(tmp_path):
    """🚨 El cuaderno roto AVISA. `LM.15`, y es media decisión de [D-086].

    Si `record` se tragara el fallo, la traza podría llevar semanas sin escribir y
    el tablero diría "pocas prácticas" en vez de "no estoy viendo nada" — dos
    conclusiones opuestas a partir del mismo silencio.

    🔑 La otra mitad de [D-086] —que ese fallo no le cueste la práctica a nadie—
    **no se comprueba aquí**: se comprueba en `test_api.py`, porque la red de
    seguridad vive en quien llama y no en esta función.
    """
    # Una carpeta que no existe. `open(..., "a")` no crea carpetas.
    destino = tmp_path / "no" / "existe" / "trace.jsonl"

    with pytest.raises(OSError):
        trace.record(
            user="ana",
            words=3,
            score=1,
            practice=1,
            correct=True,
            seconds=1.0,
            queue_seconds=0.1,
            model_seconds=0.8,
            path=destino,
        )


def test_the_notebook_path_comes_from_the_diverted_root(tmp_path, monkeypatch):
    """Sin `path`, la traza escribe donde diga `TEAPP_DATA_DIR` — y en los tests
    eso es la carpeta temporal que puso `conftest.py`.

    🔑 **Este es el test que hace que la enmienda de [D-085] sea cierta y no una
    promesa:** el desvío que ya existía cubre la traza sola, sin que nadie añada
    una línea a `conftest.py`. Si alguien congelara la ruta, el archivo
    aparecería en `data/` de verdad y el portero de `no_data_writes.py` lo cazaría
    en la misma corrida.
    """
    from app import config

    trace.record(
        user="ana", words=3, score=1, practice=1, correct=True, seconds=1.0,
        queue_seconds=0.1, model_seconds=0.8,
    )

    esperado = config.trace_file()

    assert esperado.exists()
    assert esperado.parent == config.require_data_dir()
    # Y la raíz desviada NO es la carpeta `data/` del proyecto.
    assert esperado.parent != config.PROJECT_ROOT / "data"
