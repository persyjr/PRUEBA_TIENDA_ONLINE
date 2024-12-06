from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.utils import timezone
from django.urls import reverse_lazy
from datetime import datetime, timedelta
from django.http import HttpRequest, HttpResponseRedirect
from django.http.response import HttpResponse, JsonResponse
from django.views import generic
from typing import Any
from abm import models as m_abm
from . import models as m
from . import forms as f
# Create your views here.
class HomeView(  generic.TemplateView):
    template_name = 'gestionVentas/landingPage.html'

class listarVentasView(generic.ListView):
    model = m.Venta
    template_name = 'gestionVentas/list_ventas.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'clientes': m_abm.Clientes.objects.all(),
            #'estados': m.Herramienta.EstadoHettaEnum.choices,
        })
        return super().get_context_data(**kwargs)

class listarProductosView(generic.ListView):
    model = m.Producto
    template_name = 'gestionVentas/product_list.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'clientes': m_abm.Clientes.objects.all(),
            #'estados': m.Herramienta.EstadoHettaEnum.choices,
        })
        return super().get_context_data(**kwargs)

class RegistrarProductoView(generic.FormView):
    #permission_required = 'mantenimiento.can_ver_orden_trabajo'
    template_name = 'components/form_new_product.html'
    model = m.Producto
    form_class = f.RegistrarProductoForm

    def get_context_data(self, **kwargs):
        kwargs.update({
            #'form': f.OrdenDeTrabajoForm,
            #'clientes': m_abm.Cliente.objects.all(),
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        codigo = form.cleaned_data["codigo"]
        nombre = form.cleaned_data["nombre"]
        valor_venta = form.cleaned_data["valor_venta"]
        tiene_iva = form.cleaned_data["tiene_iva"]
        imagen = form.cleaned_data["imagen"]
        porcentaje_iva = form.cleaned_data["porcentaje_iva"]
        producto = m.Producto.objects.create(
            codigo=codigo,
            nombre=nombre,
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

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
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
        producto.nombre = form.cleaned_data["nombre"]
        producto.valor_venta = form.cleaned_data["valor_venta"]
        producto.tiene_iva = form.cleaned_data["tiene_iva"]
        producto.imagen = form.cleaned_data["imagen"]
        producto.porcentaje_iva = form.cleaned_data["porcentaje_iva"]
        
        producto.save()
       
        return HttpResponseRedirect(reverse_lazy(
            'gestionVentas:product_list'))

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors},
                            status=400)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class EliminarProductoView(generic.DeleteView):
    # permission_required = 'mantenimiento.can_ver_herramientas'
    template_name = 'components/form_delete_product.html'
    model = m.Producto
    success_url = reverse_lazy('gestionVentas:product_list')