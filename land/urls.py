from django.urls import path
from . import views
from .views import weather_view
from .views import map_view
from .views import landplots_geojson

urlpatterns = [
    path('', views.index, name='home'),
    path('zem_lease/', views.zem_lease, name='zem_lease'),
    path('zem_lease/land', views.all_land, name='land'),
    path('export/landplots/land_export', views.land_export, name='land_export'),
    path('zem_lease/freeland', views.freeland, name='freeland'),
    path('zem_lease/auction', views.auction, name='auction'),
    path('zem_lease/permanent_land', views.permanent_land, name='permanent_land'),
    path('zem_lease/water', views.water, name='water'),
    path('zem_lease/add/', views.zem_leave_add, name='zem_lease_add'),
    path('zem_lease/edit/<int:pk>/', views.zem_lease_edit, name='zem_lease_edit'),
    path('zem_lease/delete/<int:pk>/', views.zem_lease_delete, name='zem_lease_delete'),
    path('zem_lease/history/<int:pk>/', views.zem_lease_history, name='zem_lease_history'),
    path('import/landplots/', views.import_excel, name='import_landplots_excel'),
    path('owner_autocomplete/', views.owner_autocomplete, name='owner_autocomplete'),
    path('location_autocomplete/', views.location_autocomplete, name='location_autocomplete'),
    path('cadastr_autocomplete/', views.cadastr_autocomplete, name='cadastr_autocomplete'),
    path('zem_lease/filter', views.zem_lease_filter, name='zem_lease_result'),
    path('weather/', weather_view, name='weather'),
    path('map/', map_view, name='map'),
    path('landplots/geojson/', landplots_geojson, name='landplots_geojson'),
    path('api/search_landplot/', views.search_landplot, name='search_landplot'),
    path('api/status_layer/', views.status_layer_view, name='status_layer'),
    path('api/category_layer/', views.category_layer_view, name='category_layer'),
    path('api/land/<str:cadastr>/', views.land_coords, name='land_coords'),
]