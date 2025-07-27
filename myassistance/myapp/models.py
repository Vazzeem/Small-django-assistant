from django.db import models

# Create your models here.

class aimodel(models.Model):
    Username=models.CharField(max_length=300)
    email=models.CharField(max_length=300)
    password=models.CharField(max_length=300)
    