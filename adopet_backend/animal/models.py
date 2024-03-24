from django.db import models
from django.core.exceptions import ValidationError


# Create your models here.


def validate_file_size(value):
    filesize = value.size
    max_file_size = 1024000
    if filesize > max_file_size:
        raise ValidationError("O tamanho máximo de upload de imagem é 1MB")
    else:
        return value


class ImageAnimal(models.Model):
    image = models.ImageField(upload_to="image/", default="media/image/default_cat.jpg")
    is_default = models.BooleanField(default=False, validators=[validate_file_size])

    def __str__(self):
        return str(self.image)


class TemperamentAnimal(models.Model):
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

    name = models.CharField(max_length=100, unique=True, choices=TEMPERAMENT_CHOICES)

    def __str__(self):
        return str(self.name)


class Animal(models.Model):
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
    age = models.IntegerField(null=True, blank=True)
    specie = models.CharField(max_length=100, choices=SPECIE_CHOICES)
    genre = models.CharField(max_length=100, choices=GENDER_CHOICES)
    size = models.CharField(max_length=100, choices=SIZE_CHOICES, null=True, blank=True)
    temperament = models.ManyToManyField(TemperamentAnimal, blank=True)
    coat = models.CharField(max_length=100)
    weight = models.FloatField(null=True, blank=True)
    adoption_date = models.DateTimeField(null=True, blank=True)
    description = models.TextField()
    is_house_trained = models.BooleanField()
    is_special_needs = models.BooleanField()
    is_active = models.BooleanField(default=True)
    image = models.ForeignKey(
        ImageAnimal, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self):
        return str(self.name)
