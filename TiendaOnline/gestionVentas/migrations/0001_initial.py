# Generated by Django 5.1.3 on 2024-12-04 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(max_length=20)),
                ('nombre', models.CharField(max_length=30)),
                ('valor_venta', models.CharField(max_length=50, verbose_name='Domicilio Cliente')),
                ('tiene_iva', models.BooleanField(default=False, null=True)),
                ('porcentaje_iva', models.FloatField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'permissions': [('can_read_producto', 'Puede ver producto')],
            },
        ),
    ]