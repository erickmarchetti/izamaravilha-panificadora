from django.db.models.fields import UUIDField
from django.test import TestCase
import uuid

from contas.models import Conta
from enderecos.models import Endereco


class EnderecosModelTest(TestCase):
    def test_atributos_model(self):
        id = Endereco._meta.get_field("id")
        conta = Endereco._meta.get_field("conta")

        self.assertIs(type(id), UUIDField)
        self.assertEqual(id.primary_key, True)
        self.assertEqual(id.default, uuid.uuid4)
        self.assertEqual(id.editable, False)
        self.assertEqual(conta.related_model, Conta)
