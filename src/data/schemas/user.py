from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from uuid import UUID as UUIDType


class UserSchema(BaseModel):
    """
    Schema for user serialization and deserialization, used to represent a user entity.

    Attributes:
        id (UUIDType): The unique identifier for the user.
        email (str): The email address of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        hashed_password (bytes): The hashed password for the user.
        gender (int): The gender of the user represented as an integer.
        phone (Optional[str]): The phone number of the user.
        created_at (datetime): The date and time when the user was created.
        updated_at (datetime): The date and time when the user information was last updated.
    """

    id: UUIDType = Field(description="The unique identifier for the user.")
    email: str = Field(..., max_length=255, description="The user's email address.")
    first_name: str = Field(..., max_length=16, description="The user's first name.")
    last_name: str = Field(..., max_length=16, description="The user's last name.")
    hashed_password: bytes = Field(
        ..., description="The hashed password, stored securely."
    )
    gender: int = Field(..., description="The user's gender as an integer value.")
    phone: Optional[str] = Field(
        max_length=16, description="The user's contact phone number."
    )

    class Config:
        orm_mode = True
