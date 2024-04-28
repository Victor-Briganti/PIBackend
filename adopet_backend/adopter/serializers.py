from rest_framework import serializers
from .models import Adopter, Adoption, AnimalRegister


class AdopterSerializer(serializers.Serializer):
    class Meta:
        model = Adopter
        fields = "__all__"


class AnimalRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnimalRegister
        fields = "__all__"


class AdoptionSerializer(serializers.Serializer):
    class Meta:
        model = Adoption
        fields = "__all__"
