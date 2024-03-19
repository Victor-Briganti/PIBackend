from django.urls import path

from . import views

urlpatterns = [
    path("", views.UsuarioView.as_view(), name="usuario_perfil"),
    path("signup/", views.UsuarioSignup.as_view(), name="usuario_signup"),
    path("login/", views.UsuarioLogin.as_view(), name="usuario_login"),
    path("logout/", views.UsuarioLogout.as_view(), name="usuario_logout"),
]
