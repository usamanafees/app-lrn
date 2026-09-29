"""Download sample PDFs and create a synthetic scan image for OCR practice."""

from pathlib import Path

import httpx
from PIL import Image, ImageDraw, ImageFont
from tenacity import RetryError, retry, stop_after_attempt, wait_exponential

ROOT = Path(__file__).resolve().parents[1]
SAMPLES = ROOT / "data" / "samples"

# Small public PDF (W3C sample) — stable URL for text extraction demos.
TEXT_PDF_URL = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"

# UN ECE regulation PDF excerpt (public regulatory-style document).
REG_PDF_URL = (
    "https://unece.org/fileadmin/DAM/trans/doc/2016/wp29/"
    "ECE-TRANS-WP29-2016-03-Rev1.pdf"
)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(min=1, max=8))
def download_file(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    with httpx.Client(timeout=60.0, follow_redirects=True) as client:
        response = client.get(url)
        response.raise_for_status()
        dest.write_bytes(response.content)
    print(f"saved {dest} ({dest.stat().st_size} bytes)")


def try_download(url: str, dest: Path) -> None:
    try:
        download_file(url, dest)
    except (httpx.HTTPError, RetryError) as exc:
        print(f"skip {dest.name}: {exc}")


def create_scan_image(dest: Path) -> None:
    """Simulate a scanned regulatory snippet — OCR path when PDF has no text layer."""
    dest.parent.mkdir(parents=True, exist_ok=True)
    img = Image.new("RGB", (900, 400), color=(245, 245, 240))
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    lines = [
        "UN ECE R152 — Pedestrian Detection",
        "REQ-001: The system shall detect pedestrians at speeds up to 60 km/h.",
        "REQ-002: Warning shall be issued within 2.0 seconds of detection.",
        "REQ-003: False positive rate shall not exceed 1 per 100 km.",
    ]
    y = 40
    for line in lines:
        draw.text((40, y), line, fill=(20, 20, 20), font=font)
        y += 50
    img.save(dest)
    print(f"created scan image {dest}")


def main() -> None:
    SAMPLES.mkdir(parents=True, exist_ok=True)
    try_download(TEXT_PDF_URL, SAMPLES / "dummy_text.pdf")
    try_download(REG_PDF_URL, SAMPLES / "un_ece_regulation.pdf")
    create_scan_image(SAMPLES / "regulation_scan.png")
    print("done — check data/samples/")


if __name__ == "__main__":
    main()
