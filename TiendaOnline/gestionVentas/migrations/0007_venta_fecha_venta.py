# Generated by Django 5.1.3 on 2024-12-06 03:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVentas', '0006_producto_fecha_creacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='venta',
            name='fecha_venta',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
