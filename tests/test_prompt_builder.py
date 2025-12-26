from custom_gpt import PromptBuilder, PromptSection


def test_add_section_and_render():
    builder = PromptBuilder().add_section("Instructions", "Be helpful.")
    assert builder.render() == "Instructions:\nBe helpful."


def test_add_examples():
    builder = PromptBuilder().add_examples({"Hi": "Hello!"})
    result = builder.render()
    assert "Example:\nInput: Hi\nOutput: Hello!" in result


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
    builder = (
        PromptBuilder()
        .add_section("One", "First")
        .add_section("Two", "Second")
    )

    assert builder.render() == "One:\nFirst\n\nTwo:\nSecond"
