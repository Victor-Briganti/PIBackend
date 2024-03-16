from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("sobre/", views.sobre, name="sobre"),
    path("contato/", views.contato, name="contato"),
    path("login/", views.login_page, name="login"),
    path("cadastro/", views.cadastro, name="cadastro"),
    # TODO: Excluir a página de sucesso
    path("sucesso/", views.sucesso, name="sucesso"),
]
