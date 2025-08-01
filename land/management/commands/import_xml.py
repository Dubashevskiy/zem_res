import os
from django.core.management.base import BaseCommand
from xml.etree import ElementTree as ET
from land.models import LandPlot
from django.contrib.gis.geos import Polygon, LinearRing
from pyproj import Transformer


class Command(BaseCommand):
    help = 'Пакетний імпорт координат ділянок з усіх XML файлів у папці'

    def add_arguments(self, parser):
        parser.add_argument('folder', type=str, help='Шлях до папки з XML файлами')
        parser.add_argument('--crs', type=str, default='EPSG:7827',
                            help='Вхідна система координат (за замовчуванням EPSG:7827)')

    def handle(self, *args, **kwargs):
        folder = kwargs['folder']
        input_crs = kwargs['crs']
        transformer = Transformer.from_crs(input_crs, "EPSG:4326", always_xy=True)

        if not os.path.isdir(folder):
            self.stderr.write(f"Помилка: Папка {folder} не існує або недоступна")
            return

        files = [f for f in os.listdir(folder) if f.lower().endswith('.xml')]
        total_files = len(files)
        self.stdout.write(f"Знайдено {total_files} XML файлів у папці {folder}")

        for idx, filename in enumerate(files, start=1):
            filepath = os.path.join(folder, filename)
            self.stdout.write(f"\nОбробка файлу {idx}/{total_files}: {filename}")
            try:
                tree = ET.parse(filepath)
                root = tree.getroot()

                # Збираємо всі точки у словник: ключ - UIDP, значення - (lon, lat)
                points = {}
                for point in root.findall('.//Point'):
                    uidp = point.findtext('UIDP')
                    y_str = point.findtext('X')
                    x_str = point.findtext('Y')
                    if not uidp or not x_str or not y_str:
                        self.stderr.write(f'Файл {filename}: пропущена точка або координати (UIDP={uidp})')
                        continue

                    # Замінюємо кому на крапку, якщо є
                    x_str = x_str.replace(',', '.')
                    y_str = y_str.replace(',', '.')

                    try:
                        x_orig = float(x_str)
                        y_orig = float(y_str)
                    except ValueError:
                        self.stderr.write(f'Файл {filename}: некоректні координати для UIDP={uidp}')
                        continue

                    lon, lat = transformer.transform(x_orig, y_orig)
                    points[uidp] = (lon, lat)

                # Отримуємо номер зони
                zone_elem = root.find('.//CadastralZoneInfo/CadastralZoneNumber')
                zone_number = zone_elem.text if zone_elem is not None else None

                if not zone_number:
                    self.stderr.write(f'Файл {filename}: не знайдено номер кадастрової зони')
                    continue

                quarters = root.findall('.//CadastralZoneInfo/CadastralQuarters/CadastralQuarterInfo')

                for quarter in quarters:
                    quarter_number = quarter.findtext('CadastralQuarterNumber')
                    if not quarter_number:
                        self.stderr.write(f'Файл {filename}: не знайдено номер кадастрового кварталу')
                        continue

                    parcels = quarter.findall('./Parcels/ParcelInfo')
                    for parcel in parcels:
                        parcel_id = parcel.findtext('./ParcelMetricInfo/ParcelID')
                        if not parcel_id:
                            self.stderr.write(f'Файл {filename}: не знайдено ParcelID для ділянки')
                            continue

                        cadastral_code = f"{zone_number}:{quarter_number}:{parcel_id}"
                        self.stdout.write(f"  Обробка ділянки: {cadastral_code}")

                        # Збір координат полігону
                        boundary_lines = parcel.findall('.//Boundary/Lines/Line')
                        polygon_points = []

                        for line in boundary_lines:
                            ulid = line.findtext('ULID')
                            if not ulid:
                                self.stderr.write(f'Файл {filename}: не знайдено ULID у межах')
                                continue

                            line_elem = root.find(f".//Polyline/PL[ULID='{ulid}']")
                            if line_elem is None:
                                self.stderr.write(f'Файл {filename}: не знайдено Polyline з ULID={ulid}')
                                continue

                            line_points = [p.text for p in line_elem.findall('Points/P')]
                            for p_id in line_points:
                                coord = points.get(p_id)
                                if coord:
                                    polygon_points.append(coord)
                                else:
                                    self.stderr.write(f'Файл {filename}: не знайдено точку з UIDP={p_id}')

                        if len(polygon_points) < 3:
                            self.stderr.write(f'Файл {filename}: недостатньо точок для побудови полігону ділянки {cadastral_code}')
                            continue

                        if polygon_points[0] != polygon_points[-1]:
                            polygon_points.append(polygon_points[0])

                        try:
                            polygon = Polygon(LinearRing(polygon_points))
                        except Exception as e:
                            self.stderr.write(f'Файл {filename}: помилка створення полігону для {cadastral_code}: {e}')
                            continue

                        updated_count = LandPlot.objects.filter(cadastr_number=cadastral_code).update(geom=polygon)
                        if updated_count > 0:
                            self.stdout.write(self.style.SUCCESS(f'  Оновлено {updated_count} ділянок з кадастровим номером {cadastral_code}'))
                        else:
                            self.stderr.write(f'  Ділянку з кадастровим номером {cadastral_code} не знайдено в базі')

            except Exception as e:
                self.stderr.write(f'Помилка обробки файлу {filename}: {e}')

        self.stdout.write(self.style.SUCCESS('Пакетний імпорт координат завершено'))