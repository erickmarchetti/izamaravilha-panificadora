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

        self.client.post("/api/usuario/", data=usuario_comum, format="json")
        self.token_comum = self.client.post(
            "/api/login/", data=usuario_comum_login
        ).json()["token"]

        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_adm)

        self.client.post("/api/funcionario/", data=usuario_funcionario, format="json")
        self.token_funcionario = self.client.post(
            "/api/login/", data=usuario_funcionario_login
        ).json()["token"]

        print(self.token_adm, self.token_comum, self.token_funcionario)

        self.produto_1 = Produto.objects.create(
            **produto_mockado, categoria=Categoria.objects.create(**categoria_mockada)
        )

    def test_tentando_criar_uma_comanda(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_comum)
        valores = {
            "produto_id": self.produto_1,
            "quantidade": 2,
        }
        response = self.client.post("/api/comanda/", data=valores)
        expected_status = status.HTTP_201_CREATED

        self.assertEqual(expected_status, response.status_code)
        self.assertIn(response.data, "id")
        self.assertIn(response.data, "status")
        self.assertIn(response.data, "data_criacao")
        self.assertIn(response.data, "conta")
        self.assertIn(response.data, "produtos")
