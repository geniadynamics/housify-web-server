from pydantic import BaseModel, Field, validator, EmailStr


class LoginSchema(BaseModel):
    """ """

    email: EmailStr = Field(
        ..., max_length=255, description="The user's email address."
    )
    hashed_password: bytes = Field(
        ..., description="The hashed password, stored securely."
    )

    @validator("hashed_password")
    def validate_hashed_password(cls, v):
        # if len(v) != 64:
        #     raise ValueError("Invalid hashed password length")
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


class LoginSchemaWithToken(BaseModel):
    """ """

    email: EmailStr = Field(
        ..., max_length=255, description="The user's email address."
    )


class TokenResponse(BaseModel):
    """ """

    access_token: str
    refresh_token: str
