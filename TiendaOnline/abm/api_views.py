from django.contrib.auth.models import User
from rest_framework import generics
from common.api_views import DataTablePagination, DataTableSearchFilter
from . import models as m
from . import serializers as se


class ListarClientesView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.ListClientesSerializer
    filter_backends = [DataTableSearchFilter]
    search_fields = [
            'id', 'nombre', 'email', 'telefono', 'direccion',
        ]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = m.Clientes.objects.all().order_by('-fecha_creacion')

class ListarUsersAPIView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.UsersListSerializer
    #permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter]
    search_fields = ['username', 'first_name', 'last_name']
    queryset = User.objects.all()