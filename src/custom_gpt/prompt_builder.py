"""Tools for composing simple multi-part prompts."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Iterable, List


@dataclass
class PromptSection:
    """Represents one section of a prompt.

    Attributes:
        header: Optional title shown before the content.
        body: The raw lines that make up this section.
    """

    header: str | None
    body: List[str] = field(default_factory=list)

    def render(self) -> str:
        """Return the section as a single formatted string.

        Sections with a header are rendered as ``<header>:\n<body>`` while
        headerless sections return just the body content. Empty bodies render
        as an empty string to avoid stray newlines in the final prompt.
        """

        if not self.body:
            return ""

        content = "\n".join(self.body).strip()
        if self.header:
            return f"{self.header}:\n{content}\n"
        return f"{content}\n"


class PromptBuilder:
    """Utility for assembling reproducible prompts.

    The builder keeps ordered sections to make it easier to reuse common
    components, like instructions and examples, across different calls.
    """

    def __init__(self) -> None:
        self._sections: List[PromptSection] = []

    def add_section(self, header: str | None, *lines: str) -> "PromptBuilder":
        """Add a section to the prompt.

        Args:
            header: Optional title for the section (``None`` for no title).
            *lines: Each line of content to append to the section.

        Returns:
            The builder instance to allow chaining.
        """

        self._sections.append(PromptSection(header, list(lines)))
        return self

    def add_examples(self, examples: Dict[str, str]) -> "PromptBuilder":
        """Add examples from a mapping of input to output strings."""

        for input_text, output_text in examples.items():
            self.add_section("Example", f"Input: {input_text}", f"Output: {output_text}")
        return self

    def extend(self, sections: Iterable[PromptSection]) -> "PromptBuilder":
        """Append pre-built sections to the prompt."""

        self._sections.extend(sections)
        return self

    def render(self) -> str:
        """Return the final prompt string, skipping empty sections."""

        rendered = [section.render() for section in self._sections if section.render()]
        return "\n".join(rendered).strip()


__all__ = ["PromptBuilder", "PromptSection"]
