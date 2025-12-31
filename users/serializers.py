from rest_framework import serializers
from django.contrib.auth.models import  User

class UserSerializer(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        return user
    
class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta: # type: ignore
        model = User
        fields = ["password","first_name","last_name","username","email"]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)  
        user.save()
        return user

