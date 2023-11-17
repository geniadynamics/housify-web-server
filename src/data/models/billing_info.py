from tortoise import fields
from tortoise.models import Model

from .payment import Payment
from .invoice import Invoice

class BillingInfo(Model):
    """
    Represents billing information associated with a user.

    Attributes:
        id (UUIDField): Unique identifier of the billing information.
        address (ForeignKeyField): The address associated with this billing information.
        credit_card (ForeignKeyField): The credit card associated with this billing information.
        user (ForeignKeyField): The user to whom this billing information belongs.
        nif (CharField): Tax identification number, optional.
        created_at (DatetimeField): Timestamp when the billing info was created, set automatically.
        updated_at (DatetimeField): Timestamp when the billing info was last updated, set automatically.
        payment (ReverseRelation): Reverse relation to Payment.
        invoice (ReverseRelation): Reverse relation to Invoice.
    """

    id = fields.UUIDField(pk=True)

    nif = fields.CharField(max_length=16, null=True)
    bill_to_email = fields.BooleanField(default=True)

    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    address = fields.ForeignKeyField("models.Address", related_name="billing_info")
    credit_card = fields.ForeignKeyField(
        "models.CreditCard", related_name="billing_info"
    )
    user = fields.ForeignKeyField("models.User", related_name="billing_info")

    payment = fields.ReverseRelation["Payment"]
    invoice = fields.ReverseRelation["Invoice"]
