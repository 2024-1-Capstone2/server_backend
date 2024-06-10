from django.db import models

# Create your models here.

class GlobalLanguage(models.Model):
    api_name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)

    def __str__(self):
        return self.api_name