from rest_framework import serializers
from .models import Store, Product, StockMovement

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = ['id', 'name', 'location', 'created_at']

class StockMovementSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'quantity', 'movement_type', 'created_at']

class ProductSerializer(serializers.ModelSerializer):
    store = StoreSerializer(read_only=True)
    movements = StockMovementSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['id', 'store', 'name', 'description', 'price', 'stock_quantity', 'created_at', 'updated_at', 'movements']