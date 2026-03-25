from __future__ import annotations

from .registry import ConnectorRegistry


def route_connectors_by_capability(
    registry: ConnectorRegistry,
    required_tags: set[str],
) -> list[str]:
    """Return connector names that contain all requested capability tags."""
    return [
        connector.name
        for connector in registry.connectors.values()
        if required_tags.issubset(connector.capability_tags)
    ]
