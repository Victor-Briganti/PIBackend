from django.urls import path

from .views import UsuarioAPIView, EnderecoAPIView

urlpatterns = [
    path("usuario/", UsuarioAPIView.as_view()),
    path("endereco/", EnderecoAPIView.as_view()),
]
