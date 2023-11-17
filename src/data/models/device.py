from tortoise import fields
from tortoise.models import Model

from .device_login import DeviceLogin


class Device(Model):
    """
    Represents a device used by a user, potentially for authentication purposes.

    Attributes:
        id (UUIDField): Unique identifier of the device.
        description (CharField): Description of the device.
        device_login (ReverseRelation): Reverse relation to DeviceLogin, representing login
            attempts or sessions from this device.
    """

    device_id = fields.UUIDField(pk=True)
    description = fields.TextField(null=True)

    device_logins = fields.ReverseRelation["DeviceLogin"]
