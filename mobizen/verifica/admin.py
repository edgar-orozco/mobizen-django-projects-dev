from django.contrib import admin
from django import forms
from verifica.models import *
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline

admin.site.site_header = "Verifica administrator"
admin.site.site_title = "Verifica Admin"

class AppConfigInline(admin.TabularInline):
    model = AppConfig
    can_delete = False

# class AppConfigAdmin(admin.ModelAdmin):
#     model = AppConfig
# admin.site.register(AppConfig, AppConfigAdmin)
class DeviceConfigInline(admin.TabularInline):
    model = DeviceInfo
    can_delete = True

class ClientAdmin(admin.ModelAdmin):
    model = Client
    inlines = [AppConfigInline,DeviceConfigInline]
    list_display = ("deviceToken", "appVersion", "last_login", "timestamp")
    list_filter = ('appVersion','timestamp')

admin.site.register(Client, ClientAdmin)

class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer

admin.site.register(Manufacturer, ManufacturerAdmin)

class ImecaAdmin(admin.ModelAdmin):
    model = Imeca

admin.site.register(Imeca, ImecaAdmin)
    
class CarAdmin(admin.ModelAdmin):
    model = Car

admin.site.register(Car, CarAdmin)
    
class TelefonoInline(admin.TabularInline):
    model = Telefono

class AseguradoraAdmin(admin.ModelAdmin):
    model = Aseguradora
    inlines = [TelefonoInline]

admin.site.register(Aseguradora, AseguradoraAdmin)

class SeguroAdmin(admin.TabularInline):
    model = Seguro
#admin.site.register(Seguro, SeguroAdmin)
     
class InfraccionInline(admin.TabularInline):
    model = Infraccion
    extra = 0

class TenenciaInline(admin.TabularInline):
    model = Tenencia
    extra = 1

class VerificacionInline(admin.TabularInline):
    model = Verificacion

class VehiculoConfigInline(admin.TabularInline):
    model = VehiculoConfig
    can_delete = False

class VehiculoAdmin(admin.ModelAdmin):
    model = Vehiculo
    inlines = [VehiculoConfigInline, TenenciaInline, VerificacionInline, SeguroAdmin, InfraccionInline]
    exclude = ('client','car')

admin.site.register(Vehiculo, VehiculoAdmin)

class ReleaseNotesInline(admin.TabularInline):
    model = ReleaseNotes
    extra = 0
    inlines = []

class BuildNotesInline(NestedTabularInline):
    model = BuildNote
    extra = 1
    inlines = []

class BuildsInline(NestedStackedInline):
    model = Builds
    extra = 1
    inlines = [BuildNotesInline]

class AppVersionAdmin(NestedModelAdmin):
    model = AppVersion
    inlines = [BuildsInline, ReleaseNotesInline]

admin.site.register(AppVersion, AppVersionAdmin)

class PlazoAdmin(admin.ModelAdmin):
    model = Plazo

admin.site.register(Plazo, PlazoAdmin)

class PaqueteAdmin(admin.ModelAdmin):
    model = Paquete

admin.site.register(Paquete, PaqueteAdmin)

class CotizadorErrorAdmin(admin.ModelAdmin):
    raw_id_fields = ('cotizacion',)
    model = CotizadorError
admin.site.register(CotizadorError, CotizadorErrorAdmin)

class CotizadorErrorInline(admin.TabularInline):
    raw_id_fields = ('cotizacion',)
    model = CotizadorError
    extra = 0

class ReciboInline(admin.TabularInline):
    raw_id_fields = ('cotizacion', 'seguro','vehiculo')
    model = Recibo
    extra = 0

class CotizacionAdmin(admin.ModelAdmin):
    readonly_fields = ('client','aseguradora')
    list_display = ("aseguradora", "paquete", "costo", "timestamp")
    model = Cotizacion
    inlines = [CotizadorErrorInline, ReciboInline]

admin.site.register(Cotizacion, CotizacionAdmin)

class CostoInline(admin.TabularInline):
    list_display = ("aseguradora", "costo")
    model = Comparacion.costos.through
    extra = 0
    can_delete = False
    
class ComparacionAdmin(admin.ModelAdmin):
    list_display = ("paquete", "plazo", "coche_registrado", "timeout", "elapsed", "timestamp")
    exclude = ('costos',)
    model = Comparacion
    inlines = [CostoInline,]

admin.site.register(Comparacion, ComparacionAdmin)

class TarifaItemInline(admin.TabularInline):
    model = TarifaItem
    extra = 0
    
class TarifaAdmin(admin.ModelAdmin):
    model = Tarifa
    inlines = [TarifaItemInline,]

admin.site.register(Tarifa, TarifaAdmin)

class SalarioMinimoAdmin(admin.ModelAdmin):
    model = SalarioMinimo

admin.site.register(SalarioMinimo, SalarioMinimoAdmin)

class FeriadosAdmin(admin.ModelAdmin):
    model = Feriado

admin.site.register(Feriado, FeriadosAdmin)

class TipoPlacaAdmin(admin.ModelAdmin):
    model = TipoPlaca

admin.site.register(TipoPlaca, TipoPlacaAdmin)

###
#
# Reglas Hoy No Circula Y Contingencia
class TerminacionAdmin(admin.ModelAdmin):
    model = Terminacion

admin.site.register(Terminacion, TerminacionAdmin)

class HologramaAdmin(admin.ModelAdmin):
    model = Holograma

admin.site.register(Holograma, HologramaAdmin)

class SemanaAdmin(admin.ModelAdmin):
    model = Semana

admin.site.register(Semana, SemanaAdmin)

class ReglaAdmin(admin.ModelAdmin):
    model = ReglaCirculacion
    def get_form(self, request, obj=None, **kwargs):
        form = super(ReglaAdmin, self).get_form(request, obj, **kwargs)
        form.base_fields['terminaciones'].widget = forms.CheckboxSelectMultiple()
        form.base_fields['hologramas'].widget = forms.CheckboxSelectMultiple()
        form.base_fields['semanas'].widget = forms.CheckboxSelectMultiple()
        return form

admin.site.register(ReglaCirculacion, ReglaAdmin)

class DiaAdmin(admin.ModelAdmin):
    model = Dia

admin.site.register(Dia, DiaAdmin)

class ReglaInline(admin.TabularInline):
    list_display = ("title","terminaciones", "hologramas", "semanas")
    model = ReglaCirculacion
    extra = 1
    can_delete = True

class ProgramaAdmin(admin.ModelAdmin):
    model = Programa

admin.site.register(Programa, ProgramaAdmin)

class ContingenciaAdmin(admin.ModelAdmin):
    model = Contingencia

admin.site.register(Contingencia, ContingenciaAdmin)
