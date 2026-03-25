from events.models import EventEnvelope, RunStatus, StepStatus
from storage.runs import InMemoryRunsStorage
from workflows.engine import WorkflowEngine


def test_pr_opened_triggers_analysis_workflow() -> None:
    storage = InMemoryRunsStorage(durable_log_path="data/test-runs.log")
    engine = WorkflowEngine(storage)

    event = EventEnvelope.create(
        event_type="pull_request",
        repository="acme/repo",
        actor="octocat",
        payload={"action": "opened", "number": 1},
    )

    run = engine.dispatch(event)

    assert run.workflow_name == "pr_opened_analysis"
    assert run.status == RunStatus.COMPLETED
    assert all(step.status == StepStatus.COMPLETED for step in run.steps)
    notify_step = next(step for step in run.steps if step.name == "notify")
    assert "github_comment" == notify_step.output["target"]
