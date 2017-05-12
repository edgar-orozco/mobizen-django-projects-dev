# -*- coding: utf-8 -*- 
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms
from drivemee import models
from datetimewidget.widgets import DateTimeWidget, DateWidget, TimeWidget
from django.utils import timezone

from django_modalview.generic.edit import ModalFormView, ModalUpdateView, ModalFormUtilView, ModalCreateView, ModalDeleteView, ModalEditContextMixin, ProcessModalFormView, ModalTemplateMixin
from django_modalview.generic.component import ModalResponse, ModalButton
from django_modalview.generic.base import ModalTemplateView, ModalTemplateUtilView
from django.views.generic.edit import FormMixin

class MyModalFormMixin(ModalEditContextMixin, FormMixin):
    """
            Mixin that provide a way to show and to handle a modal with a django
            form.
    """
    def get_context_modal_data(self, **kwargs):
        if self.inited_form:
            kwargs.update({
                'form': self.inited_form,
            })
        else:
            kwargs.update({
                'form': self.get_form(self.get_form_class()),
            })
        return super(MyModalFormMixin, self).get_context_modal_data(**kwargs)

    def _form_response(self, **kwargs):
        kwargs.update(self.get_context_modal_data())
        return self.render_to_response(context=kwargs)

    def form_valid(self, form, **kwargs):
        self._can_redirect = True
        return self._form_response(**kwargs)

    def form_invalid(self, form, **kwargs):
        return self._form_response(**kwargs)

class MyBaseModalFormView(MyModalFormMixin, ProcessModalFormView):
    """
            A base view that provide a way to handle a modal with a form.
    """

class MyModalFormView(ModalTemplateMixin, MyBaseModalFormView):
    """
            Reemplaza django_modalview.edit.ModalFormView para poder pasar un Form pre-inicializado
    """
    
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
    estados = (
        ('DIF', 'Ciudad de México'),
        ('MEX', 'Estado de México'),
    )
    calle = forms.CharField(required=True)
    exterior = forms.CharField(required=True, label='Núm. Ext.')
    interior = forms.CharField(required=True, label='Núm. Int.')
    colonia = forms.CharField(required=True)
    delegacion = forms.CharField(required=True, label='Delegación')
    estado = forms.ChoiceField(choices=estados, required=True)
    codigo = forms.CharField(required=True, label='Código Postal')
    referencias = forms.CharField(required=False)
    def clean_telefono(self):
        telefono = self.cleaned_data.get('telefono', None)
        try:
            int(telefono)
        except (ValueError, TypeError):
            raise forms.ValidationError('Número de teléfono inválido')
        if len(telefono) < 7:
            raise forms.ValidationError('Número de teléfono inválido')
        return telefono
    def clean_codigo(self):
        codigo = self.cleaned_data.get('codigo', None)
        try:
            int(codigo)
        except (ValueError, TypeError):
            raise forms.ValidationError('Código Postal inválido')
        if len(codigo) < 4:
            raise forms.ValidationError('Código Postal inválido')
        return codigo

class OperadorCreateForm(forms.ModelForm):
    class Meta:
       model = models.Operador
       exclude = ['foto', 'calificacion', 'owner']

class OperadorCreateFormFull(forms.ModelForm):
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
    'daysOfWeekDisabled': [],
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
    'daysOfWeekDisabled': [],
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
    'daysOfWeekDisabled': [],
    'hoursOfDayDisabled': [0,1,2,3,4,5,6,19,20,21,22,23],
    'minuteStep': 10,
    'clearBtn': True,
    'maxView': 2,
    }
    fecha = forms.DateTimeField(required=True,
                                    widget=DateTimeWidget(usel10n=False, bootstrap_version=3, options=dateTimeOptions))
    doble_cero = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkbox_buttons'}), required=False)
    pago_tarjeta = forms.BooleanField(widget=forms.CheckboxInput(attrs={'class':'checkbox_buttons'}), required=False)

class SolicitudScheduleNoPaymentForm(forms.Form):
    startDate = timezone.localtime(timezone.now()).strftime("%Y-%m-%d %H:%M")
    dateTimeOptions = {
    'startDate': startDate,
    'format': 'yyyy-mm-dd hh:ii',
    'autoclose': True,
    'daysOfWeekDisabled': [],
    'hoursOfDayDisabled': [0,1,2,3,4,5,6,19,20,21,22,23],
    'minuteStep': 10,
    'clearBtn': True,
    'maxView': 2,
    }
    fecha = forms.DateTimeField(required=True,
                                    widget=DateTimeWidget(usel10n=False, bootstrap_version=3, options=dateTimeOptions))
    doble_cero = forms.BooleanField(required=False, widget=forms.CheckboxInput(attrs={'class':'checkbox_buttons'}))

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
    def __init__(self, proveedor=None, *args, **kwargs):
        self.proveedor = proveedor
        super(OperadorForm, self).__init__(*args, **kwargs)
        if proveedor:
            self.fields['nombre'].queryset = models.Operador.objects.filter(owner=proveedor)
#             self.fields['nombre'].widget = forms.ModelChoiceField(queryset=models.Operador.objects.filter(owner=proveedor))

        
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
