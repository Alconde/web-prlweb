from django.contrib import admin
from .models import (
    Instalacion, DocumentoInstalacion, EquipoTrabajo, AutorizacionEquipo,
    PuestoTrabajo, Trabajador, ProductoQuimico, PlanPrevencion, Empresa, 
    MedioProteccion, EPI,     DocumentoCAE, AccesoRegistro, ReunionCAE, 
    IncidenciaCAE, RecursoPreventivo, EmergenciaPlan
   
)

admin.site.register(Empresa)
admin.site.register(Instalacion)
admin.site.register(DocumentoInstalacion)
admin.site.register(EquipoTrabajo)
admin.site.register(AutorizacionEquipo)
admin.site.register(PuestoTrabajo)
admin.site.register(Trabajador)
admin.site.register(ProductoQuimico)
admin.site.register(PlanPrevencion)
admin.site.register(MedioProteccion)
admin.site.register(EPI)
admin.site.register(DocumentoCAE)
admin.site.register(AccesoRegistro)
admin.site.register(ReunionCAE)
admin.site.register(IncidenciaCAE)
admin.site.register(RecursoPreventivo)
admin.site.register(EmergenciaPlan)

