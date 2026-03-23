# CUSTOM-GPT

A lightweight Python package for composing reusable prompt snippets when experimenting with GPT-style assistants.

## Features
- Chainable `PromptBuilder` for titled and untitled prompt sections.
- `add_text_section` helper for converting multi-line text blocks into clean prompt lines.
- `add_examples` helper that accepts either a mapping or a list of `(input, output)` tuples.
- Read-only `sections` property and `clear()` helper for easier prompt lifecycle management.
- `render_template` support for filling variables (strict and non-strict modes).

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

## Template rendering example
```python
from custom_gpt import PromptBuilder

builder = PromptBuilder().add_section("System", "You are {assistant_name}.")
prompt = builder.render_template({"assistant_name": "Custom GPT"})
```

## Development setup
Install development tools and run checks:

```bash
pip install -e .[dev]
python -m pytest
ruff check .
ruff format --check .
```

## Next tasks (plan)
- [x] Upgrade prompt builder with template rendering.
- [x] Expand tests for strict/non-strict variable interpolation.
- [x] Add GitHub Actions CI workflow for automated checks.
- [ ] Add semantic versioning and changelog automation.
