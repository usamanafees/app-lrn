"""Extract requirements from first manifest doc using Claude or Gemini."""

import argparse
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.schemas import Requirement  # noqa: E402
from app.services.llm_extract import Provider, extract_requirements_from_text  # noqa: E402

load_dotenv(ROOT / ".env")

MANIFEST_PATH = ROOT / "data" / "raw" / "manifest.jsonl"


def main() -> None:
    parser = argparse.ArgumentParser(description="Extract requirements with Claude or Gemini")
    parser.add_argument(
        "--provider",
        choices=["claude", "gemini"],
        default="claude",
        help="LLM provider (default: claude)",
    )
    parser.add_argument(
        "--lines",
        type=int,
        default=30,
        help="Number of document lines to send (default: 30)",
    )
    args = parser.parse_args()
    provider: Provider = args.provider

    with open(MANIFEST_PATH, encoding="utf-8") as f:
        first_line = next(line for line in f if line.strip())
    entry = json.loads(first_line)

    path = ROOT / entry["path"]
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    text = "\n".join(path.read_text(encoding="utf-8").splitlines()[: args.lines])
    raw_items = extract_requirements_from_text(text, provider=provider)
    validated = [Requirement(**item) for item in raw_items]

    print(f"provider: {provider}")
    print(f"document: {entry.get('doc_id') or entry.get('document_id', path.name)}")
    print(f"extracted: {len(validated)}")


if __name__ == "__main__":
    main()
