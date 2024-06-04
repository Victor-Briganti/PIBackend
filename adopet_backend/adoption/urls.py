from django.urls import path
from . import views

urlpatterns = [
    path("", views.AdoptionList.as_view(), name="adoption_list"),
    path("<int:pk>", views.AdoptionDetailById.as_view(), name="adoption_detail_id"),
    path(
        "animal/<int:animal>",
        views.AdoptionDetailByAnimalId.as_view(),
        name="adoption_detail_animalId",
    ),
    path("register/", views.AdoptionRegister.as_view(), name="adoption_register"),
    path("update/<int:pk>", views.AdoptionUpdate.as_view(), name="adoption_update"),
    path("delete/<int:pk>", views.AdoptionDelete.as_view(), name="adoption_delete"),
]
