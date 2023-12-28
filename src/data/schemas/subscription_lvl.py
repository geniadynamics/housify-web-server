from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID as UUIDType


class SubscriptionLvlSchema(BaseModel):
    """
    A schema representing different levels of subscription.
    """

    description: str = Field(
        description="A brief description of the subscription level."
    )
    price: float = Field(description="The price of this level of subscription.")
    upload_size_limit: int = Field(
        description="The limit on upload size for this subscription level."
    )
    storage_limit: int = Field(
        description="The storage limit provided by this subscription level."
    )
    its: float = Field(description="Iterations per second (inference), rate limit.")
    api_key_limit: int = Field(description="The limit on the number of API keys.")
    requests_hour: int = Field(description="The number of requests allowed per hour.")
    watermark: bool = Field(
        description="Indicates if watermarks are applied at this level."
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
