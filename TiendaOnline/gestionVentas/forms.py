from django import forms
from . import models as m


class ImageCompressWidget(forms.ClearableFileInput):
    template_name = 'components/customInputWidget.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        attrs = self.attrs
        context['name'] = name

        if value:
            context['value'] = value
        if 'required' in attrs:
            context['required'] = 'required'
        if 'allowFiles' in attrs:
            context['allowFiles'] = 'allowFiles'
        if 'retirarNA' in attrs:
            context['noaplica'] = 'noaplica'
        if 'cleareable' in attrs:
            context['cleareable'] = 'cleareable'
        if 'label' in attrs:
            context['label'] = attrs['label']
        if 'className' in attrs:
            context['className'] = attrs['className']
        else:
            context['label'] = name

        return context


class RegistrarProductoForm(forms.ModelForm):
    class Meta:
        model = m.Producto
        fields = ['nombre', 'codigo', 'valor_venta','tiene_iva','porcentaje_iva','imagen']
    
    widgets={
            'telefono': forms.NumberInput(attrs={'min': '3000000000','max': '9999999999', 'class': 'form-comtrol'}),
            'porcentaje_iva': forms.NumberInput(),
            'imagen':ImageCompressWidget({'retirarNA': 'retirarNA'}),
     }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].label = 'Código'
        self.fields['valor_venta'].label = 'Valor Venta'
        self.fields['tiene_iva'].label = '¿Tiene iva?'
        self.fields['nombre'].required = True
        self.fields['codigo'].required = True
        self.fields['valor_venta'].required = True
        self.fields['tiene_iva'].required = True
        # self.fields['porcentaje_iva'].required = True
        self.fields['nombre'].widget.attrs.update(
            {"class": "text-info",
             "placeholder": 'Ingresa nombre del producto'})
        self.fields['codigo'].widget.attrs.update(
            {"class": "text-info",
             "placeholder": 'Ingresa código del producto'})
        self.fields['valor_venta'].widget.attrs.update(
            {"class": "text-info",
             "placeholder": 'Ingresa el valor de la venta'})
        self.fields['tiene_iva'].widget.attrs.update(
            {"class": "text-info"})
        self.fields['porcentaje_iva'].widget.attrs.update(
            {"class": "text-info",
             "placeholder": 'Ingresa el % de iva'})
        
        if 'imagen-NA' in self.data:
            self.fields['imagen'].initial = 'NA.png'

class NuevaVeta(forms.ModelForm):
    class Meta:
        model = m.Venta
        fields = [
            'cliente',
            'fecha_venta',
            ]
        widgets = {
                'fecha_venta': forms.DateInput(
                    {'class': 'form control',
                    'type': 'datetime-local',
                    'style': 'border-style: none;'}),
            }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].required = True
        self.fields['cliente'].widget.attrs.update(
            {"class": "text-info"})

class ActualizarVentaForm(forms.ModelForm):
    class Meta:
        model = m.Venta
        fields = ['cliente',]
        widgets = {}