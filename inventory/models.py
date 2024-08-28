from django.db import models
from products.models import Product
from users.models import Administrator


class Stock(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE, related_name='stock_product')
    administrator = models.ForeignKey(Administrator, on_delete=models.CASCADE)
    available_quantity = models.PositiveIntegerField()
    last_updated = models.DateTimeField(auto_now=True)
