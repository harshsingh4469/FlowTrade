from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import TokenViewSet, TradeViewSet, LiquidityPoolViewSet

router = DefaultRouter()
router.register(r'tokens', TokenViewSet)
router.register(r'trades', TradeViewSet)
router.register(r'pools',  LiquidityPoolViewSet)

urlpatterns = [
    path('', include(router.urls)),
]