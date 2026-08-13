"""La báscula local: cuánto tarda `respond()` en lo que NO es el modelo.

🔑 **Cierra la última rendija de `[A-011]`, y sin gastar un centavo.** Es la
hermana barata de `measure_tutor.py`: aquella llama a Claude y cuesta dinero,
esta no llama a nadie.

Una práctica son tres piezas (`app/english_tutor.py:85-87`):

    respond() = count_words + judge_grammar + record_practice
                    ^^^^                          ^^^^
                    esto es lo que mide este guion

`judge_grammar` ya está medido y **además tiene techo impuesto**: el cliente de
Anthropic corta a los `8,0 s` (`app/tools.py:83`), pase lo que pase. Lo que
nunca se había cronometrado es el resto — y `[L-045]` lo dejó escrito como el
único hueco que quedaba:

> *"Los 10 s no pueden disparar por modelo lento (corta el cliente antes) ni por
> cola (la cola no se forma, por construcción). La única rendija que queda es que
> `respond()` fuera del modelo se coma más de 2 s."*

**Medido el 2026-08-13, cuatro corridas: 51 ms el peor caso.** Contra 2 000 ms
de presupuesto. Ver `[D-070]`.

🚨 **No gasta dinero.** Ninguna de las dos piezas llama a Anthropic. Por eso no
tiene `CallBudget`: no hay nada que presupuestar.

⚠️ **No escribe en `data/`** — es `[L-023]`, donde la báscula de `T-054` sí
escribió donde no debía. `record_practice` acepta `users_dir` y aquí se le pasa
una carpeta temporal que se borra sola.

🔑 **Se mide con contención, y la contención se provoca quitando sitio.** Es la
regla de `[L-045]`: cerrar cajas, no traer clientes. Cuarenta hilos escribiendo
en **el mismo archivo** se ponen en fila de uno por el candado — que es el peor
caso que el pool de 40 (`api.TUTOR_POOL_SIZE`) puede producir.

Se corre a mano, desde la raíz del proyecto:

    python measure_local_parts.py
"""

import statistics
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from app.tools import count_words, record_practice

# El mismo tamaño del pool del servidor (`api.TUTOR_POOL_SIZE`). Es el número
# máximo de prácticas que pueden estar escribiendo a la vez.
#
# ⚠️ Va escrito aquí y no importado de `api` a propósito: importar `api` levanta
# la app entera —y su pool de verdad— para medir dos funciones que no la
# necesitan. Si los dos números se separan, esta báscula mide de menos; lo vigila
# `test_the_local_scale_uses_the_real_pool_size`.
POOL_SIZE = 40

SENTENCE = "She go to school every day"


def time_count_words(repetitions: int = 1000) -> list[float]:
    """`count_words` a solas.

    Se repite mil veces porque una sola pasada no se ve: el reloj del sistema
    tiene menos resolución que la función.
    """
    times = []
    for _ in range(repetitions):
        started = time.perf_counter()
        count_words(SENTENCE)
        times.append(time.perf_counter() - started)
    return times


def time_record_alone(users_dir: Path, repetitions: int = 50) -> list[float]:
    """`record_practice` sin nadie compitiendo: el caso feliz."""
    times = []
    for _ in range(repetitions):
        started = time.perf_counter()
        record_practice("solo", correct=True, users_dir=users_dir)
        times.append(time.perf_counter() - started)
    return times


def time_record_contended(users_dir: Path, writers: int) -> list[float]:
    """`record_practice` con `writers` hilos sobre el MISMO archivo.

    🔑 **El mismo archivo es lo que hace el experimento.** Con un archivo por
    persona el candado no se toca y saldría el caso feliz disfrazado de contención.
    """

    def one_write(_):
        started = time.perf_counter()
        record_practice("crowded", correct=True, users_dir=users_dir)
        return time.perf_counter() - started

    with ThreadPoolExecutor(max_workers=writers) as pool:
        return list(pool.map(one_write, range(writers)))


def report(label: str, times: list[float]) -> float:
    """Imprime un resumen y devuelve el peor caso.

    🚨 **ASCII puro al imprimir, ni emoji ni tildes** — es `[L-001]`, que ya
    tumbó `measure_tutor.py` con `UnicodeEncodeError` en la consola cp1252 de
    Windows. Los emoji de los comentarios no molestan: nadie los imprime.
    """
    worst = max(times)
    print(f"\n{label}  (n={len(times)})")
    print(f"    mediana:  {statistics.median(times) * 1000:8.3f} ms")
    print(f"    peor:     {worst * 1000:8.3f} ms")
    return worst


def main() -> None:
    print("BASCULA LOCAL - las piezas de respond() que no llaman al modelo")
    print("No gasta dinero. No escribe en data/.")
    print("-" * 70)

    with tempfile.TemporaryDirectory() as temporary:
        users_dir = Path(temporary)

        worst_count = report("count_words", time_count_words())
        report("record_practice - sin competencia", time_record_alone(users_dir))
        worst_contended = report(
            f"record_practice - {POOL_SIZE} a la vez, mismo archivo",
            time_record_contended(users_dir, POOL_SIZE),
        )

    print("\n" + "=" * 70)
    local_worst = worst_count + worst_contended
    print(f"PEOR CASO LOCAL (count_words + record_practice): "
          f"{local_worst * 1000:8.1f} ms")
    print(f"TECHO DEL MODELO (timeout del cliente, impuesto): "
          f"{8.0 * 1000:8.1f} ms")
    print(f"TECHO DE UNA PRACTICA ENTERA:                    "
          f"{(8.0 + local_worst) * 1000:8.1f} ms")
    print(f"PRESUPUESTO DE LA RUTA (TUTOR_TIMEOUT_SECONDS):  "
          f"{10.0 * 1000:8.1f} ms")
    print(f"MARGEN QUE QUEDA:                                "
          f"{(10.0 - 8.0 - local_worst) * 1000:8.1f} ms")
    print("\nOJO - lo que este numero NO dice:")
    print("    1. No incluye la COLA del pool. El invariante de api.py:172")
    print("       (pool 40 = fichas de anyio 40) dice que no se forma cola, y")
    print("       lo vigila test_the_pool_matches_the_threads_fastapi")
    print("       _actually_uses, en tests/test_api.py.")
    print("    2. Medido en la maquina de desarrollo, no en el servidor.")
    print("       Otro disco da otro numero. Ver [D-070].")


if __name__ == "__main__":
    main()
