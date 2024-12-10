from django.contrib.auth.models import User
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

class UsersListSerializer(serializers.ModelSerializer):
    email = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'is_active',
            'first_name',
            'last_name',
            'email'
        )

    def get_email(self, obj):
        if obj.email:
            return obj.email.lower()