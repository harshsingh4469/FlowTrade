from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import authenticate
from .models import WalletUser, Portfolio
from .serializers import WalletUserSerializer, PortfolioSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset         = WalletUser.objects.all()
    serializer_class = WalletUserSerializer

    @action(detail=False, methods=['post'])
    def register(self, request):
        """Register a new wallet user."""
        data = request.data
        try:
            user = WalletUser.objects.create_user(
                username       = data['username'],
                password       = data['password'],
                email          = data.get('email', ''),
                wallet_address = data.get('wallet_address', ''),
                chain          = data.get('chain', 'ETH'),
                balance_usdt   = 1000.00
            )
            return Response({
                'success': True,
                'user_id': user.id,
                'username': user.username,
                'wallet_address': user.wallet_address,
                'balance_usdt': str(user.balance_usdt),
                'message': 'User registered successfully!'
            })
        except Exception as e:
            return Response({'success': False, 'error': str(e)},
                          status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def login(self, request):
        """Login with username and password."""
        user = authenticate(
            username = request.data.get('username'),
            password = request.data.get('password')
        )
        if user:
            return Response({
                'success':        True,
                'user_id':        user.id,
                'username':       user.username,
                'wallet_address': user.wallet_address,
                'balance_usdt':   str(user.balance_usdt),
                'total_trades':   user.total_trades,
            })
        return Response({'success': False, 'error': 'Invalid credentials'},
                       status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=True, methods=['get'])
    def portfolio(self, request, pk=None):
        """Get user portfolio."""
        user      = self.get_object()
        portfolio = Portfolio.objects.filter(user=user)
        return Response({
            'username':     user.username,
            'balance_usdt': str(user.balance_usdt),
            'total_trades': user.total_trades,
            'portfolio':    PortfolioSerializer(portfolio, many=True).data
        })


class PortfolioViewSet(viewsets.ModelViewSet):
    queryset         = Portfolio.objects.all()
    serializer_class = PortfolioSerializer