from rest_framework import serializers
from categorias.models import Categoria
from produtos.models import Produto
from categorias.serializers import SerializerCategoriaProduto


class ProdutoSerializer(serializers.ModelSerializer):
    categoria = SerializerCategoriaProduto()
    produtosRecentes = serializers.SerializerMethodField(
        method_name="atualizar_pelo_mais_recente_produto"
    )

    class Meta:
        model = Produto
        fields = [
            "id",
            "categoria",
            "preco",
            "nome",
            "imagem",
            "descricao",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        dados = validated_data.pop("categoria")
        categoria = Categoria.objects.get_or_create(**dados)[0]
        resultado = Produto.objects.create(**validated_data, categoria=categoria)
        return resultado
