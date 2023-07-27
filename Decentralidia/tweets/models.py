from django.db import models

# Create your models here.
class Tweet(models.Model):
    id = models.AutoField(primary_key=True)
    text = models.CharField(max_length=200)
    category = models.CharField(max_length=200)
    votes = models.CharField(max_length=200, default="", blank=True)
