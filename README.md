# TEAPP — Teaching English Application

Agente de IA para practicar inglés escrito, puesto en producción: navegador,
identidad, servidor propio y despliegue en la nube.

> Escribes una frase en inglés. El agente cuenta las palabras con Python, juzga
> la gramática con el modelo, responde en tono positivo, y lleva un marcador que
> sigue ahí mañana.

## Estado

**Paso 0 de 9** — repositorio y esqueleto. Todavía no hay código que correr.
El estado al día está en `_persistence/progress.md`.

## Cómo se corre

Nada todavía. Esta sección se llena en el paso 1.

## Estructura

| carpeta | qué guarda |
|---|---|
| `_context/` | qué es el proyecto: alcance, arquitectura, plan de pasos |
| `_persistence/` | cómo se está construyendo: avance, tareas, decisiones |
| `.claude/` | los agentes y protocolos de inicio y cierre de sesión |

## Stack

Backend **FastAPI** (Python) · Frontend **TypeScript puro** · Modelo **Claude**.

El detalle y el porqué están en `_context/architecture.md`.

## Configuración

Copia `.env.example` como `.env` y pon tu llave.
⚠️ `.env` nunca se sube al repositorio.
