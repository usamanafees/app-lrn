import io

import pdfplumber
import fitz  # pymupdf

from app.schemas import ExtractedPage, PdfExtractResponse


def extract_with_pdfplumber(file_bytes: bytes, filename: str) -> PdfExtractResponse:
    pages: list[ExtractedPage] = []
    with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            pages.append(ExtractedPage(page_number=i, text=text.strip(), method="pdf_text"))
    total = sum(len(p.text) for p in pages)
    return PdfExtractResponse(filename=filename, pages=pages, total_chars=total)


def extract_with_pymupdf(file_bytes: bytes, filename: str) -> PdfExtractResponse:
    pages: list[ExtractedPage] = []
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for i, page in enumerate(doc, start=1):
        text = page.get_text().strip()
        pages.append(ExtractedPage(page_number=i, text=text, method="pdf_text"))
    total = sum(len(p.text) for p in pages)
    return PdfExtractResponse(filename=filename, pages=pages, total_chars=total)
