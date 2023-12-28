from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID as UUIDType

from .credit_card import CreditCardSchema
from .address import AddressSchema


class BillingInfoSchemaIn(BaseModel):
    """
    A schema representing billing information associated with a user.
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
        """
        Configuration class for UserSchema.

        This configuration is used by Pydantic to perform additional behavior in schema
        validation and serialization.

        Attributes:
            from_attributes (bool): Indicates that the model can be constructed from objects
            with attributes (like ORM models). This replaces the deprecated `orm_mode`.
        """

        from_attributes = True


class BillingInfoSchema(BaseModel):
    """
    A schema representing billing information (complete) associated with a user.
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
        """
        Configuration class for UserSchema.

        This configuration is used by Pydantic to perform additional behavior in schema
        validation and serialization.

        Attributes:
            from_attributes (bool): Indicates that the model can be constructed from objects
            with attributes (like ORM models). This replaces the deprecated `orm_mode`.
        """

        from_attributes = True


# class BillingInfoSchemaRm(BaseModel):
#     """
#     A schema representing billing information associated with a user (removal).
#     """
#
#     id: UUIDType = Field(
#         description="The unique identifier for the billing information."
#     )
#     user_id: UUIDType = Field(description="The unique identifier for the user.")
#
#     class Config:
#         """
#         Configuration class for UserSchema.
#
#         This configuration is used by Pydantic to perform additional behavior in schema
#         validation and serialization.
#
#         Attributes:
#             from_attributes (bool): Indicates that the model can be constructed from objects
#             with attributes (like ORM models). This replaces the deprecated `orm_mode`.
#         """
#
#         from_attributes = True
