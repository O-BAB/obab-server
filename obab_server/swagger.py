from django.urls import path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator


class BothHttpAndHttpsSchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        schema = super().get_schema(request, public)
        schema.schemes = ["https", "http"]
        return schema


def get_swagger_urls():
    schema_view = get_schema_view(
        openapi.Info(
            title="Obab API",
            default_version="v1",
            description="Obab API 문서입니다.\n토큰 인증을 하실 때는 헤더에 'Token xxx' 형태로 액세스 토큰에 Token(Bearer) 접두사를 붙여주세요."
            "\n로컬에서 개발하실 때에는 하단의 HTTP 스키마를 선택해 주시고, 실제 서버에서는 HTTPS 스키마를 선택해 주세요.",
            terms_of_service="https://github.com/orgs/O-BAB/repositories",
        ),
        generator_class=BothHttpAndHttpsSchemaGenerator,
        validators=["flex"],
        public=True,
        permission_classes=[permissions.AllowAny],
    )

    return [
        path(
            "swagger.<str:format>",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        path(
            "swagger/",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        path(
            "redoc/",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
    ]
