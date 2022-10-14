
from ninja import NinjaAPI
from typing import List
from api.models import Intervalos
from api.schemas.intervalos_schema import IntervalosSchema

api = NinjaAPI()

@api.get('/recomendacoes')
def recomendacoes(request):
    return "Olá Mundo 2"

@api.get('/intervalos', response=List[IntervalosSchema])
def intervalos(request):
    return  Intervalos.objects.all()