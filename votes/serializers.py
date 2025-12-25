from rest_framework import serializers
from .models import Resource_votes,Comments_votes
from users.serializers import UserSerializer
class VotesSerializer(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = Resource_votes
        fields = '__all__'

class Comments_votes_Serializers(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = Comments_votes
        fields = ["user","vote"]
