from django.contrib import admin
from .models import Product, StockMovement

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'current_quantity']

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ['product', 'movement_type', 'quantity', 'timestamp', 'current_product_quantity']

    def current_product_quantity(self, obj):
        return obj.product.current_quantity()
    current_product_quantity.short_description = 'Current Quantity'