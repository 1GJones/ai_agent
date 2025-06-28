# ai_agent
Ai_ LLM Agent
# 🤖 ai_agent — A Toy Claude Code Using Gemini API

Welcome to `ai_agent`, a CLI-based experimental project that mimics a simplified version of Anthropic's Claude Code, powered by **Google's free Gemini API**.

As long as you have access to an LLM (Large Language Model), building a (somewhat) effective custom code agent is surprisingly straightforward—and fun.

---

## 🚀 What Does the Agent Do?

The AI agent is designed to automate and interact with your codebase to solve coding tasks. Here's what it does:

1. **Accepts a natural-language coding task**  
   _Example:_
   > "strings aren't splitting in my app, pweeze fix 🥺👉🏽👈🏽"

2. **Chooses from a set of predefined functions to handle the task**, such as:
   - Scanning all files in a directory
   - Reading the contents of a specific file
   - Overwriting a file with new content
   - Executing a Python file

3. **Loops intelligently** through steps 2 until:
   - ✅ The task is complete  
   - ❌ It fails miserably (yes, that’s part of the fun)

---

## 🧠 How It Works

Under the hood, this project sends prompts to the Gemini API and uses your natural language instructions to drive decision-making about which tools to use.

### 🧰 Tools Provided to the Agent

- `list_files(directory)`
- `read_file(filepath)`
- `write_file(filepath, contents)`
- `run_python(filepath)`

You can expand or customize this toolset to suit your workflow.

---

## 🧪 Requirements

- Python 3.8+
- Access to Google's Gemini API (API key required)
- `openai` or `google-generativeai` Python SDK (depending on LLM used)

Install dependencies:

```bash
pip install -r requirements.txt
