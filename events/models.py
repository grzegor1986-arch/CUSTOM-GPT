from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any
from uuid import uuid4


class RunStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


class StepStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass(slots=True)
class EventEnvelope:
    event_id: str
    event_type: str
    source: str
    occurred_at: str
    repository: str
    actor: str
    payload: dict[str, Any]
    raw: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        event_type: str,
        repository: str,
        actor: str,
        payload: dict[str, Any],
        source: str = "github",
        raw: dict[str, Any] | None = None,
    ) -> "EventEnvelope":
        return cls(
            event_id=f"evt_{uuid4()}",
            event_type=event_type,
            source=source,
            occurred_at=datetime.now(tz=timezone.utc).isoformat(),
            repository=repository,
            actor=actor,
            payload=payload,
            raw=raw or {},
        )


@dataclass(slots=True)
class StepResult:
    name: str
    status: StepStatus = StepStatus.PENDING
    output: dict[str, Any] = field(default_factory=dict)
    error: str | None = None
    started_at: str | None = None
    finished_at: str | None = None


@dataclass(slots=True)
class RunRecord:
    run_id: str
    event: EventEnvelope
    workflow_name: str
    status: RunStatus = RunStatus.PENDING
    steps: list[StepResult] = field(default_factory=list)
    created_at: str = field(default_factory=lambda: datetime.now(tz=timezone.utc).isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now(tz=timezone.utc).isoformat())

    @classmethod
    def create(cls, event: EventEnvelope, workflow_name: str) -> "RunRecord":
        return cls(run_id=f"run_{uuid4()}", event=event, workflow_name=workflow_name)
