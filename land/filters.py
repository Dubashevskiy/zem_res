import django_filters
from .models import LandPlot



class LandPlotFilter(django_filters.FilterSet):
    class Meta:
        model = LandPlot
        fields = ['cadastr_number', 'location', 'area', 'owner_name', 'category', 'destination', 'rent_start', 'rent_end', 'interest', 'assessment', 'land']
