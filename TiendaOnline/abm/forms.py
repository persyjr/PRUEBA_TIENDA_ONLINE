from django import forms
from . import models as m


class RegistrarClienteForm(forms.ModelForm):
    class Meta:
        model = m.Clientes
        fields = ['nombre', 'email', 'telefono', 'direccion']
        widgets = {
            'telefono': forms.NumberInput(attrs={'min': '3000000000',
                                                 'max': '9999999999',
                                                 'class': 'form-comtrol'}),
                                                 }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telefono'].label = 'Teléfono'
        self.fields['direccion'].label = 'Dirección'
        self.fields['nombre'].required = True
        self.fields['email'].required = True
        self.fields['email'].widget.attrs.update(
            {"class": "text-info",
             "placeholder": 'Ingresa un email'})
        self.fields['nombre'].widget.attrs.update(
            {"class": "text-info",
             "placeholder": 'Ingresa nombre completo'})
        self.fields['telefono'].widget.attrs.update(
            {"class": "text-info",
             "placeholder": 'Ingresa un número de teléfono'})
        self.fields['direccion'].widget.attrs.update(
            {"class": "text-info",
             "placeholder": 'Ingresa tu dirección'})