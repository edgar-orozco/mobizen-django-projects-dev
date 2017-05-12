
from django.db.models import Q
from django.utils.html import escape
from servicios.models import Telefono, Municipio, Colonia
from selectable.base import ModelLookup
from selectable.registry import registry
from django.contrib import messages

class TelefonoLookup(ModelLookup):
    model = Telefono
    search_fields = ('telnumber__icontains', )

registry.register(TelefonoLookup)

class MunicipioLookup(ModelLookup):
    model = Municipio
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super(MunicipioLookup, self).get_query(request, term)
        estado = request.GET.get('estado', '')
        if estado:
            results = results.filter(estado=estado)
        else:
            results = None
        return results

    def get_item_label(self, item):
        return "%s" % (item.name)


registry.register(MunicipioLookup)

class ColoniaLookup(ModelLookup):
    model = Colonia
    search_fields = ('name__icontains', )

    def get_query(self, request, term):
        results = super(ColoniaLookup, self).get_query(request, term)
        municipio = request.GET.get('municipio', '')
        if municipio:
            results = results.filter(municipio__name=municipio)
        else:
            results = None
        return results

    def get_item_label(self, item):
        return "%s" % (item.name)


registry.register(ColoniaLookup)
