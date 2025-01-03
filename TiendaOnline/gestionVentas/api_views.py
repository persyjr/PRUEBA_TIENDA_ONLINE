from rest_framework import generics
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
    # permission_classes = [permissions.IsAuthenticated]
    queryset = m.Venta.objects.all().order_by('-fecha_creacion')


class ListarProductosView(generics.ListAPIView):

    pagination_class = DataTablePagination
    serializer_class = se.ListProductosSerializer
    filter_backends = [DataTableSearchFilter]
    search_fields = [
            'id', 'nombre', 'codigo',
        ]
    # permission_classes = [permissions.IsAuthenticated]
    queryset = m.Producto.objects.all().order_by('-fecha_creacion')


class InfoProductosAPIView(CspExemptMixin, generics.ListAPIView):
    serializer_class = se.FilterProductosSerializer
    # permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DataTableSearchFilter]
    search_fields = ['nombre', 'codigo']

    def get_queryset(self, **kwargs):
        try:
            productos = m.Producto.objects.filter(cantidad__gt=0)
        except Exception as e:
            print(e)
            productos = m.Producto.objects.none() 
        return productos
