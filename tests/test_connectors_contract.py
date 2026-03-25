from __future__ import annotations

from connectors.registry import load_registry
from connectors.schema import HEALTH_SCHEMA, REQUEST_SCHEMA, RESPONSE_SCHEMA, validate_shape


def test_registry_loads_connectors_from_config() -> None:
    registry = load_registry()

    assert set(registry.connectors.keys()) == {"github", "slack", "postgres"}


def test_each_connector_contract_request_response_and_health() -> None:
    registry = load_registry()

    for connector in registry.connectors.values():
        tools = connector.describe_tools()
        assert tools, f"Connector {connector.name} should expose at least one tool"

        request = {"tool_name": tools[0]["name"], "args": {"example": True}}
        validate_shape(request, REQUEST_SCHEMA)

        response = connector.execute(request["tool_name"], request["args"])
        validate_shape(response, RESPONSE_SCHEMA)

        health = connector.health()
        validate_shape(health, HEALTH_SCHEMA)
        assert sorted(health["capability_tags"]) == sorted(connector.capability_tags)
