from rest_framework.test import APITestCase
from rest_framework import status


from utils.mocks import (
    conta_cliente_mockada,
    conta_funcionario_mockada,
    conta_adm_mockada,
    usuario_adm_login,
    usuario_comum_login,
    usuario_funcionario_login,
    categoria_mockada,
    endereco_mockado,
    produto_mockado,
    coxinha_mockada,
)


from categorias.models import Categoria
from contas.models import Conta
from produtos.models import Produto
from enderecos.models import Endereco
from estoque.models import Estoque


class TesteIntegracaoComanda(APITestCase):
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

        categoria = Categoria.objects.create(**categoria_mockada)
        self.produto_1 = Produto.objects.create(**produto_mockado, categoria=categoria)
        self.estoque_1 = Estoque.objects.create(quantidade=300, produto=self.produto_1)

    def test_permite_alterar_quantidade_de_produtos_no_estoque(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        quantidade = {"quantidade": 30}
        response_estoque = self.client.patch(
            f"/api/estoque/{self.produto_1.id}/", data=quantidade
        )
        expected_status = status.HTTP_200_OK

        self.assertEqual(expected_status, response_estoque.status_code)
        self.assertEqual(30, response_estoque.json()["estoque"]["quantidade"])

    def test_nao_permite_usuario_comum_alterar_quantidade_de_produtos_no_estoque(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)

        quantidade = {"quantidade": 30}
        response_estoque = self.client.patch(
            f"/api/estoque/{self.estoque_1.id}/",
            data=quantidade,
        )
        expected_status = status.HTTP_403_FORBIDDEN

        self.assertEqual(expected_status, response_estoque.status_code)

    def test_permite_listagem_de_todos_os_produtos_sem_estoque(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_funcionario)

        self.client.post(
            "/api/produtos/",
            data={**coxinha_mockada, "estoque": {"quantidade": 0}},
            format="json",
        )

        response_estoque_1 = self.client.get("/api/estoque/")
        response_estoque_2 = self.client.get("/api/estoque/?quantidade=300")
        expected_status = status.HTTP_200_OK

        self.assertEqual(expected_status, response_estoque_1.status_code)
        self.assertEqual(expected_status, response_estoque_2.status_code)
        self.assertEqual(len(response_estoque_1.json()), 1)
        self.assertEqual(len(response_estoque_2.json()), 2)

    def test_nao_permite_usuario_comum_listar_todos_os_produtos_sem_estoque(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)

        response_estoque_1 = self.client.get("/api/estoque/")
        expected_status = status.HTTP_403_FORBIDDEN

        self.assertEqual(expected_status, response_estoque_1.status_code)
