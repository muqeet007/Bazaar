from django.contrib import admin
from .models import Store, Product, StockMovement, AuditLog

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'created_at')
    search_fields = ('name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'store', 'price', 'stock_quantity', 'created_at')
    list_filter = ('store',)
    search_fields = ('name',)

@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'movement_type', 'created_at')
    list_filter = ('movement_type', 'created_at')
    search_fields = ('product__name',)

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('stock_movement', 'user', 'action', 'timestamp')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username',)
    fields = ('stock_movement', 'user', 'action')
    readonly_fields = ('timestamp',)