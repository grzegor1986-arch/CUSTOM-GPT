from __future__ import annotations

from events.models import EventEnvelope


def match_workflow(event: EventEnvelope) -> str:
    """Select workflow based on event type/action rules."""
    if event.event_type == "pull_request" and event.payload.get("action") == "opened":
        return "pr_opened_analysis"
    return "default_automation"
