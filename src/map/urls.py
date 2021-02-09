from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="map-home"),
    path('createcustom', views.create_custom, name="create-custom"),
    path('createbyregion', views.create_by_region, name="create-by-region"),
    path('createworld', views.create_world, name="create-world"),
    path('<int:id>/', views.get_map, name='get-map'),
]