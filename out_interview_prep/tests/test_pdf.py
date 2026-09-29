from pathlib import Path

import pytest

from app.services.pdf_extract import extract_with_pdfplumber

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples"


@pytest.mark.skipif(
    not (SAMPLES / "dummy_text.pdf").exists(),
    reason="Run scripts/download_samples.py first",
)
def test_pdfplumber_extracts_text() -> None:
    pdf_bytes = (SAMPLES / "dummy_text.pdf").read_bytes()
    result = extract_with_pdfplumber(pdf_bytes, "dummy_text.pdf")
    assert result.total_chars > 0
    assert len(result.pages) >= 1
