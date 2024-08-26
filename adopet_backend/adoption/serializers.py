from rest_framework import serializers

from animal.serializers import AnimalSerializer
from user.serializers import UserSerializer
from .models import Adoption


class AdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = "__all__"


class AdoptionDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    animal = serializers.SerializerMethodField()

    class Meta:
        model = Adoption
        fields = ["id", "user", "animal"]

    def get_id(self, obj):
        return obj.id

    def get_user(self, obj):
        return UserSerializer(obj.adopter).data

    def get_animal(self, obj):
        return AnimalSerializer(obj.animal).data
