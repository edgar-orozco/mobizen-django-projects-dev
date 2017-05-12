from django import forms
from localflavor.mx.forms import MXStateSelect

import selectable.forms as selectable
from servicios.lookups import TelefonoLookup, MunicipioLookup, ColoniaLookup
from servicios.models import Telefono, Establecimiento, Direccion

class DireccionChainedForm(forms.ModelForm):
#     estado = MXStateSelect()
#     municipio = selectable.AutoCompleteSelectField(
#         lookup_class=MunicipioLookup,
#         label='Municipio',
#         required=True,
#         widget=selectable.AutoComboboxSelectWidget,
#     )
#     colonia = selectable.AutoCompleteSelectField(
#         lookup_class=ColoniaLookup,
#         label='Colonia',
#         required=True,
#         widget=selectable.AutoComboboxSelectWidget,
#     )
    class Meta(object):
        model = Direccion
        widgets = {
            'estado': MXStateSelect(),
            'municipio': selectable.AutoComboboxSelectWidget(lookup_class=MunicipioLookup,),
            'colonia' : selectable.AutoComboboxSelectWidget(lookup_class=ColoniaLookup,),
        }
        exclude = ('', )

class EstablecimientoAdminForm(forms.ModelForm):
    class Meta(object):
        model = Establecimiento
        widgets = {
            'telefonos': selectable.AutoCompleteSelectMultipleWidget(lookup_class=TelefonoLookup),
        }
        exclude = ('', )

class TelefonoAdminForm(forms.ModelForm):
    telefono = selectable.AutoCompleteSelectField(lookup_class=TelefonoLookup, allow_new=True)
    class Meta(object):
        model = Telefono
        widgets = {
            'telnumber': selectable.AutoCompleteSelectMultipleWidget(lookup_class=TelefonoLookup),
        }
        exclude = ('telnumber', )

    def __init__(self, *args, **kwargs):
        super(TelefonoAdminForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.pk and self.instance.telnumber:
            self.initial['telefono'] = self.instance.pk

    def save(self, *args, **kwargs):
        tel = self.cleaned_data['telefono']
        if tel and not tel.pk:
            tel = Telefono.objects.create(telnumber=tel.telnumber)
        return super(TelefonoAdminForm, self).save(*args, **kwargs)