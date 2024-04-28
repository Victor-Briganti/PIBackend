from django.contrib import admin
from .models import User

# Register your models here.

# Permite que o modelo User seja gerenciado pelo painel administrativo do Django
admin.site.register(User)
