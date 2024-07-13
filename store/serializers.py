from rest_framework import serializers
from .models import Product, Collection, Cart, CartItem


class SimpleProductSerializer(serializers.ModelSerializer):
    """A simple product serializer

        The serializer only displays basic meta data of a product
    """
    class Meta:
        model = Product
        fields = ['id', 'title', 'inventory', 'unit_price']


class CollectionRetrieveSerializer(serializers.ModelSerializer):
    """A serializer to retrieve collection data

        featured_product_names returns simple data of featured products of the collection
    """

    featured_products = serializers.SerializerMethodField(
        method_name='get_featured_products')

    class Meta:
        model = Collection
        fields = ['id', 'title', 'featured_products']

    def get_featured_products(self, collection):
        products = collection.featured_product
        return SimpleProductSerializer(products, many=True).data


class CollectionModifySerializer(serializers.ModelSerializer):
    """A serialzier to modify collection data"""
    class Meta:
        model = Collection
        fields = ['title']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'collection', 'title', 'slug',
                  'description', 'inventory', 'promotions', 'unit_price']


class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def save(self):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']

        try:
            cart_item = CartItem.objects.get(
                product_id=product_id, cart_id=cart_id)
            cart_item.quantity += self.validated_data['quantity']
            cart_item.save()
            self.instance = cart_item

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(
                cart_id=cart_id, **self.validated_data)

        return self.instance

    class Meta:
        model = CartItem
        fields = ['product_id', 'quantity']


class CartItemSerializer(serializers.ModelSerializer):
    products = serializers.SerializerMethodField(method_name='get_products')
    total_price = serializers.SerializerMethodField(
        method_name='calc_total_price')

    def get_products(self, cart_item: CartItem):
        return SimpleProductSerializer(cart_item.product).data

    def calc_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price if cart_item.product else 0

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'products', 'total_price']


class CartSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField('get_cart_items')
    cart_total_price = serializers.SerializerMethodField(
        'calc_cart_total_price')
    id = serializers.UUIDField(read_only=True)

    def get_cart_items(self, cart: Cart):
        return CartItemSerializer(cart.cartitem_set, many=True).data

    def calc_cart_total_price(self, cart: Cart):
        return sum([(item.quantity * item.product.unit_price)
                    for item in cart.cartitem_set.select_related('product').all() if item.product])

    class Meta:
        model = Cart
        fields = ['id', 'created_at', 'items', 'cart_total_price']


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']