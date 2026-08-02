# Alcance — TEAPP v1

## Qué hace

> Escribes una frase en inglés. El agente **cuenta las palabras con Python**,
> **juzga la gramática con el modelo**, responde en tono positivo, y lleva un
> marcador que sigue ahí mañana. En el navegador, con identidad, desde AWS.

Tres herramientas, y cada una hace un trabajo distinto:

| herramienta | quién la ejecuta | por qué así |
|---|---|---|
| contar palabras | **Python**, sin modelo | lo que tiene una sola respuesta correcta no se le pide al modelo |
| juzgar gramática | **el modelo**, con rúbrica | no hay `if` que juzgue una frase |
| marcador | un archivo | tiene que seguir ahí mañana |

## Qué entra y qué no

| Entra en la v1 | Fuera de la v1 |
|---|---|
| nivel **A1**, tres temas | los niveles A2 a C2 |
| **escrito** | la voz |
| **3** herramientas | los 25 temas |
| memoria por persona | preguntas sorpresa, repaso express |

## Cómo se decide un caso dudoso

Pregunta: **¿esto es necesario para que la tubería completa funcione en
producción?** Si no, es v2.

> 🔑 **Este proyecto no trata sobre el agente. Trata sobre lo que lo rodea:** la
> puerta, la pantalla, la identidad, la memoria, los frenos y el despliegue.

Un agente más grande no enseñaría nada nuevo, y llegaría al despliegue sin
fuerzas. El agente es pequeño **a propósito**.
