"""Tools for composing simple multi-part prompts."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass, field


@dataclass
class PromptSection:
    """Represents one section of a prompt.

    Attributes:
        header: Optional title shown before the content.
        body: The raw lines that make up this section.
    """

    header: str | None
    body: list[str] = field(default_factory=list)

    def render(self) -> str:
        """Return the section as a single formatted string.

        Empty and whitespace-only body lines are discarded so sections render
        cleanly and do not introduce accidental blank lines. A header is only
        shown when it contains visible text.
        """

        content_lines = [line.rstrip() for line in self.body if line.strip()]
        if not content_lines:
            return ""

        content = "\n".join(content_lines)
        normalized_header = self.header.strip() if self.header else ""
        if normalized_header:
            return f"{normalized_header}:\n{content}"
        return content


class PromptBuilder:
    """Utility for assembling reproducible prompts.

    The builder keeps ordered sections to make it easier to reuse common
    components, like instructions and examples, across different calls.
    """

    def __init__(self) -> None:
        self._sections: list[PromptSection] = []

    @property
    def sections(self) -> tuple[PromptSection, ...]:
        """Return a read-only view of currently configured sections."""

        return tuple(self._sections)

    def add_section(self, header: str | None, *lines: str) -> PromptBuilder:
        """Add a section to the prompt.

        Args:
            header: Optional title for the section (``None`` for no title).
            *lines: Each line of content to append to the section.

        Returns:
            The builder instance to allow chaining.
        """

        self._sections.append(PromptSection(header, [line.rstrip() for line in lines]))
        return self

    def add_text_section(self, header: str | None, text: str) -> PromptBuilder:
        """Add a section from a single text block.

        Args:
            header: Optional title for the section (``None`` for no title).
            text: Text block that will be split on newlines and trimmed.
        """

        lines = [line.strip() for line in text.strip().splitlines() if line.strip()]
        return self.add_section(header, *lines)

    def add_examples(
        self, examples: Mapping[str, str] | Sequence[tuple[str, str]]
    ) -> PromptBuilder:
        """Add examples from key/value pairs of input and output strings."""

        iterable: Iterable[tuple[str, str]]
        if isinstance(examples, Mapping):
            iterable = examples.items()
        else:
            iterable = examples

        for input_text, output_text in iterable:
            self.add_section(
                "Example", f"Input: {input_text}", f"Output: {output_text}"
            )
        return self

    def extend(self, sections: Iterable[PromptSection]) -> PromptBuilder:
        """Append pre-built sections to the prompt."""

        self._sections.extend(sections)
        return self

    def clear(self) -> PromptBuilder:
        """Remove all configured sections."""

        self._sections.clear()
        return self

    def render(self) -> str:
        """Return the final prompt string, skipping empty sections."""

        rendered_sections = []
        for section in self._sections:
            rendered = section.render()
            if rendered:
                rendered_sections.append(rendered)

        return "\n\n".join(rendered_sections)


__all__ = ["PromptBuilder", "PromptSection"]
