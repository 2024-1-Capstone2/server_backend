# Generated by Django 5.0.6 on 2024-06-03 03:06

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busInfo', '0003_alter_busschedule_t1_weekday_times_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=10)),
                ('fare', models.PositiveIntegerField()),
                ('company', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BusStop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='District',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='districts', to='busInfo.city')),
            ],
        ),
        migrations.CreateModel(
            name='TimeTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.TimeField()),
            ],
        ),
        migrations.DeleteModel(
            name='BusInfo',
        ),
        migrations.DeleteModel(
            name='BusSchedule',
        ),
        migrations.AddField(
            model_name='busstop',
            name='district',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bus_stops', to='busInfo.district'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='arrival_bus_stop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='arrival_timetables', to='busInfo.busstop'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='bus',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='busInfo.bus'),
        ),
        migrations.AddField(
            model_name='timetable',
            name='departure_bus_stop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departure_timetables', to='busInfo.busstop'),
        ),
        migrations.AddField(
            model_name='bus',
            name='bus_stop',
            field=models.ManyToManyField(through='busInfo.TimeTable', to='busInfo.busstop'),
        ),
    ]
