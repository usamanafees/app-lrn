import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
import json
from schemas import Requirement

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY_NEW")

if not api_key:
    raise ValueError("GEMINI_API_KEY_NEW not found in .env")

client = genai.Client(api_key=api_key)

# path = Path("data/raw/documents/un_ece_r152_pedestrian_detection.txt")

manifest_path = Path("data/raw/manifest.jsonl")
with open(manifest_path, encoding="utf-8") as f:
    first_line = next(line for line in f if line.strip())
entry = json.loads(first_line)

path = Path("data/raw") / entry["file_path"]

text = "\n".join(path.read_text(encoding="utf-8").splitlines()[:30])

prompt = f"""
Extract regulatory requirements from the text below.
Return ONLY valid JSON: a list of objects with keys: id, section, text.

TEXT:
{text}
"""

result = client.interactions.create(
    model="gemini-3.6-flash",
    input=prompt,
)
regulations = json.loads(result.output_text.strip())

validated_list = [Requirement(**item) for item in regulations]

expected = json.loads(Path("data/expected/requirements.json").read_text(encoding="utf-8"))
doc_id = entry["document_id"]
expected_for_doc = [r for r in expected if r["document_id"] == doc_id]

print("extracted:", len(validated_list))
print("expected:", len(expected_for_doc))
# print(validated_list)
