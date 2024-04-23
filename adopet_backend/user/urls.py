from django.urls import path

from . import views

urlpatterns = [
    # Endpoints para o usuário.
    path("", views.UserDetail.as_view(), name="user_perfil"),
    path("register/", views.UserRegister.as_view(), name="user_register"),
    path("login/", views.UserLogin.as_view(), name="user_login"),
    path("logout/", views.UserLogout.as_view(), name="user_logout"),
    path("delete/", views.UserDelete.as_view(), name="user_delete"),
    path("update/", views.UserUpdate.as_view(), name="user_update"),
    # Endpoints para o adotante.
    path("adopter/register", views.AdopterRegister.as_view(), name="adopter_register"),
    path("adopter/", views.AdopterDetail.as_view(), name="adopter_detail"),
    path("adopter/list", views.AdopterList.as_view(), name="adopter_list"),
    path("adopter/update/", views.AdopterUpdate.as_view(), name="adopter_update"),
    path("adopter/delete/", views.AdopterDelete.as_view(), name="adopter_delete"),
]
