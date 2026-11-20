
"""GraphQL-Client für OctoMesh."""

import datetime as dt
import os

import httpx

from zoneinfo import ZoneInfo

ARCHIVE_ID = "ec0000000000000000000a01"
ZEITZONE = ZoneInfo("Europe/Vienna")


def lade_zeitstempel(
    datum: dt.date,
    messdaten_anker_id: str
) -> list[str]:
    """Lädt Zeitstempel einer Messreihe aus OctoMesh."""

    assets_url = os.environ["OCTO_ASSETS_URL"].rstrip("/")
    token_url = os.environ["OCTO_TOKEN_URL"]
    tenant = os.environ["OCTO_TENANT"]
    client_id = os.environ["OCTO_CLIENT_ID"]
    client_secret = os.environ["OCTO_CLIENT_SECRET"]

    # OAuth2: Zugriffstoken anfordern
    with httpx.Client(timeout=40) as client:
        token_antwort = client.post(
            token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": "octo_api",
                "acr_values": f"tenant:{tenant}",
            },
        )

        token_antwort.raise_for_status()
        access_token = token_antwort.json()["access_token"]

        # Österreichische Tagesgrenzen in UTC umrechnen
        beginn = dt.datetime.combine(
            datum, dt.time.min, ZEITZONE
        ).astimezone(dt.timezone.utc)

        ende = dt.datetime.combine(
            datum + dt.timedelta(days=1),
            dt.time.min,
            ZEITZONE
        ).astimezone(dt.timezone.utc)

        query = """
        query($archive: OctoObjectId!, $anker: [OctoObjectId!],
              $von: DateTime, $bis: DateTime) {
          streamData {
            transientStreamDataQuery {
              simple(
                archiveRtId: $archive
                rtIds: $anker
                columnPaths: ["Amount.Value"]
                arg: {
                  from: $von
                  to: $bis
                  queryMode: DEFAULT
                }
                first: 1
              ) {
                items {
                  rows(first: 150) {
                    totalCount
                    pageInfo { hasNextPage }
                    items { timestamp }
                  }
                }
              }
            }
          }
        }
        """

        antwort = client.post(
            f"{assets_url}/tenants/{tenant}/GraphQL",
            headers={"Authorization": f"Bearer {access_token}"},
            json={
                "query": query,
                "variables": {
                    "archive": ARCHIVE_ID,
                    "anker": [messdaten_anker_id],
                    "von": beginn.isoformat(),
                    "bis": ende.isoformat(),
                },
            },
        )

        antwort.raise_for_status()
        daten = antwort.json()

    if daten.get("errors"):
        raise RuntimeError(
            "GraphQL-Abfrage fehlgeschlagen: "
            + daten["errors"][0].get("message", "Unbekannter Fehler")
        )

    ergebnis = daten["data"]["streamData"]["transientStreamDataQuery"]["simple"]
    if not ergebnis or not ergebnis["items"]:
        raise RuntimeError("OctoMesh hat kein Abfrageergebnis geliefert.")

    zeilen = ergebnis["items"][0]["rows"]

    if zeilen["pageInfo"]["hasNextPage"]:
        raise RuntimeError("Nicht alle Messwerte wurden abgerufen.")

    zeitstempel = [
        eintrag["timestamp"]
        for eintrag in zeilen["items"]
    ]

    if zeilen["totalCount"] != len(zeitstempel):
        raise RuntimeError("Anzahl der Messwerte stimmt nicht überein.")

    return zeitstempel



def lade_messdaten_anker() -> list[dict]:
    """Lädt alle EnergyMeasurement-Anker mit Zählpunkt-Zuordnung."""

    assets_url = os.environ["OCTO_ASSETS_URL"].rstrip("/")
    token_url = os.environ["OCTO_TOKEN_URL"]
    tenant = os.environ["OCTO_TENANT"]
    client_id = os.environ["OCTO_CLIENT_ID"]
    client_secret = os.environ["OCTO_CLIENT_SECRET"]

    query = """
    query {
      runtime {
        basicEnergyEnergyMeasurement(first: 100) {
          totalCount
          pageInfo {
            hasNextPage
          }
          items {
            rtId
            obisCode
            parent(
              ckTypeIds: [
                "EnergyCommunity/Consumer"
                "EnergyCommunity/Producer"
              ]
            ) {
              items {
                ... on EnergyCommunityConsumer {
                  rtId
                  meteringPointNumber
                  name
                }
                ... on EnergyCommunityProducer {
                  rtId
                  meteringPointNumber
                  name
                }
              }
            }
          }
        }
      }
    }
    """

    with httpx.Client(timeout=40) as client:
        token_antwort = client.post(
            token_url,
            data={
                "grant_type": "client_credentials",
                "client_id": client_id,
                "client_secret": client_secret,
                "scope": "octo_api",
                "acr_values": f"tenant:{tenant}",
            },
        )
        token_antwort.raise_for_status()
        token = token_antwort.json()["access_token"]

        antwort = client.post(
            f"{assets_url}/tenants/{tenant}/GraphQL",
            headers={"Authorization": f"Bearer {token}"},
            json={"query": query},
        )
        antwort.raise_for_status()
        daten = antwort.json()

    if daten.get("errors"):
        raise RuntimeError(
            "GraphQL-Abfrage fehlgeschlagen: "
            + daten["errors"][0].get("message", "Unbekannter Fehler")
        )

    ergebnis = daten["data"]["runtime"]["basicEnergyEnergyMeasurement"]
    anker = ergebnis["items"]

    if ergebnis["pageInfo"]["hasNextPage"]:
        raise RuntimeError("Nicht alle Messdaten-Anker wurden geladen.")

    if len(anker) != ergebnis["totalCount"]:
        raise RuntimeError("Die Ankerliste ist unvollständig.")

    for eintrag in anker:
        if len(eintrag["parent"]["items"]) != 1:
            raise RuntimeError(
                f"Ungültige Zählpunkt-Zuordnung für {eintrag['rtId']}"
            )

    return anker
