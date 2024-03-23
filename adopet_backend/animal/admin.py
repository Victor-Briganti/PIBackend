from django.contrib import admin

from .models import Animal, TemperamentAnimal, ImageAnimal

# Register your models here.

admin.site.register(Animal)
admin.site.register(TemperamentAnimal)
admin.site.register(ImageAnimal)
