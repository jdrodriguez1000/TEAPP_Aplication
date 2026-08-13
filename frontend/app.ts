// La pantalla de TEAPP. Identifica a quien practica, lee la frase, se la manda
// al servidor y pinta las tres piezas que contesta.
//
// 🔑 Este es el archivo que se EDITA. El que el navegador lee es
// `app/static/app.js`, y lo escribe el compilador: si lo editas a mano, la
// siguiente compilada se lleva tus cambios por delante.
//
// ⚠️ Aqui no hay ninguna llave, y no puede haberla. Todo lo que llega al
// navegador se puede leer. Quien habla con Claude es el servidor.
//
// 🚨 **Y aqui tampoco hay identidad.** La sesion vive en una cookie `HttpOnly`,
// que este archivo NO puede leer — a proposito. Esa es la diferencia con el
// `localStorage` del paso 4, que cualquier script leia. Este codigo no sabe
// quien eres: se lo pregunta al servidor con `GET /me`. Ver [D-021].

/** Las tres piezas que devuelve el servidor.
 *
 * Es el mismo contrato que `PracticeResponse` en `app/api.py`, escrito aqui
 * para que TypeScript pueda avisar. Sin esto, `reply.verdcit` —con la `i` y la
 * `c` cambiadas— no seria un error: valdria `undefined` y la pantalla mostraria
 * la palabra "undefined" sin explotar. Ese es justo el fallo que se compro
 * evitar al elegir TypeScript.
 */
interface PracticeResponse {
  verdict: string;
  words: number;
  /** Frases CORRECTAS. Desde [D-066] ya no cuenta practicas. */
  score: number;
  /** Frases practicadas, acertadas o no. */
  practice: number;
}

/** Quien eres, segun el servidor. El mismo contrato que `MeResponse`. */
interface MeResponse {
  user: string;
}

/** Busca un elemento del HTML y falla claro si no esta.
 *
 * `getElementById` devuelve el elemento O `null`, porque nadie le garantiza que
 * ese `id` exista. Con `strict` encendido, TypeScript no deja seguir sin
 * resolver ese `null` — y hace bien: si el `id` se escribio mal, es mejor un
 * error que dice cual falta que una pantalla muerta sin explicacion.
 */
function requireElement<T extends HTMLElement>(id: string): T {
  const element = document.getElementById(id);
  if (element === null) {
    throw new Error(`Falta el elemento #${id} en index.html`);
  }
  return element as T;
}

const signedOutBox = requireElement<HTMLElement>("signed-out");
const signedInBox = requireElement<HTMLElement>("signed-in");
const signinForm = requireElement<HTMLFormElement>("signin-form");
const userInput = requireElement<HTMLInputElement>("user");
const passwordInput = requireElement<HTMLInputElement>("password");
const loginButton = requireElement<HTMLButtonElement>("login");
const registerButton = requireElement<HTMLButtonElement>("register");
const logoutButton = requireElement<HTMLButtonElement>("logout");
const whoamiBox = requireElement<HTMLElement>("whoami");
const practiceForm = requireElement<HTMLFormElement>("practice-form");
const sentenceInput = requireElement<HTMLInputElement>("sentence");
const sendButton = requireElement<HTMLButtonElement>("send");
const verdictBox = requireElement<HTMLParagraphElement>("verdict");
const wordsBox = requireElement<HTMLSpanElement>("words");
const scoreBox = requireElement<HTMLSpanElement>("score");
const practiceBox = requireElement<HTMLSpanElement>("practice");
const errorBox = requireElement<HTMLParagraphElement>("error");

/** Muestra un error a quien esta usando la app, y limpia la respuesta vieja.
 *
 * Dejar el veredicto anterior en pantalla junto a un error seria peor que no
 * mostrar nada: parece que la frase nueva se juzgo, y no se juzgo.
 */
function showError(message: string): void {
  errorBox.textContent = message;
  verdictBox.textContent = "";
}

/** Saca el mensaje de error de lo que contesto el servidor.
 *
 * FastAPI contesta `{"detail": ...}`, pero el `detail` no siempre es texto:
 * cuando lo rechaza la validacion (422) es una lista de objetos. Volcarla tal
 * cual pintaria "[object Object]" en la cara de quien pregunta.
 */
async function readErrorMessage(response: Response): Promise<string> {
  try {
    const body: unknown = await response.json();
    if (
      typeof body === "object" &&
      body !== null &&
      "detail" in body &&
      typeof (body as { detail: unknown }).detail === "string"
    ) {
      return (body as { detail: string }).detail;
    }
  } catch {
    // El cuerpo no era JSON. No pasa nada: abajo hay un mensaje de repuesto.
  }
  return "El servidor no acepto la peticion. Intenta de nuevo.";
}

/** Ensena la mitad de la pantalla que toca segun quien seas.
 *
 * 🔑 **Esto es comodidad, no seguridad.** Esconder el formulario de practicar
 * no impide practicar: cualquiera puede llamar a `/practice` con `curl` sin
 * pasar por aqui. Quien de verdad frena es el 401 del servidor. Lo de aqui solo
 * evita ensenar una casilla que no iba a funcionar.
 */
function showAs(user: string | null): void {
  const signedIn = user !== null;

  signedInBox.hidden = !signedIn;
  signedOutBox.hidden = signedIn;
  whoamiBox.textContent = user ?? "";

  if (!signedIn) {
    // Al salir se limpia el marcador de la pantalla. Dejarlo puesto le mostraria
    // a la siguiente persona los puntos de la anterior.
    wordsBox.textContent = "—";
    scoreBox.textContent = "—";
    practiceBox.textContent = "—";
    verdictBox.textContent = "";
  }
}

/** Le pregunta al servidor quien eres. Es la unica forma que tiene la pantalla.
 *
 * La cookie es `HttpOnly`, asi que este codigo no la puede leer ni de lejos.
 * Y esta bien que sea asi: si la pudiera leer, tambien podria leerla cualquier
 * script que se colara en la pagina.
 */
async function whoAmI(): Promise<string | null> {
  try {
    const response = await fetch("/me");
    if (!response.ok) {
      return null;
    }
    return ((await response.json()) as MeResponse).user;
  } catch {
    return null;
  }
}

/** Manda el nombre y la contrasena a `/login` o a `/register`. */
async function signIn(route: "/login" | "/register"): Promise<void> {
  // Aqui solo se comprueba que no esten vacios. El resto de las reglas —el
  // largo, los caracteres, si el nombre esta cogido— las aplica el servidor y
  // solo el servidor: lo que corre en el navegador se puede saltar, asi que
  // repetirlas aqui daria una sensacion de freno que no es real ([D-014]).
  const user = userInput.value.trim();
  if (user === "") {
    showError("Escribe tu nombre primero.");
    return;
  }

  const password = passwordInput.value;
  if (password === "") {
    showError("Escribe tu contrasena primero.");
    return;
  }

  loginButton.disabled = true;
  registerButton.disabled = true;
  try {
    const response = await fetch(route, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user: user, password: password }),
    });

    if (!response.ok) {
      showError(await readErrorMessage(response));
      return;
    }

    // 🚨 La contrasena se borra de la casilla en cuanto deja de hacer falta.
    // Escrita ahi se queda visible en el DOM el resto de la visita, y viaja en
    // cualquier volcado de la pagina.
    passwordInput.value = "";
    errorBox.textContent = "";

    showAs(((await response.json()) as MeResponse).user);
  } catch {
    showError("No se pudo hablar con el servidor. Revisa que este encendido.");
  } finally {
    loginButton.disabled = false;
    registerButton.disabled = false;
  }
}

signinForm.addEventListener("submit", async (event: SubmitEvent) => {
  // Sin esto el navegador recarga la pagina entera al enviar el formulario, que
  // es lo que hacian los formularios antes de que existiera `fetch`.
  event.preventDefault();
  await signIn("/login");
});

// "Create account" es `type="button"` en el HTML a proposito: dentro de un
// formulario, un boton sin tipo envia el formulario, y crear cuenta acabaria
// disparando el inicio de sesion.
registerButton.addEventListener("click", async () => {
  await signIn("/register");
});

logoutButton.addEventListener("click", async () => {
  try {
    await fetch("/logout", { method: "POST" });
  } catch {
    // Si la peticion no llego, la cookie sigue en el navegador. Se avisa en vez
    // de pintar la pantalla de "has salido": diria una mentira.
    showError("No se pudo cerrar la sesion. Revisa que el servidor este encendido.");
    return;
  }
  showAs(null);
});

practiceForm.addEventListener("submit", async (event: SubmitEvent) => {
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
    // 🔑 **En el cuerpo ya no va el nombre**, y ese hueco es el paso 5. Antes
    // aqui viajaba `{ user: ... }` y el servidor se lo creia. Ahora quien
    // practica sale de la cookie firmada, que el navegador adjunta solo.
    //
    // Ruta relativa, sin `http://localhost:8000` delante. Funciona igual en tu
    // maquina y en la nube porque la pantalla y el servidor son el MISMO
    // origen: el mismo FastAPI entrega este archivo y atiende /practice. Por
    // eso no hizo falta configurar CORS — ver [D-011].
    const response = await fetch("/practice", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ sentence: sentence }),
    });

    if (response.status === 401) {
      // La sesion caduco mientras la pagina seguia abierta. Se devuelve la
      // pantalla al estado real en vez de dejar puesto un formulario que ya no
      // funciona.
      showAs(null);
      showError("Tu sesion caduco. Vuelve a entrar.");
      return;
    }

    if (!response.ok) {
      showError(await readErrorMessage(response));
      return;
    }

    const reply = (await response.json()) as PracticeResponse;
    errorBox.textContent = "";
    verdictBox.textContent = reply.verdict;
    wordsBox.textContent = String(reply.words);
    scoreBox.textContent = String(reply.score);
    practiceBox.textContent = String(reply.practice);
  } catch {
    // Aqui se cae cuando la peticion ni siquiera llego: servidor apagado, cable
    // desconectado. No hay respuesta que leer, asi que no hay detalle que dar.
    showError("No se pudo hablar con el servidor. Revisa que este encendido.");
  } finally {
    // `finally` corre pase lo que pase. Sin el, un fallo dejaria el boton
    // apagado para siempre y habria que recargar la pagina.
    sendButton.disabled = false;
  }
});

// Al abrir la pagina no se sabe si hay sesion: se pregunta. Las dos secciones
// nacen con `hidden` en el HTML para que no parpadee la equivocada mientras
// llega la respuesta.
void whoAmI().then(showAs);
