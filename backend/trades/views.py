from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
import random
from .models import Token, Trade, LiquidityPool
from .serializers import TokenSerializer, TradeSerializer, LiquidityPoolSerializer

class TokenViewSet(viewsets.ModelViewSet):
    queryset         = Token.objects.all()
    serializer_class = TokenSerializer

    @action(detail=False, methods=['get'])
    def market_overview(self, request):
        tokens = Token.objects.all()
        data   = TokenSerializer(tokens, many=True).data
        return Response({
            'total_tokens': tokens.count(),
            'total_volume': sum(float(t.volume_24h) for t in tokens),
            'tokens':       data
        })

class TradeViewSet(viewsets.ModelViewSet):
    queryset         = Trade.objects.all().order_by('-created_at')
    serializer_class = TradeSerializer

    @action(detail=False, methods=['post'])
    def execute(self, request):
        data = request.data
        try:
            token_in  = Token.objects.get(id=data['token_in_id'])
            token_out = Token.objects.get(id=data['token_out_id'])
            amount_in = float(data['amount_in'])
            price_ratio = float(token_in.price) / float(token_out.price)
            slippage    = float(data.get('slippage', 0.5)) / 100
            amount_out  = amount_in * price_ratio * (1 - slippage)
            gas_fee     = random.uniform(0.001, 0.01)
            trade = Trade.objects.create(
                token_in       = token_in,
                token_out      = token_out,
                amount_in      = amount_in,
                amount_out     = amount_out,
                trade_type     = 'SWAP',
                status         = 'COMPLETED',
                slippage       = slippage * 100,
                gas_fee        = gas_fee,
                wallet_address = data.get('wallet_address', '0x000'),
                completed_at   = timezone.now()
            )
            return Response({
                'success':    True,
                'trade_id':   trade.id,
                'amount_in':  amount_in,
                'amount_out': round(amount_out, 6),
                'gas_fee':    round(gas_fee, 6),
                'status':     'COMPLETED',
                'message':    f'Swapped {amount_in} {token_in.symbol} → {round(amount_out, 6)} {token_out.symbol}'
            })
        except Exception as e:
            return Response({'success': False, 'error': str(e)},
                          status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        trades    = Trade.objects.all()
        completed = trades.filter(status='COMPLETED')
        return Response({
            'total_trades':     trades.count(),
            'completed_trades': completed.count(),
            'success_rate':     round(completed.count() / max(trades.count(), 1) * 100, 1),
            'total_volume':     sum(float(t.amount_in) for t in completed),
        })

class LiquidityPoolViewSet(viewsets.ModelViewSet):
    queryset         = LiquidityPool.objects.all()
    serializer_class = LiquidityPoolSerializer

    @action(detail=False, methods=['get'])
    def overview(self, request):
        pools = LiquidityPool.objects.all()
        return Response({
            'total_pools':    pools.count(),
            'average_uptime': round(sum(float(p.uptime) for p in pools) / max(pools.count(), 1), 1),
            'pools':          LiquidityPoolSerializer(pools, many=True).data
        })