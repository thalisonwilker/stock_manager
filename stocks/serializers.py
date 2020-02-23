from rest_framework import serializers
from .models import Item, StockItem


class StockSerializer(serializers.Serializer):

    def to_representation(self, obj):
        data = {}
        print(obj)
        return data


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class SampleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("id", "name", "price", "cost")

class StockItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockItem
        fields = "__all__"
