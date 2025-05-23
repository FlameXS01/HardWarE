# Generated by Django 5.1.3 on 2025-05-05 20:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chasis',
            fields=[
                ('id_chasis', models.BigAutoField(primary_key=True, serialize=False)),
                ('tipo_chasis', models.CharField(max_length=50)),
                ('serial_board', models.CharField(max_length=50, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entidad',
            fields=[
                ('id_entidad', models.BigAutoField(primary_key=True, serialize=False)),
                ('tipoEntidad', models.CharField(max_length=50)),
                ('nombre', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Almacenamiento',
            fields=[
                ('id_almacenamiento', models.BigAutoField(primary_key=True, serialize=False)),
                ('no_serie_alm', models.CharField(max_length=100, unique=True)),
                ('tipo_alm', models.CharField(max_length=50)),
                ('interface_alm', models.CharField(max_length=50)),
                ('modelo_alm', models.CharField(max_length=50)),
                ('capacidad_alm', models.BigIntegerField()),
                ('id_chasis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Storage.chasis')),
            ],
        ),
        migrations.CreateModel(
            name='Fuente',
            fields=[
                ('id_fuente', models.BigAutoField(primary_key=True, serialize=False)),
                ('fabricante_fuente', models.CharField(max_length=50)),
                ('no_serie_fuente', models.CharField(max_length=50)),
                ('potencia_fuente', models.CharField(max_length=50)),
                ('id_chasis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Storage.chasis')),
            ],
        ),
        migrations.CreateModel(
            name='Lector',
            fields=[
                ('id_lector', models.BigAutoField(primary_key=True, serialize=False)),
                ('desc_lector', models.CharField(max_length=50)),
                ('tipo_lector', models.CharField(max_length=50)),
                ('id_chasis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Storage.chasis')),
            ],
        ),
        migrations.CreateModel(
            name='Pc',
            fields=[
                ('id_pc', models.BigAutoField(primary_key=True, serialize=False)),
                ('serial_pc', models.CharField(max_length=50, unique=True)),
                ('so', models.CharField(max_length=50)),
                ('nombre_equipo', models.CharField(max_length=50)),
                ('ultimo_reporte', models.DateField()),
                ('id_chasis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='pc', to='Storage.chasis')),
                ('id_entidad', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Storage.entidad')),
            ],
        ),
        migrations.CreateModel(
            name='Incidencias',
            fields=[
                ('id_incidencia', models.BigAutoField(primary_key=True, serialize=False)),
                ('desc_incidencia', models.CharField(max_length=50)),
                ('fecha_incidencia', models.CharField(max_length=50)),
                ('observacion', models.CharField(max_length=50)),
                ('id_pc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Storage.pc')),
            ],
        ),
        migrations.CreateModel(
            name='Perifericos',
            fields=[
                ('id_periferico', models.BigAutoField(primary_key=True, serialize=False)),
                ('tipo_periferico', models.CharField(max_length=50)),
                ('no_serie_periferico', models.CharField(max_length=50)),
                ('fabricante_periferico', models.CharField(max_length=50)),
                ('modelo_periferico', models.CharField(max_length=50)),
                ('id_pc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Storage.pc')),
            ],
        ),
        migrations.CreateModel(
            name='Placa_Base',
            fields=[
                ('id_placa', models.BigAutoField(primary_key=True, serialize=False)),
                ('no_serie_placa', models.CharField(max_length=50)),
                ('fabricante_placa', models.CharField(max_length=50)),
                ('modelo_placa', models.CharField(max_length=50)),
                ('id_chasis', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Storage.chasis')),
            ],
        ),
        migrations.CreateModel(
            name='Procesador',
            fields=[
                ('id_procesador', models.BigAutoField(primary_key=True, serialize=False)),
                ('desc_procesador', models.CharField(max_length=100)),
                ('velocidad_procesador', models.IntegerField()),
                ('arq_procesador', models.CharField(max_length=50)),
                ('id_placa', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Storage.placa_base')),
            ],
        ),
        migrations.CreateModel(
            name='Ram',
            fields=[
                ('id_ram', models.BigAutoField(primary_key=True, serialize=False)),
                ('capacidad_ram', models.IntegerField()),
                ('no_serie_ram', models.CharField(max_length=50)),
                ('tipo_ram', models.CharField(max_length=50)),
                ('id_placa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Storage.placa_base')),
            ],
        ),
        migrations.CreateModel(
            name='Ranura_Expansion',
            fields=[
                ('id_ranuras_expansion', models.BigAutoField(primary_key=True, serialize=False)),
                ('id_slot', models.IntegerField()),
                ('id_board', models.CharField(max_length=50)),
                ('conector_ranura', models.CharField(max_length=50)),
                ('uso', models.CharField(max_length=50)),
                ('id_chasis', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Storage.chasis')),
            ],
        ),
        migrations.CreateModel(
            name='Tarjeta_Red',
            fields=[
                ('id_tarjeta', models.BigAutoField(primary_key=True, serialize=False)),
                ('mac', models.CharField(max_length=50)),
                ('ip', models.CharField(max_length=50)),
                ('subnet', models.CharField(max_length=50)),
                ('gateway', models.CharField(max_length=50)),
                ('id_placa', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Storage.placa_base')),
            ],
        ),
    ]
