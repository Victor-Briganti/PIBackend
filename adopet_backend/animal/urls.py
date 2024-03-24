from django.urls import path

from . import views

urlpatterns = [
    path("", views.AnimalList.as_view(), name="animal_list"),
    path("<int:pk>", views.AnimalDetail.as_view(), name="animal_detail"),
    path("register/", views.AnimalRegister.as_view(), name="animal_register"),
    path("delete/<int:pk>", views.AnimalDelete.as_view(), name="animal_delete"),
    path("update/", views.AnimalUpdate.as_view(), name="animal_update"),
    path(
        "temperament/", views.TemperamentAnimalList.as_view(), name="temperament_list"
    ),
    path(
        "temperament/<int:pk>",
        views.TemperamentAnimalDetail.as_view(),
        name="temperament_detail",
    ),
    path(
        "temperament/create/",
        views.TemperamentAnimalCreate.as_view(),
        name="temperament_create",
    ),
    path(
        "temperament/delete/<int:pk>",
        views.TemperamentAnimalDelete.as_view(),
        name="temperament_delete",
    ),
    path(
        "temperament/update/",
        views.TemperamentAnimalUpdate.as_view(),
        name="temperament_update",
    ),
]
