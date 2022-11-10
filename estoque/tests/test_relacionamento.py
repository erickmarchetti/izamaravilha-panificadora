from rest_framework.test import APITestCase
from django.db.utils import IntegrityError
from estoque.models import Estoque
from produtos.models import Produto
from categorias.models import Categoria
from utils.mocks import produto_mockado, categoria_mockada


class RelacionamentoEstoqueTest(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.categoria_create = Categoria.objects.create(**categoria_mockada)
        cls.produto_create = Produto.objects.create(
            **produto_mockado, categoria=cls.categoria_create
        )
        cls.estoque_create = Estoque.objects.create(
            quantidade=5, produto=cls.produto_create
        )

    def test_relacionamento_estoque_e_produto(self):
        """Verifica se o produto está relacionado com o o estoque."""
        self.assertEqual(self.produto_create, self.estoque_create.produto)

        """Verifca erro de integridade"""
        with self.assertRaises(IntegrityError):
            Estoque.objects.create(quantidade=5, produto=self.produto_create)
