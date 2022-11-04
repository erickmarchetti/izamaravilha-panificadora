from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token

from contas.models import Conta
from produtos.models import Produto


class TesteIntegracaoComanda(APITestCase):
    def setUp(self) -> None:
        usuario_superuser = {
            "username": "jorge",
            "first_name": "jorge",
            "last_name": "junior",
            "telefone": "99999999999",
            "cpf": "99999999999",
            "data_nascimento": "1997-01-01",
            "password": "1234",
        }
        self.superuser = Conta.objects.create_superuser(**usuario_superuser)

        usuario_funcionario = {
            "username": "jorge",
            "password": "1234",
            "first_name": "jorge",
            "last_name": "junior",
            "telefone": "99999999999",
            "cpf": "99999999999",
            "data_nascimento": "1997-01-01",
            "endereco": {
                "rua": "Rua rau ruau",
                "numero": "50",
                "complemento": "bloco 20",
                "cidade": "Belo horizonte",
                "estado": "Minas Gerais",
                "ponto_de_referencia": "Proximo ao aviário 101",
            },
        }
        self.funcionario = Conta.objects.create_user(**usuario_funcionario)

        usuario_comum = {
            "username": "patrick",
            "password": "1234",
            "first_name": "patrick",
            "last_name": "junior",
            "telefone": "99999999999",
            "cpf": "99999999999",
            "data_nascimento": "1999-01-01",
            "endereco": {
                "rua": "Rua sim",
                "numero": "50",
                "complemento": "bloco 50",
                "cidade": "Paraná",
                "estado": "Curitiba",
                "ponto_de_referencia": "Proximo ao kilão verduras frescas",
            },
        }
        self.comum = Conta.objects.create_user(**usuario_comum)

        produto_1 = {
            "preco": 9.00,
            "nome": "Requeijão Cremoso",
            "imagem": "requeijaocremoso.jpg",
            "descricao": "Saboroso e ótimo para acompanhar com pães fresquinhos",
        }
        """
        PRODUTO TEM QUE SER CRIADO, JUNTO COM O PRODUTO VEM A CATEGORIA.
        """

    def test_tentando_criar_uma_comanda(self):
        token = Token.objects.create(self.comum)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
        valores = {}
