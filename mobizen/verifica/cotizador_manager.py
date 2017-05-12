from django.db import models

class CotizadorQueryset(models.query.QuerySet):
    """Seguros que tienen recibo"""
    def completed_sales(self):
        return self.filter(recibos__isnull = False)

class CotizadorManager(models.Manager):
    def get_queryset(self):
        return CotizadorQueryset(self.model, using=self._db)

    def completed_sales(self):
        return self.get_queryset().completed_sales()
