# TEAPP — Teaching English Application

Agente de IA para practicar inglés escrito, puesto en producción: navegador,
identidad, servidor propio y despliegue en la nube.

> Escribes una frase en inglés. El agente cuenta las palabras con Python, juzga
> la gramática con el modelo, responde en tono positivo, y lleva un marcador que
> sigue ahí mañana.

## Estado

**Paso 5 de 9** — la identidad se comprueba de verdad. Cada persona tiene su
cuenta con contraseña y su propio marcador, y el servidor solo atiende a quien
enseña una sesión firmada por él. El mismo FastAPI entrega la pantalla y atiende
la ruta del agente. La terminal sigue funcionando: las dos puertas dan el mismo
resultado, y comparten las mismas cuentas.

⚠️ El agente es **falso** a propósito: `judge_grammar` devuelve siempre el mismo
texto sin mirar la frase, y **nada valida que lo escrito sea inglés** — solo se
rechaza la frase vacía. El modelo se enchufa en el paso 8, y hasta entonces el
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

Y una sola vez también, el compilador de la pantalla. Necesita Node instalado:

```bash
npm install
```

**Cada vez**, con el entorno activado, hay dos puertas de entrada. Dan el mismo
resultado: por dentro llaman al mismo agente.

⚠️ **Una a la vez, no las dos** — si vas a practicar con el mismo nombre en las
dos. Cada persona tiene su archivo (`data/users/<nombre>.json`), así que dos
personas distintas ya no se estorban; pero el mismo nombre desde la terminal y
desde el servidor son dos procesos con un candado cada uno, y los puntos de esa
persona se pierden. Está anotado como suposición `A-002` en
`_persistence/assumptions.md`.

### La terminal

```bash
python main.py
```

Primero pide tu nombre y tu contraseña —una vez, al arrancar— y luego lee
frases. Si el nombre es nuevo, te crea la cuenta ahí mismo. Para salir, Enter en
una línea vacía.

🔑 **Es la misma cuenta que la del navegador**, porque hay un solo almacén de
credenciales y no uno por puerta.

```
Your name: juan
Password:

> I like coffee
Nice work! That sentence looks correct to me.
Words: 3
Score: 1
```

### El navegador

Dos comandos, en este orden:

```bash
npm run build
```

```bash
python -m uvicorn app.api:app --reload
```

El primero traduce la pantalla de TypeScript a JavaScript. El segundo enciende el
servidor. Después, abre en el navegador:

```
http://127.0.0.1:8000/
```

La primera vez, escribe un nombre y una contraseña y pulsa **Create account**.
Después ya entras con **Log in**. Con la sesión abierta, escribe una frase y
pulsa **Send**: aparecen el veredicto, las palabras y tu marcador.

🔑 **El nombre ya no viaja con la frase.** Quien practica sale de una cookie que
firma el servidor, así que no se puede escribir el nombre de otra persona para
quedarse con su marcador — que es justo lo que sí se podía hacer en el paso 4.
Ver `D-021` y `D-013`.

⚠️ **Hace falta el `.env` con `TEAPP_SECRET_KEY` y `TEAPP_DATA_DIR`.** Sin llave
el servidor se niega a firmar y contesta un 500; sin la carpeta de datos **no
arranca siquiera**. Están en la sección *Configuración*, al final.

La terminal del segundo comando se queda **quieta, ocupada**. No está colgada:
está escuchando, y va escribiendo cada petición que recibe. Para apagarlo,
`Ctrl + C`. Si quieres recompilar sin apagar el servidor, abre una **segunda
terminal**.

#### Qué hay que volver a correr, y cuándo

> 🔑 **`npm run build` solo traduce TypeScript.** Nada más pasa por él.

| si cambias… | qué haces |
|---|---|
| `frontend/*.ts` | `npm run build` y recargas el navegador |
| `app/static/index.html` | solo recargas. El HTML no se compila |
| `app/*.py` | se reinicia el servidor — con `--reload` lo hace solo |

⚠️ **El error previsible:** editar el `.ts` y olvidar compilar. El navegador
sigue con el `.js` viejo, tu código correcto no hace nada, y se busca el fallo en
el sitio equivocado. `npm run watch` deja el compilador vigilando y traduce solo
al guardar.

Si compilaste, recargaste y sigue igual, prueba `Ctrl + F5`: recarga ignorando lo
que el navegador tenga guardado del archivo anterior.

#### La página de FastAPI

```
http://127.0.0.1:8000/docs
```

La genera FastAPI sola a partir del código. Sirve para probar la ruta sin la
pantalla: **POST /practice** → *Try it out* → escribe la frase → *Execute*. Útil
para saber si un fallo está en el servidor o en el navegador.

> `127.0.0.1` es tu propia máquina. Ese servidor no está en internet y nadie más
> lo ve. Salir a internet es el paso 7.

⚠️ **Arráncalo sin `--workers`, y con `main.py` cerrado.** Es la misma regla de
arriba: el candado del marcador solo existe dentro de un proceso. Varios
workers, o la terminal encendida al mismo tiempo, son varios procesos con un
candado cada uno — y los puntos de quien coincida en los dos se vuelven a
perder. Suposición `A-002`.

El `--reload` es comodidad de desarrollo: reinicia solo al cambiar el código. En
la nube no se usa.

Cada persona tiene su marcador en `data/users/<nombre>.json`, y sigue ahí la
próxima vez.

El nombre se normaliza antes de tocar el disco —minúsculas y sin espacios de
sobra, así que `Juan` y `juan` son la misma persona— y solo admite letras sin
tilde, números, guion y guion bajo. Lo demás se rechaza con un 422, porque con
ese nombre se construye una ruta de archivo. Ver `D-014`.

## Los tests

```bash
python -m pytest
```

## Estructura

| carpeta | qué guarda |
|---|---|
| `main.py` | la terminal. El único archivo del proyecto con `input()` |
| `app/api.py` | el servidor FastAPI. Entrega la pantalla (`GET /`), la identidad (`/register`, `/login`, `/logout`, `/me`) y el agente (`POST /practice`). 🚨 Aquí no puede haber `input()`: no hay teclado detrás |
| `app/accounts.py` | quién existe y cómo se comprueba. **La única autoridad sobre quién existe** |
| `app/sessions.py` | la tarjeta firmada: se reparte al entrar y se reconoce en cada petición |
| `app/config.py` | de dónde salen los secretos. 🚨 Ninguno se escribe en el código |
| `app/` | el agente y sus herramientas |
| `frontend/` | el código de la pantalla en TypeScript. **Es lo que se edita** |
| `app/static/` | lo que el navegador recibe: el `index.html`, y el `app.js` que **escribe el compilador** — editarlo a mano se pierde en la siguiente compilada |
| `tests/` | los tests |
| `data/users/` | un marcador por persona, `<nombre>.json`. **No va a Git** |
| `data/accounts.json` | las credenciales, con la contraseña cifrada de ida. **No va a Git**. Archivo aparte del marcador a propósito: dos cosas con vidas distintas no comparten archivo |
| `_context/` | qué es el proyecto: alcance, arquitectura, plan de pasos |
| `_persistence/` | cómo se está construyendo: avance, tareas, decisiones |
| `.claude/` | los agentes y protocolos de inicio y cierre de sesión |

> 🔑 `respond(sentence, user) -> TutorReply`, en `app/english_tutor.py`, es la junta
> del proyecto: entra un texto, salen tres piezas sueltas —veredicto, palabras y
> marcador—. La llaman `main.py` y FastAPI, y el agente no se entera de cuál de
> los dos fue. Quien junta las piezas en un texto es quien las va a mostrar.

## Stack

Backend **FastAPI** (Python) · Frontend **TypeScript puro**, compilado con `tsc`
· Modelo **Claude**.

Sin React, sin Next.js, sin Tailwind. Node solo compila en tu máquina: **no se
despliega**, así que en la nube se enciende un servicio y no dos.

La pantalla y el servidor son el **mismo origen** —un solo FastAPI para las dos
cosas—, por eso no hay nada de CORS que configurar.

El detalle y el porqué están en `_context/architecture.md`.

## Configuración

Copia `.env.example` como `.env`. ⚠️ `.env` nunca se sube al repositorio.

| variable | hace falta | para qué |
|---|---|---|
| `TEAPP_SECRET_KEY` | **sí, desde el paso 5** | firmar las sesiones |
| `TEAPP_DATA_DIR` | **sí, desde el paso 7** | dónde se guardan cuentas, marcadores y cuota |
| `TEAPP_COOKIE_SECURE` | en local, `false` | ver abajo |
| `ANTHROPIC_API_KEY` | todavía no, entra en el paso 8 | hablar con el modelo |

🚨 **`TEAPP_DATA_DIR` va con ruta ABSOLUTA a una carpeta que ya exista**, y sin
ella la app **no arranca**. No tiene valor por defecto a propósito: cuando lo
tenía, un script que importara la app y se olvidara de desviarlo escribía en los
datos de personas de verdad sin decir nada. Ver `[D-037]` y `[L-023]`.

⚠️ Una ruta relativa se **rechaza**, no se resuelve: se resolvería contra la
carpeta desde la que arrancaste, y el mismo programa escribiría en sitios
distintos según desde dónde se lance. Y la carpeta **no se crea sola**: una ruta
mal escrita se convertiría en un `data/` vacío donde todo el mundo parece haber
perdido su marcador, sin ningún error.

```
TEAPP_DATA_DIR=C:\ruta\hasta\TEAPP\data
```

La llave de firma se genera así, y se pega en el `.env`:

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

⚠️ **Si esa llave cambia, todas las sesiones abiertas mueren y todo el mundo
tiene que volver a entrar.** No es un fallo: es cómo funciona una firma. Nadie
pierde su cuenta ni su marcador. Anotado como `A-008`.

⚠️ **`TEAPP_COOKIE_SECURE=false` en local, y solo en local.** Por defecto vale
`true`, que es lo seguro y lo que hay que usar en la nube. Pero el navegador
**descarta en silencio** una cookie `Secure` que llega por `http://localhost`:
el inicio de sesión parecería no hacer nada, sin ningún error. El servidor
escribe al arrancar cuál de los dos modos tiene activo, justo para no buscarlo a
ciegas.
