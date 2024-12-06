from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from . import models as m

class ListVentasSerializer(serializers.ModelSerializer):
    cliente = serializers.SerializerMethodField()

    class Meta:
        model = m.Venta
        fields = (
            'cliente',
            'consecutivo',
            'total_venta',
            'fecha_creacion',
        )

    def get_cliente(self, obj):
        if obj.cliente:
            return (str(obj.cliente.nombre))

class ListProductosSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = m.Producto
        fields = (
            'id',
            'nombre',
            'codigo',
            'valor_venta',
            'tiene_iva',
            'porcentaje_iva',
            'imagen',
            'fecha_creacion',
        )

    def get_cliente(self, obj):
        if obj.cliente:
            return (str(obj.cliente.nombre))