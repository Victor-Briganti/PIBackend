from django.urls import path

from .views import UsuarioAPIView, EnderecoAPIView

urlpatterns = [
    path("usuario/", UsuarioAPIView.as_view()),
    path("endereco/", EnderecoAPIView.as_view()),
    path("usuario/<str:cpf>", UsuarioAPIView.as_view()),
    path("endereco/<int:endereco_id>", EnderecoAPIView.as_view()),

]
