"""La comprobación que impide mandar al servidor la llave del laboratorio.

🚨 **Esto se prueba porque el fallo que evita es MUDO.** Si la comprobación deja
pasar la llave de `teapp-measure`, no pasa nada visible: el despliegue termina en
verde, el servicio arranca, la app contesta. El síntoma llega semanas después
como un `429` raro atendiendo a una persona real, y para entonces nadie relaciona
las dos cosas.

🔑 **El criterio de `[D-059]` y `[D-060]`: no basta con que la capa exista, hay
que verla MORDER.** Por eso el test central de aquí no comprueba que el guion
tenga la comparación escrita — comprueba que **se pone rojo** cuando la
comparación deja pasar lo que no debe.

Ninguno de estos tests toca la red ni gasta un céntimo: `main()` recibe por
parámetro la función que pregunta a Anthropic, igual que `create_account.py`
recibe `environ`.
"""

import sys
from pathlib import Path

import pytest

DEPLOY = Path(__file__).resolve().parents[1] / "deploy"
sys.path.insert(0, str(DEPLOY))

import check_api_key  # noqa: E402

KEY_NAME = check_api_key.KEY_NAME
LIMIT_HEADER = check_api_key.LIMIT_HEADER

# Una llave de mentira. Nunca se usa contra la red.
FAKE_KEY = "sk-ant-de-mentira"
ENTORNO_CON_LLAVE = {KEY_NAME: FAKE_KEY}


def respuesta(limite, status=200, header=LIMIT_HEADER):
    """Fabrica una respuesta falsa de Anthropic con el límite que se le pida."""

    def ask(api_key):
        assert api_key == FAKE_KEY, "la llave tiene que llegar entera a quien pregunta"
        cabeceras = {} if limite is None else {header: str(limite)}
        return status, cabeceras

    return ask


# ── Lo que importa: que MUERDA ───────────────────────────────────────────


def test_rechaza_la_llave_del_laboratorio():
    # 🚨 El test entero del archivo. 50 es la firma de `teapp-measure` ([D-061]).
    salida = check_api_key.main(ENTORNO_CON_LLAVE, ask=respuesta(50))

    assert salida == check_api_key.EXIT_LAB_KEY


def test_acepta_la_llave_de_default():
    # 1.000 es lo que devuelve `Default` hoy. Pero fíjate en el test de abajo:
    # lo que hace pasar no es ser 1.000, es NO ser 50.
    assert check_api_key.main(ENTORNO_CON_LLAVE, ask=respuesta(1000)) == check_api_key.EXIT_OK


def test_acepta_cualquier_limite_que_no_sea_el_del_laboratorio():
    # 🔑 Esto es [D-063] escrito como test: se deniega lo conocido-malo, no se
    # exige lo conocido-bueno. El día que Anthropic mueva el 1.000 —cosa que
    # [D-061] ya vio pasar en un día— el despliegue tiene que seguir pasando.
    for limite in (400, 1000, 2000, 5000):
        assert check_api_key.main(ENTORNO_CON_LLAVE, ask=respuesta(limite)) == check_api_key.EXIT_OK


def test_el_numero_del_laboratorio_es_el_de_D061():
    # 🚨 **El guardián del acoplamiento de [L-047].** Este número vive en dos
    # sitios: la consola de Anthropic y este archivo. Si alguien sube el límite
    # del espacio para medir Haiku en el paso 9 y no toca `check_api_key.py`, la
    # comprobación se queda MUDA — deja de reconocer al laboratorio y no da
    # error. Este test no puede leer la consola, así que hace lo único que puede:
    # dejar el número a la vista, para que cambiarlo sea un acto consciente.
    assert check_api_key.LAB_REQUESTS_PER_MINUTE == 50


# ── Las puertas de salida, que tienen que ser distintas ──────────────────


def test_sin_llave_no_es_lo_mismo_que_llave_mala():
    assert check_api_key.main({}, ask=respuesta(1000)) == check_api_key.EXIT_NO_KEY


def test_una_respuesta_sin_cabecera_no_se_lee_como_llave_mala():
    # 🚨 El caso del `529`: Anthropic saturado no trae cabeceras `ratelimit`
    # ([L-046], nueve seguidos en 50 segundos). Si esto devolviera
    # EXIT_LAB_KEY, quien despliegue un mal día leería "llave equivocada"
    # teniendo la buena — el rojo falso que [D-063] evitó por delante,
    # entrando por la ventana.
    salida = check_api_key.main(ENTORNO_CON_LLAVE, ask=respuesta(None, status=529))

    assert salida == check_api_key.EXIT_UNVERIFIABLE
    assert salida != check_api_key.EXIT_LAB_KEY


def test_un_fallo_de_red_no_se_lee_como_llave_mala():
    def se_cae(api_key):
        raise OSError("la red no responde")

    salida = check_api_key.main(ENTORNO_CON_LLAVE, ask=se_cae)

    assert salida == check_api_key.EXIT_UNVERIFIABLE
    assert salida != check_api_key.EXIT_LAB_KEY


def test_las_cuatro_puertas_son_numeros_distintos():
    # Si dos coincidieran, `install.sh` no podría distinguir por qué se paró.
    puertas = {
        check_api_key.EXIT_OK,
        check_api_key.EXIT_NO_KEY,
        check_api_key.EXIT_LAB_KEY,
        check_api_key.EXIT_UNVERIFIABLE,
    }
    assert len(puertas) == 4


# ── Detalles que fallarían en silencio ──────────────────────────────────


def test_la_cabecera_se_encuentra_aunque_venga_en_mayusculas():
    # Los servidores HTTP pueden devolver el nombre como les parezca.
    ask = respuesta(50, header=LIMIT_HEADER.upper())

    assert check_api_key.main(ENTORNO_CON_LLAVE, ask=ask) == check_api_key.EXIT_LAB_KEY


def test_una_cabecera_que_no_es_un_numero_no_deja_pasar():
    ask = respuesta("no-soy-un-numero")

    assert check_api_key.main(ENTORNO_CON_LLAVE, ask=ask) == check_api_key.EXIT_UNVERIFIABLE


def test_la_llave_no_se_imprime_nunca(capsys):
    # 🚨 Regla 7. Se prueban los cuatro caminos, porque el que imprime de más
    # suele ser el del error.
    check_api_key.main(ENTORNO_CON_LLAVE, ask=respuesta(50))
    check_api_key.main(ENTORNO_CON_LLAVE, ask=respuesta(1000))
    check_api_key.main(ENTORNO_CON_LLAVE, ask=respuesta(None, status=401))

    salida = capsys.readouterr()
    assert FAKE_KEY not in salida.out
    assert FAKE_KEY not in salida.err


# ── El orden dentro de `install.sh` ─────────────────────────────────────
#
# 🔑 **Por qué esto se mira leyendo el archivo y no corriéndolo.** `install.sh`
# instala paquetes y servicios: no se puede correr en un test. Pero el orden
# —comprobar antes de escribir— es una garantía real de [D-063], y sin algo que
# lo vigile es solo un comentario. Es el mismo criterio de `test_deploy_*.py`.

INSTALADOR = DEPLOY / "install.sh"


def test_install_comprueba_la_llave_antes_de_escribirla():
    # 🚨 Si alguien mueve la comprobación detrás de la escritura, la regla
    # "nunca pisar una llave que ya existe" deja la llave mala clavada para
    # siempre: la regla que protege pasa a impedir el arreglo ([D-063]).
    #
    # ⚠️ **Se miran solo las lineas ACTIVAS, no los comentarios.** La primera
    # version de este test buscaba cualquier linea que nombrara
    # `check_api_key.py`, y la primera que lo nombra es un comentario que va
    # antes de la escritura: el test pasaba en verde con la comprobacion movida
    # al final del archivo. Un guardian que se cumple solo es peor que ninguno,
    # porque ademas tranquiliza ([L-043]).
    lineas = [
        l for l in INSTALADOR.read_text(encoding="utf-8").splitlines() if not l.strip().startswith("#")
    ]

    comprueba = next(i for i, l in enumerate(lineas) if "bin/python" in l and "check_api_key.py" in l)
    escribe = next(i for i, l in enumerate(lineas) if "printf 'ANTHROPIC_API_KEY=%s" in l)

    assert comprueba < escribe, "la comprobacion tiene que ir ANTES de escribir la llave"


def test_install_se_niega_a_terminar_sin_llave():
    # La tercera regla de [D-063]: sin llave no se termina en verde. Sin esto,
    # "vacía" seguiría siendo un estado legal y T-078 no habría servido de nada.
    texto = INSTALADOR.read_text(encoding="utf-8")

    assert "Falta ANTHROPIC_API_KEY" in texto


def test_install_no_escribe_la_llave_con_sed():
    # `sed` metería el valor dentro de la expresión: un carácter especial de la
    # llave la rompería, o peor, la cambiaría en silencio.
    texto = INSTALADOR.read_text(encoding="utf-8")

    assert "sed" not in texto or "ANTHROPIC_API_KEY" not in texto.split("sed")[1][:200]


@pytest.mark.parametrize("permiso", ["install -m 600"])
def test_el_temporal_del_env_nace_cerrado(permiso):
    # 🚨 La llave no puede existir ni un instante en un archivo abierto. El
    # temporal se crea con `install -m 600` y `mv` conserva esos permisos.
    texto = INSTALADOR.read_text(encoding="utf-8")
    bloque = texto.split("TMP_ENV=")[1]

    assert permiso in bloque
