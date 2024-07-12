from django_filters.rest_framework import FilterSet
from .models import Collection
import django_filters


class CollectionFilter(FilterSet):
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains', label='title')
    id = django_filters.NumberFilter(
        field_name='id', lookup_expr='exact', label='id')

    class Meta:
        model = Collection
        fields = ['id', 'title']
