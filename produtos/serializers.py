from rest_framework import serializers
from categorias.models import Categoria
from produtos.models import Produto
from categorias.serializers import SerializerCategoriaProduto
from estoque.serializers import EstoqueSerializer
from estoque.models import Estoque


class ProdutoSerializer(serializers.ModelSerializer):
    estoque = EstoqueSerializer()
    categoria = SerializerCategoriaProduto()

    class Meta:
        model = Produto
        fields = [
            "id",
            "categoria",
            "preco",
            "nome",
            "imagem",
            "descricao",
            "estoque",
        ]
        read_only_fields = ["id"]

    def create(self, validated_data):
        dados_estoque = validated_data.pop("estoque")
        dados_categoria = validated_data.pop("categoria")

        categoria = Categoria.objects.get_or_create(**dados_categoria)[0]
        resultado_produto = Produto.objects.create(
            **validated_data, categoria=categoria
        )

        estoque = Estoque.objects.create(**dados_estoque, produto=resultado_produto)
        return resultado_produto

    def update(self, instance, validated_data: dict):
        cortando_categoria = validated_data.pop("categoria")
        cortando_estoque = validated_data.pop("estoque")
        if cortando_categoria:
            pegando_ou_criando = Categoria.objects.get_or_create(**cortando_categoria)[
                0
            ]
            instance.categoria = pegando_ou_criando
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance
