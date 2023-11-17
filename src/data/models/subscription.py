from tortoise import fields
from tortoise.models import Model


class SubscriptionLvl(Model):
    """ """

    subscription_lvl_id = fields.UUIDField(pk=True)
    description = fields.TextField()
    is_active = fields.BooleanField()
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    upload_size_limit = fields.IntField()
    storage_limit = fields.IntField()
    its = fields.DecimalField(max_digits=10, decimal_places=2)
    api_key_limit = fields.IntField()
    requests_hour = fields.IntField()
    watermark = fields.BooleanField()
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)
