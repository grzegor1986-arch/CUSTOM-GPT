# CUSTOM-GPT

A minimal Python package for composing reusable prompt snippets when experimenting with GPT-style assistants.

## Features
- Chainable `PromptBuilder` for adding titled or untitled prompt sections (via
  `add_section` or `add_text_section` for multi-line blocks).
- Convenience helper for appending example input/output pairs.
- Reusable `PromptSection` objects that can be shared across builders.

## Getting started
1. Create a virtual environment and install dependencies:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -e .
   ```
2. Run the demo CLI to see a rendered prompt:
   ```bash
   python -m custom_gpt
   ```
3. Run tests:
   ```bash
   python -m pytest
   ```
