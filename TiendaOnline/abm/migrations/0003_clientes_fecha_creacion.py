# Generated by Django 5.1.3 on 2024-12-05 13:47

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abm', '0002_alter_clientes_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
