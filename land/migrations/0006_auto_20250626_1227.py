from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        # вкажіть вашу останню міграцію, наприклад:
        ('land', '0005_historicallandplot_has_passport_and_more'),
    ]

    operations = [
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS postgis;"),
        migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS postgis_topology;"),
        # migrations.RunSQL("CREATE EXTENSION IF NOT EXISTS postgis_raster;"),
    ]