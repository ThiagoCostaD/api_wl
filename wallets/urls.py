from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CreateUserViewSet, TransactionViewSet, UserViewSet,
                    WalletViewSet)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename="user")
router.register(r'wallets', WalletViewSet, basename="wallet")
router.register(r'transactions', TransactionViewSet, basename="transaction")

urlpatterns = [
    path('', include(router.urls)),

    path(
        "users/create/",
        CreateUserViewSet.as_view({"post": "create"}),
        name="user-create"
    ),

    path(
        "wallets/<int:pk>/add_balance/",
        WalletViewSet.as_view({"post": "add_balance"}),
        name="wallet-add-balance"
    ),

    path(
        "transactions/transfer/",
        TransactionViewSet.as_view({"post": "transfer"}),
        name="transaction-transfer"
    ),
]
