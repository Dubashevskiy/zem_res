import os
import django
import xml.etree.ElementTree as ET
from pyproj import Transformer
from django.contrib.gis.geos import Polygon

# Налаштовуємо Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

from land.models import LandPlot  # вже після setup()

# Трансформер
transformer = Transformer.from_crs("EPSG:7827", "EPSG:4326", always_xy=True)

def import_from_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Збираємо точки
    points_dict = {}
    for point in root.findall(".//PointInfo/Point"):
        uid = point.find("UIDP").text
        x = float(point.find("Y").text)
        y = float(point.find("X").text)
        lon, lat = transformer.transform(x, y)
        points_dict[uid] = (lon, lat)

    # Лінії полігону
    boundary = root.find(".//Externals/Boundary/Lines")
    polygon_points = []
    for line in boundary.findall("Line"):
        ulid = line.find("ULID").text
        for pl in root.findall(f".//Polyline/PL[ULID='{ulid}']/Points/P"):
            point_id = pl.text
            polygon_points.append(points_dict[point_id])

    if polygon_points[0] != polygon_points[-1]:
        polygon_points.append(polygon_points[0])  # Закриваємо полігон

    cadastral_number = root.find(".//CadastralCode").text.strip()
    polygon = Polygon(polygon_points)

    plot, created = LandPlot.objects.get_or_create(cadastr_number=cadastral_number)
    plot.geom = polygon
    plot.save()

    print(f"✅ Ділянка {cadastral_number} імпортована!")

# Запуск:
if __name__ == "__main__":
    import_from_xml("шлях_до_XML_файлу.xml")
