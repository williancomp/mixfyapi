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

class IntervaloObject(Schema):
    danceability_min:float
    danceability_max:float
    energy_min:float
    energy_max:float
    loudness_min:float
    loudness_max:float
    speechiness_min:float
    speechiness_max:float
    acousticness_min:float
    acousticness_max:float
    instrumentalness_min:float
    instrumentalness_max:float
    liveness_min:float
    liveness_max:float
    valence_min:float
    valence_max:float


