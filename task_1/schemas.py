from pydantic import BaseModel, field_validator


class DataSchema(BaseModel):
    phone: str
    address: str

    @field_validator("phone")
    def check_phone(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("Phone field must be digit")
        return v
