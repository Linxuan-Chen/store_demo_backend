from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

router.register('collections', views.CollectionViewSet)
router.register('products', views.ProductViewSet)
router.register('cart', views.CartViewSet)
router.register('customers', views.CustomerView)
router.register('orders', views.OrderViewSet)
router.register('addresses', views.AddressViewSet, basename='addresses')

router_cart_items = NestedDefaultRouter(router, 'cart', lookup='cart')
router_cart_items.register('items', views.CartItemViewSet, basename='items')
router_product_image = NestedDefaultRouter(router, 'products', lookup='product')
router_product_image.register('images', views.ProductImageViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('', include(router_cart_items.urls)),
    path('', include(router_product_image.urls)),
]
