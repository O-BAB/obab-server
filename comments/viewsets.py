from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, UpdateModelMixin, DestroyModelMixin
from drf_yasg.utils import swagger_auto_schema


from recipes.permissions import IsOwnerOrReadOnly
from .serializers import CommentSerializer
from accounts.functions import get_user_id


from .models import Comments


class CommentViewSet(
    CreateModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    queryset = Comments.objects.all()
    serializer_class = CommentSerializer

    def perform_create(self, serializer):
        serializer.save(user=get_user_id(self.request))

    @swagger_auto_schema(operation_id="댓글 생성", tags=["댓글"])
    def create(self, request, *args, **kwargs):
        """
        댓글 생성
        ---
        root는 대댓글을 달 부모 댓글id 입력
        일반 댓글의 경우 root에는 null값 전송
        """
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="댓글 전체 수정", tags=["댓글"])
    def update(self, request, *args, **kwargs):
        """
        댓글 전체 수정
        ---
        recipe는 본문의 id값
        모든 파라미터를 입력해서 보내주셔야합니다.
        """
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="댓글 부분 수정", tags=["댓글"])
    def partial_update(self, request, *args, **kwargs):
        """
        댓글 부분 수정
        ---
        recipe는 본문의 id값
        수정할 내용만 파라미터로 보내주시면 됩니다.
        """
        return super().partial_update(request, *args, **kwargs)

    @swagger_auto_schema(operation_id="댓글 삭제", tags=["댓글"])
    def destroy(self, request, *args, **kwargs):
        """
        댓글 삭제
        ---
        댓글 삭제
        """
        return super().destroy(request, *args, **kwargs)
