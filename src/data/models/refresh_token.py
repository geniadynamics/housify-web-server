from tortoise import fields
from tortoise.models import Model


class RefreshToken(Model):
    """
    Represents a refresh token for authentication, allowing users to obtain a new access token.

    Attributes:
        id (UUIDField): Unique identifier of the refresh token.
        user (ForeignKeyField): User to whom the refresh token belongs.
        token (TextField): The actual refresh token string.
        expiration (DatetimeField): Expiry date and time of the token.
        revoked (BooleanField): Flag indicating whether the token has been revoked.
        device_login_id (CharField): ID of the device login associated with the token.
        created_at (DatetimeField): Timestamp when the token was created, set automatically.
        updated_at (DatetimeField): Timestamp when the token was last updated, set automatically.
    """

    token_id = fields.UUIDField(pk=True)

    token = fields.TextField()
    expiration = fields.DatetimeField()
    revoked = fields.BooleanField(default=False)

    device_login = fields.ForeignKeyField(
        "models.DeviceLogin", related_name="refresh_tokens", null=True
    )
    user = fields.ForeignKeyField("models.User", related_name="refresh_tokens")

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
