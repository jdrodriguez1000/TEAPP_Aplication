"""El portero de `_persistence/seals/`: que un sello no cambie después de sellado.

🚨 **Es un portero DISTINTO al de `labels/`, y la diferencia es el punto entero.**
Allí se vigila la **extensión** —que no entre un archivo por la rendija del `glob`,
que es `T-108`—. Aquí eso no sirve de nada: el sello es un `.json` a propósito y es
el único archivo de la carpeta. Lo que hay que vigilar aquí es **que el contenido no
se mueva**.

🔑 **Y esta sí es una cerradura, al revés que el resto del sello.** `[D-104]` dice
en voz alta que **no leer** el archivo es procedimiento y no cerradura: está en
claro, en un repositorio público (`[C-007]`), y una casilla pregunta, no detecta.
Pero *"nadie lo editó después de sellarlo"* **sí** lo puede comprobar un programa, y
es justo la mitad que da valor a haber sellado: un sello que se puede reescribir
después de ver el resultado no es un sello, es una nota.

⚠️ **La carpeta nació sin portero y eso fue un defecto, no una etapa.** El sello se
escribió primero dentro de `_persistence/labels/`, donde **ningún test lo miró**
porque el `glob` de aquella carpeta busca `*.jsonl` y esto es `.json` — o sea que
cruzó la rendija de `T-108` **al primer intento y sin querer**. Sacarlo a una carpeta
propia arregló eso y creó el mismo agujero un piso más allá: una carpeta nueva que
ningún `glob` mira. Este archivo lo cierra.
"""

import hashlib
import json
from pathlib import Path

REPO = Path(__file__).parent.parent
SEALS_DIR = REPO / "_persistence" / "seals"
ARMS_FILE = SEALS_DIR / "hard_arms_sealed.json"
DECISIONS = REPO / "_persistence" / "decisions.md"

# 🔒 **El sello de `T-112`, escrito el 2026-08-19 ANTES de etiquetar y ANTES de
# correr el juez.** Va a mano y va aquí a propósito: es una **decisión**, no una
# relación — es la huella que se promete no mover. Derivarla del propio archivo
# haría un test que no puede fallar, que es lo mismo que no tenerlo (`[L-087]`).
ARMS_SHA256 = "1f15dfe8aa03b0260c5f62b5212a411cfa1c4df84e66cca9d72a20519590e6cc"


def test_the_sealed_arms_file_has_not_been_touched():
    """🚨 El sello de `[D-104]`, byte a byte como se selló.

    Si esto se pone rojo, alguien editó el reparto de brazos **después** de
    sellarlo. No se arregla actualizando la constante de arriba: se averigua qué
    cambió y por qué, porque el valor entero de haber sellado está en que no se
    pudiera mover al ver el resultado.
    """
    assert ARMS_FILE.exists(), f"falta el sello: {ARMS_FILE}"

    actual = hashlib.sha256(ARMS_FILE.read_bytes()).hexdigest()

    assert actual == ARMS_SHA256, (
        f"el sello de brazos CAMBIO despues de sellarse.\n"
        f"  escrito el 2026-08-19: {ARMS_SHA256}\n"
        f"  hoy:                   {actual}"
    )


def test_the_written_seal_and_the_decision_say_the_same():
    """🔑 La huella vive en DOS sitios, y por eso se cruzan.

    Lo mismo escrito en dos sitios solo miente cuando nadie compara — es el
    argumento de `replies.name_matches_rows`, aquí un piso más arriba. Si alguien
    actualiza la constante de este archivo para callar el test de arriba, esta
    comprobación canta, porque `[D-104]` no se movió.
    """
    assert ARMS_SHA256 in DECISIONS.read_text(encoding="utf-8"), (
        "el sha256 de este archivo no aparece en decisions.md: "
        "o se cambio aqui sin tocar [D-104], o al reves"
    )


def test_the_arms_split_is_fifteen_and_fifteen_over_the_new_sentences():
    """El reparto cubre 61-90 entero, sin solapes y 15 por brazo.

    ⚠️ **Esto NO abre el sello para nadie que lo lea:** comprueba la FORMA del
    reparto —cuántos y cuáles números— sin decir qué frase cae en qué brazo, que es
    lo contaminante. Un test puede mirar lo que una persona no debe.
    """
    data = json.loads(ARMS_FILE.read_text(encoding="utf-8"))

    arms = [value for key, value in data.items() if key.startswith("brazo_")]

    assert len(arms) == 2, "tienen que ser dos brazos, ni uno ni tres"
    assert all(len(arm) == 15 for arm in arms), "cada brazo lleva 15 frases"
    assert sorted(arms[0] + arms[1]) == list(range(61, 91)), (
        "el reparto tiene que cubrir 61-90 exactamente una vez cada una"
    )
