from tortoise import fields
from tortoise.models import Model


class Request(Model):
    id = fields.UUIDField(pk=True)
    user = fields.ForeignKeyField("models.User", related_name="request")

    input = fields.TextField()
    r_type = fields.CharField(max_length=128)

    img_input = fields.CharField(max_length=256, null=True)
    img_output = fields.CharField(max_length=256, null=True)

    output_description = fields.CharField(max_length=600, null=True)
    output_classification = fields.CharField(max_length=128, null=True)

    request_classification = fields.FloatField()
    is_public = fields.BooleanField(default=False)

    created_at = fields.DatetimeField(auto_now_add=True)
    finished_at = fields.DatetimeField(auto_now=True)
    finished_state = fields.CharField(max_length=128)
