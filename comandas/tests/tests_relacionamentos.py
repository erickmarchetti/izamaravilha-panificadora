from django.test import TestCase

from comandas.models import Comanda
from contas.models import Conta

from utils.mocks import (
    conta_cliente_mockada,
    conta_adm_mockada,
    conta_funcionario_mockada,
)


class ComandaRelacionamentosTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.cliente = Conta.objects.create_user(**conta_cliente_mockada)
        cls.comanda = Comanda.objects.create(conta=cls.cliente)

    def test_relacionamento_de_comanda_para_conta(self):
        self.assertEqual(self.comanda.conta, self.cliente)

        novo_cliente = Conta.objects.create_user(
            **conta_cliente_mockada, cpf="36593511007"
        )

        self.comanda.conta = novo_cliente
        self.comanda.save()

        self.assertEqual(self.comanda.conta, novo_cliente)

    def test_relacionamento_de_conta_para_comanda(self):
        self.assertEqual(self.cliente.comandas.count(), 1)
        self.assertEqual(self.cliente.comandas.first(), self.comanda)

        for _ in range(10):
            Comanda.objects.create(conta=self.cliente)

        self.assertEqual(self.cliente.comandas.count(), 11)
