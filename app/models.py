from django.db import models

# Create your models here.
class testUnit(models.Model):
    var1 = models.CharField(max_length=30)
    class Meta():
        verbose_name = "test_table"
        verbose_name_plural = "OOHH"

# class user(models.Model):
