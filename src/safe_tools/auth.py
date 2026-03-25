from __future__ import annotations

import hashlib
import hmac
from dataclasses import dataclass, field
from typing import Iterable

from .models import Principal


@dataclass(frozen=True)
class ServiceToken:
    token_id: str
    subject: str
    secret_hash: str
    active: bool = True


@dataclass(frozen=True)
class RoleBinding:
    subject: str
    roles: tuple[str, ...]


@dataclass
class AuthService:
    _tokens: dict[str, ServiceToken] = field(default_factory=dict)
    _roles: dict[str, tuple[str, ...]] = field(default_factory=dict)

    @staticmethod
    def hash_secret(raw_secret: str) -> str:
        return hashlib.sha256(raw_secret.encode("utf-8")).hexdigest()

    def register_token(self, token_id: str, subject: str, raw_secret: str) -> ServiceToken:
        token = ServiceToken(
            token_id=token_id,
            subject=subject,
            secret_hash=self.hash_secret(raw_secret),
            active=True,
        )
        self._tokens[token_id] = token
        return token

    def bind_roles(self, subject: str, roles: Iterable[str]) -> None:
        self._roles[subject] = tuple(sorted(set(roles)))

    def authenticate(self, token_id: str, raw_secret: str) -> Principal:
        token = self._tokens.get(token_id)
        if token is None or not token.active:
            raise PermissionError("Invalid or inactive service token")

        submitted_hash = self.hash_secret(raw_secret)
        if not hmac.compare_digest(token.secret_hash, submitted_hash):
            raise PermissionError("Invalid service token secret")

        roles = self._roles.get(token.subject, tuple())
        return Principal(subject=token.subject, token_id=token.token_id, roles=roles)

    def authorize_tool(self, principal: Principal, allowed_roles: set[str]) -> None:
        if not allowed_roles:
            return

        if not set(principal.roles).intersection(allowed_roles):
            raise PermissionError(
                f"Principal '{principal.subject}' lacks required roles: {sorted(allowed_roles)}"
            )
