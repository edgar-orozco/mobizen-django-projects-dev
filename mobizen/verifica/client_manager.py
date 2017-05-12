from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime

class ClientQueryset(models.query.QuerySet):
    """Usuarios que han usado la app en los ultimos 15 dias"""
    def active(self):
        return self.filter(last_login__gte = timezone.localtime(timezone.now())+relativedelta(days=-15))

class ClientManager(models.Manager):
    def get_queryset(self):
        return ClientQueryset(self.model, using=self._db)

    def active(self):
        return self.get_queryset().active()
