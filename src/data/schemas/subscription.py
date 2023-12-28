from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType


class SubscriptionSchema(BaseModel):
    """
    A schema representing a user's subscription.
    """

    id: UUIDType = Field(description="The unique identifier for the subscription.")
    subscription_lvl: UUIDType = Field(
        ..., description="The associated subscription level ID."
    )
    user: UUIDType = Field(
        ..., description="The user ID to whom the subscription belongs."
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
