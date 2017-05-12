from django.forms import widgets
from verifica_news import models
from rest_framework import serializers

class AppEntryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AppEntry
        fields = ('id','title','image','fecha','short_description','link','important')
