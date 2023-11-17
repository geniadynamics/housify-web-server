from tortoise import fields
from tortoise.models import Model


class Address(Model):
    """
    Represents a client's address.

    Attributes:
        id (UUIDField): Unique identifier of the address.
        country (CharField): Country part of the address.
        city (CharField): City part of the address.
        zip_code (CharField): Postal code of the address.
        addr_line_1 (CharField): First line of the street address.
        addr_line_2 (CharField): Second line of the street address, optional.
    """

    id = fields.UUIDField(pk=True)

    country = fields.CharField(max_length=128)
    city = fields.CharField(max_length=128)
    zip_code = fields.CharField(max_length=64)
    addr_line_1 = fields.CharField(max_length=255)
    addr_line_2 = fields.CharField(max_length=255, null=True)
