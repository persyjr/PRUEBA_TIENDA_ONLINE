from django.utils import timezone
from datetime import timedelta
from rest_framework import serializers
from . import models as m

class ListClientesSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = m.Clientes
        fields = (
            'id',
            'nombre',
            'email',
            'telefono',
            'direccion',
        )
