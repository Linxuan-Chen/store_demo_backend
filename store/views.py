from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CollectionFilter, ProductFilter
from .paginations import ProductPagination
from .models import Collection, Product
from .serializers import CollectionRetrieveSerializer, CollectionModifySerializer, ProductSerializer


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.select_related('featured_product').all()
    serializer_class = CollectionRetrieveSerializer
    http_method_names = ['get', 'delete', 'patch', 'post']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionFilter

    def get_serializer_class(self) -> type[BaseSerializer]:
        return CollectionRetrieveSerializer if self.request.method == 'GET' else CollectionModifySerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.select_related(
        'collection').prefetch_related('promotions').all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']
    pagination_class = ProductPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
