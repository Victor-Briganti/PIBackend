from django.shortcuts import get_object_or_404
from rest_framework import generics

from .models import Usuario
from .serializers import UsuarioSerializer

# Create your views here.


class UsuarioList(generics.ListCreateAPIView):
    """
    Lista todos os usuários ou cria um novo
    """

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer


class UsuarioDetail(generics.RetrieveUpdateDestroyAPIView):
    """
    Retorna, atualiza uo deleta um usuário
    """

    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    lookup_field = "email"

    # Alterado o método get_object para buscar o usuário pelo email ao invés da chave primária
    def get_object(self):
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, email=self.kwargs["email"])
        return obj
