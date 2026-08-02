# TEAPP — Teaching English Application

Agente de IA para practicar inglés escrito, puesto en producción: navegador,
identidad, servidor propio y despliegue en la nube.

> Escribes una frase en inglés. El agente cuenta las palabras con Python, juzga
> la gramática con el modelo, responde en tono positivo, y lleva un marcador que
> sigue ahí mañana.

## Estado

**Paso 1 de 9** — el agente corre en la terminal, con sus tres herramientas.

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

**Cada vez**, con el entorno activado:

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

El marcador se guarda en `data/score.json` y sigue ahí la próxima vez.

## Los tests

```bash
python -m pytest
```

## Estructura

| carpeta | qué guarda |
|---|---|
| `main.py` | la terminal. El único archivo con `input()`; muere en el paso 2 |
| `app/` | el agente y sus herramientas |
| `tests/` | los tests |
| `data/` | el marcador de quien usa la app. **No va a Git** |
| `_context/` | qué es el proyecto: alcance, arquitectura, plan de pasos |
| `_persistence/` | cómo se está construyendo: avance, tareas, decisiones |
| `.claude/` | los agentes y protocolos de inicio y cierre de sesión |

> 🔑 `respond(sentence) -> str`, en `app/english_tutor.py`, es la junta del
> proyecto: entra un texto, sale un texto. Hoy la llama `main.py`; en el paso 2
> la llamará FastAPI sin que el agente se entere.

## Stack

Backend **FastAPI** (Python) · Frontend **TypeScript puro** · Modelo **Claude**.

El detalle y el porqué están en `_context/architecture.md`.

## Configuración

Copia `.env.example` como `.env` y pon tu llave.
⚠️ `.env` nunca se sube al repositorio.

Todavía no hace falta: hasta el paso 8 no se llama al modelo.
