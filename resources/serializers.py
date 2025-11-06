from rest_framework import serializers
from .models import Resource
from users.models import User
from votes.serializers import VotesSerializer
class UserResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username"]


class ResourceViewSerializer(serializers.ModelSerializer):
    user = UserResourceSerializer(read_only = True)
    class Meta:
        model = Resource
        fields = ["id", "title", "user", "views"]


class ResourcePostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["id", "title", "url", "description", "category", "tech_stack", "user"]
     
class ResourceViewSerializerID(serializers.ModelSerializer):
    user = UserResourceSerializer(read_only = True)
    class Meta:
        model = Resource
        fields = ["id","title","url","description","category","tech_stack","user","views","created_at","updated_at"]

class ResourcePUTSerializerID(serializers.ModelSerializer):
    class Meta:
        model = Resource
        fields = ["title","url","description","category","tech_stack"]

        