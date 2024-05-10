from rest_framework import status
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

from core.constants import SystemCodeManager
from core.responses import Response


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)

    if isinstance(exc, CustomAPIException):
        return response
    if response is not None:
        response.data["status_code"] = response.status_code

    return Response(
        data={
            "code": SystemCodeManager.get_message("base_code", "UNKNOWN_SERVER_ERROR")
        },
        status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


class CustomAPIException(APIException):

    def __init__(self, **kwargs):
        self.status_code = kwargs.get("status", 400)
        self.code = kwargs.get(
            "code", SystemCodeManager.get_message("base_code", "BAD_REQUEST")
        )
        self.detail = self.code[1]


def raise_exception(**kwargs):
    raise CustomAPIException(**kwargs)
