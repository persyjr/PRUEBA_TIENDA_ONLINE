from django.urls import path
from . import views
from . import api_views

app_name = 'gestionVentas'
urlpatterns = [
    path(
        '',
        views.HomeView.as_view(),
        name='home'),
    path(
        'sales_list',
        views.listarVentasView.as_view(),
        name='sales_list'),
    path(
        'product_list',
        views.listarProductosView.as_view(),
        name='product_list'),
    path(
        'api/sales/',
        api_views.ListarVentasView.as_view(),
        name='sales_list_api'),
    path(
        'api/products/',
        api_views.ListarProductosView.as_view(),
        name='products_list_api'),
    path(
        'add_product',
        views.RegistrarProductoView.as_view(),
        name='add_product'),
    path(
        'update_product/<pk>/',
        views.ActualizarProducto.as_view(),
        name='update_product'),
    path(
        'delete_product/<pk>/',
        views.EliminarProductoView.as_view(),
        name='delete_product_view'),
]