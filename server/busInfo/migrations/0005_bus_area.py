# Generated by Django 5.0.6 on 2024-06-03 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busInfo', '0004_bus_busstop_city_district_timetable_delete_businfo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bus',
            name='area',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]