from rest_framework import serializers
from .models import Adoption


class AdoptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Adoption
        fields = "__all__"
