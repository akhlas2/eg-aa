
"""Client für den vorhandenen Kubernetes-Tagessummen-Dienst."""

import datetime as dt
import os

import httpx


def lade_tagessummen(datum: dt.date) -> dict:
    """Lädt die echten Tagesregister über unsere bestehende API."""

    basis_url = os.getenv(
        "TAGESSUMMEN_URL",
        "http://127.0.0.1:8082"
    )

    api_key = os.getenv("API_KEY")

    if not api_key:
        raise RuntimeError("API_KEY ist nicht konfiguriert.")

    antwort = httpx.get(
        f"{basis_url.rstrip('/')}/tagessummen",
        params={
            "von": datum.isoformat(),
            "bis": datum.isoformat(),
        },
        headers={"X-API-Key": api_key},
        timeout=40,
    )

    antwort.raise_for_status()
    return antwort.json()
