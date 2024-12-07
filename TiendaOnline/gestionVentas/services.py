from . import resources as r
from . import models as m

def descargar_reporte_all_ventas():
    resource = r.ReporteVentasResource()
    return resource.export(m.Venta.objects.all())

def descargar_reporte_all_products():
    resource = r.ReporteProductosResource()
    return resource.export(m.Producto.objects.all())