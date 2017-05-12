from django.db import models
from django.utils import timezone
from dateutil.relativedelta import relativedelta
import datetime

class VehiculoQueryset(models.query.QuerySet):
    """Usuarios que han usado la app en los ultimos 15 dias"""
    def tiene_seguro(self):
        return self.filter(seguro__isnull=False)

class VehiculoManager(models.Manager):
    def get_queryset(self):
        return VehiculoQueryset(self.model, using=self._db)

    def tiene_seguro(self):
        return self.get_queryset().tiene_seguro()
