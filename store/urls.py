from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()

# router.register('carts', )