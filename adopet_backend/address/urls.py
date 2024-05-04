from django.urls import path
from . import views

urlpatterns = [
    # Endpoints para endereço.
    path("", views.AddressList.as_view(), name="address_list"),
    path("<int:pk>", views.AddressDetail.as_view(), name="address_detail"),
    path("register/", views.AddressRegister.as_view(), name="address_register"),
    path("state/", views.StateList.as_view(), name="state_list"),
    path("city/", views.CityList.as_view(), name="city_list"),
    path("city/<int:pk>", views.CityDetail.as_view(), name="city_detail"),
    path("city/register/", views.CityRegister.as_view(), name="city_register"),
]
