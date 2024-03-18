from django.urls import include, path
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

from .views import usuario_list, usuario_detail

urlpatterns = [
    path("", usuario_list),
    path("<str:email>", usuario_detail),
]

urlpatterns = format_suffix_patterns(urlpatterns)
