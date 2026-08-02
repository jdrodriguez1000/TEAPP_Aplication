# Arquitectura — TEAPP

## El dibujo

```
   NAVEGADOR                    TU SERVIDOR
                           ┌──────────────────────────┐
   pantalla TS    ──────►  │  FastAPI (el portero)    │
                           │      ▼                   │
   ◄────  respuesta        │  el agente en Python     │
                           │      ▼                   │
                           │  API de Claude 💰        │
                           │  memoria de cada persona │
                           │  skills/*.md · registro  │
                           └──────────────────────────┘
                              ⬆ la llave vive AQUÍ
```

> 🔑 **FastAPI no es un framework de agentes: es un recepcionista.** Recibe texto
> de afuera, llama a una función tuya que ya existía, devuelve el resultado.

## Las dos piezas

| | Frontend | Backend |
|---|---|---|
| descartado | Next.js | Next.js (TS) — obligaría a reescribir el agente en TS |
| **elegido ✅** | **TypeScript puro** | **FastAPI (Python)** |

El agente ya existe en Python. Un backend en TypeScript significaría reescribirlo
entero para no ganar nada.

## Por qué TypeScript puro — sin React, Next.js ni Tailwind

1. **Next.js trae su propio servidor de Node.** Serían **dos** servidores
   encendidos en la nube en vez de uno, y la nube cobra por estar encendida. Con
   TS puro la pantalla son **archivos quietos** (`.html` + `.css` + `.js`).
2. **Una cosa nueva a la vez.** Este proyecto ya trae cinco (FastAPI, identidad,
   HTTP, la nube, despliegue). React sería la sexta, y es un tema entero.
3. 🔑 **React sin haber sufrido el problema que resuelve no se entiende.** Existe
   para no enloquecer actualizando la pantalla a mano.

📌 **Es la única decisión reversible del proyecto**, y por eso se tomó barata:
React/Next/Tailwind viven **dentro** de la caja "pantalla". No mueven la llave,
no tocan FastAPI, no tocan el agente.

**La señal para que React entre:** cuando `app.ts` se llene de *"borra esto,
pinta aquello, esconde lo otro"* y ya no sepas qué hay en pantalla. Ese dolor es
exactamente el que React quita. Antes de ese dolor, es burocracia.

## Dónde vive la llave

En el servidor. **Nunca en el navegador.**

Todo lo que llega al navegador el usuario lo puede leer — el HTML, el CSS, el
JavaScript, y cualquier cosa que viaje dentro. No hay forma de esconder algo ahí.

Por eso la pantalla **nunca** habla con la API de Claude. Habla con FastAPI, y
FastAPI es quien tiene la llave.

## Las dos memorias — no se confunden

| | qué guarda | ¿va a Git? |
|---|---|---|
| `_persistence/` | cómo se construyó el proyecto | **sí** |
| `data/` | lo que escriben las personas usando la app | **no** |

## Los permisos

El permiso interactivo de una terminal (*"¿autorizas esto? s/n"*) **no se
traduce: se sustituye.** En un servidor no hay teclado — y el problema de fondo
no es técnico: **quien usa la app no es dueño del servidor**, así que no tiene
con qué decidir.

> 🔑 En la terminal el freno pregunta **en el momento**. Aquí el freno se escribe
> **de antemano**: el código decide a qué archivo puede escribir cada persona.
> Es más fuerte, no más débil.

Y el criterio al escribirlos: **denegar por defecto**. Lo que no esté permitido
explícitamente, se rechaza. El olvido tiene que fallar hacia el lado seguro.
