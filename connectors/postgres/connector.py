from __future__ import annotations

from typing import Any

from connectors.adapters import HTTPOrSDKAdapter
from connectors.base import Connector


class PostgresConnector(Connector):
    name = "postgres"
    capability_tags = {"knowledge", "tickets"}

    def __init__(self, dsn: str = "postgresql://localhost:5432/app") -> None:
        self.adapter = HTTPOrSDKAdapter(mode="sdk", target=dsn)

    def describe_tools(self) -> list[dict[str, Any]]:
        return [
            {"name": "run_query", "description": "Run SQL query"},
            {"name": "describe_table", "description": "Describe table schema"},
        ]

    def execute(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        response = self.adapter.run(tool_name=tool_name, args=args)
        return {
            "status": response["status"],
            "tool": tool_name,
            "result": response["result"],
            "meta": {"transport": response["transport"], "target": response["target"]},
        }

    def health(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "connector": self.name,
            "capability_tags": sorted(self.capability_tags),
            "details": {"transport": "sdk", "target": self.adapter.target},
        }
