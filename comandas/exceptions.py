from rest_framework.views import status
from rest_framework.exceptions import APIException


class RequestInvalida(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
