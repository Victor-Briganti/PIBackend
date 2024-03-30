from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework import routers


from . import views

router = routers.DefaultRouter()

router.register(r'create', views.ImageAnimalCreateView, basename='create_image')
router.register(r'', views.ImageAnimalListView, basename='list_image')
router.register(r'show', views.ImageAnimalDetailView, basename='detail_image')
router.register(r'delete', views.ImageAnimalDeleteView, basename='delete_image')
router.register(r'update', views.ImageAnimalUpdateView, basename='update_image')






urlpatterns = [
    # Endpoints para o animal.
    path('images/', include(router.urls), name='imageanimal_list'),
    path('images/<int:pk>', include(router.urls), name='imageanimal_detail'),
    path('images/', include(router.urls), name='imageanimal_create'),
    path('images/<int:pk>',include(router.urls), name='imageanimal_delete'),
    path('images/<int:pk>', include(router.urls), name='imageanimal_update'),
    path("byimage/<int:pk>", views.ImageAnimalFilterby.as_view(), name="image_by_animal"),
    path("", views.AnimalList.as_view(), name="animal_list"),
    path("<int:pk>", views.AnimalDetail.as_view(), name="animal_detail"),
    path("register/", views.AnimalRegister.as_view(), name="animal_register"),
    path("delete/<int:pk>", views.AnimalDelete.as_view(), name="animal_delete"),
    path("update/<int:pk>", views.AnimalUpdate.as_view(), name="animal_update"),
    
    # Endpoints para o temperamento do animal.
    path(
        "temperament/", views.TemperamentAnimalList.as_view(), name="temperament_list"
    ),
    path(
        "temperament/<int:pk>",
        views.TemperamentAnimalDetail.as_view(),
        name="temperament_detail",
    ),
    path(
        "temperament/register/",
        views.TemperamentAnimalRegister.as_view(),
        name="temperament_register",
    ),
    path(
        "temperament/delete/<int:pk>",
        views.TemperamentAnimalDelete.as_view(),
        name="temperament_delete",
    ),
    path(
        "temperament/update/<int:pk>",
        views.TemperamentAnimalUpdate.as_view(),
        name="temperament_update",
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
