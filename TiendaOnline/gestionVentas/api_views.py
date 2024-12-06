from rest_framework import generics, permissions, filters
from common.api_views import DataTablePagination, DataTableSearchFilter
from csp.decorators import csp_exempt
from . import models as m
from . import serializers as se

class CspExemptMixin:
    @csp_exempt
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    
class ListarVentasView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.ListVentasSerializer
    filter_backends = [DataTableSearchFilter]
    search_fields = [
            'id', 'cliente__nombre',
        ]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = m.Venta.objects.all().order_by('-fecha_creacion')


class ListarProductosView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.ListProductosSerializer
    filter_backends = [DataTableSearchFilter]
    search_fields = [
            'id', 'nombre','codigo',
        ]
    #permission_classes = [permissions.IsAuthenticated]
    queryset = m.Producto.objects.all().order_by('-fecha_creacion')

class InfoProductosAPIView(CspExemptMixin, generics.ListAPIView):
    serializer_class = se.FilterProductosSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter]
    search_fields = ['nombre', 'codigo']

    def get_queryset(self, **kwargs):
        try:
            repuestos = m.Producto.objects.all()
        except Exception as e:
            print(e)
            repuestos = ''
        return repuestos