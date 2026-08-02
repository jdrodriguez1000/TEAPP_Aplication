# TEAPP — Teaching English Application

Agente de IA para practicar inglés escrito, puesto en producción: navegador,
identidad, servidor propio y despliegue en la nube.

> Escribes una frase en inglés. El agente cuenta las palabras con Python, juzga
> la gramática con el modelo, responde en tono positivo, y lleva un marcador que
> sigue ahí mañana.

## Estado

**Paso 2 de 9** — el agente corre detrás de un servidor FastAPI, además de en la
terminal. Las dos puertas dan el mismo resultado.

⚠️ El agente es **falso** a propósito: `judge_grammar` devuelve siempre el mismo
texto sin mirar la frase. El modelo se enchufa en el paso 8, y hasta entonces el
proyecto no cuesta un centavo. El porqué está en `_context/roadmap.md`.

El estado al día está en `_persistence/progress.md`.

## Cómo se corre

**La primera vez**, se crea el entorno virtual y se instalan las dependencias.
Un entorno virtual es una caja de librerías propia del proyecto: lo que se
instale aquí dentro no toca al resto de la máquina.

```bash
python -m venv .venv
```

Después se activa. El comando cambia según dónde estés:

| dónde | comando |
|---|---|
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (Git Bash) | `source .venv/Scripts/activate` |
| macOS / Linux | `source .venv/bin/activate` |

Sabes que está activo porque el prompt pasa a empezar por `(.venv)`. Con él
activo:

```bash
pip install -r requirements.txt
```

**Cada vez**, con el entorno activado, hay dos puertas de entrada. Dan el mismo
resultado: por dentro llaman al mismo agente.

⚠️ **Una a la vez, no las dos.** Las dos escriben el mismo `data/score.json`, y
el candado que protege el marcador solo existe dentro de un proceso. Con la
terminal y el servidor encendidos a la vez son dos procesos, cada uno con su
candado, y los puntos se pierden. Está anotado como suposición `A-002` en
`_persistence/assumptions.md`.

### La terminal

```bash
python main.py
```

Escribe una frase en inglés y pulsa Enter. Para salir, Enter en una línea vacía.

```
> I like coffee
Nice work! That sentence looks correct to me.
Words: 3
Score: 1
```

### El servidor

```bash
python -m uvicorn app.api:app --reload
```

La terminal se queda **quieta, ocupada**. No está colgada: está escuchando. Para
apagarlo, `Ctrl + C`.

Con el servidor encendido, abre en el navegador:

```
http://127.0.0.1:8000/docs
```

Esa página la genera FastAPI sola a partir del código. Sirve para probar la ruta
sin escribir comandos: **POST /practice** → *Try it out* → escribe la frase →
*Execute*.

> `127.0.0.1` es tu propia máquina. Ese servidor no está en internet y nadie más
> lo ve. Salir a internet es el paso 7.

⚠️ **Arráncalo sin `--workers`, y con `main.py` cerrado.** Es la misma regla de
arriba: el candado del marcador solo existe dentro de un proceso. Varios
workers, o la terminal encendida al mismo tiempo, son varios procesos con un
candado cada uno — y los puntos se vuelven a perder. Suposición `A-002`.

El `--reload` es comodidad de desarrollo: reinicia solo al cambiar el código. En
la nube no se usa.

El marcador se guarda en `data/score.json`, escriba quien escriba, y sigue ahí la
próxima vez.

## Los tests

```bash
python -m pytest
```

## Estructura

| carpeta | qué guarda |
|---|---|
| `main.py` | la terminal. El único archivo del proyecto con `input()` |
| `app/api.py` | el servidor FastAPI. Una ruta: `POST /practice`. 🚨 Aquí no puede haber `input()`: no hay teclado detrás |
| `app/` | el agente y sus herramientas |
| `tests/` | los tests |
| `data/` | el marcador de quien usa la app. **No va a Git** |
| `_context/` | qué es el proyecto: alcance, arquitectura, plan de pasos |
| `_persistence/` | cómo se está construyendo: avance, tareas, decisiones |
| `.claude/` | los agentes y protocolos de inicio y cierre de sesión |

> 🔑 `respond(sentence) -> TutorReply`, en `app/english_tutor.py`, es la junta
> del proyecto: entra un texto, salen tres piezas sueltas —veredicto, palabras y
> marcador—. La llaman `main.py` y FastAPI, y el agente no se entera de cuál de
> los dos fue. Quien junta las piezas en un texto es quien las va a mostrar.

## Stack

Backend **FastAPI** (Python) · Frontend **TypeScript puro** · Modelo **Claude**.

El detalle y el porqué están en `_context/architecture.md`.

## Configuración

Copia `.env.example` como `.env` y pon tu llave.
⚠️ `.env` nunca se sube al repositorio.

Todavía no hace falta: hasta el paso 8 no se llama al modelo.
