from tortoise import fields
from tortoise.models import Model
from datetime import datetime


class DeviceLogin(Model):
    """ """

    device_login_id = fields.UUIDField(pk=True)
    device = fields.ForeignKeyField("models.Device", related_name="device_logins")
    user = fields.ForeignKeyField("models.User", related_name="device_logins")
    ip = fields.CharField(max_length=255)
    date = fields.DatetimeField(default=datetime.now)
