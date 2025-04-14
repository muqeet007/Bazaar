# stock/tasks.py
from celery import shared_task
from django.db import transaction
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from stock.models import Product, StockMovement, AuditLog

@shared_task(bind=True, max_retries=3)
def process_stock_update(self, product_id, quantity, movement_type, user_id=None):
    try:
        with transaction.atomic():
            product = Product.objects.select_for_update().get(id=product_id)
            if movement_type == 'SALE' and product.stock_quantity < quantity:
                raise ValueError('Not enough stock for sale')
            if movement_type in ['SALE', 'MANUAL_REMOVAL'] and quantity > 0:
                quantity = -quantity

            user = User.objects.get(id=user_id) if user_id else None
            
            # Create stock movement
            stock_movement = StockMovement.objects.create(
                product=product,
                quantity=quantity,
                movement_type=movement_type,
                user=user
            )
            
            # Create audit log
            AuditLog.objects.create(
                stock_movement=stock_movement,
                stock_movement_created_at=stock_movement.created_at,
                user=user,
                action=movement_type
            )
            
            return {
                'status': 'success',
                'stock_movement_id': stock_movement.id,
                'new_stock_quantity': product.stock_quantity
            }
            
    except ValidationError as e:
        # Retry on validation errors
        raise self.retry(exc=e, countdown=2 ** self.request.retries)
    except Exception as e:
        # Log the error and retry
        raise self.retry(exc=e, countdown=2 ** self.request.retries)