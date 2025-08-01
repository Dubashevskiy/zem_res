import django_filters
from .models import Pond



class WaterFilter(django_filters.FilterSet):
    class Meta:
        model = Pond
        fields = ['cadastr_number', 'location', 'area', 'destination', 'land', 'coordinates', 'owner_name',
                      'rent_start', 'rent_end', 'interest', 'assessment', 'notes',
                      'pass_number', 'pass_name', 'pass_area', 'pass_volume', 'pass_depth', 'date_approval',
                      'pass_developer']

