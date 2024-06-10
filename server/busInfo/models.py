from django.db import models

# Create your models here.

class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='districts')

    def __str__(self):
        return self.name


class BusStop(models.Model):
    name = models.CharField(max_length=100)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='bus_stops', null=True)

    def __str__(self):
        return self.name

class Bus(models.Model):
    number = models.CharField(max_length=10)
    area = models.CharField(max_length=100, default='Unknown')  # area 필드 추가
    bus_stop = models.ManyToManyField(BusStop, through='TimeTable', through_fields=('bus', 'arrival_bus_stop'))
    fare = models.PositiveIntegerField(default=0)  # 요금 필드 추가
    company = models.CharField(max_length=100)  # 회사 이름 필드 추가

    def __str__(self):
        return self.number

class TimeTable(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    departure_bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='departure_timetables')
    arrival_bus_stop = models.ForeignKey(BusStop, on_delete=models.CASCADE, related_name='arrival_timetables')
    time = models.TimeField()

    def __str__(self):
        return f'{self.bus} - {self.departure_bus_stop} to {self.arrival_bus_stop} - {self.time}'