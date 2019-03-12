from django.db import models
from datetime import datetime

# Create your models here.#
class Pictures(models.Model):
    title = models.CharField(max_length=20)
    time=models.DateTimeField()
    name=models.CharField(max_length=40)
    size=models.CharField(max_length=40)
    text=models.CharField(max_length=100)

    class Meta:
    	db_table='Oam'
