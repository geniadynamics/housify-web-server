from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID as UUIDType


class AddressSchema(BaseModel):
    """
    A schema representing an address (creation).
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
        """
        Configuration class for UserSchema.

        This configuration is used by Pydantic to perform additional behavior in schema
        validation and serialization.

        Attributes:
            from_attributes (bool): Indicates that the model can be constructed from objects
            with attributes (like ORM models). This replaces the deprecated `orm_mode`.
        """

        from_attributes = True
