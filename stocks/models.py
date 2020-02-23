from uuid import uuid4
from django.db import models

# Create your models here.


class Item(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4)
    name = models.CharField(max_length=200, db_column="item")
    price = models.DecimalField(decimal_places=2, max_digits=9999)
    cost = models.DecimalField(decimal_places=2, max_digits=9999)
    created_date = models.DateTimeField(auto_now=True)
    updated_date = models.DateTimeField(auto_now=True,null=False, blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class StockItem(models.Model):
    id = models.UUIDField(primary_key=True, editable=False, default=uuid4, db_column="stock_item")
    stock_quantity = models.IntegerField()
    min_stock = models.IntegerField(default=1)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.item.name} - Quantity: {self.stock_quantity}'


