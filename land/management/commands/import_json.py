import json
from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Polygon, MultiPolygon, LinearRing
from land.models import LandPlot

class Command(BaseCommand):
    help = 'Імпорт ділянок з GeoJSON файлу'

    def add_arguments(self, parser):
        parser.add_argument('geojson_file', type=str, help='Шлях до GeoJSON файлу')

    def handle(self, *args, **kwargs):
        geojson_file = kwargs['geojson_file']
        try:
            with open(geojson_file, encoding='utf-8') as f:
                geojson = json.load(f)
        except Exception as e:
            self.stderr.write(f"Не вдалося відкрити файл: {e}")
            return

        for feature in geojson['features']:
            props = feature.get('properties', {})
            geom = feature.get('geometry')
            cadastral_number = props.get('cadastr')

            if not cadastral_number:
                self.stderr.write("Властивість 'cadastr' відсутня у фічі, пропускаємо")
                continue

            geom_type = geom.get('type')
            coords = geom.get('coordinates')

            try:
                if geom_type == 'Polygon':
                    shell = [(pt[0], pt[1]) for pt in coords[0]]
                    django_geom = Polygon(LinearRing(shell))

                elif geom_type == 'MultiPolygon':
                    polygons = []
                    for poly_coords in coords:
                        shell = [(pt[0], pt[1]) for pt in poly_coords[0]]
                        polygons.append(Polygon(LinearRing(shell)))
                    django_geom = MultiPolygon(polygons)
                else:
                    self.stderr.write(f"Непідтримуваний тип геометрії: {geom_type}")
                    continue

                updated = LandPlot.objects.filter(cadastr_number=cadastral_number).update(geom=django_geom)
                if updated:
                    self.stdout.write(self.style.SUCCESS(f"Оновлено ділянку {cadastral_number}"))
                else:
                    self.stderr.write(f"Ділянку {cadastral_number} не знайдено в базі")

            except Exception as e:
                self.stderr.write(f"Помилка при обробці {cadastral_number}: {e}")

        self.stdout.write(self.style.SUCCESS('Імпорт завершено'))