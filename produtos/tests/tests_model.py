from django.test import TestCase
from categorias.models import Categoria
from produtos.models import Produto
import uuid


class TesteModelsProdutos(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.salgado_data = {
            "id": str(uuid.uuid4()),
            "preco": 5.00,
            "nome": "Coxinha de Frango",
            "imagem": "https://www.fomitasgourmet.com.br/arquivos/LoginID_321/Blog/receita-tradicional-de-coxinha-1729.jpg",
            "descricao": "Coxinha de frango com catupiry.",
        }
        cls.categoria = Categoria.objects.create(nome="teste categoria3")
        cls.salgado = Produto.objects.create(
            **cls.salgado_data, categoria=cls.categoria
        )

    def test_max_length(self):
        max_length = Produto._meta.get_field("nome").max_length
        self.assertEqual(max_length, 100)

    def test_campo_nulo(self):
        nullable = Produto._meta.get_field("descricao").null
        self.assertTrue(nullable)

    def test_campos_preenchidos_corretamente(self):
        self.assertEqual(self.salgado.preco, self.salgado_data["preco"])
        self.assertEqual(self.salgado.nome, self.salgado_data["nome"])
        self.assertEqual(self.salgado.imagem, self.salgado_data["imagem"])
        self.assertEqual(self.salgado.descricao, self.salgado_data["descricao"])

   
