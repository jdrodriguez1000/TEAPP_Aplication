"""Tests del freno de la cuota.

🔑 **El reloj entra por parámetro, y sin eso este archivo no existiría.** Un tope
por día no se puede comprobar esperando a mañana. Aquí se viaja al futuro
escribiendo una fecha.

La carpeta de la cuota la desvía `conftest.py` a una temporal, con `autouse`, así
que ningún test de aquí toca `data/quota/`.
"""

import json
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pytest

from app import config, quota
from app.quota import QuotaExceededError, QuotaFileError
from app.tools import InvalidUserError

USER = "juan"

# La zona del proyecto y la del servidor de la nube, para poder enfrentarlas.
BOGOTA = timezone(timedelta(hours=-5))
UTC = timezone.utc


def at(text: str) -> datetime:
    """Un instante concreto, con zona. `at("2026-08-04 10:00-05:00")`."""
    return datetime.fromisoformat(text)


# ── Qué día es hoy ────────────────────────────────────────────────────────


def test_the_day_comes_from_the_project_timezone():
    assert quota.today(at("2026-08-04 10:00-05:00")) == "2026-08-04"


def test_the_day_is_translated_when_it_arrives_in_another_timezone():
    # El mismo instante escrito en UTC. La cuota tiene que verlo como el día que
    # es AQUÍ, no como el día que es en el reloj de quien lo mandó.
    assert quota.today(at("2026-08-04 15:00+00:00")) == "2026-08-04"


def test_the_utc_midnight_window_does_not_change_the_day():
    # 🚨 **Este es el test que justifica [D-024], y el único que fallaría si
    # alguien "simplificara" la zona a UTC.**
    #
    # `2026-08-05 02:30 UTC` es el 5 de agosto en el servidor de la nube y el 4
    # aquí. Sin la traducción, la cuota se reiniciaría a las 7 de la tarde — y el
    # fallo solo aparecería en producción, nunca en esta máquina.
    utc_after_midnight = datetime(2026, 8, 5, 2, 30, tzinfo=UTC)

    assert utc_after_midnight.astimezone(UTC).date().isoformat() == "2026-08-05"
    assert quota.today(utc_after_midnight) == "2026-08-04"


def test_a_clock_without_timezone_is_rejected():
    # 🔑 Un `datetime` sin zona no sabe qué día es en ningún sitio concreto.
    # Aceptarlo sería dejar que Python lo interprete como hora local, que en la
    # nube es UTC — el mismo fallo de arriba, entrando por otra puerta.
    with pytest.raises(ValueError):
        quota.today(datetime(2026, 8, 4, 10, 0))


def test_without_a_clock_it_uses_the_real_one():
    # No se comprueba QUÉ día devuelve —eso cambiaría cada noche— sino que
    # devuelve un día bien formado sin que nadie le pase la hora.
    assert quota.today() == datetime.now(BOGOTA).date().isoformat()


# ── El gasto se cuenta ────────────────────────────────────────────────────


def test_nobody_has_spent_anything_on_their_first_day():
    assert quota.read_usage(USER, at("2026-08-04 10:00-05:00")) == 0


def test_spending_adds_one():
    assert quota.spend(USER, at("2026-08-04 10:00-05:00")) == 1


def test_spending_twice_adds_two():
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment)

    assert quota.spend(USER, moment) == 2


def test_what_was_spent_survives_being_read_again():
    # El contador vive en disco, no en memoria: si viviera en memoria, esto
    # pasaría igual y el freno se borraría en cada arranque del servidor.
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment)
    quota.spend(USER, moment)

    assert quota.read_usage(USER, moment) == 2


def test_two_people_do_not_share_a_counter():
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment)
    quota.spend(USER, moment)

    assert quota.read_usage("maria", moment) == 0


def test_the_same_person_written_differently_is_the_same_counter():
    # Mismo criterio que [D-014] con el marcador: `  JUAN ` y `juan` son una
    # persona. Si no, cambiar las mayúsculas regalaría una cuota nueva.
    moment = at("2026-08-04 10:00-05:00")
    quota.spend("  JUAN ", moment)

    assert quota.read_usage("juan", moment) == 1


def test_a_name_that_cannot_be_a_file_is_rejected():
    with pytest.raises(InvalidUserError):
        quota.spend("../../CLAUDE", at("2026-08-04 10:00-05:00"))


# ── El día siguiente ──────────────────────────────────────────────────────


def test_the_counter_resets_the_next_day():
    # 🔑 Sin barrer nada: el archivo guarda el día, y un día que no es hoy vale 0.
    quota.spend(USER, at("2026-08-04 23:00-05:00"))
    quota.spend(USER, at("2026-08-04 23:30-05:00"))

    assert quota.read_usage(USER, at("2026-08-05 00:30-05:00")) == 0


def test_spending_after_midnight_starts_from_one():
    quota.spend(USER, at("2026-08-04 23:00-05:00"))

    assert quota.spend(USER, at("2026-08-05 00:30-05:00")) == 1


def test_someone_who_hit_the_limit_can_practice_again_tomorrow():
    yesterday = at("2026-08-04 10:00-05:00")
    quota.spend(USER, yesterday, limit=2)
    quota.spend(USER, yesterday, limit=2)

    assert quota.spend(USER, at("2026-08-05 10:00-05:00"), limit=2) == 1


# ── El freno muerde ───────────────────────────────────────────────────────


def test_the_limit_stops_the_next_one():
    # El tope entra por parámetro: con 20 incrustado, este test necesitaría 21
    # llamadas para demostrar lo mismo.
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment, limit=1)

    with pytest.raises(QuotaExceededError):
        quota.spend(USER, moment, limit=1)


def test_the_refusal_says_why():
    # 🔑 Un freno sin motivo obliga a adivinar. La excepción lleva los datos
    # encima para que la puerta no tenga que reconstruirlos.
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment, limit=1)

    with pytest.raises(QuotaExceededError) as refusal:
        quota.spend(USER, moment, limit=1)

    assert refusal.value.user == USER
    assert refusal.value.used == 1
    assert refusal.value.limit == 1
    assert refusal.value.day == "2026-08-04"


def test_a_refused_attempt_does_not_keep_counting():
    # 🔑 Si el contador siguiera subiendo con el freno puesto, el número dejaría
    # de significar "prácticas hechas" y pasaría a significar "veces que lo
    # intentó" — y quien mirara el archivo leería un dato que no es.
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment, limit=1)

    for _ in range(3):
        with pytest.raises(QuotaExceededError):
            quota.spend(USER, moment, limit=1)

    assert quota.read_usage(USER, moment) == 1


def test_the_default_limit_is_twenty():
    # El número es una predicción sin medir ([A-010]). Este test no dice que 20
    # esté bien: dice que el valor por defecto es el que se acordó, para que
    # cambiarlo sea una decisión y no un descuido.
    assert quota.DAILY_LIMIT == 20


# ── Cuando el archivo está roto ───────────────────────────────────────────


@pytest.fixture
def broken_counter(tmp_path, monkeypatch):
    """Deja el archivo de cuota de USER con basura dentro."""
    # La raiz entera se muda, y la cuota cuelga de ella ([D-037]).
    root = tmp_path / "broken-root"
    directory = root / "quota"
    directory.mkdir(parents=True)
    monkeypatch.setenv(config.DATA_DIR_NAME, str(root))

    path = directory / f"{USER}.json"
    path.write_text("esto no es json", encoding="utf-8")
    return path


def test_a_broken_counter_does_not_let_anyone_through(broken_counter):
    # 🚨 **Denegar por defecto.** Devolver 0 ante un archivo roto sería regalar
    # la cuota entera justo cuando el freno está averiado.
    with pytest.raises(QuotaFileError):
        quota.spend(USER, at("2026-08-04 10:00-05:00"))


def test_a_broken_counter_is_not_overwritten(broken_counter):
    # Mismo criterio que `add_point`: nunca pises un dato que no lograste
    # entender. Mientras siga ahí, alguien puede abrirlo y arreglarlo a mano.
    with pytest.raises(QuotaFileError):
        quota.spend(USER, at("2026-08-04 10:00-05:00"))

    assert broken_counter.read_text(encoding="utf-8") == "esto no es json"


@pytest.mark.parametrize(
    "content",
    [
        '{"used": 3}',  # sin el dia: no se sabe de cuando es
        '{"day": "2026-08-04"}',  # sin el gasto
        '{"day": "2026-08-04", "used": "tres"}',  # el gasto no es un numero
        '{"day": "2026-08-04", "used": true}',  # bool hereda de int en Python
        '{"day": "2026-08-04", "used": -1}',  # un gasto negativo daria cuota extra
        '["2026-08-04", 3]',  # ni siquiera es un diccionario
    ],
)
def test_a_counter_that_cannot_be_understood_is_refused(tmp_path, monkeypatch, content):
    root = tmp_path / "odd-root"
    directory = root / "quota"
    directory.mkdir(parents=True)
    monkeypatch.setenv(config.DATA_DIR_NAME, str(root))
    (directory / f"{USER}.json").write_text(content, encoding="utf-8")

    with pytest.raises(QuotaFileError):
        quota.read_usage(USER, at("2026-08-04 10:00-05:00"))


# ── Lo que se guarda en el archivo ────────────────────────────────────────


def test_the_file_keeps_the_day_and_the_amount():
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment)

    saved = json.loads(quota.quota_file(USER).read_text(encoding="utf-8"))

    assert saved == {"day": "2026-08-04", "used": 1}


# ── Dos peticiones a la vez ───────────────────────────────────────────────
#
# 🔑 Mismo problema que [T-022] con el marcador, y aquí es peor: allí se perdía
# un punto, aquí se cuela una práctica gratis por cada carrera perdida. Un freno
# con un agujero del tamaño de las peticiones simultáneas no frena.

SPENDERS = 50


def spend_many_at_once(moment, spenders=SPENDERS, limit=1000):
    with ThreadPoolExecutor(max_workers=spenders) as pool:
        return list(pool.map(lambda _: quota.spend(USER, moment, limit), range(spenders)))


def test_nothing_gets_through_free_with_many_at_once():
    # Cada hilo gasta una práctica, así que el contador final tiene que valer
    # EXACTAMENTE los hilos que hubo. Sin el candado se queda corto, y lo que
    # falta son prácticas que nadie cobró.
    moment = at("2026-08-04 10:00-05:00")
    spend_many_at_once(moment)

    assert quota.read_usage(USER, moment) == SPENDERS


def test_no_two_at_once_get_the_same_number():
    # Que el total cuadre no basta: si dos llamadas devolvieran el mismo número,
    # las dos se creerían la misma práctica. Los números tienen que ser 1..N.
    moment = at("2026-08-04 10:00-05:00")
    spent = spend_many_at_once(moment)

    assert sorted(spent) == list(range(1, SPENDERS + 1))


def test_the_limit_holds_with_many_at_once():
    # 🚨 El test que de verdad prueba el freno. 50 peticiones simultáneas contra
    # un tope de 10: exactamente 10 pasan y 40 se rechazan. Sin candado pasarían
    # de más, porque varias leerían el mismo número por debajo del tope.
    moment = at("2026-08-04 10:00-05:00")
    allowed = 10

    def try_to_spend(_):
        try:
            quota.spend(USER, moment, limit=allowed)
            return True
        except QuotaExceededError:
            return False

    with ThreadPoolExecutor(max_workers=SPENDERS) as pool:
        results = list(pool.map(try_to_spend, range(SPENDERS)))

    assert sum(results) == allowed
    assert quota.read_usage(USER, moment) == allowed


def test_no_leftovers_are_left_behind():
    # La escritura atómica crea un temporal al lado. Si alguno sobreviviera, la
    # carpeta se llenaría de basura un archivo por práctica.
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment)
    quota.spend(USER, moment)

    leftovers = list(config.quota_dir().glob("*.tmp"))

    assert leftovers == []


# ── La medianoche entre la comprobación y la escritura ────────────────────
#
# 🚨 `spend` preguntaba DOS veces qué día era: una para sí y otra dentro de
# `read_usage`. Entre las dos cabía la medianoche, y cuando cabía se comprobaba
# contra el día nuevo —limpio, así que pasaba— y se escribía bajo el día viejo,
# borrando lo gastado. **Cuota gratis, una vez al día.** Ver [L-013].


@pytest.fixture
def midnight_between_calls(monkeypatch):
    """Hace que el reloj cambie de día entre la primera y la segunda pregunta."""
    days = iter(["2026-08-04", "2026-08-05", "2026-08-05", "2026-08-05"])
    monkeypatch.setattr(quota, "today", lambda now=None: next(days))


def test_midnight_does_not_hand_out_free_quota(midnight_between_calls):
    # El día 4 está agotado. Si `spend` comprobara contra un día y escribiera
    # contra otro, esta llamada pasaría y dejaría el archivo del día 4 en 1.
    quota.quota_file(USER).parent.mkdir(parents=True, exist_ok=True)
    quota.quota_file(USER).write_text(
        json.dumps({"day": "2026-08-04", "used": 20}), encoding="utf-8"
    )

    with pytest.raises(QuotaExceededError):
        quota.spend(USER, limit=20)


def test_the_day_it_checks_is_the_day_it_writes(midnight_between_calls):
    # El otro lado: cuando sí queda cuota, el día que se escribe tiene que ser
    # el mismo contra el que se comprobó, no otro que cambió por el camino.
    quota.spend(USER, limit=20)

    saved = json.loads(quota.quota_file(USER).read_text(encoding="utf-8"))

    assert saved["day"] == "2026-08-04"


# ── Devolver lo que nunca empezó ──────────────────────────────────────────


def test_refund_gives_back_one_practice():
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment)
    quota.spend(USER, moment)

    assert quota.refund(USER, moment) == 1


def test_refund_does_not_invent_quota_when_nothing_was_spent():
    # 🔑 Bajar a -1 sería regalar una práctica. Devolver de más es peor que no
    # devolver: el freno acabaría dejando pasar más de lo que dice.
    moment = at("2026-08-04 10:00-05:00")

    assert quota.refund(USER, moment) == 0
    assert quota.read_usage(USER, moment) == 0


def test_refund_from_yesterday_does_not_touch_today():
    # Si la medianoche cae entre el cobro y la devolución, lo cobrado es de ayer
    # y ya no cuenta contra nadie. Restarlo de hoy regalaría cuota.
    quota.spend(USER, at("2026-08-04 23:59-05:00"))

    assert quota.refund(USER, at("2026-08-05 00:01-05:00")) == 0
    assert quota.read_usage(USER, at("2026-08-05 00:01-05:00")) == 0


def test_a_refunded_practice_can_be_spent_again():
    moment = at("2026-08-04 10:00-05:00")
    quota.spend(USER, moment, limit=1)
    quota.refund(USER, moment)

    assert quota.spend(USER, moment, limit=1) == 1
