from django.db import models

# Create your models here.


class Clientes(models.Model):
    #el campo id es opcional, de no crearlo lo crea django al migrar
    nombre=models.CharField(max_length=50)
    email = models.EmailField(blank=True, null=True)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=250, blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return  f'{self.nombre} - {self.email}'

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        permissions = [
            ('can_crear_cliente', 'Puede crear Cliente'),
        ]