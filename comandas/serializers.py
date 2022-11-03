from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.core.validators import MinValueValidator
from django.shortcuts import get_object_or_404

from comandas.models import Comanda, Comanda_Produto
from contas.models import Conta
from produtos.models import Produto

from utils.services import (
    pegar_ou_criar_comanda_mais_nova,
    verificacar_se_produto_tem_estoque,
    listar_produtos_de_uma_comanda,
)


class AdicionarOuListarProdutoSerializer(serializers.ModelSerializer):
    produto_id = serializers.UUIDField(
        write_only=True,
        validators=[
            UniqueValidator(
                Comanda_Produto.objects.all(), "produto já adicionado a comanda"
            )
        ],
    )
    quantidade = serializers.IntegerField(
        write_only=True, validators=[MinValueValidator(1)]
    )
    produtos = serializers.SerializerMethodField(method_name="listar_produtos")

    class Meta:
        model = Comanda
        fields = [
            "id",
            "status",
            "data_criacao",
            "conta",
            "produto_id",
            "quantidade",
            "produtos",
        ]
        read_only_fields = ["id", "status", "data_criacao", "conta"]

    def listar_produtos(self, comanda: Comanda):
        return listar_produtos_de_uma_comanda(comanda)

    def create(self, validated_data):
        """
        TODO
        - verificar se o produto tem estoque sufuciente
        - verificar se o usuário tem endereço cadastrado
        """

        dono_comanda: Conta = validated_data["conta"]

        produto = get_object_or_404(Produto, id=validated_data["produto_id"])

        comanda_mais_nova = pegar_ou_criar_comanda_mais_nova(dono_comanda)

        comanda_mais_nova.comanda_produto.create(
            produto=produto,
            quantidade=validated_data["quantidade"],
        )

        return comanda_mais_nova


class EditarQuantidadeProdutoSerializer(serializers.ModelSerializer):
    quantidade = serializers.IntegerField(
        write_only=True, validators=[MinValueValidator(1)]
    )
    produtos = serializers.SerializerMethodField(method_name="listar_produtos")

    class Meta:
        model = Comanda
        fields = [
            "id",
            "status",
            "data_criacao",
            "conta",
            "quantidade",
            "produtos",
        ]
        read_only_fields = ["id", "status", "data_criacao", "conta"]

    def listar_produtos(self, comanda: Comanda):
        return listar_produtos_de_uma_comanda(comanda)

    def update(self, instance: Comanda_Produto, validated_data: dict):
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance.comanda


# class ListarProdutoSerializer(serializers.ModelSerializer):
#     produto_id = serializers.UUIDField(
#         write_only=True,
#         validators=[
#             UniqueValidator(
#                 Comanda_Produto.objects.all(), "produto já adicionado a comanda"
#             )
#         ],
#     )
#     quantidade = serializers.IntegerField(
#         write_only=True, validators=[MinValueValidator(1)]
#     )
#     produtos = serializers.SerializerMethodField(method_name="listar_produtos")

#     class Meta:
#         model = Comanda
#         fields = [
#             "id",
#             "status",
#             "data_criacao",
#             "conta",
#             "produto_id",
#             "quantidade",
#             "produtos",
#         ]
#         read_only_fields = ["id", "status", "data_criacao", "conta"]

#     def listar_produtos(self, comanda: Comanda):
#         return listar_produtos_de_uma_comanda(comanda)


class EditarProdutoSerializer(serializers.ModelSerializer):
    produto_id = serializers.UUIDField(
        write_only=True,
        validators=[
            UniqueValidator(
                Comanda_Produto.objects.all(), "produto já adicionado a comanda"
            )
        ],
    )
    quantidade = serializers.IntegerField(
        write_only=True, validators=[MinValueValidator(1)]
    )
    produtos = serializers.SerializerMethodField(method_name="listar_produtos")

    class Meta:
        model = Comanda
        fields = [
            "id",
            "status",
            "data_criacao",
            "conta",
            "produto_id",
            "quantidade",
            "produtos",
        ]
        read_only_fields = [
            "id",
            "data_criacao",
            "conta",
            "produto_id",
            "quantidade",
            "produtos",
        ]

    def listar_produtos(self, comanda: Comanda):
        return listar_produtos_de_uma_comanda(comanda)

    # def create(self, validated_data):
    #     """
    #     TODO
    #     - verificar se o produto tem estoque sufuciente
    #     - verificar se o usuário tem endereço cadastrado
    #     """

    #     dono_comanda: Conta = validated_data["conta"]

    #     produto = get_object_or_404(Produto, id=validated_data["produto_id"])

    #     comanda_mais_nova = pegar_ou_criar_comanda_mais_nova(dono_comanda)

    #     comanda_mais_nova.comanda_produto.create(
    #         produto=produto,
    #         quantidade=validated_data["quantidade"],
    #     )

    #     return comanda_mais_nova
