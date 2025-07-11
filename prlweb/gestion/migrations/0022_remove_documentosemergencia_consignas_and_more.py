# Generated by Django 5.2 on 2025-06-28 18:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestion', '0021_rename_documentoemergencia_documentosemergencia'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='documentosemergencia',
            name='consignas',
        ),
        migrations.RemoveField(
            model_name='documentosemergencia',
            name='documento_designacion',
        ),
        migrations.RemoveField(
            model_name='documentosemergencia',
            name='nombre',
        ),
        migrations.RemoveField(
            model_name='documentosemergencia',
            name='simulacros',
        ),
        migrations.AddField(
            model_name='documentosemergencia',
            name='certificados_formacion',
            field=models.FileField(blank=True, null=True, upload_to='emergencias/'),
        ),
        migrations.AddField(
            model_name='documentosemergencia',
            name='consignas_emergencia',
            field=models.FileField(blank=True, null=True, upload_to='emergencias/'),
        ),
        migrations.AddField(
            model_name='documentosemergencia',
            name='nombramientos',
            field=models.FileField(blank=True, null=True, upload_to='emergencias/'),
        ),
        migrations.AddField(
            model_name='documentosemergencia',
            name='registro_simulacros',
            field=models.FileField(blank=True, null=True, upload_to='emergencias/'),
        ),
        migrations.AlterField(
            model_name='documentosemergencia',
            name='plan_emergencia',
            field=models.FileField(blank=True, null=True, upload_to='emergencias/'),
        ),
    ]
