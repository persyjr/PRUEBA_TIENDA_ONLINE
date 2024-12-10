from rest_framework import serializers
from . import models as m


class ListVentasSerializer(serializers.ModelSerializer):
    cliente = serializers.SerializerMethodField()
    _fecha_creacion = serializers.DateTimeField(source='fecha_creacion',
                                                format='%d-%m-%Y %H:%M')

    class Meta:
        model = m.Venta
        fields = (
            'id',
            'cliente',
            'consecutivo',
            'total_venta',
            '_fecha_creacion',
        )

    def get_cliente(self, obj):
        if obj.cliente:
            return (str(obj.cliente.nombre))


class ListProductosSerializer(serializers.ModelSerializer):
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model = m.Producto
        fields = (
            'id',
            'nombre',
            'codigo',
            'cantidad',
            'valor_venta',
            'tiene_iva',
            'porcentaje_iva',
            'imagen',
            'fecha_creacion',
            'subtotal',
        )

    def get_cliente(self, obj):
        if obj.cliente:
            return (str(obj.cliente.nombre))
    
    def get_subtotal(self, obj):
        if obj.tiene_iva and obj.valor_venta:
            subtotal = float(obj.valor_venta)+(float(obj.valor_venta)* obj.porcentaje_iva/100)
            return (str(subtotal))
        else:
            return (str(obj.valor_venta))


class FilterProductosSerializer(serializers.ModelSerializer):
    text = serializers.SerializerMethodField()
    value = serializers.SerializerMethodField()

    class Meta:
        model = m.Producto
        fields = [
            'value',
            'text',
        ]

    def get_value(self, obj):
        return obj.id

    def get_text(self, obj):

        try:
            return f"""[{obj.id}] - {obj.nombre} - {obj.codigo}
                    <img alt='Imagen {obj.nombre}' src='{obj.imagen.url}'
                    style='width: 40px; border-radius: 15%;
                    object-fit: cover;' >"""
        except Exception as ex:
            print(ex)
            return f"""[{obj.id}] - {obj.nombre} - {obj.codigo}
                    <img alt='Imagen {obj.nombre}' src='{obj.imagen.url}'
                    style='width: 40px; border-radius: 15%;
                    object-fit: cover;' >"""
