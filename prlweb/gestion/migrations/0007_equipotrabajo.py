# Generated by Django 5.2 on 2025-06-24 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0006_documentoinstalacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='EquipoTrabajo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('marca', models.CharField(max_length=100)),
                ('modelo', models.CharField(max_length=100)),
                ('numero_serie', models.CharField(max_length=100)),
                ('marcado_ce', models.BooleanField(default=True)),
                ('declaracion_ce', models.FileField(blank=True, null=True, upload_to='equipos/declaraciones_ce/')),
                ('manual_instrucciones', models.FileField(blank=True, null=True, upload_to='equipos/manuales/')),
                ('requiere_mantenimiento', models.BooleanField(default=False)),
                ('fecha_mantenimiento', models.DateField(blank=True, null=True)),
                ('frecuencia_mantenimiento_dias', models.PositiveIntegerField(default=365)),
            ],
        ),
    ]
