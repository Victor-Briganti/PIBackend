from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserDetail.as_view(), name="user_perfil"),
    path("register/", views.UserRegister.as_view(), name="user_register"),
    path("login/", views.UserLogin.as_view(), name="user_login"),
    path("logout/", views.UserLogout.as_view(), name="user_logout"),
    path("delete/", views.UserDelete.as_view(), name="user_delete"),
    path("update/", views.UserUpdate.as_view(), name="user_update"),
]
