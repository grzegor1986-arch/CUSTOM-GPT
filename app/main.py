from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException

from events.github_transformer import transform_github_webhook
from storage.runs import InMemoryRunsStorage
from workflows.engine import WorkflowEngine

app = FastAPI(title="Automation Event Layer")
storage = InMemoryRunsStorage()
engine = WorkflowEngine(storage=storage)


@app.post("/webhooks/github")
async def github_webhook(payload: dict, x_github_event: str = Header(default="")) -> dict:
    event = transform_github_webhook(event_name=x_github_event, body=payload)
    if event is None:
        raise HTTPException(status_code=400, detail=f"Unsupported GitHub event: {x_github_event}")

    run = engine.dispatch(event)
    return {
        "accepted": True,
        "run_id": run.run_id,
        "status": run.status.value,
        "workflow": run.workflow_name,
        "event": {"id": run.event.event_id, "type": run.event.event_type},
    }


@app.get("/runs/{run_id}")
async def get_run(run_id: str) -> dict:
    run = storage.get(run_id)
    if run is None:
        raise HTTPException(status_code=404, detail="Run not found")

    return {
        "run_id": run.run_id,
        "workflow": run.workflow_name,
        "status": run.status.value,
        "steps": [
            {
                "name": step.name,
                "status": step.status.value,
                "output": step.output,
                "error": step.error,
            }
            for step in run.steps
        ],
    }
