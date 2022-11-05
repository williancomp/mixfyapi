# Generated by Django 4.1.2 on 2022-11-05 11:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_avaliacoes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Artistas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.CharField(max_length=100)),
                ('idArtista', models.CharField(max_length=100)),
                ('likes', models.IntegerField(default=0)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
