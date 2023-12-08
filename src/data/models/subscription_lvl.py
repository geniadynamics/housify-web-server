from tortoise import fields
from tortoise.models import Model


class SubscriptionLvl(Model):
    """
    Represents a level or tier of subscription, defining the features and limits.

    Attributes:
        id (UUIDField): Unique identifier of the subscription level.
        description (CharField): Description of the subscription level.
        is_active (BooleanField): Indicates whether the subscription level is active.
        price (DecimalField): Price of the subscription level.
        upload_size_limit (IntField): Upload size limit associated with the subscription level.
        storage_limit (IntField): Storage limit provided by this subscription level.
        its (DecimalField): Additional decimal attribute, possibly intended for internal tracking.
        api_key_limit (IntField): Limit on the number of API keys available at this level.
        requests_hour (IntField): Number of requests per hour allowed at this level.
        watermark (BooleanField): Indicates whether watermarks are applied at this level.
        created_at (DatetimeField): Timestamp when the subscription level was created, set automatically.
        updated_at (DatetimeField): Timestamp when the subscription level was last updated, set automatically.
    """

    id = fields.UUIDField(pk=True)

    description = fields.CharField(max_length=255)
    is_active = fields.BooleanField(default=True)
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    upload_size_limit = fields.IntField()
    storage_limit = fields.IntField()
    its = fields.DecimalField(max_digits=10, decimal_places=2)
    api_key_limit = fields.IntField()
    requests_hour = fields.IntField()
    watermark = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
