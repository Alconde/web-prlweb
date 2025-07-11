# Generated by Django 5.2 on 2025-07-01 15:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0025_documentotipo_investigacion_procedimiento'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Accidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True)),
                ('descripcion', models.TextField()),
                ('gravedad', models.CharField(choices=[('LEVE', 'Leve'), ('GRAVE', 'Grave'), ('MUY_GRAVE', 'Muy Grave')], max_length=10)),
                ('empleado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='AccionCorrectiva',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=200)),
                ('descripcion', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvestigacionAccidente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_investigacion', models.DateField(auto_now_add=True)),
                ('causas_inmediatas', models.TextField()),
                ('causas_raiz', models.TextField()),
                ('accidente', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='gestion.accidente')),
                ('acciones', models.ManyToManyField(blank=True, to='gestion.accioncorrectiva')),
            ],
        ),
        migrations.CreateModel(
            name='ProcedimientoInvestigacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archivo', models.FileField(blank=True, help_text='Sube aquí el PDF del procedimiento de investigación', null=True, upload_to='investigaciones/')),
            ],
        ),
        migrations.DeleteModel(
            name='Procedimiento',
        ),
    ]
