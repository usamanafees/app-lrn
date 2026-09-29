import json
from pathlib import Path

manifest_path = Path("data/raw/manifest.jsonl")

with open(manifest_path, encoding="utf-8") as f:
    for line in f:
        if line.strip():
            entry = json.loads(line)
            print(entry)
            break