from .models import Comments
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    root_comment = serializers.SerializerMethodField()
    user = serializers.ReadOnlyField(source="user.nickname")

    class Meta:
        model = Comments
        fields = ["id", "user", "recipe", "root", "text", "created_at", "root_comment"]

    def get_root_comment(self, instance):
        serializer = self.__class__(instance.root_comment, many=True)
        serializer.bind("", self)
        return serializer.data
