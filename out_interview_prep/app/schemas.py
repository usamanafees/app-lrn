from typing import Literal

from pydantic import BaseModel, Field


class Requirement(BaseModel):
    id: str
    section: str
    text: str
    obligation_level: str | None = None


class ExtractedPage(BaseModel):
    page_number: int
    text: str
    method: str = Field(description="pdf_text or ocr")


class PdfExtractResponse(BaseModel):
    filename: str
    pages: list[ExtractedPage]
    total_chars: int


class OcrResponse(BaseModel):
    filename: str
    text: str


class ValidationErrorItem(BaseModel):
    field: str
    message: str


class ValidateResponse(BaseModel):
    valid: bool
    parsed_count: int
    errors: list[ValidationErrorItem]


class LlmExtractRequest(BaseModel):
    text: str
    provider: Literal["claude", "gemini"] = "claude"


class LlmExtractResponse(BaseModel):
    provider: str
    requirements: list[Requirement]
    count: int
