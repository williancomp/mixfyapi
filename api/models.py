from django.db import models


# Create your models here.

class Intervalos(models.Model):
    context  = models.CharField(max_length=100)
    genre  = models.CharField(max_length=100)
    danceability_min = models.FloatField(null = True)
    danceability_max = models.FloatField(null = True)
    energy_min = models.FloatField(null = True)
    energy_max = models.FloatField(null = True)
    loudness_min = models.FloatField(null = True)
    loudness_max = models.FloatField(null = True)
    speechiness_min = models.FloatField(null = True)
    speechiness_max = models.FloatField(null = True)
    acoustic_min = models.FloatField(null = True)
    acoustic_max = models.FloatField(null = True)
    instrumentalness_min = models.FloatField(null = True)
    instrumentalness_max = models.FloatField(null = True)
    liveness_min = models.FloatField(null = True)
    liveness_max = models.FloatField(null = True)
    valence_min = models.FloatField(null = True)
    valence_max = models.FloatField(null = True)