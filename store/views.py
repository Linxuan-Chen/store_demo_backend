from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet
from .models import Collection
from .serializers import CollectionRetrieveSerializer, CollectionModifySerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from .filters import CollectionFilter


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.select_related('featured_product').all()
    serializer_class = CollectionRetrieveSerializer
    http_method_names = ['get', 'delete', 'patch', 'post']
    filter_backends = [DjangoFilterBackend]
    filterset_class = CollectionFilter

    def get_serializer_class(self) -> type[BaseSerializer]:
        return CollectionRetrieveSerializer if self.request.method == 'GET' else CollectionModifySerializer
