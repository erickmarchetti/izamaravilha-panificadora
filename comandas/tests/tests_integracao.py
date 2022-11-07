import ipdb

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from comandas.models import Comanda
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

        self.client.post("/api/usuario/", data=usuario_comum, format="json")
        self.token_comum = self.client.post(
            "/api/login/", data=usuario_comum_login
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_adm)

        self.client.post("/api/funcionario/", data=usuario_funcionario, format="json")
        self.token_funcionario = self.client.post(
            "/api/login/", data=usuario_funcionario_login
        ).json()["token"]

        self.produto_1 = Produto.objects.create(
            **produto_mockado, categoria=Categoria.objects.create(**categoria_mockada)
        )

    def test_tentando_criar_uma_comanda(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)
        valores = {
            "produto_id": self.produto_1.id,
            "quantidade": 2,
        }
        response = self.client.post("/api/comanda/", data=valores)
        expected_status = status.HTTP_201_CREATED

        self.assertEqual(expected_status, response.status_code)
        self.assertEqual(Comanda.objects.count(), 1)
        self.assertIn("id", response.data)
        self.assertIn("status", response.data)
        self.assertIn("data_criacao", response.data)
        self.assertIn("conta", response.data)
        self.assertIn("produtos", response.data)

    def test_permite_remocao_de_um_produto_em_uma_comanda(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)
        valores = {
            "produto_id": self.produto_1.id,
            "quantidade": 2,
        }
        response_produto = self.client.post("/api/comanda/", data=valores)
        response_comanda = self.client.delete(
            f'/api/comanda/{response_produto.data["id"]}/produto/{response_produto.data["produtos"][0]["id"]}/'
        )
        expected_status = status.HTTP_204_NO_CONTENT

        self.assertEqual(expected_status, response_comanda.status_code)
        self.assertEqual(Comanda.objects.count(), 1)

    def test_permite_alterar_quantidade_de_produtos_dentro_da_comanda(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)
        valores = {
            "produto_id": self.produto_1.id,
            "quantidade": 2,
        }
        response_produto = self.client.post("/api/comanda/", data=valores)
        quantidade = {"quantidade": 9}
        response_comanda = self.client.patch(
            f'/api/comanda/{response_produto.data["id"]}/produto/{response_produto.data["produtos"][0]["id"]}/',
            data=quantidade,
        )
        expected_status = status.HTTP_200_OK

        self.assertEqual(expected_status, response_comanda.status_code)
        self.assertEqual(Comanda.objects.count(), 1)
        self.assertIn("id", response_produto.data)
        self.assertIn("status", response_produto.data)
        self.assertIn("data_criacao", response_produto.data)
        self.assertIn("conta", response_produto.data)
        self.assertIn("produtos", response_produto.data)

    def test_permite_alterar_o_status_da_comanda(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)
        valores = {
            "produto_id": self.produto_1.id,
            "quantidade": 2,
        }
        response_produto = self.client.post("/api/comanda/", data=valores)
        alteracao = {"status": "fechada"}
        response_comanda = self.client.patch(
            f'/api/comanda/{response_produto.data["id"]}/status/', data=alteracao
        )
        expected_status = status.HTTP_200_OK

        self.assertEqual(expected_status, response_comanda.status_code)
        self.assertEqual(Comanda.objects.count(), 1)
        self.assertIn("status", response_comanda.data)
        self.assertIn("id", response_comanda.data)
        self.assertIn("status", response_comanda.data)
        self.assertEqual(response_comanda.data["status"], "fechada")
        self.assertIn("data_criacao", response_comanda.data)
        self.assertIn("conta", response_comanda.data)
        self.assertNotIn("produtos", response_comanda.data)

    def test_permite_listagem_de_todas_as_comandas_finalizadas(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)
        valores = {
            "produto_id": self.produto_1.id,
            "quantidade": 2,
        }
        response_produto = self.client.post("/api/comanda/", data=valores)
        alteracao = {"status": "fechada"}
        self.client.patch(
            f'/api/comanda/{response_produto.data["id"]}/status/', data=alteracao
        )
        response_comanda = self.client.get("/api/comanda/finalizadas/")
        expected_status = status.HTTP_200_OK

        self.assertEqual(expected_status, response_comanda.status_code)
        self.assertEqual(Comanda.objects.count(), 1)
        self.assertEqual(response_comanda.data[0]["status"], "fechada")

    def test_permite_listagem_de_todas_as_comandas_abertas(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)
        valores1 = {
            "produto_id": self.produto_1.id,
            "quantidade": 2,
        }
        valores2 = {
            "produto_id": self.produto_1.id,
            "quantidade": 2,
        }
        self.client.post("/api/comanda/", data=valores1)
        self.client.post("/api/comanda/", data=valores2)
        response_comanda = self.client.get("/api/comanda/abertas/")
        expected_status = status.HTTP_200_OK

        self.assertEqual(expected_status, response_comanda.status_code)
        self.assertEqual(Comanda.objects.count(), 2)

    def test_permite_listagem_de_uma_comanda_específica(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)
        valores1 = {
            "produto_id": self.produto_1.id,
            "quantidade": 2,
        }
        valores2 = {
            "produto_id": self.produto_1.id,
            "quantidade": 2,
        }
        produto = self.client.post("/api/comanda/", data=valores1)
        self.client.post("/api/comanda/", data=valores2)
        response_comanda = self.client.get(f'/api/comanda/{produto["id"]}/')
        expected_status = status.HTTP_200_OK

        self.assertEqual(expected_status, response_comanda.status_code)
        self.assertEqual(Comanda.objects.count(), 1)
