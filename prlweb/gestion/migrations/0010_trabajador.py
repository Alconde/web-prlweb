# Generated by Django 5.2 on 2025-06-25 16:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0009_remove_puestotrabajo_medidas_preventivas_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('apellidos', models.CharField(max_length=150)),
                ('dni', models.CharField(max_length=9, unique=True)),
                ('puesto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gestion.puestotrabajo')),
            ],
        ),
    ]
