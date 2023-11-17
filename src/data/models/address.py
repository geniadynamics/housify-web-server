from tortoise import fields
from tortoise.models import Model


class Address(Model):
    """ """

    addr_id = fields.UUIDField(pk=True)
    country = fields.CharField(max_length=255)
    city = fields.CharField(max_length=255)
    zip_code = fields.TextField()
    addr_line_1 = fields.TextField()
    addr_line_2 = fields.TextField(null=True)

    user = fields.ForeignKeyField("models.User", related_name="addresses")
