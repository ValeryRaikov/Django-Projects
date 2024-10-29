from django.db import models
from django.contrib.auth import get_user_model
from django.core import validators

User = get_user_model()


class Customer(models.Model):
    NAME_MAX_LEN = 100
    NAME_MIN_LEN = 2

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        validators=[
            validators.MinLengthValidator(NAME_MIN_LEN),
        ],
    )

    email = models.EmailField()

    def __str__(self):
        return self.name


class Product(models.Model):
    NAME_MAX_LEN = 100
    NAME_MIN_LEN = 2
    PRICE_MIN_VALUE = 0

    name = models.CharField(
        max_length=NAME_MAX_LEN,
        validators=[
            validators.MinLengthValidator(NAME_MIN_LEN),
        ],
    )

    price = models.DecimalField(
        max_digits=7,
        decimal_places=2,
        validators=[
            validators.MinValueValidator(PRICE_MIN_VALUE),
        ],
    )

    digital = models.BooleanField(
        default=False,
        null=True,
        blank=True,
    )

    image = models.ImageField(
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name

    @property
    def imageUrl(self):
        try:
            url = self.image.url
        except:
            url = ''

        return url


class Order(models.Model):
    TRANSACTION_ID_MAX_LEN = 50
    TRANSACTION_ID_MIN_LEN = 2

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    date_order = models.DateTimeField(
        auto_now_add=True,
    )

    complete = models.BooleanField(
        default=False,
    )

    transaction_id = models.CharField(
        max_length=TRANSACTION_ID_MAX_LEN,
        validators=[
            validators.MinLengthValidator(TRANSACTION_ID_MIN_LEN),
        ],
    )

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_cart_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def shipping(self):
        shipping = False

        order_items = self.orderitem_set.all()
        for item in order_items:
            if not item.product.digital:
                shipping = True

        return shipping


class OrderItem(models.Model):
    QUANTITY_MIN_VALUE = 0

    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    quantity = models.IntegerField(
        default=0,
        validators=[
            validators.MinValueValidator(QUANTITY_MIN_VALUE),
        ],
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        total = self.product.price * self.quantity
        return total


class ShippingAddress(models.Model):
    ADDRESS_MAX_LEN = 200
    CITY_MAX_LEN = 100
    STATE_MAX_LEN = 100
    ZIPCODE_MAX_LEN = 100
    FIELD_MIN_LEN = 2

    customer = models.ForeignKey(
        Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    order = models.ForeignKey(
        Order,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    address = models.CharField(
        max_length=ADDRESS_MAX_LEN,
        validators=[
            validators.MinValueValidator(FIELD_MIN_LEN),
        ],
    )

    city = models.CharField(
        max_length=CITY_MAX_LEN,
        validators=[
            validators.MinValueValidator(FIELD_MIN_LEN),
        ],
    )

    state = models.CharField(
        max_length=STATE_MAX_LEN,
        validators=[
            validators.MinValueValidator(FIELD_MIN_LEN),
        ],
    )

    zipcode = models.CharField(
        max_length=ZIPCODE_MAX_LEN,
        validators=[
            validators.MinValueValidator(FIELD_MIN_LEN),
        ],
    )

    date_added = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.address
