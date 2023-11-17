from tortoise import fields
from tortoise.models import Model

from .device_login import DeviceLogin
from .refresh_token import RefreshToken
from .device import Device
from .address import Address


class User(Model):
    """ """

    user_id = fields.UUIDField(pk=True)
    email = fields.CharField(max_length=255, unique=True)
    first_name = fields.CharField(max_length=16, null=True)
    last_name = fields.CharField(max_length=16, null=True)
    hashed_password = fields.BinaryField()
    gender = fields.IntField(null=True)
    phone = fields.CharField(max_length=16, null=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    devices = fields.ReverseRelation["Device"]
    refresh_tokens = fields.ReverseRelation["RefreshToken"]
    addresses = fields.ReverseRelation["Address"]
    device_logins = fields.ReverseRelation["DeviceLogin"]
    subscription_lvl = fields.ForeignKeyField(
        "models.SubscriptionLvl", related_name="users"
    )
