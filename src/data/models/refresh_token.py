from tortoise import fields
from tortoise.models import Model


class RefreshToken(Model):
    """
    Represents a refresh token in the system.

    This class is used to manage refresh tokens as part of the authentication system.
    It inherits from :class:`tortoise.models.Model`.

    Attributes
    ----------
    * :attr token_id: (:class:`fields.UUIDField`) Unique identifier of the refresh
        token. It is the primary key.
    * :attr user: (:class:`fields.ForeignKeyField`) Foreign key linking to the User
        model. Represents the user owning the refresh token.
    * :attr token: (:class:`fields.TextField`) The actual refresh token string.
    * :attr expiration: (:class:`fields.DatetimeField`) Datetime when the token
        expires.
    * :attr revoked: (:class:`fields.BooleanField`) Boolean flag indicating if the
        token is revoked.
    * :attr device_login: (:class:`fields.ForeignKeyField`) Optional foreign key
        linking to a DeviceLogin model. Represents the device originating the token.
    * :attr created_at: (:class:`fields.DatetimeField`) Datetime when the token was
        created. Automatically set.
    * :attr updated_at: (:class:`fields.DatetimeField`) Datetime when the token was
        last updated. Automatically updated.
    """

    token_id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="refresh_tokens")
    token = fields.TextField()
    expiration = fields.DatetimeField()
    revoked = fields.BooleanField(default=False)
    device_login = fields.ForeignKeyField(
        "models.DeviceLogin", related_name="refresh_tokens", null=True
    )
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
