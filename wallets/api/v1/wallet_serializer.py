from rest_framework import serializers

from wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ["id", "account", "balance"]
        extra_kwargs = {
            "account": {"read_only": True}
        }


class WalletBalanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Wallet
        fields = ["id", "balance"]
