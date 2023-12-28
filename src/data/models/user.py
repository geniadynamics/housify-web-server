from tortoise import fields
from tortoise.models import Model
from .device_login import DeviceLogin
from .device import Device
from .address import Address
from .subscription import Subscription
from .billing_info import BillingInfo

from data.models import DeviceLogin, Device


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
    addresses: fields.ReverseRelation["Address"]
    device_logins: fields.ReverseRelation["DeviceLogin"]

    subscription_lvl = fields.CharField(max_length=128, default="Free-Tier")
