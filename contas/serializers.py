from rest_framework import serializers
from enderecos.serializers import EnderecoResumidoSerializer
from enderecos.models import Endereco

from .models import Conta
from django.contrib.auth.hashers import make_password

from django.core.mail import send_mail
from django.conf import settings


class LoginSerializer(serializers.ModelSerializer):

    username = serializers.CharField()
    password = serializers.CharField()


class ContaClienteSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=256, write_only=True)
    endereco = EnderecoResumidoSerializer()
    is_active = serializers.BooleanField(default=False)

    class Meta:
        model = Conta
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "is_active",
            "pontos_de_fidelidade",
            "endereco",
        ]
        read_only_fields = [
            "id",
            "is_employee",
            "pontos_de_fidelidade",
        ]

    def create(self, validated_data):

        dados_endereco = validated_data.pop("endereco")
        dados_primeiro_nome = validated_data["first_name"]
        dados_ultimo_nome = validated_data["last_name"]

        usuario = Conta.objects.create_user(**validated_data)

        dado_secret_key = usuario.secret_key

        Endereco.objects.create(**dados_endereco, conta=usuario)

        send_mail(
            subject="NÃO RESPONDA - Confirmação de Conta Izamaravilha Panificadora",
            message=f"Olá {dados_primeiro_nome} {dados_ultimo_nome} seja bem-vindo(a) a Izamaravilha Panificadora, insira o código {dado_secret_key} e valide sua conta",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[validated_data["email"]],
            fail_silently=False,
        )

        return usuario


class ContaFuncionarioSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=256, write_only=True)
    endereco = EnderecoResumidoSerializer()

    class Meta:
        model = Conta
        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
            "endereco",
        ]
        read_only_fields = ["id", "is_employee", "pontos_de_fidelidade"]

    def create(self, validated_data):

        dados_endereco = validated_data.pop("endereco")

        usuario = Conta.objects.create_user(**validated_data, is_employee=True)

        Endereco.objects.create(**dados_endereco, conta=usuario)

        return usuario


class RecuperarDadosContaCompletaClienteFuncionarioSerializer(
    serializers.ModelSerializer
):

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = Conta
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
        ]
        read_only_fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
        ]


class AtualizarPropriaContaSerializer(serializers.ModelSerializer):

    id = serializers.UUIDField(read_only=True)
    password = serializers.CharField(max_length=256, write_only=True)

    class Meta:
        model = Conta
        fields = [
            "id",
            "username",
            "password",
            "first_name",
            "last_name",
            "telefone",
            "cpf",
            "data_nascimento",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
        ]
        read_only_fields = [
            "id",
            "cpf",
            "is_employee",
            "is_superuser",
            "pontos_de_fidelidade",
        ]

    def update(self, instance, validated_data):

        for key, value in validated_data.items():
            if key == "password":
                valor_alterado = make_password(value)
            else:
                valor_alterado = value

            setattr(instance, key, valor_alterado)

        instance.save()

        return instance


class VerificarConta(serializers.ModelSerializer):
    class Meta:
        model = Conta
        fields = ["is_active"]
        read_only_fields = ["id"]

    def update(self, instance, validated_data):

        token = validated_data.pop("secret_key")

        usuario = Conta.objects.filter(secret_key=token)[0]

        usuario.is_active = True

        usuario.save()

        return usuario
