from rest_framework.exceptions import APIException
from rest_framework.views import status


class ContaJaPossuiEnderecoCadastrado(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = "error"
    default_detail = "Essa conta já possui um endereço cadastrado."
