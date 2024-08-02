# Create your views here.
from rest_framework import status, permissions, filters, generics
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserMetadata
from django.db import transaction

from .models import Animal, ImageAnimal
from .serializers import (
    AnimalSerializer,
    ImageAnimalSerializer,
    ImageFilterbyAnimalSerializer,
)


class AnimalList(APIView):
    """
    Lista todos os animais disponíveis para adoção.
    Para isso é necessário verificar se o mesmo está ativo(is_active).
    """

    permission_classes = (permissions.AllowAny,)
    pagination_class = PageNumberPagination()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = {
        "name",
        "description",
        "temperament",
        "specie",
        "age",
        "size",
        "coat",
        "weight",
        "gender",
        "donor__email",
    }
    ordering_fields = [
        "name",
        "specie",
        "age",
        "size",
        "weight",
        "adopted_date",
        "register_date",
        "is_house_trained",
        "is_special_needs",
        "is_vaccinated",
        "is_castrated",
    ]

    def get(self, request):
        animals = Animal.objects.filter(is_active=True)

        search_filter = filters.SearchFilter()
        ordering_filter = filters.OrderingFilter()

        animals = search_filter.filter_queryset(request, animals, self)
        animals = ordering_filter.filter_queryset(request, animals, self)

        # Adiciona paginação na requisição(se necessário)
        page = self.pagination_class.paginate_queryset(animals, request)
        if page is not None:
            serializer = AnimalSerializer(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)

        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimalDonorList(APIView):
    """
    Lista todos os animais cadastrados por um determinado usuário.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    pagination_class = PageNumberPagination()

    def get(self, request):
        user = self.request.user
        animals = Animal.objects.filter(is_active=True, donor=user)

        # Adiciona paginação na requisição(se necessário)
        page = self.pagination_class.paginate_queryset(animals, request)
        if page is not None:
            serializer = AnimalSerializer(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)

        serializer = AnimalSerializer(animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimalDetail(APIView):
    """
    Retorna um animal em especifíco.
    Para isso é necessário verificar se o mesmo está ativo(is_active).
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, _, pk):
        try:
            animal = Animal.objects.get(pk=pk, is_active=True)
        except Animal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AnimalRegister(APIView):
    """
    Registra um novo animal para adoção.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        # Acessa o usuário realizando a requisição
        user = request.user

        try:
            _ = UserMetadata.objects.get(user=user)
        except UserMetadata.DoesNotExist:
            return Response(
                "Usuário não foi propriamente cadastrado",
                status=status.HTTP_400_BAD_REQUEST,
            )

        request.data["donor"] = user.id
        request.data["is_active"] = False
        serializer = AnimalSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AnimalDelete(APIView):
    """
    Desativa o animal especificado.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def delete(self, _, pk):
        animal = Animal.objects.get(pk=pk)
        if animal:
            animal.is_active = False
            animal.save()
            return Response(status=status.HTTP_200_OK)
        return Response("Animal não encontrado", status=status.HTTP_404_NOT_FOUND)


class AnimalUpdate(APIView):
    """
    Atualiza os valores do animal especificado.
    Nessa chamada se espera que todos os valores antigos também sejam passados.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def put(self, request, pk):
        data = request.data

        try:
            animal = Animal.objects.get(pk=pk, is_active=True)
        except Animal.DoesNotExist:
            return Response("Animal não encontrado", status=status.HTTP_404_NOT_FOUND)

        serializer = AnimalSerializer(animal, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            animal = serializer.save()
            if animal:
                return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageAnimalList(APIView):
    """
    Lista todas as imagens de animais disponíveis.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        images = ImageAnimal.objects.all()
        serializer = ImageAnimalSerializer(
            images, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageAnimalDetail(APIView):
    """
    Retorna informações sobre a imagem especificada.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, _, pk):
        image = ImageAnimal.objects.get(pk=pk)
        if image:
            serializer = ImageAnimalSerializer(image)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Imagem não encontrada", status=status.HTTP_404_NOT_FOUND)


class ImageAnimalFilterby(APIView):
    """
    Retorna todas as imagens de um animal específico.
    """

    serializer_class = ImageFilterbyAnimalSerializer

    def get_queryset(self, pk):
        return ImageAnimal.objects.filter(animal=pk)

    def get(self, request, pk):
        queryset = self.get_queryset(pk)
        serializer = ImageFilterbyAnimalSerializer(
            queryset, many=True, context={"request": request}
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class ImageAnimalUpload(APIView):
    """
    Registra uma nova imagem para um animal.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = ImageAnimalSerializer

    def post(self, request):
        data = request.data
        animal_id = data["animal"]
        animal = Animal.objects.get(pk=animal_id)
        serializer = ImageAnimalSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            animal.is_active = True
            animal.save()
            serializer.save(animal=animal)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ImageAnimalUpdate(APIView):
    """
    Atualiza a imagem de um animal.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    serializer_class = ImageAnimalSerializer

    def retrieve(self, request, pk=None):
        image = ImageAnimal.objects.get(pk=pk)
        serializer = ImageAnimalSerializer(image, context={"request": request})
        return Response(serializer.data)

    def put(self, request, pk=None):
        data = request.data
        try:
            image = ImageAnimal.objects.get(pk=pk)
        except ImageAnimal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ImageAnimalSerializer(image, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            image = serializer.save()
            if image:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageAnimalDelete(APIView):
    """
    Deleta uma imagem de animal.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def delete(self, _, pk):
        image = ImageAnimal.objects.get(pk=pk)
        if image:
            image.delete()
            return Response(status=status.HTTP_200_OK)
        return Response("Imagem não encontrada", status=status.HTTP_404_NOT_FOUND)
