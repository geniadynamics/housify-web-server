from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID as UUIDType


class AddressSchema(BaseModel):
    """
    A schema representing an address.

    Attributes:
        id (UUIDType): The unique identifier for the address.
        country (str): The country part of the address.
        city (str): The city part of the address.
        zip_code (str): The postal code.
        addr_line_1 (str): The first line of the street address.
        addr_line_2 (Optional[str]): The second line of the street address (optional).
    """

    id: UUIDType = Field(description="The unique identifier for the address.")
    country: str = Field(..., description="The country part of the address.")
    city: str = Field(..., description="The city part of the address.")
    zip_code: str = Field(..., description="The postal code.")
    addr_line_1: str = Field(..., description="The first line of the street address.")
    addr_line_2: Optional[str] = Field(
        description="The second line of the street address (optional)."
    )

    class Config:
        orm_mode = True
