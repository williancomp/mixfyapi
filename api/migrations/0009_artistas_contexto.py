# Generated by Django 4.1.2 on 2022-11-05 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_artistas'),
    ]

    operations = [
        migrations.AddField(
            model_name='artistas',
            name='contexto',
            field=models.CharField(max_length=100, null=True),
        ),
    ]