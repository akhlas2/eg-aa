# EG-AA – GitHub-Workflow

**Lokales Projekt:** `~/projekte/eg-aa` · **Repository:** [akhlas2/eg-aa](https://github.com/akhlas2/eg-aa) · **Branch:** `main`

Das Git-Repository ist **bereits eingerichtet**. Der erste Commit (`d5d35cf`) wurde erfolgreich hochgeladen. **Kein neues Repository erstellen und nicht erneut `git init` ausführen.**

## 1. Dokumentation aktualisieren

Die vier Dateien aus dem aktuellen Dokumentationspaket in den Projekt-Hauptordner übernehmen:

```text
eg-aa/
├── README.md
├── VSYS_Team_AA_Projektuebersicht.md
├── VSYS_Team_AA_Technische_Dokumentation.md
└── GITHUB_UPLOAD.md
```

Vor dem Ersetzen prüfen, ob du vorhandene Dateien zwischenzeitlich selbst verändert hast. Nur die vier Markdown-Dateien ersetzen; `backend/`, `frontend/` und `.gitignore` **nicht** überschreiben.

## 2. Änderungen und Tests kontrollieren

Im WSL-Terminal:

```bash
cd ~/projekte/eg-aa

git status --short
git diff --stat
# Zeigt Änderungen an bereits versionierten Dokumenten und Quelltexten:
git diff

source .venv/bin/activate
PYTHONPATH=backend python -m unittest discover -s backend -p 'test_*.py' -q
```

Zuletzt nachgewiesen: **20 Tests, OK**. Wenn Git neue Dateien mit `??` zeigt, sind diese zunächst **noch nicht** Bestandteil von `git diff`.

## 3. Gewünschte Dateien gezielt vormerken

```bash
git add README.md \
  VSYS_Team_AA_Projektuebersicht.md \
  VSYS_Team_AA_Technische_Dokumentation.md \
  GITHUB_UPLOAD.md \
  backend/main.py \
  backend/auth.py backend/test_auth.py \
  backend/permissions.py backend/test_permissions.py

git diff --cached --name-only
git diff --cached --stat
git diff --cached
```

**Vor dem Commit den vollständigen vorgemerkten Diff prüfen:** Keine echten Tokens, Passwörter, Client-Secrets, privaten kubeconfigs, `.env`-Dateien oder personenbezogenen Rohdaten hochladen. Auch bei einem **privaten** Repository dürfen keine Geheimnisse eingecheckt werden. `.gitignore` ist nur eine zusätzliche Schutzmaßnahme.

## 4. Commit und Push

Wenn Tests, Inhalt und Geheimnisprüfung passen:

```bash
git commit -m "docs: aktualisiere EG-AA-Dokumentation und Zugriffsschutz"
git push
git status -sb
```

Für den bestehenden Branch `main` mit eingerichteter Upstream-Verbindung reicht **`git push`**. Eine erfolgreiche Ausgabe enthält üblicherweise `main -> main`; `git status -sb` sollte dann keine offenen Änderungen mehr anzeigen.

Das Repository öffnen: <https://github.com/akhlas2/eg-aa>

## 5. Häufige Fragen

| Situation | Vorgehen |
|---|---|
| `.venv` aktivieren? | Für Python-Tests ja: `source .venv/bin/activate`. Für Git nicht nötig. |
| Änderung noch nicht sichtbar? | Erst committen, dann `git push`; danach GitHub-Seite neu laden. |
| Git zeigt `??`? | Neue, noch nicht vorgemerkte Datei; gezielt mit `git add DATEI` aufnehmen. |
| Falsche Branch? | `git status -sb` und `git branch --show-current` kontrollieren. |
| Zugriff für Teammitglied? | In einem privaten persönlichen Repository unter **Settings → Collaborators** einladen; diese Berechtigung umfasst üblicherweise auch Schreibzugriff. Für echten Read-only-Zugriff eine GitHub-Organisation mit passender Rolle verwenden. |
| Eine Datei enthält ein echtes Secret? | **Nicht committen/pushen**; zuerst bereinigen. Bereits veröffentlichte Secrets als kompromittiert behandeln und rotieren. |

## 6. Nächste Entwicklungsarbeiten

Die technische Umsetzung wird in [der technischen Dokumentation](VSYS_Team_AA_Technische_Dokumentation.md) und [der Projektübersicht](VSYS_Team_AA_Projektuebersicht.md) dokumentiert. Die nächste fachliche Aufgabe ist **eine vertrauenswürdige Benutzeranmeldung und serverseitige RBAC-Durchsetzung**, nicht die erneute Einrichtung von Git.
