"""Los cuatro guardianes de la pieza de apagado automático (`[D-045]`, `T-073`).

🚨 **Todo lo que se vigila aquí falla en SILENCIO.** Ese es el criterio para
que algo merezca un test en vez de un comentario, y es el mismo de `[D-042]`:
un comentario protege a quien lo lee, y quien viene a "arreglar" un apagado que
se portó raro no lo lee.

La app funciona igual con la pieza rota. Nadie se entera. El único síntoma
llega semanas después, en el panel de facturación — o no llega, porque lo que
falla es al revés y la máquina se apaga cuando no debe.

Los cuatro modos de fallo, y por qué ninguno grita:

| si alguien… | pasa que… | el síntoma es… |
|---|---|---|
| cambia `-P` por `-h` | la máquina muere por dentro y **sigue cobrando** | ninguno: desde fuera se ve igual de apagada |
| pone `Persistent=true` | al encenderla, se apaga sola en la cara | "no arranca bien", y nadie mira este archivo |
| quita el `UTC` | la hora la manda la zona de la máquina | ninguno, hasta que la zona cambie |
| le pone `[Install]` a la orden | se apaga en **cada** encendido | parece que la máquina está rota |

📌 Es el tercer test de TEAPP que lee `deploy/`, por la misma razón que los dos
primeros (`[D-035]`, `[D-042]`): acoplamiento real entre archivos que no se
conocen, invisible desde Python.
"""

import re
from pathlib import Path

# 🔑 Se importa en vez de copiarse. Este repo ya tiene historial de datos
# duplicados que se corrigen en un sitio y no en el otro (`[L-025]`): si algún
# día cambia cómo se reconoce un comentario, cambia para todos a la vez.
# systemd y Caddy marcan el comentario igual, con `#`.
from test_deploy_limits import líneas_activas

DEPLOY = Path(__file__).resolve().parents[1] / "deploy"
ORDEN = DEPLOY / "teapp-shutdown.service"
TEMPORIZADOR = DEPLOY / "teapp-shutdown.timer"
INSTALADOR = DEPLOY / "install.sh"


# ── Guardián 1: `-P`, nunca `-h` ─────────────────────────────────────────
#
# 🚨 El más importante de los cuatro, y el que más se parece a un detalle.
#
#   -P → poweroff de verdad. AWS lo ve, aplica `Detener`, y **para el reloj**
#        de las horas de instancia.
#   -h → halt. La documentación de AWS: *"only places the CPU into a HLT state
#        while the instance continues to run"*. Muerta por dentro, **viva para
#        la factura**.
#
# 🔑 Las dos dejan la máquina sin contestar. Desde fuera son idénticas. La
# diferencia solo se ve en el `running`/`stopped` de la consola o a fin de mes.


def apaga_de_verdad(archivo: Path = ORDEN) -> bool:
    """Si la orden usa `-P` (apagar) y no `-h` (parar la CPU y seguir cobrando).

    El parámetro existe para poder ver al guardián ROJO sin estropear el archivo
    de verdad — `[L-007]`: un control se mide con el fallo puesto y sin él, o no
    se midió.
    """
    activo = líneas_activas(archivo)
    return " -P " in activo and " -h " not in activo


def test_la_orden_apaga_la_maquina_y_no_solo_la_cpu():
    """🚨 Si esto se pone rojo, la máquina pasa la noche cobrando sin síntomas."""
    assert apaga_de_verdad(), (
        "deploy/teapp-shutdown.service ya no usa `shutdown -P`. "
        "Con `-h` la máquina deja de contestar pero AWS la sigue viendo "
        "ENCENDIDA y cobrando las horas de instancia. El fallo es mudo: desde "
        "fuera se ve exactamente igual que un apagado correcto, y solo se nota "
        "en la consola (`running` vs `stopped`) o en la factura. Ver [D-045]."
    )


def test_el_guardian_1_se_pone_rojo_con_el_fallo_puesto(tmp_path):
    """El control ROJO. Un guardián que nunca se ha visto rojo no vigila (`[L-020]`)."""
    def con(contenido: str) -> bool:
        archivo = tmp_path / "prueba.service"
        archivo.write_text(contenido, encoding="utf-8")
        return apaga_de_verdad(archivo)

    assert not con("ExecStart=/usr/sbin/shutdown -h now\n")  # el fallo mudo
    assert con("ExecStart=/usr/sbin/shutdown -P now\n")  # y el verde

    # Y que no lo engañe la prosa que explica por qué NO se usa `-h`.
    assert con("# Nunca -h : ver [D-045]\nExecStart=/usr/sbin/shutdown -P now\n")


# ── Guardián 2: `Persistent` no puede estar en `true` ────────────────────
#
# `Persistent=true` = "si te perdiste un disparo estando apagada, hazlo al
# arrancar". Aquí la máquina se pierde el disparo TODAS las noches, a propósito.
# Con eso puesto, encenderla a las 07:00 la apagaría inmediatamente.


def recupera_disparos_perdidos(archivo: Path = TEMPORIZADOR) -> bool:
    """Si el temporizador se dispararía al arrancar por haberse saltado el de anoche."""
    return "Persistent=true" in líneas_activas(archivo).replace(" ", "")


def test_el_temporizador_no_recupera_el_disparo_de_anoche():
    """🚨 Si esto se pone rojo, la máquina se apaga sola al encenderla."""
    assert not recupera_disparos_perdidos(), (
        "deploy/teapp-shutdown.timer tiene `Persistent=true`. La máquina se "
        "salta el disparo de las 23:00 TODAS las noches (está apagada a "
        "propósito), así que systemd lo 'recuperaría' en cuanto alguien la "
        "encienda por la mañana: se apagaría sola nada más arrancar. Y el "
        "síntoma no señalaría a este archivo — parecería que no arranca bien."
    )


def test_el_guardian_2_se_pone_rojo_con_el_fallo_puesto(tmp_path):
    """El control ROJO, incluyendo la forma con espacios que systemd también acepta."""
    def con(contenido: str) -> bool:
        archivo = tmp_path / "prueba.timer"
        archivo.write_text(contenido, encoding="utf-8")
        return recupera_disparos_perdidos(archivo)

    assert con("Persistent=true\n")
    assert con("Persistent = true\n")  # systemd la lee igual
    assert not con("Persistent=false\n")
    assert not con("# Persistent=true seria un desastre aqui\nPersistent=false\n")


# ── Guardián 3: la hora lleva su zona escrita ────────────────────────────
#
# Sin `UTC`, systemd lee la hora en la zona horaria de la MÁQUINA — un ajuste
# que vive fuera de este repo y que nadie vuelve a mirar. El día que cambie, el
# apagado se muda de hora sin un solo error.


def la_hora_lleva_zona(archivo: Path = TEMPORIZADOR) -> bool:
    """Si `OnCalendar` dice explícitamente en qué zona horaria está esa hora."""
    for línea in líneas_activas(archivo).splitlines():
        if línea.strip().startswith("OnCalendar"):
            return línea.strip().endswith("UTC")
    return False


def test_la_hora_del_apagado_no_depende_de_la_zona_de_la_maquina():
    """🚨 Si esto se pone rojo, la ventana de [D-045] deja de ser la que dice."""
    assert la_hora_lleva_zona(), (
        "El `OnCalendar` de deploy/teapp-shutdown.timer ya no acaba en `UTC`. "
        "Sin la zona escrita, systemd interpreta la hora en la zona de la "
        "máquina, que es un ajuste de fuera de este repo. La ventana de "
        "[D-045] (12:00–23:00 UTC) pasaría a depender de algo que nadie vigila."
    )


def test_el_guardian_3_se_pone_rojo_con_el_fallo_puesto(tmp_path):
    """El control ROJO."""
    def con(contenido: str) -> bool:
        archivo = tmp_path / "prueba.timer"
        archivo.write_text(contenido, encoding="utf-8")
        return la_hora_lleva_zona(archivo)

    assert not con("OnCalendar=*-*-* 23:00:00\n")  # la hora sin zona
    assert not con("Persistent=false\n")  # y sin `OnCalendar`, no hay hora
    assert con("OnCalendar=*-*-* 23:00:00 UTC\n")


# ── Guardián 4: la orden no se habilita ni se arranca ────────────────────
#
# 🚨 Dos formas distintas de que la máquina se apague cuando no debe, y las dos
# empiezan por confundir la ORDEN con el TEMPORIZADOR:
#
#   1. Una sección `[Install]` en `teapp-shutdown.service` → se apagaría en cada
#      encendido.
#   2. Un `systemctl start` sobre esa orden dentro de `install.sh` → se apagaría
#      A MITAD DE LA INSTALACIÓN, en la máquina de quien la está instalando.


def test_la_orden_de_apagado_no_se_puede_habilitar():
    """`[Install]` aquí = la máquina se apaga en cada arranque."""
    assert "[Install]" not in líneas_activas(ORDEN), (
        "deploy/teapp-shutdown.service tiene una sección [Install]. Esa "
        "sección es la que dice 'arráncame en cada encendido', y esta unidad "
        "apaga la máquina: se apagaría sola nada más encenderla, cada vez. "
        "Al temporizador se le habilita; a la orden se le llama."
    )


# 🔑 **No se busca un texto literal, y esa fue una corrección al escribirlo.**
# La primera versión buscaba `systemctl start teapp-shutdown.service`, que
# `install.sh` no escribiría JAMÁS: el guion usa `${SERVICE_NAME}-shutdown`.
# Era un guardián que no podía ponerse rojo ante el fallo real — o sea, `[L-020]`
# cometido dentro del archivo que lo cita.
#
# Lo que se busca es la FORMA del fallo: arrancar algo que se llama `shutdown` y
# NO es el temporizador, sea cual sea la variable con la que esté escrito.
ARRANQUE_DE_UNIDAD = re.compile(r"systemctl\s+(?:[-\w]+\s+)*(start|restart)\s+(\S+)")


def arranca_la_orden_de_apagado(archivo: Path = INSTALADOR) -> bool:
    """Si el guion arranca la orden que apaga, en vez de solo el temporizador."""
    for _verbo, unidad in ARRANQUE_DE_UNIDAD.findall(líneas_activas(archivo)):
        if "shutdown" in unidad and not unidad.endswith(".timer"):
            return True
    return False


def test_el_instalador_no_arranca_la_orden_de_apagado():
    """Un `start` sobre la orden apagaría la máquina a mitad de la instalación."""
    assert not arranca_la_orden_de_apagado(), (
        "install.sh arranca la unidad de apagado. Esa unidad apaga la máquina: "
        "la instalación moriría a mitad, apagando la máquina de quien la está "
        "instalando. Solo se arranca el `.timer`."
    )


def test_el_guardian_4_se_pone_rojo_con_el_fallo_puesto(tmp_path):
    """El control ROJO, con la variable puesta como la escribe el guion de verdad."""
    def con(contenido: str) -> bool:
        archivo = tmp_path / "prueba.sh"
        archivo.write_text(contenido, encoding="utf-8")
        return arranca_la_orden_de_apagado(archivo)

    # El fallo, en las formas en que de verdad se escribiría.
    assert con('systemctl start "${SERVICE_NAME}-shutdown.service"\n')
    assert con("systemctl restart teapp-shutdown\n")  # sin extensión: vale igual
    assert con('systemctl --quiet start "${SERVICE_NAME}-shutdown"\n')

    # Y el verde: el temporizador SÍ se arranca, y hacerlo es correcto.
    assert not con('systemctl enable --quiet --now "${SERVICE_NAME}-shutdown.timer"\n')
    assert not con('systemctl restart "${SERVICE_NAME}"\n')
