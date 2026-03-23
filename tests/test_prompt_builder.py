import pytest

from custom_gpt import MissingTemplateVariableError, PromptBuilder, PromptSection


def test_add_section_and_render():
    builder = PromptBuilder().add_section("Instructions", "Be helpful.")
    assert builder.render() == "Instructions:\nBe helpful."


def test_add_examples_from_mapping():
    builder = PromptBuilder().add_examples({"Hi": "Hello!"})
    result = builder.render()
    assert "Example:\nInput: Hi\nOutput: Hello!" in result


def test_add_examples_from_sequence_pairs():
    builder = PromptBuilder().add_examples([("A", "B"), ("C", "D")])

    assert builder.render() == (
        "Example:\nInput: A\nOutput: B\n\nExample:\nInput: C\nOutput: D"
    )


def test_extend_sections():
    sections = [PromptSection("Context", ["Test context"])]
    builder = PromptBuilder().extend(sections)
    assert "Context:\nTest context" in builder.render()


def test_add_text_section_splits_multiline_block():
    builder = PromptBuilder().add_text_section(
        "Context", "First line\nSecond line\n\nThird line"
    )
    rendered = builder.render().splitlines()

    assert rendered[0] == "Context:"
    assert rendered[1:] == ["First line", "Second line", "Third line"]


def test_render_separates_sections_with_blank_line():
    builder = PromptBuilder().add_section("One", "First").add_section("Two", "Second")

    assert builder.render() == "One:\nFirst\n\nTwo:\nSecond"


def test_render_skips_whitespace_only_sections():
    builder = PromptBuilder().add_section("A", "   ").add_section("B", "value")

    assert builder.render() == "B:\nvalue"


def test_render_trims_header_whitespace():
    builder = PromptBuilder().add_section("  Instructions  ", "Do work")

    assert builder.render() == "Instructions:\nDo work"


def test_sections_property_is_read_only_tuple():
    builder = PromptBuilder().add_section("One", "Line")

    assert isinstance(builder.sections, tuple)
    assert builder.sections[0].header == "One"


def test_clear_removes_all_sections():
    builder = PromptBuilder().add_section("One", "Line").clear()

    assert builder.render() == ""
    assert builder.sections == ()


def test_render_template_replaces_variables():
    builder = PromptBuilder().add_section("System", "You are {assistant_name}.")

    assert (
        builder.render_template({"assistant_name": "Codex"})
        == "System:\nYou are Codex."
    )


def test_render_template_raises_for_missing_variable_when_strict():
    builder = PromptBuilder().add_section("System", "You are {assistant_name}.")

    with pytest.raises(MissingTemplateVariableError):
        builder.render_template({}, strict=True)


def test_render_template_keeps_missing_variable_when_not_strict():
    builder = PromptBuilder().add_section("System", "You are {assistant_name}.")

    assert (
        builder.render_template({}, strict=False)
        == "System:\nYou are {assistant_name}."
    )
