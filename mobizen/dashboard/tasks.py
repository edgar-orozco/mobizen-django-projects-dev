# -*- coding: utf-8 -*- 
from mobizen import celery_app
from verifica import models as verifica_models
from dashboard.models import *

@celery_app.task()
def save_user_counts():
    DailyTotalUser.objects.create(number_of_users=verifica_models.Client.objects.all().count())
    DailyActiveUser.objects.create(number_of_users=verifica_models.Client.objects.active().count())
    return True