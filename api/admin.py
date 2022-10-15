from django.contrib import admin
# Register your models here.
from .models import Intervalos

class IntervalosAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Intervalos._meta.fields]

admin.site.register(Intervalos, IntervalosAdmin)
