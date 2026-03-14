# AI-Agent
# AI Agent in Python

A toy agentic code editor built as part of the [Boot.dev "Build an AI Agent" course](https://www.boot.dev/courses/build-ai-agent-python). This project recreates the core mechanics of tools like Claude Code or Cursor's Agent Mode using the Google Gemini API.

## What It Does

The agent accepts a natural language instruction, then autonomously calls tools in a loop to read files, write code, and run Python until the task is complete.

```
> uv run main.py "fix my calculator app, it's not starting correctly"
# Calling function: get_files_info
# Calling function: get_file_content
# Calling function: write_file
# Calling function: run_python_file
# Final response: The calculator app is now working correctly.
```

## Prerequisites

- Python 3.10+
- [`uv`](https://docs.astral.sh/uv/getting-started/installation/) package manager
- A Unix-like shell (bash or zsh)
- A Google Gemini API key (a paid account is recommended — free tier rate limits are very restrictive as of late 2025)

## Setup

1. **Clone the repo**

   ```bash
   git clone <your-repo-url>
   cd <repo-name>
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Set your API key**

   ```bash
   export GEMINI_API_KEY="your-key-here"
   ```

## Usage

Pass a task as a command-line argument:

```bash
uv run main.py "describe what this project does"
uv run main.py "find and fix any bugs in the calculator module"
uv run main.py "add error handling to main.py"
```

The agent will print each function call it makes before giving a final response.

## How It Works

The agent is built on two key concepts:

**Function calling** — the LLM is given a set of tools it can invoke (e.g. `get_files_info`, `get_file_content`, `write_file`, `run_python_file`). Instead of answering directly, it decides which tool to call and with what arguments.

**The agentic loop** — after each tool call, the result is fed back to the model. The loop continues until the model produces a final text response rather than another tool call.

```
User prompt
    │
    ▼
┌─────────────┐
│  Gemini LLM │◄──────────────────┐
└──────┬──────┘                   │
       │ tool call?               │ tool result
       ▼                          │
┌─────────────┐                   │
│  Execute    ├───────────────────┘
│  Function   │
└─────────────┘
       │ final text response
       ▼
    Output
```

## Project Structure

```
.
├── main.py          # Entry point and agentic loop
├── functions/       # Tool implementations
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── write_file.py
│   └── run_python_file.py
├── calculator/      # Sample buggy project for the agent to fix
└── pyproject.toml
```

## Learning Goals

- Understand how LLM-powered agents work under the hood
- Use the Gemini API with function/tool calling
- Build and manage a feedback loop between an LLM and real system tools
- Get comfortable with multi-directory Python project structure

## Notes on the Gemini API

Google's free tier for `gemini-2.5-flash` has significant rate limits as of late 2025. If you hit errors frequently, consider setting up a paid Google AI account — costs for this project should be well under $2.
