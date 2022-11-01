from django.test import TestCase
from produtos.models import Produto
import uuid

# Create your tests here.


class TesteModelsProdutos(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.boloChocolate_data = {
            "id": str(uuid.uuid4()),
            # "categoria_id": "",
            "preco": 10.50,
            "nome": "Bolo de Chocolate",
            "imagem": "https://cakeshouse.com.br/wp-content/uploads/2020/08/Bolo-de-chocolate-scaled.jpg",
            "descricao": "Um delicioso bolo de chocolate com muurangos.",
        }
        cls.boloChocolate = Produto.objects.create(**cls.boloChocolate_data)

        cls.leiteCaixinha_data = {
            "id": str(uuid.uuid4()),
            # "categoria_id": "",
            "preco": 4.50,
            "nome": "Leite de caixinha",
            "imagem": "https://www.ninho.com.br/sites/default/files/styles/image_webp/public/2022-10/ninho-forti-uht-integral-1l-sombra.png.webp?itok=W_N115tb",
        }
        cls.leiteCaixinha = Produto.objects.create(**cls.leiteCaixinha_data)

        cls.salgado_data = {
            "id": str(uuid.uuid4()),
            # "categoria_id": "",
            "preco": 5.00,
            "nome": "Coxinha de Frango",
            "imagem": "https://www.fomitasgourmet.com.br/arquivos/LoginID_321/Blog/receita-tradicional-de-coxinha-1729.jpg",
            "descricao": "Coxinha de frango com catupiry.",
        }
        cls.salgado = Produto.objects.create(**cls.salgado_data)

    def test_max_length(self):
        max_length = self.boloChocolate._meta.get_field("nome").max_length
        self.assertEqual(max_length, 100)

    def test_campo_nulo(self):
        nullable = self.leiteCaixinha._meta.get_field("descricao").null
        self.assertTrue(nullable)

    def test_campos_preenchidosCorretamente(self):
        self.assertEqual(self.salgado.preco, self.salgado_data["preco"])
        self.assertEqual(self.salgado.nome, self.salgado_data["nome"])
        self.assertEqual(self.salgado.imagem, self.salgado_data["imagem"])
        self.assertEqual(self.salgado.descricao, self.salgado_data["descricao"])
