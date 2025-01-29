from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .api.v1.transaction_serializer import TransactionSerializer
from .api.v1.user_serializer import UserSerializer
from .api.v1.wallet_serializer import WalletSerializer
from .models import Transaction, User, Wallet


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WalletViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
