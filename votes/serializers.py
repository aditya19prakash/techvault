from rest_framework import serializers
from .models import Votes,Comments_votes
from users.serializers import UserSerializer
class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = '__all__'

class Comments_votes_Serializers(serializers.ModelSerializer):
    class Meta:
        model = Comments_votes
        fields = ["user","vote"]
