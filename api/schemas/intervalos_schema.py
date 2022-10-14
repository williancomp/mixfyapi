from ninja import Schema, ModelSchema

from api.models import Intervalos


class IntervalosSchema(ModelSchema):
    class Config:
        model = Intervalos
        model_fields = "__all__"