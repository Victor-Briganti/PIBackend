from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate

from .models import ImageAnimal, TemperamentAnimal, Animal


class ImageAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAnimal
        fields = "__all__"


class TemperamentAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemperamentAnimal
        fields = "__all__"


class AnimalSerializer(serializers.ModelSerializer):
    temperament = TemperamentAnimalSerializer(many=True, read_only=True)

    class Meta:
        model = Animal
        fields = "__all__"
