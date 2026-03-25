from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any


class Connector(ABC):
    """Common connector contract for all external sources."""

    name: str
    capability_tags: set[str]

    @abstractmethod
    def describe_tools(self) -> list[dict[str, Any]]:
        """Return tool metadata for hub routing and discovery."""

    @abstractmethod
    def execute(self, tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
        """Execute a tool and return normalized payload."""

    @abstractmethod
    def health(self) -> dict[str, Any]:
        """Return connector health details."""
