from django.test import TestCase

# Create your tests here.


from contas.models import Conta
from enderecos.models import Endereco


class ContaModelTeste(TestCase):
    @classmethod
    def setUpTestData(cls) -> Conta:

        cls.dados_conta = {
            "username": "bruno COMUM",
            "password": "1234",
            "email": "emailteste@email.com",
            "first_name": "Bruno",
            "last_name": "Tiberio",
            "telefone": "61992535393",
            "cpf": "17117117171",
            "data_nascimento": "1990-03-28",
            "endereco": {
                "rua": "Rua Azevedo",
                "numero": "4",
                "complemento": "Quandra 29",
                "cidade": "Luziânia",
                "estado": "Goiás",
                "ponto_de_referencia": "Proximo ao trem",
            },
        }

        cls.dados_endereco = cls.dados_conta.pop("endereco")

        cls.usuario = Conta.objects.create_user(**cls.dados_conta)

        cls.endereco = Endereco.objects.create(**cls.dados_endereco, conta=cls.usuario)

    def teste_de_propriedades_campos_model(self):
        """Verifica se os campos da model estão com as configurações corretas"""

        self.assertEqual(
            True,
            Conta._meta.get_field("id").primary_key,
            f'Verifique se a propriedade `primary_key` de "id" foi definida como True',
        )
        self.assertEqual(
            False,
            Conta._meta.get_field("id").editable,
            f'Verifique se a propriedade `editable` de "id" foi definida como False',
        )
        self.assertEqual(
            30,
            Conta._meta.get_field("username").max_length,
            f'Verifique se a propriedade `max_length` de "username" foi definida como 30',
        )
        self.assertEqual(
            True,
            Conta._meta.get_field("username").unique,
            f'Verifique se a propriedade `unique` de "username" foi definida como True',
        )

        self.assertEqual(
            True,
            Conta._meta.get_field("email").unique,
            f'Verifique se a propriedade `unique` de "email" foi definida como True',
        )
        self.assertEqual(
            90,
            Conta._meta.get_field("first_name").max_length,
            f'Verifique se a propriedade `max_length` de "first_name" foi definida como 90',
        )
        self.assertEqual(
            120,
            Conta._meta.get_field("last_name").max_length,
            f'Verifique se a propriedade `max_length` de "first_name" foi definida como 120',
        )
        self.assertEqual(
            False,
            Conta._meta.get_field("is_employee").default,
            f"Verifique se o campo foi definido com o valor default False",
        )
        self.assertEqual(
            11,
            Conta._meta.get_field("cpf").max_length,
            f'Verifique se a propriedade `max_length` de "first_name" foi definida como 11',
        )
        self.assertEqual(
            True,
            Conta._meta.get_field("cpf").unique,
            f'Verifique se a propriedade `unique` de "cpf" foi definida como True',
        )
        self.assertEqual(
            15,
            Conta._meta.get_field("telefone").max_length,
            f'Verifique se a propriedade `max_length` de "telefone" foi definida como 15',
        )
        self.assertEqual(
            0,
            Conta._meta.get_field("pontos_de_fidelidade").default,
            f'Verifique se a propriedade `max_length` de "pontos_de_fidelidade" foi definida como 0',
        )

    def teste_se_dados_estao_corretos_nos_campos(self):
        """Verifica se os dados passados nos campos são recebidos corretamente"""

        self.assertEqual(
            self.dados_conta["username"],
            self.usuario.username,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            self.dados_conta["email"],
            self.usuario.email,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            self.dados_conta["first_name"],
            self.usuario.first_name,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            self.dados_conta["last_name"],
            self.usuario.last_name,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            False,
            self.usuario.is_employee,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            self.dados_conta["data_nascimento"],
            self.usuario.data_nascimento,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            self.dados_conta["cpf"],
            self.usuario.cpf,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            self.dados_conta["telefone"],
            self.usuario.telefone,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            0,
            self.usuario.pontos_de_fidelidade,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            "Rua Azevedo",
            self.endereco.rua,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            "4",
            self.endereco.numero,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            "Quandra 29",
            self.endereco.complemento,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            "Luziânia",
            self.endereco.cidade,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            "Goiás",
            self.endereco.estado,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
        self.assertEqual(
            "Proximo ao trem",
            self.endereco.ponto_de_referencia,
            f"Verifique se todos os dados estão passando corretamente pela Model",
        )
