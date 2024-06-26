# Generated by Django 5.0.6 on 2024-05-28 05:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('busInfo', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BusSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bus_number', models.CharField(max_length=15, unique=True)),
                ('t1_weekday_times', models.TextField()),
                ('t1_weekend_times', models.TextField()),
                ('t2_weekday_times', models.TextField()),
                ('t2_weekend_times', models.TextField()),
            ],
        ),
        migrations.RenameField(
            model_name='businfo',
            old_name='adult_fare',
            new_name='bus_number',
        ),
        migrations.RenameField(
            model_name='businfo',
            old_name='arrival_time',
            new_name='departure_station',
        ),
        migrations.RenameField(
            model_name='businfo',
            old_name='available_seats',
            new_name='location',
        ),
        migrations.RemoveField(
            model_name='businfo',
            name='child_fare',
        ),
        migrations.RemoveField(
            model_name='businfo',
            name='company',
        ),
        migrations.RemoveField(
            model_name='businfo',
            name='departure_time',
        ),
        migrations.RemoveField(
            model_name='businfo',
            name='grade',
        ),
        migrations.RemoveField(
            model_name='businfo',
            name='student_fare',
        ),
    ]
