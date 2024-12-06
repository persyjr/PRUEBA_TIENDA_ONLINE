from rest_framework import generics, permissions, filters
from common.api_views import DataTablePagination, DataTableSearchFilter
from . import models as m
from . import serializers as se
class ListarClientesView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.ListClientesSerializer
    filter_backends = [DataTableSearchFilter]
    search_fields = [
            'id','nombre','email','telefono','direccion',
        ]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = m.Clientes.objects.all().order_by('-fecha_creacion')