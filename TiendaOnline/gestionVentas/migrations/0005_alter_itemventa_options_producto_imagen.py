# Generated by Django 5.1.3 on 2024-12-05 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVentas', '0004_itemventa_venta_venta_cliente'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemventa',
            options={'permissions': [('can_crear_Item_venta', 'Puede crear Item Venta')], 'verbose_name': 'Item Venta', 'verbose_name_plural': 'Items Ventas'},
        ),
        migrations.AddField(
            model_name='producto',
            name='imagen',
            field=models.FileField(blank=True, null=True, upload_to='gestionVentas/productos'),
        ),
    ]
