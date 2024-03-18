from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .serializer import UsuarioSerializer, EnderecoSerializer
from .models import Usuario, Endereco

# Create your views here.


class UsuarioAPIView(APIView):
    def get(self, request, cpf=None):
        if cpf:
            usuario = Usuario.objects.get(cpf=cpf)
            serializer = UsuarioSerializer(usuario)
            return Response(serializer.data, status=status.HTTP_200_OK)

        usuarios = Usuario.objects.all()
        serializer = UsuarioSerializer(usuarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class EnderecoAPIView(APIView):
    def get(self, request, endereco_id=None):
        if endereco_id:
            endereco = Endereco.objects.get(id=endereco_id)
            serializer = EnderecoSerializer(endereco)
            return Response(serializer.data, status=status.HTTP_200_OK)

        enderecos = Endereco.objects.all()
        serializer = EnderecoSerializer(enderecos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
