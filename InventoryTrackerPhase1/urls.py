from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from stock.views import StoreViewSet, ProductViewSet, StockMovementViewSet, StockMovementTrendsView, LowStockAlertsView

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'products', ProductViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/stock-movement-trends/', StockMovementTrendsView.as_view(), name='stock-movement-trends'),
    path('api/low-stock-alerts/', LowStockAlertsView.as_view(), name='low-stock-alerts'),
]