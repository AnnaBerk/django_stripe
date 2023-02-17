from django.db import models


class Item(models.Model):
    name = models.CharField(
        unique=True,
        max_length=256,
        verbose_name='Item')
    description = models.TextField(verbose_name='Description')
    price = models.DecimalField(
        max_digits=9,
        decimal_places=2)

    def __str__(self):
        return self.name


# class Order(models.Model):
#     item = models.ForeignKey(Item, on_delete=models.PROTECT)
#     checkout_session = models.CharField(max_length=200, unique=True)