import sys
import os
import json
import datetime
import subprocess
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from peft import PeftModel

# === CONFIG ===
base_model = "microsoft/phi-2"
adapter_path = "./phi2-lora-adapter"

tokenizer = AutoTokenizer.from_pretrained(adapter_path)
base = AutoModelForCausalLM.from_pretrained(base_model, device_map="auto", torch_dtype=torch.float16)
model = PeftModel.from_pretrained(base, adapter_path, is_trainable=False)

# === Get prompt ===
prompt = sys.argv[1] if len(sys.argv) > 1 else input("Enter instruction:\n")

# === Format for inference ===
formatted = f"### Instruction:\n{prompt}\n\n### Response:\n"
inputs = tokenizer(formatted, return_tensors="pt").to(model.device)

# === Generate output ===
with torch.no_grad():
    outputs = model.generate(**inputs, max_new_tokens=100)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)

# === Extract response only
if "### Response:" in response:
    response = response.split("### Response:")[-1].strip()

print("\n📋 Plan Generated:\n" + response)

# === Dry-run first line if shell command
first_line = response.strip().split('\n')[0]

def is_shell_command(text):
    return any(text.startswith(cmd) for cmd in ["git ", "tar ", "grep ", "find ", "python ", "./", "ls ", "cd ", "mkdir ", "echo ", "rm ", "curl ", "wget ", "pip ", "bash ", "source "])

if is_shell_command(first_line):
    print("\n🧪 Dry-run:")
    subprocess.run(f"echo {first_line}", shell=True)

# === Save logs
log = {
    "timestamp": datetime.datetime.now().isoformat(),
    "prompt": prompt,
    "response": response,
    "dry_run_command": first_line if is_shell_command(first_line) else None
}

os.makedirs("logs", exist_ok=True)
with open("logs/trace.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(log) + "\n")
