from django.contrib import admin
from servicios.models import *
from servicios import forms

# Register your models here.

class EstadoAdmin(admin.ModelAdmin):
    model = Estado

admin.site.register(Estado, EstadoAdmin)

class MunicipioAdmin(admin.ModelAdmin):
    model = Municipio

admin.site.register(Municipio, MunicipioAdmin)
    
class ColoniaAdmin(admin.ModelAdmin):
    model = Colonia

admin.site.register(Colonia, ColoniaAdmin)

class TramiteAdmin(admin.ModelAdmin):
    model = Tramite

admin.site.register(Tramite, TramiteAdmin)

class CodigoPostalAdmin(admin.ModelAdmin):
    model = CodigoPostal

admin.site.register(CodigoPostal, CodigoPostalAdmin)

class TelefonoAdmin(admin.ModelAdmin):
    model = Telefono
admin.site.register(Telefono, TelefonoAdmin)

class DireccionAdmin(admin.ModelAdmin):
    add_form_template = 'advanced.html'
    change_form_template = 'advanced.html'
    form = forms.DireccionChainedForm

admin.site.register(Direccion, DireccionAdmin)

class DireccionInline(admin.StackedInline):
    model = Direccion
    form = forms.DireccionChainedForm

class ServicioAdmin(admin.ModelAdmin):
    model = Servicio

admin.site.register(Servicio, ServicioAdmin)

class EstablecimientoAdmin(admin.ModelAdmin):
    add_form_template = 'advanced.html'
    change_form_template = 'advanced.html'
    form = forms.EstablecimientoAdminForm
    inlines = [DireccionInline]

admin.site.register(Establecimiento, EstablecimientoAdmin)

