from __future__ import annotations

import json
from dataclasses import asdict, dataclass
from pathlib import Path

from .models import AuditEvent


@dataclass
class AuditLogger:
    path: Path

    def log(self, event: AuditEvent) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = asdict(event)
        payload["timestamp"] = event.timestamp.isoformat()
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload, ensure_ascii=False) + "\n")
