# Generated by Django 4.1.2 on 2022-11-05 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_artistas_contexto'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistas',
            name='nomeArtista',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
