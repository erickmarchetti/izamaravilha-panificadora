from django.db import IntegrityError
from django.test import TransactionTestCase

from enderecos.models import Endereco
from contas.models import Conta

from utils.mocks import (
    conta_cliente_mockada,
    conta_adm_mockada,
    conta_funcionario_mockada,
    endereco_mockado,
)


class EnderecosRelacionamentosTest(TransactionTestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.conta_cliente = Conta.objects.create_user(**conta_cliente_mockada)
        cls.conta_funcionario = Conta.objects.create_user(**conta_adm_mockada)
        cls.conta_adm = Conta.objects.create_user(**conta_funcionario_mockada)
        cls.endereco_cliente = Endereco.objects.create(
            **endereco_mockado, conta=cls.conta_cliente
        )
        cls.endereco_funcionario = Endereco.objects.create(
            **endereco_mockado, conta=cls.conta_funcionario
        )
        cls.endereco_adm = Endereco.objects.create(
            **endereco_mockado, conta=cls.conta_adm
        )

    def test_relacionamento_de_endereco_para_conta(self):
        self.setUpTestData()

        self.assertEqual(self.endereco_cliente.conta, self.conta_cliente)
        self.assertEqual(self.endereco_funcionario.conta, self.conta_funcionario)
        self.assertEqual(self.endereco_adm.conta, self.conta_adm)

        with self.assertRaises(IntegrityError):
            Conta.objects.create_user(**conta_cliente_mockada)

        with self.assertRaises(IntegrityError):
            Conta.objects.create_user(**conta_funcionario_mockada)

        with self.assertRaises(IntegrityError):
            Conta.objects.create_user(**conta_adm_mockada)

        conta_cliente_mockada.pop("username")
        conta_cliente_mockada.pop("cpf")

        conta_funcionario_mockada.pop("username")
        conta_funcionario_mockada.pop("cpf")

        conta_adm_mockada.pop("username")
        conta_adm_mockada.pop("cpf")

        nova_conta_cliente = Conta.objects.create_user(
            **conta_cliente_mockada, username="fidel", cpf="12345678900"
        )

        nova_conta_funcionario = Conta.objects.create_user(
            **conta_funcionario_mockada, username="bruno", cpf="00100200355"
        )

        nova_conta_adm = Conta.objects.create_user(
            **conta_adm_mockada, username="hitalo", cpf="78945612300"
        )

        self.endereco_cliente.conta = nova_conta_cliente
        self.endereco_funcionario.conta = nova_conta_funcionario
        self.endereco_adm.conta = nova_conta_adm

        self.endereco_cliente.save()
        self.endereco_funcionario.save()
        self.endereco_adm.save()

        self.assertEqual(self.endereco_cliente.conta, nova_conta_cliente)
        self.assertEqual(self.endereco_funcionario.conta, nova_conta_funcionario)
        self.assertEqual(self.endereco_adm.conta, nova_conta_adm)

    def test_relacionamento_de_conta_para_endereco(self):
        self.setUpTestData()

        # lista_de_enderecos = Conta.objects.count()

        # self.assertEqual(Endereco.objects.count(), 1)
        # self.assertEqual(self.conta_funcionario.endereco.count(), 1)
        # self.assertEqual(self.conta_adm.endereco.count(), 1)

        # self.assertEqual(self.conta_cliente.endereco.first(), self.endereco_cliente)
        # self.assertEqual(
        #     self.conta_funcionario.endereco.first(), self.endereco_funcionario
        # )
        # self.assertEqual(self.conta_adm.endereco.first(), self.endereco_adm)
