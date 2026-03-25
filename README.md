# CUSTOM-GPT

A lightweight workspace for experimenting with custom GPT behaviors and prompts.

## ops-ui
Repository now contains `ops-ui/` frontend for orchestrator operators:
- Runs: timeline kroków, błędy i logi narzędzi.
- Connectors: healthcheck i status autoryzacji.
- Policies: edycja reguł dostępu i listy dozwolonych akcji.
- Operator actions: retry run, cancel run, manual approve dla kroków wrażliwych.
- KPI dashboard: średni czas wykonania, skuteczność, najczęściej używane narzędzia.

### Run locally
1. `cd ops-ui`
2. `npm install`
3. `npm run dev`

Frontend expected orchestrator API under `/api/*` (configured in Vite proxy with `ORCHESTRATOR_URL`, default `http://localhost:8080`).
