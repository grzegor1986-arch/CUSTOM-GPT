# CUSTOM-GPT

A lightweight Python package for composing reusable prompt snippets when experimenting with GPT-style assistants.

## Features
- Chainable `PromptBuilder` for titled and untitled prompt sections.
- `add_text_section` helper for converting multi-line text blocks into clean prompt lines.
- `add_examples` helper that accepts either a mapping or a list of `(input, output)` tuples.
- Read-only `sections` property and `clear()` helper for easier prompt lifecycle management.

## Quick start
1. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```
2. Install the package in editable mode:
   ```bash
   pip install -e .
   ```
3. Run the demo CLI:
   ```bash
   python -m custom_gpt
   ```

## Development setup
Install development tools and run checks:

```bash
pip install -e .[dev]
python -m pytest
ruff check .
ruff format --check .
```
