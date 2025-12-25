from rest_framework import serializers
from .models import Comment
class CommentsPOSTSerializer(serializers.ModelSerializer):
    class Meta:# type: ignore
        model = Comment
        fields = ["user","resource","comment" ]

class CommentsGETSerializer(serializers.ModelSerializer):
    class Meta:# type: ignore
        model = Comment
        fields = ["id","created_at","comment"]

class NestedCommentsSerializer(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = Comment
        fields = ["user","parent","resource","comment"]