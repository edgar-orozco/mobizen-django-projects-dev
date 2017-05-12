from django.contrib import admin
from drivemee.models import *
from nested_inline.admin import NestedStackedInline, NestedModelAdmin, NestedTabularInline

class DireccionConfigInline(admin.TabularInline):
    model = Direccion
    can_delete = True
    extra = 1

class CitaConfigInline(admin.TabularInline):
    model = Cita
    can_delete = True

class ResultadoConfigInline(admin.TabularInline):
    model = Resultado
    can_delete = True

class ReporteConfigInline(admin.TabularInline):
    model = Reporte
#     can_delete = False

class CalificacionConfigInline(admin.TabularInline):
    model = CalificacionCliente
    can_delete = False
    exclude = ('client',)

class EvaluacionConfigInline(admin.TabularInline):
    model = Evaluacion
#     can_delete = False

class NotaInline(admin.TabularInline):
    model = Note

class DocumentosConfigInline(admin.TabularInline):
    model = Documento
    can_delete = False

class SolicitudAdmin(admin.ModelAdmin):
    model = Solicitud
    inlines = [DocumentosConfigInline, CitaConfigInline, DireccionConfigInline, ReporteConfigInline, CalificacionConfigInline, EvaluacionConfigInline, ResultadoConfigInline, NotaInline]
#     list_display = ("deviceToken", "appVersion", "last_login", "timestamp")
    exclude = ('vehiculo','client','solicitudToken')

admin.site.register(Solicitud, SolicitudAdmin)

class EmpresaAdmin(admin.ModelAdmin):
    model = Empresa

admin.site.register(Empresa, EmpresaAdmin)
    
class OperadorAdmin(admin.ModelAdmin):
    model = Operador

admin.site.register(Operador, OperadorAdmin)
    
class CuponAdmin(admin.ModelAdmin):
    model = Cupon

admin.site.register(Cupon, CuponAdmin)

class TarifaAdmin(admin.ModelAdmin):
    model = Tarifa
    
admin.site.register(Tarifa, TarifaAdmin)
