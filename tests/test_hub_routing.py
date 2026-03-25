from __future__ import annotations

from connectors.hub import route_connectors_by_capability
from connectors.registry import load_registry


def test_route_connectors_by_capability() -> None:
    registry = load_registry()

    assert route_connectors_by_capability(registry, {"code"}) == ["github"]
    assert sorted(route_connectors_by_capability(registry, {"knowledge"})) == [
        "github",
        "postgres",
        "slack",
    ]
    assert route_connectors_by_capability(registry, {"messaging", "knowledge"}) == ["slack"]
