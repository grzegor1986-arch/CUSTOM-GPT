from __future__ import annotations

from typing import Any

from events.models import EventEnvelope

SUPPORTED_EVENTS = {"push", "pull_request", "issue_comment"}


def transform_github_webhook(event_name: str, body: dict[str, Any]) -> EventEnvelope | None:
    """Convert a GitHub webhook payload into internal EventEnvelope."""
    if event_name not in SUPPORTED_EVENTS:
        return None

    repository = (body.get("repository") or {}).get("full_name", "unknown/unknown")
    sender = (body.get("sender") or {}).get("login", "unknown")

    if event_name == "push":
        payload = {
            "ref": body.get("ref"),
            "before": body.get("before"),
            "after": body.get("after"),
            "commits": body.get("commits", []),
        }
    elif event_name == "pull_request":
        pr = body.get("pull_request") or {}
        payload = {
            "action": body.get("action"),
            "number": body.get("number"),
            "title": pr.get("title"),
            "state": pr.get("state"),
            "draft": pr.get("draft"),
            "base": (pr.get("base") or {}).get("ref"),
            "head": (pr.get("head") or {}).get("ref"),
            "diff_url": pr.get("diff_url"),
            "html_url": pr.get("html_url"),
        }
    else:
        issue = body.get("issue") or {}
        comment = body.get("comment") or {}
        payload = {
            "action": body.get("action"),
            "issue_number": issue.get("number"),
            "issue_title": issue.get("title"),
            "comment_body": comment.get("body"),
            "comment_url": comment.get("html_url"),
        }

    return EventEnvelope.create(
        event_type=event_name,
        repository=repository,
        actor=sender,
        payload=payload,
        raw=body,
    )
