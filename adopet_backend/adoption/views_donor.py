from .pagination import DonationsDetailPagination
from .models import Adoption
from .serializers import AdoptionSerializer, AdoptionDetailSerializer
from animal.models import Animal
from rest_framework import status, permissions, filters
from rest_framework.authentication import SessionAuthentication
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from user.models import UserMetadata
from animal.serializers import AnimalSerializer
from django.utils import timezone
from user.views import UserSerializer
import threading
from .utils import send_adoption_email
# Create your views here.


class AdoptionDonorList(APIView):
    """
    Lista todas as doações ligadas a esse usuário.
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
        adoption = adoption.order_by("-response_date", "-request_date")
        serializer = AdoptionSerializer(adoption, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionDonorAnimalList(APIView):
    """
    Lista todas as doações aceitas de animais ligadas a esse usuário.
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

        adoptions = Adoption.objects.filter(donor=user, request_status="approved")
        unique_animal_ids = set()
        for adoption in adoptions:
            unique_animal_ids.add(adoption.animal_id)

        unique_animals = Animal.objects.filter(id__in=unique_animal_ids)
        unique_animals = unique_animals.order_by("-adoption_date")

        # Paginate the result
        page = self.pagination_class.paginate_queryset(unique_animals, request)
        if page is not None:
            serializer = AnimalSerializer(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)

        serializer = AnimalSerializer(unique_animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionRequestAnimalList(APIView):
    """
    Lista todas as doações pendentes de animais ligadas a esse usuário.
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

        adoptions = Adoption.objects.filter(donor=user, request_status="pending")
        adoptions = adoptions.order_by("-request_date")

        unique_animal_ids = set()
        for adoption in adoptions:
            unique_animal_ids.add(adoption.animal_id)

        unique_animals = Animal.objects.filter(
            id__in=unique_animal_ids, is_adopted=False, is_active=True
        )

        # Paginate the result
        page = self.pagination_class.paginate_queryset(unique_animals, request)
        if page is not None:
            serializer = AnimalSerializer(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)

        serializer = AnimalSerializer(unique_animals, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionRequestUserDetail(APIView):
    """
    Retorna um usuário específico que está solicitando um animal.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request, pk):
        # Requisita uma adoção pendente para o animal especificado
        try:
            adoption = Adoption.objects.get(pk=pk, request_status="pending")
            requesting_user = adoption.adopter
        except Adoption.DoesNotExist:
            return Response(
                {"detail": "Adoção não encontrada."}, status=status.HTTP_404_NOT_FOUND
            )

        # Serializa o usuário
        serializer = UserSerializer(requesting_user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionDonorDetailById(APIView):
    """
    Retorna a doação especifíca.
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


class AdoptionDonorDetailByAnimalId(APIView):
    """
    Retorna a doação especifíca.
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
            adoption = Adoption.objects.filter(animal=animal)
        except Animal.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AdoptionSerializer(adoption, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionDonorUpdate(APIView):
    """
    Atualiza uma doação.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def put(self, request, pk):
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
            adoption = Adoption.objects.get(pk=pk)
        except Adoption.DoesNotExist:
            return Response("Doação não encontrada", status=status.HTTP_404_NOT_FOUND)

        if adoption.donor != user:
            return Response(
                "Você não tem permissão para atualizar essa doação",
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = AdoptionSerializer(adoption, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdoptionDonorDelete(APIView):
    """
    Deleta uma doação.
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def delete(self, request, pk):
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
        except Adoption.DoesNotExist:
            return Response("Doação não encontrada", status=status.HTTP_404_NOT_FOUND)

        if adoption.donor != user:
            return Response(
                "Você não tem permissão para deletar essa doação",
                status=status.HTTP_403_FORBIDDEN,
            )

        adoption.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdoptionRequestList(APIView):
    """
    Lista todas as solicitações de adoção
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    pagination_class = PageNumberPagination()
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = [
        "request_status",
        "comments",
        "animal__name",
        "animal__specie",
        "animal__coat",
        "animal__size",
        "donor__email",
    ]
    ordering_fields = ["request_date", "response_date", "request_status"]

    def get(self, request):
        user = request.user

        search_filter = filters.SearchFilter()
        ordering_filter = filters.OrderingFilter()

        try:
            _ = UserMetadata.objects.get(user=user)
        except UserMetadata.DoesNotExist:
            return Response(
                "Usuário não foi propriamente cadastrado",
                status=status.HTTP_400_BAD_REQUEST,
            )

        adoptions = Adoption.objects.all()
        adoptions = search_filter.filter_queryset(request, adoptions, self)
        adoptions = ordering_filter.filter_queryset(request, adoptions, self)
        adoptions = adoptions.order_by("-response_date", "-request_date")
        serializer = AdoptionSerializer(adoptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionRequestDetail(APIView):
    """
    Retorna a solicitação de adoção de acordo com o id da própria solicitação
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)
    pagination_class = DonationsDetailPagination()

    def get(self, request):
        user = request.user

        try:
            _ = UserMetadata.objects.get(user=user)
        except UserMetadata.DoesNotExist:
            return Response(
                "Usuário não foi propriamente cadastrado",
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            adoptions = Adoption.objects.filter(donor=user, request_status="pending")
        except Adoption.DoesNotExist:
            return Response(
                "Solicitações de adoção não encontradas",
                status=status.HTTP_404_NOT_FOUND,
            )

        page = self.pagination_class.paginate_queryset(adoptions, request)
        if page is not None:
            serializer = AdoptionDetailSerializer(page, many=True)
            return self.pagination_class.get_paginated_response(serializer.data)

        serializer = AdoptionDetailSerializer(adoptions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionRequestDetailById(APIView):
    """
    Retorna a solicitação de adoção de acordo com o id da propria solicitacao
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
        except Adoption.DoesNotExist:
            return Response(
                "Solicitação de adoção não encontrada", status=status.HTTP_404_NOT_FOUND
            )

        serializer = AdoptionSerializer(adoption)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AdoptionRequestAccept(APIView):
    """
    Aceita a solicitação de adoção e rejeita as outras solicitações para o mesmo animal
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request, pk):
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
        except Adoption.DoesNotExist:
            return Response(
                "Solicitação de adoção não encontrada", status=status.HTTP_404_NOT_FOUND
            )

        if adoption.request_status != "pending" or adoption.animal.is_adopted:
            return Response(
                "Solicitação de adoção não está pendente",
                status=status.HTTP_400_BAD_REQUEST,
            )

        adoption.request_status = "approved"
        adoption.animal.is_adopted = True
        adoption.response_date = timezone.now()
        adoption.animal.adoption_date = timezone.now()
        adoption.save()
        adoption.animal.save()
        serializer = AdoptionSerializer(adoption)
        threading.Thread(target=send_adoption_email,
                         args = (adoption.adopter.email, f"Sua solicitação de adoção para o animal {adoption.animal.name} foi aceita.")).start()

        remains = Adoption.objects.filter(
            animal=adoption.animal, request_status="pending"
        )
        for remain in remains:
            remain.request_status = "rejected"
            remain.response_date = timezone.now()
            remain.save()
            
            threading.Thread(target=send_adoption_email,
                         args = (remain.adopter.email, f"Sua solicitação de adoção para o animal {remain.animal.name} foi rejeitada.")).start()

        return Response(serializer.data, status=status.HTTP_200_OK)
    



class AdoptionRequestReject(APIView):
    """
    Rejeita a solicitação de adoção
    """

    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request, pk):
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
        except Adoption.DoesNotExist:
            return Response(
                "Solicitação de adoção não encontrada", status=status.HTTP_404_NOT_FOUND
            )

        adoption.request_status = "rejected"
        adoption.response_date = timezone.now()
        adoption.save()
        threading.Thread(target=send_adoption_email,
                         args = (adoption.adopter.email, f"Sua solicitação de adoção para o animal {adoption.animal.name} foi rejeitada.")).start()
        serializer = AdoptionSerializer(adoption)
        return Response(serializer.data, status=status.HTTP_200_OK)
