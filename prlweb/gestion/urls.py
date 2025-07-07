from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [  
    path('', views.home, name='home'),  
    path('informacion/', views.informacion_empresa, name='informacion_empresa'),
    path('instalaciones/', views.lista_instalaciones, name='lista_instalaciones'),
    path('instalaciones/nueva/', views.nueva_instalacion, name='nueva_instalacion'),
    path('instalaciones/<int:pk>/editar/', views.editar_instalacion, name='editar_instalacion'),
    path('instalaciones/<int:pk>/eliminar/', views.eliminar_instalacion, name='eliminar_instalacion'),
    path('instalaciones/<int:instalacion_id>/documento/', views.subir_documento_instalacion, name='subir_documento_instalacion'),
    path('instalaciones/<int:pk>/', views.detalle_instalacion, name='detalle_instalacion'),
    path('documento/<int:pk>/editar/', views.editar_documento_instalacion, name='editar_documento_instalacion'),
    path('documento/<int:pk>/eliminar/', views.eliminar_documento_instalacion, name='eliminar_documento_instalacion'),
    # Equipos de trabajo
    path('equipos/', views.lista_equipos, name='lista_equipos'),
    path('equipos/nuevo/', views.crear_equipo, name='nuevo_equipo'),
    path('equipos/<int:pk>/autorizacion/', views.autorizacion_equipo, name='autorizacion_equipo'),
    #path('equipos/autorizacion/', views.generar_autorizacion_general, name='autorizacion_general'),
    path('equipos/autorizacion/', views.autorizacion_general, name='autorizacion_general'),
    # Puestos de trabajo
    path('puestos/', views.lista_puestos, name='lista_puestos'),
    path('puestos/nuevo/', views.crear_puesto, name='crear_puesto'),
    path('puestos/<int:pk>/', views.detalle_puesto, name='detalle_puesto'),
    path('puestos/<int:pk>/editar/', views.editar_puesto, name='editar_puesto'),
    path('puestos/<int:pk>/eliminar/', views.eliminar_puesto, name='eliminar_puesto'),
    # Trabajadores
    path('trabajadores/', views.lista_trabajadores, name='lista_trabajadores'),
    path('trabajadores/nuevo/', views.crear_trabajador, name='crear_trabajador'),
    path('trabajadores/<int:pk>/editar/', views.editar_trabajador, name='editar_trabajador'),
    path('trabajadores/<int:pk>/eliminar/', views.eliminar_trabajador, name='eliminar_trabajador'),
    # Productos químicos
    path('productos/', views.lista_productos, name='lista_productos'),
    path('productos/nuevo/', views.crear_producto, name='crear_producto'),
    path('productos/editar/<int:pk>/', views.editar_producto, name='editar_producto'),
    path('productos/eliminar/<int:pk>/', views.eliminar_producto, name='eliminar_producto'),  
    # Plan de Prevención
    path('plan-prevencion/', views.listar_plan_prevencion, name='listar_plan_prevencion'),
    path('plan-prevencion/nuevo/', views.crear_plan_prevencion, name='crear_plan_prevencion'),
    path('plan-prevencion/<int:pk>/editar/', views.editar_plan_prevencion, name='editar_plan_prevencion'),
    # Login
    path('login/', auth_views.LoginView.as_view(template_name='gestion/login.html'), name='login'),
    # Evaluación y planificación
    path('medidas/', views.listar_medidas, name='listar_medidas'),
    path('medidas/nueva/', views.crear_medida, name='crear_medida'),
    path('medidas/<int:pk>/editar/', views.editar_medida, name='editar_medida'),
    path('medidas/<int:pk>/eliminar/', views.eliminar_medida, name='eliminar_medida'),
    path('medidas/exportar/', views.exportar_medidas_excel, name='exportar_medidas_excel'),
    path('prevencion/documentos/', views.documentos_prevencion, name='documentos_prevencion'),
    path('medidas/importar/', views.importar_medidas_excel, name='importar_medidas_excel'),
    path('evaluacion/editar/', views.editar_evaluacion, name='editar_evaluacion'),
    path('planificacion/editar/', views.editar_planificacion, name='editar_planificacion'),
    path('programa-evaluacion/', views.programa_evaluacion, name='programa_evaluacion'),
    path('evaluacion-planificacion/', views.listar_evaluacion_planificacion, name='listar_evaluacion_planificacion'),
    # Medidas de Emergencia
    path('emergencias/', views.emergencias_dashboard, name='emergencias_dashboard'),
    path('emergencias/editar_documentos/', views.editar_documentos_emergencia, name='editar_documentos_emergencia'),
    path('emergencias/editar_equipos/', views.editar_equipos_emergencia, name='editar_equipos_emergencia'),
    path('emergencias/medios_proteccion/<int:empresa_id>/', views.editar_medios_proteccion, name='editar_medios_proteccion'),
    path('emergencias/descargar_plantilla_nombramiento/', views.descargar_plantilla_nombramiento, name='descargar_plantilla_nombramiento'),
    # Investigaciones de accidentes
    path('investigaciones/', views.dashboard_investigaciones, name='dashboard_investigaciones'),
    path('investigaciones/nueva/', views.nueva_investigacion, name='nueva_investigacion'),
    path('investigaciones/lista/', views.lista_investigaciones, name='lista_investigaciones'),
    path('investigaciones/procedimiento/editar/',views.editar_procedimiento_investigacion,name='editar_procedimiento_investigacion'),
    # Epi´s
    path('epis/', views.listado_epis, name='listado_epis'),
    path('epis/seleccionar/', views.seleccionar_epis_puesto, name='seleccionar_epis_puesto'),
    path('epis/acuse/<int:trabajador_id>/', views.acuse_recibo_epi_pdf, name='acuse_recibo_epi_pdf'), 
    path('trabajador/<int:trabajador_id>/acuse-epi/', views.descargar_acuse_recibo_epi, name='descargar_acuse_recibo_epi'),
    path('puestos/<int:puesto_id>/asignar-epis/', views.asignar_epis, name='asignar_epis'),
    path('epis/editar_puesto/<int:puesto_id>/', views.editar_epis_puesto, name='editar_epis_puesto'),
    # CAE
    path('cae/', views.dashboard_cae, name='dashboard_cae'),
    path('cae/subir/', views.subir_documento_cae, name='subir_documento_cae'),




    
]
