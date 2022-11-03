from rest_framework import serializers
from produtos.models import Produto


class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto
        fields = [
            "id",
            # "categoria_id",
            "preco",
            "nome",
            "imagem",
            "descricao",
        ]
        read_only_fields = ["id"]
