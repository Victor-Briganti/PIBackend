from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.parsers import JSONParser

from .models import Usuario
from .serializers import UsuarioSerializer

# Create your views here.


def usuario_list(request):
    """
    Lista todos os usuários ou cria um novo
    """
    if request.method == "GET":
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return JsonResponse(serializer.data, safe=False)

    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)

    return JsonResponse(serializer.errors, status=400)


def usuario_detail(request, email):
    """
    Retorna, atualiza ou deleta um usuário
    """
    try:
        usuario = Usuario.objects.get(email=email)
    except Usuario.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == "GET":
        serializer = UsuarioSerializer(usuario)
        return JsonResponse(serializer.data)

    if request.method == "PUT":
        data = JSONParser().parse(request)
        serializer = UsuarioSerializer(usuario, data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    elif request.method == "DELETE":
        usuario.delete()
        return HttpResponse(status=204)

    return JsonResponse(serializer.errors, status=400)
