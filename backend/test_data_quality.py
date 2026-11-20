import datetime as dt
import unittest

from data_quality import pruefe_vollstaendigkeit


class TestDatenqualitaet(unittest.TestCase):

    def test_normaler_tag(self):
        ergebnis = pruefe_vollstaendigkeit(dt.date(2026, 10, 23), 96)
        self.assertEqual(ergebnis["erwartete_intervalle"], 96)
        self.assertTrue(ergebnis["vollstaendig"])

    def test_sommerzeitumstellung(self):
        ergebnis = pruefe_vollstaendigkeit(dt.date(2026, 3, 29), 92)
        self.assertEqual(ergebnis["erwartete_intervalle"], 92)
        self.assertTrue(ergebnis["vollstaendig"])

    def test_winterzeitumstellung(self):
        ergebnis = pruefe_vollstaendigkeit(dt.date(2026, 10, 25), 100)
        self.assertEqual(ergebnis["erwartete_intervalle"], 100)
        self.assertTrue(ergebnis["vollstaendig"])

    def test_fehlende_werte(self):
        ergebnis = pruefe_vollstaendigkeit(dt.date(2026, 10, 23), 80)
        self.assertEqual(ergebnis["fehlende_werte"], 16)
        self.assertFalse(ergebnis["vollstaendig"])

    def test_zu_viele_werte(self):
        ergebnis = pruefe_vollstaendigkeit(dt.date(2026, 10, 23), 98)
        self.assertEqual(ergebnis["status"], "zu_viele_werte")


if __name__ == "__main__":
    unittest.main()
