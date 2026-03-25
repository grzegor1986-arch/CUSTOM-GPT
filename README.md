# CUSTOM-GPT

A lightweight workspace for experimenting with custom GPT behaviors and prompts.

## Connector architecture
The repository now includes a connector hub with a shared contract and source-specific adapters:

- `connectors/base.py` defines the `Connector` interface with `describe_tools()`, `execute(tool_name, args)` and `health()`.
- `connectors/registry.py` loads connector instances from `config/connectors.yaml`.
- `connectors/hub.py` supports capability-tag routing (`code`, `tickets`, `knowledge`, `messaging`).
- Source-specific connectors live in:
  - `connectors/github` (MCP server adapter)
  - `connectors/slack` (HTTP adapter)
  - `connectors/postgres` (SDK adapter)

## Getting started
1. Ensure you have Python 3.11 or later installed.
2. Create and activate a virtual environment (e.g., `python -m venv .venv && source .venv/bin/activate`).
3. Install dependencies as needed (for tests: `pip install pytest pyyaml`).

## Development
- Commit changes in small, reviewable increments.
- Keep configuration files under version control and avoid committing secrets.
- Use `.gitignore` to keep transient artifacts out of the repository.

## Testing
Run:

```bash
pytest
```
