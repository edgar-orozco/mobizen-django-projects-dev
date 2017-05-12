# -*- coding: utf-8 -*- 
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from drivemee import models
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from django.utils import timezone

class PublicCreateSolicitudForm(forms.Form):
    nombre = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    telefono = forms.CharField(label='Teléfono', required=True)
    placa = forms.CharField(required=True)
    marca = forms.CharField(required=True)
    submarca = forms.CharField(required=True)
    hologramas = (
        ('DOBLE CERO', 'Doble Cero'),
        ('CERO', 'Cero'),
        ('UNO', 'Uno'),
        ('DOS', 'Dos'),
    )
    year = timezone.now().year+1
    modelos = [(str(year), str(year)),]
    cupon = forms.CharField(label='Código', required=False)
    for x in range(1, 16):
        modelos.append((str(year-x), str(year-x)))
    modelo = forms.ChoiceField(choices=modelos, required=True)
    holograma = forms.ChoiceField(choices=hologramas, required=True)
    terms = forms.BooleanField(required=True)
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', None)
        try:
            int(telefono)
        except (ValueError, TypeError):
            raise forms.ValidationError('Número de teléfono inválido')
        if len(telefono) < 7:
            raise forms.ValidationError('Número de teléfono inválido')
        return telefono

class OperadorCreateForm(forms.ModelForm):
    class Meta:
       model = models.Operador
       exclude = ['foto', 'calificacion']

class DomicilioForm(forms.ModelForm):
    class Meta:
       model = models.Direccion
       fields = ['tipo', 'calle', 'numero_exterior', 'numero_interior', 'colonia', 'municipio', 'estado', 'codigo_postal', 'referencias', 'latitud', 'longitud']
    
class SolicitudVerificarForm(forms.Form):
    resultados = (
        ('', '-----'),
        ('DOBLE CERO', 'Doble Cero'),
        ('CERO', 'Cero'),
        ('UNO', 'Uno'),
        ('DOS', 'Dos'),
        ('EXENTO', 'Exento'),
        ('RECHAZO', 'Rechazo'),
    )
    resultado = forms.ChoiceField(choices=resultados, required=True)

class SolicitudPreagendarForm(forms.Form):
    startDate = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M")
    dateTimeOptions = {
    'startDate': startDate,
    'format': 'yyyy-mm-dd hh:ii',
    'autoclose': True,
    'daysOfWeekDisabled': [0,],
    'hoursOfDayDisabled': [0,1,2,3,4,5,6,19,20,21,22,23],
    'minuteStep': 15,
    'clearBtn': True,
    }
    fecha = forms.DateTimeField(required=True,
                                    widget=DateTimeWidget(usel10n=False, bootstrap_version=3, options=dateTimeOptions))

class SolicitudProcrastinateForm(forms.Form):
    startDate = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M")
    dateTimeOptions = {
    'startDate': startDate,
    'format': 'yyyy-mm-dd hh:ii',
    'autoclose': True,
    'daysOfWeekDisabled': [0,],
    'hoursOfDayDisabled': [0,1,2,3,4,5,6,19,20,21,22,23],
    'minuteStep': 15,
    'clearBtn': True,
    }
    fecha = forms.DateTimeField(required=True,
                                    widget=DateTimeWidget(usel10n=False, bootstrap_version=3, options=dateTimeOptions))
    motivo = forms.CharField(required=True)

class SolicitudNotesForm(forms.Form):
    motivo = forms.CharField(required=True)

class SolicitudScheduleForm(forms.Form):
    startDate = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M")
    dateTimeOptions = {
    'startDate': startDate,
    'format': 'yyyy-mm-dd hh:ii',
    'autoclose': True,
    'daysOfWeekDisabled': [0,],
    'hoursOfDayDisabled': [0,1,2,3,4,5,6,19,20,21,22,23],
    'minuteStep': 10,
    'clearBtn': True,
    'maxView': 2,
    }
    fecha = forms.DateTimeField(required=True,
                                    widget=DateTimeWidget(usel10n=False, bootstrap_version=3, options=dateTimeOptions))
#     motivo = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'required'}))
#     class Meta:
#         model = models.Cita
#         widgets = {
#             #Use localization and bootstrap 3
#             'fecha': DateTimeWidget(attrs={'id':"fecha"}, usel10n = True, bootstrap_version=3)
#         }
#         fields = ['fecha',]

class OperadorForm(forms.ModelForm):
    nombre = forms.ModelChoiceField(queryset=models.Operador.objects.filter(status='activo'))
    class Meta:
       model = models.Operador
       fields = ['nombre',]

class DatosClienteForm(forms.ModelForm):
    class Meta:
       model = models.Solicitud
       fields = ['nombre', 'email', 'telefono', 'cupon']

class SolicitudCreateForm(forms.ModelForm):
    class Meta:
       model = models.Solicitud
       fields = ['nombre', 'email', 'telefono', 'client', 'placa', 'marca', 'submarca', 'ultimo_holograma', 'modelo', 'cupon']

class CancelForm(forms.Form):
    estados = (
        ('', '-----'),
        ('cancelado', 'Cancelado'),
        ('caido', u'Cita Caída'),
        ('no_contratado', 'No Contratado'),
    )
    status = forms.ChoiceField(choices=estados, required=True)
    motivo = forms.CharField(required=True, widget=forms.TextInput(attrs={'class': 'required'}))
