"""Las tres herramientas del tutor.

Cada una hace un trabajo distinto, y ninguna sabe que las otras existen. Esa
independencia es lo que permite cambiar una sin tocar las demás — en el paso 8
`judge_grammar` se reescribe entera y estas otras dos ni se enteran.
"""

import json
import os
import re
import tempfile
import threading
from pathlib import Path

from app import config

# Dónde viven los marcadores: uno por persona, `<raiz>/users/<nombre>.json`.
# `data/` no va a Git: son datos de quien usa la app.
#
# 🚨 **La raíz ya no se calcula aquí: la da `config.users_dir()`, y sale de
# `TEAPP_DATA_DIR`.** Antes era `PROJECT_ROOT / "data" / "users"` resuelta en
# este archivo, con la carpeta real como valor por defecto — así que cualquier
# script que importara esto y se olvidara de desviarla escribía en los datos de
# personas de verdad. Es lo que pasó ([L-023]) y lo que arregla [D-037].
#
# 🔑 Antes esto era UN archivo para todo el mundo. Mientras hubo terminal era
# verdad —habia una sola persona—; desde que hay servidor era mentira, y de las
# que no dan error: dos personas veian subir el mismo numero.

# El veredicto falso. Siempre el mismo, a propósito.
FAKE_VERDICT = "Nice work! That sentence looks correct to me."

# El candado del marcador. Quien quiera sumar un punto pasa por aqui, de uno en
# uno. En la terminal no hacia falta: habia una sola persona escribiendo. Desde
# que hay servidor, dos peticiones llegan a la vez de verdad.
#
# ⚠️ Vale dentro de UN proceso. Si uvicorn se lanzara con `--workers 2` serian
# dos procesos con un candado cada uno, y no se enterarian el uno del otro. Ver
# la suposicion [A-002].
#
# 🔑 Con un archivo por persona ese riesgo ENCOGE, no desaparece. Dos personas
# distintas en dos procesos distintos ya no se pisan: escriben en archivos
# distintos. Lo que queda es la MISMA persona dos veces a la vez —dos pestañas,
# dos dispositivos— cayendo en procesos distintos.
_SCORE_LOCK = threading.Lock()

# ── Las reglas del nombre ─────────────────────────────────────────────────
#
# 🚨 El nombre llega del navegador, y con el se construye una RUTA DE ARCHIVO.
# Sin frenos, quien usa la app elige a que archivo escribe el servidor: manda
# `../../CLAUDE.md` y el marcador aterriza fuera de `data/`.
#
# Por eso se sigue el criterio de `_context/architecture.md`: **denegar por
# defecto**. No se hace lista de lo prohibido —siempre falta algo— sino lista de
# lo PERMITIDO, y todo lo demas se rechaza.

# Solo minusculas, numeros, guion y guion bajo. Ni puntos (adios `..`), ni
# barras (adios `../`), ni espacios, ni tildes, ni nada fuera del ASCII.
USER_PATTERN = re.compile(r"^[a-z0-9_-]+$")

# Un nombre no puede ser infinito: al ponerle `.json` detras acabaria pasandose
# del limite del sistema de archivos, y eso revienta al escribir, no al validar.
MAX_USER_LENGTH = 32

# ⚠️ Windows reserva estos nombres para dispositivos, y los reserva **con
# cualquier extension**: `con.json` sigue siendo el dispositivo, no un archivo.
# Se cuelan enteros por la lista blanca de arriba, porque son letras y numeros.
# 🔑 Validar los caracteres no es validar el nombre.
WINDOWS_RESERVED_NAMES = frozenset(
    {"con", "prn", "aux", "nul"}
    | {f"com{digit}" for digit in range(1, 10)}
    | {f"lpt{digit}" for digit in range(1, 10)}
)


class InvalidUserError(Exception):
    """El nombre de la persona no sirve para nombrar un archivo.

    Excepción propia, y no `ValueError`, por la misma razón que
    `ScoreFileError`: FastAPI tiene que poder distinguir "el nombre no vale"
    —culpa de quien pregunta, 422— de cualquier otro fallo.
    """

    # Los mensajes van sin tildes a propósito (ver [L-001]).


class ScoreFileError(Exception):
    """El archivo del marcador existe, pero no se puede entender.

    Es una excepción propia del proyecto, y no la de `json`, a propósito. En el
    paso 2 FastAPI tiene que poder distinguir "el marcador está roto" de
    cualquier otro fallo, y un `JSONDecodeError` no le dice eso: le dice que
    algún JSON, en algún sitio, no se pudo leer.

    ⚠️ Solo para el archivo ROTO. Que el archivo no exista no es un error: es
    el primer día de esa persona, y el marcador vale 0.
    """

    # Los mensajes van sin tildes a propósito: acaban impresos en la terminal, y
    # la consola de Windows no sabe pintar nada fuera de ASCII (ver [L-001]).


def count_words(sentence: str) -> int:
    """Cuenta las palabras de una frase. Python puro, sin modelo.

    Contar tiene una sola respuesta correcta, así que no se le pregunta al
    modelo: se calcula. `split()` sin argumentos parte por cualquier espacio en
    blanco —espacios, saltos de línea, tabulaciones— y descarta los huecos
    vacíos, así que los espacios de más no cuentan.

    🔑 Si no llega un texto, se avisa; no se convierte. Hoy `main.py` siempre
    manda texto, pero en el paso 2 FastAPI recibe JSON de internet y por ahí
    entra un numero, un `null` o una lista. Hacer `str(sentence)` por nuestra
    cuenta taparia el problema: contaria "4" como una palabra y devolveria 1,
    tan campante. El problema estaria antes, y nadie se enteraria.

    :raises TypeError: si lo que llega no es un `str`.
    """
    if not isinstance(sentence, str):
        raise TypeError(
            f"count_words esperaba un texto (str) y recibio "
            f"{type(sentence).__name__}: {sentence!r}"
        )

    return len(sentence.split())


def judge_grammar(sentence: str) -> str:
    """Juzga la gramática de una frase. FALSA: no mira la frase.

    Devuelve siempre el mismo texto. No es pereza: el modelo es la única pieza
    que no responde igual dos veces, y mientras se construye la tubería
    conviene que no esté en el camino. Si algo falla ahora, esta función no
    puede ser la culpable.

    En el paso 8 se borra y en su lugar entra la llamada a Claude.
    """
    # `sentence` no se usa todavía, y es intencional: la firma ya es la
    # definitiva, para que el paso 8 solo cambie el cuerpo.
    return FAKE_VERDICT


def normalize_user(name: str) -> str:
    """Convierte el nombre escrito en la pantalla en un nombre de archivo seguro.

    Hace dos trabajos que se parecen y no son el mismo: **normalizar** (dejar
    el nombre en su forma única) y **validar** (rechazar lo que no sirve).

    🔑 **Normalizar primero, y una sola vez.** `  Juan `, `JUAN` y `juan` son la
    misma persona, y tienen que acabar en el mismo archivo. Si no se normaliza,
    Windows los junta —no distingue mayúsculas— y Linux los separa. O sea: en
    tu máquina serían una persona y en la nube del paso 7 serían tres. **Sin
    ningún error y con todos los tests en verde**, que es el peor tipo de fallo.

    :raises TypeError: si lo que llega no es un `str`. Igual que en
        `count_words`: por la red entra un número, un `null` o una lista, y
        convertirlo en silencio taparía el problema.
    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    """
    if not isinstance(name, str):
        raise TypeError(
            f"normalize_user esperaba un texto (str) y recibio "
            f"{type(name).__name__}: {name!r}"
        )

    user = name.strip().lower()

    # Los cuatro frenos van por separado, y cada uno dice lo suyo. Un unico
    # "nombre invalido" para todo dejaria a quien lo lea adivinando cual de las
    # cuatro reglas se salto.
    if not user:
        raise InvalidUserError("El nombre no puede estar vacio.")

    if len(user) > MAX_USER_LENGTH:
        raise InvalidUserError(
            f"El nombre no puede pasar de {MAX_USER_LENGTH} caracteres, "
            f"y este tiene {len(user)}."
        )

    if not USER_PATTERN.match(user):
        raise InvalidUserError(
            "El nombre solo admite letras sin tilde, numeros, guion y guion "
            f"bajo. Este no encaja: {name!r}"
        )

    if user in WINDOWS_RESERVED_NAMES:
        raise InvalidUserError(
            f"{user!r} es un nombre que Windows reserva para un dispositivo, "
            "y no se puede usar como archivo. Elige otro."
        )

    return user


def score_file(name: str, users_dir: Path | None = None) -> Path:
    """Devuelve el archivo del marcador de una persona.

    🔑 **Este es el único sitio donde un nombre se convierte en una ruta**, y
    por eso valida aquí dentro en vez de fiarse de quien llame. La puerta de red
    ya rechaza los nombres malos antes —para contestar un 422 con explicación—,
    pero esta función es la que toca el disco: si algún día la llama alguien que
    se saltó el filtro, tiene que negarse igual. **El olvido tiene que fallar
    hacia el lado seguro.**

    🚨 **El valor por defecto se resuelve AQUÍ DENTRO, no en la firma.** Escribir
    `users_dir: Path = config.users_dir()` parece lo mismo y no lo es: Python
    evalúa los valores por defecto **una sola vez, al importar el módulo**, y se
    queda con la carpeta de aquel momento para siempre. Hasta [T-071] esta
    función tenía esa firma, y por eso los tests no podían desviar el marcador:
    tenían que sustituir `add_point` entera por un maniquí, y el camino de verdad
    —API, marcador, disco— se quedaba sin recorrer. Preguntando en cada llamada,
    cambiar `TEAPP_DATA_DIR` cambia de verdad dónde se escribe.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises MissingDataDirError: si no hay raíz de datos declarada. Ver [D-037].
    """
    directory = config.users_dir() if users_dir is None else users_dir
    return directory / f"{normalize_user(name)}.json"


def read_score(name: str, users_dir: Path | None = None) -> int:
    """Lee el marcador de una persona. Si su archivo aún no existe, es 0.

    🔑 **Ausente y roto no son lo mismo.** Si no hay archivo, es el primer día y
    el marcador vale 0. Si el archivo existe pero no se entiende, se avisa con
    `ScoreFileError`: devolver 0 en silencio sería decirle "tienes cero puntos"
    a alguien que tenia seis.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises ScoreFileError: si el archivo existe pero no se puede interpretar.
    """
    path = score_file(name, users_dir)

    if not path.exists():
        return 0

    try:
        saved = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise ScoreFileError(
            f"El marcador {path} no es un JSON valido ({error}). "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        ) from error

    if not isinstance(saved, dict) or "score" not in saved:
        raise ScoreFileError(
            f"El marcador {path} no tiene la clave 'score'. "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        )

    total = saved["score"]

    # `isinstance(True, int)` vale True en Python: `bool` hereda de `int`. Sin
    # descartarlo, un {"score": true} pasaria por un 1 perfectamente valido.
    if not isinstance(total, int) or isinstance(total, bool):
        raise ScoreFileError(
            f"El marcador {path} guarda {total!r}, que no es un numero entero. "
            "No se ha tocado el archivo: revisalo o borralo para empezar de cero."
        )

    return total


def add_point(name: str, users_dir: Path | None = None) -> int:
    """Suma un punto al marcador de una persona y devuelve su total nuevo.

    Crea el archivo —y la carpeta `data/users/`— la primera vez.

    🔑 **Nunca sobrescribas un dato que no lograste entender.** Si el archivo
    está roto, quien lo use todavia puede abrirlo y recuperar su marcador a
    mano; si lo pisamos con un 1, ya no. Por eso el `read_score` va PRIMERO y
    su error sube sin atrapar: cuando falla, la escritura de abajo ni se
    intenta. No es casualidad del orden — es el orden lo que protege el dato.

    🔑 **La escritura es atómica: se escribe al lado y se renombra encima.**
    `write_text` haria dos cosas seguidas —vaciar el archivo y luego llenarlo— y
    entre las dos hay un instante. Un corte de luz justo ahi deja el marcador
    vacio o partido por la mitad, y el punto de arriba no sirve de nada: el
    archivo roto ya lo habriamos creado nosotros.

    Renombrar, en cambio, es UNA sola operacion del sistema operativo: o paso
    entera, o no paso. Nunca deja el archivo a medias. Asi, ante un corte, o
    queda el marcador viejo entero o el nuevo entero.

    🔑 **El candado y la escritura atomica resuelven cosas distintas.** La
    escritura atomica protege de UNA escritura cortada por la mitad. El candado
    protege de DOS escrituras pisandose. Tener la primera no da la segunda:
    hasta que hubo servidor no se noto, porque en la terminal solo escribia una
    persona a la vez.

    Y el candado abarca la lectura Y la escritura juntas, no solo la escritura.
    Si abarcara solo la escritura, dos peticiones leerian el mismo 5, las dos
    sumarian 1 y las dos escribirian 6: un punto perdido y dos personas con el
    mismo numero. El problema no esta en escribir, esta en el hueco entre leer
    y escribir.

    🔑 **Un candado para todos, no uno por persona.** Ahora que cada quien tiene
    su archivo, dos personas distintas ya no se pisan nunca — pero un candado
    unico sigue siendo correcto: solo hace esperar unos milisegundos a quien
    llegue segundo. Un diccionario de candados seria complejidad que nadie ha
    pedido, y candados que nadie borra nunca.

    :raises InvalidUserError: si el nombre no puede nombrar un archivo.
    :raises ScoreFileError: si el archivo existe pero no se puede interpretar.
        En ese caso el archivo queda intacto.
    """
    path = score_file(name, users_dir)

    with _SCORE_LOCK:
        total = read_score(name, users_dir) + 1
        path.parent.mkdir(parents=True, exist_ok=True)

        # Cada escritura estrena su propio temporal. Con un nombre fijo y
        # compartido, dos peticiones a la vez se lo quitan de las manos —una
        # renombrando mientras la otra sobrescribe— y Windows lo corta en seco
        # con un "Acceso denegado".
        #
        # `dir=path.parent` no es un detalle: el temporal tiene que nacer en la
        # MISMA carpeta que el definitivo. Renombrar solo es atomico dentro del
        # mismo disco; cruzando de disco deja de ser un renombrado y pasa a ser
        # copiar y borrar, que es justo lo que se esta evitando.
        handle, temporary_name = tempfile.mkstemp(
            dir=path.parent, prefix=f"{path.name}.", suffix=".tmp"
        )
        temporary = Path(temporary_name)

        try:
            # `mkstemp` devuelve el archivo ya abierto, a bajo nivel. `fdopen`
            # lo envuelve para poder escribirle texto, y el `with` lo cierra.
            # Cerrarlo antes de renombrar es obligatorio en Windows: no deja
            # mover un archivo que sigue abierto.
            with os.fdopen(handle, "w", encoding="utf-8") as file:
                file.write(json.dumps({"score": total}))

            # `os.replace` pisa el destino aunque ya exista, y lo hace igual en
            # Windows y en Linux. `Path.rename` no: en Windows revienta si el
            # destino existe.
            os.replace(temporary, path)
        except BaseException:
            # Si algo falla, el temporal no se queda de recuerdo. `BaseException`
            # y no `Exception` para que un Ctrl-C tambien limpie.
            temporary.unlink(missing_ok=True)
            raise

        return total
