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
        data = request.data
        serializer = AnimalSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            animal = serializer.save()
            if animal:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

    def put(self, request):
        data = request.data

        try:
            animal = Animal.objects.get(pk=data["id"], is_active=True)
        except Animal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AnimalSerializer(animal, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            animal = serializer.save()
            if animal:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
