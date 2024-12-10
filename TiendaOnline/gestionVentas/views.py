from django.urls import reverse_lazy
from datetime import datetime
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse
from django.views import generic
from typing import Any
from abm import models as m_abm
from . import services as s
from . import models as m
from . import forms as f
import pytz
tz = pytz.timezone('America/Bogota')
# Create your views here.


class HomeView(generic.TemplateView):
    template_name = 'gestionVentas/landingPage.html'


class listarVentasView(generic.ListView):
    model = m.Venta
    template_name = 'gestionVentas/list_ventas.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
        })
        return super().get_context_data(**kwargs)


class listarProductosView(generic.ListView):
    model = m.Producto
    template_name = 'gestionVentas/product_list.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
        })
        return super().get_context_data(**kwargs)


class RegistrarProductoView(generic.FormView):
    # permission_required = 'mantenimiento.can_ver_orden_trabajo'
    template_name = 'components/form_new_product.html'
    model = m.Producto
    form_class = f.RegistrarProductoForm

    def get_context_data(self, **kwargs):
        kwargs.update({
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        codigo = form.cleaned_data["codigo"]
        nombre = form.cleaned_data["nombre"]
        cantidad = form.cleaned_data["cantidad"]
        valor_venta = form.cleaned_data["valor_venta"]
        tiene_iva = form.cleaned_data["tiene_iva"]
        if form.cleaned_data["imagen"] is not None:
            imagen = form.cleaned_data["imagen"]
        elif form.cleaned_data["imagen"] is None or form.cleaned_data["imagen"] is False:
            imagen = '/NA.png'

        if tiene_iva:
            porcentaje_iva = form.cleaned_data["porcentaje_iva"]
        else:
            porcentaje_iva = 0

        producto = m.Producto.objects.create(
            codigo=codigo,
            nombre=nombre,
            cantidad=cantidad,
            valor_venta=valor_venta,
            tiene_iva=tiene_iva,
            imagen=imagen,
            porcentaje_iva=porcentaje_iva,
            )
        producto.save()  

        return HttpResponseRedirect(reverse_lazy('gestionVentas:product_list'))

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors},
                            status=400)

    def post(self, request: HttpRequest, *args: str,
             **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ActualizarProducto(generic.UpdateView):
    template_name = 'components/form_update_product.html'
    model = m.Producto
    form_class = f.RegistrarProductoForm

    def get_context_data(self, **kwargs):
        kwargs.update({
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        producto = self.get_object()
        producto.codigo = form.cleaned_data["codigo"]
        producto.cantidad = form.cleaned_data["cantidad"]
        producto.nombre = form.cleaned_data["nombre"]
        producto.valor_venta = form.cleaned_data["valor_venta"]
        producto.tiene_iva = form.cleaned_data["tiene_iva"]
        if form.cleaned_data["imagen"] is not None:
            producto.imagen = form.cleaned_data["imagen"]

        if form.cleaned_data["tiene_iva"] is not None:
            producto.porcentaje_iva = form.cleaned_data["porcentaje_iva"]
        else:
            producto.porcentaje_iva = 0

        producto.save()

        return HttpResponseRedirect(reverse_lazy(
            'gestionVentas:product_list'))

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors},
                            status=400)

    def post(self, request: HttpRequest, *args: str,
             **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EliminarProductoView(generic.DeleteView):
    # permission_required = 'mantenimiento.can_ver_herramientas'
    template_name = 'components/form_delete_product.html'
    model = m.Producto
    success_url = reverse_lazy('gestionVentas:product_list')


class RegistrarVentaView(generic.FormView):
    # permission_required = 'mantenimiento.can_ver_solicitudes'
    template_name = 'components/form_nueva_venta.html'
    model = m.Venta
    form_class = f.NuevaVeta

    def get_context_data(self, **kwargs):
        kwargs.update({
        })
        return super().get_context_data(**kwargs)

    def obtenerids(self, cadena):
        codigos = cadena.split(",")
        ids = []
        for codigo in codigos:
            try:
                inicio = codigo.find('[')
                fin = codigo.find(']')
                if inicio >= 0:
                    ids.append(codigo[inicio+1:fin])
            except Exception as e:
                print(e)
                pass

        return ids

    def form_valid(self, form, **kwargs):
        cliente = form.cleaned_data["cliente"]
        fecha_venta = form.cleaned_data["fecha_venta"]
        productos = self.request.POST['repuestos']

        venta = m.Venta.objects.create(
            cliente=cliente,
            fecha_venta=fecha_venta,
        )
        venta.save()
        venta.consecutivo = f'SALE-{datetime.now().strftime("%Y")}-{venta.id}'
        venta.save()
        listaids = self.obtenerids(productos)
        for numid in listaids:
            item_venta = m.ItemVenta.objects.create(
                cantidad=1,
                producto_id=numid,
                venta_id=venta.id,)
        item_venta.save()

        return HttpResponseRedirect(reverse_lazy(
            'gestionVentas:sale_detail',
            kwargs={'pk': venta.id}))

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors},
                            status=400)

    def post(self, request: HttpRequest, *args: str,
             **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class DetalleVentaView(generic.UpdateView):
    # permission_required = 'mantenimiento.can_read_cotizacion'
    template_name = 'gestionVentas/detalle_venta.html'
    model = m.Venta
    form_class = f.ActualizarVentaForm

    def get_context_data(self, **kwargs):
        kwargs.update({
            'items_cotizacion': self.get_items_cotizacion(),
            'totales': self.get_totales(),
        })
        return super().get_context_data(**kwargs)

    def get_items_cotizacion(self,):
        items = m.ItemVenta.objects.filter(venta=self.get_object())
        for item in items:
            cantidad = item.cantidad
            if item.producto.tiene_iva:
                porcentaje_iva = (item.producto.porcentaje_iva / 100)
                item.iva = float(item.producto.valor_venta)*porcentaje_iva*cantidad
            else:
                item.iva = 0.0
            item.valor = item.iva+float(item.producto.valor_venta)*cantidad
            item.save()
        return items

    def get_totales(self,):
        items = self.get_items_cotizacion()
        subtotal = 0
        iva = 0
        if items:
            for item in items:
                if item.valor:
                    subtotal += item.valor
                    iva += item.iva

        total = round(subtotal+iva, 1)
        iva = round(iva, 1)
        subtotal = round(subtotal, 1)
        totales = {
            'total': total,
            'subtotal': subtotal,
            'iva': iva
                 }
        venta = self.get_object()
        venta.total_venta = total
        venta.save()
        return totales

    def form_valid(self, form):
        id_cotizacion = self.kwargs['pk']
        cotizacion = self.get_object()
        cotizacion.datos_borrador_cliente = form.cleaned_data['datos_borrador_cliente']
        cotizacion.datos_borrador_herramienta = form.cleaned_data['datos_borrador_herramienta']
        cotizacion.save()
        return HttpResponseRedirect(
            reverse_lazy('mantenimiento:detalle_cotizacion_programada',
                         kwargs={'pk': id_cotizacion}))

    def form_invalid(self, form):
        return JsonResponse({'status': 'error',
                             'errors': form.errors}, status=400)

    def post(self, request: HttpRequest, *args: str,
             **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class EliminarVentaView(generic.DeleteView):
    # permission_required = 'mantenimiento.can_ver_herramientas'
    template_name = 'components/form_delete_sale.html'
    model = m.Venta
    success_url = reverse_lazy('gestionVentas:sales_list')


class EliminarItemVentaView(generic.DeleteView):
    # permission_required = 'mantenimiento.can_ver_herramientas'
    template_name = 'components/form_delete_item_sale.html'
    model = m.ItemVenta

    def get_success_url(self):
        venta = self.object.venta.id
        return reverse_lazy('gestionVentas:sale_detail', kwargs={'pk': venta})


class CrearItemVenta(generic.FormView):
    # permission_required = 'mantenimiento.can_create_cotizacion'
    template_name = 'components/form_crear_item_venta.html'
    model = m.ItemVenta
    form_class = f.NuevoItemVeta  

    def get_context_data(self, **kwargs):
        kwargs.update({
            'id_cotizacion': self.kwargs['pk'],

        })
        return super().get_context_data(**kwargs)

    def obtenerids(self, cadena):
        codigos = cadena.split(",")
        ids = []
        for codigo in codigos:
            try:
                inicio = codigo.find('[')
                fin = codigo.find(']')
                if inicio >= 0:
                    ids.append(codigo[inicio+1:fin])
            except Exception as e:
                print(e)
                pass

        return ids

    def form_valid(self, form, **kwargs):
        venta_id = self.kwargs['pk']
        productos = self.request.POST['repuestos']
        listaids = self.obtenerids(productos)
        for numid in listaids:
            item_venta = m.ItemVenta.objects.create(
                cantidad=1,
                producto_id=numid,
                venta_id=venta_id,)
        item_venta.save()

        return HttpResponseRedirect(reverse_lazy(
            'gestionVentas:sale_detail',
            kwargs={'pk': venta_id}))

    def form_invalid(self, form):
        return JsonResponse(
            {'status': 'error', 'errors': form.errors},
            status=400)

    def post(self, request: HttpRequest, *args: str,
             **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ActualizarItemVenta(generic.UpdateView):
    template_name = 'components/form_update_sale_item.html'
    model = m.ItemVenta
    form_class = f.NuevoItemVeta

    def get_context_data(self, **kwargs):
        kwargs.update({
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        itemVenta = self.get_object()
        cantidad = form.cleaned_data["cantidad"]
        itemVenta.cantidad = cantidad
        if itemVenta.producto.tiene_iva:
            itemVenta.iva = float(cantidad)*float(itemVenta.producto.porcentaje_iva)*float(itemVenta.producto.valor_venta)
            
            itemVenta.valor = float(itemVenta.iva) + (float(cantidad) *float(itemVenta.producto.valor_venta))
        else:
            itemVenta.valor = float(cantidad) * float(itemVenta.producto.valor_venta)
        itemVenta.save()
        print(itemVenta.cantidad)
        print(itemVenta.iva)
        print(itemVenta.valor)

        return HttpResponseRedirect(reverse_lazy(
            'gestionVentas:sale_detail',
            kwargs={'pk': itemVenta.venta.id}))

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors},
                            status=400)

    def post(self, request: HttpRequest, *args: str,
             **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ActualizarDatosVenta(generic.UpdateView):
    template_name = 'components/form_update_sale.html'
    model = m.Venta
    form_class = f.ActualizarDatosVentaForm

    def get_context_data(self, **kwargs):
        kwargs.update({
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        producto = self.get_object()
        if form.cleaned_data["fecha_venta"] is  not None:
            producto.fecha_venta = form.cleaned_data["fecha_venta"]
        producto.cliente = form.cleaned_data["cliente"]
        producto.save()

        return HttpResponseRedirect(reverse_lazy(
            'gestionVentas:sale_detail',
            kwargs={'pk': self.get_object().id}))

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors},
                            status=400)

    def post(self, request: HttpRequest, *args: str,
             **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ReporteVentasView(generic.View):

    def get(self, request):
        data = s.descargar_reporte_all_ventas()
        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=reporte_ventas.xlsx'
        return response


class ReporteProductosView(generic.View):

    def get(self, request):
        data = s.descargar_reporte_all_products()
        response = HttpResponse(data.export('xlsx'), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=reporte_productos.xlsx'
        return response


class ConfirmarVentaView(generic.UpdateView):
    # permission_required = 'mantenimiento.can_ver_solicitudes'
    template_name = 'components/form_confirm_sale.html'
    model = m.Venta
    form_class = f.ActualizarDatosVentaForm

    def get_context_data(self, **kwargs):
        kwargs.update({
        })
        return super().get_context_data(**kwargs)
    
    def Actualizar_inventario(self,):
        items = m.ItemVenta.objects.filter(venta=self.get_object())
        for item in items:
            cantidad = item.cantidad
            item.producto.cantidad=item.producto.cantidad-cantidad
            item.producto.save()

    def post(self, request: HttpRequest, *args: str,
             **kwargs: Any) -> HttpResponse:
        confirmacion=request.POST['confirmacion']
        # print(confirmacion)
        if confirmacion == 'yes':
            self.Actualizar_inventario()

        return HttpResponseRedirect(reverse_lazy(
            'gestionVentas:sale_detail',
            kwargs={'pk': self.get_object().id}))