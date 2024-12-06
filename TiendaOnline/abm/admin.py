from django.contrib import admin
from abm import models as m

# Register your models here.
@admin.register(m.Clientes)
class Abm(admin.ModelAdmin):
    list_display = (
        'nombre',
        'email',
        'telefono',
        )
    fields =(
        'nombre',
        'email',
        'telefono',
        'direccion'
        )