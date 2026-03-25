from __future__ import annotations

import time
import uuid
from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class Span:
    trace_id: str
    name: str
    start_monotonic: float
    tags: dict[str, str]


@dataclass
class Tracer:
    active: dict[str, Span] = field(default_factory=dict)

    def start(self, name: str, tags: dict[str, str] | None = None) -> Span:
        span = Span(
            trace_id=uuid.uuid4().hex,
            name=name,
            start_monotonic=time.monotonic(),
            tags=tags or {},
        )
        self.active[span.trace_id] = span
        return span

    def finish(self, span: Span) -> float:
        self.active.pop(span.trace_id, None)
        return (time.monotonic() - span.start_monotonic) * 1000


@dataclass
class InMemoryMetrics:
    counters: dict[str, float] = field(default_factory=lambda: defaultdict(float))
    timers: dict[str, list[float]] = field(default_factory=lambda: defaultdict(list))

    def inc(self, name: str, value: float = 1.0, **labels: str) -> None:
        key = self._key(name, labels)
        self.counters[key] += value

    def observe(self, name: str, value: float, **labels: str) -> None:
        key = self._key(name, labels)
        self.timers[key].append(value)

    def _key(self, name: str, labels: dict[str, str]) -> str:
        ordered = ",".join(f"{k}={v}" for k, v in sorted(labels.items()))
        return f"{name}|{ordered}" if ordered else name
