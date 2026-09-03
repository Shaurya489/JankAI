# JankAI 

JankAI is a lightweight, interactive CLI-based AI coding assistant powered by OpenRouter. It allows you to debug, analyze, and modify your codebase using natural language directly from your terminal.

---

## Features

- **Interactive Onboarding:** Automatically prompts you for your OpenRouter API key on the first run and stores it securely in your home directory.
- **File & Directory Management:** Seamlessly reads, writes, and modifies source files in any target directory.
- **Multi-Language Support:** Works with Python, C++, and various other programming languages.
- **Verbose Mode:** Trace every tool call, file read, and LLM decision in real-time.

---

## Installation

You can install JankAI directly from GitHub using `pipx` (recommended for CLI tools):

```bash
pipx install git+https://github.com/Shaurya489/JankAI.git
```

Or for local development:

```bash
git clone https://github.com/Shaurya489/JankAI.git
cd JankAI
pip install -e .
```

---

## Quick Start

1. Run the CLI tool with a natural language instruction pointing to your target folder:
   ```bash
   jankai "fix the bug in test1.py" --dir ./testFolder --verbose
   ```

2. **First-Time Setup:** If you haven't set an environment variable, JankAI will prompt you securely for your OpenRouter API key:
   ```text
   [JankAI Setup] OpenRouter API key not found.
   Get a free key at: https://openrouter.ai/keys

   Enter your OpenRouter API key: 
   ```
   *(Your key is saved securely to `~/.jankai_key` so you only have to enter it once).*

---

## Command Line Options

- `user_prompt`: The task or question you want the AI agent to solve (required).
- `--dir`: Target working directory (default: current directory `.`).
- `--verbose`: Enable detailed logging of function and tool calls.