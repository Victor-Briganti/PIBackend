from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import State, City, Address
from .serializers import StateSerializer, CitySerializer, AddressSerializer

# Create your views here.


class StateList(APIView):
    """
    Lista todos os estados disponíveis.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, _):
        state = State.objects.all()
        serializer = StateSerializer(state, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityList(APIView):
    """
    Lista todas cidades disponíveis.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, _):
        city = City.objects.all()
        serializer = CitySerializer(city, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityDetail(APIView):
    """
    Retorna a cidade especificada.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, _, pk):
        try:
            city = City.objects.get(pk=pk)
        except City.DoesNotExists:
            return Response("Cidade não encontrada", status=status.HTTP_404_NOT_FOUND)

        serializer = CitySerializer(city)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CityRegister(APIView):
    """
    Registra uma nova cidade.
    Necessário passar um estado junto
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        serializer = CitySerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddressList(APIView):
    """
    Lista todos endereços.
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, _):
        address = Address.objects.all()
        serializer = AddressSerializer(address, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressDetail(APIView):
    """
    Retorna o endereço especifico
    """

    permission_classes = (permissions.AllowAny,)

    def get(self, _, pk):
        try:
            address = Address.objects.get(pk=pk)
        except Address.DoesNotExists:
            return Response("Endereço não encontrada", status=status.HTTP_404_NOT_FOUND)

        serializer = AddressSerializer(address)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AddressRegister(APIView):
    """
    Registra um novo endereço.
    Necessário passar uma cidade junto(que por sua vez precisa de um estado)
    """

    permission_classes = (permissions.AllowAny,)

    def post(self, request):
        if "user_data" not in request.session:
            return Response(
                {"error": "User registration step 1 not completed."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AddressSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            request.session["address_data"] = serializer.validated_data
            request.session.modified = True
            return Response(serializer.validated_data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
