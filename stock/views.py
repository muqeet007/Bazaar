from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Store, Product, StockMovement
from .serializers import StoreSerializer, ProductSerializer, StockMovementSerializer
from .tasks import process_stock_update

class StoreViewSet(viewsets.ModelViewSet):
    queryset = Store.objects.all()
    serializer_class = StoreSerializer
    permission_classes = [permissions.IsAuthenticated]

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = Product.objects.all().select_related('store')
        store_id = self.request.query_params.get('store_id')
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        return queryset

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

    @action(detail=True, methods=['post'])
    def stock_in(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        if quantity <= 0:
            return Response({'error': 'Quantity must be positive'}, status=400)
        process_stock_update.delay(product.id, quantity, 'STOCK_IN', user_id=request.user.id)
        return Response({'status': f'Queued stock addition of {quantity} to {product.name}'})

    @action(detail=True, methods=['post'])
    def sell(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        if quantity <= 0 or quantity > product.stock_quantity:
            return Response({'error': 'Invalid quantity'}, status=400)
        process_stock_update.delay(product.id, -quantity, 'SALE', user_id=request.user.id)
        return Response({'status': f'Queued sale of {quantity} of {product.name}'})

    @action(detail=True, methods=['post'])
    def remove(self, request, pk=None):
        product = self.get_object()
        quantity = int(request.data.get('quantity', 0))
        if quantity <= 0 or quantity > product.stock_quantity:
            return Response({'error': 'Invalid quantity'}, status=400)
        process_stock_update.delay(product.id, -quantity, 'MANUAL_REMOVAL', user_id=request.user.id)
        return Response({'status': f'Queued removal of {quantity} of {product.name}'})

class StockMovementViewSet(viewsets.ModelViewSet):
    queryset = StockMovement.objects.all()
    serializer_class = StockMovementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = StockMovement.objects.all().select_related('product__store')
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

    @method_decorator(cache_page(60 * 15))  # Cache for 15 minutes
    def list(self, *args, **kwargs):
        return super().list(*args, **kwargs)

class StockMovementTrendsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        store_id = request.query_params.get('store_id')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        queryset = StockMovement.objects.all()
        if store_id:
            queryset = queryset.filter(product__store_id=store_id)
        if start_date:
            queryset = queryset.filter(created_at__gte=start_date)
        if end_date:
            queryset = queryset.filter(created_at__lte=end_date)

        trends = (queryset
                  .annotate(date=TruncDate('created_at'))
                  .values('date', 'movement_type')
                  .annotate(total_quantity=Sum('quantity'), count=Count('id'))
                  .order_by('date'))

        return Response(trends)

class LowStockAlertsView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        threshold = int(request.query_params.get('threshold', 10))
        store_id = request.query_params.get('store_id')

        queryset = Product.objects.filter(stock_quantity__lte=threshold)
        if store_id:
            queryset = queryset.filter(store_id=store_id)

        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)