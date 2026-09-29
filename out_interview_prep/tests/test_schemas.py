import pytest
from pydantic import ValidationError

from app.schemas import Requirement
from app.services.validate import validate_requirements


def test_requirement_valid() -> None:
    req = Requirement(id="REQ-001", section="1.0", text="System shall log events.")
    assert req.id == "REQ-001"


def test_requirement_missing_field() -> None:
    with pytest.raises(ValidationError):
        Requirement(id="REQ-001", section="1.0")  # type: ignore[call-arg]


def test_validate_requirements_ok() -> None:
    items = [{"id": "REQ-001", "section": "1.0", "text": "Foo shall bar."}]
    result = validate_requirements(items)
    assert result.valid is True
    assert result.parsed_count == 1
    assert result.errors == []


def test_validate_requirements_bad() -> None:
    items = [{"id": "REQ-001", "section": "1.0"}]
    result = validate_requirements(items)
    assert result.valid is False
    assert result.parsed_count == 0
    assert len(result.errors) == 1
