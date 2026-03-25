from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class MCPServerAdapter:
    """Adapter that mimics dispatch to an MCP server-backed tool."""

    server_name: str

    def run(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        # In a production setup this would open an MCP transport and invoke the tool.
        return {
            "transport": "mcp",
            "server": self.server_name,
            "tool": tool_name,
            "args": args,
            "status": "ok",
            "result": {"echo": args},
        }


@dataclass(slots=True)
class HTTPOrSDKAdapter:
    """Adapter for systems that are not MCP-compatible."""

    mode: str
    target: str

    def run(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        if self.mode not in {"http", "sdk"}:
            raise ValueError(f"Unsupported mode: {self.mode}")

        return {
            "transport": self.mode,
            "target": self.target,
            "tool": tool_name,
            "args": args,
            "status": "ok",
            "result": {"echo": args},
        }
