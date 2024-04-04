from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


from . import views

router = routers.DefaultRouter()

urlpatterns = [
    # Endpoints para o animal.
    path("", views.AnimalList.as_view(), name="animal_list"),
    path("<int:pk>", views.AnimalDetail.as_view(), name="animal_detail"),
    path("register/", views.AnimalRegister.as_view(), name="animal_register"),
    path("delete/<int:pk>", views.AnimalDelete.as_view(), name="animal_delete"),
    path("update/<int:pk>", views.AnimalUpdate.as_view(), name="animal_update"),
    # Endpoints para o temperamento do animal.
    path(
        "temperament/", views.TemperamentAnimalList.as_view(), name="temperament_list"
    ),
    path(
        "temperament/<int:pk>",
        views.TemperamentAnimalDetail.as_view(),
        name="temperament_detail",
    ),
    path(
        "temperament/register/",
        views.TemperamentAnimalRegister.as_view(),
        name="temperament_register",
    ),
    path(
        "temperament/delete/<int:pk>",
        views.TemperamentAnimalDelete.as_view(),
        name="temperament_delete",
    ),
    path(
        "temperament/update/<int:pk>",
        views.TemperamentAnimalUpdate.as_view(),
        name="temperament_update",
    ),
    # Endpoints para as imagens
    path("images/", views.ImageAnimalList.as_view(), name="imageanimal_list"),
    path(
        "images/<int:pk>", views.ImageAnimalDetail.as_view(), name="imageanimal_detail"
    ),
    path(
        "images/register/",
        views.ImageAnimalRegister.as_view(),
        name="imageanimal_register",
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
