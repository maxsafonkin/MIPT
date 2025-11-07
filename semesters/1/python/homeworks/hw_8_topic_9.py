import typing as t
import re
import uvicorn
from datetime import date
import uuid
from pydantic import BaseModel, StrictStr, field_validator, ValidationInfo
from fastapi import FastAPI, responses


app = FastAPI()


class Validator:
    def __init__(self, pattern: str):
        self._pattern: re.Pattern = re.compile(pattern)

    def validate(self, value: t.Any) -> t.Any:
        if not self._pattern.fullmatch(str(value)):
            raise ValueError


PATTERNS = {
    "cyrillic_capitalized": r"[А-Я][а-я]+",
    "phone": r"\+7[0-9]{10}",
    "email": r"[\w\.]+@[\w]+\.[\w]+",
}
FIELD_TO_PATTERN_NAME = {
    "name": "cyrillic_capitalized",
    "last_name": "cyrillic_capitalized",
    "phone": "phone",
    "email": "email",
}


def create_validator(field_name: str) -> Validator:
    return Validator(pattern=PATTERNS[FIELD_TO_PATTERN_NAME[field_name]])


FIELD_VALIDATORS = {
    field: create_validator(field) for field in ["name", "last_name", "phone", "email"]
}


class Appeal(BaseModel):
    name: StrictStr
    last_name: StrictStr
    birthdate: date
    phone: StrictStr
    email: StrictStr

    @field_validator("*")
    def validate_field(cls, value: t.Any, info: ValidationInfo) -> t.Any:
        if validator := FIELD_VALIDATORS.get(info.field_name or ""):
            validator.validate(value=value)
        return value


@app.post("/appeal")
def create_appeal(
    name: StrictStr,
    last_name: StrictStr,
    birthdate: date,
    phone: StrictStr,
    email: StrictStr,
) -> responses.JSONResponse:
    try:
        appeal = Appeal(
            name=name,
            last_name=last_name,
            birthdate=birthdate,
            phone=phone,
            email=email,
        )
        appeal_id = uuid.uuid4()

        with open(f"{appeal_id}.json", "w") as f:
            f.write(appeal.model_dump_json())

        return responses.JSONResponse(
            content={"success": True, "data": {"appeal_id": str(appeal_id)}},
            status_code=200,
        )
    except Exception as exc:
        return responses.JSONResponse(
            content={"success": False, "error": str(exc)}, status_code=200
        )


if __name__ == "__main__":
    uvicorn.run(app, port=7654)
