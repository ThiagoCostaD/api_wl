from django.utils.dateparse import parse_date
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .api.v1.transaction_serializer import TransactionSerializer
from .api.v1.user_serializer import UserSerializer
from .api.v1.wallet_serializer import WalletSerializer
from .models import Transaction, User, Wallet


class CreateUserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WalletViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAuthenticated])
    def add_balance(self, request, pk=None):
        wallet = self.get_object()
        amount = request.data.get("amount")

        if not amount or float(amount) <= 0:
            return Response(
                {"error": "O valor deve ser maior que 0."},
                status=status.HTTP_400_BAD_REQUEST
            )

        wallet.balance += float(amount)
        wallet.save()
        return Response(
            {
                "message": "Saldo adicionado com sucesso!",
                "new_balance": wallet.balance
            },
            status=status.HTTP_200_OK
        )


class WalletBalanceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer

    def get_queryset(self):
        return Wallet.objects.filter(account=self.request.user)


class TransactionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    @action(detail=False, methods=['post'])
    def transfer(self, request):
        """Cria uma transferência entre usuários"""
        sender_wallet = Wallet.objects.get(account=request.user)
        receiver_id = request.data.get("receiver_id")
        amount = float(request.data.get("amount", 0))

        if amount <= 0:
            return Response(
                {"error": "O valor da transferência deve ser maior que zero."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            receiver_wallet = Wallet.objects.get(account__id=receiver_id)
        except Wallet.DoesNotExist:
            return Response(
                {"error": "Destinatário não encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        if sender_wallet.balance < amount:
            return Response(
                {"error": "Saldo insuficiente."},
                status=status.HTTP_400_BAD_REQUEST
            )

        sender_wallet.balance -= amount
        receiver_wallet.balance += amount
        sender_wallet.save()
        receiver_wallet.save()

        transaction = Transaction.objects.create(
            sender=sender_wallet, receiver=receiver_wallet, amount=amount)
        return Response(
            {
                "message": "Transferência realizada com sucesso!",
                "transaction_id": transaction.id
            },
            status=status.HTTP_201_CREATED
        )

    def get_queryset(self):
        queryset = Transaction.objects.filter(sender__account=self.request.user)
        start_date = self.request.query_params.get("start_date")
        end_date = self.request.query_params.get("end_date")

        if start_date:
            queryset = queryset.filter(timestamp__gte=parse_date(start_date))
        if end_date:
            queryset = queryset.filter(timestamp__lte=parse_date(end_date))

        return queryset
