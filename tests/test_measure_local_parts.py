"""El invariante de la báscula local: que mida el peor caso de verdad.

🚨 **Por qué existe este archivo.** `measure_local_parts.py` produjo el número
que cierra `[A-011]` (`[D-070]`): **56,3 ms** de trabajo local —el peor caso de
cinco corridas— contra 2 000 ms de presupuesto. Ese número solo vale si la báscula empuja **tantos hilos como el
servidor puede tener escribiendo a la vez**.

🔑 **Y el `40` está escrito dos veces**, una en `app/api.py` y otra en la
báscula, porque importar `api` levantaría la app entera para medir dos funciones
que no la necesitan. Un número duplicado sin vigilante se separa en silencio — y
si se separa por abajo, la báscula mide **menos** contención de la real y
devuelve un margen optimista. Este test es el vigilante.

⚠️ Aquí no se llama a Anthropic ni se escribe en `data/`: `measure_local_parts`
no toca ninguna de las dos cosas, y ese es justo su punto.
"""

from app import api
from measure_local_parts import POOL_SIZE


def test_the_local_scale_uses_the_real_pool_size():
    """El peor caso de la báscula es el peor caso del servidor, no otro.

    🚨 **El fallo que caza es MUDO y cae del lado optimista.** Si alguien sube
    `TUTOR_POOL_SIZE` y no toca la báscula, esta sigue midiendo con menos hilos:
    sale un número más pequeño, el margen parece más ancho, y nadie ve un error.
    """
    assert POOL_SIZE == api.TUTOR_POOL_SIZE
