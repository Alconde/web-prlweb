from django.shortcuts import render, redirect, get_object_or_404
from .models import (Instalacion, DocumentoInstalacion, EquipoTrabajo, PuestoTrabajo, Trabajador, 
                     ProductoQuimico, PlanPrevencion, MedidaPreventiva, DocumentosPrevencion, 
                     DocumentosEmergencia, EquipoEmergencia, MedioProteccion, EmpresaMedioProteccion,
                     Empresa, ProcedimientoInvestigacion, InvestigacionAccidente,EquipoProteccionIndividual, 
                     EPIPuesto, EPI ,DocumentoCAE, AccesoRegistro, ReunionCAE, IncidenciaCAE, RecursoPreventivo, 
                     EmergenciaPlan, DocumentoCAE, Empresa, 
                    )
from .forms import (InstalacionForm, DocumentoInstalacionForm, EquipoTrabajoForm, EquipoTrabajo, 
                    PuestoTrabajoForm, TrabajadorForm, ProductoQuimicoForm, PlanPrevencionForm, 
                    MedidaPreventivaForm, DocumentosPrevencionForm, ImportarExcelForm, DocumentosEmergenciaForm,
                    MedioProteccionForm, EmpresaMedioProteccionForm, EquipoEmergenciaForm,InvestigacionForm, 
                    ProcedimientoInvestigacionForm, EPISelectionForm, AsignarEPIForm, AsignarEpisPuestoForm,
                    EditarEpisPuestoForm, DocumentoCAEForm
                    )



from django.utils import timezone
from django.core.mail import send_mail
from reportlab.lib.pagesizes import A4
from django.template.loader import render_to_string
import io
from reportlab.pdfgen import canvas
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from prlweb.utils.generar_plantilla import crear_plantilla
from django.conf import settings
import os
from django.http import FileResponse, Http404
from datetime import date
from django.http import FileResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
import csv
from django.http import HttpResponse
import pandas as pd
from django.contrib import messages
from openpyxl import Workbook
from django.db import models
from django.db.models.functions import Length
from django.db.models import Q
from .filters import DocumentoCAEFilter

def home(request):
    return render(request, 'gestion/home.html')

# Información empresa
def informacion_empresa(request):
    return render(request, 'gestion/informacion_empresa.html')

# Gestión instalaciones

@login_required
def nueva_instalacion(request):
    if request.method == 'POST':
        form = InstalacionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_instalaciones')  # Crearás esta vista después
    else:
        form = InstalacionForm()
    return render(request, 'gestion/nueva_instalacion.html', {'form': form})

@login_required
def lista_instalaciones(request):
    instalaciones = Instalacion.objects.all()
    return render(request, 'gestion/lista_instalaciones.html', {'instalaciones': instalaciones})

@login_required
def editar_instalacion(request, pk):
    instalacion = get_object_or_404(Instalacion, pk=pk)
    if request.method == 'POST':
        form = InstalacionForm(request.POST, request.FILES, instance=instalacion)
        if form.is_valid():
            form.save()
            return redirect('lista_instalaciones')
    else:
        form = InstalacionForm(instance=instalacion)
    return render(request, 'gestion/editar_instalacion.html', {'form': form})

@login_required
def eliminar_instalacion(request, pk):
    instalacion = get_object_or_404(Instalacion, pk=pk)
    if request.method == 'POST':
        instalacion.delete()
        return redirect('lista_instalaciones')
    return render(request, 'gestion/eliminar_instalacion.html', {'instalacion': instalacion})

# subir documentos
def subir_documento_instalacion(request, instalacion_id):
    instalacion = get_object_or_404(Instalacion, id=instalacion_id)

    if request.method == 'POST':
        form = DocumentoInstalacionForm(request.POST, request.FILES, instalacion=instalacion)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.instalacion = instalacion
            documento.save()
            return redirect('detalle_instalacion', pk=instalacion.pk)
    else:
        form = DocumentoInstalacionForm(instalacion=instalacion)

    return render(request, 'gestion/subir_documento.html', {'form': form, 'instalacion': instalacion})

# Detalle de la instalación
@login_required
def detalle_instalacion(request, pk):
    instalacion = get_object_or_404(Instalacion, pk=pk)
    return render(request, 'gestion/detalle_instalacion.html', {'instalacion': instalacion})

# editar y eliminar documentos de la instalación
@login_required
def editar_documento_instalacion(request, pk):
    documento = get_object_or_404(DocumentoInstalacion, pk=pk)
    if request.method == 'POST':
        form = DocumentoInstalacionForm(request.POST, request.FILES, instance=documento, instalacion=documento.instalacion)
        if form.is_valid():
            form.save()
            return redirect('detalle_instalacion', pk=documento.instalacion.pk)
    else:
        form = DocumentoInstalacionForm(instance=documento, instalacion=documento.instalacion)
    return render(request, 'gestion/editar_documento.html', {'form': form, 'documento': documento})

@login_required
def eliminar_documento_instalacion(request, pk):
    documento = get_object_or_404(DocumentoInstalacion, pk=pk)
    instalacion_id = documento.instalacion.pk
    if request.method == 'POST':
        documento.delete()
        return redirect('detalle_instalacion', pk=instalacion_id)
    return render(request, 'gestion/eliminar_documento.html', {'documento': documento})

# Equipos de trabajo
@login_required
def lista_equipos(request):
    equipos = EquipoTrabajo.objects.all()
    return render(request, 'gestion/listar_equipos.html', {'equipos': equipos})

@login_required
def crear_equipo(request):
    if request.method == 'POST':
        form = EquipoTrabajoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_equipos')
    else:
        form = EquipoTrabajoForm()
    return render(request, 'gestion/formulario_equipos.html', {'form': form})

def autorizacion_equipo(request, pk):
    equipo = get_object_or_404(EquipoTrabajo, pk=pk)
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 12)
    p.drawString(50, 800, f"Autorización de uso del equipo: {equipo.nombre}")
    p.drawString(50, 780, f"Marca: {equipo.marca}")
    p.drawString(50, 760, f"Modelo: {equipo.modelo}")
    p.drawString(50, 740, f"Nº Serie: {equipo.numero_serie}")
    p.drawString(50, 720, f"Marcado CE: {'Sí' if equipo.marcado_ce else 'No'}")
    p.drawString(50, 700, f"Último mantenimiento: {equipo.fecha_mantenimiento or 'No registrado'}")
    p.drawString(50, 680, f"Próxima revisión: {equipo.proxima_revision or 'No aplica'}")
    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename=f"autorizacion_{equipo.pk}.pdf")

def generar_autorizacion_general(request):
    equipos = EquipoTrabajo.objects.all()
    buffer = BytesIO()
    p = canvas.Canvas(buffer)
    p.setTitle("Autorización general de equipos")

    p.drawString(100, 800, "Autorización de uso de equipos de trabajo")
    y = 780
    for equipo in equipos:
        p.drawString(100, y, f"- {equipo.nombre} ({equipo.marca}, modelo {equipo.modelo})")
        y -= 20
        if y < 100:
            p.showPage()
            y = 800

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename="autorizacion_general_equipos.pdf")






def autorizacion_general(request):
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Datos fijos (esto se puede modificar para que sea dinámico)
    empresa = "EMPRESA DEMO SL"
    representante = "Nombre del Responsable"
    dni_rep = "12345678X"
    trabajador = "Nombre del Trabajador"
    dni_trabajador = "87654321Z"

    # Encabezado
    p.setFont("Helvetica-Bold", 12)
    p.drawString(100, 800, "AUTORIZACIÓN DE USO DE MAQUINARIA Y DECLARACIÓN DE ESTADO ÓPTIMO DE CONSERVACIÓN Y MANTENIMIENTO")

    # Cuerpo
    p.setFont("Helvetica", 10)
    texto = f"""
D. {representante}, con DNI: {dni_rep}, como representante de la empresa {empresa},
autorizo a D. {trabajador}, DNI: {dni_trabajador}, como operario de esta empresa, al manejo y uso de la siguiente maquinaria/herramienta:
"""
    p.drawString(50, 770, texto.strip())

    # Listado de equipos
    equipos = EquipoTrabajo.objects.all()
    y = 740
    for equipo in equipos:
        p.drawString(70, y, f"- {equipo.nombre} ({equipo.marca} {equipo.modelo})")
        y -= 15
        if y < 100:
            p.showPage()
            y = 800

    texto2 = """
Para las cuales, ha recibido la correspondiente formación y se le ha hecho entrega del manual de instrucciones y riesgos de las mismas.
Así mismo, se compromete a conservar y realizar el mantenimiento de las máquinas/herramientas respetando siempre las indicaciones del fabricante
y la normativa vigente, así como a conocer y respetar el manual de instrucciones o libro de usuario y especialmente las normas de seguridad.
"""
    p.drawString(50, y - 30, texto2.strip())

    hoy = date.today()
    p.drawString(50, y - 80, f"En _____________________, a {hoy.day} de {hoy.strftime('%B')} de {hoy.year}.")

    # Firmas
    p.drawString(50, y - 110, "Firma/Sello empresa:")
    p.drawString(300, y - 110, "Firma trabajador:")
    p.drawString(50, y - 130, f"D. {representante}")
    p.drawString(300, y - 130, f"D. {trabajador}")

    p.showPage()
    p.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=False, filename='autorizacion_uso_maquinaria.pdf')

# Puestos de trabajo
@login_required
def lista_puestos(request):
    puestos = PuestoTrabajo.objects.all()
    return render(request, 'gestion/listar_puestos.html', {'puestos': puestos})

@login_required
def crear_puesto(request):
    if request.method == 'POST':
        form = PuestoTrabajoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_puestos')
    else:
        form = PuestoTrabajoForm()
    return render(request, 'gestion/formulario_puesto.html', {'form': form})

@login_required
def detalle_puesto(request, pk):
    puesto = get_object_or_404(PuestoTrabajo, pk=pk)
    return render(request, 'gestion/detalle_puesto.html', {'puesto': puesto})

@login_required
def editar_puesto(request, pk):
    puesto = get_object_or_404(PuestoTrabajo, pk=pk)
    if request.method == 'POST':
        form = PuestoTrabajoForm(request.POST, instance=puesto)
        if form.is_valid():
            form.save()
            return redirect('detalle_puesto', pk=pk)
    else:
        form = PuestoTrabajoForm(instance=puesto)
    return render(request, 'gestion/formulario_puesto.html', {'form': form})

@login_required
def eliminar_puesto(request, pk):
    puesto = get_object_or_404(PuestoTrabajo, pk=pk)
    if request.method == 'POST':
        puesto.delete()
        return redirect('lista_puestos')
    return render(request, 'gestion/confirmar_eliminar_puesto.html', {'puesto': puesto})

# Trabajadores
@login_required
def lista_trabajadores(request):
    trabajadores = Trabajador.objects.all()
    return render(request, 'gestion/listar_trabajadores.html', {'trabajadores': trabajadores})

@login_required
def crear_trabajador(request):
    if request.method == 'POST':
        form = TrabajadorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_trabajadores')
    else:
        form = TrabajadorForm()
    return render(request, 'gestion/formulario_trabajador.html', {'form': form})

@login_required
def editar_trabajador(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    if request.method == 'POST':
        form = TrabajadorForm(request.POST, instance=trabajador)
        if form.is_valid():
            form.save()
            return redirect('lista_trabajadores')
    else:
        form = TrabajadorForm(instance=trabajador)
    return render(request, 'gestion/formulario_trabajador.html', {'form': form})

@login_required
def eliminar_trabajador(request, pk):
    trabajador = get_object_or_404(Trabajador, pk=pk)
    if request.method == 'POST':
        trabajador.delete()
        return redirect('lista_trabajadores')
    return render(request, 'gestion/confirmar_eliminar_trabajador.html', {'trabajador': trabajador})

# Productos químicos
@login_required
def lista_productos(request):
    productos = ProductoQuimico.objects.all()
    return render(request, 'gestion/listar_productos.html', {'productos': productos})

def crear_producto(request):
    form = ProductoQuimicoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('lista_productos')
    return render(request, 'gestion/formulario_producto.html', {'form': form})

@login_required
def editar_producto(request, pk):
    producto = get_object_or_404(ProductoQuimico, pk=pk)
    form = ProductoQuimicoForm(request.POST or None, request.FILES or None, instance=producto)
    if form.is_valid():
        form.save()
        return redirect('lista_productos')
    return render(request, 'gestion/formulario_producto.html', {'form': form})

@login_required
def eliminar_producto(request, pk):
    producto = get_object_or_404(ProductoQuimico, pk=pk)
    if request.method == 'POST':
        producto.delete()
        return redirect('lista_productos')
    return render(request, 'gestion/confirmar_eliminar_producto.html', {'producto': producto})

# Plan de Prevención
@login_required
def crear_plan_prevencion(request):
    if request.method == 'POST':
        form = PlanPrevencionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('listar_plan_prevencion')
    else:
        form = PlanPrevencionForm()
    return render(request, 'gestion/crear_plan_prevencion.html', {'form': form})

@login_required
def listar_plan_prevencion(request):
    empresa = request.user.perfil.empresa
    plan = PlanPrevencion.objects.filter(empresa=empresa).first()    
    return render(request, 'gestion/listar_plan_prevencion.html', {'plan': plan})

@login_required
def editar_plan_prevencion(request, pk):
    plan = get_object_or_404(PlanPrevencion, pk=pk)
    if request.method == 'POST':
        form = PlanPrevencionForm(request.POST, request.FILES, instance=plan)
        if form.is_valid():
            form.save()
            return redirect('listar_plan_prevencion')
    else:
        form = PlanPrevencionForm(instance=plan)
    return render(request, 'plan_prevencion/formulario_plan.html', {'form': form})

# Evaluación y Planificación


def listar_medidas(request):
    documentos = DocumentosPrevencion.objects.first()
    medidas = MedidaPreventiva.objects.all()
    return render(request, 'gestion/listar_evaluacion_planificacion.html', {
        'documentos': documentos,
        'medidas': medidas
    })

def crear_medida(request):
    form = MedidaPreventivaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('listar_medidas')
    return render(request, 'gestion/formulario_medida.html', {'form': form})

def editar_medida(request, pk):
    medida = get_object_or_404(MedidaPreventiva, pk=pk)
    form = MedidaPreventivaForm(request.POST or None, instance=medida)
    if form.is_valid():
        form.save()
        return redirect('listar_medidas')
    return render(request, 'gestion/formulario_medida.html', {'form': form})

def eliminar_medida(request, pk):
    medida = get_object_or_404(MedidaPreventiva, pk=pk)
    if request.method == 'POST':
        medida.delete()
        return redirect('listar_medidas')
    return render(request, 'gestion/confirmar_eliminar_medida.html', {'medida': medida})



def exportar_medidas_excel(request):
    # Crear un libro de Excel
    wb = Workbook()
    ws = wb.active
    ws.title = "Medidas Preventivas"

    # Escribir encabezados
    ws.append(['Medida Preventiva', 'Plazo', 'Responsable', 'Coste', 'Estado'])

    # Añadir datos
    for medida in MedidaPreventiva.objects.all():
        ws.append([
            medida.medida,
            medida.plazo.strftime("%d/%m/%Y") if medida.plazo else "",
            medida.responsable,
            medida.coste,
            medida.get_estado_display()
        ])

    # Crear respuesta HTTP con el contenido del Excel
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="medidas.xlsx"'

    # Guardar el libro en la respuesta
    wb.save(response)
    return response






@login_required
def importar_medidas_excel(request):
    if request.method == 'POST':
        form = ImportarExcelForm(request.POST, request.FILES)
        if form.is_valid():
            archivo = request.FILES['archivo']

            # Leer el Excel con pandas
            df = pd.read_excel(archivo)

            # Esperamos columnas: Descripción, Plazo, Responsable, Coste, Estado
            for _, row in df.iterrows():
                MedidaPreventiva.objects.create(
                    medida=row['Medida Preventiva'],
                    plazo=row['Plazo'],
                    responsable=row['Responsable'],
                    coste=row['Coste'],
                    estado=row['Estado']
                )
            messages.success(request, "Medidas importadas correctamente.")
            return redirect('listar_medidas')
    else:
        form = ImportarExcelForm()
    return render(request, 'gestion/importar_medidas.html', {'form': form})

@login_required
def documentos_prevencion(request):
    doc = DocumentosPrevencion.objects.first()
    if request.method == 'POST':
        form = DocumentosPrevencionForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('documentos_prevencion')
    else:
        form = DocumentosPrevencionForm(instance=doc)
    return render(request, 'gestion/documentos_prevencion.html', {'form': form})

@login_required
def editar_evaluacion(request):
    doc, _ = DocumentosPrevencion.objects.get_or_create(pk=1)
    if request.method == "POST":
        form = DocumentosPrevencionForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('listar_medidas')  # O donde prefieras redirigir
    else:
        form = DocumentosPrevencionForm(instance=doc)
    return render(request, 'gestion/editar_documento.html', {'form': form, 'tipo': 'Evaluación de Riesgos'})

def editar_planificacion(request):
    doc, _ = DocumentosPrevencion.objects.get_or_create(pk=1)
    if request.method == "POST":
        form = DocumentosPrevencionForm(request.POST, request.FILES, instance=doc)
        if form.is_valid():
            form.save()
            return redirect('listar_medidas')
    else:
        form = DocumentosPrevencionForm(instance=doc)
    return render(request, 'gestion/editar_documento.html', {'form': form, 'tipo': 'Planificación de la Actividad Preventiva'})

@login_required
def programa_evaluacion(request):
    return HttpResponse("Vista temporal del programa de evaluación. Próximamente...")

@login_required
def listar_evaluacion_planificacion(request):
    documentos = DocumentosPrevencion.objects.first()
    medidas = MedidaPreventiva.objects.all()

    return render(request, 'gestion/listar_evaluacion_planificacion.html', {
        'documentos': documentos,
        'medidas': medidas,
    })

# Emergencias
@login_required
def gestionar_documentos_emergencia(request):
    documento, created = DocumentoEmergencia.objects.get_or_create(nombre="Documentos de Emergencia")
    if request.method == "POST":
        form = DocumentoEmergenciaForm(request.POST, request.FILES, instance=documento)
        if form.is_valid():
            form.save()
            return redirect("documentos_emergencia")
    else:
        form = DocumentoEmergenciaForm(instance=documento)
    return render(request, "gestion/documentos_emergencia.html", {"form": form})

def listar_equipos_emergencia(request):
    equipos = EquipoEmergencia.objects.all()
    return render(request, "gestion/listar_equipos_emergencia.html", {"equipos": equipos})

# Pantalla principal del módulo
@login_required
def emergencias_dashboard(request):
    documentos = DocumentosEmergencia.objects.first()
    equipos = EquipoEmergencia.objects.all()

    empresa = Empresa.objects.first()
    if not empresa:
        raise Exception("No hay ninguna Empresa creada.")

    empresa_medios, created = EmpresaMedioProteccion.objects.get_or_create(empresa=empresa)
    medios = empresa_medios.medios.all()

    return render(request, 'gestion/emergencias_dashboard.html', {
        'documentos': documentos,
        'equipos': equipos,
        'medios': medios,
        'empresa_id': empresa.id   # 🚨 Aquí pasamos el ID
    })


# Seleccionar medios de protección
@login_required
def editar_medios_proteccion(request, empresa_id):
    empresa = Empresa.objects.get(id=empresa_id)
    obj, created = EmpresaMedioProteccion.objects.get_or_create(empresa=empresa)

    # Crear automáticamente medios si no existen
    if not MedioProteccion.objects.exists():
        medios_por_defecto = [
            "Extintor de polvo",
            "Extintor CO2",
            "Boca de incendio equipada (BIE)",
            "Detectores de humos",
            "Pulsadores de alarma",
            "Sistema de rociadores automáticos",
            "Señalización de emergencia",
            "Iluminación de emergencia",
            "Botiquín",
            "No dispone de medios"
        ]
        for nombre in medios_por_defecto:
            MedioProteccion.objects.create(nombre=nombre)

    if request.method == 'POST':
        form = EmpresaMedioProteccionForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('emergencias_dashboard')
    else:
        form = EmpresaMedioProteccionForm(instance=obj)

    return render(request, 'gestion/editar_medios_proteccion.html', {
        'form': form,
        'empresa': empresa,
    })




# Subir/editar documentos PDF
@login_required
def editar_documentos_emergencia(request):
    documentos = DocumentosEmergencia.objects.first()
    if request.method == 'POST':
        form = DocumentosEmergenciaForm(request.POST, request.FILES, instance=documentos)
        if form.is_valid():
            form.save()
            return redirect('emergencias_dashboard')
    else:
        form = DocumentosEmergenciaForm(instance=documentos)
    return render(request, 'gestion/editar_documentos_emergencia.html', {'form': form})

# Gestionar equipos de emergencia
@login_required
def editar_equipos_emergencia(request):
    if request.method == 'POST':
        form = EquipoEmergenciaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('emergencias_dashboard')
    else:
        form = EquipoEmergenciaForm()
    return render(request, 'gestion/editar_equipos_emergencia.html', {'form': form})



# Descargar plantilla de nombramiento de equipos
@login_required
#def descargar_plantilla_nombramiento(request):
 #   try:
  #      filepath = 'media/plantillas/plantilla_nombramiento.pdf'
   #     return FileResponse(open(filepath, 'rb'), as_attachment=True, filename='Plantilla_Nombramiento.pdf')
    #except FileNotFoundError:
     #   raise Http404("No se encuentra la plantilla")


def descargar_plantilla_nombramiento(request):
    output = os.path.join(settings.MEDIA_ROOT, 'plantillas/plantilla_nombramiento.pdf')
    if not os.path.exists(output):
        crear_plantilla(output)
    try:
        # Sirve inline en lugar de forzar descarga
        response = FileResponse(
            open(output, 'rb'),
            filename='Plantilla_Nombramiento.pdf'
        )
        response['Content-Disposition'] = 'inline; filename="Plantilla_Nombramiento.pdf"'
        return response
    except FileNotFoundError:
        raise Http404("No se encuentra la plantilla")

    


@login_required
def dashboard_investigaciones(request):
    proc = ProcedimientoInvestigacion.objects.order_by('-updated_at').first()

    # manejo del upload
    if request.method == 'POST' and 'archivo' in request.FILES:
        form = ProcedimientoInvestigacionForm(request.POST, request.FILES, instance=proc)
        if form.is_valid():
            form.save()
            return redirect('dashboard_investigaciones')
    else:
        form = ProcedimientoInvestigacionForm(instance=proc)

    ultimas = InvestigacionAccidente.objects.order_by('-fecha_investigacion')[:5]
    total = InvestigacionAccidente.objects.count()

    # Cálculo de longitud media del campo 'acciones'
    avg_acciones = InvestigacionAccidente.objects.aggregate(
        avg_len=Avg(Length('acciones'))
    )['avg_len']

    stats = {'total': total, 'media_acciones': avg_acciones}

    return render(request, 'gestion/dashboard_investigaciones.html', {
        'procedimiento': proc,
        'form': form,
        'ultimas': ultimas,
        'stats': stats,
    })




@login_required
def nueva_investigacion(request):
    if request.method=='POST':
        form = InvestigacionForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('lista_investigaciones')
    else:
        form = InvestigacionForm()
    return render(request, 'gestion/form_investigacion.html', {'form': form})

@login_required
def lista_investigaciones(request):
    invs = InvestigacionAccidente.objects.all()
    return render(request, 'gestion/lista_investigaciones.html', {'invs': invs})


@login_required
def editar_procedimiento_investigacion(request):
    obj, _ = ProcedimientoInvestigacion.objects.get_or_create(pk=1)
    if request.method == 'POST':
        form = ProcedimientoInvestigacionForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('dashboard_investigaciones')
    else:
        form = ProcedimientoInvestigacionForm(instance=obj)
    return render(request, 'gestion/editar_procedimiento_investigacion.html', {'form': form})

# Epi´s



@login_required
def listado_epis(request):
    epis = EquipoProteccionIndividual.objects.all()
    return render(request, "gestion/listado_epis.html", {'epis': epis})

@login_required
def seleccionar_epis_puesto(request):
    if request.method == 'POST':
        form = EPISelectionForm(request.POST)
        if form.is_valid():
            puesto = form.cleaned_data['puesto']
            epis = form.cleaned_data['epis']
            EPIPuesto.objects.filter(puesto=puesto).delete()
            for epi in epis:
                EPIPuesto.objects.create(puesto=puesto, epi=epi)
            return redirect('acuse_recibo_epi', puesto_id=puesto.id)
    else:
        form = EPISelectionForm()
    return render(request, "gestion/seleccionar_epis_puesto.html", {'form': form})



def acuse_recibo_epi_pdf(request, trabajador_id):
    trabajador = Trabajador.objects.get(id=trabajador_id)
    puesto = trabajador.puesto
    epis = puesto.epis.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="acuse_recibo_{trabajador.nombre}.pdf"'

    p = canvas.Canvas(response, pagesize=A4)
    width, height = A4

    # Cabecera
    p.setFont("Helvetica-Bold", 14)
    p.drawString(60, height - 60, "Acuse de recibo de entrega de EPIs")

    p.setFont("Helvetica", 11)
    p.drawString(60, height - 100, f"Trabajador: {trabajador.nombre}")
    p.drawString(60, height - 120, f"Puesto de Trabajo: {puesto.nombre}")

    y = height - 160
    p.setFont("Helvetica-Bold", 11)
    p.drawString(60, y, "EPI")
    p.drawString(260, y, "Riesgo")
    p.drawString(400, y, "Norma UNE")
    p.setFont("Helvetica", 10)

    y -= 20
    for epi in epis:
        p.drawString(60, y, epi.nombre)
        p.drawString(260, y, epi.riesgos)
        p.drawString(400, y, epi.norma)
        y -= 18

    # Pie de firma
    y -= 30
    p.drawString(60, y, "Firma del trabajador: _______________________")
    y -= 20
    p.drawString(60, y, "Fecha: ____/____/________")

    p.showPage()
    p.save()
    return response



@login_required
def asignar_epis_puesto(request, pk):
    puesto = get_object_or_404(PuestoTrabajo, pk=pk)
    if request.method == 'POST':
        form = AsignarEPIForm(request.POST, instance=puesto)
        if form.is_valid():
            form.save()
            return redirect('detalle_puesto', pk=pk)
    else:
        form = AsignarEPIForm(instance=puesto)
    return render(request, 'gestion/asignar_epis_puesto.html', {'form': form, 'puesto': puesto})



def descargar_acuse_recibo_epi(request, trabajador_id):
    trabajador = get_object_or_404(Trabajador, id=trabajador_id)
    puesto = trabajador.puesto
    empresa = ... # Recupera tu objeto empresa según tu lógica (puede ser request.user.empresa, o como lo tengas)
    epis = puesto.epis.all()
    html = render_to_string("gestion/acuse_recibo_epi.html", {
        "trabajador": trabajador,
        "puesto": puesto,
        "epis": epis,
        "empresa": empresa,
        "fecha": date.today()
    })
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="acuse_epi_{trabajador.dni}.pdf"'
    weasyprint.HTML(string=html).write_pdf(response)
    return response

@login_required
def listado_epis(request):
    puestos = PuestoTrabajo.objects.all()
    trabajadores = Trabajador.objects.select_related("puesto").all()
    query = request.GET.get("q", "")
    puesto_filtro = request.GET.get("puesto", "")
    epis = EPI.objects.all()

    if query:
        epis = epis.filter(
            Q(nombre__icontains=query) |
            Q(riesgos__icontains=query) |
            Q(norma__icontains=query)
        )
    if puesto_filtro:
        trabajadores = trabajadores.filter(puesto__id=puesto_filtro)

    context = {
        "trabajadores": trabajadores,
        "puestos": puestos,
        "epis": epis,
        "q": query,
        "puesto_filtro": puesto_filtro,
    }
    return render(request, "gestion/listado_epis.html", context)

def asignar_epis(request, puesto_id):
    puesto = get_object_or_404(PuestoTrabajo, id=puesto_id)
    if request.method == 'POST':
        form = AsignarEPIsForm(request.POST, instance=puesto)
        if form.is_valid():
            form.save()
            return redirect('listado_epis')  # Cambia esto según tu url de listado
    else:
        form = AsignarEPIsForm(instance=puesto)
    return render(request, 'gestion/asignar_epis.html', {'form': form, 'puesto': puesto})

@login_required
def listar_epis(request):
    trabajadores = Trabajador.objects.select_related('puesto').all()
    puestos = PuestoTrabajo.objects.prefetch_related('epis').all()

    # Almacena formularios para cada puesto
    forms = {}
    for puesto in puestos:
        forms[puesto.id] = AsignarEpisPuestoForm(instance=puesto, prefix=str(puesto.id))

    # Procesar envío de formulario de algún puesto
    if request.method == 'POST':
        puesto_id = request.POST.get('puesto_id')
        puesto = get_object_or_404(PuestoTrabajo, id=puesto_id)
        form = AsignarEpisPuestoForm(request.POST, instance=puesto, prefix=str(puesto_id))
        if form.is_valid():
            form.save()
            return redirect('listado_epis')
        forms[puesto.id] = form  # Mostrar errores si los hay

    return render(request, 'gestion/listado_epis.html', {
        'trabajadores': trabajadores,
        'puestos': puestos,
        'forms': forms,
    })

@login_required
def editar_epis_puesto(request, puesto_id):
    puesto = get_object_or_404(PuestoTrabajo, id=puesto_id)
    epis = EPI.objects.all()
    if request.method == "POST":
        # Obtén la lista de IDs de EPIs seleccionados
        selected_epis_ids = request.POST.getlist("epis")
        # Asigna los EPIs seleccionados al puesto de trabajo
        puesto.epis.set(selected_epis_ids)
        puesto.save()
        return redirect("listado_epis")  # Cambia al nombre real de tu listado

    return render(
        request,
        "gestion/editar_epis_puesto.html",
        {
            "puesto": puesto,
            "epis": epis,
            
        }
    )

@login_required
def dashboard_cae(request):
    documentos = DocumentoCAE.objects.select_related('empresa').all()
    filtro = DocumentoCAEFilter(request.GET, queryset=documentos)
    docs_filtrados = filtro.qs

    # Notificación: documentos por caducar (ejemplo simple, se puede automatizar)
    docs_por_caducar = docs_filtrados.filter(
        fecha_caducidad__lte=timezone.now().date() + timezone.timedelta(days=7),
        fecha_caducidad__gte=timezone.now().date()
    )
    for doc in docs_por_caducar:
        # NOTA: esto es solo un ejemplo, en producción usar Celery/tareas periódicas y mejor gestión de emails
        if doc.empresa.contacto:
            send_mail(
                'Aviso: Documento CAE próximo a caducar',
                f'El documento "{doc.nombre}" de la empresa "{doc.empresa}" caduca el {doc.fecha_caducidad}.',
                'prl@tuservidor.com',
                [doc.empresa.contacto],
                fail_silently=True,
            )

    return render(request, 'gestion/dashboard_cae.html', {
        'documentos': docs_filtrados,
        'filtro': filtro,
    })

@login_required
def subir_documento_cae(request):
    if request.method == 'POST':
        form = DocumentoCAEForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Documento subido correctamente.')
            return redirect('dashboard_cae')
    else:
        form = DocumentoCAEForm()
    return render(request, 'gestion/subir_documento_cae.html', {'form': form})