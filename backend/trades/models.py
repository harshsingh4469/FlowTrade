from django.db import models

class Token(models.Model):
    CHAIN_CHOICES = [
        ('ETH', 'Ethereum'),
        ('BSC', 'Binance Smart Chain'),
        ('POLY', 'Polygon'),
        ('SOL', 'Solana'),
    ]
    name     = models.CharField(max_length=100)
    symbol   = models.CharField(max_length=20)
    chain    = models.CharField(max_length=10, choices=CHAIN_CHOICES)
    price    = models.DecimalField(max_digits=20, decimal_places=8)
    liquidity = models.DecimalField(max_digits=20, decimal_places=2)
    volume_24h = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} ({self.chain})"


class Trade(models.Model):
    STATUS_CHOICES = [
        ('PENDING',   'Pending'),
        ('COMPLETED', 'Completed'),
        ('FAILED',    'Failed'),
    ]
    TYPE_CHOICES = [
        ('BUY',  'Buy'),
        ('SELL', 'Sell'),
        ('SWAP', 'Swap'),
    ]
    token_in    = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='trades_in')
    token_out   = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='trades_out')
    amount_in   = models.DecimalField(max_digits=20, decimal_places=8)
    amount_out  = models.DecimalField(max_digits=20, decimal_places=8)
    trade_type  = models.CharField(max_length=10, choices=TYPE_CHOICES)
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    slippage    = models.DecimalField(max_digits=5, decimal_places=2, default=0.5)
    gas_fee     = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    wallet_address = models.CharField(max_length=100)
    created_at  = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.trade_type} {self.amount_in} {self.token_in.symbol} → {self.token_out.symbol}"


class LiquidityPool(models.Model):
    token_a     = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='pools_a')
    token_b     = models.ForeignKey(Token, on_delete=models.CASCADE, related_name='pools_b')
    reserve_a   = models.DecimalField(max_digits=20, decimal_places=8)
    reserve_b   = models.DecimalField(max_digits=20, decimal_places=8)
    fee_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.3)
    chain       = models.CharField(max_length=10)
    uptime      = models.DecimalField(max_digits=5, decimal_places=2, default=98.0)
    created_at  = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.token_a.symbol}/{self.token_b.symbol} Pool"