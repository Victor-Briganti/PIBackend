from django.urls import path
from . import views

urlpatterns = [
    path("", views.AdopterDetail.as_view(), name="adopter_detail"),
    path("register/", views.AdopterRegister.as_view(), name="adopter_register"),
    path("update/", views.AdopterUpdate.as_view(), name="adopter_update"),
]
