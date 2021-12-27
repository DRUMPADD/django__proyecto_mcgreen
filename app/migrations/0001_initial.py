# Generated by Django 3.1.7 on 2021-12-27 21:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id_cliente', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_cliente', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=255)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Compras',
            fields=[
                ('id_compra', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('id_MovAlm', models.CharField(max_length=20)),
                ('valor_total', models.DecimalField(decimal_places=4, max_digits=19)),
                ('fecha_compra', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id_dep', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_dep', models.CharField(max_length=100)),
                ('desc_dep', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Empleados',
            fields=[
                ('id_empleado', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('ap_paterno', models.CharField(max_length=30)),
                ('ap_materno', models.CharField(max_length=30)),
                ('fecha_registro', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Imagenes',
            fields=[
                ('id_img', models.IntegerField(primary_key=True, serialize=False)),
                ('nombre_arch', models.CharField(max_length=50)),
                ('archivo', models.FileField(max_length=255, upload_to=None)),
                ('fecha_subida', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id_producto', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_producto', models.CharField(max_length=50)),
                ('descripcion', models.CharField(max_length=100)),
                ('cantidad', models.FloatField()),
                ('medida', models.CharField(max_length=15)),
                ('id_dep', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.departamento')),
                ('id_img', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.imagenes')),
            ],
        ),
        migrations.CreateModel(
            name='Movimientos_almacen',
            fields=[
                ('id_MovAlm', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tipo_mov', models.CharField(max_length=10)),
                ('origen_destino', models.CharField(max_length=50)),
                ('motivo', models.CharField(max_length=150)),
                ('fecha_mov', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Privilegios',
            fields=[
                ('id_priv', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('tipo_privilegio', models.CharField(max_length=40)),
            ],
        ),
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id_provee', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_provee', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('email', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Usuarios',
            fields=[
                ('email', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('pass_word', models.CharField(max_length=50)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.empleados')),
                ('privilegio', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.privilegios')),
            ],
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id_venta', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('valor_total', models.DecimalField(decimal_places=4, max_digits=19)),
                ('fecha_venta', models.DateField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.usuarios')),
                ('id_MovAlm', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.movimientos_almacen')),
            ],
        ),
        migrations.CreateModel(
            name='Puestos',
            fields=[
                ('id_puesto', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('nombre_puesto', models.CharField(max_length=40)),
                ('descr_p', models.CharField(max_length=255)),
                ('id_dep', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.departamento')),
            ],
        ),
        migrations.CreateModel(
            name='PRECIO_INV_VENTA',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('PRECIO_UNIT_VENTA', models.DecimalField(decimal_places=4, max_digits=19)),
                ('ID_PRODUCTO', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Mov_Ind',
            fields=[
                ('id_MovInd', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('cant_prod', models.FloatField()),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.usuarios')),
                ('id_MovAlm', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.movimientos_almacen')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.inventario')),
            ],
        ),
        migrations.CreateModel(
            name='Est_Prod',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('estado', models.CharField(max_length=20)),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.inventario')),
            ],
        ),
        migrations.AddField(
            model_name='empleados',
            name='id_img',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.imagenes'),
        ),
        migrations.AddField(
            model_name='empleados',
            name='puesto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.puestos'),
        ),
        migrations.CreateModel(
            name='detalles_ventas',
            fields=[
                ('id_detalle', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('precio_unitario', models.DecimalField(decimal_places=4, max_digits=19)),
                ('cant_xprod', models.DecimalField(decimal_places=4, max_digits=19)),
                ('id_cliente', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.clientes')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.inventario')),
                ('id_venta', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.ventas')),
            ],
        ),
        migrations.CreateModel(
            name='detalles_compras',
            fields=[
                ('id_detalle', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('precio_unitario', models.DecimalField(decimal_places=4, max_digits=19)),
                ('cant_xprod', models.DecimalField(decimal_places=4, max_digits=19)),
                ('id_compra', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.compras')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.inventario')),
                ('id_provee', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.proveedor')),
            ],
        ),
        migrations.CreateModel(
            name='cuentas_por_cobrar',
            fields=[
                ('id_cpc', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('status', models.CharField(max_length=50)),
                ('fecha_de_pago_fact', models.CharField(max_length=20)),
                ('contrarecibo', models.CharField(max_length=25)),
                ('fecha_rec_pago', models.CharField(max_length=20)),
                ('sp', models.CharField(max_length=35)),
                ('oc', models.CharField(max_length=35)),
                ('fecha', models.DateField()),
                ('pozo', models.CharField(max_length=100)),
                ('total_servicios', models.FloatField()),
                ('subtotal_usd', models.DecimalField(decimal_places=4, max_digits=19)),
                ('iva', models.DecimalField(decimal_places=4, max_digits=19)),
                ('total_usd_xservicio', models.DecimalField(decimal_places=4, max_digits=19)),
                ('monto_total', models.DecimalField(decimal_places=4, max_digits=19)),
                ('fact_no', models.CharField(max_length=35)),
                ('fecha_de_fac', models.CharField(max_length=20)),
                ('recibo_pag_fac_mcgreen', models.CharField(max_length=20)),
                ('fecha_de_rec_pago', models.CharField(max_length=20)),
                ('dllr', models.CharField(max_length=20)),
                ('monto_mxp', models.DecimalField(decimal_places=4, max_digits=19)),
                ('monto_mxp_pagado', models.DecimalField(decimal_places=4, max_digits=19)),
                ('email', models.ForeignKey(null=True, on_delete=django.db.models.deletion.RESTRICT, to='app.usuarios')),
                ('id_producto', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.inventario')),
            ],
        ),
        migrations.AddField(
            model_name='compras',
            name='email',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.usuarios'),
        ),
        migrations.CreateModel(
            name='auditoria',
            fields=[
                ('id_audit', models.AutoField(primary_key=True, serialize=False)),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('email', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app.usuarios')),
            ],
        ),
    ]
