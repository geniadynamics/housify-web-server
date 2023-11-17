from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID as UUIDType


class PaymentSchema(BaseModel):
    """
    A schema representing a payment record.

    Attributes:
        id (UUIDType): The unique identifier for the payment.
        billing_info (UUIDType): The associated billing info ID.
        status (dict): The JSON status object of the payment.
        processed_at (datetime): Timestamp when the payment was processed.
    """

    id: UUIDType = Field(description="The unique identifier for the payment.")
    billing_info: UUIDType = Field(..., description="The associated billing info ID.")
    status: dict = Field(..., description="The JSON status object of the payment.")
    processed_at: datetime = Field(
        description="Timestamp when the payment was processed."
    )

    class Config:
        orm_mode = True
