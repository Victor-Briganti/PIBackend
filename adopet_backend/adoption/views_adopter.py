from .models import Adoption
from .serializers import AdoptionSerializer
from animal.models import Animal
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserMetadata
from animal.serializers import AnimalSerializer

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

        adoption = Adoption.objects.filter(adopter=user)
        adoption = adoption.order_by("-response_date","-request_date")
        serializer = AdoptionSerializer(adoption, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionAnimalsList(APIView):
    """
    Lista todos os animais associados às adoções do usuário.
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

        # Requisita uma lista e usuários que realizaram adoções que foram aceitas
        adoptions = Adoption.objects.filter(adopter=user, request_status="approved")
        # Retorna o ID dos animais
        unique_animal_ids = set(adoption.animal_id for adoption in adoptions)

        # Busca os animais baseado em seus IDs
        
        unique_animals = Animal.objects.filter(id__in=unique_animal_ids)
        unique_animals = unique_animals.order_by("-adoption_date")

        # Coloca os resultado em paginação
        page = self.pagination_class.paginate_queryset(unique_animals, request)
        if page is not None:
            serializer = AnimalSerializer(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)

        serializer = AnimalSerializer(unique_animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionDetailById(APIView):
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


class AdoptionDetailByAnimalId(APIView):
    """
    Retorna a adoção especifíca.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, animal):
        user = request.user

        try:
            _ = UserMetadata.objects.get(user=user)
        except UserMetadata.DoesNotExist:
            return Response(
                "Usuário não foi propriamente cadastrado",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            adoption = Adoption.objects.get(animal=animal)
        except Animal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AdoptionSerializer(adoption)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionDetailByAdopter(APIView):
    """
    Retorna a adoção especifíca.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, animal):
        user = request.user

        try:
            _ = UserMetadata.objects.get(user=user)
        except UserMetadata.DoesNotExist:
            return Response(
                "Usuário não foi propriamente cadastrado",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            adoption = Adoption.objects.get(animal=animal, adopter=user)
        except Adoption.DoesNotExist:
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
            return Response("Animal não encontrado", status=status.HTTP_404_NOT_FOUND)

        if animal.is_adopted:
            return Response(
                "Animal não está mais disponível para adoção",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            Adoption.objects.get(animal=data["animal"], adopter=user)
            return Response(
                "Requisição já realizada", status=status.HTTP_400_BAD_REQUEST
            )
        except Adoption.DoesNotExist:
            serializer = AdoptionSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
