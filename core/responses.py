from rest_framework.response import Response


class CustomResponse(Response):
    def __init__(self, data=None, **kwargs):
        status = kwargs.get("status", 200)
        code = kwargs.pop("code", (0, "SUCCESS"))
        msg = kwargs.get("msg", code[1])

        payload = {"status_code": status, "msg": msg, "code": code[0], "data": data}
        super().__init__(payload, **kwargs)


def Response(**kwargs):
    return CustomResponse(**kwargs)
