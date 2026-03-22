# CUSTOM-GPT

A lightweight workspace for experimenting with custom GPT behaviors and prompts. This repository currently contains scaffolding for future automation and serves as a starting point for small utilities or notebooks.

## Repository review (current state)
- The project is intentionally minimal and currently acts as a starter workspace.
- There is no application code yet (only documentation), so most value comes from clear setup and execution guidance.
- The next practical step is to define a first runnable utility (CLI, notebook, or script) and document how to run it.

## Getting started
1. Ensure you have Python 3.11 or later installed.
2. Create and activate a virtual environment (e.g., `python -m venv .venv && source .venv/bin/activate`).
3. Install any project dependencies as they are added.

## Connect GitHub to CustomGPT
### English
If you want to connect a GitHub repository to CustomGPT, follow these steps:
1. In the CustomGPT UI, open **Integrations** → **GitHub**.
2. Click **Connect GitHub** and authorize the CustomGPT app for your GitHub account.
3. Select the repository (or organization) you want to make available to CustomGPT.
4. Confirm the permissions and finish the setup.

Troubleshooting:
- Make sure you are logged into the correct GitHub account before authorizing.
- If you manage an organization, check that you have permission to install GitHub apps.
- If the repo does not appear, refresh the integration or re-run the authorization flow.

### Polski
Jeśli chcesz podłączyć repozytorium GitHub do CustomGPT, wykonaj te kroki:
1. W interfejsie CustomGPT otwórz **Integrations** → **GitHub**.
2. Kliknij **Connect GitHub** i autoryzuj aplikację CustomGPT na swoim koncie GitHub.
3. Wybierz repozytorium (lub organizację), które chcesz udostępnić w CustomGPT.
4. Potwierdź uprawnienia i zakończ konfigurację.

Wskazówki:
- Upewnij się, że jesteś zalogowany na właściwe konto GitHub przed autoryzacją.
- Jeśli zarządzasz organizacją, sprawdź, czy masz uprawnienia do instalacji aplikacji GitHub.
- Jeśli repozytorium nie jest widoczne, odśwież integrację lub ponownie uruchom proces autoryzacji.

## Suggested next upgrade
To move this repository from scaffolding to a usable starter, consider adding:
1. A `scripts/` or `src/` folder with one executable example.
2. A `requirements.txt` or `pyproject.toml` with pinned dependencies.
3. A short "Run" section with exact commands and expected output.
4. A simple CI check (format/lint) to keep changes consistent.

## Development
- Commit changes in small, reviewable increments.
- Keep configuration files under version control and avoid committing secrets.
- Use `.gitignore` to keep transient artifacts out of the repository.

## Contributing
Issues and pull requests are welcome as the project grows. Please include clear descriptions of any changes or ideas for new functionality.
