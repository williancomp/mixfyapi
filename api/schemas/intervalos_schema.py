from ninja import Schema, ModelSchema

from api.models import Intervalos, Usuarios, Avaliacoes, Artistas


class IntervalosSchema(ModelSchema):
    class Config:
        model = Intervalos
        model_fields = "__all__"

class UsuariosSchema(ModelSchema):
    class Config:
        model = Usuarios
        model_fields = "__all__"

class AvaliacoesSchema(ModelSchema):
    class Config:
        model = Avaliacoes
        model_fields = "__all__"

class ArtistasSchema(ModelSchema):
    class Config:
        model = Artistas
        model_fields = "__all__"

class GenreSchema(Schema):
    genre1: str
    genre2: str
    genre3: str

class ComentarioSchema(Schema):
    id: str
    artista: str
    nomeArtista:str
    context: str
    radio: str
    comentario: str

class TrackSchema(Schema):
    context: str
    danceability:float
    energy:float
    loudness:float
    speechiness:float
    acousticness:float
    instrumentalness:float
    liveness:float
    valence:float


