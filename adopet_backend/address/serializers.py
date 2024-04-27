"""
    Definição dos Serializers para a API de Endereços.

    Serializers são responsáveis por serializar e desserializar os
    objetos do Django para JSON e vice-versa.
"""

from rest_framework import serializers
from .models import State, City, Address


class StateSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ["uf"]

    def create(self, validated_data):
        uf = validated_data.get("uf")

        # Verifica se o estado já existe
        state_instance = State.objects.filter(uf=uf).first()
        if state_instance:
            return state_instance

        # Caso contrário crie-o.
        return super().create(validated_data)


class CitySerializer(serializers.ModelSerializer):
    state = StateSerializer()

    class Meta:
        model = City
        fields = "__all__"

    def create(self, validated_data):
        # Cria uma nova cidade e um estado associado.
        state_data = validated_data.pop("state")
        state = State.objects.get_or_create(**state_data)
        city = City.objects.create(state=state, **validated_data)
        return city


class AddressSerializer(serializers.ModelSerializer):
    city = CitySerializer()

    class Meta:
        model = Address
        fields = "__all__"

    def create(self, validated_data):
        # Extract city data
        city_data = validated_data.pop("city")

        # Create or retrieve the associated state instance
        state_data = city_data.pop("state")
        state_instance, _ = State.objects.get_or_create(**state_data)

        # Create or retrieve the associated city instance
        city_instance, _ = City.objects.get_or_create(state=state_instance, **city_data)

        # Create the address instance
        address = Address.objects.create(city=city_instance, **validated_data)
        return address
