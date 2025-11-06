from rest_framework import serializers
from .models import Votes
from users.serializers import UserSerializer
class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votes
        fields = '__all__'
