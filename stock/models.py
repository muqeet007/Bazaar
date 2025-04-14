from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils import timezone

class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    store = models.ForeignKey(Store, on_delete=models.CASCADE, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['store', 'stock_quantity']),
        ]

class StockMovement(models.Model):
    MOVEMENT_TYPES = [
        ('STOCK_IN', 'Stock In'),
        ('SALE', 'Sale'),
        ('MANUAL_REMOVAL', 'Manual Removal'),
    ]
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='stock_movements')
    quantity = models.IntegerField()
    movement_type = models.CharField(max_length=20, choices=MOVEMENT_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def clean(self):
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than zero')
        
        if self.movement_type in ['SALE', 'MANUAL_REMOVAL']:
            if self.product.stock_quantity < self.quantity:
                raise ValidationError('Not enough stock available')

    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.movement_type} of {self.quantity} for {self.product.name}"

    class Meta:
        indexes = [
            models.Index(fields=['product', 'movement_type', 'created_at']),
        ]
        ordering = ['-created_at']

class AuditLog(models.Model):
    stock_movement = models.ForeignKey(StockMovement, on_delete=models.CASCADE, related_name='audit_logs', null=True, blank=True)
    stock_movement_created_at = models.DateTimeField(null=True, blank=True, default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if not self.stock_movement and not self.stock_movement_created_at:
            raise ValidationError('Either stock_movement or stock_movement_created_at must be provided')
        if self.stock_movement and self.stock_movement_created_at:
            self.stock_movement_created_at = self.stock_movement.created_at

    def save(self, *args, **kwargs):
        self.full_clean()  # Run validation
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.action} by {self.user} at {self.timestamp}"

    class Meta:
        indexes = [
            models.Index(fields=['stock_movement', 'timestamp']),
        ]
        ordering = ['-timestamp']