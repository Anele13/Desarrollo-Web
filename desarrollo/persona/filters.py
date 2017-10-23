from .models import *
import django_filters
from liquidacion import models as mliq

class UserFilter(django_filters.FilterSet):
    nya = django_filters.CharFilter(lookup_expr='icontains', label='Nombre/Apellido')
    documento= django_filters.CharFilter(lookup_expr='icontains', label="Documento")
    cuil = django_filters.CharFilter(lookup_expr='icontains', label="Cuil")
    class Meta:
        model = Persona
        fields = ['documento', 'nya', 'cuil', ]
