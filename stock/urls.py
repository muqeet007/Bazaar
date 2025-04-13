from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from stock.views import StoreViewSet, ProductViewSet, StockMovementViewSet

router = DefaultRouter()
router.register(r'stores', StoreViewSet)
router.register(r'products', ProductViewSet)
router.register(r'stock-movements', StockMovementViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]