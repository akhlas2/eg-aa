
"""Automatisierte Tests für die technische Authentifizierung."""

import os
import unittest
from unittest.mock import patch

from fastapi import HTTPException

from auth import authentifiziere_service


class TestAuthentifizierung(unittest.TestCase):

    def test_gueltiger_api_key(self):
        with patch.dict(os.environ, {"API_KEY": "test-schluessel"}):
            ergebnis = authentifiziere_service("test-schluessel")

        self.assertEqual(ergebnis, "eg-aa-service")

    def test_falscher_api_key(self):
        with patch.dict(os.environ, {"API_KEY": "test-schluessel"}):
            with self.assertRaises(HTTPException) as kontext:
                authentifiziere_service("falsch")

        self.assertEqual(kontext.exception.status_code, 401)

    def test_fehlender_api_key(self):
        with patch.dict(os.environ, {"API_KEY": "test-schluessel"}):
            with self.assertRaises(HTTPException) as kontext:
                authentifiziere_service(None)

        self.assertEqual(kontext.exception.status_code, 401)

    def test_fehlende_serverkonfiguration(self):
        with patch.dict(os.environ, {"API_KEY": ""}):
            with self.assertRaises(HTTPException) as kontext:
                authentifiziere_service("test-schluessel")

        self.assertEqual(kontext.exception.status_code, 401)


if __name__ == "__main__":
    unittest.main()
