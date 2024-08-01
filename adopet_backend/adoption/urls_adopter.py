from django.urls import path
from . import views_adopter

urlpatterns = [
    path("", views_adopter.AdoptionList.as_view(), name="adoption_list"),
    path(
        "animals/",
        views_adopter.AdoptionAnimalsList.as_view(),
        name="adoption_animals_list",
    ),
    path(
        "<int:pk>",
        views_adopter.AdoptionDetailById.as_view(),
        name="adoption_detail_id",
    ),
    path(
        "animal/<int:animal>",
        views_adopter.AdoptionDetailByAnimalId.as_view(),
        name="adoption_detail_animalId",
    ),
    path(
        "adopter/<int:animal>",
        views_adopter.AdoptionDetailByAdopter.as_view(),
        name="adoption_detail_adopter",
    ),
    path(
        "register/", views_adopter.AdoptionRegister.as_view(), name="adoption_register"
    ),
]
