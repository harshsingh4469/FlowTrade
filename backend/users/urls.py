from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, PortfolioViewSet

router = DefaultRouter()
router.register(r'users',     UserViewSet)
router.register(r'portfolio', PortfolioViewSet)

urlpatterns = [
    path('', include(router.urls)),
]