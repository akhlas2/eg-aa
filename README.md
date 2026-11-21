# EG-AA – Energiegemeinschaft

Projekt im Lehrveranstaltungslabor **Verteilte Systeme und Cloud-Technologien (WS 2026/27)** an der FH Salzburg. Team **AA**, OctoMesh-Mandant **`eg-aa`**.

**Stand: 21.11.2026** · [Technische Dokumentation](VSYS_Team_AA_Technische_Dokumentation.md) · [Projektübersicht](VSYS_Team_AA_Projektuebersicht.md)

## Projektziel

Messdaten einer Energiegemeinschaft abrufen, prüfen und für Tagesprofile, Prognosen, Handel und spätere Mitgliederabrechnung bereitstellen. Die Umsetzung erfolgt mit OctoMesh (GraphQL), Python/FastAPI und Kubernetes.

## Aktueller Stand

| Bereich | Nachgewiesen | Noch offen |
|---|---|---|
| **FH-Referenzdienst** | `tagessummen` im FH-Namespace `grp-eg-aa` eingerichtet; Abruf über Port-Forward mit API-Key erfolgreich | Externe DNS-/HTTPS-Erreichbarkeit, fachlicher AIT-Vertrag und Abnahme |
| **Eigenes EG-AA-Backend** | Lokale FastAPI-Anwendung; GraphQL-Ankerliste mit **16 Zählpunkten / 36 Messdaten-Ankern** | Deployment der Eigenanwendung im FH-Cluster |
| **Datenqualität** | Am **23.10.2026**: **36/36 vollständige** Zeitstempelreihen à 96 Viertelstunden; keine fehlenden, doppelten oder ungültigen Zeitstempel | Prüfung von Energie-/Leistungswerten auf Plausibilität |
| **API & Sicherheit** | Technischer `X-API-Key`; `/eg/datenqualitaet/gesamt` mit `Depends(authentifiziere_service)`; **200** mit gültigem, **401** ohne Schlüssel; **20 Unit-Tests bestanden** | Individuelle Anmeldung und tatsächliche benutzerbezogene RBAC-Durchsetzung |
| **Dashboard** | Lokale HTML-Demo über `/dashboard` | Authentifizierte Live-Daten-Anbindung |
| **Fachintegration** | Vorbereitung und technische Grundlagen | AIT-Prognose, IMC-Handel, Abrechnung, Observability |

**Abgrenzung:** Der **FH-Referenzdienst** und das **eigene lokale EG-AA-Backend** sind unterschiedliche Deployments. Ein erfolgreicher lokaler Test bedeutet nicht, dass die Eigenanwendung im FH-Cluster ausgerollt ist. „Vollständig“ bezieht sich derzeit auf **Zeitstempel**, nicht auf die inhaltliche Richtigkeit der Messwerte.

## Projektstruktur

```text
eg-aa/
├── backend/
│   ├── main.py                  # FastAPI-Endpunkte
│   ├── octomesh_client.py       # GraphQL-Zugriff
│   ├── data_quality.py          # Zeitstempel-Prüflogik
│   ├── eg_data_quality.py       # Prüfung aller Anker
│   ├── auth.py                  # Technischer API-Key
│   ├── permissions.py           # Rollen-/Zählpunktregeln
│   └── test_*.py                # Unit-Tests
├── frontend/index.html         # Demo-Dashboard
├── README.md
├── VSYS_Team_AA_Projektuebersicht.md
├── VSYS_Team_AA_Technische_Dokumentation.md
└── GITHUB_UPLOAD.md
```

## Lokal prüfen

In WSL2/Ubuntu im Projektordner:

```bash
cd ~/projekte/eg-aa
source .venv/bin/activate
PYTHONPATH=backend python -m unittest discover -s backend -p 'test_*.py' -q
```

Erwarteter zuletzt bestätigter Stand: **20 Tests, OK**. Für den Backend-Start sind die OctoMesh-Konfiguration und der technische API-Key aus Kubernetes erforderlich; den **vollständigen sicheren Start- und Testablauf** enthält die [technische Dokumentation, Kapitel 16](VSYS_Team_AA_Technische_Dokumentation.md#16-betrieb-wiederanlauf-und-diagnose).

## Dokumentation

- [Projektübersicht](VSYS_Team_AA_Projektuebersicht.md): Auftrag, Architektur, nachgewiesener Stand, offene Arbeiten und wichtige Pfade.
- [Technische Dokumentation](VSYS_Team_AA_Technische_Dokumentation.md): Aufbau, ausgeführte Übungen, GraphQL-Abfragen, Programmteile, Tests, Fehleranalysen und Wiederanlauf.
- [GitHub-Anleitung](GITHUB_UPLOAD.md): Änderungen sicher prüfen, committen und pushen.

## Sicherheit

**Keine Secrets, OAuth-Tokens, privaten kubeconfigs oder echten Zugangsdaten committen.** Der gemeinsame `X-API-Key` ist **keine individuelle Benutzeranmeldung**. Das Demo-Dashboard enthält noch keine Live-Energiedaten. Vor jeder Freigabe solcher Daten müssen Authentifizierung, Autorisierung und Zählpunktberechtigungen serverseitig umgesetzt sein.
