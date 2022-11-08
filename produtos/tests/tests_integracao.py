from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from utils.mocks import (
    usuario_comum,
    usuario_funcionario,
    conta_adm_mockada,
    usuario_adm_login,
    usuario_comum_login,
    usuario_funcionario_login,
    produto_mockado,
    categoria_mockada,
)
from rest_framework import status

from categorias.models import Categoria
from contas.models import Conta
from produtos.models import Produto


class TesteIntegracaoComanda(APITestCase):
    def setUp(self) -> None:

        Conta.objects.create_superuser(**conta_adm_mockada)
        self.token_adm = self.client.post("/api/login/", data=usuario_adm_login).json()[
            "token"
        ]

        res = self.client.post("/api/usuario/", data=usuario_comum, format="json")
        self.token_comum = self.client.post(
            "/api/login/", data=usuario_comum_login
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_adm)

        self.client.post("/api/funcionario/", data=usuario_funcionario, format="json")
        self.token_funcionario = self.client.post(
            "/api/login/", data=usuario_funcionario_login
        ).json()["token"]

        # self.produto_1 = Produto.objects.create(
        #     **produto_mockado, categoria=Categoria.objects.create(**categoria_mockada)
        # )

    def test_tentando_criar_um_produto_como_funcionario(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        response = self.client.post(
            "/api/produtos/", data=produto_mockado, format="json"
        )
        expected_status = status.HTTP_201_CREATED

        self.assertEqual(expected_status, response.status_code)
        self.assertEqual(Produto.objects.count(), 1)
        self.assertIn("id", response.data)
        self.assertIn("categoria", response.data)
        self.assertIn("preco", response.data)
        self.assertIn("nome", response.data)
        self.assertIn("imagem", response.data)
        self.assertIn("descricao", response.data)

    def test_tentando_criar_um_produto_como_usuario_comum(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)

        response = self.client.post(
            "/api/produtos/", data=produto_mockado, format="json"
        )
        expected_status = status.HTTP_401_UNAUTHORIZED

        self.assertEqual(expected_status, response.status_code)
        self.assertEqual(Produto.objects.count(), 0)
        self.assertNotIn("id", response.data)
        self.assertNotIn("categoria", response.data)
        self.assertNotIn("preco", response.data)
        self.assertNotIn("nome", response.data)
        self.assertNotIn("imagem", response.data)
        self.assertNotIn("descricao", response.data)

    def test_permite_apagar_um_produto(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        criacao_produto = self.client.post("/api/produtos/", data=produto_mockado)
        response_produto = self.client.delete(
            f'/api/produtos/{criacao_produto.data["id"]}/'
        )
        expected_status = status.HTTP_204_NO_CONTENT

        self.assertEqual(expected_status, response_produto.status_code)
        self.assertEqual(Produto.objects.count(), 0)

    def test_nao_permite_apagar_um_produto_como_usuario_comum(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        criacao_produto = self.client.post("/api/produtos/", data=produto_mockado)

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)

        response_produto = self.client.delete(
            f'/api/produtos/{criacao_produto.data["id"]}/'
        )
        expected_status = status.HTTP_401_UNAUTHORIZED

        self.assertEqual(expected_status, response_produto.status_code)
        self.assertEqual(Produto.objects.count(), 1)

    def test_permite_alterar_dados_do_produto(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        response_produto = self.client.post("/api/produtos/", data=produto_mockado)
        alteracoes = {"preco": 9.00, "nome": "Maçã do Amor"}
        response_comanda = self.client.patch(
            f'/api/produtos/{response_produto.data["id"]}/', data=alteracoes
        )
        expected_status = status.HTTP_200_OK

        self.assertEqual(expected_status, response_comanda.status_code)
        self.assertEqual(Produto.objects.count(), 1)
        self.assertIn("id", response_produto.data)
        self.assertIn("status", response_produto.data)
        self.assertIn("data_criacao", response_produto.data)
        self.assertIn("conta", response_produto.data)
        self.assertIn("produtos", response_produto.data)
