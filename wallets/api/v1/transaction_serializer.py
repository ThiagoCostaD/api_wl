from rest_framework import serializers

from wallets.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):

    sender_username = serializers.CharField(source="sender.account.username", read_only=True)
    receiver_username = serializers.CharField(source="receiver.account.username", read_only=True)

    class Meta:
        model = Transaction
        fields = ["id", "sender", "sender_username", "receiver",
                  "receiver_username", "timestamp", "amount"]
        extra_kwargs = {
            "sender": {"read_only": True},
            "receiver": {"read_only": True},
            "timestamp": {"read_only": True}
        }
