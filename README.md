# CUSTOM-GPT

A minimal Python package for composing reusable prompt snippets when experimenting with GPT-style assistants.

## Features
- Chainable `PromptBuilder` for adding titled or untitled prompt sections.
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
A lightweight workspace for experimenting with custom GPT behaviors and prompts. This repository currently contains scaffolding for future automation and serves as a starting point for small utilities or notebooks.

## Getting started
1. Ensure you have Python 3.11 or later installed.
2. Create and activate a virtual environment (e.g., `python -m venv .venv && source .venv/bin/activate`).
3. Install any project dependencies as they are added.

## Development
- Commit changes in small, reviewable increments.
- Keep configuration files under version control and avoid committing secrets.
- Use `.gitignore` to keep transient artifacts out of the repository.

## Contributing
Issues and pull requests are welcome as the project grows. Please include clear descriptions of any changes or ideas for new functionality.
