from django_filters.rest_framework import FilterSet
from .models import Collection, Product
import django_filters


class CollectionFilter(FilterSet):
    """Custom filter for collection model

        example: /api/store/collections/?title=your_title
    """
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains', label='title')

    class Meta:
        model = Collection
        fields = ['title']


class ProductFilter(FilterSet):
    """Custom filter for product model

        example: /api/store/products/?title=your_title&description=keywords
    """
    title = django_filters.CharFilter(
        field_name='title', lookup_expr='icontains', label='title')
    description = django_filters.CharFilter(
        field_name='description', lookup_expr='icontains', label='description')

    class Meta:
        model = Product
        fields = ['title', 'description']
