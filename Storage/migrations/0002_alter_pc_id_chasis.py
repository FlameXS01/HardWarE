# Generated by Django 5.1.3 on 2025-05-06 13:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Storage', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pc',
            name='id_chasis',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Storage.chasis'),
        ),
    ]
