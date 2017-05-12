from django.db import models

class TenenciaQueryset(models.query.QuerySet):
    """Seguros que tienen recibo"""
    def completed_sales(self):
        return self.filter(recibos__isnull = False)
    def pendientes(self):
        return self.filter(pagado=False)

class TenenciaManager(models.Manager):
    def get_queryset(self):
        return TenenciaQueryset(self.model, using=self._db)

    def pendientes(self):
        return self.get_queryset().pendientes()
