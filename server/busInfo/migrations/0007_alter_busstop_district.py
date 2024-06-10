# Generated by Django 5.0.6 on 2024-06-08 12:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busInfo', '0006_alter_bus_fare'),
    ]

    operations = [
        migrations.AlterField(
            model_name='busstop',
            name='district',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='bus_stops', to='busInfo.district'),
        ),
    ]