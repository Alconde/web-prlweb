# filters.py (puedes usar django-filter)
import django_filters
from .models import DocumentoCAE, Empresa

class DocumentoCAEFilter(django_filters.FilterSet):
    empresa = django_filters.ModelChoiceFilter(queryset=Empresa.objects.all())
    nombre = django_filters.CharFilter(lookup_expr='icontains', label='Nombre documento')
    estado = django_filters.ChoiceFilter(
        label="Estado",
        choices=[('vigente', 'Vigente'), ('caducado', 'Caducado'), ('por_caducar', 'Por caducar')],
        method='filter_estado'
    )

    def filter_estado(self, queryset, name, value):
        hoy = timezone.now().date()
        if value == 'vigente':
            return queryset.filter(fecha_caducidad__gt=hoy)
        if value == 'caducado':
            return queryset.filter(fecha_caducidad__lt=hoy)
        if value == 'por_caducar':
            lim = hoy + timezone.timedelta(days=30)
            return queryset.filter(fecha_caducidad__gt=hoy, fecha_caducidad__lte=lim)
        return queryset

    class Meta:
        model = DocumentoCAE
        fields = ['empresa', 'nombre', 'estado']
