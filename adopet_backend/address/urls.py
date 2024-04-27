from django.urls import path
from . import views

urlpatterns = [
    # Endpoints para o usuário.
    path("", views.AddressList.as_view(), name="address_list"),
    path("register/", views.AddressRegister.as_view(), name="address_register"),
    path("state/", views.StateList.as_view(), name="state_list"),
    path("city/", views.CityList.as_view(), name="city_list"),
    path("city/register/", views.CityRegister.as_view(), name="city_register"),
]
