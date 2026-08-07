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


def líneas_activas(archivo: Path) -> str:
    """El Caddyfile sin sus comentarios: solo lo que Caddy obedece.

    🔑 Vive aparte porque **lo usan dos controles distintos**, y este repo ya
    tiene un historial de datos replicados que se corrigen en un sitio y no en
    el otro (`[L-025]`). Si algún día cambia cómo se marca un comentario, cambia
    para los dos a la vez.
    """
    texto = archivo.read_text(encoding="utf-8")
    return "\n".join(
        línea for línea in texto.splitlines() if not línea.strip().startswith("#")
    )


def leer_max_size_de_caddy(archivo: Path = CADDYFILE) -> int:
    """El tope de cuerpo del Caddyfile, en bytes.

    El parámetro existe solo para poder medir el conversor con archivos de
    mentira: sin él, la única forma de comprobar que `KB` y `KiB` dan números
    distintos sería editar el Caddyfile de verdad.
    """
    # Solo las líneas que no son comentario: el porqué del número está escrito
    # arriba y menciona el número varias veces.
    encontrado = re.search(r"max_size\s+(\d+)\s*([A-Za-z]*)", líneas_activas(archivo))
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
    """Fiador del número, **no medición** — la medida se hizo aparte (`[D-035]`).

    ⚠️ Este test no comprueba nada contra Caddy: afirma la tabla `UNIDADES`
    contra sí misma, y solo puede ponerse rojo si alguien la edita. Eso es justo
    lo que se quiere —que cambiar ese número sea deliberado y no un descuido—
    pero **fiador no es báscula**, y conviene que el nombre no engañe.

    ✅ La báscula ya existe, y esta tabla salió indemne: el 2026-08-07 se midió
    con Caddy 2.11.4 real en contenedor (`caddy adapt` → `"max_size":16000`,
    control `16KiB` → `16384`; y por HTTP, 16000 B pasa y 16001 B devuelve 413).
    Lo que murió con esa corrida fue `[A-019]`, la suposición de que esto estaba
    solo leído. El número de aquí **no cambió**, y por eso este test sigue igual.
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


# ── El guardián de T-055: que la plantilla NO se fíe de nadie ─────────────
#
# 🚨 **Lo que protege, y por qué el fallo sería MUDO.** Medido el 2026-08-07 con
# Caddy 2.11.4 real (la tabla vive en `deploy/README.md`): un cliente que manda
# `X-Forwarded-For: 9.9.9.9` llega al backend como su dirección de verdad. Caddy
# **reescribe** la cabecera en vez de añadirle la falsa delante.
#
# 🔑 **Y eso NO lo hace por bondad: lo hace porque la plantilla no declara
# `trusted_proxies`.** La política de Caddy es *"By default, no proxies are
# trusted"*, así que lo que traiga el cliente es no confiable y se descarta.
#
# ⚠️ El día que alguien añada `trusted_proxies` —y hay motivos plausibles para
# quererlo: meter una CDN delante, o copiar una receta de internet— la cabecera
# forjada pasa a ser creíble, y con ella el origen. Entonces el freno de `/login`
# **se convierte en el ataque**: quien lo intenta pone una dirección distinta en
# cada intento y no se frena nunca. Y no falla nada, en ningún log, en ninguna
# parte: la app sigue contestando 200.
#
# 📌 Este guardián no comprueba comportamiento —eso ya se midió— sino que la
# **premisa** de aquella medida siga en pie. Ver `[A-014]` y `T-055`.

DIRECTIVA_PROHIBIDA = "trusted_proxies"


def declara_trusted_proxies(archivo: Path = CADDYFILE) -> bool:
    """Si el Caddyfile se fía de las cabeceras que le manden.

    El parámetro existe para poder ver al guardián ponerse ROJO sin tener que
    estropear la plantilla de verdad — `[L-007]`: un control se mide con el fallo
    puesto y sin él, o no se midió.
    """
    return DIRECTIVA_PROHIBIDA in líneas_activas(archivo)


def test_la_plantilla_no_se_fia_de_ningun_proxy():
    """🚨 El guardián. Si esto se pone rojo, el freno de `/login` es forjable."""
    assert not declara_trusted_proxies(), (
        f"`{DIRECTIVA_PROHIBIDA}` apareció en deploy/Caddyfile.template. "
        "Con esa directiva Caddy CREE la cabecera `X-Forwarded-For` que le "
        "mande el cliente en vez de reescribirla, y el freno de intentos de "
        "/login pasa a contar un origen que quien ataca elige en cada intento: "
        "no se frena nunca, y no falla nada en ningún log. "
        "Si de verdad hace falta (una CDN delante), no basta con quitar este "
        "test: hay que volver a medir la cadena entera — ver deploy/README.md."
    )


def test_el_guardian_ve_la_directiva_donde_puede_aparecer(tmp_path):
    """El control ROJO, en las dos formas en que Caddy la acepta.

    ⚠️ Sin esto, el de arriba sería verde y no se sabría si por estar bien la
    plantilla o por no saber mirar. Un control que nunca se ha visto rojo no
    distingue una cosa de la otra (`[L-020]`).
    """
    def con(contenido: str) -> bool:
        archivo = tmp_path / "Caddyfile.prueba"
        archivo.write_text(contenido, encoding="utf-8")
        return declara_trusted_proxies(archivo)

    # Forma 1: en el bloque global de opciones del servidor.
    assert con("{\n\tservers {\n\t\ttrusted_proxies static private_ranges\n\t}\n}\n")

    # Forma 2: dentro del propio reverse_proxy.
    assert con("sitio {\n\treverse_proxy 127.0.0.1:8000 {\n\t\ttrusted_proxies static 10.0.0.0/8\n\t}\n}\n")

    # Y el verde, con la forma que tiene la plantilla de verdad.
    assert not con("sitio {\n\treverse_proxy 127.0.0.1:8000\n}\n")


def test_el_guardian_no_se_dispara_por_un_comentario(tmp_path):
    """Que vigile lo que Caddy obedece, no lo que se escribió para explicarlo.

    La plantilla y este archivo **nombran** la directiva para contar por qué no
    está. Un guardián que leyera la prosa se pondría rojo sobre su propia
    explicación, y el arreglo sería borrar la explicación — justo al revés.
    """
    archivo = tmp_path / "Caddyfile.prueba"
    archivo.write_text(
        "# NO se declara trusted_proxies a proposito: ver T-055\n"
        "sitio {\n\treverse_proxy 127.0.0.1:8000\n}\n",
        encoding="utf-8",
    )

    assert not declara_trusted_proxies(archivo)


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
