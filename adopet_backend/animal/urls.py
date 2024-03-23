from django.urls import path

from . import views

urlpatterns = [
    path("", views.AnimalList.as_view(), name="animal_list"),
    path("<int:pk>", views.AnimalDetail.as_view(), name="animal_detail"),
    path("register/", views.AnimalRegister.as_view(), name="animal_register"),
    path("delete/<int:pk>", views.AnimalDelete.as_view(), name="animal_delete"),
    path("update/", views.AnimalUpdate.as_view(), name="animal_update"),
]
