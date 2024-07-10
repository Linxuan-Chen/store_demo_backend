from typing import Any
from django.contrib import admin
from django.urls import reverse
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html
from django.utils.http import urlencode
from django.http import HttpRequest
from store import models
from django import forms


class ProductInventoryLevelFilter(admin.SimpleListFilter):
    """This class filters product by inventory level

        Inventory levels: 
        Low - inventory < low_threshold
        Medium - low_threshold <= inventory <= high_threshold
        High - inventory > high_threshold 
    """
    title = 'Inventory Level'
    parameter_name = 'inventory'

    def lookups(self, request: Any, model_admin: Any) -> list[tuple[Any, str]]:
        return [
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
        ]

    def queryset(self, request: Any, queryset: QuerySet[Any]) -> QuerySet[Any] | None:
        """This method returns queryset after filtering

        Returns:
            QuerySet[Any] | None: queryset after filtering
        """
        INVENTORY_TO_LEVEL_MAPPING = {
            'low': 10,  # low inventory threshold
            'high': 60  # high inventory threshold
        }
        if self.value() == 'low':
            return queryset.filter(inventory__lt=INVENTORY_TO_LEVEL_MAPPING['low'])
        elif self.value() == 'medium':
            return queryset.filter(inventory__gte=INVENTORY_TO_LEVEL_MAPPING['low'], inventory__lte=INVENTORY_TO_LEVEL_MAPPING['high'])
        elif self.value() == 'high':
            return queryset.filter(inventory__gt=INVENTORY_TO_LEVEL_MAPPING['high'])


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Custom admin configuration for Collection model

    This class specifies how Collection model is displayed
    """
    list_display = ['title', 'product_count']

    def product_count(self, collection: models.Collection):
        url = reverse('admin:store_product_changelist') + \
            '?' + urlencode({'collection_id': collection.id})
        return format_html('<a href={}>{}</a>', url, collection.product_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        """Return a queryset annotated with 'product_count' to display the number of products 
        associated with each collection instance.

        Returns:
            QuerySet[Any]: Queryset with an additional 'product_count' column.
        """
        return super().get_queryset(request).annotate(product_count=Count('product'))


@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    """Custom admin configuration for Product model

    This class specifies how product pannel is displayed
    """
    list_display = ['title', 'inventory', 'unit_price', 'collection_title']
    list_editable = ['unit_price', 'inventory',]
    list_select_related = ['collection']
    ordering = ['title', 'unit_price', 'inventory']
    search_fields = ['title', 'unit_price']
    list_per_page = 10
    list_filter = [ProductInventoryLevelFilter]
    prepopulated_fields = {'slug': ('title',)}

    def collection_title(self, product: models.Product):
        return product.collection.title


@admin.register(models.Address)
class AddressAdmin(admin.ModelAdmin):
    """Custom admin configurations for address

        This class specifies how customer model is displayed
    """
    list_display = ['street', 'city', 'zip']
    search_fields = ['street', 'city', 'zip']


@admin.register(models.Customer)
class CustomerAdmin(admin.ModelAdmin):
    """This class specifies how customer model is displayed

        New addresses can be added and mapped on the page
    """
    list_display = ['full_name', 'membership', 'customer_address']
    list_filter = ['membership']
    ordering = ['id']
    autocomplete_fields = ['addresses']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).prefetch_related('addresses')

    def full_name(self, customer: models.Customer):
        return f'{customer.first_name} {customer.last_name}'

    def customer_address(self, customer: models.Customer):
        return [address for address in customer.addresses.all()]
