from __future__ import annotations

from dataclasses import dataclass, field
from fnmatch import fnmatch
from typing import Iterable

from .models import Principal, ToolCall


@dataclass(frozen=True)
class PolicyRule:
    effect: str  # allow | deny
    action_pattern: str
    connector_pattern: str = "*"
    required_roles: tuple[str, ...] = ()


@dataclass
class PolicyEngine:
    rules: list[PolicyRule] = field(default_factory=list)

    def add_rules(self, rules: Iterable[PolicyRule]) -> None:
        self.rules.extend(rules)

    def evaluate(self, principal: Principal, request: ToolCall) -> None:
        decision = "deny"
        matched = False

        for rule in self.rules:
            if not fnmatch(request.action, rule.action_pattern):
                continue
            if not fnmatch(request.connector, rule.connector_pattern):
                continue
            if rule.required_roles and not set(principal.roles).intersection(rule.required_roles):
                continue

            matched = True
            decision = rule.effect
            if rule.effect == "deny":
                break

        if not matched:
            raise PermissionError(
                f"No matching policy rule for action='{request.action}' connector='{request.connector}'"
            )

        if decision != "allow":
            raise PermissionError(
                f"Policy denied action='{request.action}' on connector='{request.connector}'"
            )
