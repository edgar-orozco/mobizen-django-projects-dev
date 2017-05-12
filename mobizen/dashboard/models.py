from django.db import models

# Create your models here.
class DailyActiveUser(models.Model):
    timestamp = models.DateField(auto_now_add=True, blank=True, unique=True)
    number_of_users = models.IntegerField()

class DailyTotalUser(models.Model):
    timestamp = models.DateField(auto_now_add=True, blank=True, unique=True)
    number_of_users = models.IntegerField()
