from django.test import TestCase

from comandas.models import Comanda, Comanda_Produto
from contas.models import Conta
from produtos.models import Produto
from categorias.models import Categoria

from utils.mocks import conta_cliente_mockada, produto_mockado, categoria_mockada


class ComandaRelacionamentosTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.cliente = Conta.objects.create_user(**conta_cliente_mockada)
        cls.comanda = Comanda.objects.create(conta=cls.cliente)

    def test_relacionamento_de_comanda_para_conta(self):
        self.assertEqual(self.comanda.conta, self.cliente)

        novo_cliente = Conta.objects.create_user(
            **{
                **conta_cliente_mockada,
                "cpf": "36593511007",
                "username": "erick 2",
                "email": "user427@gmail.com",
            }
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


class Comanda_ProdutoRelacionamentosTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.cliente = Conta.objects.create_user(**conta_cliente_mockada)
        cls.comanda = Comanda.objects.create(conta=cls.cliente)
        cls.categoria = Categoria.objects.create(**categoria_mockada)
        cls.produto = Produto.objects.create(**produto_mockado, categoria=cls.categoria)
        cls.instancia_comanda_produto = Comanda_Produto.objects.create(
            produto=cls.produto, comanda=cls.comanda, quantidade=1
        )

    def test_relacionamento_de_comanda_produto_para_comanda(self):
        self.assertEqual(self.instancia_comanda_produto.comanda, self.comanda)

        nova_comanda = Comanda.objects.create(conta=self.cliente)
        self.instancia_comanda_produto.comanda = nova_comanda
        self.instancia_comanda_produto.save()

        self.assertEqual(self.instancia_comanda_produto.comanda, nova_comanda)
        self.assertNotEqual(self.instancia_comanda_produto.comanda, self.comanda)

    def test_relacionamento_de_comanda_produto_para_produto(self):
        self.assertEqual(self.instancia_comanda_produto.produto, self.produto)

        novo_produto = Produto.objects.create(
            **produto_mockado, categoria=self.categoria
        )
        self.instancia_comanda_produto.produto = novo_produto
        self.instancia_comanda_produto.save()

        self.assertEqual(self.instancia_comanda_produto.produto, novo_produto)
        self.assertNotEqual(self.instancia_comanda_produto.produto, self.produto)
