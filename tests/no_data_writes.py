"""El portero de los datos: vigila que la suite no escriba en `data/` de verdad.

`data/` son los datos de las personas que usan la app: sus marcadores, sus
cuentas y su cuota. No van a Git, y por eso **nadie los echa de menos**. Si un
test escribe ahi, `git status` no dice nada, la suite se pone verde y el estropicio
no se descubre — esa es la leccion [L-020].

Este modulo pone un portero en la puerta: toma la huella de `data/` antes de cada
test y la vuelve a tomar despues. Si cambio algo, ese test se pone rojo y dice
que archivo fue.

Se enchufa solo, en `conftest.py`, para TODOS los tests. 🔑 Un vigia que hay que
acordarse de encender es un vigia que algun dia no esta.

## Por que vigila la puerta y no al inquilino

La otra forma de cerrar [T-071] era un test que comprobara que `add_point`
escribe dentro de la carpeta temporal. Eso vigila a UN inquilino: el dia que
aparezca otro camino hacia `data/` —y ya se sabe que existe al menos uno, ver
abajo— ese test seguiria verde sin mirar.

El portero no pregunta quien escribe ni por que. Pregunta si `data/` cambio. Un
test escrito dentro de un año por alguien que no leyo nada de esto cae igual.
Misma idea que `no_network.py`, que no vigila a `english_tutor` sino a `connect`.

## Por que la huella es del CONTENIDO y no de la lista de archivos

Mirar solo que archivos existen es un portero ciego a la mitad del daño: un
`{"score": 5}` que pasa a `{"score": 6}` no crea ningun archivo y no lo veria
nadie. Justo el fallo que este arreglo viene a matar, cometido dentro del propio
arreglo. Por eso se compara un `md5` del contenido, no un `iterdir()`.

## Por que la carpeta se resuelve aqui

`REAL_DATA_DIR` cuelga de la ruta de ESTE archivo, y **no de `TEAPP_DATA_DIR` ni
de `config.users_dir()`**. Es a proposito: `conftest.py` apunta esa variable a una
carpeta temporal, y un portero que la siguiera se estaria mirando a si mismo —
verde siempre, sin vigilar nada.

🚨 Eso NO cambia con [D-037]: cuanto mas se centralice la ruta de los datos, mas
tentador es colgar de ahi tambien al vigilante. El control que lo impide es
`test_the_doorman_looks_at_the_real_folder_not_a_diverted_one`.

## 🚨 Lo que este portero NO puede ver

**Lo que corre fuera de pytest.** El portero vive dentro de la suite: se enchufa
en `conftest.py` y solo existe mientras corre un test. Un script suelto de
medicion, `python -m app.api`, o uvicorn levantado a mano, escriben en `data/`
de verdad y el portero ni se entera.

No es hipotetico. El 2026-08-06 a las 14:48:33 aparecieron a la vez
`data/users/otronombrelargo.json` y `data/quota/otronombrelargo.json` —el mismo
nanosegundo, cinco practicas— de una cuenta que no existe en `data/accounts.json`.
No pudo ser `pytest`: `conftest.py` desvia la cuota, asi que una corrida normal
no puede escribir en `data/quota/`. Fue algo corriendo por fuera.

🔑 **Ya se sabe QUE fue, y es peor de lo que parecia: la propia bascula de
`T-054`** —un script de medicion que desvio `accounts.ACCOUNTS_FILE` y se olvido
de `USERS_DIR` y `QUOTA_DIR`. No un intruso: el instrumento de medida. Cerrado en
`T-072`, contado entero en `[L-023]`.

**Es la misma frontera que los subprocesos de `no_network.py`, y por la misma
razon: no es un descuido que se pueda arreglar, es como esta construido.**
[T-071] blinda pytest y lo hace del todo; ese otro camino era otro animal, se
cerro en `T-072` y esta escrito en `[L-023]`.

🚨 **Y de ahi salio [D-037], que es lo que de verdad cierra esto.** Ya no hay tres
sitios que desviar: la raiz de los datos sale de `TEAPP_DATA_DIR`, **una sola
variable y sin valor por defecto**, y quien no la ponga no arranca. La regla para
el que venga es esa: un script que importe `app` fuera de la suite **apunta
`TEAPP_DATA_DIR` a una carpeta temporal suya** —que tiene que existir, y ser una
ruta absoluta— y, si quiere el cinturon ademas de los tirantes, toma huella con
`fingerprint()` antes y despues. Este modulo se puede importar desde fuera de
pytest, y para eso sirve.

⚠️ **El olvido ya no es silencioso.** Antes, olvidarse de un desvio escribia en los
datos de alguien sin decir nada; ahora falta la variable y no arranca. Ese es el
cambio, y por eso este portero pasa de ser la unica defensa a ser la segunda.

**Lo que se escribe con los mismos bytes.** La huella es del CONTENIDO, asi que
este portero es ciego a todo lo que no sean bytes: fechas, permisos, un archivo
reescrito con el mismo texto. Hoy no importa —sumar un punto siempre cambia el
numero, y renombrar encima cambia el contenido— pero es de la misma clase que lo
de arriba y conviene tenerlo escrito, no descubierto.

⚠️ Ese punto ciego ya mordio una vez, y no dentro de un test: restaurando `data/`
con `cp -r` tras sabotear este portero, las siete huellas coincidieron —bien— y
las fechas se perdieron, con ellas la prueba del camino de las 14:48. Un `md5` no
dice "todo igual": dice "los bytes, iguales". Ver `[L-022]`.

**Y un maniqui puesto mañana.** Si alguien vuelve a sustituir `add_point` por un
doble `autouse`, nadie escribe, el portero se queda verde — y el camino completo
se queda otra vez sin recorrer. Eso no lo caza un portero, lo caza el test que
exige ver el archivo aparecer en la carpeta temporal
(`test_practice_writes_the_score_inside_the_temporary_folder`, en `test_api.py`).
Las dos piezas hacen falta y vigilan cosas distintas.

Para comprobar que el portero sigue mordiendo: `tests/check_no_data_writes.py`.
"""

import hashlib
from pathlib import Path

# 🚨 La carpeta de verdad, resuelta desde ESTE archivo: `tests/no_data_writes.py`
# → sube a `tests/` → sube a `TEAPP/`. Sin pasar por `app.tools` ni `app.quota`,
# que es lo que `conftest.py` desvia. Ver "Por que la carpeta se resuelve aqui".
REAL_DATA_DIR = Path(__file__).resolve().parent.parent / "data"


class DataTouched(Exception):
    """Un test escribio en los datos de verdad. La leccion [L-020] se repitio."""


def fingerprint(directory: Path = REAL_DATA_DIR) -> dict[str, str]:
    """Huella del CONTENIDO de la carpeta: cada archivo, con el `md5` de sus bytes.

    Si la carpeta no existe todavia, la huella es vacia — y crearla se vera como
    un cambio, que es lo correcto.

    `rglob` entra en las subcarpetas (`users/`, `quota/`). Las carpetas en si no
    se apuntan: lo que importa es el contenido, y una carpeta vacia que aparece
    sin archivos dentro no ha estropeado ningun dato de nadie.
    """
    if not directory.exists():
        return {}

    prints = {}
    for path in sorted(directory.rglob("*")):
        if path.is_file():
            digest = hashlib.md5(path.read_bytes()).hexdigest()
            prints[str(path.relative_to(directory))] = digest

    return prints


def describe_changes(before: dict[str, str], after: dict[str, str]) -> list[str]:
    """Que cambio entre las dos huellas, en frases legibles.

    🔑 Decir "algo cambio" no sirve de nada a las 11 de la noche. El mensaje tiene
    que decir QUE archivo y COMO, para que quien lo lea sepa si tiene que
    restaurar algo o solo borrar basura.
    """
    changes = []

    for name in sorted(after.keys() - before.keys()):
        changes.append(f"se creo {name}")

    for name in sorted(before.keys() - after.keys()):
        changes.append(f"se borro {name}")

    for name in sorted(before.keys() & after.keys()):
        if before[name] != after[name]:
            changes.append(f"cambio el contenido de {name}")

    return changes


def raise_if_changed(before: dict[str, str], directory: Path = REAL_DATA_DIR) -> None:
    """Vuelve a tomar la huella y protesta si no coincide con la de antes.

    :raises DataTouched: si algo en `data/` se creo, se borro o cambio.
    """
    changes = describe_changes(before, fingerprint(directory))

    if changes:
        raise DataTouched(
            f"Este test escribio en los datos de verdad ({directory}): "
            + "; ".join(changes)
            + ". Los datos de `data/` son de las personas que usan la app y no "
            "van a Git: nadie los echa de menos si se estropean. Desvia lo que "
            "toque a una carpeta temporal en `conftest.py`."
        )
