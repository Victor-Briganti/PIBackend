from django.contrib import admin
from .models import Adopter, Adoption, AnimalRegister

# Register your models here.
admin.site.register(Adopter)
admin.site.register(Adoption)
admin.site.register(AnimalRegister)
