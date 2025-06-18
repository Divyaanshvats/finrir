# FINRIR SECURITY

# AI/ML Internship Technical Task – CLI Agent for Command-Line Instructions

## Overview

This project demonstrates a complete mini end-to-end AI assistant that interprets natural language command-line instructions and responds with shell-style commands and plans. It is built for the technical task set by Fenrir Security Private Limited, strictly following all guidelines outlined in the official PDF.

---

## Contents

- `data/questions.json` – 150+ real-world command-line Q&A pairs collected from Stack Overflow using the Stack Exchange API (not LLM-generated).
- `phi2-lora-adapter/` – LoRA adapter weights and tokenizer files fine-tuned on the above dataset.
- `training.ipynb` – Google Colab notebook containing all fine-tuning steps using QLoRA and PEFT.
- `agent.py` – The CLI agent script. Takes a natural language prompt and generates a step-by-step plan. If the first line is a shell command, it is echoed (dry-run). Every interaction is logged in `logs/trace.jsonl`.
- `eval_static.md` – Comparison between base and fine-tuned model outputs on 5 test prompts + 2 edge cases.
- `eval_dynamic.md` – Actual CLI agent outputs and dry-run evaluation with 0–2 score per prompt.
- `report.md` – One-page summary including training details, evaluation metrics, and two improvement ideas.
- `logs/trace.jsonl` – Automatically generated log file from running `agent.py`.
- `demo.mp4` – A short video demonstration of the agent in action (optional but included).

---

## Requirements

Ensure Python 3.8+ is installed. Install dependencies via:

```bash
pip install -r requirements.txt





---

### 📄 `eval_static.md`

```markdown
# Static Evaluation – Base vs Fine-Tuned Model Outputs

## Prompt 1: Create a new Git branch and switch to it.
❌ No CLI output
**Score:** 0

## Prompt 2: Compress the folder reports into reports.tar.gz
Python code block for `tarfile` module
**Score:** 1

## Prompt 3: List all Python files
❌ No response
**Score:** 0

## Prompt 4: Set up virtualenv and install requests
Returned `import requests` code
**Score:** 0

## Prompt 5: Fetch top 10 lines from output.log
Incomplete Python snippet
**Score:** 1

## Prompt 6: Find 'error' in `.log` files
Python logic using `glob` and `open()`
**Score:** 1

## Prompt 7: Delete `.tmp` files with confirmation
Returns: `rm -rf *.tmp`
**Score:** 1

**Total Score:** 5 / 14

