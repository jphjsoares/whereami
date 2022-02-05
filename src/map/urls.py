from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="map-home"),
    # feature not working atm: path('createcustom', views.create_custom, name="create-custom"),
    path('createbyregion', views.create_by_region, name="create-by-region"),
    path('createworld', views.create_world, name="create-world"),
    path('report/<slug:image_key>/<int:reason_low_quality>/<int:reason_wrong_coordinates>/', views.report_image, name="report-image"),
    path('check_reported/<slug:image_key>', views.check_reported, name="check-reported")
]