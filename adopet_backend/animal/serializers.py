"""
    Definição dos Serializers para a API de Animal.

    Serializers são responsáveis por serializar e desserializar os 
    objetos do Django para JSON e vice-versa.
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from .models import TemperamentAnimal, Animal


class TemperamentAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperamentAnimal
        fields = "__all__"


class AnimalSerializer(serializers.ModelSerializer):
    temperament = TemperamentAnimalSerializer(many=True, read_only=True)

    class Meta:
        model = Animal
        fields = "__all__"
