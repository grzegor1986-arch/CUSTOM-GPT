from __future__ import annotations

import time
from dataclasses import dataclass, field


@dataclass
class TokenBucket:
    rate_per_minute: int
    burst: int
    tokens: float = field(init=False)
    updated_at: float = field(default_factory=time.monotonic)

    def __post_init__(self) -> None:
        self.tokens = float(self.burst)

    def allow(self, cost: float = 1.0) -> bool:
        now = time.monotonic()
        elapsed = now - self.updated_at
        refill = elapsed * (self.rate_per_minute / 60)
        self.tokens = min(float(self.burst), self.tokens + refill)
        self.updated_at = now

        if self.tokens >= cost:
            self.tokens -= cost
            return True
        return False


@dataclass
class ConnectorGuard:
    kill_switches: dict[str, bool] = field(default_factory=dict)
    buckets: dict[str, TokenBucket] = field(default_factory=dict)

    def configure(self, connector: str, rate_per_minute: int, burst: int) -> None:
        self.buckets[connector] = TokenBucket(rate_per_minute=rate_per_minute, burst=burst)

    def set_kill_switch(self, connector: str, enabled: bool) -> None:
        self.kill_switches[connector] = enabled

    def check(self, connector: str, cost: float = 1.0) -> None:
        if self.kill_switches.get(connector, False):
            raise RuntimeError(f"Connector '{connector}' disabled by kill-switch")

        bucket = self.buckets.get(connector)
        if bucket is None:
            return
        if not bucket.allow(cost=cost):
            raise RuntimeError(f"Rate limit exceeded for connector '{connector}'")
