# Generated by Django 5.1.3 on 2024-12-09 23:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestionVentas', '0009_alter_producto_valor_venta'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='cantidad',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
