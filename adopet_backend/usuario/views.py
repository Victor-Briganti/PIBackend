from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Usuario
from .serializers import UsuarioSerializer

# Create your views here.


@api_view(["GET", "POST"])
def usuario_list(request, format=None):
    """
    Lista todos os usuários ou cria um novo
    """
    if request.method == "GET":
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = UsuarioSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    return JsonResponse(serializer.errors, status=400)


@api_view(["GET", "PUT", "DELETE"])
def usuario_detail(request, email, format=None):
    """
    Retorna, atualiza ou deleta um usuário
    """
    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UsuarioSerializer(usuario)
        return Response(serializer.data)

    if request.method == "PUT":
        serializer = UsuarioSerializer(usuario, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        usuario.delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

    return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
