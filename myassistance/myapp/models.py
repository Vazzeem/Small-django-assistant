from django.db import models

# Create your models here.

class myai(models.Model):
    admin=models.CharField(max_length=300)
    password=models.CharField(max_length=300)