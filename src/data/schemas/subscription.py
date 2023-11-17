from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType


class SubscriptionSchema(BaseModel):
    """
    A schema representing a user's subscription.

    Attributes:
        id (UUIDType): The unique identifier for the subscription.
        subscription_lvl (UUIDType): The associated subscription level ID.
        user (UUIDType): The user ID to whom the subscription belongs.
    """

    id: UUIDType = Field(description="The unique identifier for the subscription.")
    subscription_lvl: UUIDType = Field(
        ..., description="The associated subscription level ID."
    )
    user: UUIDType = Field(
        ..., description="The user ID to whom the subscription belongs."
    )

    class Config:
        orm_mode = True
