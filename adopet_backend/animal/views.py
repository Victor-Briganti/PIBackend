from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Animal, ImageAnimal, TemperamentAnimal
from .serializers import (
    AnimalSerializer,
    ImageAnimalSerializer,
    TemperamentAnimalSerializer,
)
from .validation import validate_temperament

# Create your views here.


class AnimalList(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        animals = Animal.objects.filter(is_active=True)
        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimalDetail(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk):
        try:
            animal = Animal.objects.get(pk=pk, is_active=True)
        except Animal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimalRegister(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        animal_data = {
            key: value for key, value in request.data.items() if key != "temperament"
        }
        temperament_data = validate_temperament(request.data["temperament"])

        # Create the Animal instance without assigning the temperament field
        animal = Animal.objects.create(**animal_data)

        animal.save()

        temperaments = []
        for temperament in temperament_data:
            temperaments.append(TemperamentAnimal.objects.get(name=temperament["name"]))

        animal.temperament.set(temperaments)

        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnimalDelete(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def delete(self, request, pk):
        animal = Animal.objects.get(pk=pk)
        if animal:
            animal.is_active = False
            animal.save()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AnimalUpdate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def put(self, request, pk):
        animal_data = {
            key: value for key, value in request.data.items() if key != "temperament"
        }
        temperament_data = validate_temperament(request.data["temperament"])

        try:
            animal = Animal.objects.get(pk=pk, is_active=True)
        except Animal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        temperaments = []
        for temperament in temperament_data:
            temperaments.append(TemperamentAnimal.objects.get(name=temperament["name"]))

        animal.temperament.set(temperaments)

        serializer = AnimalSerializer(animal, data=animal_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            animal = serializer.save()
            if animal:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemperamentAnimalList(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        temperaments = TemperamentAnimal.objects.all()
        serializer = TemperamentAnimalSerializer(temperaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TemperamentAnimalDetail(APIView):
    permission_classes = (permissions.AllowAny,)

    def get(self, request, pk):
        try:
            temperament = TemperamentAnimal.objects.get(pk=pk)
        except TemperamentAnimal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TemperamentAnimalSerializer(temperament)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TemperamentAnimalCreate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        serializer = TemperamentAnimalSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            temperament = serializer.save()
            if temperament:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemperamentAnimalUpdate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def put(self, request, pk):
        data = request.data
        try:
            temperament = TemperamentAnimal.objects.get(pk=pk)
        except TemperamentAnimal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = TemperamentAnimalSerializer(temperament, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            temperament = serializer.save()
            if temperament:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemperamentAnimalDelete(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def delete(self, request, pk):
        temperament = TemperamentAnimal.objects.get(pk=pk)
        if temperament:
            temperament.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
