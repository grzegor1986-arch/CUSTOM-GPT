from __future__ import annotations

from typing import Any

from connectors.adapters import HTTPOrSDKAdapter
from connectors.base import Connector


class SlackConnector(Connector):
    name = "slack"
    capability_tags = {"messaging", "knowledge"}

    def __init__(self, api_base: str = "https://slack.com/api") -> None:
        self.adapter = HTTPOrSDKAdapter(mode="http", target=api_base)

    def describe_tools(self) -> list[dict[str, Any]]:
        return [
            {"name": "post_message", "description": "Send a channel message"},
            {"name": "search_messages", "description": "Search message history"},
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
            "details": {"transport": "http", "target": self.adapter.target},
        }
