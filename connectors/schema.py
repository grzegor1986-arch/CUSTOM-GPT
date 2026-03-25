from __future__ import annotations

from typing import Any

ALLOWED_CAPABILITY_TAGS = {"code", "tickets", "knowledge", "messaging"}

REQUEST_SCHEMA = {
    "required": {"tool_name", "args"},
    "types": {"tool_name": str, "args": dict},
}

RESPONSE_SCHEMA = {
    "required": {"status", "tool", "result"},
    "types": {"status": str, "tool": str, "result": dict},
}

HEALTH_SCHEMA = {
    "required": {"status", "connector", "capability_tags"},
    "types": {"status": str, "connector": str, "capability_tags": list},
}


def validate_shape(payload: dict[str, Any], schema: dict[str, Any]) -> None:
    missing = schema["required"] - payload.keys()
    if missing:
        raise AssertionError(f"Missing keys in payload: {sorted(missing)}")

    for key, expected_type in schema["types"].items():
        if key in payload and not isinstance(payload[key], expected_type):
            raise AssertionError(
                f"Invalid type for '{key}': expected {expected_type.__name__}, "
                f"got {type(payload[key]).__name__}"
            )
