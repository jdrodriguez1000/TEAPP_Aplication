"use strict";
// La pantalla de TEAPP. Lee la frase, se la manda al servidor y pinta las tres
// piezas que contesta.
//
// 🔑 Este es el archivo que se EDITA. El que el navegador lee es
// `app/static/app.js`, y lo escribe el compilador: si lo editas a mano, la
// siguiente compilada se lleva tus cambios por delante.
//
// ⚠️ Aqui no hay ninguna llave, y no puede haberla. Todo lo que llega al
// navegador se puede leer. Quien habla con Claude es el servidor.
/** Busca un elemento del HTML y falla claro si no esta.
 *
 * `getElementById` devuelve el elemento O `null`, porque nadie le garantiza que
 * ese `id` exista. Con `strict` encendido, TypeScript no deja seguir sin
 * resolver ese `null` — y hace bien: si el `id` se escribio mal, es mejor un
 * error que dice cual falta que una pantalla muerta sin explicacion.
 */
function requireElement(id) {
    const element = document.getElementById(id);
    if (element === null) {
        throw new Error(`Falta el elemento #${id} en index.html`);
    }
    return element;
}
const practiceForm = requireElement("practice-form");
const sentenceInput = requireElement("sentence");
const sendButton = requireElement("send");
const verdictBox = requireElement("verdict");
const wordsBox = requireElement("words");
const scoreBox = requireElement("score");
const errorBox = requireElement("error");
/** Muestra un error a quien esta usando la app, y limpia la respuesta vieja.
 *
 * Dejar el veredicto anterior en pantalla junto a un error seria peor que no
 * mostrar nada: parece que la frase nueva se juzgo, y no se juzgo.
 */
function showError(message) {
    errorBox.textContent = message;
    verdictBox.textContent = "";
}
/** Saca el mensaje de error de lo que contesto el servidor.
 *
 * FastAPI contesta `{"detail": ...}`, pero el `detail` no siempre es texto:
 * cuando lo rechaza la validacion (422) es una lista de objetos. Volcarla tal
 * cual pintaria "[object Object]" en la cara de quien pregunta.
 */
async function readErrorMessage(response) {
    try {
        const body = await response.json();
        if (typeof body === "object" &&
            body !== null &&
            "detail" in body &&
            typeof body.detail === "string") {
            return body.detail;
        }
    }
    catch {
        // El cuerpo no era JSON. No pasa nada: abajo hay un mensaje de repuesto.
    }
    return "El servidor no acepto la frase. Intenta de nuevo.";
}
/** Pinta las tres piezas, cada una en su sitio.
 *
 * Por esto [D-008] hizo que el servidor mandara los ingredientes y no el plato
 * servido: con un texto ya cocinado, esta funcion solo podria volcarlo entero.
 */
function showReply(reply) {
    errorBox.textContent = "";
    verdictBox.textContent = reply.verdict;
    wordsBox.textContent = String(reply.words);
    scoreBox.textContent = String(reply.score);
}
practiceForm.addEventListener("submit", async (event) => {
    // Sin esto el navegador recarga la pagina entera al enviar el formulario, que
    // es lo que hacian los formularios antes de que existiera `fetch`.
    event.preventDefault();
    const sentence = sentenceInput.value.trim();
    if (sentence === "") {
        showError("Escribe una frase primero.");
        return;
    }
    // Se apaga el boton mientras se espera. Sin esto, diez clics seguidos son diez
    // peticiones y diez puntos sumados por una sola frase.
    sendButton.disabled = true;
    try {
        // Ruta relativa, sin `http://localhost:8000` delante. Funciona igual en tu
        // maquina y en la nube porque la pantalla y el servidor son el MISMO
        // origen: el mismo FastAPI entrega este archivo y atiende /practice. Por
        // eso no hizo falta configurar CORS — ver [D-011].
        const response = await fetch("/practice", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ sentence: sentence }),
        });
        if (!response.ok) {
            showError(await readErrorMessage(response));
            return;
        }
        showReply((await response.json()));
    }
    catch {
        // Aqui se cae cuando la peticion ni siquiera llego: servidor apagado, cable
        // desconectado. No hay respuesta que leer, asi que no hay detalle que dar.
        showError("No se pudo hablar con el servidor. Revisa que este encendido.");
    }
    finally {
        // `finally` corre pase lo que pase. Sin el, un fallo dejaria el boton
        // apagado para siempre y habria que recargar la pagina.
        sendButton.disabled = false;
    }
});
