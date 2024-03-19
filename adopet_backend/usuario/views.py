"""
Funções de acesso direto ao banco de dados para o modelo Usuário.
<https://docs.djangoproject.com/en/5.0/topics/db/>
<https://docs.djangoproject.com/en/5.0/topics/db/models/>
"""

from django.contrib.auth import login, logout
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import (
    UsuarioSerializer,
    UsuarioLoginSerializer,
    UsuarioSignupSerializer,
)

from .validation import (
    custom_validation,
    validate_email,
    validate_password,
)

# Create your views here.


class UsuarioSignup(APIView):
    # Define as permissões de acesso a essa API.
    # AllowAny: Qualquer usuário pode acessar.
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = custom_validation(request.data)
        serializer = UsuarioSignupSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            usuario = serializer.save()
            if usuario:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UsuarioLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    # Define o tipo de autenticação usado pela API.
    # SessionAuthentication: Autenticação por sessão.
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UsuarioLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.validated_data
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UsuarioLogout(APIView):
    # Define as permissões de acesso a essa API.
    # IsAuthenticated: Somente usuários autenticados podem acessar.
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UsuarioView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UsuarioSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
