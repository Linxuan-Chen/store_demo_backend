from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('collections', views.CollectionViewSet)
router.register('products', views.ProductViewSet)
router.register('cart', views.CartViewSet)

router_cart_items = NestedDefaultRouter(router, 'cart', lookup='cart')
router_cart_items.register('items', views.CartItemViewSet, basename='items')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_cart_items.urls)),
]
