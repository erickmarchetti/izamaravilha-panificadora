from django.db import IntegrityError
from django.test import TestCase

from enderecos.models import Endereco
from contas.models import Conta

from utils.mocks import (
    conta_cliente_mockada,
    endereco_mockado,
)


class EnderecosRelacionamentosTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.conta_cliente = Conta.objects.create_user(**conta_cliente_mockada)

        cls.endereco_cliente = Endereco.objects.create(
            **endereco_mockado, conta=cls.conta_cliente
        )

    def test_relacionamento_de_endereco_para_conta(self):

        self.assertEqual(self.endereco_cliente.conta, self.conta_cliente)

        with self.assertRaises(IntegrityError):
            Endereco.objects.create(**endereco_mockado, conta=self.conta_cliente)
