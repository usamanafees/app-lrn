import io
import os
import shutil

import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image

if cmd := os.getenv("TESSERACT_CMD"):
    pytesseract.pytesseract.tesseract_cmd = cmd
elif shutil.which("tesseract"):
    pytesseract.pytesseract.tesseract_cmd = shutil.which("tesseract") or "tesseract"


def ocr_image_bytes(file_bytes: bytes) -> str:
    image = Image.open(io.BytesIO(file_bytes))
    return pytesseract.image_to_string(image).strip()


def ocr_pdf_scanned(file_bytes: bytes) -> list[str]:
    images = convert_from_bytes(file_bytes)
    return [pytesseract.image_to_string(img).strip() for img in images]
