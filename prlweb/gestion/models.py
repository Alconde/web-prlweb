from django.db import models
from datetime import timedelta
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator

# Empresa
class Empresa(models.Model):    
    TIPO_CHOICES = [
        ('titular', 'Empresa Titular'),
        ('contratista', 'Contratista'),
        ('subcontrata', 'Subcontrata'),
    ]
    nombre = models.CharField(max_length=200, null=True, blank=True)
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, null=True, blank=True)
    responsable = models.CharField(max_length=100, blank=True)
    contacto = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.nombre
    
# Perfil
class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.empresa.nombre}"



# Instalación
class Instalacion(models.Model):
    NOMBRE_CHOICES = [
        ("eléctrica", "Instalación eléctrica"),
        ("centro_transformacion", "Centro de transformación"),
        ("pci", "Protección contra incendios"),
        ("compresor", "Compresor"),
        ("puertas", "Puertas/portones"),
        ("vehiculos", "Flota de vehículos"),
        ("caldera_gas", "Caldera de gas"),
        ("caldera_gasoil", "Caldera de gasoil"),
        ("almacenamiento_quimicos", "Almacenamiento de productos químicos"),
        ("instalacion_petrolifera", "Instalaciones petrolíferas"),
        ("frigorificas", "Instalaciones frigoríficas"),
        ("estanterias", "Estanterías industriales"),
    ]
    nombre = models.CharField(max_length=50, choices=NOMBRE_CHOICES)
    fecha_mantenimiento = models.DateField(null=True, blank=True)
    mantenimiento_realizado = models.BooleanField(default=False)
    frecuencia_mantenimiento_dias = models.PositiveIntegerField(default=365)
    documentacion = models.FileField(upload_to='documentacion/', null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.fecha_mantenimiento:
            self.mantenimiento_realizado = True
        else:
            self.mantenimiento_realizado = False
        super().save(*args, **kwargs)

    @property
    def proxima_fecha_mantenimiento(self):
        if self.fecha_mantenimiento:
            return self.fecha_mantenimiento + timedelta(days=self.frecuencia_mantenimiento_dias)
        return None

    def __str__(self):
        return self.get_nombre_display()


# Gestionar la documentación de las instalaciones
from django.db import models

class DocumentoInstalacion(models.Model):
    TIPO_DOCUMENTO_CHOICES = [
        ("plano_unifilar", "Plano unifilar"),
        ("certificado_instalacion", "Certificado de instalación"),
        ("contrato_mantenimiento", "Contrato de mantenimiento"),
        ("revision_periodica", "Revisión periódica"),
        ("manual_fabricante", "Manual del fabricante"),
        ("boletin_revision", "Boletín de revisión"),
        ("informe_mantenimiento", "Informe de mantenimiento"),
        ("protocolo_actuacion", "Protocolo de actuación"),
        ("ubicacion_equipos", "Plano ubicación equipos"),
        ("libro_mantenimiento", "Libro de mantenimiento"),
        ("manual_uso", "Manual de uso"),
        ("ficha_tecnica", "Ficha técnica"),
        ("certificado_presion", "Certificado presión"),
        ("documentacion_presion", "Documentación recipientes presión"),
        ("marcado_ce", "Marcado CE"),
        ("registro_inspeccion", "Registro de inspección"),
        ("plano_instalacion", "Plano instalación"),
        ("protocolo_limpieza", "Protocolo limpieza conductos"),
        ("itv", "ITV"),
        ("registro_revisiones", "Registro de revisiones"),
        ("parte_reparacion", "Partes de reparación"),
    ]

    instalacion = models.ForeignKey('Instalacion', on_delete=models.CASCADE, related_name='documentos')
    tipo_documento = models.CharField(max_length=50, choices=TIPO_DOCUMENTO_CHOICES)
    archivo = models.FileField(upload_to='documentacion/')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.instalacion} - {self.get_tipo_documento_display()}"

# Equipos de trabajo
class EquipoTrabajo(models.Model):
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    numero_serie = models.CharField(max_length=100)
    marcado_ce = models.BooleanField(default=True)
    declaracion_ce = models.FileField(upload_to='equipos/declaraciones_ce/', blank=True, null=True)
    manual_instrucciones = models.FileField(upload_to='equipos/manuales/', blank=True, null=True)
    requiere_mantenimiento = models.BooleanField(default=False)
    fecha_mantenimiento = models.DateField(null=True, blank=True)
    frecuencia_mantenimiento_dias = models.PositiveIntegerField(default=365)

    @property
    def proxima_revision(self):
        if self.fecha_mantenimiento:
            return self.fecha_mantenimiento + timedelta(days=self.frecuencia_mantenimiento_dias)
        return None

    def __str__(self):
        return f"{self.nombre} ({self.marca} {self.modelo})"
    
class AutorizacionEquipo(models.Model):
    trabajador = models.CharField(max_length=100)
    dni = models.CharField(max_length=20)
    fecha = models.DateField(auto_now_add=True)
    equipos_autorizados = models.ManyToManyField(EquipoTrabajo)

# Puesto de trabajo
class EPI(models.Model):
    nombre = models.CharField(max_length=100)
    riesgos = models.CharField(max_length=200)
    norma = models.CharField(max_length=50)

    def __str__(self):
        return self.nombre
    
class PuestoTrabajo(models.Model):
    nombre = models.CharField(max_length=100)
    departamento = models.CharField(max_length=100, blank=True)
    tareas = models.TextField()
    equipos_trabajo = models.TextField(blank=True)
    #epis_necesarios = models.TextField(blank=True)
    epis = models.ManyToManyField(EPI, blank=True)
    productos_quimicos = models.TextField(blank=True)
    manipulacion_cargas = models.BooleanField(default=False)
    trabajos_altura = models.BooleanField(default=False)
    espacios_confinados = models.BooleanField(default=False)
    exposicion_ruido = models.BooleanField(default=False)
    tipo_exposicion = models.CharField(max_length=200, blank=True)
    horario = models.CharField(max_length=100, blank=True)
    uso_pvd = models.BooleanField(default=False)    
    formacion_requerida = models.TextField(blank=True)
    autorizacion_equipos = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Trabajador(models.Model):
    nombre = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=150)
    dni = models.CharField(max_length=9, unique=True)
    puesto = models.ForeignKey(PuestoTrabajo, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.nombre} {self.apellidos}"
    
# Productos químicos
class ProductoQuimico(models.Model):
    nombre = models.CharField(max_length=200)
    lugar_uso = models.CharField(max_length=200)
    lugar_almacenamiento = models.CharField(max_length=200)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    unidad = models.CharField(max_length=20, choices=[('kg', 'kg'), ('L', 'L'), ('uds', 'uds')])
    observaciones = models.TextField(blank=True)
    fds = models.FileField(upload_to='productos/fds/', blank=True, null=True)

    def __str__(self):
        return self.nombre

# Plan de Prevención
class PlanPrevencion(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, null=True, blank=True)
    documento_plan = models.FileField(upload_to='planes_prevencion/', null=True, blank=True)
    tiene_delegado_prevencion = models.BooleanField(default=False)
    acta_delegado = models.FileField(upload_to='delegados/', blank=True, null=True)
    formacion_delegado = models.FileField(upload_to='delegados/', blank=True, null=True)
    
    trabajos_altura = models.BooleanField(default=False)
    espacios_confinados = models.BooleanField(default=False)
    atm_explosivas = models.BooleanField(default=False)
    excavaciones = models.BooleanField(default=False)
    
    tiene_recurso_preventivo = models.BooleanField(default=False)
    nombramiento_recurso = models.FileField(upload_to='recursos_preventivos/', blank=True, null=True)
    formacion_recurso = models.FileField(upload_to='recursos_preventivos/', blank=True, null=True)

    def __str__(self):
        return "Plan de Prevención"

#Evaluación de Riesgos
class MedidaPreventiva(models.Model):
    medida = models.CharField(max_length=255)
    plazo = models.CharField(max_length=255)
    responsable = models.CharField(max_length=255)
    coste = models.CharField(max_length=255, blank= True, null=True)
    estado = models.CharField(
        max_length=50,
        choices=[
            ('pendiente', 'Pendiente'),
            ('en curso', 'En curso'),
            ('implantada', 'Implantada')
        ],
        default='pendiente'
    )

    def __str__(self):
        return self.medida


# Subir documentos
class DocumentosPrevencion(models.Model):
    documento_evaluacion = models.FileField(
        upload_to="prevencion/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )
    documento_planificacion = models.FileField(
        upload_to="prevencion/",
        blank=True,
        null=True,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])]
    )



class DocumentosEmergencia(models.Model):
    plan_emergencia = models.FileField(upload_to="emergencias/", null=True, blank=True)
    registro_simulacros = models.FileField(upload_to="emergencias/", null=True, blank=True)
    consignas_emergencia = models.FileField(upload_to="emergencias/", null=True, blank=True)
    nombramientos = models.FileField(upload_to="emergencias/", null=True, blank=True)
    certificados_formacion = models.FileField(upload_to="emergencias/", null=True, blank=True)
    plano = models.FileField(upload_to="emergencias/", null=True, blank=True)

    def __str__(self):
        return "Documentos de Emergencia"


class EquipoEmergencia(models.Model):
    TIPO_CHOICES = [
        ('JEFE', 'Jefe de Emergencia'),
        ('SUSTITUTO', 'Sustituto Jefe de Emergencia'),
        ('INTERVENCION', 'Equipo de Intervención'),
        ('EVACUACION', 'Equipo de Alarma y Evacuación'),
        ('PRIMEROS AUXILIOS', 'Equipo de Primeros Auxilios'),
    ]
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES)
    responsable = models.CharField(max_length=100)
    sustituto = models.CharField(max_length=100, blank=True)
    registro_designacion = models.FileField(
        upload_to="emergencia/designaciones/",
        help_text="Documento firmado por el trabajador",
        blank=True,
        null=True
    )
    certificado_formacion = models.FileField(
        upload_to="emergencia/formacion/",
        help_text="Certificado de formación en emergencias",
        blank=True,
        null=True
    )

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.responsable}"


class MedioProteccion(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre

class EmpresaMedioProteccion(models.Model):
    empresa = models.ForeignKey('Empresa', on_delete=models.CASCADE,  blank=True, null=True )
    medios = models.ManyToManyField(MedioProteccion)

# Investigación de accidentes
class ProcedimientoInvestigacion(models.Model):
    pdf = models.FileField(upload_to="investigaciones/procedimientos/", blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Procedimiento actualizado {self.updated_at:%Y-%m-%d}"

class InvestigacionAccidente(models.Model):
    codigo = models.CharField(
        max_length=10,
        unique=True,
        default="NA-000",  # valor por defecto para migración
        help_text="Código único de investigación"
    )
    fecha_investigacion = models.DateField()
    formato = models.FileField(upload_to="investigaciones/formularios/" , blank=True, null=True)
    informe_pdf = models.FileField(
        upload_to="investigaciones/informes/",
        blank=True,
        null=True
    )
    # Campos INSHT
    causas_inmediatas = models.TextField(help_text="Causas inmediatas del accidente", blank=True, null=True)
    causas_raiz = models.TextField(help_text="Causas raíz del accidente", blank=True, null=True)
    acciones = models.TextField(help_text="Acciones correctivas/preventivas" , blank=True, null=True)

    def __str__(self):
        return self.codigo
    
# Epi´s
from django.db import models

class EquipoProteccionIndividual(models.Model):
    nombre = models.CharField(max_length=100)
    riesgos = models.CharField(max_length=255, help_text="Riesgos de los que protege")
    norma_une = models.CharField(max_length=100, help_text="Norma UNE de referencia")

    def __str__(self):
        return self.nombre



class EPIPuesto(models.Model):
    puesto = models.ForeignKey(PuestoTrabajo, on_delete=models.CASCADE)
    epi = models.ForeignKey(EquipoProteccionIndividual, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('puesto', 'epi')

    def __str__(self):
        return f"{self.epi} asignado a {self.puesto}"
    
# CAE
class DocumentoCAE(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    archivo = models.FileField(upload_to='cae/documentos/')
    fecha_subida = models.DateField(auto_now_add=True)
    fecha_caducidad = models.DateField(null=True, blank=True)
    es_obligatorio = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.empresa} - {self.nombre}"

class AccesoRegistro(models.Model):
    persona = models.CharField(max_length=200)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    fecha_entrada = models.DateTimeField()
    fecha_salida = models.DateTimeField(null=True, blank=True)
    observaciones = models.TextField(blank=True)

class ReunionCAE(models.Model):
    fecha = models.DateField()
    empresas = models.ManyToManyField(Empresa)
    acta = models.FileField(upload_to='cae/reuniones/', blank=True, null=True)
    resumen = models.TextField()

class IncidenciaCAE(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    fecha = models.DateField()
    descripcion = models.TextField()
    solucion = models.TextField(blank=True)
    cerrada = models.BooleanField(default=False)

class RecursoPreventivo(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=200)
    actividad = models.CharField(max_length=200)
    fecha_designacion = models.DateField()
    presente = models.BooleanField(default=False)

class EmergenciaPlan(models.Model):
    descripcion = models.TextField()
    documento = models.FileField(upload_to='cae/emergencias/')
    empresas = models.ManyToManyField(Empresa)


    
