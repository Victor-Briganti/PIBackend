from django.urls import path
from . import views_requests

urlpatterns = [
    path("", views_requests.AdoptionRequestList.as_view(), name="adoption_list"),
    path(
        "<int:pk>",
        views_requests.AdoptionRequestDetailById.as_view(),
        name="adoption_detail_id",
    ),
    path(
        "accept/<int:pk>",
        views_requests.AdoptionRequestAccept.as_view(),
        name="adoption_accept",
        
        
    ),
    
]