from django.db import models


# Create your models here.

class Intervalos(models.Model):
    context  = models.CharField(max_length=100)
    genre  = models.CharField(max_length=100)
    danceability_min = models.FloatField()
    danceability_max = models.FloatField()
    energy_min = models.FloatField()
    energy_max = models.FloatField()
    loudness_min = models.FloatField()
    loudness_max = models.FloatField()
    speechiness_min = models.FloatField()
    speechiness_max = models.FloatField()
    acoustic_min = models.FloatField()
    acoustic_max = models.FloatField()
    instrumentalness_min = models.FloatField()
    instrumentalness_max = models.FloatField()
    liveness_min = models.FloatField()
    liveness_max = models.FloatField()
    valence_min = models.FloatField()
    valence_max = models.FloatField()
    pub_date = models.DateTimeField('date published')