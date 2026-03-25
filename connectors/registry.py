from __future__ import annotations

import json
from dataclasses import dataclass, field
from importlib import import_module
from pathlib import Path
from typing import Any

from connectors.base import Connector
from connectors.schema import ALLOWED_CAPABILITY_TAGS


@dataclass
class ConnectorRegistry:
    connectors: dict[str, Connector] = field(default_factory=dict)

    def register(self, connector: Connector) -> None:
        self.connectors[connector.name] = connector

    def get(self, connector_name: str) -> Connector:
        return self.connectors[connector_name]


def _load_yaml_with_fallback(config_path: Path) -> dict[str, Any]:
    try:
        import yaml  # type: ignore

        with config_path.open("r", encoding="utf-8") as handle:
            parsed = yaml.safe_load(handle)
            if not isinstance(parsed, dict):
                raise ValueError("connectors config must be a mapping")
            return parsed
    except ModuleNotFoundError:
        # YAML 1.2 accepts JSON as a subset; we keep config parseable without PyYAML.
        raw = config_path.read_text(encoding="utf-8")
        parsed = json.loads(raw)
        if not isinstance(parsed, dict):
            raise ValueError("connectors config must be a mapping")
        return parsed


def load_registry(config_path: str = "config/connectors.yaml") -> ConnectorRegistry:
    parsed = _load_yaml_with_fallback(Path(config_path))
    connectors_config = parsed.get("connectors", [])

    registry = ConnectorRegistry()
    for config in connectors_config:
        module = import_module(config["module"])
        connector_class = getattr(module, config["class"])

        kwargs = config.get("kwargs", {})
        connector: Connector = connector_class(**kwargs)

        configured_tags = set(config.get("capability_tags", []))
        unknown_tags = configured_tags - ALLOWED_CAPABILITY_TAGS
        if unknown_tags:
            raise ValueError(
                f"Connector '{config['name']}' has unknown capability tags: {sorted(unknown_tags)}"
            )
        connector.capability_tags = configured_tags

        registry.register(connector)

    return registry
