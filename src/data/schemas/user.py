from pydantic import BaseModel, Field, validator, EmailStr, ConfigDict
from typing import Optional
from uuid import UUID as UUIDType
import uuid
from datetime import date, datetime
import re


class UserRegisterSchema(BaseModel):
    """
    Schema for user serialization and deserialization, used for user registration.

    Validators:
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
    hashed_password: str = Field(
        ..., description="The hashed password, stored securely."
    )
    gender: int = Field(..., description="The user's gender as an integer value.")
    phone: Optional[str] = Field(
        None, max_length=16, description="The user's contact phone number."
    )
    birth_date: date = Field(..., description="The user's birth date.")
    # subscription_lvl_description: str = Field(
    #     default="Free-Tier",
    #     description="The user's current subscription lvl, Free is default.",
    # )

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
        excluded = ["subscription_lvl"]


class UserSchema(BaseModel):
    """
    Schema for user serialization and deserialization, used for user registration.

    Validators:
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
    gender: int = Field(..., description="The user's gender as an integer value.")
    phone: Optional[str] = Field(
        None, max_length=16, description="The user's contact phone number."
    )
    birth_date: date = Field(..., description="The user's birth date.")
    subscription_lvl: str = Field(
        default="Free-Tier",
        description="The user's current subscription lvl, Free is default.",
    )

    @validator("gender")
    def validate_gender(cls, v):
        if v not in [0, 1, 2]:
            raise ValueError("Invalid gender value")
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
        # excluded = ["subscription_lvl"]
