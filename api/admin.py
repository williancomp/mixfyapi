from django.contrib import admin
# Register your models here.
from .models import Intervalos, Usuarios

class IntervalosAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Intervalos._meta.fields]

class UsuariosAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Usuarios._meta.fields]

admin.site.register(Intervalos, IntervalosAdmin)
admin.site.register(Usuarios, UsuariosAdmin)
