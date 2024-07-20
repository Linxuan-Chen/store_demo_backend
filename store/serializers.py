from rest_framework import serializers
from django.db.transaction import atomic
from .models import Product, Collection, Cart, CartItem, Customer, CustomerDetails, Address
from django.contrib.auth.models import User


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


class AddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'zip']


class CustomerDetailsSerialzier(serializers.ModelSerializer):

    class Meta:
        model = CustomerDetails
        fields = ['id', 'email', 'phone', 'birth_date']


class CustomerSerializer(serializers.ModelSerializer):
    addresses = serializers.SerializerMethodField(method_name='get_addresses')
    customer_details = CustomerDetailsSerialzier()
    user_id = serializers.IntegerField(read_only=True)
    id = serializers.IntegerField(read_only=True)

    def get_addresses(self, customer: Customer):
        return AddressSerializer(customer.addresses, many=True).data

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name',
                  'membership', 'customer_details', 'addresses', 'user_id']


class UserSerializer(serializers.ModelSerializer):
    # username = serializers.CharField(write_only=True)
    # password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password']


class UpdateCustomerSerializer(serializers.ModelSerializer):
    customer_details = CustomerDetailsSerialzier()
    id = serializers.IntegerField(read_only=True)
    user = UserSerializer(source='user_id', write_only=True)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name',
                  'membership', 'customer_details', 'user']
        
    def create(self, validated_data):
        customer_details = validated_data.pop('customer_details')
        user_info = validated_data.pop('user_id')

        with atomic():
            User.objects.create_user(
                username=user_info.get('username'), password=user_info.get('password'), email=customer_details.get('email'))

            customer = Customer.objects.create(
                first_name=validated_data.get('first_name'), last_name=validated_data.get('last_name'), membership=validated_data.get('membership'))
            CustomerDetails.objects.create(
                customer=customer, **customer_details)

            return customer

    def update(self, instance, validated_data):
        customer_details_data = validated_data.get('customer_details')

        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.membership = validated_data.get('membership')
        instance.save()

        customer_details = instance.customer_details
        customer_details.email = customer_details_data.get('email')
        customer_details.phone = customer_details_data.get('phone')

        customer_details.save()

        return instance
