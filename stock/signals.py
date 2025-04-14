from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction
from .models import StockMovement

@receiver(post_save, sender=StockMovement)
def update_product_stock(sender, instance, created, **kwargs):
    if created:  # Only update on creation, not on updates
        with transaction.atomic():
            product = instance.product
            if instance.movement_type == 'STOCK_IN':
                product.stock_quantity += instance.quantity
            elif instance.movement_type in ['SALE', 'MANUAL_REMOVAL']:
                product.stock_quantity -= instance.quantity
            product.save()