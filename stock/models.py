from django.db import models
from django.core.exceptions import ValidationError

class Store(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.store.name})"

class StockMovement(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='movements')
    quantity = models.IntegerField()  # Positive for stock-in, negative for sales/removals
    movement_type = models.CharField(max_length=50, choices=[
        ('STOCK_IN', 'Stock In'),
        ('SALE', 'Sale'),
        ('MANUAL_REMOVAL', 'Manual Removal'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} {self.quantity} of {self.product.name}"

    def clean(self):
        # Validate quantity based on movement_type
        if self.movement_type == 'STOCK_IN' and self.quantity <= 0:
            raise ValidationError("Quantity must be positive for STOCK_IN.")
        elif self.movement_type in ['SALE', 'MANUAL_REMOVAL'] and self.quantity >= 0:
            raise ValidationError("Quantity must be negative for SALE or MANUAL_REMOVAL.")
        # Ensure stock_quantity doesn't go negative
        if self.movement_type in ['SALE', 'MANUAL_REMOVAL']:
            new_stock = self.product.stock_quantity + self.quantity  # quantity is negative
            if new_stock < 0:
                raise ValidationError(f"Cannot reduce stock below 0. Current stock: {self.product.stock_quantity}, attempted reduction: {-self.quantity}")