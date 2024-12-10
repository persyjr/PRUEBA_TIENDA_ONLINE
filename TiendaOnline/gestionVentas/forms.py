from django import forms
from abm import models as abm_m
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
        fields = ['nombre', 'codigo', 'valor_venta', 'tiene_iva',
                  'porcentaje_iva', 'imagen', 'cantidad']

        widgets = {
                'tiene_iva': forms.CheckboxInput({'style': 'height: 0.9rem;'}),
                'porcentaje_iva': forms.NumberInput(attrs={
                    'min': '0',
                    'max': '100',
                    'class': 'form-control'
                }),
                'imagen': ImageCompressWidget({
                    'cleareable': 'cleareable',
                    }),
        }

    def clean_porcentaje_iva(self):
        porcentaje_iva = self.cleaned_data.get('porcentaje_iva')
        if porcentaje_iva is not None:
            if porcentaje_iva < 0 or porcentaje_iva > 100:
                raise forms.ValidationError("El IVA debe estar entre 0 y 100.")
        return porcentaje_iva

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['codigo'].label = 'Código'
        self.fields['valor_venta'].label = 'Valor Venta'
        self.fields['tiene_iva'].label = '¿Tiene iva?'
        self.fields['nombre'].required = True
        self.fields['codigo'].required = True
        self.fields['cantidad'].required = True
        self.fields['valor_venta'].required = True
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
        self.fields['cantidad'].widget.attrs.update(
            {"class": "text-info",
             "placeholder": 'Ingresa la cantidad'})
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


class ActualizarDatosVentaForm(forms.ModelForm):
    class Meta:
        model = m.Venta
        fields = ['cliente', 'fecha_venta']
        widgets = {
            'fecha_venta': forms.DateInput(
                    {'class': 'form control',
                     'type': 'datetime-local',
                     'style': 'border-style: none;'}),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            if self.instance:
                self.fields['cliente'].queryset = abm_m.Clientes.objects.all()
            self.fields['cliente'].widget.attrs.update(
                {"class": "text-info"})


class NuevoItemVeta(forms.ModelForm):
    class Meta:
        model = m.ItemVenta
        fields = [
            'cantidad',
            ]
        widgets = {
                'cantidad': forms.NumberInput(attrs={
                    'min': '0',
                    'max': '100', #m.ItemVenta.producto.cantidad
                    'class': 'form-control'
                }),}
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
         # Asegúrate de que self.instance está definido
        if self.instance and self.instance.producto:
            max_cantidad = self.instance.producto.cantidad  # Obtén la cantidad del producto
            self.fields['cantidad'].widget.attrs.update({
                'max': max_cantidad,  # Actualiza el atributo 'max' dinámicamente
                "class": "text-info"
            })