
"""Datenqualitätsprüfung für alle Messdaten-Anker der EG."""

import datetime as dt

from octomesh_client import (
    lade_messdaten_anker,
    lade_zeitstempel,
)
from data_quality import pruefe_zeitstempel


def pruefe_eg_datenqualitaet(datum: dt.date) -> dict:
    """Prüft alle Messdaten-Anker für einen bestimmten Tag."""

    anker_liste = lade_messdaten_anker()

    ergebnisse = []
    vollstaendig = 0
    unvollstaendig = 0
    fehler = 0

    for anker in anker_liste:
        parent = anker["parent"]["items"][0]

        eintrag = {
            "zaehlpunkt": parent["name"],
            "zaehlpunktnummer": parent["meteringPointNumber"],
            "anker_id": anker["rtId"],
            "obis_code": anker["obisCode"],
        }

        try:
            zeitstempel = lade_zeitstempel(
                datum,
                anker["rtId"],
            )

            pruefung = pruefe_zeitstempel(
                datum,
                zeitstempel,
            )

            eintrag["datenqualitaet"] = pruefung

            if pruefung["vollstaendig"]:
                vollstaendig += 1
                eintrag["status"] = "vollstaendig"
            else:
                unvollstaendig += 1
                eintrag["status"] = "unvollstaendig"

        except Exception:
            fehler += 1
            eintrag["status"] = "fehler"
            eintrag["datenqualitaet"] = None

        ergebnisse.append(eintrag)

    return {
        "datum": datum.isoformat(),
        "anzahl_zaehlpunkte": len({
            a["parent"]["items"][0]["rtId"]
            for a in anker_liste
        }),
        "anzahl_anker": len(anker_liste),
        "zusammenfassung": {
            "vollstaendig": vollstaendig,
            "unvollstaendig": unvollstaendig,
            "fehler": fehler,
        },
        "ergebnisse": ergebnisse,
    }
