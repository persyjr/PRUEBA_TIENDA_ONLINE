# Generated by Django 5.1.3 on 2024-12-04 15:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVentas', '0002_itemventa_venta'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemventa',
            options={'permissions': [('can_crear_Item_venta', 'Puede crear Item Venta')], 'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
        migrations.AlterModelOptions(
            name='venta',
            options={'permissions': [('can_crear_venta', 'Puede crear Venta')], 'verbose_name': 'Venta', 'verbose_name_plural': 'Ventas'},
        ),
    ]
