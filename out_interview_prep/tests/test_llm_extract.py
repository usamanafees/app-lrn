from unittest.mock import MagicMock, patch

import pytest

from app.services.llm_extract import _parse_json_list, extract_requirements_from_text


def test_parse_json_list_strips_markdown_fence() -> None:
    raw = '```json\n[{"id": "REQ-001", "section": "1", "text": "Foo."}]\n```'
    result = _parse_json_list(raw)
    assert result[0]["id"] == "REQ-001"


@patch("app.services.llm_extract.extract_with_claude")
def test_extract_requirements_claude(mock_claude: MagicMock) -> None:
    mock_claude.return_value = [{"id": "REQ-001", "section": "1.0", "text": "Shall do X."}]
    result = extract_requirements_from_text("sample text", provider="claude")
    assert len(result) == 1
    mock_claude.assert_called_once()


@patch("app.services.llm_extract.extract_with_gemini")
def test_extract_requirements_gemini(mock_gemini: MagicMock) -> None:
    mock_gemini.return_value = [{"id": "REQ-002", "section": "2.0", "text": "Shall do Y."}]
    result = extract_requirements_from_text("sample text", provider="gemini")
    assert len(result) == 1
    mock_gemini.assert_called_once()
