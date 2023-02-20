from _decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Item(models.Model):
    """ Model for selling items."""
    CUR = (
        ('USD', 'USD'),
        ('EUR', 'EUR'),
    )
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Item name')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.50'))] # price must be more than 50 cents
    )
    currency = models.CharField(
        max_length=10,
        default='USD',
        choices=CUR)

    def __str__(self):
        return self.name


class Discount(models.Model):
    """ Model for discount."""
    name = models.CharField(max_length=30,
                            unique=True,)
    percent_off = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(99)])

    def __str__(self):
        return str(self.name) + ' is ' + f'{self.percent_off}%'


class Tax(models.Model):
    """ Model for taxes."""
    value = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)])
    name = models.CharField(max_length=30, unique=True)
    stripe_id = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return str(self.name) + ' - ' + f'{self.value}%'


class Order(models.Model):
    """ Model for order. Can combine multiple items.."""
    customer = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='posts')
    item = models.ForeignKey(
        Item,
        on_delete=models.PROTECT)
    is_paid = models.BooleanField(default=False, verbose_name='Payment status')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    tax = models.ForeignKey(
        Tax,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT)
    discount = models.ForeignKey(
        Discount,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT)

    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    """ Model for connecting items and orders."""
    order = models.ForeignKey(
        Order,
        related_name='items',
        on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item,
        related_name='order_items',
        on_delete=models.CASCADE)
    price = models.IntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.item)

    def get_cost(self):
        return self.price * self.quantity
