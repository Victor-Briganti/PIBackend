from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("create/", views.create_view, name="create"),,
    path("sobre/", views.sobre, name="sobre"),
    path("contato/", views.contato, name="contato"),
]
