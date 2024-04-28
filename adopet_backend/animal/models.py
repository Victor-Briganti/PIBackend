from django.db import models

# Verificador usado para limitar valores negativos
from django.core.validators import (
    MinValueValidator,
)

# Create your models here.


class Animal(models.Model):
    """
    Representa um animal que pode ser adotado.
    """

    AGE_CHOICES = [
        ("puppy", "Filhote"),
        ("adult", "Adulto"),
        ("old", "Idoso"),
    ]

    COAT_CHOICES = [
        ("short", "Curto"),
        ("medium", "Médio"),
        ("long", "Longo"),
    ]

    GENDER_CHOICES = [
        ("M", "Macho"),
        ("F", "Fêmea"),
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

    name = models.CharField(max_length=100)
    age = models.CharField(choices=AGE_CHOICES)
    specie = models.CharField(choices=SPECIE_CHOICES)
    gender = models.CharField(choices=GENDER_CHOICES)
    size = models.CharField(
        max_length=100,
        choices=SIZE_CHOICES,
        null=True,
        blank=True,
    )
    temperament = models.CharField(null=True, blank=True)
    coat = models.CharField(null=True, blank=True, choices=COAT_CHOICES)
    weight = models.FloatField(null=True, blank=True, validators=[MinValueValidator(0)])
    adoption_date = models.DateTimeField(null=True, blank=True)
    register_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    is_house_trained = models.BooleanField()
    is_special_needs = models.BooleanField()
    is_active = models.BooleanField(default=True)
    is_vaccinated = models.BooleanField()
    is_castrated = models.BooleanField()
    is_adopted = models.BooleanField()

    def __str__(self):
        return str(self.name)


class ImageAnimal(models.Model):
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="image/animals/", default="")

    def __str__(self):
        return str(self.image)
