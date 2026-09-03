# JankAI

An experimental AI agent framework that enables an LLM to inspect, modify, and run code files dynamically. Built with OpenRouter and OpenAI's client library, JankAI demonstrates how to create a programmable agent that can work autonomously on a project directory.

## Overview

JankAI is a toy AI agent (inspired by Claude Code, Cursor AI) that gives an LLM safe, sandboxed access to file operations and code execution. The agent can read files, write new code, run Python scripts, and inspect directory structures—all within a controlled working directory. This enables interactive code generation, testing, and iteration in real time.

### Stack

- **Language:** Python 3.14+
- **LLM Integration:** OpenAI client (OpenRouter via `openai==2.44.0`)
- **Notable Libraries:**
  - `openai` (2.44.0) – OpenAI-compatible API client
  - `python-dotenv` (1.1.0) – Environment configuration
  - `subprocess` – Safe Python code execution

## How It's Organized

```
JankAI/
├── main.py                      Main agent loop with LLM integration
├── config.py                    Configuration (MAX_CHARS for file reads)
├── prompts.py                   System prompt for agent behavior
├── call_function.py             Tool dispatcher and schema definitions
│
├── functions/                   Tool implementations (agent capabilities)
│   ├── get_files_info.py        List directory contents with metadata
│   ├── get_file_content.py      Read file contents (with truncation)
│   ├── run_python_file.py       Execute Python scripts safely
│   └── write_file.py            Write/create files
│
├── calculator/                  Example project the agent works on
│   ├── main.py                  Calculator CLI entry point
│   ├── tests.py                 Test suite
│   ├── README.md                Calculator documentation
│   └── pkg/
│       ├── calculator.py        Infix expression evaluator (+ - * /)
│       └── render.py            JSON output formatter
│
├── pyproject.toml               Project metadata (name: jankai, Python >=3.14)
└── [test files]                 Demo scripts for individual tools
```

### How It Fits Together

1. **Agent Loop** (`main.py`):
   - Reads user prompt from CLI
   - Sends prompt + system instructions to OpenRouter's free model
   - Receives tool calls (function names + arguments) from the LLM

2. **Tool Dispatch** (`call_function.py`):
   - Parses LLM function calls
   - Routes to appropriate tool implementation
   - Always passes `working_directory="./calculator"` for sandboxing

3. **Tool Set** (`functions/`):
   - **get_files_info**: Lists files with size and directory status
   - **get_file_content**: Reads up to 10,000 characters per file
   - **write_file**: Creates or overwrites files (with path validation)
   - **run_python_file**: Executes Python scripts with optional arguments (30s timeout)

4. **Safety**: All file operations validate that target paths stay within the working directory. Relative paths are used throughout.

5. **Iteration**: The agent runs up to 20 tool call cycles, adding results to the message history. When the LLM stops calling tools, it outputs a final response.

## Requirements

- **Python** ≥ 3.14
- **OpenRouter API Key** – Get one free at [openrouter.ai](https://openrouter.ai)

Dependencies (in `pyproject.toml`):
- `openai==2.44.0`
- `python-dotenv==1.1.0`

## Installation

### 1. Clone & Setup

```bash
git clone https://github.com/Shaurya489/JankAI.git
cd JankAI
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -e .
```

### 2. Configure API Key

Create a `.env` file in the repo root:

```env
OPENROUTER_API_KEY=your_key_here
```

Or export it:

```bash
export OPENROUTER_API_KEY="your_key_here"
```

## Usage

### Agent Mode (Main)

Give the agent a task. It will read, write, and execute files in `./calculator`:

```bash
# Ask the agent to modify or analyze the calculator
python main.py "Add a modulo operator to the calculator"

# Verbose output: shows function calls and their results
python main.py "Write tests for the calculator" --verbose
```

The agent:
1. Reads relevant files with `get_files_info` and `get_file_content`
2. Writes changes with `write_file`
3. Runs `run_python_file` to test its changes
4. Reports back with a final response

### Calculator CLI (Standalone)

Run the calculator directly:

```bash
python calculator/main.py "3 + 5 * 2"
# Output: {"expression": "3 + 5 * 2", "result": 13}

python calculator/main.py "10 / 2 - 3"
# Output: {"expression": "10 / 2 - 3", "result": 2}
```

### Test Individual Tools

Each tool can be tested independently:

```bash
# Test file listing
python test_get_files_info.py

# Test file reading
python test_get_file_content.py

# Test Python execution
python test_run_python_file.py

# Test file writing
python test_write_file.py
```

## How the Calculator Works

The calculator evaluates infix expressions with proper operator precedence:

- **Operators**: `+`, `-`, `*`, `/`
- **Precedence**: `*` and `/` before `+` and `-`
- **Implementation**: Two-stack algorithm (values + operators) in `calculator/pkg/calculator.py`

Example:

```python
from calculator.pkg.calculator import Calculator

calc = Calculator()
result = calc.evaluate("3 + 5 * 2")  # 13 (not 16)
```

## Key Design Decisions

1. **Sandboxing**: Working directory is fixed to `./calculator`. All paths are validated to prevent escape.
2. **Character Limit**: File reads are capped at 10,000 characters (`config.MAX_CHARS`) to avoid overwhelming the LLM.
3. **Tool Schemas**: Each tool exports an OpenAI-compatible schema for function calling.
4. **System Prompt**: Guides the agent to use tools efficiently and avoid redundant calls (`prompts.py`).
5. **Error Handling**: Tools return string error messages, not exceptions, so the agent can respond gracefully.

## Example Agent Interaction

```
User: "Fix the calculator tests"

Agent:
  1. Calls get_files_info(".") → lists calculator/ files
  2. Calls get_file_content("tests.py") → reads test suite
  3. Analyzes the issue
  4. Calls write_file("tests.py", ...) → fixes the tests
  5. Calls run_python_file("tests.py") → runs tests to verify
  6. Returns: "✓ All tests pass! Fixed [specific issues]"
```

## Development

### Testing

Run calculator tests manually:

```bash
cd calculator
python tests.py
```

Or run via the agent:

```bash
python main.py "Run the tests and tell me if they pass"
```

### Extending the Agent

To add a new tool:

1. Create `functions/my_tool.py` with a function and `schema_my_tool` dict
2. Import in `call_function.py` and add to `function_map` and `available_functions`
3. Reference in `prompts.py` system message

### Ideas for Contribution

- Add error recovery and retry logic for API calls
- Implement tool call caching to avoid duplicate reads
- Add more tools: file deletion, directory creation, git operations
- Create a web UI for the agent
- Add persistent memory of previous interactions
- Optimize token usage (context compression, chunking)

## Limitations & Next Steps

- **No file deletion**: Safety measure; add with caution
- **No git integration**: Manual version control currently
- **No persistent state**: Each run starts fresh
- **Model selection**: Currently uses OpenRouter's free model; consider upgrading for complex tasks
- **No formal test harness**: Use pytest to formalize tests

## Contributing

Issues and pull requests welcome! Areas of interest:

- Better prompt engineering for complex tasks
- Additional tool implementations
- Performance optimizations
- UI/UX improvements
- Documentation and examples

## License

See LICENSE file (to be determined).

## Contact

**Maintainer:** [@Shaurya489](https://github.com/Shaurya489)

Questions? Open an issue on GitHub.
