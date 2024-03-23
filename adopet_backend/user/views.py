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

from .models import User
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)
from .validation import (
    user_validation,
    validate_email,
    validate_password,
)

# Create your views here.


class UserRegister(APIView):
    # Define as permissões de acesso a essa API.
    # AllowAny: Qualquer usuário pode acessar.
    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        data = user_validation(request.data)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    # Define o tipo de autenticação usado pela API.
    # SessionAuthentication: Autenticação por sessão.
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        assert validate_email(data)
        assert validate_password(data)
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.data["email"])
            if user.is_active is False:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user = serializer.validated_data
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)


class UserLogout(APIView):
    # Define as permissões de acesso a essa API.
    # IsAuthenticated: Somente usuários autenticados podem acessar.
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserDelete(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def delete(self, request):
        serializer = UserSerializer(request.user)
        user = User.objects.get(id=serializer.data["id"])
        user.is_active = False
        user.save()
        logout(request)
        return Response(user.is_active, status=status.HTTP_200_OK)


class UserUpdate(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def put(self, request):
        data = request.data
        user = User.objects.get(id=data["id"])
        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
