from django.urls import path

from . import views_donor

urlpatterns = [
    path("", views_donor.AdoptionDonorList.as_view(), name="adoption_donor_list"),
    path(
        "<int:pk>",
        views_donor.AdoptionDonorDetailById.as_view(),
        name="adoption_donor_detail_id",
    ),
    path(
        "animal/list/",
        views_donor.AdoptionDonorAnimalList.as_view(),
        name="adoption_donor_animal_list",
    ),
    path(
        "animal/<int:animal>",
        views_donor.AdoptionDonorDetailByAnimalId.as_view(),
        name="adoption_donor_detail_animalId",
    ),
    path(
        "update/<int:pk>",
        views_donor.AdoptionDonorUpdate.as_view(),
        name="adoption_donor_update",
    ),
    path(
        "delete/<int:pk>",
        views_donor.AdoptionDonorDelete.as_view(),
        name="adoption_donor_delete",
    ),
    path(
        "requests/",
        views_donor.AdoptionRequestList.as_view(),
        name="adoption_request_list",
    ),
    path(
        "request/<int:pk>",
        views_donor.AdoptionRequestDetailById.as_view(),
        name="adoption_request_detail",
    ),
    path(
        "request/accept/<int:pk>",
        views_donor.AdoptionRequestAccept.as_view(),
        name="adoption_request_accept",
    ),
    path(
        "request/reject/<int:pk>",
        views_donor.AdoptionRequestReject.as_view(),
        name="adoption_request_reject",
    ),
]
