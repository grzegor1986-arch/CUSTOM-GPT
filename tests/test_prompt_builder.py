from custom_gpt import PromptBuilder, PromptSection


def test_add_section_and_render():
    builder = PromptBuilder().add_section("Instructions", "Be helpful.")
    assert builder.render() == "Instructions:\nBe helpful."


def test_add_examples():
    builder = PromptBuilder().add_examples({"Hi": "Hello!"})
    result = builder.render()
    assert "Example:\nInput: Hi\nOutput: Hello!" in result


def test_extend_sections():
    sections = [PromptSection("Context", ["Test context"]) ]
    builder = PromptBuilder().extend(sections)
    assert "Context:\nTest context" in builder.render()
