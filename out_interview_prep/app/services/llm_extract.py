import json
import os
import re
from typing import Literal

Provider = Literal["claude", "gemini"]

EXTRACTION_PROMPT = """Extract regulatory requirements from the text below.
Return ONLY valid JSON: a list of objects with keys: id, section, text.

TEXT:
{text}
"""


def _parse_json_list(raw: str) -> list[dict]:
    text = raw.strip()
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\n?", "", text)
        text = re.sub(r"\n?```$", "", text).strip()
    data = json.loads(text)
    if not isinstance(data, list):
        raise ValueError("Model response is not a JSON list")
    return data


def extract_with_claude(prompt: str) -> list[dict]:
    from anthropic import Anthropic

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY not found in .env")

    model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
    client = Anthropic(api_key=api_key)
    message = client.messages.create(
        model=model,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    return _parse_json_list(message.content[0].text)


def extract_with_gemini(prompt: str) -> list[dict]:
    from google import genai

    api_key = os.getenv("GEMINI_API_KEY") or os.getenv("GEMINI_API_KEY_NEW")
    if not api_key:
        raise ValueError("GEMINI_API_KEY or GEMINI_API_KEY_NEW not found in .env")

    model = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
    client = genai.Client(api_key=api_key)
    result = client.interactions.create(
        model=model,
        input=prompt,
        response_mime_type="application/json",
    )
    return _parse_json_list(result.output_text)


def extract_requirements_from_text(text: str, provider: Provider = "claude") -> list[dict]:
    prompt = EXTRACTION_PROMPT.format(text=text)
    if provider == "claude":
        return extract_with_claude(prompt)
    return extract_with_gemini(prompt)
