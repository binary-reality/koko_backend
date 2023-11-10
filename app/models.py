from django.db import models

# Create your models here.
class testUnit(models.Model):
    var1 = models.CharField(max_length=30)
    class Meta():
        verbose_name = "test_table"
        verbose_name_plural = "OOHH"
    
class user(models.Model):
    open_id = models.CharField(max_length=100, primary_key=True, unique=True)
    create_time = models.DateField(auto_now_add=True)
    
