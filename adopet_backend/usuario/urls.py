from django.urls import include, path
from rest_framework import routers

from .views import usuario_list, usuario_detail

urlpatterns = [
    path("", usuario_list),
    path("<str:email>", usuario_detail),
]
