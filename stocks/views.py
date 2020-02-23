from django.db.models import Count, Min, Max,Sum
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import ItemSerializer, SampleItemSerializer, StockItemSerializer, StockSerializer
from .models import Item, StockItem


class ItemViewSets(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer


class StockItemViewSets(viewsets.ModelViewSet):
    queryset = StockItem.objects.all()
    serializer_class = StockItemSerializer

    def create(self, request):
        item = request.POST.get("item")
        return self._send_item_to_stock(item, request)
        

    def _send_item_to_stock(self, item, data):
        try:
            stock_item = StockItem.objects.filter(item=item)
            if(len(stock_item) > 0):
                return self._update_stock_item(stock_item[0], data)
            return self._create_stock_item(data)
        except:
            return self._create_stock_item(data)

    def _update_stock_item(self, stock_item, data):
        new_quantity = data.POST.get("stock_quantity", None)
        min_stock = data.POST.get("min_stock", None)
        if(min_stock):
            stock_item.min_stock = int(min_stock)
        if(new_quantity):
            stock_item.stock_quantity += int(new_quantity)
        stock_item.save()
        serializer = StockItemSerializer(stock_item)
        return Response(serializer.data)


    def _create_stock_item(self, data):
        print("create")
        serializer = StockItemSerializer(data=data.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class StockViewSets(viewsets.ViewSet):

    def list(self, request):
        items_in_stock = StockItem.objects.all().count()
        total_quantity = StockItem.objects.aggregate(total_quantity=Sum("stock_quantity"))        
        total_price = StockItem.objects.aggregate(total_price=Sum("item__price"))
        total_cost = StockItem.objects.aggregate(total_cost=Sum("item__cost"))

        max_stock_item = StockItem.objects.aggregate(max_stock=Max("item"))["max_stock"]
        min_tock_item = StockItem.objects.aggregate(min_tock=Max("item"))["min_tock"]

        max_stock_item = self._get_item_or_none(max_stock_item)
        min_tock_item = self._get_item_or_none(min_tock_item)

        total_price = total_price["total_price"]
        total_cost = total_cost["total_cost"]

        total_money_in_stock = total_price - total_cost

        return Response(
            {
                "total_money": total_money_in_stock,
                "total_items_in_stock": items_in_stock,
                "max_stock_item":max_stock_item,
                "min_tock_item": min_tock_item
            }
            )


    def _get_item_or_none(self, item):
        try:
            item = Item.objects.get(pk=item)
            serializer = SampleItemSerializer(item)
            return serializer.data
        except:
            return None
