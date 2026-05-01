from django.db import models
from django.contrib.auth.models import AbstractUser

class WalletUser(AbstractUser):
    wallet_address = models.CharField(max_length=100, unique=True, null=True, blank=True)
    chain          = models.CharField(max_length=20, default='ETH')
    balance_usdt   = models.DecimalField(max_digits=20, decimal_places=2, default=1000.00)
    balance_eth    = models.DecimalField(max_digits=20, decimal_places=8, default=1.0)
    is_verified    = models.BooleanField(default=False)
    created_at     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username} ({self.wallet_address})"


class Portfolio(models.Model):
    user       = models.ForeignKey(WalletUser, on_delete=models.CASCADE, related_name='portfolio')
    token      = models.CharField(max_length=20)
    amount     = models.DecimalField(max_digits=20, decimal_places=8)
    avg_price  = models.DecimalField(max_digits=20, decimal_places=8)
    chain      = models.CharField(max_length=20)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.token}"