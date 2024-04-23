from django.contrib import admin

from .models import User, Address, Adopter

# Register your models here.

# Permite que o modelo User seja gerenciado pelo painel administrativo do Django
admin.site.register(User)
admin.site.register(Address)
admin.site.register(Adopter)
