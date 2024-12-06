from django.urls import path
from . import views
from . import api_views

app_name = 'abm'
urlpatterns = [
    path(
        'customer_list',
        views.listarClientes.as_view(),
        name='customer_list'),
    path(
        'user_list',
        views.listarUsuarios.as_view(),
        name='user_list'),
    path(
        'add_customer',
        views.RegistrarClienteView.as_view(),
        name='add_customer'),
    path(
        'api/customers/',
        api_views.ListarClientesView.as_view(),
        name='customers_list_api'),
    path(
        'aupdate_customer/<int:pk>/',
        views.ActualizarClienteView.as_view(),
        name='update_customer'),
    path(
        'delete_customer/<pk>/',
        views.EliminarClienteView.as_view(),
        name='delete_customer_view'),
]