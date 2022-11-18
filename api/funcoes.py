from api.models import Intervalos, Usuarios, Artistas, Avaliacoes
from api.schemas.intervalos_schema import AvaliacoesSchema, IntervaloObject
import requests
from api.utils import convertGenreBanco, convertGenreSpotify 
import numpy as np
from typing import List

def getListasComIntervalos(email:str, usuario: Usuarios, token:str, context:str, genre1:str, genre2:str, genre3, popularidade:str, limite:str):
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

    if(intervalos1.danceability_min != None):
        url1 = "https://api.spotify.com/v1/recommendations?access_token="+token+"&seed_genres="+genreSpotify1+"&min_danceability="+str(intervalos1.danceability_min)+"&max_danceability="+str(intervalos1.danceability_max)+"&min_energy="+str(intervalos1.energy_min)+"&max_energy="+str(intervalos1.energy_max)+"&min_loudness="+str(intervalos1.loudness_min)+"&max_loudness="+str(intervalos1.loudness_max)+"&min_speechiness="+str(intervalos1.speechiness_min)+"&max_speechiness="+str(intervalos1.speechiness_max)+"&min_acousticness="+str(intervalos1.acoustic_min)+"&max_acousticness="+str(intervalos1.acoustic_max)+"&min_valence="+str(intervalos1.valence_min)+"&max_valence="+str(intervalos1.valence_max)+"&min_popularity="+str(popularidade)+"&limit="+str(limite)
    if(intervalos2.danceability_min != None):
        url2 = "https://api.spotify.com/v1/recommendations?access_token="+token+"&seed_genres="+genreSpotify2+"&min_danceability="+str(intervalos2.danceability_min)+"&max_danceability="+str(intervalos2.danceability_max)+"&min_energy="+str(intervalos2.energy_min)+"&max_energy="+str(intervalos2.energy_max)+"&min_loudness="+str(intervalos2.loudness_min)+"&max_loudness="+str(intervalos2.loudness_max)+"&min_speechiness="+str(intervalos2.speechiness_min)+"&max_speechiness="+str(intervalos2.speechiness_max)+"&min_acousticness="+str(intervalos2.acoustic_min)+"&max_acousticness="+str(intervalos2.acoustic_max)+"&min_valence="+str(intervalos2.valence_min)+"&max_valence="+str(intervalos2.valence_max)+"&min_popularity="+str(popularidade)+"&limit="+str(limite)
    if(intervalos3.danceability_min != None):
        url3 = "https://api.spotify.com/v1/recommendations?access_token="+token+"&seed_genres="+genreSpotify3+"&min_danceability="+str(intervalos3.danceability_min)+"&max_danceability="+str(intervalos3.danceability_max)+"&min_energy="+str(intervalos3.energy_min)+"&max_energy="+str(intervalos3.energy_max)+"&min_loudness="+str(intervalos3.loudness_min)+"&max_loudness="+str(intervalos3.loudness_max)+"&min_speechiness="+str(intervalos3.speechiness_min)+"&max_speechiness="+str(intervalos3.speechiness_max)+"&min_acousticness="+str(intervalos3.acoustic_min)+"&max_acousticness="+str(intervalos3.acoustic_max)+"&min_valence="+str(intervalos3.valence_min)+"&max_valence="+str(intervalos3.valence_max)+"&min_popularity="+str(popularidade)+"&limit="+str(limite)
    
    if(intervalos1.danceability_min == None):
        url1 = "https://api.spotify.com/v1/recommendations?access_token="+token+"&seed_genres="+genreSpotify1+"&min_popularity="+str(popularidade)+"&limit="+str(limite)
    if(intervalos2.danceability_min == None):
        url2 = "https://api.spotify.com/v1/recommendations?access_token="+token+"&seed_genres="+genreSpotify2+"&min_popularity="+str(popularidade)+"&limit="+str(limite)
    if(intervalos3.danceability_min == None):
        url3 = "https://api.spotify.com/v1/recommendations?access_token="+token+"&seed_genres="+genreSpotify3+"&min_popularity="+str(popularidade)+"&limit="+str(limite)
    
   

    lista1 = requests.get(url1).json()
    lista2 = requests.get(url2).json()
    lista3 = requests.get(url3).json()

    return (lista1, lista2, lista3)



def getListaArtistasPreferidos(artista, token, popularidade, limite):
    topArtistas = ""
    for i in range(len(artista)):
        if(i < 3):
            topArtistas += artista[i].idArtista + ","

    urlArtista = "https://api.spotify.com/v1/recommendations?access_token="+token+"&market=BR&seed_artists="+topArtistas+"&min_popularity="+str(popularidade)+"&limit="+str(limite)

    listaArtista = requests.get(urlArtista).json()
    return listaArtista

def getUnirListas(lista1, lista2, lista3, artista, token, popularidade, limite):
    if(artista.exists()):
        listaArtista = getListaArtistasPreferidos(artista, token, popularidade, limite)
        
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


def getIntervalosAvaliacoes(avaliacoes:List[Avaliacoes]):
    
    danceability = np.array([])
    energy = np.array([])
    loudness = np.array([])
    speechiness = np.array([])
    acousticness = np.array([])
    instrumentalness = np.array([])
    liveness = np.array([])
    valence = np.array([])


    for av in avaliacoes:
        danceability = np.append(danceability, av.danceability)
        energy = np.append(energy, av.energy)
        loudness = np.append(loudness, av.loudness)
        speechiness = np.append(speechiness, av.speechiness)
        acousticness = np.append(acousticness, av.acousticness)
        instrumentalness = np.append(instrumentalness, av.instrumentalness)
        liveness =  np.append(liveness, av.liveness)
        valence = np.append(valence, av.valence)

    quartil_min = .10
    quartil_max = .90
    intervalo = IntervaloObject(
        danceability_min = round(np.quantile(danceability, quartil_min), 2),
        danceability_max = round(np.quantile(danceability, quartil_max), 2),
        energy_min = round(np.quantile(energy, quartil_min), 2),
        energy_max = round(np.quantile(energy, quartil_max), 2),
        loudness_min = round(np.quantile(loudness, quartil_min), 2),
        loudness_max = round(np.quantile(loudness, quartil_max), 2),
        speechiness_min = round(np.quantile(speechiness, quartil_min), 2),
        speechiness_max = round(np.quantile(speechiness, quartil_max), 2),
        acousticness_min = round(np.quantile(acousticness, quartil_min), 2),
        acousticness_max = round(np.quantile(acousticness, quartil_max), 2),
        instrumentalness_min = round(np.quantile(instrumentalness, quartil_min), 2),
        instrumentalness_max = round(np.quantile(instrumentalness, quartil_max), 2),
        liveness_min = round(np.quantile(liveness, quartil_min), 2),
        liveness_max = round(np.quantile(liveness, quartil_max), 2),
        valence_min = round(np.quantile(valence, quartil_min), 2),
        valence_max = round(np.quantile(valence, quartil_max), 2),
    )
    
    return intervalo


def getListaIntervaloAprendido(intObject: IntervaloObject, artista, token, genre1, genre2, genre3, popularidade, limite):

    url = "https://api.spotify.com/v1/recommendations?access_token="+token+"&market=BR&seed_genres="+convertGenreSpotify(genre1)+","+convertGenreSpotify(genre2)+","+convertGenreSpotify(genre3)+"&min_danceability="+str(intObject.danceability_min)+"&max_danceability="+str(intObject.danceability_max)+"&min_energy="+str(intObject.energy_min)+"&max_energy="+str(intObject.energy_max)+"&min_loudness="+str(intObject.loudness_min)+"&max_loudness="+str(intObject.loudness_max)+"&min_speechiness="+str(intObject.speechiness_min)+"&max_speechiness="+str(intObject.speechiness_max)+"&min_acousticness="+str(intObject.acousticness_min)+"&max_acousticness="+str(intObject.acousticness_max)+"&min_valence="+str(intObject.valence_min)+"&max_valence="+str(intObject.valence_max)+"&min_popularity="+str(popularidade)+"&limit=10"
    listaAprendida = requests.get(url).json()

    if(artista.exists()):
        listaArtista = getListaArtistasPreferidos(artista, token, popularidade, limite)
        

        backLista1 = listaAprendida
        listaAprendida = listaArtista
        listaArtista = backLista1


        #ADICIONA A LISTA DE ARTISTAS NA LISTA APRENDIDA - SOMENTE SE TIVER ARTISTA PREFERIDO
        contador1:int = 0
        for item1 in listaArtista['tracks']:
            for item2 in listaAprendida['tracks']:
                if(item1['name'] == item2['name']):
                    contador1+=1
            if(contador1 == 0):
                listaAprendida['tracks'].append(item1)
            else:
                contador1=0


    return listaAprendida