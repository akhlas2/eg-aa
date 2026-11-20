
import datetime as dt
from zoneinfo import ZoneInfo

ZEITZONE = ZoneInfo("Europe/Vienna")


def erwartete_intervalle(datum: dt.date) -> int:
    """Berechnet die erwarteten Viertelstunden eines Wiener Kalendertags."""
    beginn = dt.datetime.combine(datum, dt.time.min, ZEITZONE)
    ende = dt.datetime.combine(datum + dt.timedelta(days=1), dt.time.min, ZEITZONE)

    dauer = ende.astimezone(dt.timezone.utc) - beginn.astimezone(dt.timezone.utc)
    return int(dauer.total_seconds() / 900)


def pruefe_vollstaendigkeit(datum: dt.date, vorhandene_werte: int) -> dict:
    """Prüft die Anzahl vorhandener 15-Minuten-Messwerte eines Zählpunkts."""
    erwartet = erwartete_intervalle(datum)

    if vorhandene_werte < 0:
        raise ValueError("Die Anzahl vorhandener Werte darf nicht negativ sein.")

    return {
        "datum": datum.isoformat(),
        "erwartete_intervalle": erwartet,
        "vorhandene_werte": vorhandene_werte,
        "fehlende_werte": max(0, erwartet - vorhandene_werte),
        "vollstaendig": vorhandene_werte == erwartet,
        "abdeckung_prozent": round(min(vorhandene_werte / erwartet * 100, 100), 2),
        "status": (
            "vollstaendig" if vorhandene_werte == erwartet
            else "unvollstaendig" if vorhandene_werte < erwartet
            else "zu_viele_werte"
        ),
    }



def pruefe_zeitstempel(
    datum: dt.date,
    zeitstempel: list[str]
) -> dict:
    """Prüft 15-Minuten-Intervalle anhand ihrer UTC-Endzeitstempel."""

    beginn = dt.datetime.combine(
        datum, dt.time.min, ZEITZONE
    ).astimezone(dt.timezone.utc)

    ende = dt.datetime.combine(
        datum + dt.timedelta(days=1),
        dt.time.min,
        ZEITZONE
    ).astimezone(dt.timezone.utc)

    schritt = dt.timedelta(minutes=15)

    # Erwartete Endzeitpunkte der Viertelstunden
    erwartet = set()
    zeit = beginn + schritt

    while zeit <= ende:
        erwartet.add(zeit)
        zeit += schritt

    # Tatsächlich gelieferte Zeitstempel
    vorhanden = []

    for wert in zeitstempel:
        zeit = dt.datetime.fromisoformat(
            wert.replace("Z", "+00:00")
        ).astimezone(dt.timezone.utc)

        vorhanden.append(zeit)

    eindeutige = set(vorhanden)

    fehlend = sorted(erwartet - eindeutige)
    ausserhalb = sorted(eindeutige - erwartet)

    doppelte = len(vorhanden) - len(eindeutige)

    return {
        "datum": datum.isoformat(),
        "erwartete_intervalle": len(erwartet),
        "vorhandene_werte": len(vorhanden),
        "eindeutige_zeitstempel": len(eindeutige),
        "fehlende_intervalle": len(fehlend),
        "doppelte_zeitstempel": doppelte,
        "ungueltige_intervalle": len(ausserhalb),
        "vollstaendig": (
            not fehlend
            and not ausserhalb
            and doppelte == 0
        ),
        "fehlende_zeitstempel": [
            zeit.isoformat() for zeit in fehlend
        ],
    }
