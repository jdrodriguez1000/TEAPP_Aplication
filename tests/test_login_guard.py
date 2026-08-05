"""Tests del freno de intentos contra `/login`.

🔑 **El reloj entra por parámetro, igual que en la cuota.** Un castigo de quince
minutos no se comprueba esperando quince minutos: se comprueba viajando al
futuro con un número.

El `dict` de intentos lo vacía `conftest.py` antes de cada test, con `autouse`.
Sin eso, los fallos de un test contarían contra el siguiente — y el freno mordería
donde nadie lo pidió.
"""

import threading

import pytest

from app import login_guard
from app.login_guard import TooManyAttemptsError

ORIGIN = "10.0.0.1"

# Un instante cualquiera. Lo que importa no es cuál, sino las distancias entre
# los que se usan a partir de él.
NOW = 1_000_000.0


# ── Que muerde ────────────────────────────────────────────────────────────


def test_the_first_failures_are_let_through():
    for _ in range(4):
        login_guard.record_failure(ORIGIN, now=NOW)

    # Cuatro fallos con tope de cinco: todavia no se cierra.
    login_guard.check(ORIGIN, now=NOW)


def test_it_bites_when_the_limit_is_reached():
    for _ in range(5):
        login_guard.record_failure(ORIGIN, now=NOW)

    with pytest.raises(TooManyAttemptsError):
        login_guard.check(ORIGIN, now=NOW)


def test_a_lowered_limit_bites_sooner():
    # 🔑 El tope entra por parametro justo para esto: ver el freno morder sin
    # escribir seis peticiones.
    login_guard.record_failure(ORIGIN, now=NOW)
    login_guard.record_failure(ORIGIN, now=NOW)

    with pytest.raises(TooManyAttemptsError):
        login_guard.check(ORIGIN, now=NOW, limit=2)


def test_the_refusal_says_how_long_is_left():
    for _ in range(5):
        login_guard.record_failure(ORIGIN, now=NOW)

    with pytest.raises(TooManyAttemptsError) as caught:
        login_guard.check(ORIGIN, now=NOW)

    error = caught.value

    assert error.origin == ORIGIN
    assert error.attempts == 5
    assert error.limit == 5
    # Los cinco fallos son de este mismo instante, asi que falta la ventana
    # entera. El +1 es el redondeo hacia arriba de `check`.
    assert error.retry_after == login_guard.LOCKOUT_WINDOW_SECONDS + 1


def test_each_origin_is_counted_apart():
    # 🚨 Si los origenes compartieran cubo, quien atacara desde una direccion
    # dejaria fuera a todo el mundo. El freno se volveria el ataque.
    for _ in range(5):
        login_guard.record_failure(ORIGIN, now=NOW)

    login_guard.check("10.0.0.2", now=NOW)


# ── Que suelta ────────────────────────────────────────────────────────────


def test_the_lockout_ends_when_the_window_passes():
    for _ in range(5):
        login_guard.record_failure(ORIGIN, now=NOW)

    later = NOW + login_guard.LOCKOUT_WINDOW_SECONDS + 1

    login_guard.check(ORIGIN, now=later)


def test_a_success_wipes_the_count():
    for _ in range(4):
        login_guard.record_failure(ORIGIN, now=NOW)

    login_guard.clear(ORIGIN)

    # Y no queda ni el rastro: el siguiente fallo empieza a contar desde uno.
    assert login_guard.record_failure(ORIGIN, now=NOW) == 1


def test_clearing_an_origin_that_never_failed_is_not_an_error():
    # Pasa en cada acierto a la primera, que es el caso normal.
    login_guard.clear("10.0.0.9")


# ── El barrido ────────────────────────────────────────────────────────────
#
# 🚨 **Esta es la parte que evita que el freno se coma la memoria.** Sin barrido,
# quien ataque desde mil direcciones deja mil entradas que no se van nunca.


def test_the_sweep_removes_origins_whose_failures_expired():
    login_guard.record_failure("10.0.0.1", now=NOW)
    login_guard.record_failure("10.0.0.2", now=NOW)

    later = NOW + login_guard.LOCKOUT_WINDOW_SECONDS + 1

    assert login_guard.sweep(now=later) == 2
    assert login_guard.tracked_origins() == 0


def test_the_sweep_keeps_origins_that_still_count():
    # ⚠️ El segundo fallo llega **dentro** de la ventana del primero, a
    # proposito. Si llegara justo al final, el barrido automatico de
    # `record_failure` ya se habria llevado al primero y aqui no quedaria nada
    # que barrer: el test pasaria a medir otra cosa sin avisar.
    login_guard.record_failure("10.0.0.1", now=NOW)
    login_guard.record_failure(
        "10.0.0.2", now=NOW + login_guard.LOCKOUT_WINDOW_SECONDS - 10
    )

    later = NOW + login_guard.LOCKOUT_WINDOW_SECONDS + 1

    # El primero caduco; el segundo todavia no.
    assert login_guard.sweep(now=later) == 1
    assert login_guard.tracked_origins() == 1


def test_the_sweep_runs_by_itself_when_new_failures_arrive():
    # 🔑 El barrido va dentro de `record_failure` para que no dependa de que
    # alguien se acuerde de llamarlo. Este test es el que lo demuestra: aqui
    # nadie llama a `sweep`, y aun asi las mil entradas viejas desaparecen.
    for number in range(1000):
        login_guard.record_failure(f"10.0.{number // 256}.{number % 256}", now=NOW)

    assert login_guard.tracked_origins() == 1000

    later = NOW + login_guard.LOCKOUT_WINDOW_SECONDS + 1
    login_guard.record_failure("10.9.9.9", now=later)

    # Queda el recien llegado y nadie mas.
    assert login_guard.tracked_origins() == 1


def test_old_failures_stop_counting_without_wiping_the_new_ones():
    # Cuatro fallos viejos y uno nuevo: el tope no se alcanza, porque los viejos
    # ya no cuentan. Sin la ventana deslizante, este origen quedaria cerrado por
    # fallos de hace horas.
    for _ in range(4):
        login_guard.record_failure(ORIGIN, now=NOW)

    later = NOW + login_guard.LOCKOUT_WINDOW_SECONDS + 1
    login_guard.record_failure(ORIGIN, now=later)

    login_guard.check(ORIGIN, now=later)


# ── El candado ────────────────────────────────────────────────────────────


def test_simultaneous_failures_are_all_counted():
    # 🚨 Mismo peligro que en la cuota: el hueco entre leer y escribir. Sin
    # candado, dos fallos a la vez se pisan y uno se pierde — y perder fallos es
    # aflojar el freno.
    barrier = threading.Barrier(20)

    def fail() -> None:
        barrier.wait()
        login_guard.record_failure(ORIGIN, now=NOW)

    threads = [threading.Thread(target=fail) for _ in range(20)]

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    with pytest.raises(TooManyAttemptsError) as caught:
        login_guard.check(ORIGIN, now=NOW)

    assert caught.value.attempts == 20
