from django import forms
from .models import (
    Instalacion, DocumentoInstalacion, EquipoTrabajo, PuestoTrabajo, Trabajador, 
    ProductoQuimico, PlanPrevencion, MedidaPreventiva, DocumentosPrevencion, 
    DocumentosEmergencia, EquipoEmergencia, MedioProteccion, EmpresaMedioProteccion, 
    InvestigacionAccidente, ProcedimientoInvestigacion, EPIPuesto, EquipoProteccionIndividual,  
    EPI, DocumentoCAE
    )


class InstalacionForm(forms.ModelForm):
    fecha_ultimo_mantenimiento = forms.DateField(
        input_formats=['%Y-%m-%d', '%d/%m/%Y'],
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Instalacion
        fields = ['nombre', 'fecha_ultimo_mantenimiento', 'documentacion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cargar valor desde el modelo
        if self.instance and self.instance.pk:
            self.fields['fecha_ultimo_mantenimiento'].initial = self.instance.fecha_mantenimiento

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.fecha_mantenimiento = self.cleaned_data.get('fecha_ultimo_mantenimiento')
        if commit:
            instance.save()
        return instance


        
        
# formulario para subir la documentación de las instalaciones
# Mapeo por tipo de instalación
DOCUMENTOS_POR_TIPO = {
    "eléctrica": ["plano_unifilar", "certificado_instalacion", "contrato_mantenimiento", "revision_periodica"],
    "centro_transformacion": ["manual_fabricante", "boletin_revision", "informe_mantenimiento", "protocolo_actuacion"],
    "pci": ["ubicacion_equipos", "contrato_mantenimiento", "libro_mantenimiento", "manual_uso"],
    "compresor": ["ficha_tecnica", "libro_mantenimiento", "certificado_presion", "documentacion_presion"],
    "puertas": ["marcado_ce", "manual_uso", "registro_inspeccion"],
    "caldera_gas": ["plano_instalacion", "libro_mantenimiento"],
    "caldera_gasoil": ["plano_instalacion", "libro_mantenimiento"],
    "vehiculos": ["ficha_tecnica", "itv", "registro_revisiones", "parte_reparacion"],
    "almacenamiento_quimicos": ["manual_uso"],
    "instalacion_petrolifera": ["certificado_instalacion", "libro_mantenimiento"],
    "frigorificas": ["plano_instalacion", "protocolo_limpieza"],
    "estanterias": ["manual_uso", "registro_inspeccion"],
}

class DocumentoInstalacionForm(forms.ModelForm):
    class Meta:
        model = DocumentoInstalacion
        fields = ['tipo_documento', 'archivo', 'descripcion']

    def __init__(self, *args, **kwargs):
        instalacion = kwargs.pop('instalacion', None)
        super().__init__(*args, **kwargs)
        if instalacion:
            tipos_validos = DOCUMENTOS_POR_TIPO.get(instalacion.nombre, [])
            self.fields['tipo_documento'].choices = [
                (codigo, nombre) for codigo, nombre in DocumentoInstalacion.TIPO_DOCUMENTO_CHOICES if codigo in tipos_validos
            ]

# Equipos de trabajo
class EquipoTrabajoForm(forms.ModelForm):
    class Meta:
        model = EquipoTrabajo
        fields = '__all__'
        widgets = {
            'fecha_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
        }

# Puestos de trabajo
class PuestoTrabajoForm(forms.ModelForm):
    class Meta:
        model = PuestoTrabajo
        fields = '__all__'
        widgets = {
            'tareas': forms.Textarea(attrs={'rows': 3}),            
            'formacion_requerida': forms.Textarea(attrs={'rows': 2}),
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }

# Trabajadores
class TrabajadorForm(forms.ModelForm):
    class Meta:
        model = Trabajador
        fields = ['nombre', 'apellidos', 'dni', 'puesto']

# Productos químicos
class ProductoQuimicoForm(forms.ModelForm):
    class Meta:
        model = ProductoQuimico
        fields = '__all__'

# Plan de Prevención 
class PlanPrevencionForm(forms.ModelForm):
    class Meta:
        model = PlanPrevencion
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['documento_plan'].widget.attrs.update({'class': 'form-control'})

# Evaluación de riesgos y Planificación
class MedidaPreventivaForm(forms.ModelForm):
    class Meta:
        model = MedidaPreventiva
        fields = '__all__'

class DocumentosPrevencionForm(forms.ModelForm):
    class Meta:
        model = DocumentosPrevencion
        fields = '__all__'

class ImportarExcelForm(forms.Form):
    archivo = forms.FileField(label="Selecciona un archivo Excel")

# Emergencia
class DocumentosEmergenciaForm(forms.ModelForm):
    class Meta:
        model = DocumentosEmergencia
        fields = [
            "plan_emergencia",
            "registro_simulacros",
            "consignas_emergencia",
            "nombramientos",
            "certificados_formacion",
            "plano",
        ]


class EquipoEmergenciaForm(forms.ModelForm):
    class Meta:
        model = EquipoEmergencia
        fields = ['tipo', 'responsable', 'sustituto', 'registro_designacion', 'certificado_formacion']
        widgets = {
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'responsable': forms.TextInput(attrs={'class': 'form-control'}),
            'sustituto': forms.TextInput(attrs={'class': 'form-control'}),
        }

class MedioProteccionForm(forms.ModelForm):
    class Meta:
        model = MedioProteccion
        fields = "__all__"



class EmpresaMedioProteccionForm(forms.ModelForm):
    class Meta:
        model = EmpresaMedioProteccion
        fields = ['medios']
        widgets = {
            'medios': forms.CheckboxSelectMultiple(attrs={'class': 'list-group'})
        }

# Investigación de accidentes
class InvestigacionForm(forms.ModelForm):
    class Meta:
        model = InvestigacionAccidente
        fields = [
            'codigo', 'fecha_investigacion', 'formato', 'informe_pdf',
            'causas_inmediatas', 'causas_raiz', 'acciones'
        ]
        widgets = {
            'fecha_investigacion': forms.DateInput(attrs={'type':'date'}),
            'causas_inmediatas': forms.Textarea(attrs={'rows':3}),
            'causas_raiz': forms.Textarea(attrs={'rows':3}),
            'acciones': forms.Textarea(attrs={'rows':3}),
        }

# gestion/forms.py
from django import forms
from .models import ProcedimientoInvestigacion

class ProcedimientoInvestigacionForm(forms.ModelForm):
    class Meta:
        model = ProcedimientoInvestigacion
        fields = '__all__'  # o lista explícita de campos



class EPIPuestoForm(forms.ModelForm):
    class Meta:
        model = EPIPuesto
        fields = ['puesto', 'epi']

class EPISelectionForm(forms.Form):
    puesto = forms.ModelChoiceField(queryset=PuestoTrabajo.objects.all())
    epis = forms.ModelMultipleChoiceField(
        queryset=EquipoProteccionIndividual.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )



class AsignarEPIForm(forms.ModelForm):
    epis = forms.ModelMultipleChoiceField(
        queryset=EPI.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="EPIs necesarios"
    )
    class Meta:
        model = PuestoTrabajo
        fields = ['epis']
        widgets = {
            'epis': forms.CheckboxSelectMultiple
        }

class AsignarEpisPuestoForm(forms.ModelForm):
    class Meta:
        model = PuestoTrabajo
        fields = ['epis']
        widgets = {
            'epis': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
        }

class EditarEpisPuestoForm(forms.ModelForm):
    class Meta:
        model = PuestoTrabajo
        fields = ['epis']
        widgets = {
            'epis': forms.CheckboxSelectMultiple(attrs={'class': 'list-group'})
        }

# CAE
class DocumentoCAEForm(forms.ModelForm):
    class Meta:
        model = DocumentoCAE
        fields = ['empresa', 'nombre', 'archivo', 'fecha_caducidad', 'es_obligatorio']
        widgets = {
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }