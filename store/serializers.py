from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from django.db.transaction import atomic
from .models import Product, Collection, Cart, CartItem, Customer, CustomerDetails, Address, Order, OrderItem


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
    product = serializers.SerializerMethodField(method_name='get_product')
    total_price = serializers.SerializerMethodField(
        method_name='calc_total_price')

    def get_product(self, cart_item: CartItem):
        return SimpleProductSerializer(cart_item.product).data

    def calc_total_price(self, cart_item: CartItem):
        return cart_item.quantity * cart_item.product.unit_price if cart_item.product else 0

    class Meta:
        model = CartItem
        fields = ['id', 'quantity', 'product', 'total_price']


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

    def update(self, instance, validated_data):
        # Check if default address already exists for the customer,
        # if so, set previous default address as normal one
        customer = Customer.objects.get(user_id=self.context['user_id'])
        if validated_data.get('is_default', False):
            customer.addresses.filter(is_default=True).update(is_default=False)
        # Update target address
        instance.street = validated_data.get('street', instance.street)
        instance.city = validated_data.get('city', instance.city)
        instance.zip = validated_data.get('zip', instance.zip)
        instance.is_default = validated_data.get(
            'is_default', instance.is_default)
        instance.save()

        return instance

    class Meta:
        model = Address
        fields = ['id', 'street', 'city', 'zip', 'is_default']


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


class UpdateCustomerSerializer(serializers.ModelSerializer):
    customer_details = CustomerDetailsSerialzier(
        allow_null=True, required=False)
    id = serializers.IntegerField(read_only=True)
    address = AddressSerializer(
        write_only=True, allow_null=True, required=False)

    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name',
                  'membership', 'customer_details', 'address']

    def create(self, validated_data):
        customer_details = validated_data.pop('customer_details')

        with atomic():
            customer = Customer.objects.create(
                first_name=validated_data.get('first_name'), last_name=validated_data.get('last_name'), membership=validated_data.get('membership'))
            CustomerDetails.objects.create(
                customer=customer, **customer_details)
            return customer

    def update(self, instance, validated_data):
        customer_details_data = validated_data.get('customer_details')

        with atomic():
            instance.first_name = validated_data.get(
                'first_name', instance.first_name)
            instance.last_name = validated_data.get(
                'last_name', instance.last_name)
            instance.membership = validated_data.get(
                'membership', instance.membership)

            address_data = validated_data.get('address')
            if address_data:
                street = address_data.get('street', None)
                city = address_data.get('city', None)
                zip_code = address_data.get('zip', None)
                is_default = address_data.get('is_default', False)
                # Unselect previous default default address
                if is_default:
                    instance.addresses.filter(is_default=True).update(is_default=False)

                (address, created) = Address.objects.get_or_create(
                    street=street, city=city, zip=zip_code, is_default=is_default
                )
                instance.addresses.add(address)
            instance.save()

            if customer_details_data:
                if hasattr(instance, 'customer_details'):
                    customer_details = instance.customer_details
                    customer_details.email = customer_details_data.get(
                        'email', customer_details.email)
                    customer_details.phone = customer_details_data.get(
                        'phone', customer_details.phone)
                    customer_details.birth_date = customer_details_data.get(
                        'birth_date', customer_details.birth_date)
                    customer_details.save()
                else:
                    new_email = customer_details_data.get('email', None)
                    new_phone = customer_details_data.get('phone', None)
                    new_birth_date = customer_details_data.get(
                        'birth_date', None)
                    CustomerDetails.objects.create(
                        email=new_email, phone=new_phone, birth_date=new_birth_date, customer=instance
                    )
                    instance.save()
        return instance


class SimpleOrderItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = ['id', 'product_title', 'quantity', 'unit_price']


class OrderSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField(method_name='get_items')
    customer = serializers.SerializerMethodField(
        method_name='get_customer_name')
    total_price = serializers.SerializerMethodField(
        method_name='get_total_price')

    def get_items(self, order: Order):
        order_items = order.orderitem_set
        order_items_serializer = SimpleOrderItemSerializer(
            order_items, many=True)
        return order_items_serializer.data

    def get_customer_name(self, order: Order):
        customer_name = f'{order.customer.first_name if order.customer else ''} {
            order.customer.last_name if order.customer else ''}'
        return customer_name

    def get_total_price(self, order: Order):
        total_price = sum([item.quantity *
                           item.unit_price for item in order.orderitem_set.all()])
        return total_price

    class Meta:
        model = Order
        fields = ['id', 'customer', 'created_at',
                  'payment_status', 'items', 'total_price', 'address']


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()
    address_id = serializers.IntegerField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise ValidationError('No cart matches the given cart id')
        if CartItem.objects.filter(cart=cart_id).count() == 0:
            raise ValidationError('The cart is empty')
        return cart_id

    def validate_address_id(self, address_id):
        user_id = self.context['user_id']
        customer = Customer.objects.get(user_id=user_id)
        if not Address.objects.filter(customer=customer, id=address_id).exists():
            raise ValidationError(
                'Address with the given id does not belong to current customer')
        return address_id

    def save(self, **kwargs):
        cart_id = self.validated_data['cart_id']
        address_id = self.validated_data['address_id']
        user_id = self.context['user_id']

        with atomic():
            cart_items = CartItem.objects.select_related(
                'product').filter(cart_id=cart_id)
            customer = Customer.objects.get(user_id=user_id)
            address = customer.addresses.get(id=address_id)
            address_str = f'{address.street}, {address.city} {address.zip}'
            print(address_str)

            order = Order.objects.create(customer=customer, address=address_str)

            order_items = [OrderItem(order=order, product_title=item.product.title,
                                     unit_price=item.product.unit_price, quantity=item.quantity) for item in cart_items]
            OrderItem.objects.bulk_create(order_items)
            [item.delete() for item in cart_items]
        return order


class UpdateOrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ['payment_status']
