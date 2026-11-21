
"""Rollen und Berechtigungen für AA_Nexus."""

from dataclasses import dataclass
from enum import Enum


class Rolle(str, Enum):
    ADMIN = "admin"
    MITGLIED = "mitglied"


@dataclass
class Benutzer:
    benutzer_id: str
    rolle: Rolle
    erlaubte_zaehlpunkte: set[str]


def darf_gesamtuebersicht_sehen(
    benutzer: Benutzer,
) -> bool:
    """Nur Administratoren dürfen die gesamte EG sehen."""

    return benutzer.rolle == Rolle.ADMIN


def darf_zaehlpunkt_sehen(
    benutzer: Benutzer,
    zaehlpunkt_id: str,
) -> bool:
    """Prüft die Berechtigung für einen Zählpunkt."""

    if benutzer.rolle == Rolle.ADMIN:
        return True

    return (
        benutzer.rolle == Rolle.MITGLIED
        and zaehlpunkt_id in benutzer.erlaubte_zaehlpunkte
    )
