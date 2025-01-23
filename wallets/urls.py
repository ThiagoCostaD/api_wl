from django.urls import path

from .views import TransactionViewSet, UserViewSet, WalletViewSet

urlpatterns = [
    path(
        'transactions/',
        TransactionViewSet.as_view(
            {'get': 'list', 'post': 'create'}
        )
    ),
    path(
        'transactions/<int:pk>/',
        TransactionViewSet.as_view(
            {'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}
        )
    ),
    path(
        'users/',
        UserViewSet.as_view(
            {'get': 'list', 'post': 'create'}
        )
    ),
    path(
        'user/<int:pk>/',
        UserViewSet.as_view(
            {'get': 'retrieve'}
        )
    ),
    path(
        'wallets<int:pk>/',
        WalletViewSet.as_view(
            {'get': 'list', 'post': 'create'}
        )
    ),
]
