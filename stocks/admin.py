from django.contrib import admin
from .models import StockItem, Item

admin.site.register(Item)
admin.site.register(StockItem)
# Register your models here.
