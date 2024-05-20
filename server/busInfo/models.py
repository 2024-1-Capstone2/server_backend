from django.db import models

# Create your models here.
class BusInfo(models.Model):
    # 도착 정류소 이름, 버스 번호, 지역(구)
    bus_number = models.CharField(max_length=100)
    departure_station = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
