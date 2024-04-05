from django.shortcuts import render

# Create your views here.
from rest_framework import status, permissions, viewsets
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from django.shortcuts import redirect, get_object_or_404
from .models import Animal, ImageAnimal, TemperamentAnimal
from .serializers import (
    AnimalSerializer,
    ImageAnimalSerializer,
    TemperamentAnimalSerializer,
    ImageFilterbyAnimalSerializer,
)
from .validation import validate_temperament
# Create your views here.


class AnimalList(APIView):
    """
    Lista todos os animais disponíveis para adoção.
    Para isso é necessário verificar se o mesmo está ativo(is_active).
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        animals = Animal.objects.filter(is_active=True)
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
        # Dividi os dados do request em duas partes, uma para o animal e outra para o temperamento
        animal_data = {
            key: value for key, value in request.data.items() if key != "temperament"
        }
        temperament_data = validate_temperament(request.data["temperament"])

        # Verifica os temperamentos passados
        temperaments = []
        for temperament in temperament_data:
            try:
                temperaments.append(
                    TemperamentAnimal.objects.get(name=temperament["name"])
                )
            except TemperamentAnimal.DoesNotExist:
                return Response(
                    "Temperamento não encontrado", status=status.HTTP_404_NOT_FOUND
                )

        # Cria o animal e salva no banco de dados
        animal = Animal.objects.create(**animal_data)
        animal.save()

        # Adiciona os temperamentos ao animal
        animal.temperament.set(temperaments)

        serializer = AnimalSerializer(animal)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


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
        # Dividi os dados do request em duas partes, uma para o animal e outra para o temperamento
        animal_data = {
            key: value for key, value in request.data.items() if key != "temperament"
        }
        temperament_data = validate_temperament(request.data["temperament"])

        try:
            animal = Animal.objects.get(pk=pk, is_active=True)
        except Animal.DoesNotExist:
            return Response("Animal não encontrado", status=status.HTTP_404_NOT_FOUND)

        # Verifica os temperamentos passados
        temperaments = []
        for temperament in temperament_data:
            try:
                temperaments.append(
                    TemperamentAnimal.objects.get(name=temperament["name"])
                )
            except TemperamentAnimal.DoesNotExist:
                return Response(
                    "Temperamento não encontrado", status=status.HTTP_404_NOT_FOUND
                )

        # Insere os novos temperamentos passados
        animal.temperament.set(temperaments)

        serializer = AnimalSerializer(animal, data=animal_data, partial=True)
        if serializer.is_valid(raise_exception=True):
            animal = serializer.save()
            if animal:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemperamentAnimalList(APIView):
    """
    Lista todos os temperamentos disponíveis para um animal.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, request):
        temperaments = TemperamentAnimal.objects.all()
        serializer = TemperamentAnimalSerializer(temperaments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TemperamentAnimalDetail(APIView):
    """
    Retorna somente um temperamento específico.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, _, pk):
        try:
            temperament = TemperamentAnimal.objects.get(pk=pk)
        except TemperamentAnimal.DoesNotExist:
            return Response(
                "Temperamento não encontrado", status=status.HTTP_404_NOT_FOUND
            )
        serializer = TemperamentAnimalSerializer(temperament)
        return Response(serializer.data, status=status.HTTP_200_OK)


class TemperamentAnimalRegister(APIView):
    """
    Registra um novo temperamento que poderá ser usado pelos animais.
    Os valores válidos para temperamento são encontrados em "models.py"
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data
        serializer = TemperamentAnimalSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            temperament = serializer.save()
            if temperament:
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemperamentAnimalUpdate(APIView):
    """
    Atualiza o valor de um temperamento.
    Os valores válidos para temperamento são encontrados em "models.py"
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def put(self, request, pk):
        data = request.data
        try:
            temperament = TemperamentAnimal.objects.get(pk=pk)
        except TemperamentAnimal.DoesNotExist:
            return Response(
                "Temperamento não encontrado.", status=status.HTTP_404_NOT_FOUND
            )
        serializer = TemperamentAnimalSerializer(temperament, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            temperament = serializer.save()
            if temperament:
                return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TemperamentAnimalDelete(APIView):
    """
    Deleta um temperamento
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def delete(self, _, pk):
        temperament = TemperamentAnimal.objects.get(pk=pk)
        if temperament:
            temperament.delete()
            return Response(status=status.HTTP_200_OK)
        return Response(
            "Não foi possível excluir o temperamento. Verifique se o mesmo é válido.",
            status=status.HTTP_404_NOT_FOUND,
        )


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


class ImageAnimalRegister(APIView):
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
            image = serializer.save(animal=animal)
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