
from gc import get_objects
from ninja import NinjaAPI
from typing import List
from api.models import Intervalos, Usuarios
from api.schemas.intervalos_schema import GenreSchema, IntervalosSchema, UsuariosSchema
from django.shortcuts import get_object_or_404
from django.http import JsonResponse

import requests

from api.utils import convertGenreBanco, convertGenreSpotify 

api = NinjaAPI()


@api.get('/intervalos', response=List[IntervalosSchema])
def intervalos(request):
    return  Intervalos.objects.all()

@api.get('/usuarios', response=List[UsuariosSchema])
def usuarios(request):
    return  Usuarios.objects.all()

@api.get('/usuarios/{email}', response=UsuariosSchema)
def usuarios(request, email: str):
    return  get_object_or_404(Usuarios, email=email)

@api.post('/generos/{email}')
def generos(request, email: str, genre:GenreSchema):
    usuario = get_object_or_404(Usuarios, email=email)
    usuario.genre1 = genre.genre1
    usuario.genre2 = genre.genre2
    usuario.genre3 = genre.genre3
    usuario.save()
    return "sucesso"

@api.get('/recomendacoes/{email}/{context}/{popularidade}/{token}')
def recomendacoes(request, email:str, context:str, popularidade:str, token:str):
    limite = 10
    usuario = Usuarios.objects.filter(email = email).first()
    genre1 = usuario.genre1
    genre2 = usuario.genre2
    genre3 = usuario.genre3
    #print(genre1)
    #print(genre2)
    #print(genre3)
    #VERIFICA SE O CONTEXTO VEIO, POIS O USUARIO PODE BUSCAR MÚSICAS SEM INFORMAR O CONTEXTO
    if(context != 'none'):
        #BUSCA O INTERVALO DO CONTEXTO INFORMADO.
        #SEPARA O INTERVALO PARA CADA GENERO
        #CONVERTE O GENERO DO PERFIL DO USUARIO PARA O GENERO DA LISTA DE INTERVALOS
        intervalos1 = Intervalos.objects.filter(context = context, genre = convertGenreBanco(genre1)).first()
        intervalos2 = Intervalos.objects.filter(context = context, genre = convertGenreBanco(genre2)).first()
        intervalos3 = Intervalos.objects.filter(context = context, genre = convertGenreBanco(genre3)).first()
        
        #CONVERTE O GENERO (BRASIL) DO PERFIL DO USUARIO PARA UM GENERO EQUIVALENTE NO SPOTIFY
        genreSpotify1 = convertGenreSpotify(usuario.genre1)
        genreSpotify2 = convertGenreSpotify(usuario.genre2)
        genreSpotify3 = convertGenreSpotify(usuario.genre3)

        url1 = "https://api.spotify.com/v1/recommendations?access_token="+token+"&market=BR&seed_genres="+genreSpotify1+"&danceability_min="+str(intervalos1.danceability_min)+"&danceability_max="+str(intervalos1.danceability_max)+"&energy_min="+str(intervalos1.energy_min)+"&energy_max="+str(intervalos1.energy_max)+"&loudness_min="+str(intervalos1.loudness_min)+"&loudness_max="+str(intervalos1.loudness_max)+"&speechiness_min="+str(intervalos1.speechiness_min)+"&speechiness_max="+str(intervalos1.speechiness_max)+"&acoustic_min="+str(intervalos1.acoustic_min)+"&acoustic_max="+str(intervalos1.acoustic_max)+"&valence_min="+str(intervalos1.valence_min)+"&valence_max="+str(intervalos1.valence_max)+"&min_popularity="+str(popularidade)+"&limit="+str(limite)
        url2 = "https://api.spotify.com/v1/recommendations?access_token="+token+"&market=BR&seed_genres="+genreSpotify2+"&danceability_min="+str(intervalos2.danceability_min)+"&danceability_max="+str(intervalos2.danceability_max)+"&energy_min="+str(intervalos2.energy_min)+"&energy_max="+str(intervalos2.energy_max)+"&loudness_min="+str(intervalos2.loudness_min)+"&loudness_max="+str(intervalos2.loudness_max)+"&speechiness_min="+str(intervalos2.speechiness_min)+"&speechiness_max="+str(intervalos2.speechiness_max)+"&acoustic_min="+str(intervalos2.acoustic_min)+"&acoustic_max="+str(intervalos2.acoustic_max)+"&valence_min="+str(intervalos2.valence_min)+"&valence_max="+str(intervalos2.valence_max)+"&min_popularity="+str(popularidade)+"&limit="+str(limite)
        url3 = "https://api.spotify.com/v1/recommendations?access_token="+token+"&market=BR&seed_genres="+genreSpotify3+"&danceability_min="+str(intervalos3.danceability_min)+"&danceability_max="+str(intervalos3.danceability_max)+"&energy_min="+str(intervalos3.energy_min)+"&energy_max="+str(intervalos3.energy_max)+"&loudness_min="+str(intervalos3.loudness_min)+"&loudness_max="+str(intervalos3.loudness_max)+"&speechiness_min="+str(intervalos3.speechiness_min)+"&speechiness_max="+str(intervalos3.speechiness_max)+"&acoustic_min="+str(intervalos3.acoustic_min)+"&acoustic_max="+str(intervalos3.acoustic_max)+"&valence_min="+str(intervalos3.valence_min)+"&valence_max="+str(intervalos3.valence_max)+"&min_popularity="+str(popularidade)+"&limit="+str(limite)

        lista1 = requests.get(url1).json()
        lista2 = requests.get(url2).json()
        lista3 = requests.get(url3).json()
        #print(lista1)
        return lista1
    #print('RETORNANDO LISTA SEM CONTEXTO DEFINIDO------')
    link: str = "https://api.spotify.com/v1/recommendations?seed_genres="+convertGenreSpotify(usuario.genre1)+"&market=BR&min_popularity="+popularidade+"&limit=10"
    return requests.get(link, headers={'Authorization': 'Bearer ' + token}).json()
