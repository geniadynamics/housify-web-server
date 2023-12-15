from pydantic import BaseModel, Field
from datetime import datetime
from uuid import UUID as UUIDType


class RefreshTokenSchema(BaseModel):
    """
    A schema for refresh token serialization and deserialization, part of the authentication system.

    Attributes:
        id (UUIDType): The unique identifier for the refresh token.
        user (UUIDType): The ID of the user to whom the token belongs.
        token (str): The token string used for refreshing authentication.
        expiration (datetime): The datetime when the token expires.
        revoked (bool): A boolean flag indicating if the token has been revoked.
    """

    id: UUIDType = Field(description="The unique identifier for the refresh token.")
    user: UUIDType = Field(
        ..., description="The ID of the user to whom the token belongs."
    )
    token: str | None = Field(
        description="The token string used for refreshing authentication."
    )
    expiration: datetime = Field(description="The datetime when the token expires.")
    revoked: bool = Field(
        description="A boolean flag indicating if the token has been revoked."
    )

    class Config:
        from_attributes = True
