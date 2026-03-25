from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass(frozen=True)
class ToolCall:
    connector: str
    tool: str
    action: str
    arguments: dict[str, Any]
    request_id: str


@dataclass(frozen=True)
class Principal:
    subject: str
    token_id: str
    roles: tuple[str, ...]


@dataclass
class ExecutionResult:
    ok: bool
    output: Any
    error: str | None = None
    retries: int = 0
    cost: float = 0.0


@dataclass
class AuditEvent:
    timestamp: datetime
    request_id: str
    subject: str
    connector: str
    tool: str
    action: str
    arguments: dict[str, Any]
    outcome: str
    error: str | None
    latency_ms: float
    retries: int
    cost: float
    trace_id: str

    @classmethod
    def from_result(
        cls,
        *,
        request: ToolCall,
        principal: Principal,
        result: ExecutionResult,
        latency_ms: float,
        trace_id: str,
    ) -> "AuditEvent":
        return cls(
            timestamp=datetime.now(timezone.utc),
            request_id=request.request_id,
            subject=principal.subject,
            connector=request.connector,
            tool=request.tool,
            action=request.action,
            arguments=request.arguments,
            outcome="success" if result.ok else "error",
            error=result.error,
            latency_ms=latency_ms,
            retries=result.retries,
            cost=result.cost,
            trace_id=trace_id,
        )


@dataclass
class ToolConfig:
    allowed_roles: set[str] = field(default_factory=set)
    risk_level: str = "medium"
    rate_per_minute: int = 60
    burst: int = 15
