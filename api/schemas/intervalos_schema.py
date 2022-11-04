from ninja import Schema, ModelSchema

from api.models import Intervalos, Usuarios


class IntervalosSchema(ModelSchema):
    class Config:
        model = Intervalos
        model_fields = "__all__"

class UsuariosSchema(ModelSchema):
    class Config:
        model = Usuarios
        model_fields = "__all__"

class GenreSchema(Schema):
    genre1: str
    genre2: str
    genre3: str

class ComentarioSchema(Schema):
    id: str
    artista: str
    context: str
    radio: str
    comentario: str
