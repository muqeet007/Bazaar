from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Store, Product, StockMovement
from .serializers import StoreSerializer, ProductSerializer, StockMovementSerializer

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all()
        store_id = self.request.query_params.get('store_id')
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset

    @action(detail=True, methods=['post'])
    def stock_in(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        if quantity <= 0:
            return Response({'error': 'Quantity must be positive'}, status=400)
        # No need to update stock_quantity manually; the signal will handle it
        StockMovement.objects.create(
            product=product,
            quantity=quantity,
            movement_type='STOCK_IN'
        )
        return Response({'status': f'Added {quantity} to {product.name}'})

    @action(detail=True, methods=['post'])
    def sell(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        if quantity <= 0 or quantity > product.stock_quantity:
            return Response({'error': 'Invalid quantity'}, status=400)
        # No need to update stock_quantity manually; the signal will handle it
        StockMovement.objects.create(
            product=product,
            quantity=-quantity,  # Ensure quantity is negative for SALE
            movement_type='SALE'
        )
        return Response({'status': f'Sold {quantity} of {product.name}'})

    @action(detail=True, methods=['post'])
    def remove(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        if quantity <= 0 or quantity > product.stock_quantity:
            return Response({'error': 'Invalid quantity'}, status=400)
        # No need to update stock_quantity manually; the signal will handle it
        StockMovement.objects.create(
            product=product,
            quantity=-quantity,  # Ensure quantity is negative for MANUAL_REMOVAL
            movement_type='MANUAL_REMOVAL'
        )
        return Response({'status': f'Removed {quantity} of {product.name}'})

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = StockMovement.objects.all()
        store_id = self.request.query_params.get('store_id')
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        if store_id:
            queryset = queryset.filter(product__store_id=store_id)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)
        return queryset