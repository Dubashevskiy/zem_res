from rest_framework import serializers
from .models import LandPlot

class LandPlotSerializer(serializers.ModelSerializer):
    geom = serializers.SerializerMethodField()

    class Meta:
        model = LandPlot
        fields = ('cadastr_number', 'geom', 'area', 'location', 'destination')  # можна додати інші поля за потребою

        def get_geom(self, obj):
            return obj.geom.geojson if obj.geom else None