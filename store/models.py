from django.db import models
from django.db.models import Manager
from uuid import uuid4


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        'Product', on_delete=models.SET_NULL, null=True, related_name='+')

    def __str__(self):
        return self.title


class Promotions(models.Model):
    title = models.CharField(max_length=255)
    discount = models.DecimalField(max_digits=6, decimal_places=2)


class Product(models.Model):
    collection = models.ForeignKey(Collection, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(default='-')
    description = models.TextField()
    inventory = models.IntegerField()
    promotions = models.ManyToManyField(Promotions, blank=True)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    last_updated = models.DateTimeField(auto_now=True)


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

    # Type annotation
    customerdetails_set: Manager['CustomerDetails']
    address_set: Manager['Address']


class CustomerDetails(models.Model):
    customer_id = models.OneToOneField(Customer, on_delete=models.CASCADE)
    email = models.EmailField()
    phone = models.CharField(max_length=255)
    birth_date = models.DateField(null=True)


class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255)
    customer = models.ManyToManyField(
        Customer, blank=True)


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


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, null=True)
    product_title = models.CharField(max_length=255)
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    cart_id: Manager['CartItem']


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()


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
