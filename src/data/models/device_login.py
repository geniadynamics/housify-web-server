from tortoise import fields
from tortoise.models import Model


class DeviceLogin(Model):
    """
    Represents a login event from a device, associated with a user.

    Attributes:
        id (UUIDField): Unique identifier of the device login record.
        device (ForeignKeyField): Device used for the login.
        user (ForeignKeyField): User who logged in.
        ip (CharField): IP address from which the login was made.
        date (DatetimeField): Timestamp when the login occurred, set automatically.
    """

    id = fields.UUIDField(pk=True)

    ip = fields.CharField(max_length=128)
    date = fields.DatetimeField(auto_now_add=True)

    device = fields.ForeignKeyField("models.Device", related_name="device_login")
    user = fields.ForeignKeyField("models.User", related_name="device_login")
