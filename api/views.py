
from gc import get_objects
from ninja import NinjaAPI
from typing import List
from api.models import Intervalos, Usuarios, Avaliacoes
from api.schemas.intervalos_schema import GenreSchema, IntervalosSchema, UsuariosSchema, ComentarioSchema, AvaliacoesSchema, Artistas, ArtistasSchema
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import datetime


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
    print(token)
    limite = 5
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
        

        #VERIFICA O ARTISTA PREFERIDO E BUSCA RECOMENDAÇÕES BASEADA NO ARTISTA PREFERIDO
        artista = Artistas.objects.filter(email = email, contexto = context).order_by('-likes')
        if(artista.exists()):
            topArtistas = ""
            for i in range(len(artista)):
                if(i < 3):
                    topArtistas += artista[i].idArtista + ","

            urlArtista = "https://api.spotify.com/v1/recommendations?access_token="+token+"&market=BR&seed_artists="+topArtistas+"&min_popularity="+str(popularidade)+"&limit="+str(limite)

            listaArtista = requests.get(urlArtista).json()
            
            backLista1 = lista1
            lista1 = listaArtista
            listaArtista = backLista1
            

            #ADICIONA A LISTA DE ARTISTAS NA LISTA 1 - SOMENTE SE TIVER ARTISTA PREFERIDO
            contador3:int = 0
            for item5 in listaArtista['tracks']:
                for item6 in lista1['tracks']:
                    if(item5['name'] == item6['name']):
                        contador3+=1
                if(contador3 == 0):
                    ##print(item5['name'])
                    lista1['tracks'].append(item5)
                else:
                    contador3=0
        #REUNI TODAS AS MUSICAS DE CADA GENERO EM UMA UNICA LISTA E REMOVE DUPLICADOS
        contador1:int = 0
        for item2 in lista2['tracks']:
            for item1 in lista1['tracks']:
                if(item2['name'] == item1['name']):
                    contador1+=1
            if(contador1 == 0):
                lista1['tracks'].append(item2)
                #array_push(lista1['tracks'], item2)
            else:
                contador1 = 0

        contador2:int = 0
        for item3 in lista3['tracks']:
            for item4 in lista1['tracks']:
                if(item3['name'] == item4['name']):
                    contador2+=1
            if(contador2 == 0):
                lista1['tracks'].append(item3)
            else:
                contador2=0       

        
        return lista1
    #print('RETORNANDO LISTA SEM CONTEXTO DEFINIDO------')
    link: str = "https://api.spotify.com/v1/recommendations?seed_genres="+convertGenreSpotify(usuario.genre1)+"&market=BR&min_popularity="+popularidade+"&limit=10"
    return requests.get(link, headers={'Authorization': 'Bearer ' + token}).json()




@api.post('/avaliacoes/{email}/{token}')
def generos(request, email:str, token:str, comentario:List[ComentarioSchema]):

    url = "https://api.spotify.com/v1/audio-features"
    
    #ADICIONA TODOS IDs DAS MUSICAS EM UM UNICA STRING
    ids:str = ''
    for item in comentario:
        ids+= item.id + ","

    #BUSCA AS MÚSICAS PELO SEUS IDs
    response = requests.get(url, params={
        "access_token": token, 
        "ids": ids
    }).json()
    
    features = response['audio_features']
    

    for i in range(len(comentario)):
        
        avaliacao = Avaliacoes()
        avaliacao.idMusic = comentario[i].id
        avaliacao.email = email
        avaliacao.context = comentario[i].context
        avaliacao.artista = comentario[i].artista
        avaliacao.nomeArtista = comentario[i].nomeArtista
        avaliacao.evaluation = comentario[i].radio
        avaliacao.comentario = comentario[i].comentario
        avaliacao.danceability = features[i]['danceability']
        avaliacao.energy = features[i]['energy']
        avaliacao.loudness = features[i]['loudness']
        avaliacao.speechiness = features[i]['speechiness']
        avaliacao.acousticness = features[i]['acousticness']
        avaliacao.instrumentalness = features[i]['instrumentalness']
        avaliacao.liveness = features[i]['liveness']
        avaliacao.valence = features[i]['valence']
        avaliacao.tempo = features[i]['tempo']
        avaliacao.pub_date = datetime.datetime.now()
        avaliacao.save()
        
        artista = Artistas.objects.filter(email = email, contexto = comentario[i].context, idArtista = comentario[i].artista).first()
        if(artista == None):
            newArtista = Artistas()
            newArtista.email = email
            newArtista.contexto = comentario[i].context
            newArtista.idArtista = comentario[i].artista
            newArtista.nomeArtista = comentario[i].nomeArtista
            newArtista.likes = 1
            newArtista.pub_date = datetime.datetime.now()
            newArtista.save()
        else:
            artista.likes+=1   
            artista.save()     
    return 'sucesso'

@api.get('/avaliacoes')
def generos(request):
    artista = Artistas.objects.filter(email = 'willian@gmail.com').order_by('-likes').first()
    if(artista != None):
        return artista.idArtista
    else:
        return "None"


