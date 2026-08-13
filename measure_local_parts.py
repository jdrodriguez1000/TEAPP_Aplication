"""La báscula local: cuánto tarda `respond()` en lo que NO es el modelo.

🔑 **Cierra la última rendija de `[A-011]`, y sin gastar un centavo.** Es la
hermana barata de `measure_tutor.py`: aquella llama a Claude y cuesta dinero,
esta no llama a nadie.

Una práctica son tres piezas (`app/english_tutor.py:85-87`):

    respond() = count_words + judge_grammar + record_practice
                    ^^^^                          ^^^^
                    esto es lo que mide este guion

`judge_grammar` **no tiene techo duro**, aunque el presupuesto del cliente lo
parezca. 🔴 **Descubierto el 2026-08-13 por auditoría externa:** un `timeout`
escalar no es un tope de la llamada — `httpx` lo reparte a **cuatro fases con
cronómetro independiente**, así que multiplica por cuatro en vez de dividir.
Compruébalo sin gastar nada:

    python -c "import anthropic; t=anthropic.Anthropic(api_key='x', timeout=8.0)._client.timeout; print(t.connect, t.read, t.write, t.pool)"

⚠️ **Los números concretos NO se repiten aquí a propósito.** Viven en
`app/tools.py` (`TIMEOUT`, `TIMEOUT_SECONDS`) y este guion los **lee**, no los
copia. Escribirlos en esta prosa fue exactamente el fallo que se corrigió tres
vueltas seguidas en este mismo archivo: se deduplicaron las constantes y se
dejaron los números sueltos en el texto, que **ningún `import` mantiene al día**.
Ver `[D-071]`, `[D-072]` y `[D-073]`.

Lo que mide este guion —el trabajo local— no depende de la red y sigue siendo
válido. Lo que se cayó fue la otra mitad de la cuenta. Ver `[A-011]`, reabierta,
y `[D-070]`, enmendada.

**Medido el 2026-08-13: 44,9 / 45,9 / 49,2 / 50,6 / 56,3 / 62,4 ms** en seis
corridas. ⚠️ **Y el máximo sube en cada tanda, que es el dato importante:** "el
peor de N" no es un techo, es un suelo que crece con N. Misma trampa que
`[L-043]` nombró con "la peor de diez". Para decidir algo se mira el orden de
magnitud —decenas de milisegundos— no la última cifra.

El orden de magnitud es lo que aguanta: **decenas de ms contra un hueco de casi
un segundo.** Lo que NO se puede hacer es restar y llamarlo margen; eso fue el
error de `[D-070]`.

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

from app import api, tools
from app.tools import count_words, record_practice

# El mismo tamaño del pool del servidor. Es el número máximo de prácticas que
# pueden estar escribiendo a la vez.
#
# 🔑 **Se LEE de `api`, no se escribe aquí.** Hasta el 2026-08-13 era un `40` a
# mano, con un test que vigilaba que no se separase del de `api`. Ese test ya no
# existe, y es una mejora: **el duplicado desapareció, así que no hay nada que
# vigilar.** Un número que se lee del sitio donde vive no puede desincronizarse.
#
# ⚠️ El precio, escrito para que se sepa: importar `api` levanta la app y su pool
# de verdad. En un guion que se corre a mano no cuesta nada; en un test sí, y por
# eso el aviso está aquí y no allí.
POOL_SIZE = api.TUTOR_POOL_SIZE

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
    # 🚨 Los dos numeros de abajo se LEEN del codigo, no se escriben a mano. Si
    # el presupuesto cambia, esta bascula imprimiria uno viejo — y un guion de
    # medir que imprime un presupuesto caducado miente con cara de dato.
    #
    # 🔑 Antes esto lo vigilaba un test (`test_the_local_scale_uses_the_real_
    # pool_size`). **Ya no existe, y es una mejora:** se quito el duplicado en vez
    # de vigilarlo. Lo que no se duplica no se puede desincronizar.
    budget = tools.TIMEOUT_SECONDS
    route = api.TUTOR_TIMEOUT_SECONDS
    print(f"PEOR CASO LOCAL (count_words + record_practice): "
          f"{local_worst * 1000:8.1f} ms")
    print(f"PRESUPUESTO DEL CLIENTE (suma de las 4 fases):   "
          f"{budget * 1000:8.1f} ms")
    print(f"PRESUPUESTO DE LA RUTA (TUTOR_TIMEOUT_SECONDS):  "
          f"{route * 1000:8.1f} ms")
    print(f"HUECO ENTRE LOS DOS, menos el trabajo local:     "
          f"{(route - budget - local_worst) * 1000:8.1f} ms")

    print("\nOJO - NINGUNO DE ESTOS DOS PRESUPUESTOS ES UN TECHO DURO:")
    print("    1. El del cliente NO lo es: httpcore aplica el reloj `read`")
    print("       tambien a cada lectura del cuerpo, asi que una respuesta en")
    print("       muchos trozos puede sumar mas. Ver [D-071] y [D-072].")
    print("    2. Aqui NO se resta nada para declarar un margen. Eso fue el")
    print("       error de [D-070]: restar de un techo que no existia.")
    print("    3. La COLA del pool no esta medida - y SI se forma: un 504")
    print("       suelta la ficha de anyio pero no el sitio del pool, que")
    print("       queda ocupado por el tutor zombi. Ver [L-056].")
    print("    4. Medido en la maquina de desarrollo, no en el servidor.")
    print("       Otro disco da otro numero.")


if __name__ == "__main__":
    main()
