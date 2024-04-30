from . import views
from django.urls import path
from rest_framework import routers

router = routers.DefaultRouter()

urlpatterns = [
    # Endpoints para o animal.
    path("", views.AnimalList.as_view(), name="animal_list"),
    path("<int:pk>", views.AnimalDetail.as_view(), name="animal_detail"),
    path("register/", views.AnimalRegister.as_view(), name="animal_register"),
    path("delete/<int:pk>", views.AnimalDelete.as_view(), name="animal_delete"),
    path("update/<int:pk>", views.AnimalUpdate.as_view(), name="animal_update"),
    path("choices/", views.AnimalChoices.as_view(), name="animal_choices"),
    # Endpoints para as imagens
    path("images/", views.ImageAnimalList.as_view(), name="imageanimal_list"),
    path(
        "images/<int:pk>", views.ImageAnimalDetail.as_view(), name="imageanimal_detail"
    ),
    path(
        "images/upload/",
        views.ImageAnimalUpload.as_view(),
        name="imageanimal_upload",
    ),
    path(
        "images/delete/<int:pk>",
        views.ImageAnimalDelete.as_view(),
        name="imageanimal_delete",
    ),
    path(
        "images/update/<int:pk>",
        views.ImageAnimalUpdate.as_view(),
        name="imageanimal_update",
    ),
    path(
        "images/filterby/<int:pk>",
        views.ImageAnimalFilterby.as_view(),
        name="imageanimal_filterby",
    ),
]
