from django_filters import rest_framework as filters
from .models import CruiseDetailFinal

class CruiseFilter(filters.FilterSet):
    min_cost = filters.NumberFilter(field_name="cost", lookup_expr='gte')
    max_cost = filters.NumberFilter(field_name="cost", lookup_expr='lte')
    min_nights = filters.NumberFilter(field_name="nights", lookup_expr='gte')
    max_nights = filters.NumberFilter(field_name="nights", lookup_expr='lte')
    start_date_after = filters.DateFilter(field_name="startDate", lookup_expr='gte')
    start_date_before = filters.DateFilter(field_name="startDate", lookup_expr='lte')
    
    class Meta:
        model = CruiseDetailFinal
        fields = {
            'type': ['exact', 'icontains'],
            'origin': ['exact', 'icontains'],
            'visiting': ['icontains'],
            'continent': ['exact', 'icontains'],
            'country': ['exact', 'icontains'],
        }