from django.db import models
from django.db.models.base import Model

# Create your models here.
class Product(models.Model):
    Name = models.CharField(max_length=200)
    Price = models.FloatField()