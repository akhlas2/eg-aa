# AA_Nexus – Energiegemeinschaft (VSYS WS 2026/27)

**Team:** AA · **FH Salzburg** · **Mandant:** `eg-aa` · **Stand:** 20.11.2026

Dieses Repository dokumentiert die EG-Arbeiten in **Verteilte Systeme und Cloud-Technologien**. Es gibt **zwei getrennte Implementierungsstände**: (1) den im FH-Cluster `cloud-lab` eingesetzten **Tagessummen-Referenzdienst** (Ingress/DNS noch offen) und (2) das **eigene lokale EG-AA-FastAPI-Backend** samt GraphQL-Client, Datenqualitätsprüfung und Demo-Dashboard. Die zweite Anwendung ist noch nicht im FH-Cluster deployed oder formal abgenommen.

## Dokumentation

- **[Projektübersicht](VSYS_Team_AA_Projektuebersicht.md):** Ziel, Architektur, lokaler/FH-Status, offene Aufgaben, Kurzfassung Schritt 20.
- **[Technische Dokumentation](VSYS_Team_AA_Technische_Dokumentation.md):** Vollständige historische Schritte, sichere Befehle, Kubernetes, FH-Deployment, Ingress, GraphQL-Recherche, Backend, Datenqualität und Tests.
- **[GitHub-Anleitung](GITHUB_UPLOAD.md):** Dokumentation ins eigene Repository übernehmen und sicher veröffentlichen.

## Aktueller nachgewiesener lokaler Stand

| Teil | Ergebnis |
|---|---|
| Zählpunkte / Messdaten-Anker | 16 / 36, über GraphQL dynamisch ermittelt |
| Zeitstempelqualität am 23.10.2026 | 36/36 vollständige Viertelstunden-Messreihen |
| Testabdeckung | 11 Unit-Tests bestanden |
| Eigene API | `GET /eg/datenqualitaet`, `/eg/datenqualitaet/gesamt` – HTTP 200 mit Key, 401 ohne |
| Browser-Dashboard | `http://127.0.0.1:8000/dashboard` – lokale Demo, keine Live-Daten |
| Benutzerbezogene Authentifizierung und RBAC | noch nicht integriert |
| AIT / IMC / M2 und FH-Deployment der Eigenanwendung | noch offen |

> **Sicherheit:** Diese Dateien enthalten keine Tokens, Passwörter oder privaten kubeconfigs. Live-Energiedaten gehören nicht ohne Benutzerprüfung in ein öffentliches Frontend. Vor Commit und Push immer `git diff --cached` kontrollieren.
