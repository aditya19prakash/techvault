from rest_framework import serializers
from .models import Resource
from aiservice.models import Ai_summary
from django.contrib.auth.models import  User

class UserResourceSerializer(serializers.ModelSerializer):
    class Meta:# type: ignore
        model = User
        fields = ["username"]

class Ai_summarySerializers(serializers.ModelSerializer):
    class Meta:# type: ignore
        model = Ai_summary
        fields = ["summary"]
        
class ResourceViewSerializer(serializers.ModelSerializer):
    user = UserResourceSerializer(read_only = True)
    class Meta:# type: ignore
        model = Resource
        fields = ["id", "title", "user", "views"]

class ResourcePostSerializer(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = Resource
        fields = ["id", "title", "url", "description", "category", "tech_stack", "user"]
     
class ResourceViewSerializerID(serializers.ModelSerializer):
    user = UserResourceSerializer(read_only = True)
    class Meta:# type: ignore
        model = Resource
        fields = ["id","title","url","description","category","tech_stack","user","views","created_at","updated_at"]

class ResourcePUTSerializerID(serializers.ModelSerializer):
    class Meta:# type: ignore
        model = Resource
        fields = ["title","url","description","category","tech_stack"]
        
class ResourceSignalsSerializerID(serializers.ModelSerializer):
    class Meta:# type: ignore
        model = Resource
        fields = ["title","url","description","category","tech_stack"]