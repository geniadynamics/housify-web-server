from tortoise import fields
from tortoise.models import Model

from tortoise.contrib.pydantic.creator import pydantic_model_creator

from pydantic import EmailStr, validator, PydanticSchemaGenerationError


from .device_login import DeviceLogin
from .refresh_token import RefreshToken
from .device import Device
from .address import Address
from .subscription import Subscription
from .billing_info import BillingInfo
from .subscription_lvl import SubscriptionLvl

from data.models import DeviceLogin, RefreshToken, Device

from datetime import date, datetime
from typing import Union

import re


class User(Model):
    """
    Represents a user in the system.

    Attributes:
        id (UUIDField): Unique identifier of the user.
        email (CharField): Email address of the user.
        first_name (CharField): First name of the user.
        last_name (CharField): Last name of the user.
        hashed_password (BinaryField): Securely stored hashed password.
        gender (IntField): Gender of the user represented as an integer.
        phone (CharField): Contact phone number of the user.
        created_at (DatetimeField): Timestamp when the user was created, set automatically.
        updated_at (DatetimeField): Timestamp when the user was last updated, set automatically.
        billing_info (ReverseRelation): Reverse relation to BillingInfo.
        subscription (ReverseRelation): Reverse relation to Subscription.
        refresh_token (ReverseRelation): Reverse relation to RefreshToken.
        device_login (ReverseRelation): Reverse relation to DeviceLogin.
    """

    id = fields.UUIDField(pk=True)

    email = fields.CharField(max_length=255, unique=True)
    first_name = fields.CharField(max_length=16, null=True)
    last_name = fields.CharField(max_length=16, null=True)
    hashed_password = fields.CharField(max_length=128)
    gender = fields.IntField(null=True)
    phone = fields.CharField(max_length=16, null=True)
    birth_date = fields.DateField()

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    subscriptions: fields.ReverseRelation["Subscription"]
    billing_info: fields.ReverseRelation["BillingInfo"]
    devices: fields.ReverseRelation["Device"]
    refresh_tokens: fields.ReverseRelation["RefreshToken"]
    addresses: fields.ReverseRelation["Address"]
    device_logins: fields.ReverseRelation["DeviceLogin"]

    subscription_lvl = fields.CharField(max_length=128, default="Free-Tier")

    
    # class PydanticMeta:
    #     @validator("gender")
    #     def validate_gender(cls, v):
    #         if v not in [0, 1, 2]:
    #             raise ValueError("Invalid gender value")
    #         return v
    #
    #     @validator("email")
    #     def validate_email(cls, v: str) -> EmailStr:
    #         return EmailStr(v)
    #
    #     @validator("hashed_password")
    #     def validate_hashed_password(cls, v):
    #         # if len(v) != 64:
    #         #     raise ValueError("Invalid hashed password length")
    #         return v
    #
    #     @validator("birth_date")
    #     def validate_birth_date(cls, v):
    #         if (datetime.now().date() - v).days / 365.25 < 16:
    #             raise ValueError("User must be at least 16 years old")
    #         return v
    #
    #     @validator("phone")
    #     def validate_phone(cls, v):
    #         if v is not None:
    #             phone_regex = r"^\+?1?\d{9,15}$"
    #             if not re.fullmatch(phone_regex, v):
    #                 raise ValueError("Invalid phone number format")
    #         return v
