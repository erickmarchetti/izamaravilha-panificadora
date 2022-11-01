from comandas.models import Comanda, Comanda_Produto
from contas.models import Conta

# from produtos.models import Produto

from django.db.models.fields import UUIDField
from django.test import TestCase
import uuid


class ComandaModelTest(TestCase):
    def test_se_os_atributos_da_model_estao_corretos(self):
        id = Comanda._meta.get_field("id")
        conta = Comanda._meta.get_field("conta")
        status = Comanda._meta.get_field("status")
        data_criacao: Comanda._meta.get_field("data_criacao")

        expected_choices = [
            ("aberta", "Default"),
            ("fechada", "Fechada"),
            ("em rota de entrega", "Em_rota_de_entrega"),
            ("entregue", "Entregue"),
        ]

        self.assertIs(type(id), UUIDField)
        self.assertEqual(id.primary_key, True)
        self.assertEqual(id.default, uuid.uuid4)
        self.assertEqual(id.editable, False)
        self.assertEqual(conta.related_model, Conta)
        self.assertEqual(status.default.value, "aberta")
        self.assertEqual(status.choices, expected_choices)
        self.assertEqual(data_criacao.auto_now_add, True)

    def test_se_os_atributos_da_model_nao_sao_nulaveis(self):
        conta = Comanda._meta.get_field("conta")
        status = Comanda._meta.get_field("status")
        data_criacao: Comanda._meta.get_field("data_criacao")

        self.assertEqual(conta.null, False)
        self.assertEqual(status.null, False)
        self.assertEqual(data_criacao.null, False)


class Comanda_ProdutoModelTest(TestCase):
    def test_se_os_atributos_da_model_estao_corretos(self):
        id = Comanda_Produto._meta.get_field("id")
        comanda = Comanda_Produto._meta.get_field("comanda")
        # produto = Comanda_Produto._meta.get_field("produto")

        self.assertIs(type(id), UUIDField)
        self.assertEqual(id.primary_key, True)
        self.assertEqual(id.default, uuid.uuid4)
        self.assertEqual(id.editable, False)
        self.assertEqual(comanda.related_model, Comanda)
        # self.assertEqual(produto.related_model, Produto)

    def test_se_os_atributos_da_model_nao_sao_nulaveis(self):
        comanda = Comanda_Produto._meta.get_field("comanda")
        # produto = Comanda_Produto._meta.get_field("produto")

        self.assertEqual(comanda.null, False)
        # self.assertEqual(produto.null, False)
