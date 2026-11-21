
"""Authentifizierung technischer API-Clients für AA_Nexus."""

import os
import secrets

from fastapi import Header, HTTPException


def authentifiziere_service(
    x_api_key: str | None = Header(default=None),
) -> str:
    """Prüft den technischen API-Key.

    Ein gültiger Schlüssel identifiziert den API-Client,
    aber keinen individuellen Benutzer.
    """

    erwarteter_key = os.environ.get("API_KEY", "")

    if (
        not erwarteter_key
        or not x_api_key
        or not secrets.compare_digest(
            x_api_key,
            erwarteter_key,
        )
    ):
        raise HTTPException(
            status_code=401,
            detail="X-API-Key fehlt oder ist falsch",
        )

    return "eg-aa-service"
