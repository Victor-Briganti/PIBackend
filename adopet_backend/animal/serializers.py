"""
    Definição dos Serializers para a API de Animal.

    Serializers são responsáveis por serializar e desserializar os 
    objetos do Django para JSON e vice-versa.
"""

from rest_framework import serializers

from .models import ImageAnimal, Animal


class ImageAnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = ImageAnimal
        fields = "__all__"


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Animal
        fields = "__all__"


class ImageFilterbyAnimalSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField("get_image_url")

    class Meta:
        model = ImageAnimal
        fields = "__all__"

    def get_image_url(self, obj):
        return self.context["request"].build_absolute_uri(obj.image.url)
