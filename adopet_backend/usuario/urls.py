from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import UsuarioList, UsuarioDetail

urlpatterns = [
    path("", UsuarioList.as_view()),
    path("<str:email>", UsuarioDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
