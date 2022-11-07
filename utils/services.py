from django.shortcuts import get_object_or_404

from produtos.models import Produto
from comandas.models import Comanda
from contas.models import Conta

from comandas.exceptions import ChaveChoiceInvalida

# Comanda
def verificacar_se_produto_tem_estoque(produto: Produto) -> Produto:
    ...


def pegar_ou_criar_comanda_mais_nova(dono_da_comanda: Conta) -> Comanda:
    lista_de_comandas_ordenadas = dono_da_comanda.comandas.order_by("-data_criacao")

    if (
        not lista_de_comandas_ordenadas
        or lista_de_comandas_ordenadas[0].status == "fechada"
    ):
        nova_comanda = Comanda.objects.create(conta=dono_da_comanda)
        return nova_comanda
    else:
        comanda_mais_nova = lista_de_comandas_ordenadas[0]

        return comanda_mais_nova


def listar_produtos_de_uma_comanda(comanda: Comanda):

    lista_de_produtos_na_comanda = [
        {
            "id": produto_na_comanda.produto.id,
            "nome": produto_na_comanda.produto.nome,
            "preco": produto_na_comanda.produto.preco,
            "quantidade": produto_na_comanda.quantidade,
        }
        for produto_na_comanda in comanda.comanda_produto.all()
    ]

    return lista_de_produtos_na_comanda


def verificar_status_comanda(
    instance: Comanda,
    validated_data: dict,
    dono_escolhas: list,
    funcionario_escolhas: list,
):
    conta_da_request = validated_data.pop("conta")

    if (
        conta_da_request == instance.conta
        and not validated_data["status"] in dono_escolhas
    ):
        raise ChaveChoiceInvalida(
            f"Dono da comanda tem acesso aos status: {dono_escolhas}"
        )
    elif (
        not conta_da_request == instance.conta
        and not validated_data["status"] in funcionario_escolhas
    ):
        raise ChaveChoiceInvalida(
            f"Funcionários tem acesso aos status: {funcionario_escolhas}"
        )
