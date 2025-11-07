import re
import uvicorn
from datetime import date
import uuid
from pydantic import BaseModel, StrictStr, field_validator
from fastapi import FastAPI, responses


app = FastAPI()


class Appeal(BaseModel):
    name: StrictStr
    last_name: StrictStr
    birthdate: date
    phone: StrictStr
    email: StrictStr

    @field_validator("name", "last_name")
    def validate_name(cls, value) -> str:
        CYRILLIC_PATTERN = re.compile("[А-Я][а-я]+")
        if not CYRILLIC_PATTERN.fullmatch(value):
            raise ValueError

        return value

    @field_validator("phone")
    def validate_phone(cls, value: str) -> str:
        PHONE_PATTERN = re.compile(r"\+7[0-9]{10}")
        if not PHONE_PATTERN.fullmatch(value):
            raise ValueError

        return value

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        EMAIL_PATTERN = re.compile(r"[\w\.]+@[\w]+\.[\w]+")
        if not EMAIL_PATTERN.fullmatch(value):
            raise ValueError

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
