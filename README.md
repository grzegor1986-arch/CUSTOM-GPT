# CUSTOM-GPT

Minimalne repozytorium startowe do eksperymentów z własnym GPT i automatyzacjami.

## Co zawiera
- `pyproject.toml` z podstawową konfiguracją projektu Python.
- Pakiet `custom_gpt` w `src/`.
- Proste CLI dostępne jako komenda `custom-gpt`.

## Szybki start
1. Upewnij się, że masz Python 3.11+.
2. (Opcjonalnie) utwórz wirtualne środowisko:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
3. Zainstaluj projekt lokalnie:
   ```bash
   pip install -e .
   ```
4. Uruchom:
   ```bash
   custom-gpt
   ```

## Rozwój
- Rób małe, czytelne commity.
- Nie commituj sekretów.
- Uzupełniaj `.gitignore` wraz z rozwojem projektu.
