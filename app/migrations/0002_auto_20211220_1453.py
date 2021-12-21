# Generated by Django 3.1.7 on 2021-12-20 20:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='sistemas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_sist', models.CharField(max_length=100)),
                ('porcentaje', models.CharField(max_length=30)),
                ('descripcion', models.CharField(max_length=100)),
                ('cantidad', models.FloatField()),
                ('p_v_noiva_usd_unit', models.FloatField()),
            ],
        ),
        migrations.RemoveField(
            model_name='cuentas_por_cobrar',
            name='justificacion',
        ),
        migrations.AddField(
            model_name='cuentas_por_cobrar',
            name='email',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.usuarios'),
        ),
        migrations.AddField(
            model_name='cuentas_por_cobrar',
            name='id_sist',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.sistemas'),
        ),
    ]