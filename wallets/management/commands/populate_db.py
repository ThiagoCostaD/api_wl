import random

from django.core.management.base import BaseCommand
from django.utils.timezone import now
from faker import Faker

from wallets.models import Transaction, User, Wallet

fake = Faker()


class Command(BaseCommand):
    help = "Popula o banco de dados com dados fictícios"

    def handle(self, *args, **kwargs):
        self.stdout.write("Criando usuários...")
        users = [User.objects.create_user(username=fake.user_name(
        ), email=fake.email(), password="password123") for _ in range(10)]

        self.stdout.write("Criando carteiras...")
        wallets = [Wallet.objects.create(account=user, balance=random.uniform(
            100, 5000)) for user in users]

        self.stdout.write("Criando transações...")
        for _ in range(30):
            sender, receiver = random.sample(wallets, 2)
            amount = random.uniform(10, sender.balance / 2)

            Transaction.objects.create(sender=sender, receiver=receiver,
                                       amount=amount, timestamp=now())

            sender.balance -= amount
            receiver.balance += amount
            sender.save()
            receiver.save()

        self.stdout.write(self.style.SUCCESS("Banco de Dados populado com sucesso!"))
