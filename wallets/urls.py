from django.urls import path

from .views import TransactionViewSet, UserViewSet, WalletViewSet

urlpatterns = [
    # Endpoints para transações
    path(
        "transactions/",
        TransactionViewSet.as_view({"get": "list", "post": "create"}),
        name="transaction-list-create"
    ),
    path(
        "transactions/<int:pk>/",
        TransactionViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="transaction-detail"
    ),

    # Endpoints para usuários
    path(
        "users/",
        UserViewSet.as_view({"get": "list", "post": "create"}),
        name="user-list-create"
    ),
    path(
        "users/<int:pk>/",
        UserViewSet.as_view({"get": "retrieve"}),
        name="user-detail"
    ),

    # Endpoints para carteiras
    path(
        "wallets/",
        WalletViewSet.as_view({"get": "list", "post": "create"}),
        name="wallet-list-create"
    ),
    path(
        "wallets/<int:pk>/",
        WalletViewSet.as_view({"get": "retrieve", "put": "update", "delete": "destroy"}),
        name="wallet-detail"
    ),
]
