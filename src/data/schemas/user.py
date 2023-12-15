from pydantic import BaseModel, Field, validator, EmailStr
from typing import Optional
from uuid import UUID as UUIDType
import uuid
from datetime import date, datetime
import re


class UserRegisterSchema(BaseModel):
    """
    Schema for user serialization and deserialization, used for user registration.

    Attributes:
        email (EmailStr): The email address of the user, validated for standard format.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        hashed_password (bytes): The hashed password, securely stored, must be 64 bytes.
        gender (int): The gender, represented as an integer. Valid values: 0, 1, 3.
        phone (Optional[str]): The contact phone number, optional field, validated for format.
        birth_date (date): The birth date of the user, validated to ensure 16+ years.
        subscription_lvl (UUID): Current subscription level, default is Free.

    Methods:
        validate_gender(cls, v): Checks gender is a valid integer value.
        validate_hashed_password(cls, v): Ensures hashed password is 64 bytes.
        validate_birth_date(cls, v): Ensures user is at least 16 years old.
        validate_phone(cls, v): Validates the phone number format.
    """

    email: EmailStr = Field(
        ..., max_length=255, description="The user's email address."
    )
    first_name: str = Field(..., max_length=16, description="The user's first name.")
    last_name: str = Field(..., max_length=16, description="The user's last name.")
    hashed_password: bytes = Field(
        ..., description="The hashed password, stored securely."
    )
    gender: int = Field(..., description="The user's gender as an integer value.")
    phone: Optional[str] = Field(
        None, max_length=16, description="The user's contact phone number."
    )
    birth_date: date = Field(..., description="The user's birth date.")
    subscription_lvl: UUIDType = Field(
        default=uuid.UUID("403da318-0d04-4124-a5b9-1809bd76828f"),
        description="The user's current subscription lvl, Free is default.",
    )

    @validator("gender")
    def validate_gender(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError("Invalid gender value")
        return v

    @validator("hashed_password")
    def validate_hashed_password(cls, v):
        # if len(v) != 64:
        #     raise ValueError("Invalid hashed password length")
        return v

    @validator("birth_date")
    def validate_birth_date(cls, v):
        if (datetime.now().date() - v).days / 365.25 < 16:
            raise ValueError("User must be at least 16 years old")
        return v

    @validator("phone")
    def validate_phone(cls, v):
        if v is not None:
            phone_regex = r"^\+?1?\d{9,15}$"
            if not re.fullmatch(phone_regex, v):
                raise ValueError("Invalid phone number format")
        return v

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


class UserSchema(UserRegisterSchema):
    """
    Schema for user representation, extends UserRegisterSchema with a unique ID.

    Used for operations requiring user identification like retrieval or updates.

    Attributes:
        id (UUIDType): Unique identifier for the user, key for individual distinction.
    """

    id: UUIDType = Field(description="The unique identifier for the user.")
    hashed_password: Optional[bytes] = None

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
        exclude_unset = True
