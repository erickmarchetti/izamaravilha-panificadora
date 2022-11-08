from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from utils.mocks import (
    conta_adm_mockada,
    conta_cliente_mockada,
    conta_funcionario_mockada,
    usuario_adm_login,
    usuario_comum_login,
    usuario_funcionario_login,
    endereco_mockado,
    coxinha_mockada,
)
from rest_framework import status

from categorias.models import Categoria
from enderecos.models import Endereco
from contas.models import Conta
from produtos.models import Produto


class TesteIntegracaProdutos(APITestCase):
    def setUp(self) -> None:

        Conta.objects.create_superuser(**conta_adm_mockada)
        self.token_adm = self.client.post("/api/login/", data=usuario_adm_login).json()[
            "token"
        ]

        cliente = Conta.objects.create_user(**conta_cliente_mockada)
        Endereco.objects.create(**endereco_mockado, conta=cliente)
        self.token_comum = self.client.post(
            "/api/login/", data=usuario_comum_login
        ).json()["token"]

        funcionario = Conta.objects.create_user(**conta_funcionario_mockada)
        Endereco.objects.create(**endereco_mockado, conta=funcionario)
        self.token_funcionario = self.client.post(
            "/api/login/", data=usuario_funcionario_login
        ).json()["token"]

    def test_tentando_criar_um_produto_como_funcionario(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        response = self.client.post(
            "/api/produtos/", data=coxinha_mockada, format="json"
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
            "/api/produtos/", data=coxinha_mockada, format="json"
        )
        expected_status = status.HTTP_403_FORBIDDEN

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

        criacao_produto = self.client.post(
            "/api/produtos/", data=coxinha_mockada, format="json"
        )
        response_produto = self.client.delete(
            f'/api/produtos/{criacao_produto.data["id"]}/'
        )
        expected_status = status.HTTP_204_NO_CONTENT

        self.assertEqual(expected_status, response_produto.status_code)
        self.assertEqual(Produto.objects.count(), 0)

    def test_nao_permite_apagar_um_produto_como_usuario_comum(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        criacao_produto = self.client.post(
            "/api/produtos/", data=coxinha_mockada, format="json"
        )

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)

        response_produto = self.client.delete(
            f'/api/produtos/{criacao_produto.data["id"]}/'
        )
        expected_status = status.HTTP_403_FORBIDDEN

        self.assertEqual(expected_status, response_produto.status_code)
        self.assertEqual(Produto.objects.count(), 1)

    def test_permite_alterar_dados_do_produto(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        response_produto = self.client.post(
            "/api/produtos/", data=coxinha_mockada, format="json"
        )
        alteracoes = {"preco": 9.00, "nome": "Maçã do Amor"}
        response_patch = self.client.patch(
            f'/api/produtos/{response_produto.data["id"]}/',
            data=alteracoes,
            format="json",
        )
        expected_status = status.HTTP_200_OK

        self.assertEqual(expected_status, response_patch.status_code)
        self.assertEqual(Produto.objects.count(), 1)
        self.assertIn("id", response_patch.data)
        self.assertIn("categoria", response_patch.data)
        self.assertIn("preco", response_patch.data)
        self.assertIn("nome", response_patch.data)
        self.assertIn("imagem", response_patch.data)
        self.assertIn("descricao", response_patch.data)

    def test_listar_todos_os_produtos(self):
        response_get = self.client.get("/api/produtos/")

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_ler_um_produto(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        response_produto = self.client.post(
            "/api/produtos/", data=coxinha_mockada, format="json"
        )

        self.client.credentials()
        response_get = self.client.get(
            f"/api/produtos/{response_produto.json()['id']}/"
        )

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_listar_todos_os_produtos_por_categoria(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        response_produto = self.client.post(
            "/api/produtos/", data=coxinha_mockada, format="json"
        )

        self.client.credentials()
        response_get = self.client.get(
            f"/api/produtos/categoria/{response_produto.json()['categoria']['id']}/"
        )

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)

    def test_listar_todos_os_produtos(self):
        response_get = self.client.get("/api/produtos/recentes/")

        self.assertEqual(response_get.status_code, status.HTTP_200_OK)
