from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views import generic
from django.http import HttpRequest, HttpResponseRedirect
from django.urls import reverse_lazy
from django.http.response import HttpResponse, JsonResponse
from typing import Any
from . import models as m
from . import forms as f
# Create your views here.
class listarClientes(generic.ListView):
    model = m.Clientes
    template_name = 'abm/customer_list.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'clientes': m.Clientes.objects.all(),
            #'estados': m.Herramienta.EstadoHettaEnum.choices,
        })
        return super().get_context_data(**kwargs)

class listarUsuarios(generic.ListView):
    model = m.Clientes
    template_name = 'abm/user_list.html'

    def get_context_data(self, **kwargs):
        kwargs.update({
            'clientes': m.Clientes.objects.all(),
            #'estados': m.Herramienta.EstadoHettaEnum.choices,
        })
        return super().get_context_data(**kwargs)
    
class RegistrarClienteView(generic.FormView):
    #permission_required = 'mantenimiento.can_ver_orden_trabajo'
    template_name = 'components/form_new_customer.html'
    model = m.Clientes
    form_class = f.RegistrarClienteForm

    def get_context_data(self, **kwargs):
        kwargs.update({
            #'form': f.OrdenDeTrabajoForm,
            #'clientes': m_abm.Cliente.objects.all(),
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        nombre = form.cleaned_data["nombre"]
        email = form.cleaned_data["email"]
        telefono = form.cleaned_data["telefono"]
        direccion = form.cleaned_data["direccion"]
        cliente = m.Clientes.objects.create(
            nombre=nombre,
            email=email,
            telefono=telefono,
            direccion=direccion,
            )
        cliente.save()        

        return HttpResponseRedirect(reverse_lazy('abm:customer_list'))

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors},
                            status=400)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class ActualizarClienteView(generic.UpdateView):
    template_name = 'components/form_update_customer.html'
    model = m.Clientes
    form_class = f.RegistrarClienteForm

    def get_context_data(self, **kwargs):
        kwargs.update({
        })
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        cliente = self.get_object()
        cliente.nombre = form.cleaned_data['nombre']
        cliente.direccion = form.cleaned_data['direccion']
        cliente.telefono = form.cleaned_data['telefono']
        cliente.email = form.cleaned_data['email']
        cliente.save()
       
        return HttpResponseRedirect(reverse_lazy(
            'abm:customer_list'))

    def form_invalid(self, form):
        return JsonResponse({'status': 'error', 'errors': form.errors},
                            status=400)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        form = self.form_class(request.POST,request.FILES)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        
class EliminarClienteView(generic.DeleteView):
    # permission_required = 'mantenimiento.can_ver_herramientas'
    template_name = 'components/form_delete_customer.html'
    model = m.Clientes
    success_url = reverse_lazy('abm:customer_list')