"""Tests del freno que decide dónde viven los datos de las personas.

🚨 **Esto es [D-037], y lo que arregla es [L-023].** Antes la raíz de `data/` se
calculaba en tres módulos, cada uno con la carpeta REAL como valor por defecto:
un script que importara la app y se olvidara de desviar escribía en los datos de
personas de verdad, sin decir nada. Es lo que hizo la báscula de `T-054`, que se
acordó de desviar las cuentas y se olvidó del marcador y de la cuota.

Ahora la raíz sale de `TEAPP_DATA_DIR`, **sin valor por defecto**. Estos tests
vigilan las cuatro formas de equivocarse, y que las cuatro **se nieguen** en vez
de escribir en cualquier sitio.

🔑 Cada uno de estos tests borra o cambia la variable que `conftest.py` deja
puesta. Es a propósito: aquí se mide justamente el caso que la suite entera evita.
"""

import logging

import pytest

from app import config
from app.config import DATA_DIR_NAME, MissingDataDirError

# ── Las cuatro formas de equivocarse ──────────────────────────────────────


def test_without_the_variable_it_refuses(monkeypatch):
    """🚨 El caso que da nombre a la decisión: si falta, no se arranca.

    Denegar por defecto. Lo que no esté declarado por escrito, se rechaza — el
    mismo criterio que `require_secret` con la llave de firma.
    """
    monkeypatch.delenv(DATA_DIR_NAME, raising=False)

    with pytest.raises(MissingDataDirError):
        config.require_data_dir()


def test_an_empty_variable_counts_as_missing(monkeypatch):
    """Puesta pero vacía es lo mismo que no puesta.

    ⚠️ Un `TEAPP_DATA_DIR=` en el `.env` parece configurado —la línea está ahí,
    alguien la escribió— y no lo está. Si esto pasara, escribiría en la raíz del
    sistema de archivos.
    """
    monkeypatch.setenv(DATA_DIR_NAME, "   ")

    with pytest.raises(MissingDataDirError):
        config.require_data_dir()


def test_a_relative_path_is_refused_not_resolved(monkeypatch, tmp_path):
    """🚨 El test que sostiene la decisión entera.

    Una ruta relativa se resuelve contra la carpeta desde la que se lanzó el
    proceso — que es **exactamente la variable que este cambio existe para
    eliminar**. El mismo script corrido desde otra carpeta escribiría en otro
    sitio. Se rechaza; no se arregla en silencio.

    🚨 **La carpeta relativa se CREA a propósito, y ahí está el filo del test.**
    Sin crearla, quitar el freno de `is_absolute` dejaría este test igual de verde:
    la ruta se resolvería contra el directorio de trabajo, no encontraría nada, y
    saltaría el otro freno —el de la carpeta que no existe— por la razón
    equivocada. Medido: con el freno saboteado y sin esta carpeta, seguía pasando.
    Creándola, la única forma de que esto se ponga rojo es que la ruta relativa
    **se acepte**, que es justo lo que no puede pasar. Es [L-019].
    """
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    monkeypatch.setenv(DATA_DIR_NAME, "data")

    with pytest.raises(MissingDataDirError):
        config.require_data_dir()


def test_the_refusal_of_a_relative_path_says_what_to_do(monkeypatch, tmp_path):
    """Y no basta con negarse: el mensaje tiene que enseñar el arreglo.

    🔑 Quien lea esto está mirando una terminal en un servidor recién montado.
    "Ruta invalida" lo deja adivinando; decir ABSOLUTA lo resuelve en un minuto.
    """
    monkeypatch.chdir(tmp_path)
    (tmp_path / "data").mkdir()
    monkeypatch.setenv(DATA_DIR_NAME, "data")

    with pytest.raises(MissingDataDirError) as caught:
        config.require_data_dir()

    message = str(caught.value)
    assert "ABSOLUTA" in message
    assert DATA_DIR_NAME in message


def test_a_folder_that_does_not_exist_is_refused(monkeypatch, tmp_path):
    """🚨 **La carpeta NO se crea sola**, y esa es la mitad seria del freno.

    Creándola, una ruta mal tecleada se convertiría en un `data/` vacío: la app
    arranca, nadie ve un error, y todo el mundo parece haber perdido su marcador.
    Un fallo mudo, de la familia de [L-032] (antes [A-008]). Crear la carpeta es un acto de
    instalación y vive en `deploy/install.sh`.
    """
    ausente = tmp_path / "no-existe"
    monkeypatch.setenv(DATA_DIR_NAME, str(ausente))

    with pytest.raises(MissingDataDirError):
        config.require_data_dir()

    # Y no la ha creado de paso.
    assert not ausente.exists()


def test_a_file_named_like_the_folder_is_refused(monkeypatch, tmp_path):
    """`is_dir()` y no `exists()`, que no es lo mismo.

    Un ARCHIVO llamado `data` pasaría un `exists()` tan campante, y el fallo
    aparecería mucho más lejos —al escribir dentro— y sin explicación.
    """
    impostor = tmp_path / "data"
    impostor.write_text("no soy una carpeta", encoding="utf-8")
    monkeypatch.setenv(DATA_DIR_NAME, str(impostor))

    with pytest.raises(MissingDataDirError):
        config.require_data_dir()


# ── Y el camino bueno ─────────────────────────────────────────────────────


def test_with_an_absolute_existing_folder_it_answers_that_folder(monkeypatch, tmp_path):
    monkeypatch.setenv(DATA_DIR_NAME, str(tmp_path))

    assert config.require_data_dir() == tmp_path.resolve()


def test_the_path_comes_back_resolved(monkeypatch, tmp_path):
    """Una sola forma de la misma carpeta.

    🔑 Sin `resolve()`, el renglón del log diría `/opt/teapp/data/../data` y
    quien lo lea tendría que hacer el cálculo de cabeza para saber dónde escribe
    de verdad. Lo que importa es el destino, no cómo se escribió.
    """
    torcida = tmp_path / "vueltas" / ".." / "vueltas"
    (tmp_path / "vueltas").mkdir()
    monkeypatch.setenv(DATA_DIR_NAME, str(torcida))

    assert config.require_data_dir() == (tmp_path / "vueltas").resolve()
    assert ".." not in str(config.require_data_dir())


def test_the_three_places_hang_from_the_same_root(monkeypatch, tmp_path):
    """🔑 El corazón de [D-037]: **una variable, tres sitios.**

    Antes eran tres constantes independientes y había que acordarse de las tres.
    Este test es el que se pondría rojo si alguien volviera a soltar una.
    """
    monkeypatch.setenv(DATA_DIR_NAME, str(tmp_path))
    raiz = tmp_path.resolve()

    assert config.users_dir() == raiz / "users"
    assert config.quota_dir() == raiz / "quota"
    assert config.accounts_file() == raiz / "accounts.json"


def test_the_root_is_asked_again_on_every_call(monkeypatch, tmp_path):
    """🚨 Que la ruta NO se congele al importar — el defecto de [D-036] otra vez.

    Si `require_data_dir` guardara el resultado, o si los tres sitios fueran
    constantes de módulo, cambiar la variable después no movería nada: la app
    seguiría escribiendo donde apuntaba al arrancar. Este test cambia la variable
    en mitad de la corrida y exige que la respuesta cambie con ella.
    """
    primera = tmp_path / "una"
    segunda = tmp_path / "otra"
    primera.mkdir()
    segunda.mkdir()

    monkeypatch.setenv(DATA_DIR_NAME, str(primera))
    assert config.users_dir() == primera.resolve() / "users"

    monkeypatch.setenv(DATA_DIR_NAME, str(segunda))
    assert config.users_dir() == segunda.resolve() / "users"


# ── El renglón del log ────────────────────────────────────────────────────


def test_the_startup_line_says_where_the_data_lives(monkeypatch, tmp_path, caplog):
    """Una línea, y contesta "¿dónde escribe esta app?" mirando en vez de deducir.

    📌 Es además el testigo de `T-066`: al arrancar en la nube, este renglón dice
    si cogió el disco que persiste o cualquier otro sitio.
    """
    monkeypatch.setenv(DATA_DIR_NAME, str(tmp_path))

    with caplog.at_level(logging.INFO, logger=config.__name__):
        config.log_data_dir()

    assert str(tmp_path.resolve()) in caplog.text


def test_the_startup_line_refuses_instead_of_lying(monkeypatch):
    """🚨 Y si no hay variable, este renglón NO escribe "ninguna": se niega.

    Es lo que convierte el log en el freno de arranque. `app/api.py` llama a
    `log_data_dir()` al importarse, así que un servidor mal configurado **no
    llega a atender la primera petición** — falla al encender, con alguien
    delante mirando la terminal, y no dentro de una petición con alguien
    esperando al otro lado.
    """
    monkeypatch.delenv(DATA_DIR_NAME, raising=False)

    with pytest.raises(MissingDataDirError):
        config.log_data_dir()


# ── De dónde salió el valor, dicho en voz alta ────────────────────────────
#
# 🚨 **La precedencia NO se toca: el entorno le gana al `.env`, a propósito.**
# `conftest.py` desvía `TEAPP_DATA_DIR` a una carpeta temporal al importarse; si
# el `.env` ganara, `from app.api import app` traería de vuelta la ruta real y
# los 342 tests escribirían en `data/` de verdad.
#
# 🔑 Lo que se arregla no es la regla, es que era **muda**. Quien anula desde el
# entorno lo hacía sin dejar rastro. Estos tests vigilan que se note.


def test_the_env_file_loses_against_the_environment(monkeypatch, tmp_path):
    """El `.env` propone y el entorno dispone. Esta es la regla que sostiene la suite."""
    archivo = tmp_path / ".env"
    archivo.write_text(f"{DATA_DIR_NAME}=el_del_archivo\n", encoding="utf-8")
    monkeypatch.setenv(DATA_DIR_NAME, "el_de_la_corrida")

    config.load_env_file(archivo)

    import os

    assert os.environ[DATA_DIR_NAME] == "el_de_la_corrida"


def test_it_says_environment_when_the_environment_wins(monkeypatch, tmp_path):
    """🚨 El caso que da nombre a esto: la anulación silenciosa deja de serlo."""
    archivo = tmp_path / ".env"
    archivo.write_text(f"{DATA_DIR_NAME}=el_del_archivo\n", encoding="utf-8")
    monkeypatch.setenv(DATA_DIR_NAME, "el_de_la_corrida")

    config.load_env_file(archivo)

    assert config.value_origin(DATA_DIR_NAME) == "entorno"


def test_it_says_env_file_when_nobody_overrides(monkeypatch, tmp_path):
    """Y el contrario: sin anulación, el crédito es del archivo.

    ⚠️ Sin este test el anterior se pondría verde aunque la función devolviera
    siempre `"entorno"` — un control que no distingue no es un control ([L-013]).
    """
    archivo = tmp_path / ".env"
    archivo.write_text(f"{DATA_DIR_NAME}=el_del_archivo\n", encoding="utf-8")
    monkeypatch.delenv(DATA_DIR_NAME, raising=False)

    config.load_env_file(archivo)

    assert config.value_origin(DATA_DIR_NAME) == ".env"


def test_the_origin_does_not_go_stale_when_the_value_changes_later(
    monkeypatch, tmp_path
):
    """🔑 Por qué se compara el valor y no se recuerda quién ganó.

    Un apunte de "lo puse yo" dentro de `load_env_file` envejecería mal: aquí el
    archivo gana primero y **después** alguien cambia la variable, que es
    exactamente lo que hace `monkeypatch` en cada test de esta suite. Con apunte,
    esta línea seguiría diciendo `.env` sobre un valor que ya no viene de ahí.
    """
    archivo = tmp_path / ".env"
    archivo.write_text(f"{DATA_DIR_NAME}=el_del_archivo\n", encoding="utf-8")
    monkeypatch.delenv(DATA_DIR_NAME, raising=False)
    config.load_env_file(archivo)
    assert config.value_origin(DATA_DIR_NAME) == ".env"

    monkeypatch.setenv(DATA_DIR_NAME, "cambiado_despues")

    assert config.value_origin(DATA_DIR_NAME) == "entorno"


def test_without_any_value_it_says_so_instead_of_guessing(monkeypatch):
    """Sin variable no se inventa un origen. Denegar por defecto, también aquí."""
    monkeypatch.delenv(DATA_DIR_NAME, raising=False)

    assert config.value_origin(DATA_DIR_NAME) == "sin valor"


def test_the_startup_line_writes_the_origin(monkeypatch, tmp_path, caplog):
    """Y que el renglón del arranque lo lleve, que es donde se lee de verdad."""
    monkeypatch.setenv(DATA_DIR_NAME, str(tmp_path))

    with caplog.at_level(logging.INFO, logger=config.__name__):
        config.log_data_dir()

    assert "origen: entorno" in caplog.text
