from django.urls import path
from . import views

urlpatterns = [
    path("", views.AdoptionList.as_view(), name="adoption_list"),
    path("<int:pk>", views.AdoptionDetail.as_view(), name="adoption_detail"),
    path("register/", views.AdoptionRegister.as_view(), name="adoption_register"),
    path("update/<int:pk>", views.AdoptionUpdate.as_view(), name="adoption_update"),
    path("delete/<int:pk>", views.AdoptionDelete.as_view(), name="adoption_delete"),
]