from pathlib import Path

from safe_tools.audit import AuditLogger
from safe_tools.auth import AuthService
from safe_tools.gateway import ToolGateway
from safe_tools.models import ToolCall, ToolConfig
from safe_tools.policy import PolicyEngine, PolicyRule
from safe_tools.rate_limit import ConnectorGuard
from safe_tools.telemetry import InMemoryMetrics, Tracer


def _fake_repo_write(args: dict) -> dict:
    return {"status": "written", "path": args["path"], "bytes": len(args["content"])}


def build_gateway() -> ToolGateway:
    auth = AuthService()
    auth.register_token("svc-ci", "ci-bot", "super-secret")
    auth.bind_roles("ci-bot", ["repo_writer", "ops_read"])

    policies = PolicyEngine(
        rules=[
            PolicyRule(effect="allow", action_pattern="repo.write", connector_pattern="github", required_roles=("repo_writer",)),
            PolicyRule(effect="deny", action_pattern="prod.db.read", connector_pattern="*"),
        ]
    )

    gateway = ToolGateway(
        auth_service=auth,
        policy_engine=policies,
        audit_logger=AuditLogger(Path("logs/tool_audit.jsonl")),
        tracer=Tracer(),
        metrics=InMemoryMetrics(),
        connector_guard=ConnectorGuard(),
    )

    gateway.register_tool(
        connector="github",
        tool="commit_file",
        handler=_fake_repo_write,
        config=ToolConfig(allowed_roles={"repo_writer"}, risk_level="high", rate_per_minute=20, burst=5),
    )

    return gateway


if __name__ == "__main__":
    gw = build_gateway()
    response = gw.execute(
        token_id="svc-ci",
        token_secret="super-secret",
        request=ToolCall(
            connector="github",
            tool="commit_file",
            action="repo.write",
            arguments={"path": "README.md", "content": "update"},
            request_id="req-001",
        ),
        retry_count=1,
        tool_cost=0.013,
    )
    print(response)
    print(gw.metrics.counters)
