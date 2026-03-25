from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .audit import AuditLogger
from .auth import AuthService
from .models import AuditEvent, ExecutionResult, ToolCall, ToolConfig
from .policy import PolicyEngine
from .rate_limit import ConnectorGuard
from .telemetry import InMemoryMetrics, Tracer


class ToolGatewayError(RuntimeError):
    pass


@dataclass
class ToolGateway:
    auth_service: AuthService
    policy_engine: PolicyEngine
    audit_logger: AuditLogger
    tracer: Tracer
    metrics: InMemoryMetrics
    connector_guard: ConnectorGuard
    tool_registry: dict[tuple[str, str], Callable[[dict[str, Any]], Any]] = field(default_factory=dict)
    tool_configs: dict[tuple[str, str], ToolConfig] = field(default_factory=dict)

    def register_tool(
        self,
        connector: str,
        tool: str,
        handler: Callable[[dict[str, Any]], Any],
        config: ToolConfig | None = None,
    ) -> None:
        key = (connector, tool)
        self.tool_registry[key] = handler
        self.tool_configs[key] = config or ToolConfig()
        cfg = self.tool_configs[key]
        self.connector_guard.configure(connector, cfg.rate_per_minute, cfg.burst)

    def execute(
        self,
        *,
        token_id: str,
        token_secret: str,
        request: ToolCall,
        retry_count: int = 0,
        tool_cost: float = 0.0,
    ) -> ExecutionResult:
        key = (request.connector, request.tool)
        handler = self.tool_registry.get(key)
        if handler is None:
            raise ToolGatewayError(f"No tool handler registered for {key}")

        config = self.tool_configs[key]
        principal = self.auth_service.authenticate(token_id, token_secret)
        self.auth_service.authorize_tool(principal, config.allowed_roles)
        self.policy_engine.evaluate(principal, request)
        self.connector_guard.check(request.connector)

        span = self.tracer.start(
            "tool.execute",
            tags={
                "connector": request.connector,
                "tool": request.tool,
                "subject": principal.subject,
            },
        )

        self.metrics.inc("tool.calls", connector=request.connector, tool=request.tool)
        result: ExecutionResult

        try:
            output = handler(request.arguments)
            result = ExecutionResult(
                ok=True,
                output=output,
                retries=retry_count,
                cost=tool_cost,
            )
            self.metrics.inc("tool.success", connector=request.connector, tool=request.tool)
        except Exception as exc:
            result = ExecutionResult(
                ok=False,
                output=None,
                error=str(exc),
                retries=retry_count,
                cost=tool_cost,
            )
            self.metrics.inc("tool.failure", connector=request.connector, tool=request.tool)

        latency_ms = self.tracer.finish(span)
        self.metrics.observe("tool.latency_ms", latency_ms, connector=request.connector, tool=request.tool)
        self.metrics.observe("tool.retry_count", retry_count, connector=request.connector, tool=request.tool)
        self.metrics.observe("tool.cost", tool_cost, connector=request.connector, tool=request.tool)

        event = AuditEvent.from_result(
            request=request,
            principal=principal,
            result=result,
            latency_ms=latency_ms,
            trace_id=span.trace_id,
        )
        self.audit_logger.log(event)

        self.connector_guard.check(request.connector)

        return result
