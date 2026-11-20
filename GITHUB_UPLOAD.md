# Dokumentation in GitHub hochladen

## Einmalig: Dokumente ins **eigene** Repository kopieren

1. ZIP aus ChatGPT herunterladen und **lokal entpacken** (z. B. in Windows `Downloads`).
2. Die vier Markdown-Dateien `README.md`, `VSYS_Team_AA_Projektuebersicht.md`, `VSYS_Team_AA_Technische_Dokumentation.md`, `GITHUB_UPLOAD.md` in `~/projekte/eg-aa/` kopieren. Für ein bereits bestehendes `README.md` **zuerst prüfen und zusammenführen**, nicht blind überschreiben. Die bisherige Projektübersicht und technische Dokumentation sind hier bereits *fortgeschriebene Versionen*. **`GITHUB_UPLOAD.md` nur falls gewünscht**.
3. `.gitignore` im Projektwurzelverzeichnis anlegen bzw. mit dem mitgelieferten `gitignore_VORLAGE.txt` **zusammenführen**, nicht bestehende Regeln überschreiben.

Wenn die ZIP in Windows `Downloads` liegt, kannst du aus WSL so vorgehen (Windows-Benutzername anpassen):

```bash
cd ~/projekte/eg-aa
# Pfad auf den tatsächlich entpackten Ordner anpassen:
ls /mnt/c/Users/<WINDOWS-BENUTZER>/Downloads/AA_Nexus_GitHub_Dokumentation/
cp /mnt/c/Users/<WINDOWS-BENUTZER>/Downloads/AA_Nexus_GitHub_Dokumentation/*.md ./
```

**Wichtig:** Wenn Dateien im Projekt bereits verändert wurden, vor dem Kopieren sichern oder mit `diff` vergleichen. Bei der Vorlage `gitignore_VORLAGE.txt` die Regeln zur bestehenden `.gitignore` ergänzen.

## Git vorbereiten

```bash
cd ~/projekte/eg-aa
git status
# Falls das Verzeichnis noch KEIN Git-Repository ist:
git init
# Bestehende Remotes prüfen:
git remote -v
```

Verwendet ihr bereits ein Team-Repository, dessen `origin` festgelegt ist, **kein neues Repo anlegen und keine Remote ersetzen**. Falls das eigene GitHub-Repository noch fehlt: auf https://github.com/new ein **privates** Repository (z. B. `eg-aa`) erstellen, ohne Dateien vorab hinzuzufügen, wenn dein lokales Git-Repo den ersten Commit liefern soll. Danach bei fehlendem `origin`:

```bash
git remote add origin https://github.com/<GITHUB-BENUTZER-ODER-ORG>/eg-aa.git
```

## Nur die Dokumentation committen (empfohlen)

```bash
cd ~/projekte/eg-aa
git add README.md VSYS_Team_AA_Projektuebersicht.md VSYS_Team_AA_Technische_Dokumentation.md GITHUB_UPLOAD.md
# Wenn eine geprüfte .gitignore vorliegt:
git add .gitignore

git status
git diff --cached --stat
git diff --cached
# Erst nach Prüfung:
git commit -m "docs: update EG-AA architecture, GraphQL research and tests"
```

Falls `git commit` nach Name/E-Mail fragt, **eigene** Werte setzen:

```bash
git config user.name "<DEIN-NAME>"
git config user.email "<DEINE-GITHUB-EMAIL>"
```

Den ersten Push eines **neuen, eigenen** Repositories kann man so durchführen:

```bash
git branch -M main
git push -u origin main
```

**Bei bestehendem Team-Repo** zuerst mit `git branch --show-current` und `git status` die aktive Branch und den Zustand überprüfen; dann die bestehende Branch pushen, z. B. `git push origin <BRANCHNAME>`. Nicht blind `git branch -M main` oder `git push --force` ausführen. Bei GitHub-HTTPS kann eine Browser-Anmeldung / Credential Manager / ein **Personal Access Token** erforderlich sein; ein GitHub-Passwort allein funktioniert nicht als Git-Zugangsdaten. Zugangstoken niemals in die URL oder README schreiben.

## Vor jedem Push auf Geheimnisse prüfen

```bash
git status
git diff --cached --name-only
git diff --cached
```

Nicht committen: `.venv/`, `.env`, `.kube/`, echte Kubernetes-Secret-Dateien, `*.kubeconfig`, lokale Shell-Logfiles, Token/API-Keys, private Zertifikate, `__pycache__/`. Bestehende bereits versionierte Geheimnisse werden durch `.gitignore` **nicht** aus Git entfernt.

**Verlauf und Status:** Die Dokumentation bildet den Stand am 20.11.2026 ab. Neue Code-Dateien werden nicht durch dieses Doku-Paket automatisch erzeugt oder in Git hochgeladen.
