from rest_framework import serializers
from .models import Token, Trade, LiquidityPool

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Token
        fields = '__all__'

class TradeSerializer(serializers.ModelSerializer):
    token_in_symbol  = serializers.CharField(source='token_in.symbol',  read_only=True)
    token_out_symbol = serializers.CharField(source='token_out.symbol', read_only=True)

    class Meta:
        model  = Trade
        fields = '__all__'

class LiquidityPoolSerializer(serializers.ModelSerializer):
    token_a_symbol = serializers.CharField(source='token_a.symbol', read_only=True)
    token_b_symbol = serializers.CharField(source='token_b.symbol', read_only=True)

    class Meta:
        model  = LiquidityPool
        fields = '__all__'