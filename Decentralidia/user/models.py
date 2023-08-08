from django.db import models

# Create your models here.
class User(models.Model):
    id = models.AutoField(primary_key=True)
    fullname = models.CharField(max_length=200)
    votes = models.CharField(max_length=300, default="", blank=True)
