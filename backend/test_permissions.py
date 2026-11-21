
"""Tests für die Rollen und Berechtigungen."""

import unittest

from permissions import (
    Benutzer,
    Rolle,
    darf_gesamtuebersicht_sehen,
    darf_zaehlpunkt_sehen,
)


class TestBerechtigungen(unittest.TestCase):

    def setUp(self):
        self.admin = Benutzer(
            benutzer_id="admin01",
            rolle=Rolle.ADMIN,
            erlaubte_zaehlpunkte=set(),
        )

        self.mitglied = Benutzer(
            benutzer_id="mitglied01",
            rolle=Rolle.MITGLIED,
            erlaubte_zaehlpunkte={"zaehlpunkt-001"},
        )

    def test_admin_gesamtuebersicht(self):
        self.assertTrue(
            darf_gesamtuebersicht_sehen(self.admin)
        )

    def test_mitglied_keine_gesamtuebersicht(self):
        self.assertFalse(
            darf_gesamtuebersicht_sehen(self.mitglied)
        )

    def test_mitglied_eigener_zaehlpunkt(self):
        self.assertTrue(
            darf_zaehlpunkt_sehen(
                self.mitglied,
                "zaehlpunkt-001",
            )
        )

    def test_mitglied_fremder_zaehlpunkt(self):
        self.assertFalse(
            darf_zaehlpunkt_sehen(
                self.mitglied,
                "zaehlpunkt-002",
            )
        )

    def test_admin_jeder_zaehlpunkt(self):
        self.assertTrue(
            darf_zaehlpunkt_sehen(
                self.admin,
                "zaehlpunkt-002",
            )
        )


if __name__ == "__main__":
    unittest.main()
