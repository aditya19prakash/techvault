from rest_framework import serializers
from .models import Comment
class CommentsPOSTSerializer(serializers.ModelSerializer):
    class Meta:# type: ignore
        model = Comment
        fields = ["id","user","content","created_at","parent" ]

class CommentsGETSerializer(serializers.ModelSerializer):
    class Meta:# type: ignore
        model = Comment
        fields = ["id","created_at","content"]