from rest_framework import serializers
from .models import WalletUser, Portfolio

class WalletUserSerializer(serializers.ModelSerializer):
    class Meta:
        model  = WalletUser
        fields = ['id', 'username', 'email', 'wallet_address',
                  'chain', 'balance_usdt', 'total_trades', 'success_rate']

class PortfolioSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Portfolio
        fields = '__all__'