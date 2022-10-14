from django.contrib import admin
# Register your models here.
from .models import Intervalos

class IntervalosAdmin(admin.ModelAdmin):
    list_disply = ['id', 'context', 'genre']

admin.site.register(Intervalos, IntervalosAdmin)
