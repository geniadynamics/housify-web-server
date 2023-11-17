from tortoise import fields
from tortoise.models import Model


class Invoice(Model):
    """
    Represents an invoice for a subscription or service.

    Attributes:
        id (UUIDField): Unique identifier of the invoice.
        subscription (ForeignKeyField): Subscription related to the invoice.
        billing_info (ForeignKeyField): Billing information related to the invoice.
        payment (ForeignKeyField): Payment associated with the invoice, can be null.
        printed_pdf_path (CharField): File path of the printed invoice PDF, optional.
        emailed (BooleanField): Indicates whether the invoice was emailed or not.
        issued_at (DatetimeField): Timestamp when the invoice was issued, set automatically.
        include_nif (BooleanField): Indicates whether to include tax ID in the invoice.
    """

    id = fields.UUIDField(pk=True)

    printed_pdf_path = fields.CharField(max_length=255, null=True)
    emailed = fields.BooleanField()
    issued_at = fields.DatetimeField(auto_now_add=True)
    include_nif = fields.BooleanField()

    subscription = fields.ForeignKeyField("models.Subscription", related_name="invoice")
    billing_info = fields.ForeignKeyField("models.BillingInfo", related_name="invoice")
    payment = fields.ForeignKeyField(
        "models.Payment", related_name="invoice", null=True
    )
