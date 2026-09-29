import shutil
from pathlib import Path

import pytest

from app.services.ocr import ocr_image_bytes

SAMPLES = Path(__file__).resolve().parents[1] / "data" / "samples"
TESSERACT_AVAILABLE = shutil.which("tesseract") is not None


@pytest.mark.skipif(
    not (SAMPLES / "regulation_scan.png").exists(),
    reason="Run scripts/download_samples.py first",
)
@pytest.mark.skipif(
    not TESSERACT_AVAILABLE,
    reason="Install tesseract (brew install tesseract) or run tests in Docker",
)
def test_ocr_finds_requirement_text() -> None:
    img_bytes = (SAMPLES / "regulation_scan.png").read_bytes()
    text = ocr_image_bytes(img_bytes)
    assert "REQ-001" in text or "pedestrian" in text.lower()
