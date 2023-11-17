from tortoise import fields
from tortoise.models import Model


class Payment(Model):
    """
    Represents a payment transaction.

    Attributes:
        id (UUIDField): Unique identifier of the payment.
        billing_info (ForeignKeyField): Billing information related to the payment.
        status (JSONField): Status of the payment in JSON format.
        processed_at (DatetimeField): Timestamp when the payment was processed, set automatically.
    """

    id = fields.UUIDField(pk=True)

    billing_info = fields.ForeignKeyField("models.BillingInfo", related_name="payment")
    status = fields.JSONField()
    processed_at = fields.DatetimeField(auto_now_add=True)
