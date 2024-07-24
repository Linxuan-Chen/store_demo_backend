from typing import Any
from django.shortcuts import get_object_or_404
from django.db.models.query import QuerySet
from rest_framework import status, permissions
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import BaseSerializer
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CollectionFilter, ProductFilter
from .paginations import ProductPagination
from .permissions import IsAdminOrAuthenticated
from .models import Collection, Product, Cart, CartItem, Customer
from .serializers import CollectionRetrieveSerializer, \
    CollectionModifySerializer, ProductSerializer, CartSerializer, CartItemSerializer, \
    AddCartItemSerializer, UpdateCartItemSerializer, CustomerSerializer, UpdateCustomerSerializer


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
    permission_classes = [IsAdminOrAuthenticated]


class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    queryset = CartItem.objects.all()

    @action(detail=False, methods=['delete'])
    def bulk_delete(self, request: Request, *args, **kwargs):
        if request.data and isinstance(request.data, dict) and 'item_ids' in request.data:
            item_ids = request.data['item_ids']
            CartItem.objects.filter(
                id__in=item_ids).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response("item_ids is required", status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def count(self, request: Request, *args, **kwargs):
        cart_pk = self.kwargs['cart_pk']
        if cart_pk:
            try:
                cart = Cart.objects.get(id=self.kwargs['cart_pk'])
                count = cart.cartitem_set.count()
                return Response({'count': count}, status=status.HTTP_200_OK)
            except Cart.DoesNotExist:
                return Response("Cart not found", status=status.HTTP_404_NOT_FOUND)
        else:
            return Response("no data", status=status.HTTP_404_NOT_FOUND)

    def partial_update(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        instance = self.get_object()
        patch_serializer = self.get_serializer(
            instance, data=request.data, partial=True)
        patch_serializer.is_valid(raise_exception=True)
        self.perform_update(patch_serializer)

        response_serializer = CartItemSerializer(instance)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def get_queryset(self) -> QuerySet:
        cart_id = self.kwargs['cart_pk']
        return super().get_queryset().filter(cart_id=cart_id)

    def get_serializer_class(self):
        requestMethod = self.request.method
        if requestMethod == 'POST':
            return AddCartItemSerializer
        if requestMethod == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer

    def get_serializer_context(self) -> dict[str, Any]:
        context = super().get_serializer_context()
        context['cart_id'] = self.kwargs['cart_pk']
        return context


class CustomerView(RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet):
    queryset = Customer.objects.prefetch_related(
        'addresses').select_related('customer_details').all()

    @action(detail=False, methods=['get'])
    def current_cart(self, request):
        customer = get_object_or_404(Customer, user_id=request.user.id)
        return Response({'cart_id': customer.cart})

    @action(detail=False, methods=['get', 'patch'])
    def current_user(self, request):
        (customer, created) = Customer.objects.get_or_create(
            user_id=request.user.id)
        if request.method == 'PATCH':
            customer_serializer = UpdateCustomerSerializer(
                customer, data=request.data)
            customer_serializer.is_valid(raise_exception=True)
            customer_serializer.save()
            return Response(customer_serializer.data)
        return Response(CustomerSerializer(customer).data)

    def get_serializer_class(self):
        if self.request.method == 'POST' or self.request.method == 'PATCH':
            return UpdateCustomerSerializer
        return CustomerSerializer

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]
