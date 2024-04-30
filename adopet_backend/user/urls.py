from . import views
from django.urls import path

urlpatterns = [
    path("", views.UserDetail.as_view(), name="user_perfil"),
    path("register/", views.UserRegister.as_view(), name="user_register"),
    path("login/", views.UserLogin.as_view(), name="user_login"),
    path("logout/", views.UserLogout.as_view(), name="user_logout"),
    path("delete/", views.UserDelete.as_view(), name="user_delete"),
    path("update/", views.UserUpdate.as_view(), name="user_update"),
    path("metadata/", views.UserMetadataDetail.as_view(), name="usermeta_detail"),
    path(
        "metadata/register/",
        views.UserMetadataRegister.as_view(),
        name="usermeta_register",
    ),
    path(
        "metadata/update/", views.UserMetadataUpdate.as_view(), name="usermeta_update"
    ),
]
