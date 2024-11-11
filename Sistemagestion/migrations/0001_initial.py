# Generated by Django 5.1.1 on 2024-11-03 00:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Administrador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('edad', models.PositiveSmallIntegerField()),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
                'db_table': 'administrador',
            },
        ),
        migrations.CreateModel(
            name='Boleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('total', models.IntegerField()),
            ],
            options={
                'verbose_name': 'Boleta',
                'verbose_name_plural': 'Boletas',
                'db_table': 'boleta',
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('precio', models.IntegerField()),
                ('stock', models.PositiveIntegerField()),
                ('estado', models.CharField(choices=[('Disponible', 'Disponible'), ('No Disponible', 'No Disponible')], max_length=15)),
                ('descuento', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'producto',
            },
        ),
        migrations.CreateModel(
            name='InformeCierre',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateTimeField()),
                ('ventas_total', models.IntegerField()),
                ('stock_actual', models.PositiveIntegerField()),
                ('boletas_emitidas', models.PositiveIntegerField()),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistemagestion.administrador')),
            ],
            options={
                'verbose_name': 'Informe de Cierre',
                'verbose_name_plural': 'Informes de Cierre',
                'db_table': 'informecierre',
            },
        ),
        migrations.CreateModel(
            name='DetalleBoleta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cantidad', models.PositiveIntegerField()),
                ('precio_unitario', models.IntegerField()),
                ('subtotal', models.IntegerField()),
                ('boleta', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistemagestion.boleta')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Sistemagestion.producto')),
            ],
            options={
                'verbose_name': 'Detalle de Boleta',
                'verbose_name_plural': 'Detalles de Boletas',
                'db_table': 'detalleboleta',
            },
        ),
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('rut', models.CharField(max_length=12, unique=True)),
                ('edad', models.PositiveSmallIntegerField()),
                ('administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistemagestion.administrador')),
            ],
            options={
                'verbose_name': 'Trabajador',
                'verbose_name_plural': 'Trabajadores',
                'db_table': 'trabajador',
            },
        ),
        migrations.CreateModel(
            name='LogVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_hora', models.DateTimeField()),
                ('tipo_accion', models.CharField(choices=[('Creación', 'Creación'), ('Modificación', 'Modificación'), ('Eliminación', 'Eliminación')], max_length=15)),
                ('descripcion', models.TextField()),
                ('informe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistemagestion.informecierre')),
                ('trabajador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Sistemagestion.trabajador')),
            ],
            options={
                'verbose_name': 'Log de Venta',
                'verbose_name_plural': 'Logs de Venta',
                'db_table': 'logventa',
            },
        ),
        migrations.AddField(
            model_name='boleta',
            name='trabajador',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='Sistemagestion.trabajador'),
        ),
    ]
