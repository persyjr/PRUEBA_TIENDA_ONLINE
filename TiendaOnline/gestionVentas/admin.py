from django.contrib import admin
from gestionVentas import models as m

# Register your models here.


@admin.register(m.Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = (
        'codigo',
        'nombre',
        'valor_venta',
        'tiene_iva',
        'porcentaje_iva',
        'imagen',
        )
    fields = (
        'codigo',
        'nombre',
        'valor_venta',
        'tiene_iva',
        'porcentaje_iva',
        'imagen',
        )


@admin.register(m.Venta)
class VentaAdmin(admin.ModelAdmin):
    list_display = (
        'cliente',
        'consecutivo',
        'total_venta',
        'fecha_creacion',
        )
    fields = (
        'cliente',
        'consecutivo',
        'total_venta',
        )


@admin.register(m.ItemVenta)
class ItemVentaAdmin(admin.ModelAdmin):
    list_display = (
        'venta',
        'producto',
        'valor',
        'iva',
        )
    fields = (
        'venta',
        'producto',
        'valor',
        'iva',
        )
