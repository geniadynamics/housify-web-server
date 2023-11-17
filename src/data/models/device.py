from tortoise import fields
from tortoise.models import Model

from .device_login import DeviceLogin


class Device(Model):
    """ """

    device_id = fields.UUIDField(pk=True)
    description = fields.TextField(null=True)

    # Relationships
    user = fields.ForeignKeyField("models.User", related_name="devices")
    device_logins = fields.ReverseRelation["DeviceLogin"]
