import datetime as dt
import unittest

from data_quality import pruefe_zeitstempel


class TestZeitstempel(unittest.TestCase):

    def setUp(self):
        self.datum = dt.date(2026, 10, 23)
        start = dt.datetime(
            2026, 10, 22, 22, 0,
            tzinfo=dt.timezone.utc
        )

        self.werte = [
            (start + dt.timedelta(minutes=15 * i)).isoformat()
            for i in range(1, 97)
        ]

    def test_vollstaendig(self):
        ergebnis = pruefe_zeitstempel(self.datum, self.werte)
        self.assertTrue(ergebnis["vollstaendig"])
        self.assertEqual(ergebnis["fehlende_intervalle"], 0)

    def test_fehlender_wert(self):
        werte = self.werte[:20] + self.werte[21:]
        ergebnis = pruefe_zeitstempel(self.datum, werte)
        self.assertFalse(ergebnis["vollstaendig"])
        self.assertEqual(ergebnis["fehlende_intervalle"], 1)

    def test_doppelter_wert(self):
        werte = self.werte + [self.werte[10]]
        ergebnis = pruefe_zeitstempel(self.datum, werte)
        self.assertFalse(ergebnis["vollstaendig"])
        self.assertEqual(ergebnis["doppelte_zeitstempel"], 1)

    def test_fehlend_und_doppelt(self):
        werte = self.werte[:20] + self.werte[21:] + [self.werte[10]]
        ergebnis = pruefe_zeitstempel(self.datum, werte)
        self.assertEqual(ergebnis["vorhandene_werte"], 96)
        self.assertFalse(ergebnis["vollstaendig"])
        self.assertEqual(ergebnis["fehlende_intervalle"], 1)
        self.assertEqual(ergebnis["doppelte_zeitstempel"], 1)

    def test_sommerzeitumstellung(self):
        datum = dt.date(2026, 3, 29)
        start = dt.datetime(2026, 3, 28, 23, tzinfo=dt.timezone.utc)
        werte = [
            (start + dt.timedelta(minutes=15 * i)).isoformat()
            for i in range(1, 93)
        ]
        ergebnis = pruefe_zeitstempel(datum, werte)
        self.assertTrue(ergebnis["vollstaendig"])
        self.assertEqual(ergebnis["erwartete_intervalle"], 92)

    def test_winterzeitumstellung(self):
        datum = dt.date(2026, 10, 25)
        start = dt.datetime(2026, 10, 24, 22, tzinfo=dt.timezone.utc)
        werte = [
            (start + dt.timedelta(minutes=15 * i)).isoformat()
            for i in range(1, 101)
        ]
        ergebnis = pruefe_zeitstempel(datum, werte)
        self.assertTrue(ergebnis["vollstaendig"])
        self.assertEqual(ergebnis["erwartete_intervalle"], 100)


if __name__ == "__main__":
    unittest.main()
