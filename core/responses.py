from rest_framework.response import Response


from core.constants import SystemCodeManager


class CustomResponse(Response):

    def __init__(self, data=None, **kwargs):
        status = kwargs.get("status", 200)
        code = kwargs.pop("code", SystemCodeManager.get_message("base_code", "SUCCESS"))
        msg = kwargs.get("msg", code[1])

        payload = {
            "status_code": status,
            "msg": msg,
            "code": code[0],
            "data": data,
        }
        super().__init__(payload, **kwargs)


def Response(**kwargs):
    return CustomResponse(**kwargs)
