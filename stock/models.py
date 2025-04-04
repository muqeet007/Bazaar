from django.db import models
from django.core.exceptions import ValidationError

class Product(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)

    def current_quantity(self):
        total_quantity = 0
        for movement in self.movements.all(): 
            if movement.movement_type == 'IN':
                total_quantity += movement.quantity
            else:
                total_quantity -= movement.quantity
        return total_quantity  

    def __str__(self):
        return self.name

class StockMovement(models.Model):
    MOVEMENT_CATEGORIES = [
        ('IN', 'Stock In'),
        ('SALE', 'Sale'),
        ('REMOVE', 'Remove'),
    ]

    product = models.ForeignKey(Product, related_name='movements', on_delete=models.CASCADE)
    movement_type = models.CharField(max_length=10, choices=MOVEMENT_CATEGORIES)
    quantity = models.PositiveBigIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.movement_type} {self.quantity} ---> {self.product}"