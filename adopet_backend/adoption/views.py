from .models import Adoption
from .serializers import AdoptionSerializer
from animal.models import Animal
from rest_framework import status, permissions
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import User, UserMetadata

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
            adoption = Adoption.objects.get(pk=pk, is_active=True)
        except Animal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AdoptionSerializer(adoption)
        return Response(serializer.data, status=status.HTTP_200_OK)
