from __future__ import annotations

from .prompt_builder import PromptBuilder


def main() -> None:
    builder = (
        PromptBuilder()
        .add_section("Instructions", "Respond concisely.")
        .add_section("Context", "You are customizing a GPT prompt builder demo.")
        .add_examples({"Hello": "Hi there!"})
    )
    print(builder.render())


if __name__ == "__main__":
    main()
