from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (
    MinValueValidator,
)  # Verificador usado para limitar valores negativos
from user.models import Adopter
# Create your models here.


class TemperamentAnimal(models.Model):
    """
    Representa o tipo de temperamento que um animal pode ter.
    Alguns temperamentos não devem ser usados juntos, para isso defina-os em
    "validation.py".
    """

    TEMPERAMENT_CHOICES = [
        ("affectionate", "Dengoso"),
        ("aggressive", "Agressivo"),
        ("calm", "Calmo"),
        ("energetic", "Energético"),
        ("friendly", "Amigável"),
        ("playful", "Brincalhão"),
        ("shy", "Arrisco"),
        ("sociable", "Sociável"),
        ("territorial", "Territorial"),
    ]

    # "choices" é o campo usado para definir os tipos que são permitidos para o campo.
    name = models.CharField(max_length=100, unique=True, choices=TEMPERAMENT_CHOICES)

    def __str__(self):
        return str(self.name)


class Animal(models.Model):
    """
    Representa um animal que pode ser adotado.
    """
    COAT_CHOICES = [
        ("short", "Curto"),
        ("medium", "Médio"),
        ("long", "Longo"),
    ]

    SPECIE_CHOICES = [
        ("dog", "Cachorro"),
        ("cat", "Gato"),
    ]

    SIZE_CHOICES = [
        ("small", "Pequeno porte"),
        ("medium", "Médio porte"),
        ("large", "Grande porte"),
    ]

    GENDER_CHOICES = [
        ("M", "Macho"),
        ("F", "Fêmea"),
    ]

    name = models.CharField(max_length=100)
    age = models.IntegerField(validators=[MinValueValidator(0)])
    specie = models.CharField(max_length=100, choices=SPECIE_CHOICES)
    gender = models.CharField(max_length=100, choices=GENDER_CHOICES)
    size = models.CharField(
        max_length=100,
        choices=SIZE_CHOICES,
        null=True,
        blank=True,
    )
    temperament = models.ManyToManyField(TemperamentAnimal, blank=True)
    coat = models.CharField(max_length=100, null=True, blank=True, choices=COAT_CHOICES)
    weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    adoption_date = models.DateTimeField(null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_house_trained = models.BooleanField()
    is_special_needs = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_adopted = models.ForeignKey(Adopter, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.name)


class ImageAnimal(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image/", default="")

    def __str__(self):
        return str(self.image)
