import json
import logging
import os
from collections import OrderedDict
from typing import Optional

from rest_framework import status
from rest_framework.response import Response
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.viewsets import GenericViewSet, mixins
from rest_framework_simplejwt.tokens import AccessToken, OutstandingToken, RefreshToken, Token

from accounts.models import User
from core.exceptions.service_exceptions import InvalidRequest, UserNotFound
from core.middlewares import CustomJWTAuthentication

logger = logging.getLogger("django.server")


class LoggerMixin:
    __pid = os.getpid()

    def _get_formatted_string(
        self: GenericViewSet | Optional["LoggerMixin"], payload: OrderedDict | ReturnDict, _type: str, **kwargs
    ):
        return (
            f"[{_type.upper()}:{self.__pid}]:"
            + f"[{self.action}]:[{self.request._request.path}] - "
            + f"[{'HEADER' if _type == 'header' else 'PAYLOAD'}:{payload}]"
        )

    def header_logger(self: GenericViewSet | Optional["LoggerMixin"]):
        logger.info(self._get_formatted_string(self.request.headers, _type="header"))

    def request_logger(self, payload: OrderedDict = None):
        logger.info(self._get_formatted_string(payload, _type="request"))

    def response_logger(self: GenericViewSet | Optional["LoggerMixin"], payload: ReturnDict = None):
        if "list" in self.action:
            payload = json.loads(json.dumps(payload))
        elif not payload:
            pass
        else:
            payload = dict(payload)
        logger.info(self._get_formatted_string(payload, _type="response"))


class CreateModelMixin(mixins.CreateModelMixin, LoggerMixin):
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self: GenericViewSet | LoggerMixin, serializer):
        self.header_logger()
        self.request_logger(payload=self.request.data)
        serializer.save()
        self.response_logger(payload=serializer.validated_data)


class ListModelMixin(mixins.ListModelMixin, LoggerMixin):
    def list(self: GenericViewSet | LoggerMixin, request, *args, **kwargs):
        self.header_logger()
        self.request_logger(payload=request.query_params)
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            self.response_logger(payload=serializer.data)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        self.response_logger(payload=serializer.data)
        return Response(serializer.data)


class RetrieveModelMixin(mixins.RetrieveModelMixin, LoggerMixin):
    def retrieve(self: GenericViewSet | LoggerMixin, request, *args, **kwargs):
        self.header_logger()
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        self.response_logger(payload=serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateModelMixin(mixins.UpdateModelMixin, LoggerMixin):
    def perform_update(self: GenericViewSet | LoggerMixin, serializer):
        self.header_logger()
        self.request_logger(payload=self.request.data)
        serializer.save()
        self.response_logger(payload=serializer.data)

    def partial_update(self, request, *args, **kwargs):
        kwargs["partial"] = True
        return self.update(request, *args, **kwargs)


class DestroyModelMixin(mixins.DestroyModelMixin, LoggerMixin):
    def perform_destroy(self, instance):
        self.header_logger()
        self.request_logger(payload=instance)
        instance.delete()


class MappingViewSetMixin:
    serializer_class = None
    permission_classes = None

    serializer_action_map = {}
    permission_classes_map = {}

    def get_permissions(self: GenericViewSet | Optional["MappingViewSetMixin"]):
        permission_classes = self.permission_classes
        if not permission_classes:
            permission_classes = []
            if self.permission_classes_map.get(self.action, None):
                permission_classes.append(self.permission_classes_map[self.action])

        return [permission() for permission in permission_classes]

    def get_serializer_class(self: GenericViewSet | Optional["MappingViewSetMixin"]):
        if self.serializer_action_map.get(self.action, None):
            return self.serializer_action_map[self.action]
        return self.serializer_class


class TokenMixin:
    _access_token_class = AccessToken
    _refresh_token_class = RefreshToken

    @staticmethod
    def set_refresh_jti_into_access(refresh: RefreshToken) -> AccessToken:
        access: AccessToken = refresh.access_token
        access["refresh_jti"] = refresh.get("jti")

        return access

    @staticmethod
    def get_refresh_token_instance(filters: dict):
        return (
            OutstandingToken.objects.filter(**filters)
            .select_related("blacklistedtoken")
            .filter(blacklistedtoken__isnull=True)
            .first()
        )

    def is_active_user(self, _value: str = "", _value_type: str = "email"):
        """
        :param _value: str(Token) | str(EMAIL)
        :param _value_type: "access_token" | "refresh_token" | "email"

        :comment: User can have only one activated account.

        :return: True | False
        """
        user = self._get_users_object(_value, _value_type)
        if not user:
            raise UserNotFound
        return user.exists()

    @staticmethod
    def _get_users_object(_value: str | Token = "", _value_type: str = "email", token_verifying=False):
        if not _value:
            raise UserNotFound(message="유저를 특정할 정보를 찾을 수 없습니다.")

        _filters = {"id": None, "is_active": True}
        if _value_type == "email":
            user = User.objects.filter(email=_value, is_active=True).first()
            if not user:
                raise UserNotFound
            _filters["id"] = user.id
        elif _value_type == "access_token":
            _filters["id"] = AccessToken(_value, verify=token_verifying).get("user_id")
        elif _value_type == "refresh_token":
            _filters["id"] = RefreshToken(_value, verify=token_verifying).get("user_id")
        else:
            pass

        return User.objects.filter(**_filters)

    def invalid_user_handler(self, request, *args, **kwargs):
        if request.user.id != kwargs.get(self.lookup_field):
            raise InvalidRequest


class SimpleJWTMixin(CustomJWTAuthentication, TokenMixin):
    def get_raw_token(self, header: bytes) -> bytes | None:
        return super().get_raw_token(header)

    def get_user_instance(self, request, _type="access_token", token_verifying=False):
        access_token = self.get_raw_token(header=self.get_header(request))
        user = self._get_users_object(_value=access_token.decode(), _value_type=_type, token_verifying=token_verifying)
        if not user:
            raise UserNotFound
        return user.first()
