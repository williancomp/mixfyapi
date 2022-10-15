
from ninja import NinjaAPI
from typing import List
from api.models import Intervalos, Usuarios
from api.schemas.intervalos_schema import IntervalosSchema, UsuariosSchema

api = NinjaAPI()

@api.get('/recomendacoes')
def recomendacoes(request):
    return "Olá Mundo"

@api.get('/intervalos', response=List[IntervalosSchema])
def intervalos(request):
    return  Intervalos.objects.all()

@api.get('/usuarios', response=List[UsuariosSchema])
def usuarios(request):
    return  Usuarios.objects.all()