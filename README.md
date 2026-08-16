# JankAI

A small Python collection with two example CLI apps and a tiny utility:
- A simple OpenRouter/OpenAI-backed chatbot CLI (main.py).
- A minimal infix expression calculator packaged as `calculator`.
- A small file-inspection utility in `functions/`.

Quick, focused, and easy to extend for demos or learning how to wire an LLM client and small CLI tools together.

## Stack
- Language(s): Python 3.14
- Runtime: CPython + stdlib CLIs
- Notable libraries:
  - openai (openrouter usage via OpenAI client)
  - python-dotenv (load .env environment variables)

## Repository layout
```
README.md                 - this file
pyproject.toml            - project metadata (name: jankai, python >=3.14)
main.py                   - chatbot CLI using OpenRouter / OpenAI client
pyproject.toml
uv.lock                   - lock file produced by tooling
test_get_files_info.py    - small script that demonstrates functions/get_files_info
functions/                - utility functions
  get_files_info.py       - list files and metadata in a directory (safe path check)
calculator/               - small calculator CLI package
  main.py                 - CLI entry for calculator
  pkg/
    calculator.py         - Calculator class: infix evaluator with + - * /
    render.py             - JSON formatter for results
```

How it fits together: `main.py` is a standalone chatbot CLI that reads an API key from the environment and calls the OpenAI-compatible client configured for openrouter.ai. The `calculator` directory is a separate CLI program that uses `calculator.pkg` modules to evaluate expressions and print JSON-formatted results. The `functions` module contains a small utility for listing files with basic safety checks.

## Requirements
- Python >= 3.14
- An OpenRouter API key for the chatbot functionality (set in environment)

Dependencies are declared in pyproject.toml:
- openai==2.44.0
- python-dotenv==1.1.0

## Installation (dev)
Clone the repo and install in editable mode:
```bash
git clone https://github.com/Shaurya489/JankAI.git
cd JankAI
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -e .
```

## Configuration
Create a `.env` file in the repo root or export the environment variable directly:

.env:
```
OPENROUTER_API_KEY=your_api_key_here
```

Or export in your shell:
```bash
export OPENROUTER_API_KEY="your_api_key_here"
```

## Usage

Chatbot CLI (OpenRouter/OpenAI client)
```bash
# basic usage
python main.py "Give me a short joke"

# with verbose output (prints token usage if available)
python main.py "Summarize the plot of The Little Prince" --verbose
```
Output: the script prints the LLM response to stdout. The client is configured to use `base_url="https://openrouter.ai/api/v1"` and model `"openrouter/free"` by default.

Calculator CLI
```bash
# run the calculator CLI (expression tokens must be space-separated)
python calculator/main.py "3 + 5 * 2"

# example output (JSON)
# {"expression": "3 + 5 * 2", "result": 13}
```
Notes: The calculator expects expressions tokenized by spaces (e.g., `3 + 5 * 2`). The evaluator supports +, -, *, / with precedence.

Functions utility
- `functions/get_files_info.py` contains `get_files_info(working_directory, directory=".")` which returns file metadata for a safe, relative directory inside a given working directory.
- A small demo script `test_get_files_info.py` exists to exercise that function.

## Examples
Chatbot:
```bash
python main.py "Write a 3-line haiku about autumn"
```

Calculator:
```bash
python calculator/main.py "10 / 2 - 3"
# prints JSON: {"expression": "10 / 2 - 3", "result": 2}
```

## Development notes
- Project metadata lives in `pyproject.toml`.
- The calculator implementation (`calculator/pkg/calculator.py`) evaluates infix expressions using two stacks (values and operators) and applies precedence rules.
- The chatbot (`main.py`) uses environment configuration for the API key; it raises if the API key is missing.

## Running tests / checks
There are no formal test harnesses configured in pyproject. For manual checks:
- Try the calculator CLI with a few expressions (see examples above).
- Try the demo script for `functions.get_files_info`, or import `get_files_info` into a REPL and call it.

## Contributing
Contributions are welcome. Suggested starting points:
- Add argument parsing to the calculator to accept both spaced and non-spaced expressions.
- Improve input validation and add unit tests (pytest).
- Add error handling and retry/backoff for the chatbot client.

## Open questions / next work
- Add a proper test suite (pytest) and CI.
- Provide better packaging / console_scripts entry points for the CLIs.
- Decide and add a license file if this will be published.

## Contact
Maintainer: Shaurya489 (GitHub)
