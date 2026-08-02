# Los 10 pasos — TEAPP

> 🔑 **La tubería completa se construye y se prueba con un agente FALSO. El
> modelo se enchufa al final** (paso 8 de 9).

Un *agente falso* es una función de Python que devuelve siempre lo mismo, sin
llamar a Claude. La razón **no es el dinero**: el modelo es la única pieza que no
responde igual dos veces. Sacarlo del camino mientras construyes lo demás quita
la variable ruidosa — cuando algo falle, no habrá que preguntarse si fue el
modelo.

| # | Paso | Qué rompe / qué enseña | Costo |
|---|---|---|---|
| **0** | Repo y esqueleto: `git init`, `CLAUDE.md`, `_context/`, `_persistence/` | se monta el protocolo | $0 |
| 1 | El agente en terminal, **falso**. Las 3 herramientas | dominio nuevo, técnica conocida | $0 |
| 2 | **FastAPI** encima. Una ruta, local, mismo resultado que el paso 1 | 🚨 muere la espera a un humano | $0 |
| 3 | **La pantalla**: `index.html` + `app.ts` contra FastAPI local | el navegador entra | $0 |
| 4 | **Memoria por persona** | 🚨 se rompe "hay un solo usuario" | $0 |
| 5 | **Identidad** | requisito de despliegue, no adorno | $0 |
| 6 | **Frenos de producción**: tope por persona y por día, timeouts | 🚨 se rompe "existe la corrida" | $0 |
| 7 | **La nube.** ⚠️ **alarma de facturación PRIMERO**, luego subir | la tubería entera, todavía falsa | $0 |
| 8 | **Enchufar el modelo.** Se borra el agente falso | 💰 el primero |
| 9 | **Observabilidad y evals** con rúbrica | bajo |

**Hasta el paso 7 —TEAPP en internet, con URL pública— no cuesta un centavo.**

## Dos cosas del orden que no son casualidad

1. **El paso 8 cae casi al final.** Si algo falla ahí, la puerta, la pantalla, la
   identidad, la memoria, los frenos y el despliegue funcionaban ayer. **El
   sospechoso queda solo.**
2. **La nube va en el 7, no en el 1.** El plan gratuito corre **6 meses desde el
   día que se abre la cuenta**, se use o no. Los pasos 0 a 6 se hacen enteros en
   la máquina local; el día que se abra la cuenta, ya habrá algo que subir.

## Una regla al terminar cada paso

Antes de pasar al siguiente, **córrelo**. Un paso no está terminado porque el
código exista: está terminado cuando lo viste funcionar.

📌 **En qué paso vamos** → `_persistence/progress.md`. Aquí no, para que no mienta.
