import json
from copy import deepcopy

from rest_framework.exceptions import APIException
from rest_framework import status

from enum import Enum


class Contexts(Enum):
    code = 0
    message = 1

    @classmethod
    def get_members(cls):
        return cls.__members__.keys()

    @classmethod
    def get_context(cls, context):
        return cls.__getitem__(context).value


class CustomAPIException(APIException):
    """
    :comment: Default status code is `400`. If exception occurred, return JSON body value like;
              {
                "code": "UNKNOWN ERROR CODE",
                "message": "UNKNOWN MESSAGE DESCRIPTION"
              }
    """

    status_code = status.HTTP_400_BAD_REQUEST
    _msg = []
    _map = dict(
        code="UNKNOWN ERROR CODE",
        message="UNKNOWN MESSAGE DESCRIPTION",
    )

    def __init__(self, **kwargs):
        _detail_msg = deepcopy(self._msg) if self._msg else list()
        _detail_map = deepcopy(self._map)

        if kwargs:
            _detail_msg = self.get_updated_msg(items=kwargs.items(), msg=_detail_msg)

        for i, k in enumerate(_detail_map.keys()):
            _detail_map[k] = _detail_msg[i]

        # logger.error(_detail_map)
        self.detail = _detail_map

    def get_updated_msg(self, items, msg):
        """
        :param items: dict to items().
        :param msg: error message in list.

        :comment: if any `Context` in items, update it
                  * Context : `code` or `message` or `detail`
        """
        for k, v in items:
            if k in Contexts.get_members():
                msg[self._get_context_value(k)] = v
        return msg

    @staticmethod
    def _get_context_value(context):
        return Contexts.get_context(context)

    def get_error_messages(self):
        return json.dumps(self._msg, ensure_ascii=False)
