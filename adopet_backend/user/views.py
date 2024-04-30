"""
Funções de acesso direto ao banco de dados para o modelo Usuário.
<https://docs.djangoproject.com/en/5.0/topics/db/>
<https://docs.djangoproject.com/en/5.0/topics/db/models/>
"""

from django.contrib.auth import login, logout
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, UserMetadata
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
    UserMetadataSerializer,
)
from .validation import (
    validate_user,
    validate_email,
    validate_password,
)

# Create your views here.


class UserRegister(APIView):
    """
    Registra um usuário comum na aplicação.
    """

    # Define as permissões de acesso a essa API.
    # AllowAny: Qualquer usuário pode acessar.
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

    def post(self, request):
        try:
            data = validate_user(request.data)
        except ValidationError as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)
        serializer = UserRegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    """
    Loga o usuário no sistema.
    Qualquer outra view que dependa de verificações de segurança
    depende desse endpoint sendo executado primeiro.
    """

    permission_classes = (permissions.AllowAny,)
    # Define o tipo de autenticação usado pela API.
    # SessionAuthentication: Autenticação por sessão.
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data

        try:
            validate_email(data)
            validate_password(data)
        except ValidationError as err:
            return Response(err, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = User.objects.get(email=serializer.data["email"])
            if user.is_active is False:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            user = serializer.validated_data
            login(request, user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    """
    Desloga o usuário.
    Remove a sessionid atual do usuário.
    """

    # Define as permissões de acesso a essa API.
    # IsAuthenticated: Somente usuários autenticados podem acessar.
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


class UserDelete(APIView):
    """
    Desativa o usuário do sistema.
    Nenhum endpoint de delete, realmente deleta o objeto do banco, apenas não o ativa.
    """

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
    """
    Atualiza as informações do usuário.
    Espera que todas as informações do usuário sejam
    passadas, não somente o que se deseja atualizar.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = UserSerializer

    def put(self, request):
        data = request.data

        try:
            user = User.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return Response(
                {"error": "Usuário não encontrado"}, status.HTTP_404_NOT_FOUND
            )

        if (user.id != request.user.id) and (not request.user.is_superuser):
            return Response(
                {"error": "Acesso Negado"}, status=status.HTTP_403_FORBIDDEN
            )

        serializer = UserSerializer(user, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            if user:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetail(APIView):
    """
    Retorna o usuário autenticado atual.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserMetadataRegister(APIView):
    """
    Registra metadados de um usuario.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = UserMetadataSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            adopter = serializer.save()
            if adopter:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMetadataUpdate(APIView):
    """
    Atualiza um metadado.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def put(self, request):
        data = request.data

        try:
            user = User.objects.get(id=data["user"]["id"])
        except ObjectDoesNotExist:
            return Response(
                {"error": "Usuário não encontrado"}, status.HTTP_404_NOT_FOUND
            )

        if (user.id != request.user.id) and (
            (not request.user.is_superuser) or (not request.user.is_staff)
        ):
            return Response(
                {"error": "Acesso Negado"}, status=status.HTTP_403_FORBIDDEN
            )

        try:
            adopter = UserMetadata.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return Response(
                {"error": "Este usuario não possui metadados"}, status.HTTP_404_NOT_FOUND
            )

        serializer = UserMetadataSerializer(adopter, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            adopter = serializer.save()
            if adopter:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMetadataDetail(APIView):
    """
    Retorna o metadado do usuario autenticado atual.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        # Access the user object making the request
        user = request.user

        try:
            adopter = UserMetadata.objects.get(user=user)
        except UserMetadata.DoesNotExist:
            return Response("Este usuario não possui metadados", status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "cpf": adopter.cpf,
                "birth_date": adopter.birth_date,
                "phone": adopter.phone,
                "is_active": adopter.is_active,
                "user": adopter.user.id,
                "address": adopter.address.id,
            },
            status=status.HTTP_400_BAD_REQUEST, # status.HTTP_200_OK ? 
        )
