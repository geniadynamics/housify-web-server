from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID as UUIDType


class CreditCardSchema(BaseModel):
    """
    A schema representing a credit card.
    """

    id: UUIDType = Field(description="The unique identifier for the credit card.")
    holder: str = Field(..., description="The name of the cardholder.")
    number: str = Field(..., max_length=16, description="The credit card number.")
    expiry_date: datetime = Field(
        ..., description="The expiration date of the credit card."
    )
    ccv: int = Field(..., description="The card verification value/code.")
    ctype: str = Field(
        ...,
        max_length=12,
        description="The type of credit card (e.g., Visa, MasterCard).",
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
