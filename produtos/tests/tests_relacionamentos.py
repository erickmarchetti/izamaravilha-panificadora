from django.test import TestCase
from categorias.models import Categoria
from produtos.models import Produto
import uuid


class Teste_relacionamnetos(TestCase):
    @classmethod
    def setUpTestData(cls):
        ...

    def test_relacao_produtos_categoria(self):
        bolo = {
            "preco": 25.00,
            "nome": "Bolo de Chocolate",
            "imagem": "https://www.oetker.com.br/Recipe/Recipes/oetker.com.br/br-pt/baking/image-thumb__40008__RecipeDetail/bolo-de-aniversario-de-chocolate.jpg",
            "descricao": "Bolo de chocolate com Brigadeiro.",
        }
        categoria = Categoria.objects.create(nome="Bolo-Doce")

        categoria_inexistente = Categoria.objects.create(nome="Nao-tem")

        produto_criado = Produto.objects.create(**bolo, categoria=categoria)

        self.assertEqual(produto_criado.categoria, categoria)

        produto_criado.categoria = categoria_inexistente

        self.assertEqual(produto_criado.categoria, categoria_inexistente)

    def test_relacao_categoria_produtos(self):
        categoria = Categoria.objects.create(nome="Bolo-Doce")
        self.assertEqual(categoria.produtos.count(), 0)

        bolo = {
            "preco": 25.00,
            "nome": "Bolo de Chocolate",
            "imagem": "https://www.oetker.com.br/Recipe/Recipes/oetker.com.br/br-pt/baking/image-thumb__40008__RecipeDetail/bolo-de-aniversario-de-chocolate.jpg",
            "descricao": "Bolo de chocolate com Brigadeiro.",
        }

        for _ in range(50):
            Produto.objects.create(**bolo, categoria=categoria)

        self.assertEqual(categoria.produtos.count(), 50)

        self.assertNotEqual(categoria.produtos.count(), 48)
