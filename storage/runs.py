from __future__ import annotations

import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from threading import Lock
from typing import Protocol

from events.models import RunRecord


class RunsStorage(Protocol):
    def create(self, run: RunRecord) -> None: ...

    def update(self, run: RunRecord) -> None: ...

    def get(self, run_id: str) -> RunRecord | None: ...


class InMemoryRunsStorage:
    """Backed by memory + durable jsonl log.

    In production, replace with Postgres/Redis implementations.
    """

    def __init__(self, durable_log_path: str = "data/runs.log") -> None:
        self._runs: dict[str, RunRecord] = {}
        self._lock = Lock()
        self._log_path = Path(durable_log_path)
        self._log_path.parent.mkdir(parents=True, exist_ok=True)

    def create(self, run: RunRecord) -> None:
        with self._lock:
            self._runs[run.run_id] = run
            self._append_log("create", run)

    def update(self, run: RunRecord) -> None:
        with self._lock:
            run.updated_at = datetime.now(tz=timezone.utc).isoformat()
            self._runs[run.run_id] = run
            self._append_log("update", run)

    def get(self, run_id: str) -> RunRecord | None:
        return self._runs.get(run_id)

    def _append_log(self, op: str, run: RunRecord) -> None:
        entry = {"op": op, "timestamp": datetime.now(tz=timezone.utc).isoformat(), "run": asdict(run)}
        with self._log_path.open("a", encoding="utf-8") as fp:
            fp.write(json.dumps(entry, ensure_ascii=False) + "\n")
