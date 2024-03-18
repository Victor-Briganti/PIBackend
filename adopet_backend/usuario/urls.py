from django.urls import include, path
from rest_framework import routers

from .views import UsuarioViewSet

router = routers.DefaultRouter()
router.register("usuarios", UsuarioViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
]
