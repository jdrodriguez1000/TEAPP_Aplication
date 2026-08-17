"""Pregunta a Anthropic de quién es la llave, ANTES de escribirla en el `.env`.

🚨 **El error que existe para cazar, y es de los que no dan error.** Desde
`[D-061]` hay DOS llaves y en el `.env` local **se llaman igual**
(`ANTHROPIC_API_KEY`): la de `Default`, que es la que sirve a las personas, y la
de `teapp-measure`, que es la del laboratorio. Nada en el nombre distingue una de
otra. Mandar la del laboratorio al servidor deja producción con el freno de 50
peticiones por minuto y el tope de $2 al mes de `[D-062]` — y el síntoma no llega
hoy: llega dentro de semanas, como un 429 raro atendiendo a una persona real.

🔑 **Cómo se distinguen, que es el único instrumento que sirve.** Las cabeceras
`anthropic-ratelimit-*` de una respuesta dicen contra qué cubo se contó la
llamada, y ese cubo es el del espacio de trabajo al que pertenece la llave. Se
probaron cuatro maneras de averiguarlo sin gastar; ninguna sirve:

| instrumento | qué pasó |
|---|---|
| cabeceras de un `529` | no trae ninguna `ratelimit` (`[L-046]`) |
| `count_tokens` | la llave sale válida, pero **no dice cuál** (`[L-046]`) |
| columna "último uso" de la consola | no registra `count_tokens` (`[L-046]`) |
| Rate Limits API | pide llave de **Admin** —más poder del que debe tener el servidor— y además responde *qué límites hay configurados*, no *de quién es esta llave* |

Así que la comprobación cuesta una llamada de verdad. Son unos 10 tokens de
entrada y 1 de salida: la misma que `[D-061]` ya hizo, y por eso se sabe lo que
cuesta.

📌 **Lo que este guion NO hace, a propósito:** no escribe nada. Solo mira y
devuelve un código. Quien escribe es `install.sh`, y lo hace **después** — el
orden es lo que impide que una llave mala quede clavada para siempre
(`[D-063]`).
"""

import json
import os
import sys
import urllib.error
import urllib.request

# 🚨 **ESTE NÚMERO VIVE EN DOS SITIOS Y ES EL ACOPLAMIENTO DE `[L-047]`.**
#
# Sale de `[D-061]`: es el límite de peticiones por minuto que se le puso al
# espacio `teapp-measure`. Aquí no se usa como freno, se usa como **firma**: si
# la llave que nos dan responde con este límite, es la del laboratorio.
#
# ⚠️ **Si alguien cambia ese límite en la consola, hay que cambiarlo aquí en el
# mismo momento.** `[D-061]` predice por escrito que va a pasar: el paso 9 mide
# Haiku, que es mucho más rápido, y "cada modelo nuevo necesita su fila con su
# propia medida". El día que esto suba a 80 y este archivo se quede en 50, la
# comprobación **deja de reconocer al laboratorio y no avisa de nada**: se queda
# muda, no da error. Por eso `[D-061]` lleva el aviso desde su lado también.
#
# 🔑 **Y por qué se compara contra el 50 del laboratorio y no contra el 1.000 de
# `Default`, que sería lo intuitivo:** el 1.000 lo pone Anthropic y puede moverlo
# mañana — `[D-061]` lo vio desmentirse en un solo día. Un freno colgado de un
# número ajeno es un rojo falso con fecha desconocida, y un freno que muerde en
# falso se acaba quitando. Este 50 lo pusimos nosotros.
#
# 🔑 **Y este número solo significa algo junto a `MODEL`:** el límite es por
# modelo, así que la firma es el par. Cambiar uno sin el otro deja al portero
# mudo — el aviso entero está en `MODEL`, abajo.
LAB_REQUESTS_PER_MINUTE = 50

KEY_NAME = "ANTHROPIC_API_KEY"
LIMIT_HEADER = "anthropic-ratelimit-requests-limit"

# El modelo que usa la app hoy ([D-049] lo revisa en el paso 9).
#
# 🚨 **NO da igual cuál sea, y el comentario que había aquí decía que sí.** Decía
# *"da igual cuál sea para lo que se pregunta aquí: lo que interesa son las
# cabeceras"*. Es falso, y de la forma muda:
#
# `anthropic-ratelimit-requests-limit` es **por modelo**. El 50 de arriba se le
# puso a `claude-opus-5` en el espacio `teapp-measure` ([D-061]). Así que la
# firma del laboratorio no es el número 50 a secas: es **el par (espacio,
# modelo)**. Preguntar por otro modelo devuelve OTRA fila de límites.
#
# ⚠️ **Qué pasa si se cambia esta línea sin tocar `LAB_REQUESTS_PER_MINUTE`:**
# la llave del laboratorio contesta con el límite del modelo nuevo, la
# comparación de abajo (`requests_limit == LAB_REQUESTS_PER_MINUTE`) sale FALSA,
# y el guion imprime *"no es la del laboratorio"* y devuelve `EXIT_OK`. **El
# portero acepta justo la llave que existía para rechazar, y no da ningún
# error.** Denegar por defecto (regla 3) se convierte en aceptar por accidente.
#
# 🔑 **Hay DOS formas de romper la firma, y este archivo solo avisaba de una.**
# El comentario de `LAB_REQUESTS_PER_MINUTE` cubre "alguien cambia el límite en
# la consola"; esta línea es la otra puerta, y decía que no existía. Un aviso
# correcto a doce líneas de algo que lo contradice es lo que le pasó a
# `install.sh` en `T-089` — ver `[L-061]`.
#
# 🔻 **DISPARADOR — se dispara CADA VEZ que se toca esta línea, no una sola vez.**
# Antes de cambiar este valor hay que **leer en la consola el límite por minuto
# del modelo nuevo en `teapp-measure` y poner ESE número arriba, en el mismo
# cambio**. No después, no "cuando se note": no se nota, esa es la avería.
#
# 🔑 **Y son DOS cambios, no uno:** `[D-049]` mete en el paso 9 el descenso a
# **Sonnet 5 y a Haiku 4.5**. Un disparador atado a "lo primero del paso 9"
# quedaria gastado despues del primero, justo antes del segundo. Ver `T-088`.
#
# 🧪 **Y desde `T-099` esto NO depende de que alguien lea este comentario:**
# `test_la_firma_del_laboratorio_es_el_par_modelo_y_limite` clava el PAR, asi
# que tocar esta linea pone la suite ROJA. Si estas leyendo esto por ese rojo:
# el arreglo es ir a la consola y poner arriba el limite del modelo nuevo — **no
# es tocar el test**. Visto morder el 2026-08-17 con `claude-sonnet-5`.
MODEL = "claude-opus-5"
API_URL = "https://api.anthropic.com/v1/messages"
API_VERSION = "2023-06-01"
TIMEOUT_SECONDS = 20

# 🔑 **Cuatro puertas de salida distintas, y esa es media decisión de `[D-063]`.**
# Si "no pude comprobar" saliera por la misma puerta que "es la del laboratorio",
# el primero que despliegue con Anthropic saturado leería "llave equivocada"
# teniendo la buena en la mano — que es justo el rojo falso que se quiso evitar.
EXIT_OK = 0
EXIT_NO_KEY = 1
EXIT_LAB_KEY = 3
EXIT_UNVERIFIABLE = 4


def ask_anthropic(api_key: str) -> tuple[int, dict[str, str]]:
    """Hace la llamada mínima y devuelve `(código HTTP, cabeceras)`.

    🚨 Nunca imprime la llave ni la devuelve — regla 7. Entra por argumento y se
    muere aquí dentro.

    ⚠️ Un error HTTP NO es una excepción para nosotros: un `401` y un `529`
    traen cabeceras y código, y son parte de la respuesta que hay que mirar.
    """
    body = json.dumps(
        {
            "model": MODEL,
            "max_tokens": 1,
            "messages": [{"role": "user", "content": "."}],
        }
    ).encode("utf-8")

    request = urllib.request.Request(
        API_URL,
        data=body,
        headers={
            "x-api-key": api_key,
            "anthropic-version": API_VERSION,
            "content-type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
            return response.status, dict(response.headers)
    except urllib.error.HTTPError as error:
        # La respuesta de error también trae cabeceras. Se leen igual.
        return error.code, dict(error.headers)


def main(environ: dict, ask=ask_anthropic) -> int:
    """Devuelve el código de salida. `ask` entra por parámetro para poder probarlo.

    🔑 Recibe `environ` en vez de mirar `os.environ` por dentro, igual que
    `create_account.py:44`. Es la única razón por la que esto se puede probar sin
    tocar la red ni gastar un céntimo.
    """
    api_key = environ.get(KEY_NAME, "")
    if not api_key:
        print(f"[Error] Falta {KEY_NAME}.", file=sys.stderr)
        return EXIT_NO_KEY

    try:
        status, headers = ask(api_key)
    except Exception as error:  # noqa: BLE001 — cualquier fallo de red cae aquí
        print(f"[Error] No se pudo preguntar a Anthropic: {error}", file=sys.stderr)
        print("        No es que la llave este mal: es que no se pudo mirar.", file=sys.stderr)
        return EXIT_UNVERIFIABLE

    # Las cabeceras HTTP no distinguen mayúsculas. Se normaliza antes de buscar.
    limits = {name.lower(): value for name, value in headers.items()}
    raw_limit = limits.get(LIMIT_HEADER)

    if raw_limit is None:
        # 🚨 Aquí caen el `401` (llave mal escrita), el `529` de saturacion
        # —que no trae cabeceras `ratelimit`, `[L-046]`— y cualquier respuesta
        # rara. Se deniega por defecto: no comprobado NO es comprobado.
        print(
            f"[Error] Anthropic respondio {status} y sin la cabecera {LIMIT_HEADER}.",
            file=sys.stderr,
        )
        print("        No se pudo saber de quien es la llave. NO se escribe nada.", file=sys.stderr)
        print("        Si es un 529, Anthropic esta saturado: vuelve a intentarlo.", file=sys.stderr)
        return EXIT_UNVERIFIABLE

    try:
        requests_limit = int(raw_limit)
    except ValueError:
        print(f"[Error] {LIMIT_HEADER} no es un numero: {raw_limit!r}", file=sys.stderr)
        return EXIT_UNVERIFIABLE

    if requests_limit == LAB_REQUESTS_PER_MINUTE:
        print(
            f"[Error] Esa es la llave del LABORATORIO (teapp-measure): "
            f"{LIMIT_HEADER}={requests_limit}.",
            file=sys.stderr,
        )
        print("        Al servidor va la de Default, no esta ([D-059]).", file=sys.stderr)
        print("        Las dos se llaman igual en el .env local: mira en la consola.", file=sys.stderr)
        return EXIT_LAB_KEY

    print(f"==> Llave comprobada: {LIMIT_HEADER}={requests_limit}, no es la del laboratorio")
    return EXIT_OK


if __name__ == "__main__":
    sys.exit(main(os.environ))
