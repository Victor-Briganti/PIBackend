from django.contrib import admin

from .models import Usuario

# Register your models here.

# Permite que o modelo Usuario seja gerenciado pelo painel administrativo do Django
admin.site.register(Usuario)
