from django.db import models
from django.db.models import Manager
from uuid import uuid4
from django.core.validators import MinValueValidator
from django.utils.text import slugify
from decimal import Decimal


class Collection(models.Model):
    """Collection Model

        title: <str> name of the collection
        featured_product: List<Product> products that belong to the collection
    """
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title


class Promotion(models.Model):
    title = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=6, decimal_places=2)


class Product(models.Model):
    collection = models.ForeignKey(
        Collection, on_delete=models.CASCADE, null=True, blank=True, default=None)
    title = models.CharField(max_length=255)
    slug = models.SlugField(null=True, default=None)
    description = models.TextField(null=False, blank=True, default='')
    inventory = models.IntegerField(
        validators=[MinValueValidator(Decimal('0'))], default=0)
    promotions = models.ManyToManyField(
        Promotion, blank=True, default=None)
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(Decimal('0'))], null=False, blank=False)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs) -> None:
        if self.title:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.street}, {self.city} {self.zip}'

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'


class Customer(models.Model):
    MEMBERSHIP_BRONZE_NAME = 'B'
    MEMBERSHIP_SILVER_NAME = 'S'
    MEMBERSHIP_GOLD_NAME = 'G'

    MEMBERSHIP_OPTIONS = [
        (MEMBERSHIP_BRONZE_NAME, 'Bronze'),
        (MEMBERSHIP_SILVER_NAME, 'Silver'),
        (MEMBERSHIP_GOLD_NAME, 'Gold'),
    ]

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    membership = models.CharField(
        max_length=1, choices=MEMBERSHIP_OPTIONS, default=MEMBERSHIP_BRONZE_NAME)

    addresses = models.ManyToManyField(Address, blank=True)
    # Type annotations
    customerdetails: models.Manager['CustomerDetails']

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'


class CustomerDetails(models.Model):
    customer_id = models.OneToOneField(Customer, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)

    class Meta:
        verbose_name = 'Customer Detail'
        verbose_name_plural = 'Customer Details'


class Order(models.Model):
    PAYMENT_STATUS_COMPLETE = 'C'
    PAYMENT_STATUS_FAIL = 'F'
    PAYMENT_STATUS_PENDING = 'P'

    PAYMENT_STATUS_OPTIONS = [
        (PAYMENT_STATUS_COMPLETE, 'Complete'),
        (PAYMENT_STATUS_FAIL, 'Failed'),
        (PAYMENT_STATUS_PENDING, 'Pending'),
    ]

    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True)
    payment_status = models.CharField(
        max_length=1, choices=PAYMENT_STATUS_OPTIONS, default=PAYMENT_STATUS_PENDING)
    created_at = models.DateTimeField(auto_now_add=True)

    # Type annotations
    orderitem_set: Manager['OrderItem']

    def __str__(self) -> str:
        return f'{self.customer} at {self.created_at}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    product_title = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()


class Cart(models.Model):
    """Cart Model

        id: <UUID> a uuid of the cart
        created_at: <datetime> datetime that the record was created at
        cartitem_set: <Manager['CartItem']> reverse relationship created by cart item model
    """
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    # Type annotation
    cartitem_set: Manager['CartItem']

    def __str__(self):
        return str(self.id)


class CartItem(models.Model):
    """Cart Item Model

        cart_id: <int> cart id
        product_id: <ForeignKey[Product | None]> product id
        quantity: <int> item quantity
    """
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(validators=[MinValueValidator(Decimal('0'))])

    class Meta:
        verbose_name = 'Cart Item'
        verbose_name_plural = 'Cart Items'
        unique_together = [('cart', 'product')]


    def __str__(self):
        if self.product:
            return self.product.title
        return None


class Review(models.Model):
    REVIEW_RATING_OPTION_ONE = '1'
    REVIEW_RATING_OPTION_TWO = '2'
    REVIEW_RATING_OPTION_THREE = '3'
    REVIEW_RATING_OPTION_FOUR = '4'
    REVIEW_RATING_OPTION_FIVE = '5'

    REVIEW_RATING_OPTIONS = [
        (REVIEW_RATING_OPTION_ONE, '1 star'),
        (REVIEW_RATING_OPTION_TWO, '2 star'),
        (REVIEW_RATING_OPTION_THREE, '3 star'),
        (REVIEW_RATING_OPTION_FOUR, '4 star'),
        (REVIEW_RATING_OPTION_FIVE, '5 star'),
    ]

    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    description = models.TextField()
    rating = models.CharField(
        max_length=1, choices=REVIEW_RATING_OPTIONS, default=REVIEW_RATING_OPTION_ONE)
