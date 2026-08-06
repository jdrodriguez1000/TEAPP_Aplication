"""Los controles del portero de datos: comprueban que el portero de verdad muerde.

🔑 **Sin este archivo, el verde de la suite no demuestra nada.** Si el portero se
rompe en silencio, los tests siguen pasando exactamente igual — porque, con los
desvios de `conftest.py` puestos, ninguno intenta escribir en `data/`. El verde
de la suite dice "nadie escribio"; solo estos controles dicen "y si alguien lo
intentara, se le veria".

⚠️ **A proposito NO se llama `test_*.py`**, asi que `python -m pytest` no lo
recoge. Estos controles escriben en `data/` de verdad para tener algo que el
portero pueda pillar, y eso es justo lo que la suite prohibe: no pueden correr en
cada corrida normal. Mismo criterio que `check_no_network.py`, que sale a internet
de verdad por la misma razon.

Se piden por su nombre:

    python -m pytest tests/check_no_data_writes.py -v

Verde = el portero muerde. Rojo = el portero esta roto y hay que arreglarlo antes
de creerse ningun otro verde de la suite.

🚨 **Cada control deja `data/` como la encontro**, y no por cortesia: el portero
de `conftest.py` tambien vigila estos tests. Si uno se dejara el archivo de prueba
puesto, saltaria al terminar — lo que es, de paso, una segunda demostracion de que
el portero funciona.
"""

import pytest

import no_data_writes
from no_data_writes import REAL_DATA_DIR, DataTouched

# El archivo de prueba. Nombre inventado y con punto delante para que no se
# confunda nunca con el marcador de una persona de verdad.
PROBE = REAL_DATA_DIR / ".portero-de-prueba.tmp"


@pytest.fixture
def probe_cleaned_up():
    """Garantiza que el archivo de prueba no sobrevive al control, pase lo que pase.

    Va en `finally` y no al final del test: si el control falla a mitad, el
    archivo se borra igual. Un control que ensucia `data/` cuando falla seria
    peor que no tenerlo.
    """
    PROBE.unlink(missing_ok=True)
    yield PROBE
    PROBE.unlink(missing_ok=True)


def test_the_doorman_catches_a_new_file(probe_cleaned_up):
    """Lo mas parecido a lo que pasaria de verdad: un test que crea un marcador."""
    before = no_data_writes.fingerprint()

    probe_cleaned_up.write_text('{"score": 1}', encoding="utf-8")

    with pytest.raises(DataTouched):
        no_data_writes.raise_if_changed(before)


def test_the_doorman_catches_a_changed_content(probe_cleaned_up):
    """La puerta de atras: el archivo ya existia y solo cambio por dentro.

    🔑 Este es el control que separa un portero de verdad de uno ciego. Un portero
    que mirase `iterdir()` —que archivos hay— pasaria este control por alto: la
    lista de archivos es identica antes y despues. Solo cambio el numero de dentro,
    que es exactamente el punto de un marcador.
    """
    probe_cleaned_up.write_text('{"score": 5}', encoding="utf-8")
    before = no_data_writes.fingerprint()

    probe_cleaned_up.write_text('{"score": 6}', encoding="utf-8")

    with pytest.raises(DataTouched):
        no_data_writes.raise_if_changed(before)


def test_the_doorman_catches_a_deleted_file(probe_cleaned_up):
    """Borrar tambien es estropear. Un test que limpia `data/` pierde datos igual."""
    probe_cleaned_up.write_text('{"score": 5}', encoding="utf-8")
    before = no_data_writes.fingerprint()

    probe_cleaned_up.unlink()

    with pytest.raises(DataTouched):
        no_data_writes.raise_if_changed(before)


def test_the_doorman_says_which_file_changed(probe_cleaned_up):
    """Y no basta con saltar: tiene que decir cual.

    Con 328 tests, un "algo cambio" sin nombre deja a quien lo lea buscando a
    ciegas. El nombre del archivo es la mitad del valor del portero.
    """
    before = no_data_writes.fingerprint()

    probe_cleaned_up.write_text('{"score": 1}', encoding="utf-8")

    with pytest.raises(DataTouched) as caught:
        no_data_writes.raise_if_changed(before)

    assert PROBE.name in str(caught.value)


def test_the_doorman_stays_quiet_when_nothing_changed():
    """Y el portero no puede pasarse de listo: sin cambios, no protesta.

    Si saltara siempre, la suite entera estaria roja y el portero acabaria
    apagado en una semana. Un vigia que grita sin motivo es un vigia que se quita.
    """
    before = no_data_writes.fingerprint()

    no_data_writes.raise_if_changed(before)


def test_the_doorman_looks_at_the_real_folder_not_a_diverted_one():
    """🚨 El control que evita el portero que se mira a si mismo.

    `conftest.py` desvia `tools.USERS_DIR` y `quota.QUOTA_DIR` a una carpeta
    temporal. Si el portero colgara de una de esas constantes, estaria vigilando
    la carpeta desviada: verde siempre, sin mirar los datos de nadie. Por eso
    `REAL_DATA_DIR` se resuelve desde la ruta del propio archivo.

    Este control corre CON los desvios puestos —`conftest.py` se aplica igual
    aqui—, asi que si alguien reescribiera `REAL_DATA_DIR` para colgarla de
    `app.tools`, este control se pondria rojo en esa misma corrida.
    """
    from app import quota, tools

    assert REAL_DATA_DIR.name == "data"
    assert REAL_DATA_DIR.is_absolute()

    # Los desvios estan puestos ahora mismo, y el portero no los sigue.
    assert tools.USERS_DIR.parent != REAL_DATA_DIR
    assert quota.QUOTA_DIR.parent != REAL_DATA_DIR
