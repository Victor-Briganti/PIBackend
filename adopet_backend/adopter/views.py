from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User
from user.serializers import UserSerializer
from .models import Adopter
from .serializers import AdopterSerializer

# Create your views here.


class AdopterRegister(APIView):
    """
    Registra um adotante.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        serializer = AdopterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            adopter = serializer.save()
            if adopter:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdopterUpdate(APIView):
    """
    Atualiza um adotante.
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
            adopter = Adopter.objects.get(id=data["id"])
        except ObjectDoesNotExist:
            return Response(
                {"error": "Adotante não encontrado"}, status.HTTP_404_NOT_FOUND
            )

        serializer = AdopterSerializer(adopter, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            adopter = serializer.save()
            if adopter:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdopterDetail(APIView):
    """
    Retorna o adotante autenticado atual.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        # Access the user object making the request
        user = request.user

        try:
            adopter = Adopter.objects.get(user=user)
        except Adopter.DoesNotExist:
            return Response("Adotante não encontrado", status=status.HTTP_404_NOT_FOUND)

        return Response(
            {
                "cpf": adopter.cpf,
                "birth_date": adopter.birth_date,
                "phone": adopter.phone,
                "is_active": adopter.is_active,
                "user": adopter.user.id,
                "address": adopter.address.id,
            },
            status=status.HTTP_400_BAD_REQUEST,
        )
