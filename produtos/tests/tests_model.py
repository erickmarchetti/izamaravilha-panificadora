from django.test import TestCase
from categorias.models import Categoria
from produtos.models import Produto
from contas.models import Conta
import uuid
from rest_framework.test import APITestCase
from rest_framework.views import status
from rest_framework.authtoken.models import Token
import ipdb

# Create your tests here.


class TesteModelsProdutos(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.boloChocolate_data = {
            "id": str(uuid.uuid4()),
            "preco": 10.50,
            "nome": "Bolo de Chocolate",
            "imagem": "https://cakeshouse.com.br/wp-content/uploads/2020/08/Bolo-de-chocolate-scaled.jpg",
            "descricao": "Um delicioso bolo de chocolate com muurangos.",
        }
        cls.categoria = Categoria.objects.create(nome="teste categoria")
        cls.boloChocolate = Produto.objects.create(
            **cls.boloChocolate_data, categoria=cls.categoria
        )

        cls.leiteCaixinha_data = {
            "id": str(uuid.uuid4()),
            "preco": 4.50,
            "nome": "Leite de caixinha",
            "imagem": "https://www.ninho.com.br/sites/default/files/styles/image_webp/public/2022-10/ninho-forti-uht-integral-1l-sombra.png.webp?itok=W_N115tb",
        }
        cls.categoria = Categoria.objects.create(nome="teste categoria2")
        cls.leiteCaixinha = Produto.objects.create(
            **cls.leiteCaixinha_data, categoria=cls.categoria
        )

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
    @classmethod
    def setUpTestData(cls) -> None:
        cls.produto_correto_data = {
            "id": str(uuid.uuid4()),
            "preco": 5.00,
            "nome": "Coxinha de Frango",
            # "categoria": {"nome": "graos"},
            "imagem": "https://www.fomitasgourmet.com.br/arquivos/LoginID_321/Blog/receita-tradicional-de-coxinha-1729.jpg",
            "descricao": "Coxinha de frango com catupiry.",
        }
        # cls.categoria = Categoria.objects.create(nome="teste categoria 4")
        cls.categoria2 = Categoria.objects.create(nome="graos")

        cls.produto1 = Produto.objects.create(
            **cls.produto_correto_data, categoria=cls.categoria2
        )

        cls.cliente_comum = {
            "id": str(uuid.uuid4()),
            "username": "first",
            "first_name": "teste",
            "last_name": "cliente",
            "is_employee": False,
            "data_nascimento": "2001-01-01",
            "cpf": "144.111.444-89",
            "pontos_de_fidelidade": 2,
            "telefone": "3599996666",
        }
        cls.cliente = Conta.objects.create_user(**cls.cliente_comum)

        cls.adm = {
            "id": str(uuid.uuid4()),
            "first_name": "teste",
            "last_name": "cliente",
            "is_staff": True,
            "is_superuser": True,
            "data_nascimento": "2001-01-01",
            "cpf": "11111111116",
            "telefone": "3599996666",
        }
        cls.extra_fields = {"is_staff": True, "is_superuser": True}

        cls.conta_admin = Conta.objects.create_user(
            username="TesteADM",
            email=None,
            password="1234",
            **cls.adm,
        )

        cls.vendedor = {
            "id": str(uuid.uuid4()),
            "username": "teste",
            "first_name": "teste",
            "last_name": "cliente",
            "password": "1234",
            "is_employee": True,
            "data_nascimento": "2001-01-01",
            "cpf": "11111111119",
            "pontos_de_fidelidade": 2,
            "telefone": "3599996666",
        }

    def test_criacao_produto(self):
        produto_teste = {
            "categoria": Categoria.objects.create(**{"nome": "socorro4"}),
            "preco": 10,
            "nome": "teste 2",
            "imagem": "socorro 2",
        }

        criar_vendedor = Conta.objects.create_user(**self.vendedor)
        # cls.produto1 = Produto.objects.create(
        #     **cls.produto_correto_data, categoria=cls.categoria
        # )
        tokenVendedor = Token.objects.create(user=criar_vendedor)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenVendedor.key)
        # self.produto_correto_data["categoria"] = self.categoria2
        response = self.client.post("/api/produtos/", data=produto_teste)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_de_usuario_sem_autorizacao(self):
        produto_incorreto_data = {
            "id": str(uuid.uuid4()),
            "preco": 5.00,
            "descricao": "Coxinha de frango com catupiry.",
        }
        response = self.client.post("/api/produtos/", data=produto_incorreto_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cliente_listando_produtos(self):
        response = self.client.get("/api/produtos/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_cliente_crianod_produto(self):
        tokenComum = Token.objects.create(user=self.cliente)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + tokenComum.key)
        response = self.client.post("/api/produtos/", data=self.produto_correto_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
