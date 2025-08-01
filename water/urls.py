from django.urls import path
from . import views


urlpatterns = [

    path('water/add/', views.water_add, name='water_add'),
    path('edit/<int:pk>/', views.water_edit, name='water_edit'),
    path("water/delete/<int:pk>/", views.water_delete, name="water_delete"),
    path("water/history/<int:pk>/", views.water_history, name="water_history"),
    path('water/', views.water_filter, name='water_result'),
    path('export/water/', views.water_export_excel, name='export_water'),
    path('location_autocomplete/', views.location_autocomplete, name='location_autocomplete'),
    path('owner_autocomplete/', views.owner_autocomplete, name='owner_autocomplete'),
    path('cadastr_autocomplete/', views.cadastr_autocomplete, name='cadastr_autocomplete'),

    ]