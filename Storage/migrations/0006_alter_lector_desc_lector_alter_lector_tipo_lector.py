# Generated by Django 5.1.3 on 2025-05-09 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Storage', '0005_expedientehistorico'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lector',
            name='desc_lector',
            field=models.CharField(max_length=150),
        ),
        migrations.AlterField(
            model_name='lector',
            name='tipo_lector',
            field=models.CharField(max_length=150),
        ),
    ]
