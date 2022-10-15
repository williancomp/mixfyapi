# Generated by Django 4.1.2 on 2022-10-15 01:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254)),
                ('genre1', models.CharField(max_length=100)),
                ('genre2', models.CharField(max_length=100)),
                ('genre3', models.CharField(max_length=100)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
