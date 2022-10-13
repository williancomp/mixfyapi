from django.shortcuts import HttpResponse, render
from ninja import NinjaAPI


api = NinjaAPI()

@api.get('/recomendacoes')
def recomendacoes(request):
    return "Olá Mundo"