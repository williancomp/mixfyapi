
from gc import get_objects
import numpy as np
from ninja import NinjaAPI
from typing import List
from api.models import Intervalos, Usuarios, Avaliacoes
from api.schemas.intervalos_schema import GenreSchema, IntervalosSchema, UsuariosSchema, ComentarioSchema, AvaliacoesSchema, TrackSchema, Artistas, ArtistasSchema, IntervaloObject
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from river import datasets, tree, metrics
import datetime
import requests
from api.funcoes import getListasComIntervalos, getUnirListas, getIntervalosAvaliacoes, getListaIntervaloAprendido
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

    #VERIFICA SE O CONTEXTO VEIO, POIS O USUARIO PODE BUSCAR MÚSICAS SEM INFORMAR O CONTEXTO
    if(context != 'none'):
        
        #OBTEM A LISTA DE ARTISTAS PREFERIDOS
        listaArtistasPreferidos =  Artistas.objects.filter(email = email, contexto = context).order_by('-likes')

        #SE NAO TIVER AVALIAÇÕES SUFICIENTES DE UM CONTEXTO DE UM DETERMINADO USUARIO, 
        #ENTÃO, RECOMENDA MÚSICAS QUE CONSIDERAM OS INTERVALOS DO ESTUDO.
        avaliacoes = Avaliacoes.objects.filter(email = email, context = context).order_by('-pub_date')[:50]
        
        if(len(avaliacoes) < 50):

            #OBTEM 3 LISTAS DE MÚSICAS, CADA UMA DE UM GÊNERO DO USUARIO E SEU RESPECTIVO INTERVALO
            lista1, lista2, lista3 =  getListasComIntervalos(email, usuario, token, context, genre1, genre2, genre3, popularidade, limite)
            

            #FAZ A JUNÇÃO DAS LISTAS E REMOVE AS MÚSICAS DUPLICADAS
            listaFinal = getUnirListas(lista1, lista2, lista3, listaArtistasPreferidos, token, popularidade, limite)
            print("\n")
            print("RETORNANDO DO INTERVALO===")
            print("\n")
            return listaFinal

        #POSSUI AVALIAÇÕES SUFICIENTES, ENTÃO IDENTIFICA O INTERVALO A PARTIR DAS AVALIAÇÕES
        #DEPOIS UNI COM A LISTA DE ARTISTAS PREFERIDOS
        if(len(avaliacoes)>=50):

            #OBTEM INTERVALOS DE MIN E MAX APARTIR DAS AVALIACOES DO USUARIO
            intObject: IntervaloObject =  getIntervalosAvaliacoes(avaliacoes)

            #OBTEM LISTA DE MUSICAS COM INTERVALOS APRENDIDOS, CONSIDERANDO ARTISTAS E GÊNEROS PREFERIDOS
            listaFinal = getListaIntervaloAprendido(intObject, listaArtistasPreferidos, token, genre1, genre2, genre3, popularidade, limite)
            
            print("\n")
            print("RETORNANDO LISTA APRENDIDA===")
            print("\n")
            return listaFinal


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
        
        if(int(comentario[i].radio) > 1):
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




@api.post('/aprendizado/{email}/{context}')
def aprendizado(request, email: str, context:str, track:TrackSchema):
    
    # MODELO É CRIADO
    model = tree.HoeffdingTreeClassifier()

    # MÉTRICA CRIADA
    metric = metrics.ClassificationReport()


    
    avaliacoes = Avaliacoes.objects.filter(email = email, context = context)

    for avaliacao in avaliacoes:
        context = avaliacao.context
        danceability = avaliacao.danceability
        energy = avaliacao.energy
        loudness = avaliacao.loudness
        speechiness = avaliacao.speechiness
        acousticness = avaliacao.acousticness
        instrumentalness = avaliacao.instrumentalness
        liveness = avaliacao.liveness
        valence = avaliacao.valence
        x = {'context': context, 'danceability': danceability, 'energy': energy, 'loudness': loudness, 'speechiness': speechiness, 'acousticness': acousticness, 'instrumentalness': instrumentalness, 'liveness': liveness, 'valence': valence,}
        y = avaliacao.evaluation

        #VAI ALIMENTANDO O MODELO E ATUALIZANDO A MÉTRICA
        y_pred = model.predict_one(x)
        model.learn_one(x, y)
        if y_pred is not None:
            metric.update(y, y_pred)

    #MOSTRA A MÉTRICA
    print(metric)
    print("\n")



    #TESTAR VALOR RECEBIDO
    value = {'context': track.context, 'danceability': track.danceability, 'energy': track.energy, 'loudness': track.loudness, 'speechiness': track.speechiness, 'acousticness': track.acousticness, 'instrumentalness': track.instrumentalness, 'liveness': track.liveness, 'valence': track.valence,}

    proba_one = model.predict_proba_one(value)
    
    return proba_one


