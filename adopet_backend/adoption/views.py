from .models import Adoption
from .serializers import AdoptionSerializer
from animal.models import Animal
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User, UserMetadata
from user.serializers import UserMetadataSerializer

# Create your views here.


class AdoptionList(APIView):
    """
    Lista todas as adoções ligadas a esse usuário.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    pagination_class = PageNumberPagination()

    def get(self, request):
        user = request.user

        try:
            _ = UserMetadata.objects.get(user=user)
        except UserMetadata.DoesNotExist:
            return Response(
                "Usuário não foi propriamente cadastrado",
                status=status.HTTP_400_BAD_REQUEST,
            )

        adoption = Adoption.objects.filter(donor=user)
        serializer = AdoptionSerializer(adoption, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionDetail(APIView):
    """
    Retorna a adoção especifíca.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, pk):
        user = request.user

        try:
            _ = UserMetadata.objects.get(user=user)
        except UserMetadata.DoesNotExist:
            return Response(
                "Usuário não foi propriamente cadastrado",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            adoption = Adoption.objects.get(pk=pk)
        except Animal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AdoptionSerializer(adoption)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AdoptionRegister(APIView):
    """
    Registra uma adoção.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        user = request.user
        data = request.data

        try:
            _ = UserMetadata.objects.get(user=user)
        except UserMetadata.DoesNotExist:
            return Response(
                "Usuário não foi propriamente cadastrado",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            animal = Animal.objects.get(pk=data["animal"])
        except Animal.DoesNotExist:
            return Response(
                "Animal não encontrado", status=status.HTTP_404_NOT_FOUND
            )

        if animal.is_adopted:
            return Response(
                "Animal não está mais disponível para adoção",
                status=status.HTTP_400_BAD_REQUEST,
            )

        data["donor"] = user.id
        data["animal"] = animal.id
        serializer = AdoptionSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
   