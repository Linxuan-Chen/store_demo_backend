from typing import Any
from django.contrib import admin
from django.urls import reverse
from django.db.models import Count
from django.db.models.query import QuerySet
from django.utils.html import format_html
from django.utils.http import urlencode
from django.http import HttpRequest
from store import models


@admin.register(models.Collection)
class CollectionAdmin(admin.ModelAdmin):
    """Custom admin configuration for Collection model

    This class specifies how Collection model is displayed
    """
    list_display = ['title', 'product_count']
    autocomplete_fields = ['featured_product']

    def product_count(self, collection: models.Collection):
        url = reverse('admin:store_product_changelist') + \
            '?' + urlencode({'collection_id': collection.pk})
        return format_html('<a href={}>{}</a>', url, collection.product_count)

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        """Return a queryset annotated with 'product_count' to display the number of products 
        associated with each collection instance.

        Returns:
            QuerySet[Any]: Queryset with an additional 'product_count' column.
        """
        return super().get_queryset(request).annotate(product_count=Count('product'))


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
        return product.collection.title if product.collection else ''


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
    list_display = ['full_name', 'membership',
                    'customer_address', 'customer_details']
    list_filter = ['membership']
    ordering = ['id']
    autocomplete_fields = ['addresses']
    list_select_related = ['customer_details']
    search_fields = ['first_name', 'last_name',
                     'addresses__street', 'addresses__city']

    def get_queryset(self, request: HttpRequest) -> QuerySet[Any]:
        return super().get_queryset(request).prefetch_related('addresses')

    def full_name(self, customer: models.Customer):
        return f'{customer.first_name} {customer.last_name}'

    def customer_address(self, customer: models.Customer):
        return [address for address in customer.addresses.all()]

    def customer_details(self, customer: models.Customer):
        url = reverse('admin:store_customer_details_changelist') + '?' + urlencode({
            'id': customer.customer_details
        })

        return format_html('<a href={}>{}</a>', url, customer.customer_details)


@admin.register(models.Promotion)
class PromotionAdmin(admin.ModelAdmin):
    """Custom admin configs for promotion model"""
    list_display = ['id', 'title', 'discount']
    list_editable = ['title', 'discount']


@admin.register(models.CustomerDetails)
class CustomerDetailsAdmin(admin.ModelAdmin):
    """Custom admin configs for customer details model"""

    list_display = ['customer_id', 'email', 'phone', 'birth_date']
    list_display = ['email', 'phone', 'birth_date']
    autocomplete_fields = ['customer_id']


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    """Custom admin configs for order model
    
        Order items column displays total items associated with the order
        Can redirect to order items details change list page by clicking the amount of order items
    """

    list_display = ['customer', 'address',
                    'payment_status', 'created_at', 'order_items',]
    list_filter = ['payment_status']
    search_fields = ['customer__first_name',
                     'customer__first_name', 'address__street', 'address__city', 'created_at']
    list_select_related = ['customer', 'address']
    autocomplete_fields = ['customer', 'address']

    def order_items(self, order: models.Order):
        url = reverse('admin:store_orderitem_changelist') + '?' + urlencode({
            'order_id': order.pk
        })

        return format_html('<a href={}>{}</a>', url, order.orderitem_set.count())


@admin.register(models.OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    """Custom admin configs for order items model"""

    list_display = ['order_id', 'product_title', 'unit_price', 'quantity']
    list_select_related = ['order']
    autocomplete_fields = ['order']


@admin.register(models.Cart)
class CartAdmin(admin.ModelAdmin):
    """Custom admin configs for cart model"""
    list_display = ['id', 'created_at', 'cart_items']
    search_fields = ['id']

    def cart_items(self, cart: models.Cart):
        url = reverse('admin:store_cart_changelist') + '?' + \
            urlencode({
                'cart_id': cart.id
            })
        return format_html('<a href={}>{}</a>', url, cart.cartitem_set.count())


@admin.register(models.CartItem)
class CartItemAdmin(admin.ModelAdmin):
    """Custom admin configs for CartItem model"""
    list_display = ['cart', 'product', 'quantity']
    list_editable = ['product', 'quantity']
    search_fields = ['cart', 'product']
    autocomplete_fields = ['cart', 'product']


@admin.register(models.Review)
class ReviewAdmin(admin.ModelAdmin):
    """Custom admin configs for review model"""
    list_display = ['product', 'customer', 'description', 'rating']
    list_select_related = ['product', 'customer']
    autocomplete_fields = ['product', 'customer']
