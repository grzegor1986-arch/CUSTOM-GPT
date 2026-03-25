from __future__ import annotations

from typing import Any

from connectors.adapters import MCPServerAdapter
from connectors.base import Connector


class GithubConnector(Connector):
    name = "github"
    capability_tags = {"code", "tickets", "knowledge"}

    def __init__(self, server_name: str = "github-mcp") -> None:
        self.adapter = MCPServerAdapter(server_name=server_name)

    def describe_tools(self) -> list[dict[str, Any]]:
        return [
            {"name": "list_pull_requests", "description": "List pull requests"},
            {"name": "get_issue", "description": "Fetch issue details"},
        ]

    def execute(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        response = self.adapter.run(tool_name=tool_name, args=args)
        return {
            "status": response["status"],
            "tool": tool_name,
            "result": response["result"],
            "meta": {"transport": response["transport"], "server": response["server"]},
        }

    def health(self) -> dict[str, Any]:
        return {
            "status": "ok",
            "connector": self.name,
            "capability_tags": sorted(self.capability_tags),
            "details": {"transport": "mcp", "server": self.adapter.server_name},
        }
