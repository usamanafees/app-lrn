import json
from pathlib import Path

DATA_ROOT = Path(__file__).resolve().parents[2] / "data"
MANIFEST_PATH = DATA_ROOT / "raw" / "manifest.jsonl"


def read_manifest(path: Path = MANIFEST_PATH) -> list[dict]:
    entries: list[dict] = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    return entries
