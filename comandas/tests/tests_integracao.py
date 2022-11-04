from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from utils.mocks import usuario_comum, usuario_funcionario, usuario_superuser
from rest_framework import status

from categorias.models import Categoria
from contas.models import Conta
from produtos.models import Produto


class TesteIntegracaoComanda(APITestCase):
    def setUp(self) -> None:

        self.superuser = Conta.objects.create_superuser(**usuario_superuser)

        self.funcionario = Conta.objects.create_user(**usuario_funcionario)

        self.comum = Conta.objects.create_user(**usuario_comum)

        produto_1_valores = {
            "preco": 9.00,
            "nome": "Requeijão Cremoso",
            "categoria": Categoria.objects.create(**{"name": "laticínios"}),
            "imagem": "requeijaocremoso.jpg",
            "descricao": "Saboroso e ótimo para acompanhar com pães fresquinhos",
        }
        """
        PRODUTO TEM QUE SER CRIADO, JUNTO COM O PRODUTO VEM A CATEGORIA.
        """
        self.produto_1 = Produto.objects.create(**produto_1_valores)

    def test_tentando_criar_uma_comanda(self):
        token = Token.objects.create(self.comum)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        valores = {
            "produto_id": self.produto_1,
            "quantidade": 2,
        }
        response = self.client.post("/api/comanda/", data=valores)
        expected_status = status.HTTP_201_CREATED

        self.assertEqual(expected_status, response.status_code)
        # self.assertIn(response.data, "id")
        # self.assertIn(response.data, "status")
        # self.assertIn(response.data, "data_criacao")
        # self.assertIn(response.data, "conta")
        # self.assertIn(response.data, "produtos")
