from tortoise import fields
from tortoise.models import Model


class Subscription(Model):
    """
    Represents a user's subscription to a service.

    Attributes:
        id (UUIDField): Unique identifier of the subscription.
        subscription_lvl (ForeignKeyField): Subscription level associated with the subscription.
        user (ForeignKeyField): User who owns the subscription.
        is_active (BooleanField): Indicates whether the subscription is active.
        start_date (DatetimeField): Start date of the subscription, set automatically.
        end_date (DatetimeField): End date of the subscription, optional.
    """

    id = fields.UUIDField(pk=True)

    is_active = fields.BooleanField()
    start_date = fields.DatetimeField(auto_now_add=True)
    end_date = fields.DatetimeField(null=True)

    subscription_lvl = fields.ForeignKeyField(
        "models.SubscriptionLvl", related_name="subscription"
    )
    user = fields.ForeignKeyField("models.User", related_name="subscription")
