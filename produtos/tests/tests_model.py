from django.test import TestCase
from produtos.models import Produto
from contas.models import Conta
import uuid
from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token

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

    def test_campos_preenchidos_corretamente(self):
        self.assertEqual(self.salgado.preco, self.salgado_data["preco"])
        self.assertEqual(self.salgado.nome, self.salgado_data["nome"])
        self.assertEqual(self.salgado.imagem, self.salgado_data["imagem"])
        self.assertEqual(self.salgado.descricao, self.salgado_data["descricao"])


class TesteViewProdutos(APITestCase):
    def setUp(self) -> None:
        produto_correto_data = {
            "id": str(uuid.uuid4()),
            # "categoria_id": "",
            "preco": 5.00,
            "nome": "Coxinha de Frango",
            "imagem": "https://www.fomitasgourmet.com.br/arquivos/LoginID_321/Blog/receita-tradicional-de-coxinha-1729.jpg",
            "descricao": "Coxinha de frango com catupiry.",
        }
        self.produto1 = Produto.objects.create(**produto_correto_data)

        produto_incorreto_data = {
            "id": str(uuid.uuid4()),
            # "categoria_id": "",
            "preco": 5.00,
            "descricao": "Coxinha de frango com catupiry.",
        }
        self.produto1 = Produto.objects.create(**produto_incorreto_data)

        cliente_comum = {
            "id": str(uuid.uuid4()),
            "username": "first",
            "first_name": "teste",
            "last_name": "cliente",
            "e_vendedor": False,
            "data_nascimento": "2001-01-01",
            "cpf": "144.111.444-89",
            "pontos_de_fidelidade": 2,
            "telefone": "3599996666",
        }
        self.cliente = Conta.objects.create(**cliente_comum)

    def test_criacao_produto(self):
        produto_correto_data = {
            "id": str(uuid.uuid4()),
            # "categoria_id": "",
            "preco": 5.00,
            "nome": "Coxinha de Frango",
            "imagem": "https://www.fomitasgourmet.com.br/arquivos/LoginID_321/Blog/receita-tradicional-de-coxinha-1729.jpg",
            "descricao": "Coxinha de frango com catupiry.",
        }
        response = self.client.post("/api/produtos/", data=produto_correto_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_campos_preenchidos_incorretamente(self):
        produto_incorreto_data = {
            "id": str(uuid.uuid4()),
            "preco": 5.00,
            "descricao": "Coxinha de frango com catupiry.",
        }
        response = self.client.post("/api/produtos/", data=produto_incorreto_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_cliente_listando_produtos(self):
        response = self.client.get("/api/produtos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cliente_crianod_produto(self):
        produto_correto_data = {
            "id": str(uuid.uuid4()),
            # "categoria_id": "",
            "preco": 5.00,
            "nome": "Coxinha de Frango",
            "imagem": "https://www.fomitasgourmet.com.br/arquivos/LoginID_321/Blog/receita-tradicional-de-coxinha-1729.jpg",
            "descricao": "Coxinha de frango com catupiry.",
        }
        tokenComum = Token.objects.create(user=self.cliente)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenComum.key)
        response = self.client.post("/api/produtos/", data=produto_correto_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
