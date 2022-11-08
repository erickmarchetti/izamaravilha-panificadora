from categorias.models import Categoria

from produtos.models import Produto

from django.db.models.fields import UUIDField
from django.test import TestCase
import uuid


class CategoriaModelTest(TestCase):
    def test_se_os_atributos_da_model_estao_corretos(self):
        id = Categoria._meta.get_field("id")
        nome = Categoria._meta.get_field("nome")

        self.assertIs(id.get_internal_type(), UUIDField().get_internal_type())
        self.assertEqual(id.primary_key, True)
        self.assertEqual(id.default, uuid.uuid4)
        self.assertEqual(id.editable, False)
        self.assertEqual(nome.max_length, 20)
        self.assertEqual(nome.unique, True)

    def test_se_os_atributos_da_model_nao_sao_nulaveis(self):
        nome = Categoria._meta.get_field("nome")

        self.assertEqual(nome.null, False)
