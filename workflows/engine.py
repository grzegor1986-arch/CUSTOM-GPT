from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable

from events.models import EventEnvelope, RunRecord, RunStatus, StepResult, StepStatus
from storage.runs import RunsStorage
from workflows.rules import match_workflow

StepHandler = Callable[[RunRecord, dict[str, Any]], dict[str, Any]]


class WorkflowEngine:
    def __init__(self, storage: RunsStorage) -> None:
        self.storage = storage
        self.step_order = ["classify", "decide", "run_tools", "summarize", "notify"]
        self.handlers: dict[str, StepHandler] = {
            "classify": self._classify,
            "decide": self._decide,
            "run_tools": self._run_tools,
            "summarize": self._summarize,
            "notify": self._notify,
        }

    def dispatch(self, event: EventEnvelope) -> RunRecord:
        workflow_name = match_workflow(event)
        run = RunRecord.create(event, workflow_name=workflow_name)
        run.status = RunStatus.RUNNING
        run.steps = [StepResult(name=step) for step in self.step_order]
        self.storage.create(run)

        context: dict[str, Any] = {}
        for step in run.steps:
            step.started_at = datetime.now(tz=timezone.utc).isoformat()
            step.status = StepStatus.RUNNING
            self.storage.update(run)

            try:
                output = self.handlers[step.name](run, context)
                context[step.name] = output
                step.output = output
                step.status = StepStatus.COMPLETED
            except Exception as exc:  # noqa: BLE001
                step.status = StepStatus.FAILED
                step.error = str(exc)
                run.status = RunStatus.FAILED
                step.finished_at = datetime.now(tz=timezone.utc).isoformat()
                self.storage.update(run)
                return run

            step.finished_at = datetime.now(tz=timezone.utc).isoformat()
            self.storage.update(run)

        run.status = RunStatus.COMPLETED
        self.storage.update(run)
        return run

    def _classify(self, run: RunRecord, _: dict[str, Any]) -> dict[str, Any]:
        event = run.event
        return {
            "event_type": event.event_type,
            "severity": "medium" if event.event_type == "pull_request" else "low",
            "tags": [event.event_type, event.repository],
        }

    def _decide(self, run: RunRecord, context: dict[str, Any]) -> dict[str, Any]:
        classification = context["classify"]
        should_analyze_diff = run.workflow_name == "pr_opened_analysis"
        actions = ["post_summary"]
        if should_analyze_diff:
            actions.insert(0, "analyze_diff")
            actions.append("post_recommendations")
        return {"workflow": run.workflow_name, "classification": classification, "actions": actions}

    def _run_tools(self, run: RunRecord, context: dict[str, Any]) -> dict[str, Any]:
        actions: list[str] = context["decide"]["actions"]
        outputs: dict[str, Any] = {}
        if "analyze_diff" in actions:
            outputs["diff_analysis"] = {
                "risk_score": 0.35,
                "insights": [
                    "Consider adding tests for changed files.",
                    "Check if PR description maps to code changes.",
                ],
            }
        outputs["tools_executed"] = actions
        return outputs

    def _summarize(self, run: RunRecord, context: dict[str, Any]) -> dict[str, Any]:
        tools = context["run_tools"]
        summary = [f"Workflow `{run.workflow_name}` finished for `{run.event.repository}`."]
        if tools.get("diff_analysis"):
            summary.extend(tools["diff_analysis"]["insights"])
        return {"message": " ".join(summary)}

    def _notify(self, run: RunRecord, context: dict[str, Any]) -> dict[str, Any]:
        summary = context["summarize"]["message"]
        notification = {
            "target": "github_comment",
            "body": summary,
            "event_id": run.event.event_id,
            "run_id": run.run_id,
        }
        # Here you would invoke GitHub API/queue publisher.
        return notification
