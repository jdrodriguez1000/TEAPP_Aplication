"""El cuaderno de la app: una línea por práctica servida.

🚨 **Guarda la FORMA de la práctica, nunca la frase.** Cuántas palabras tenía,
qué marcador quedó, cuánto tardó, qué modelo contestó. La frase que escribió la
persona **no entra aquí y no entra en ningún sitio de este repo** ([D-085],
`PI-8`).

## Por qué existe

Hasta hoy el log solo apuntaba lo que iba mal: averías, frenos, timeouts. La
práctica que funciona terminaba en `return` sin dejar rastro, así que **el suceso
más frecuente de la aplicación era invisible** — no se podía contestar "¿está
usando esto alguien?" ni "¿cuánto tarda de normal?" sin adivinar.

## Los dos registros se cubren el uno al otro

🔑 Esta es la idea entera, y viene de [D-086]:

    este archivo (trace.jsonl) ... cuenta el CASO FELIZ
    el logger de prosa ........... cuenta cuando ESTE se rompe

Cada uno ve el punto ciego del otro. Por eso `record` **no se calla sus fallos**:
los lanza, y quien llama decide. Un instrumento que falla en silencio no da un
dato falso, da silencio — y el silencio se lee como confirmación (`LM.15`, que
nació en TEAPP cerrando `T-054`).

⚠️ **El corolario, y va escrito porque tiene un coste:** al lanzar, la red de
seguridad vive en quien llama, no aquí. Hoy hay **un solo sitio que llama** —la
ruta de `/practice`— y su `except` está a la vista. Si algún día hay dos, esto
pasa a ser algo que hay que acordarse de envolver, y entonces toca revisar la
decisión en vez de repetir el `try`.

## Por qué no hay excepción propia

`quota.py` y `tools.py` tienen la suya —`QuotaFileError`, `ScoreFileError`—
porque la puerta de red **necesita distinguir** "el contador está roto" de otro
fallo cualquiera: una cosa devuelve 500 y la otra no.

Aquí no hay nada que distinguir: **la política es la misma para todos los
fallos** —disco lleno, permisos, un valor que `json` no sabe serializar—, y es
"no propagar, apuntarlo en el log". Una excepción propia solo añadiría una capa
que nadie mira. `PI-2`.
"""

import json
from datetime import datetime, timezone
from pathlib import Path

from app.config import trace_file

# El nombre del modelo se importa de donde ya vive, en vez de repetirlo. Si algún
# día cambia —y [D-049] tiene programados dos cambios en el paso 9—, la traza
# dice el nuevo sin que nadie se acuerde de tocarla.
from app.tools import MODEL_NAME


def record(
    user: str,
    words: int,
    score: int,
    practice: int,
    correct: bool,
    seconds: float,
    model: str = MODEL_NAME,
    at: datetime | None = None,
    path: Path | None = None,
) -> None:
    """Apunta una práctica servida. Una línea, en modo añadir.

    🚨 **Puede fallar, y falla hacia fuera.** No hay `try` aquí dentro: ver el
    módulo. Quien llama es responsable de que un cuaderno roto no se coma la
    práctica de nadie.

    :param user: quién practicó. Es el nombre de la cuenta, no la frase.
    :param words: cuántas palabras tenía la frase. **La forma, no el contenido.**
    :param score: frases correctas acumuladas, después de anotar esta ([D-066]).
    :param practice: frases practicadas en total, acertadas o no.
    :param correct: si ESTA frase estaba bien. 🚨 **Es la mitad de máquina del
        veredicto, no el veredicto.** El texto del juez puede citar la frase de la
        persona dentro, así que no entra aquí ni en ningún archivo (`PI-8`).
    :param seconds: cuánto tardó el tutor, medido en la ruta con reloj de pared.
    :param model: qué modelo contestó. Por defecto el que usa el tutor hoy.
    :param at: cuándo, en UTC. Se inyecta solo en los tests.
    :param path: dónde escribir. Se inyecta solo en los tests; en producción sale
        de `config.trace_file()`, que resuelve la raíz en cada llamada.
    """
    # 🔑 **UTC y no la hora local, y no es un detalle.** El servidor está en la
    # nube y esta máquina no; dos renglones con la hora de sitios distintos no se
    # pueden ordenar entre sí. Es la misma disciplina que las lecturas de costo:
    # la hora se anota, y se anota en una sola zona.
    moment = at or datetime.now(timezone.utc)

    destination = path or trace_file()

    # `sort_keys` para que dos líneas del mismo tipo salgan con las claves en el
    # mismo orden: asi un `diff` entre dos dias enseña lo que cambio de verdad y
    # no un baile de campos.
    line = json.dumps(
        {
            "at": moment.isoformat(),
            "user": user,
            "words": words,
            "score": score,
            "practice": practice,
            "correct": correct,
            "seconds": round(seconds, 3),
            "model": model,
        },
        sort_keys=True,
    )

    # 🔑 **Modo añadir, y sin el baile del archivo temporal que usa `quota.py`.**
    # Allí se reescribe el archivo ENTERO, así que un corte a medias lo deja
    # vacío y hay que cambiarlo de golpe con `os.replace`. Aquí solo se pega una
    # línea corta al final: si el proceso muere en mitad de la escritura se
    # pierde esa línea, y perder el último apunte del cuaderno no rompe nada.
    #
    # ⚠️ **El `\n` va al final y no al principio**, a propósito: con un archivo
    # que ya termina en salto, empezar por `\n` dejaría una línea vacía entre
    # cada dos apuntes y `json.loads` reventaría al leerlas.
    with open(destination, "a", encoding="utf-8") as file:
        file.write(line + "\n")
