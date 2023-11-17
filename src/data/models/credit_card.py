from tortoise import fields
from tortoise.models import Model


class CreditCard(Model):
    """
    Represents a credit card information.

    Attributes:
        id (UUIDField): Unique identifier of the credit card.
        holder (CharField): Name of the cardholder.
        number (CharField): Credit card number.
        expiry_date (DateField): Expiration date of the credit card.
        ccv (IntField): Card verification value/code.
        type (CharField): Type of the credit card (e.g., Visa, MasterCard).
    """

    id = fields.UUIDField(pk=True)

    holder = fields.CharField(max_length=255)
    number = fields.CharField(max_length=16)
    expiry_date = fields.DateField()
    ccv = fields.IntField()
    type = fields.CharField(max_length=12)
