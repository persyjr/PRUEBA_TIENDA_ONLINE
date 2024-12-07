from . import models as m
from import_export import resources

class ReporteVentasResource(resources.ModelResource):
    cliente = resources.Field()
    consecutivo = resources.Field()
    total_venta = resources.Field()
    fecha_creacion = resources.Field()
    fecha_venta = resources.Field()
    

    class Meta:
        model = m.Venta
        fields = [
            'cliente',
            'consecutivo',
            'total_venta',
            'fecha_creacion',
            'fecha_venta',
            ]
    
    def dehydrate_cliente(self, obj):
        if not obj.cliente:
            return
        return str(obj.cliente.nombre)
    
    def dehydrate_consecutivo(self, obj):
        if not obj.consecutivo:
            return
        return str(obj.consecutivo)
    
    def dehydrate_total_venta(self, obj):
        if not obj.total_venta:
            return
        return str(obj.total_venta)
    
    def dehydrate_fecha_creacion(self, obj):
        if not obj.fecha_creacion:
            return
        return str(obj.fecha_creacion)
    
    def dehydrate_fecha_venta(self, obj):
        if not obj.fecha_venta:
            return
        return str(obj.fecha_venta)


class ReporteProductosResource(resources.ModelResource):
    nombre = resources.Field()
    codigo = resources.Field()
    valor_venta = resources.Field()
    tiene_iva = resources.Field()
    porcentaje_iva = resources.Field()
    fecha_creacion = resources.Field()

    class Meta:
        model = m.Venta
        fields = [
            'nombre',
            'codigo',
            'valor_venta',
            'tiene_iva',
            'porcentaje_iva',
            'fecha_creacion',
            ]
    
    def dehydrate_nombre(self, obj):
        if not obj.nombre:
            return
        return str(obj.nombre)

    def dehydrate_codigo(self, obj):
        if not obj.codigo:
            return
        return str(obj.codigo)

    def dehydrate_valor_venta(self, obj):
        if not obj.valor_venta:
            return
        return str(obj.valor_venta)

    def dehydrate_tiene_iva(self, obj):
        if not obj.tiene_iva:
            return
        return str(obj.tiene_iva)
    
    def dehydrate_porcentaje_iva(self, obj):
        if not obj.porcentaje_iva:
            return
        return str(obj.porcentaje_iva)
    
    def dehydrate_fecha_creacion(self, obj):
        if not obj.fecha_creacion:
            return
        return str(obj.fecha_creacion)