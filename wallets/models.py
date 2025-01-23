from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


class User(AbstractUser):
    email = models.EmailField(unique=True)
    REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'

    # Definindo related_name únicos para evitar conflitos
    groups = models.ManyToManyField(
        Group,
        related_name='wallets_user_set',  # Nome único
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='wallets_user_permissions_set',  # Nome único
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )

    def __str__(self):
        return self.username


class Wallet(models.Model):
    account = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.account.username} - R$ {self.balance}'

    class Meta:
        verbose_name = 'Wallet'
        verbose_name_plural = 'Wallets'


class Transaction(models.Model):
    sender = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='receiver')
    timestamp = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return (
            f'{self.sender.account.username} -> '
            f'{self.receiver.account.username} - R$ {self.amount}'
        )

    class Meta:
        verbose_name = 'Transaction'
        verbose_name_plural = 'Transactions'
