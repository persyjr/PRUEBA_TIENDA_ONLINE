from django.db import models
from abm import models as abm_m

# Create your models here.
class Producto(models.Model):
    codigo=models.CharField(max_length=20)
    nombre=models.CharField(max_length=30)
    valor_venta=models.CharField(max_length=50,verbose_name='Valor ventas')
    tiene_iva = models.BooleanField(default=False, null=True)
    porcentaje_iva= models.FloatField(blank=True, null=True)
    imagen = models.FileField(upload_to='gestionVentas/productos', blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return  f'{self.codigo} - {self.nombre}'

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        permissions = [
            ('can_read_producto', 'Puede ver producto'),
        ]


class Venta(models.Model):
    cliente=models.ForeignKey(
        abm_m.Clientes, blank=True,
        related_name='venta_cliente',
        on_delete=models.CASCADE,
        null=True)
    consecutivo=models.CharField(max_length=20)
    total_venta=models.FloatField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_venta = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return  f'{self.consecutivo} - {self.fecha_creacion}'

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        permissions = [
            ('can_crear_venta', 'Puede crear Venta'),
        ]

class ItemVenta(models.Model):
    venta=models.ForeignKey(
        Venta, blank=True,
        related_name='venta_items',
        on_delete=models.CASCADE,
        null=True)
    producto=producto=models.ForeignKey(
        Producto, blank=True,
        related_name='producto_items',
        on_delete=models.CASCADE,
        null=True)
    cantidad=models.IntegerField(blank=True, null=True)
    valor=models.FloatField(blank=True, null=True)
    iva=models.FloatField(blank=True, null=True)

    def __str__(self):
        return  f'{self.producto} - {self.venta}'

    class Meta:
        verbose_name = 'Item Venta'
        verbose_name_plural = 'Items Ventas'
        permissions = [
            ('can_crear_Item_venta', 'Puede crear Item Venta'),
            ]