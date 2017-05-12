from django.contrib import admin
from verifica_news.models import *
    
class AppEntryAdmin(admin.ModelAdmin):
    model = AppEntry

admin.site.register(AppEntry, AppEntryAdmin)
