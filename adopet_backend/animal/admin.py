from django.contrib import admin

from .models import Animal, TemperamentAnimal

# Register your models here.

# Modelos registradors aqui podem ser cadastros no painel de administração do Django.
admin.site.register(Animal)
admin.site.register(TemperamentAnimal)
