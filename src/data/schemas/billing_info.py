from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType

from .credit_card import CreditCardSchema
from .address import AddressSchema


class BillingInfoSchemaIn(BaseModel):
    """
    A schema representing billing information associated with a user.

    Attributes:
        id (UUIDType): The unique identifier for the billing information.
        address (UUIDType): The associated address ID.
        credit_card (UUIDType): The associated credit card ID.
        user (UUIDType): The user ID to whom this billing information belongs.
        nif (Optional[str]): The tax identification number (optional).
    """

    id: UUIDType = Field(
        description="The unique identifier for the billing information."
    )
    address: UUIDType = Field(..., description="The associated address ID.")
    credit_card: UUIDType = Field(..., description="The associated credit card ID.")
    user: UUIDType = Field(
        ..., description="The user ID to whom this billing information belongs."
    )
    nif: Optional[str] = Field(
        None, max_length=255, description="The tax identification number (optional)."
    )

    class Config:
        orm_mode = True


class BillingInfoSchema(BaseModel):
    """
    A schema representing billing information (complete) associated with a user.

    Attributes:
        id (UUIDType): The unique identifier for the billing information.
        nif (Optional[str]): The tax identification number (optional).
        user (UUIDType): The user ID to whom this billing information belongs.
        address_info (AddressSchema): The address information.
        credit_card_info (CreditCardSchema): The credit card information.
    """

    id: UUIDType = Field(
        description="The unique identifier for the billing information."
    )
    user: UUIDType = Field(
        ..., description="The user ID to whom this billing information belongs."
    )
    nif: Optional[str] = Field(
        None, max_length=255, description="The tax identification number (optional)."
    )
    address_info: AddressSchema
    credit_card_info: CreditCardSchema

    class Config:
        orm_mode = True


class BillingInfoSchemaRm(BaseModel):
    """
    A schema representing billing information associated with a user (removal).

    Attributes:
        id (UUIDType): The unique identifier for the billing information.
        user_id (UUIDType): The unique identifier for user reponsible for the
            billing information.
    """

    id: UUIDType = Field(
        description="The unique identifier for the billing information."
    )
    user_id: UUIDType = Field(description="The unique identifier for the user.")

    class Config:
        orm_mode = True