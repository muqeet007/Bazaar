from rest_framework import serializers
from .models import Product, StockMovement

class StockMovementSerializer(serializers.ModelSerializer):
    def validate_quantity(self, value):
        if value <= 0:
            raise serializers.ValidationError("Quantity must be a positive value.")
        return value
  
    class Meta:
        model = StockMovement
        fields = ['id', 'product', 'movement_type', 'quantity', 'timestamp']

class ProductSerializer(serializers.ModelSerializer):
    current_quantity = serializers.ReadOnlyField()
  
    class Meta:
        model = Product
        fields = ['id', 'name', 'current_quantity']