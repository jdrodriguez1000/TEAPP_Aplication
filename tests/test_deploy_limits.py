"""El tope de Caddy contra el tope de Python: que los dos números cuadren.

🚨 **Este es el primer test de TEAPP que lee un archivo de `deploy/`** — todos
los demás se quedan dentro de `app/`. Es una decisión, no un descuido: está
escrita en `[D-035]`.

El motivo es que aquí hay un acoplamiento real entre dos archivos que no se
conocen. `MAX_SENTENCE_LENGTH` vive en `app/api.py` y dice cuántos CARACTERES se
aceptan. `max_size` vive en `deploy/Caddyfile.template` y dice cuántos BYTES se
dejan subir. El día que alguien suba el primero, el segundo se queda corto **en
silencio**: Caddy empieza a devolver 413 a frases legítimas y en Python no falla
nada, porque la petición nunca llega. El síntoma aparece en producción, contado
por quien usa la app.

🔑 **Un carácter NO es un byte, y ahí está todo el asunto.** `MAX_SENTENCE_LENGTH`
acota caracteres; cada carácter cuesta entre 1 y 12 bytes según cómo venga
escrito. Medido el 2026-08-06 (`[D-035]`): 500 caracteres pesan 516 bytes en
inglés y 6016 en el peor caso legítimo.
"""

import json
import re
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.api import MAX_SENTENCE_LENGTH, app

CADDYFILE = Path(__file__).resolve().parents[1] / "deploy" / "Caddyfile.template"


# 🔑 **El peor caso legítimo son DOCE bytes por carácter, no cuatro.**
#
# Un emoji ocupa 4 bytes en UTF-8, que es como lo manda el navegador. Pero JSON
# también permite escribirlo "deletreado", con la forma `\uXXXX`, y un emoji no
# cabe en una sola: necesita dos seguidas (un *surrogate pair*), de la forma
# \uXXXX\uXXXX. Son 12 caracteres ASCII —12 bytes— para algo que la app cuenta
# como UNO.
#
# ⚠️ No es un ataque: es lo que produce cualquier cliente que serialice con
# `ensure_ascii=True`, que en Python es el valor por defecto. Un cliente
# legítimo puede mandarlo así sin saberlo.
BYTES_POR_CARACTER_PEOR_CASO = 12

# El sobre del JSON: `{"sentence": ""}` sin nada dentro. Se calcula, no se
# escribe a mano, porque depende de cómo se llame el campo.
JSON_ENVELOPE_BYTES = len(json.dumps({"sentence": ""}).encode("utf-8"))


# ── Leer el número de Caddy, no copiarlo ──────────────────────────────────
#
# 🚨 Escribir aquí el 16 KB a mano crearía una TERCERA copia del mismo número
# —el Caddyfile, este test y la máquina—, y sería justo este archivo, que existe
# para cazar números descoordinados, quien introdujera uno. Se lee de la única
# fuente que hay.

# go-humanize, que es lo que usa Caddy para leer estos tamaños, distingue las
# dos familias de unidades. **`KB` son 1000, `KiB` son 1024.**
#
# ⚠️ La diferencia importa aunque parezca cosmética: con `16KB` el techo real es
# 16000, y un test que afirmara 16384 se pondría verde en una franja de 384
# bytes donde Caddy YA está devolviendo 413. Un control verde midiendo un número
# que no rige es peor que no tener control.
UNIDADES = {
    "B": 1,
    "KB": 1000,
    "MB": 1000**2,
    "KIB": 1024,
    "MIB": 1024**2,
}


def leer_max_size_de_caddy(archivo: Path = CADDYFILE) -> int:
    """El tope de cuerpo del Caddyfile, en bytes.

    El parámetro existe solo para poder medir el conversor con archivos de
    mentira: sin él, la única forma de comprobar que `KB` y `KiB` dan números
    distintos sería editar el Caddyfile de verdad.
    """
    texto = archivo.read_text(encoding="utf-8")

    # Solo las líneas que no son comentario: el porqué del número está escrito
    # arriba y menciona el número varias veces.
    activas = [línea for línea in texto.splitlines() if not línea.strip().startswith("#")]

    encontrado = re.search(r"max_size\s+(\d+)\s*([A-Za-z]*)", "\n".join(activas))
    assert encontrado is not None, (
        f"No hay ninguna directiva `max_size` en {archivo.name}. "
        "O se borró el freno de T-054, o cambió de nombre."
    )

    cantidad, unidad = encontrado.groups()
    unidad = unidad.upper() or "B"
    assert unidad in UNIDADES, (
        f"Unidad `{unidad}` desconocida en {archivo.name}. "
        f"Las que este test sabe convertir son: {sorted(UNIDADES)}."
    )
    return int(cantidad) * UNIDADES[unidad]


def test_kb_se_lee_como_mil_y_no_como_mil_veinticuatro():
    """Fiador del número, **no medición** — la medida es `caddy adapt` (`[A-019]`).

    ⚠️ Este test no comprueba nada contra Caddy: afirma la tabla `UNIDADES`
    contra sí misma, y solo puede ponerse rojo si alguien la edita. Eso es justo
    lo que se quiere —que cambiar ese número sea deliberado y no un descuido—
    pero llamarlo "medido" contradiría a `[A-019]`, que dice, y bien, que esto
    está LEÍDO en la documentación de Caddy y sin pesar.
    """
    assert UNIDADES["KB"] == 1000
    assert UNIDADES["KIB"] == 1024


def test_el_conversor_aplica_la_unidad_y_no_solo_la_conoce(tmp_path):
    """Que la tabla de unidades se USE, no solo que exista.

    ⚠️ Sin este test, el de arriba se pondría verde aunque el conversor
    ignorara la unidad y devolviera siempre el número desnudo. Sería un control
    verde sobre un montaje roto: exactamente `[L-019]`.
    """
    def con(directiva: str) -> int:
        archivo = tmp_path / "Caddyfile.prueba"
        archivo.write_text(f"sitio {{\n\trequest_body {{\n\t\t{directiva}\n\t}}\n}}\n", encoding="utf-8")
        return leer_max_size_de_caddy(archivo)

    assert con("max_size 16KB") == 16_000
    assert con("max_size 16KiB") == 16_384
    assert con("max_size 512") == 512


def test_el_numero_no_se_lee_de_un_comentario(tmp_path):
    """El porqué del número está escrito arriba y lo menciona varias veces.

    Si el conversor leyera la primera coincidencia sin mirar si es código, el
    test mediría la prosa en vez del ajuste que rige.
    """
    archivo = tmp_path / "Caddyfile.prueba"
    archivo.write_text(
        "# el tope de antes era max_size 999KB, ya no rige\n"
        "sitio {\n\trequest_body {\n\t\tmax_size 16KB\n\t}\n}\n",
        encoding="utf-8",
    )

    assert leer_max_size_de_caddy(archivo) == 16_000


def test_la_frase_mas_pesada_que_la_app_acepta_cabe_en_el_tope_de_caddy():
    """🚨 El test que ata los dos archivos.

    Si se sube `MAX_SENTENCE_LENGTH` sin subir `max_size`, esto se pone rojo
    ANTES de desplegar, en vez de aparecer como un 413 inexplicable en
    producción.
    """
    peor_cuerpo = MAX_SENTENCE_LENGTH * BYTES_POR_CARACTER_PEOR_CASO + JSON_ENVELOPE_BYTES
    tope_de_caddy = leer_max_size_de_caddy()

    assert peor_cuerpo <= tope_de_caddy, (
        f"Una frase legítima de {MAX_SENTENCE_LENGTH} caracteres puede pesar "
        f"{peor_cuerpo} bytes, y Caddy corta en {tope_de_caddy}. Caddy "
        "rechazaría con 413 frases que la app acepta, y el error no saldría en "
        "ningún log de Python porque la petición no llega. "
        "Sube `max_size` en deploy/Caddyfile.template."
    )


# ── Y la prueba que exige el enunciado de T-054 ───────────────────────────
#
# El freno tiene que cortar el ataque sin romper el caso normal. Lo segundo es
# lo que se comprueba aquí: cinco alfabetos de precios distintos, todos en el
# borde exacto de 500 caracteres.

ALFABETOS = [
    pytest.param("a", id="ingles-ascii-1-byte"),
    pytest.param("ñ", id="espanol-con-tilde-2-bytes"),
    pytest.param('"', id="comilla-que-json-escapa"),
    pytest.param("中", id="chino-3-bytes"),
    pytest.param("🎉", id="emoji-4-bytes"),
]


@pytest.fixture
def sesión_abierta():
    """Una cuenta recién creada y la sesión puesta. `/practice` no atiende sin ella."""
    cliente = TestClient(app)
    respuesta = cliente.post(
        "/register",
        json={"user": "medidora", "password": "una-contrasena-larga"},
    )
    assert respuesta.status_code == 201, respuesta.text
    yield cliente
    cliente.cookies.clear()


@pytest.mark.parametrize("carácter", ALFABETOS)
def test_una_frase_legitima_de_500_pasa_en_cualquier_alfabeto(sesión_abierta, carácter):
    """Que el tope no se apriete de más.

    🔑 Un freno demasiado ajustado no falla contra el ataque: falla contra el
    uso normal, que es el único caso que nadie prueba.
    """
    frase = carácter * MAX_SENTENCE_LENGTH
    assert len(frase) == MAX_SENTENCE_LENGTH, "la app cuenta caracteres, no bytes"

    respuesta = sesión_abierta.post("/practice", json={"sentence": frase})

    assert respuesta.status_code == 200


@pytest.mark.parametrize("carácter", ALFABETOS)
def test_ninguna_frase_legitima_de_500_supera_el_tope_de_caddy(carácter):
    """Los pesos de verdad, alfabeto por alfabeto, contra el número que rige.

    El de arriba mide el peor caso teórico. Este mide los cinco casos reales, en
    las dos formas en que un cliente puede serializar el mismo texto.
    """
    frase = carácter * MAX_SENTENCE_LENGTH
    tope_de_caddy = leer_max_size_de_caddy()

    for ensure_ascii in (False, True):
        cuerpo = json.dumps({"sentence": frase}, ensure_ascii=ensure_ascii)
        assert len(cuerpo.encode("utf-8")) <= tope_de_caddy
