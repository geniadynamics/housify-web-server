from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID as UUIDType
from datetime import datetime


class RequestSchemaIn(BaseModel):
    user: str = Field()

    input: str = Field()

    img_input: Optional[str] = Field(None, max_length=256)
    img_output: Optional[str] = Field(None, max_length=256)

    output_description: Optional[str] = Field(None, max_length=600)
    output_classification: Optional[str] = Field(None, max_length=128)

    request_classification: float
    is_public: bool = False

    class Config:
        orm_mode = True


class RequestSchemaOut(BaseModel):
    input: str = Field()

    img_input: Optional[str] = Field(None, max_length=256)
    img_output: Optional[str] = Field(None, max_length=256)

    output_description: Optional[str] = Field(None, max_length=600)
    output_classification: Optional[str] = Field(None, max_length=128)

    request_classification: float
    is_public: bool = False

    class Config:
        orm_mode = True
