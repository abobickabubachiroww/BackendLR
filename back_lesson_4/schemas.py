from pydantic import BaseModel, Field, field_validator


class ServiceCreate(BaseModel):
    categoryId: int = Field(gt=0)

    title: str = Field(min_length=1, max_length=100)

    desc: str = Field(min_length=1, max_length=100)

    duration: int = Field(ge=30, le=180)

    price: float = Field(gt=0)

    @field_validator("title", "desc")
    @classmethod
    def validate_not_empty(cls, value):
        if not value.strip():
            raise ValueError("Поле не должно быть пустым")
        return value.strip()