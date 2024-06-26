from django.shortcuts import get_object_or_404

from rest_framework.views import APIView
from rest_framework.response import Response
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from .serializers import CommentSerializer
from core.tokens import CustomJWTAuthentication
from core.permissions import IsOwnerOrReadOnly
from comments.models import Comments
from core.exceptions import raise_exception


class CommentCreateAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, comment_id):
        obj = Comments.objects.get(id=comment_id)
        self.check_object_permissions(self.request, obj)
        return obj
    
    @swagger_auto_schema(
        operation_id="댓글 생성", tags=["댓글"], request_body=CommentSerializer
    )
    def post(self, request):
        """
        댓글 생성
        """
        if request.data["root"] == 0:
            request.data["root"] = None
        serializer = CommentSerializer(data=request.data)
        user = CustomJWTAuthentication().authenticate(request)[0]
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(data=serializer.data)
        else:
            raise_exception(code=(0, serializer.errors))

class CommentUpdateDeleteAPIView(APIView):
    authentication_classes = [CustomJWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, comment_id):
        obj = Comments.objects.get(id=comment_id)
        self.check_object_permissions(self.request, obj)
        return obj

    @swagger_auto_schema(
        operation_id="댓글 수정",
        tags=["댓글"],
        request_body=CommentSerializer,
    )
    def put(self, request, *args, **kwargs):
        """
        댓글 수정
        """
        comment_id = kwargs.get('id')
        if request.data["root"] == 0:
            request.data["root"] = None
        if not comment_id:
            return Response({"message": "ID가 필요합니다."})

        try:
            comment = self.get_object(comment_id)
        except Comments.DoesNotExist:
            return Response({"message": "댓글을 찾을 수 없습니다."})

        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            raise_exception(code=(0, serializer.errors))

    @swagger_auto_schema(
        operation_id="댓글 삭제",
        tags=["댓글"],
    )
    def delete(self, request, *args, **kwargs):
        """
        댓글 삭제
        """
        comment_id = kwargs.get('id')

        try:
            comment = self.get_object(comment_id)
            comment.delete()
            return Response(data={"message": "성공적으로 삭제"})
        except Comments.DoesNotExist:
            return Response(data={"message": "댓글을 찾을 수 없습니다."})
