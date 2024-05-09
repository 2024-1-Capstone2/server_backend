from django.db import models

# Create your models here.
class BusInfo(models.Model):
    # 출발 시간, 도착 시간, 가격(어른, 아이, 학생), 회사 이름, 등급, 남은 좌석
    departure_time = models.CharField(max_length=100)
    arrival_time = models.CharField(max_length=100)
    adult_fare = models.CharField(max_length=100)
    child_fare = models.CharField(max_length=100)
    student_fare = models.CharField(max_length=100)
    company = models.CharField(max_length=100)
    grade = models.CharField(max_length=100)
    available_seats = models.CharField(max_length=100)