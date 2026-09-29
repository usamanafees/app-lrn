from fastapi import FastAPI, File, HTTPException, UploadFile

from app.schemas import (
    LlmExtractRequest,
    LlmExtractResponse,
    OcrResponse,
    PdfExtractResponse,
    Requirement,
    ValidateResponse,
)
from app.services.llm_extract import extract_requirements_from_text
from app.services.manifest import read_manifest
from app.services.ocr import ocr_image_bytes, ocr_pdf_scanned
from app.services.pdf_extract import extract_with_pdfplumber, extract_with_pymupdf
from app.services.validate import validate_requirements

app = FastAPI(title="Regulatory Extraction Prep API", version="0.1.0")


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/documents")
def list_documents() -> list[dict]:
    return read_manifest()


@app.post("/extract/pdf", response_model=PdfExtractResponse)
async def extract_pdf(
    file: UploadFile = File(...),
    engine: str = "pdfplumber",
) -> PdfExtractResponse:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Upload a .pdf file")

    data = await file.read()
    if engine == "pymupdf":
        return extract_with_pymupdf(data, file.filename)
    return extract_with_pdfplumber(data, file.filename)


@app.post("/extract/pdf/ocr", response_model=list[str])
async def extract_pdf_ocr(file: UploadFile = File(...)) -> list[str]:
    if not file.filename or not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Upload a .pdf file")

    data = await file.read()
    return ocr_pdf_scanned(data)


@app.post("/extract/image/ocr", response_model=OcrResponse)
async def extract_image_ocr(file: UploadFile = File(...)) -> OcrResponse:
    allowed = (".png", ".jpg", ".jpeg", ".tif", ".tiff")
    if not file.filename or not file.filename.lower().endswith(allowed):
        raise HTTPException(status_code=400, detail=f"Upload an image: {allowed}")

    data = await file.read()
    text = ocr_image_bytes(data)
    return OcrResponse(filename=file.filename, text=text)


@app.post("/validate/requirements", response_model=ValidateResponse)
def validate_requirements_endpoint(items: list[dict]) -> ValidateResponse:
    return validate_requirements(items)


@app.post("/validate/requirements/typed", response_model=list[Requirement])
def validate_requirements_typed(items: list[Requirement]) -> list[Requirement]:
    return items


@app.post("/extract/requirements/llm", response_model=LlmExtractResponse)
def extract_requirements_llm(body: LlmExtractRequest) -> LlmExtractResponse:
    try:
        raw_items = extract_requirements_from_text(body.text, provider=body.provider)
        requirements = [Requirement(**item) for item in raw_items]
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail=f"LLM extraction failed: {exc}") from exc

    return LlmExtractResponse(
        provider=body.provider,
        requirements=requirements,
        count=len(requirements),
    )
