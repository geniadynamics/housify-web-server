from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID as UUIDType


class CreditCardSchema(BaseModel):
    """
    A schema representing a credit card.

    Attributes:
        id (UUIDType): The unique identifier for the credit card.
        holder (str): The name of the cardholder.
        number (str): The credit card number.
        expiry_date (datetime): The expiration date of the credit card.
        ccv (int): The card verification value/code.
        ctype (str): The type of credit card (e.g., Visa, MasterCard).
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
        orm_mode = True
