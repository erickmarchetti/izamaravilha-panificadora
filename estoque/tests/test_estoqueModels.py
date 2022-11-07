from django.test import TestCase
from estoque.models import Estoque
from produtos.models import Produto
from django.db.models.fields import UUIDField, IntegerField, DateTimeField
import uuid


class ModelEstoqueTest(TestCase):
    def test_atributos_model(self):
        id = Estoque._meta.get_field("id")
        quantidade = Estoque._meta.get_field("quantidade")
        atualizado_em = Estoque._meta.get_field("atualizado_em")
        produto = Estoque._meta.get_field("produto")

        self.assertIs(id.get_internal_type(), UUIDField().get_internal_type())
        self.assertEqual(id.primary_key, True)
        self.assertEqual(id.default, uuid.uuid4)
        self.assertEqual(id.editable, False)

        self.assertEqual(
            quantidade.get_internal_type(), IntegerField().get_internal_type()
        )
        self.assertEqual(
            atualizado_em.get_internal_type(), DateTimeField().get_internal_type()
        )
        self.assertEqual(produto.related_model, Produto)
