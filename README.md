# CUSTOM-GPT

A lightweight workspace for experimenting with custom GPT behaviors and prompts.

## Event-driven automation layer

This repository now includes an event automation layer based on `events/` + `workflows/`.

### What was added
- GitHub webhook receiver: `POST /webhooks/github`.
- Webhook transformation into internal `EventEnvelope` format for:
  - `push`
  - `pull_request`
  - `issue_comment`
- Workflow engine with a simple DAG-style sequence of steps:
  - `classify -> decide -> run_tools -> summarize -> notify`
- Runs storage with durable append-only logging to `data/runs.log`.
- Automatic rule example:
  - `pull_request` with action `opened` triggers `pr_opened_analysis`
  - Workflow generates recommendations-ready summary payload for notification/comment.

## Project structure
- `app/main.py` – FastAPI app with webhook endpoint and run inspection endpoint.
- `events/models.py` – event and run domain models (`EventEnvelope`, `RunRecord`, statuses).
- `events/github_transformer.py` – GitHub-to-internal event translation.
- `workflows/engine.py` – workflow orchestration and step execution.
- `workflows/rules.py` – event-to-workflow rule mapping.
- `storage/runs.py` – runs persistence abstraction + in-memory implementation with durable log.
- `tests/` – unit tests for transformer and workflow execution.

## Getting started
1. Ensure you have Python 3.11+.
2. Create and activate a virtual environment:
   - `python -m venv .venv && source .venv/bin/activate`
3. Install dependencies:
   - `pip install fastapi uvicorn pytest`
4. Run API:
   - `uvicorn app.main:app --reload`
5. Run tests:
   - `python -m pytest -q`

## Example webhook call

```bash
curl -X POST 'http://127.0.0.1:8000/webhooks/github' \
  -H 'Content-Type: application/json' \
  -H 'X-GitHub-Event: pull_request' \
  -d '{
    "action": "opened",
    "number": 42,
    "pull_request": {
      "title": "Add automation layer",
      "state": "open",
      "draft": false,
      "base": {"ref": "main"},
      "head": {"ref": "feature/events"},
      "diff_url": "https://example.com/pr.diff",
      "html_url": "https://github.com/acme/repo/pull/42"
    },
    "repository": {"full_name": "acme/repo"},
    "sender": {"login": "octocat"}
  }'
```
