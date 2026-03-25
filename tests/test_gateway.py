import json
from pathlib import Path

from safe_tools.audit import AuditLogger
from safe_tools.auth import AuthService
from safe_tools.gateway import ToolGateway
from safe_tools.models import ToolCall, ToolConfig
from safe_tools.policy import PolicyEngine, PolicyRule
from safe_tools.rate_limit import ConnectorGuard
from safe_tools.telemetry import InMemoryMetrics, Tracer


def _build_gateway(tmp_path: Path) -> ToolGateway:
    auth = AuthService()
    auth.register_token("svc", "ci-bot", "secret")
    auth.bind_roles("ci-bot", ["repo_writer"])

    gateway = ToolGateway(
        auth_service=auth,
        policy_engine=PolicyEngine(
            rules=[
                PolicyRule(effect="allow", action_pattern="repo.write", connector_pattern="github", required_roles=("repo_writer",)),
                PolicyRule(effect="deny", action_pattern="prod.db.read", connector_pattern="*"),
            ]
        ),
        audit_logger=AuditLogger(tmp_path / "audit.jsonl"),
        tracer=Tracer(),
        metrics=InMemoryMetrics(),
        connector_guard=ConnectorGuard(),
    )

    gateway.register_tool(
        connector="github",
        tool="commit_file",
        handler=lambda args: {"ok": True, **args},
        config=ToolConfig(allowed_roles={"repo_writer"}, rate_per_minute=10, burst=2),
    )
    return gateway


def test_gateway_success_and_audit(tmp_path: Path) -> None:
    gateway = _build_gateway(tmp_path)
    result = gateway.execute(
        token_id="svc",
        token_secret="secret",
        request=ToolCall(
            connector="github",
            tool="commit_file",
            action="repo.write",
            arguments={"path": "README.md"},
            request_id="req-1",
        ),
        retry_count=2,
        tool_cost=0.42,
    )

    assert result.ok is True
    assert result.output["path"] == "README.md"

    lines = (tmp_path / "audit.jsonl").read_text(encoding="utf-8").splitlines()
    event = json.loads(lines[0])
    assert event["subject"] == "ci-bot"
    assert event["action"] == "repo.write"
    assert event["retries"] == 2


def test_policy_denied(tmp_path: Path) -> None:
    gateway = _build_gateway(tmp_path)
    try:
        gateway.execute(
            token_id="svc",
            token_secret="secret",
            request=ToolCall(
                connector="github",
                tool="commit_file",
                action="prod.db.read",
                arguments={"query": "select 1"},
                request_id="req-2",
            ),
        )
    except PermissionError as exc:
        assert "Policy denied" in str(exc)
    else:
        raise AssertionError("Expected PermissionError")


def test_kill_switch(tmp_path: Path) -> None:
    gateway = _build_gateway(tmp_path)
    gateway.connector_guard.set_kill_switch("github", True)

    try:
        gateway.execute(
            token_id="svc",
            token_secret="secret",
            request=ToolCall(
                connector="github",
                tool="commit_file",
                action="repo.write",
                arguments={"path": "README.md"},
                request_id="req-3",
            ),
        )
    except RuntimeError as exc:
        assert "kill-switch" in str(exc)
    else:
        raise AssertionError("Expected RuntimeError")
