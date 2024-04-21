from django.db import models

# Create your models here.

class Items(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=100)
    price=models.IntegerField(default=0)
    img=models.ImageField(upload_to= 'pics')
