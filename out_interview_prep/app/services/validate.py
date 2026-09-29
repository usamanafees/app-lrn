from pydantic import ValidationError

from app.schemas import Requirement, ValidateResponse, ValidationErrorItem


def validate_requirements(raw_items: list[dict]) -> ValidateResponse:
    errors: list[ValidationErrorItem] = []
    parsed: list[Requirement] = []

    for index, item in enumerate(raw_items):
        try:
            parsed.append(Requirement(**item))
        except ValidationError as exc:
            for err in exc.errors():
                loc = ".".join(str(part) for part in err["loc"])
                errors.append(
                    ValidationErrorItem(
                        field=f"[{index}].{loc}",
                        message=err["msg"],
                    )
                )

    return ValidateResponse(
        valid=len(errors) == 0,
        parsed_count=len(parsed),
        errors=errors,
    )
