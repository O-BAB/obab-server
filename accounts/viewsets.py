from rest_framework import status
from rest_framework.parsers import MultiPartParser
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from accounts.models import User
from comments.models import Comments
from comments.serializers import CommentSerializer
from core.exceptions.service_exceptions import UserIsNotAuthorized
from core.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    MappingViewSetMixin,
    RetrieveModelMixin,
    SimpleJWTMixin,
    UpdateModelMixin,
)
from recipes.models import FoodRecipes
from recipes.serializers import FoodRecipesListSerializer

from .serializers import (
    UserCreateSerializer,
    UserLoginSerializer,
    UserLogoutSerializer,
    UserPatchSerializer,
    UserSerializer,
)


class UserViewSet(
    CreateModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
    DestroyModelMixin,
    MappingViewSetMixin,
    SimpleJWTMixin,
    GenericViewSet,
):
    """
    :comment: User CRUD, Login & Join.
    """

    parser_classes = (MultiPartParser,)
    serializer_action_map = {
        "create": UserCreateSerializer,
        "retrieve": UserSerializer,
        "partial_update": UserPatchSerializer,
        "login": UserLoginSerializer,
        "logout": UserLogoutSerializer,
    }
    queryset = User.objects.filter(is_active=True, is_staff=False, is_superuser=False)

    def create(self, request, *args, **kwargs):
        """
        - 회원가입

        **Description**
        - 회원가입 시 사용하는 API입니다.
        """
        return super().create(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        - 유저 정보 조회

        **Description**
        - User Id에 해당하는 유저 정보를 가져옵니다.
        - User Id와 Access Token의 User 값이 동일해야 합니다.
        """
        self.invalid_user_handler(request, *args, **kwargs)
        return super().retrieve(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        - 유저 정보 업데이트

        **Description**
        - user Id를 이용하여 유저 정보를 업데이트 합니다.
        - User Id와 Access Token의 User 값이 동일해야 합니다.
        """
        self.invalid_user_handler(request, *args, **kwargs)
        return super().partial_update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        - 회원 탈퇴

        **Description**
        - 회원 탈퇴 API 입니다.
        - 회원 탈퇴 시 데이터를 삭제하지 않고, 비활성화됩니다.
        """
        self.invalid_user_handler(request, *args, **kwargs)
        return super().destroy(request, *args, **kwargs)

    def login(self, request, *args, **kwargs):
        """
        - 로그인(SNS 인증 데이터)

        **Description**
        - 로그인 시 사용하는 API입니다.
        - 로그인 시 USERNAME_FIELD, PASSWORD를 입력받아 인증합니다.
        - 인증 완료 후 access-token과 refresh-token을 발행해줍니다.
        """
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            raise UserIsNotAuthorized

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def logout(self, request, *args, **kwargs):
        """
        - 로그아웃

        **Description**
        - 로그아웃 시 사용하는 API입니다.
        - 만료되지 않은 access-token을 이용하여 정상적인 로그아웃이 가능합니다.
        - 만약 access-token과 refresh-token 매칭이 실패할 경우 만료된 토큰으로 간주하도록 합니다.
        """
        access_token = self.get_raw_token(self.get_header(request))
        access_token = self._access_token_class(access_token, verify=False)
        refresh_token_instance = self.get_refresh_token_instance(filters={"jti": access_token.get("refresh_jti")})
        serializer = self.get_serializer(data={"refresh": refresh_token_instance.token})
        serializer.is_valid()
        return Response(status=status.HTTP_204_NO_CONTENT)


class RecipeBookmarkList(SimpleJWTMixin, ListModelMixin, GenericViewSet):
    serializer_class = FoodRecipesListSerializer

    def get_queryset(self):
        user = self.get_user_instance(self.request)
        return FoodRecipes.objects.filter(bookmark=user)

    def list(self, request, *args, **kwargs):
        """
        - 북마크 목록

        **Description**
        - access-token을 이용하여 북마크 목록을 가지고 옵니다.
        """
        return super().list(request, *args, **kwargs)


class RecipeWriteList(SimpleJWTMixin, ListModelMixin, GenericViewSet):
    serializer_class = FoodRecipesListSerializer

    def get_queryset(self):
        user = self.get_user_instance(self.request)
        return FoodRecipes.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        """
        - 작성 글 목록

        **Description**
        - access-token을 이용하여 작성 글 목록을 가지고 옵니다.
        """
        return super().list(request, *args, **kwargs)


class RecipeCommentList(SimpleJWTMixin, ListModelMixin, GenericViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):
        user = self.get_user_instance(self.request)
        return Comments.objects.filter(user=user)

    def list(self, request, *args, **kwargs):
        """
        - 작성 댓글 목록

        **Description**
        - access-token을 이용하여 댓글 목록을 가지고 옵니다.
        """
        return super().list(request, *args, **kwargs)
