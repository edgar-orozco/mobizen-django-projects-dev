# -*- coding: utf-8 -*- 
import datetime
from django.utils import timezone
from django.db import models

# Create your models here.
class AppEntry(models.Model):
    """
    De read_more se va a jalar fecha, imagen y url para abrir nota completa
    """
    timestamp = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=50, blank=False)
    fecha = models.DateField(blank=False)
    image = models.ImageField(upload_to='verifica/news/', blank=True, null=True)
    link = models.CharField(max_length=250, blank=True, null=True)
    short_description = models.TextField(max_length=255, blank=False)
    platform_ios = models.BooleanField(default=True)
    platform_android = models.BooleanField(default=True)
    important = models.BooleanField(default=False)
    def __unicode__(self):
        return self.title
